#!/usr/bin/env python3
"""Read-only RWA catalog and market-hours collector with sanitized DevEx logs."""

import argparse
import base64
import fcntl
import gzip
import hashlib
import hmac
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.server import NoRedirect, binance_credentials

BASE = "https://web3.binance.com/build"
PUBLIC_XSTOCKS = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=2"
TOKENS = "/api/v1/dex/market/rwa/tokens"
PRICE = "/api/v1/dex/market/rwa/price"
UNDERLYING_MARKET = "/api/v1/dex/market/rwa/underlying-market"
UNDERLYING_PROFILE = "/api/v1/dex/market/rwa/underlying-profile"
QUOTE = "/api/v1/dex/aggregator/quote"
SWAP_BUILD = "/api/v1/dex/aggregator/swap"
SIMULATE = "/api/v1/dex/pre-transaction/simulate"
TICKERS = {"AAPL", "NVDA", "TSLA", "COIN", "MSTR"}
CATALOG = ROOT / "data/normalized/rwa_catalog.json"
CATALOG_PARQUET = ROOT / "data/normalized/rwa_catalog.parquet"
XSTOCKS = ROOT / "data/normalized/xstocks_public.json"
DEVEX = ROOT / "docs/devex/raw"
MARKET = ROOT / "data/market_hours"
WEEKEND = ROOT / "data/weekend_2026-10-03_05"
RAW = MARKET / "raw"
CHECKPOINT = MARKET / "checkpoint.json"
HEARTBEAT = MARKET / "heartbeat.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def collecting_stalled(heartbeat, now_epoch, limit_seconds=90):
    if heartbeat.get("state") != "collecting":
        return False
    try:
        attempted = datetime.fromisoformat(heartbeat["last_attempt_at"].replace("Z", "+00:00"))
        return now_epoch - attempted.timestamp() > limit_seconds
    except (KeyError, AttributeError, ValueError, TypeError):
        return True


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def append_jsonl(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    line = (json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode()
    fd = os.open(str(path), os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o600)
    try:
        os.write(fd, line)
        os.fsync(fd)
    finally:
        os.close(fd)


def retain_raw(body, endpoint, captured_at, experiment, key, secret):
    if not body:
        return None
    if key.encode() in body or secret.encode() in body or b"X-OC-SIGN" in body:
        raise RuntimeError("raw response secret scan rejected body")
    digest = hashlib.sha256(body).hexdigest()
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / (digest + ".json.gz")
    if not target.exists():
        with tempfile.NamedTemporaryFile(dir=str(RAW), delete=False) as stream:
            temporary = Path(stream.name)
        try:
            with gzip.open(temporary, "wb") as stream:
                stream.write(body)
            os.replace(str(temporary), str(target))
        finally:
            temporary.unlink(missing_ok=True)
    append_jsonl(RAW / "manifest.jsonl", {"captured_at": captured_at, "endpoint": endpoint,
                 "experiment_id": experiment, "sha256": digest, "path": str(target.relative_to(ROOT)),
                 "origin": "LIVE"})
    return digest


def write_catalog_parquet(rows):
    sys.path.insert(0, str(ROOT / ".deps"))
    try:
        import duckdb
    except ImportError:
        return False
    CATALOG_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", dir=str(CATALOG_PARQUET.parent), delete=False, encoding="utf-8") as stream:
        source = Path(stream.name)
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    destination = CATALOG_PARQUET.with_suffix(".parquet.tmp")
    try:
        connection = duckdb.connect()
        source_sql = str(source).replace("'", "''")
        destination_sql = str(destination).replace("'", "''")
        connection.execute("COPY (SELECT * FROM read_json_auto('%s')) TO '%s' (FORMAT PARQUET)" % (source_sql, destination_sql))
        connection.close()
        os.replace(str(destination), str(CATALOG_PARQUET))
    finally:
        source.unlink(missing_ok=True)
        destination.unlink(missing_ok=True)
    return True


def safe_keys(payload):
    data = payload.get("data") if isinstance(payload, dict) else None
    first = data[0] if isinstance(data, list) and data else data
    return {
        "top_level": sorted(payload) if isinstance(payload, dict) else None,
        "data_type": type(data).__name__,
        "data_count": len(data) if isinstance(data, list) else None,
        "first_row_keys": sorted(first) if isinstance(first, dict) else None,
    }


class ApiError(RuntimeError):
    def __init__(self, message, http_status, business_code, retry_after=None):
        super().__init__(message)
        self.http_status = http_status
        self.business_code = business_code
        self.retry_after = retry_after


class Api:
    def __init__(self):
        auth = binance_credentials(ROOT)
        if auth is None:
            raise RuntimeError("missing Binance Web3 credentials in ignored .env")
        self.key, self.secret = auth

    def get(self, path, params, experiment, expected, context, allow_error=False):
        if path not in (TOKENS, PRICE, UNDERLYING_MARKET, UNDERLYING_PROFILE, QUOTE, SWAP_BUILD):
            raise ValueError("endpoint is outside the read-only allowlist")
        query = urlencode(params)
        timestamp = utc_now()
        signed_path = "/build" + path + ("?" + query if query else "")
        signature = base64.b64encode(hmac.new(
            self.secret.encode(), (timestamp + "GET" + signed_path).encode(), hashlib.sha256
        ).digest()).decode("ascii")
        request = Request(BASE + path + ("?" + query if query else ""), headers={
            "X-OC-APIKEY": self.key,
            "X-OC-TIMESTAMP": timestamp,
            "X-OC-SIGN": signature,
            "X-OC-NONCE": secrets.token_hex(16),
            "Accept": "application/json",
        }, method="GET")
        started = time.monotonic()
        status, body, error, retry_after = None, b"", None, None
        try:
            with build_opener(NoRedirect()).open(request, timeout=20) as response:
                status = response.status
                body = response.read(2_000_001)
        except HTTPError as exc:
            status = exc.code
            retry_after = exc.headers.get("Retry-After")
            body = exc.read(2_000_001)
        except (URLError, TimeoutError, OSError) as exc:
            error = type(exc).__name__
        received = utc_now()
        latency = round((time.monotonic() - started) * 1000, 2)
        payload = None
        if body and len(body) <= 2_000_000:
            try:
                payload = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                error = "invalid_json"
        elif len(body) > 2_000_000:
            error = "response_too_large"
        code = payload.get("code") if isinstance(payload, dict) else None
        expected_type = dict if path in (UNDERLYING_MARKET, UNDERLYING_PROFILE, SWAP_BUILD) else list
        valid = (status == 200 and code == 0 and isinstance(payload.get("data"), expected_type)) if isinstance(payload, dict) else False
        if not valid and error is None:
            error = "http_or_business_error" if status != 200 or code != 0 else "schema_mismatch"
        raw_hash = retain_raw(body, path, received, experiment, self.key, self.secret)
        record = {
            "timestamp": received, "endpoint": path, "method": "GET", "experiment_id": experiment,
            "expected_behavior": expected, "actual_behavior": "success" if valid else "failure",
            "latency_ms": latency, "http_status": status, "business_code": code if isinstance(code, int) else None,
            "sanitized_request": {k: v for k, v in params if k in ("binanceChainId", "platformId", "tokenContractAddress", "tokenContractAddresses", "fromTokenAddress", "toTokenAddress", "amount", "slippagePercent")},
            "sanitized_response": safe_keys(payload), "raw_response_sha256": raw_hash,
            "schema_mismatch": bool(status == 200 and code == 0 and not valid),
            "error": error, "edge_case": "missing_reference_timestamp" if valid and path in (PRICE, UNDERLYING_MARKET) else None,
            "workaround": None, "documentation_issue": "RWA response has no independent reference timestamp" if valid and path in (PRICE, UNDERLYING_MARKET) else None,
            "suggested_improvement": "Expose reference source and as-of timestamp separately" if valid and path in (PRICE, UNDERLYING_MARKET) else None,
            "market_context": context, "secret_scan": "allowlist_only_no_headers_or_raw_body",
        }
        serialized = json.dumps(record)
        if self.key in serialized or self.secret in serialized or "X-OC-SIGN" in serialized:
            raise RuntimeError("DevEx secret scan rejected record")
        append_jsonl(DEVEX / (received[:10] + ".jsonl"), record)
        if not valid and not allow_error:
            raise ApiError("API %s failed: HTTP %s, business %s, %s" % (path, status, code, error), status, code, retry_after)
        return payload if isinstance(payload, dict) else {}, received, raw_hash

    def post_simulation(self, body_obj, experiment, expected, context, allow_error=False):
        """Call only the documented off-chain simulation endpoint; never broadcast."""
        path = SIMULATE
        if body_obj.get("binanceChainId") != "56" or set(body_obj) != {"binanceChainId", "evmTx"}:
            raise ValueError("simulation request must contain BSC evmTx only")
        tx = body_obj["evmTx"]
        if not isinstance(tx, dict) or not all(tx.get(k) for k in ("from", "to", "data")):
            raise ValueError("simulation requires unsigned from, to and calldata")
        body = json.dumps(body_obj, separators=(",", ":"), ensure_ascii=False).encode()
        timestamp = utc_now()
        signature = base64.b64encode(hmac.new(
            self.secret.encode(), (timestamp + "POST" + "/build" + path).encode() + body,
            hashlib.sha256,
        ).digest()).decode("ascii")
        request = Request(BASE + path, data=body, headers={
            "X-OC-APIKEY": self.key, "X-OC-TIMESTAMP": timestamp,
            "X-OC-SIGN": signature, "X-OC-NONCE": secrets.token_hex(16),
            "Content-Type": "application/json", "Accept": "application/json",
        }, method="POST")
        started = time.monotonic()
        status, response_body, error, retry_after = None, b"", None, None
        try:
            with build_opener(NoRedirect()).open(request, timeout=20) as response:
                status, response_body = response.status, response.read(2_000_001)
        except HTTPError as exc:
            status, retry_after = exc.code, exc.headers.get("Retry-After")
            response_body = exc.read(2_000_001)
        except (URLError, TimeoutError, OSError) as exc:
            error = type(exc).__name__
        received = utc_now()
        payload = None
        if response_body and len(response_body) <= 2_000_000:
            try:
                payload = json.loads(response_body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                error = "invalid_json"
        elif len(response_body) > 2_000_000:
            error = "response_too_large"
        code = payload.get("code") if isinstance(payload, dict) else None
        valid = status == 200 and code == 0 and isinstance(payload.get("data"), dict) if isinstance(payload, dict) else False
        if not valid and error is None:
            error = "http_or_business_error" if status != 200 or code != 0 else "schema_mismatch"
        raw_hash = retain_raw(response_body, path, received, experiment, self.key, self.secret)
        record = {
            "timestamp": received, "endpoint": path, "method": "POST", "experiment_id": experiment,
            "expected_behavior": expected, "actual_behavior": "success" if valid else "failure",
            "latency_ms": round((time.monotonic() - started) * 1000, 2),
            "http_status": status, "business_code": code if isinstance(code, int) else None,
            "sanitized_request": {"binanceChainId": "56", "evmTx": {
                "to": tx["to"], "value": tx.get("value", "0"),
                "calldata_bytes": (len(tx["data"]) - 2) // 2,
                "calldata_sha256": hashlib.sha256(tx["data"].encode()).hexdigest()}},
            "sanitized_response": safe_keys(payload), "raw_response_sha256": raw_hash,
            "schema_mismatch": bool(status == 200 and code == 0 and not valid),
            "error": error, "edge_case": None, "workaround": None,
            "documentation_issue": None, "suggested_improvement": None,
            "market_context": context, "secret_scan": "allowlist_only_no_headers_or_calldata",
        }
        serialized = json.dumps(record)
        if self.key in serialized or self.secret in serialized or "X-OC-SIGN" in serialized:
            raise RuntimeError("DevEx secret scan rejected record")
        append_jsonl(DEVEX / (received[:10] + ".jsonl"), record)
        if not valid and not allow_error:
            raise ApiError("API %s failed: HTTP %s, business %s, %s" % (path, status, code, error), status, code, retry_after)
        return payload if isinstance(payload, dict) else {}, received, raw_hash

    def get_public_xstocks(self):
        started = time.monotonic()
        status, body, error = None, b"", None
        try:
            with build_opener(NoRedirect()).open(Request(PUBLIC_XSTOCKS, headers={"Accept": "application/json"}), timeout=20) as response:
                status, body = response.status, response.read(2_000_001)
        except HTTPError as exc:
            status, body = exc.code, exc.read(2_000_001)
        except (URLError, TimeoutError, OSError) as exc:
            error = type(exc).__name__
        at = utc_now()
        payload = None
        if body and len(body) <= 2_000_000:
            try:
                payload = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                error = "invalid_json"
        elif len(body) > 2_000_000:
            error = "response_too_large"
        append_jsonl(DEVEX / (at[:10] + ".jsonl"), {
            "timestamp": at, "endpoint": "/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai",
            "method": "GET", "experiment_id": "EXP-RWA-001", "expected_behavior": "public xStock candidate list",
            "actual_behavior": "success" if status == 200 and isinstance(payload, dict) else "failure",
            "latency_ms": round((time.monotonic() - started) * 1000, 2), "http_status": status,
            "sanitized_request": {"type": "2"}, "sanitized_response": safe_keys(payload),
            "raw_response_sha256": hashlib.sha256(body).hexdigest() if body else None,
            "schema_mismatch": status == 200 and not isinstance(payload, dict), "error": error,
            "market_context": "catalog", "secret_scan": "no_auth_headers_or_raw_body",
        })
        if status != 200 or not isinstance(payload, dict):
            raise RuntimeError("public xStock list failed: HTTP %s, %s" % (status, error))
        return payload, at, hashlib.sha256(body).hexdigest()


def normalize(item):
    if not isinstance(item, dict) or str(item.get("binanceChainId")) != "56":
        return None
    address = item.get("tokenContractAddress")
    if not isinstance(address, str) or len(address) != 42 or not address.startswith("0x"):
        return None
    status = item.get("statusInfo") if isinstance(item.get("statusInfo"), dict) else {}
    return {
        "source": "binance_web3_rwa_tokens", "chain_id": "56", "provider": item.get("platformId"),
        "ticker": item.get("underlyingTicker"), "underlying_name": item.get("underlyingName"),
        "asset_type": item.get("assetType"), "token_symbol": item.get("tokenSymbol"),
        "contract": address.lower(), "decimals": item.get("decimals"),
        "token_to_share_ratio": item.get("tokenToShareRatio"),
        "market_status": status.get("marketStatus"), "market_reason": status.get("reasonCode"),
        "token_price_usd": item.get("tokenPrice"), "derived_reference_price_usd": item.get("referencePrice"),
        "issuer": None, "corporate_action_metadata": status.get("reasonMsg"),
        "attestation_data": None, "independent_reference_timestamp": None,
    }


def normalize_xstock(item):
    if not isinstance(item, dict) or str(item.get("chainId")) != "56":
        return None
    address = item.get("contractAddress")
    if not isinstance(address, str) or len(address) != 42 or not address.startswith("0x"):
        return None
    return {
        "source": "binance_public_stock_list_type_2", "chain_id": "56", "provider": "xstocks_public_listing",
        "ticker": item.get("ticker"), "underlying_name": None, "asset_type": item.get("assetType"),
        "token_symbol": item.get("symbol"), "contract": address.lower(), "decimals": item.get("d"),
        "token_to_share_ratio": None, "listed_multiplier_raw": item.get("multiplier"),
        "ratio_status": "unverified_public_multiplier_semantics", "market_status": None,
        "market_reason": None, "token_price_usd": None, "derived_reference_price_usd": None,
        "issuer": None, "corporate_action_metadata": None, "attestation_data": None,
        "independent_reference_timestamp": None,
    }


def xstocks_catalog(api):
    payload, at, raw_hash = api.get_public_xstocks()
    data = payload.get("data")
    if not isinstance(data, list):
        raise RuntimeError("public xStock list has no array data")
    rows = [row for item in data if (row := normalize_xstock(item)) is not None]
    result = {"captured_at": at, "origin": "LIVE", "endpoint": PUBLIC_XSTOCKS,
              "raw_response_sha256": raw_hash,
              "coverage": "Public Binance website listing only; no signed RWA price or executable route established",
              "rows": rows}
    write_json(XSTOCKS, result)
    return result


def catalog(api, persist=True):
    payload, at, raw_hash = api.get(TOKENS, [("binanceChainId", "56")], "EXP-RWA-001",
                          "BSC RWA token list with contract, ratio and status", "catalog")
    rows = [row for item in payload["data"] if (row := normalize(item)) is not None]
    xstocks_source = None
    if XSTOCKS.exists():
        extra = json.loads(XSTOCKS.read_text(encoding="utf-8"))
        rows.extend(extra.get("rows", []))
        xstocks_source = {"captured_at": extra.get("captured_at"), "raw_response_sha256": extra.get("raw_response_sha256")}
    rows.sort(key=lambda row: (str(row["ticker"]), str(row["provider"]), row["contract"]))
    result = {
        "captured_at": at, "origin": "LIVE", "endpoint": TOKENS,
        "source_url": "https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data",
        "coverage": "BSC 56. bStock and Ondo from signed Binance Web3 RWA API; xStocks from separate public Binance website list when present. Public listings do not prove a signed RWA route.",
        "xstocks_public_source": xstocks_source,
        "raw_response_sha256": raw_hash,
        "rows": rows,
    }
    if persist:
        write_json(CATALOG, result)
        write_catalog_parquet(rows)
    else:
        write_json(MARKET / "catalog_latest.json", result)
    return result


def existing_ids(path):
    if not path.exists():
        return set()
    ids = set()
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                value = json.loads(line)
                if value.get("sample_id"):
                    ids.add(value["sample_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return ids


def observation_count():
    return sum(len(existing_ids(path)) for path in MARKET.glob("20??-??-??.jsonl"))


def collect_once(api, interval):
    now = datetime.now(timezone.utc)
    slot = int(now.timestamp()) // interval
    context = "weekend" if now.weekday() >= 5 else "weekday"
    last_success = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
    write_json(HEARTBEAT, {"updated_at": utc_now(), "state": "collecting", "pid": os.getpid(),
                           "last_attempt_at": utc_now(), "last_success_at": last_success.get("last_success_at"),
                           "consecutive_failures": 0, "observation_count": last_success.get("observation_count", observation_count()),
                           "contracts_sampled": last_success.get("contracts_sampled", 0),
                           "next_due_at_epoch": (slot + 1) * interval})
    previous_slot = None
    heartbeat_path = CHECKPOINT
    if heartbeat_path.exists():
        try:
            previous_slot = json.loads(heartbeat_path.read_text(encoding="utf-8")).get("last_success_slot")
        except (OSError, json.JSONDecodeError):
            pass
    catalog_state = catalog(api, persist=False)
    chosen = [row for row in catalog_state["rows"] if row["asset_type"] == 1 and
              (row["provider"] == "bstock" or (row["provider"] == "ondo" and row["ticker"] in TICKERS))]
    addresses = sorted({row["contract"] for row in chosen})
    if not addresses:
        raise RuntimeError("catalog returned no selected BSC stock contracts")
    prices = {}
    price_hashes = {}
    for offset in range(0, len(addresses), 100):
        payload, _, raw_hash = api.get(PRICE, [("binanceChainId", "56"), ("tokenContractAddresses", ",".join(addresses[offset:offset + 100]))],
                             "EXP-RWA-003/004/010", "prices with tokenPriceUpdatedAt", context)
        for value in payload["data"]:
            if isinstance(value, dict):
                address = str(value.get("tokenContractAddress", "")).lower()
                prices[address] = value
                price_hashes[address] = raw_hash
    day = now.strftime("%Y-%m-%d")
    target = MARKET / (day + ".jsonl")
    seen = existing_ids(target)
    weekend_target = WEEKEND / (day + ".jsonl") if "2026-10-03" <= day <= "2026-10-05" else None
    weekend_seen = existing_ids(weekend_target) if weekend_target else set()
    recorded = 0
    for row in chosen:
        price = prices.get(row["contract"], {})
        updated = price.get("tokenPriceUpdatedAt")
        observed_at = utc_now()
        observed_ms = int(datetime.fromisoformat(observed_at.replace("Z", "+00:00")).timestamp() * 1000)
        age = observed_ms - updated if isinstance(updated, int) and updated > 0 else None
        sample_id = hashlib.sha256((str(slot) + row["contract"]).encode()).hexdigest()[:24]
        if sample_id in seen and (weekend_target is None or sample_id in weekend_seen):
            continue
        sample = {
            "sample_id": sample_id, "origin": "LIVE", "observed_at": observed_at, "slot": slot,
            "experiment_ids": ["EXP-RWA-003", "EXP-RWA-004", "EXP-RWA-010"],
            "chain_id": "56", "provider": row["provider"], "ticker": row["ticker"],
            "contract": row["contract"], "token_to_share_ratio": row["token_to_share_ratio"],
            "market_status": row["market_status"], "market_reason": row["market_reason"],
            "token_price_usd": price.get("tokenPrice"),
            "derived_reference_price_usd": price.get("referencePrice"),
            "token_price_updated_at": updated, "token_price_updated_at_ms": updated, "token_price_age_ms": age,
            "token_price_age_status": "UNKNOWN" if age is None else ("FUTURE_TIMESTAMP" if age < 0 else "OBSERVED"),
            "token_price_age_calculation": "observed_at_minus_tokenPriceUpdatedAt",
            "reference_price_updated_at": None, "reference_age_seconds": None,
            "reference_age_status": "UNKNOWN",
            "independent_reference_timestamp": None, "independent_reference_age_ms": None,
            "dex_quote": None, "liquidity": None, "slippage": None,
            "source": "binance_web3_rwa_tokens_and_price",
            "catalog_sha256": catalog_state["raw_response_sha256"],
            "price_response_sha256": price_hashes.get(row["contract"]),
        }
        if sample_id not in seen:
            append_jsonl(target, sample)
        if weekend_target and sample_id not in weekend_seen:
            append_jsonl(weekend_target, sample)
        recorded += 1
    missed_slots = max(0, slot - previous_slot - 1) if isinstance(previous_slot, int) else None
    if missed_slots:
        append_jsonl(MARKET / "gaps.jsonl", {"observed_at": utc_now(), "previous_slot": previous_slot,
                                            "current_slot": slot, "missed_slots": missed_slots, "origin": "COLLECTOR_GAP"})
    checkpoint = {"last_success_at": utc_now(), "last_success_slot": slot,
                  "observation_count": observation_count(),
                  "contracts_sampled": len(chosen), "interval_seconds": interval}
    write_json(CHECKPOINT, checkpoint)
    heartbeat = {"updated_at": utc_now(), "state": "running", "last_slot": slot,
                 "last_attempt_at": utc_now(), "last_success_at": checkpoint["last_success_at"],
                 "consecutive_failures": 0, "observation_count": checkpoint["observation_count"],
                 "contracts_sampled": len(chosen), "selected_contracts": len(chosen), "recorded_this_cycle": recorded,
                 "missed_slots_since_previous": missed_slots,
                 "last_error": None, "next_due_at_epoch": (slot + 1) * interval}
    write_json(HEARTBEAT, heartbeat)
    print(json.dumps(heartbeat), flush=True)
    return heartbeat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("catalog", "once", "loop", "start", "underlying-probe", "profile-probe", "xstocks", "xstocks-shape", "health"))
    parser.add_argument("--interval", type=int, default=300, help="Sampling interval in seconds, minimum 60")
    parser.add_argument("--keep-awake", action="store_true", help="On macOS, prevent system sleep while the detached collector runs")
    args = parser.parse_args()
    if args.interval < 60:
        parser.error("interval must be at least 60 seconds")
    if args.command == "health":
        heartbeat = json.loads(HEARTBEAT.read_text(encoding="utf-8")) if HEARTBEAT.exists() else {}
        checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
        pid_path = MARKET / "collector.pid"
        pid = int(pid_path.read_text()) if pid_path.exists() else None
        alive = False
        if pid:
            try:
                os.kill(pid, 0)
                alive = True
            except OSError:
                pass
        now = time.time()
        due = heartbeat.get("next_due_at_epoch")
        overdue = bool(due and now > due + 60)
        stalled = collecting_stalled(heartbeat, now)
        print(json.dumps({"process_alive": alive, "pid": pid,
                          "last_success_at": checkpoint.get("last_success_at") or heartbeat.get("last_success_at"),
                          "last_attempt_at": heartbeat.get("last_attempt_at") or heartbeat.get("updated_at"),
                          "consecutive_failures": heartbeat.get("consecutive_failures", 0),
                          "observation_count": checkpoint.get("observation_count"),
                          "contracts_sampled": checkpoint.get("contracts_sampled") or heartbeat.get("selected_contracts"),
                          "next_expected_run": datetime.fromtimestamp(due, timezone.utc).isoformat() if due else None,
                          "overdue": overdue, "collecting_stalled": stalled, "state": heartbeat.get("state")}))
        if not alive or overdue or stalled or heartbeat.get("consecutive_failures", 0) > 0:
            raise SystemExit(1)
        return
    if args.command == "start":
        MARKET.mkdir(parents=True, exist_ok=True)
        pid_path = MARKET / "collector.pid"
        if pid_path.exists():
            try:
                os.kill(int(pid_path.read_text()), 0)
                raise SystemExit("collector already has a live PID")
            except ProcessLookupError:
                pass
        with (MARKET / "collector.log").open("a", encoding="utf-8") as log:
            process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "loop", "--interval", str(args.interval)],
                                       cwd=str(ROOT), stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
        if args.keep_awake and sys.platform == "darwin":
            with (MARKET / "caffeinate.log").open("a", encoding="utf-8") as log:
                keeper = subprocess.Popen(["/usr/bin/caffeinate", "-s", "-w", str(process.pid)],
                                          stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                          start_new_session=True)
            (MARKET / "caffeinate.pid").write_text(str(keeper.pid) + "\n", encoding="utf-8")
        print(json.dumps({"started_pid": process.pid, "interval_seconds": args.interval,
                          "keep_awake": bool(args.keep_awake and sys.platform == "darwin"),
                          "health_command": "python3 scripts/rwa_research.py health"}))
        return
    api = Api()
    if args.command == "xstocks-shape":
        payload, at, digest = api.get_public_xstocks()
        data = payload.get("data")
        examples = [{k: row.get(k) for k in ("chainId", "contractAddress", "symbol", "ticker", "d", "multiplier", "assetType", "lastUpdateTime")}
                    for row in data if isinstance(row, dict) and str(row.get("chainId")) == "56"][:3] if isinstance(data, list) else []
        print(json.dumps({"captured_at": at, "hash": digest, "shape": safe_keys(payload),
                          "examples": examples}))
    elif args.command == "xstocks":
        result = xstocks_catalog(api)
        catalog_result = catalog(api)
        print(json.dumps({"xstocks_captured_at": result["captured_at"], "xstocks_bsc_rows": len(result["rows"]),
                          "merged_bsc_rows": len(catalog_result["rows"])}))
    elif args.command == "catalog":
        result = catalog(api)
        print(json.dumps({"captured_at": result["captured_at"], "rows": len(result["rows"])}))
    elif args.command == "underlying-probe":
        rows = json.loads(CATALOG.read_text(encoding="utf-8"))["rows"]
        targets = [row for row in rows if row["ticker"] == "NVDA" and row["provider"] in ("bstock", "ondo")]
        for row in targets:
            payload, at, digest = api.get(UNDERLYING_MARKET,
                [("binanceChainId", "56"), ("tokenContractAddress", row["contract"])],
                "EXP-RWA-010", "underlying market data and any independent reference timestamp", "weekend_probe")
            data = payload.get("data") or {}
            market_data = data.get("marketData") or {}
            print(json.dumps({"captured_at": at, "provider": row["provider"], "ticker": row["ticker"],
                              "raw_response_sha256": digest, "data_keys": sorted(data),
                              "market_data_keys": sorted(market_data), "status_info": data.get("statusInfo"),
                              "candidate_timestamp_fields": {k: v for k, v in market_data.items() if "time" in k.lower() or "updated" in k.lower()}}))
    elif args.command == "profile-probe":
        rows = json.loads(CATALOG.read_text(encoding="utf-8"))["rows"]
        targets = [row for row in rows if row["ticker"] in ("CRWD", "NFLX") and row["provider"] == "ondo"]
        if len(targets) != 2:
            raise RuntimeError("expected exactly two issuer-event profile targets")
        summaries = []
        for row in targets:
            payload, at, digest = api.get(UNDERLYING_PROFILE,
                [("binanceChainId", "56"), ("tokenContractAddress", row["contract"])],
                "EXP-RWA-011", "underlying profile and any dated corporate action fields", "event_profile_probe")
            data = payload["data"]
            protections = data.get("protections") or {}
            summaries.append({"captured_at": at, "ticker": row["ticker"], "contract": row["contract"],
                              "raw_response_sha256": digest, "data_keys": sorted(data),
                              "protection_keys": sorted(protections), "token_to_share_ratio": data.get("tokenToShareRatio"),
                              "candidate_event_or_reference_time_fields": {k: v for k, v in data.items()
                                                                            if any(word in k.lower() for word in ("action", "event", "updated", "timestamp", "reference"))}})
        output = ROOT / "experiments/EXP-RWA-011/profile_probe.json"
        write_json(output, {"origin": "LIVE", "endpoint": UNDERLYING_PROFILE, "summaries": summaries,
                            "claim_limit": "Profile fields are a snapshot; no historical ratio change is proved."})
        print(json.dumps({"profiles": len(summaries), "output": str(output.relative_to(ROOT)),
                          "data_keys": {x["ticker"]: x["data_keys"] for x in summaries}}))
    elif args.command == "once":
        collect_once(api, args.interval)
    else:
        MARKET.mkdir(parents=True, exist_ok=True)
        lock_fd = os.open(str(MARKET / "collector.lock"), os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit("collector already running")
        (MARKET / "collector.pid").write_text(str(os.getpid()) + "\n", encoding="utf-8")
        failures = 0
        while True:
            try:
                collect_once(api, args.interval)
                failures = 0
                delay = max(1, (int(time.time()) // args.interval + 1) * args.interval - time.time())
            except Exception as exc:
                failures += 1
                delay = min(3600, args.interval * 2 ** min(failures - 1, 4))
                if isinstance(exc, ApiError) and (exc.http_status == 429 or exc.business_code in (429, 42900)):
                    delay = max(900, delay)
                    if exc.retry_after and exc.retry_after.isdigit():
                        delay = max(delay, min(3600, int(exc.retry_after)))
                prior = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
                write_json(HEARTBEAT, {"updated_at": utc_now(), "state": "retrying", "pid": os.getpid(),
                           "last_attempt_at": utc_now(), "last_success_at": prior.get("last_success_at"),
                           "consecutive_failures": failures, "observation_count": prior.get("observation_count", 0),
                           "contracts_sampled": prior.get("contracts_sampled", 0),
                           "last_error": str(exc)[:160], "next_due_at_epoch": int(time.time() + delay)})
                append_jsonl(MARKET / "errors.jsonl", {"at": utc_now(), "error_type": type(exc).__name__,
                                                      "message": str(exc)[:160], "consecutive_failures": failures,
                                                      "retry_seconds": delay})
                print(json.dumps({"state": "retrying", "error": str(exc)[:160]}), flush=True)
            time.sleep(delay)


if __name__ == "__main__":
    main()
