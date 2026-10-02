#!/usr/bin/env python3
"""Read-only, market-level Venus scenario server. Python 3.9 standard library only."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import base64
import hashlib
import hmac
import os
import re
import secrets
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse, parse_qs
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

getcontext().prec = 36
API_URL = "https://api.venus.io/markets?chainId=56&limit=100"
RPC_URL = "https://bsc-dataseed.bnbchain.org"
BINANCE_BASE = "https://web3.binance.com/build"
BINANCE_PATH = "/build/api/v1/dex/aggregator/quote"
RWA_SEARCH_PATH = "/api/v1/dex/market/rwa/search"
CHAIN = "56"
NVDAB = "0x02fca66c1d1afb4e2a7884261eb00f63598a7436"
USDT = "0x55d398326f99059ff775485246999027b3197955"
CORE_UNITROLLER = "0xfd36e2c2a6789db23113685031d7f16329158384"
CORE_GET_ASSETS_IN_SELECTOR = "abfceffc"
CORE_USER_POOL_ID_SELECTOR = "73769099"
MAX_CORE_ENTERED_MARKETS = 64
ZERO = Decimal("0")
MAX_INPUT = Decimal("1000000000000000")
MIN_INPUT = Decimal("0.000000000000000001")
SECRET_NAMES = ("BINANCE_WEB3_API_KEY", "BINANCE_WEB3_SECRET_KEY")
MAX_QUOTE_RESPONSE_BYTES = 1048576
BINANCE_ERROR_LABELS = {
    40001: "invalid_request_parameters", 40101: "invalid_or_disabled_api_key",
    40102: "signature_mismatch_or_missing", 40103: "timestamp_expired_or_replayed_request",
    40104: "api_key_permission_missing", 40301: "region_restricted", 40302: "vpn_restricted",
    40303: "unusual_ip", 40366: "ondo_order_above_vendor_maximum",
    40365: "ondo_token_pair_not_supported", 40367: "ondo_underlying_market_not_tradable", 40368: "ondo_stablecoin_pair_not_supported",
    40369: "bstock_underlying_market_not_tradable", 40370: "bstock_pair_not_supported",
    40374: "rwa_no_vendor_liquidity", 40375: "ondo_order_below_usd_minimum",
    42900: "rate_limit_exceeded", 50000: "internal_server_error",
    50001: "service_temporarily_unavailable", 40411: "chain_not_supported",
    40421: "insufficient_pair_liquidity",
    40441: "no_valid_vendor_quote",
    40442: "same_tokens",
}


class ScenarioError(Exception):
    def __init__(self, field, message):
        self.field, self.message = field, message


def decimal_input(value, field):
    try:
        number = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ScenarioError(field, "Enter a valid number.")
    if not number.is_finite() or number <= ZERO:
        raise ScenarioError(field, "Enter an amount greater than zero.")
    if number < MIN_INPUT or number > MAX_INPUT:
        raise ScenarioError(field, "Use an amount from 0.000000000000000001 to 1,000,000,000,000,000.")
    if number.as_tuple().exponent < -18:
        raise ScenarioError(field, "Use no more than 18 decimal places.")
    return number


def fetch_markets():
    request = Request(API_URL, headers={"User-Agent": "Dyplux-Venus-Scenario/0.1 (read-only)", "accept-version": "next"})
    with urlopen(request, timeout=12) as response:
        if response.status != 200:
            raise RuntimeError("Venus API returned HTTP %s." % response.status)
        return json.loads(response.read().decode("utf-8"))


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    request = Request(RPC_URL, data=body, headers={"Content-Type": "application/json", "User-Agent": "Dyplux-NVDAB-Balance/0.1 (read-only)"})
    try:
        with urlopen(request, timeout=12) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError("BNB Chain RPC request failed.") from exc
    if not isinstance(payload, dict) or payload.get("error") or "result" not in payload:
        raise RuntimeError("BNB Chain RPC returned no usable result.")
    return payload["result"]


def read_wallet_balance(wallet, units):
    chain_id = rpc("eth_chainId", [])
    if not isinstance(chain_id, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", chain_id) or int(chain_id, 16) != 56:
        raise RuntimeError("RPC endpoint did not confirm BNB Smart Chain mainnet (chain 56).")
    block_hex = rpc("eth_blockNumber", [])
    if not isinstance(block_hex, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", block_hex):
        raise RuntimeError("BNB Chain RPC returned an invalid block number.")
    block_number = int(block_hex, 16)
    block_tag = hex(block_number)
    code = rpc("eth_getCode", ["0x" + NVDAB[2:], block_tag])
    if not isinstance(code, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", code) or code == "0x" or int(code[2:] or "0", 16) == 0:
        raise RuntimeError("NVDAB contract code was unavailable at the recorded block.")
    decimals_word = rpc("eth_call", [{"to": "0x" + NVDAB[2:], "data": "0x313ce567"}, block_tag])
    if not isinstance(decimals_word, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", decimals_word):
        raise RuntimeError("NVDAB decimals metadata was unavailable at the recorded block.")
    decimals = int(decimals_word, 16)
    if decimals != 18:
        raise RuntimeError("NVDAB contract metadata did not report 18 decimals.")
    call_data = "0x70a08231" + wallet[2:].lower().rjust(64, "0")
    balance_word = rpc("eth_call", [{"to": "0x" + NVDAB[2:], "data": call_data}, block_tag])
    if not isinstance(balance_word, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", balance_word):
        raise RuntimeError("NVDAB balance result was unavailable at the recorded block.")
    block = rpc("eth_getBlockByNumber", [block_tag, False])
    if not isinstance(block, dict) or not isinstance(block.get("timestamp"), str) or not re.fullmatch(r"0x[0-9a-fA-F]+", block["timestamp"]):
        raise RuntimeError("BNB Chain RPC returned no timestamp for the recorded block.")
    balance_raw = int(balance_word, 16)
    balance_integer, balance_fraction = divmod(balance_raw, 10 ** decimals)
    balance = str(balance_integer)
    if balance_fraction:
        balance += "." + str(balance_fraction).rjust(decimals, "0").rstrip("0")
    return {
        "chain_id": 56,
        "block_number": block_number,
        "block_tag": block_tag,
        "block_time_utc": datetime.fromtimestamp(int(block["timestamp"], 16), timezone.utc).isoformat(timespec="seconds"),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "balance_nvdab": balance,
        "entered_units": str(units),
        "units_sufficient": balance_raw >= int(units * (Decimal(10) ** decimals)),
        "token_decimals": decimals,
        "rpc_source": RPC_URL,
        "metadata_note": "NVDAB contract code and decimals() were read at this block; decimals reported 18."
    }


def read_venus_core_account_state(wallet):
    chain_id = rpc("eth_chainId", [])
    if not isinstance(chain_id, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", chain_id) or int(chain_id, 16) != 56:
        raise RuntimeError("RPC endpoint did not confirm BNB Smart Chain mainnet (chain 56).")
    block_hex = rpc("eth_blockNumber", [])
    if not isinstance(block_hex, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", block_hex):
        raise RuntimeError("BNB Chain RPC returned an invalid block number.")
    block_number = int(block_hex, 16)
    if block_number <= 0 or block_number.bit_length() > 256:
        raise RuntimeError("BNB Chain RPC returned an invalid block number.")
    block_tag = hex(block_number)
    unitroller_code = rpc("eth_getCode", ["0x" + CORE_UNITROLLER[2:], block_tag])
    if (not isinstance(unitroller_code, str) or not re.fullmatch(r"0x[0-9a-fA-F]*", unitroller_code)
            or len(unitroller_code) <= 2 or int(unitroller_code[2:] or "0", 16) == 0):
        raise RuntimeError("Venus Core Unitroller code was unavailable at the recorded block.")

    address_word = wallet[2:].lower().rjust(64, "0")
    entered_call = "0x" + CORE_GET_ASSETS_IN_SELECTOR + address_word
    entered_result = rpc("eth_call", [{"to": "0x" + CORE_UNITROLLER[2:], "data": entered_call}, block_tag])
    if not isinstance(entered_result, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", entered_result):
        raise RuntimeError("Venus Core entered-market response was malformed.")
    entered_raw = entered_result[2:]
    if len(entered_raw) < 128 or len(entered_raw) % 64 != 0:
        raise RuntimeError("Venus Core entered-market ABI response was malformed.")
    offset = int(entered_raw[:64], 16)
    market_count = int(entered_raw[64:128], 16)
    if offset != 32 or market_count > MAX_CORE_ENTERED_MARKETS or len(entered_raw) != 128 + market_count * 64:
        raise RuntimeError("Venus Core entered-market array exceeded the validated ABI bounds.")
    markets = []
    for index in range(market_count):
        word = entered_raw[128 + index * 64:192 + index * 64]
        if len(word) != 64 or word[:24] != "0" * 24 or int(word[24:], 16) == 0:
            raise RuntimeError("Venus Core entered-market address was malformed.")
        markets.append(word[24:].lower())
    if len(set(markets)) != len(markets):
        raise RuntimeError("Venus Core entered-market response contained duplicates.")

    pool_call = "0x" + CORE_USER_POOL_ID_SELECTOR + address_word
    pool_result = rpc("eth_call", [{"to": "0x" + CORE_UNITROLLER[2:], "data": pool_call}, block_tag])
    if not isinstance(pool_result, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", pool_result):
        raise RuntimeError("Venus Core pool selection response was malformed.")
    pool_id = int(pool_result[2:], 16)
    if pool_id >= 2 ** 96:
        raise RuntimeError("Venus Core pool selection exceeded uint96 ABI bounds.")

    block = rpc("eth_getBlockByNumber", [block_tag, False])
    if (not isinstance(block, dict) or not isinstance(block.get("timestamp"), str)
            or not re.fullmatch(r"0x[0-9a-fA-F]+", block["timestamp"])):
        raise RuntimeError("BNB Chain RPC returned no timestamp for the recorded block.")
    block_timestamp = int(block["timestamp"], 16)
    if block_timestamp <= 0:
        raise RuntimeError("BNB Chain RPC returned an invalid block timestamp.")
    has_configuration = bool(markets) or pool_id != 0
    return {
        "chain_id": 56,
        "block_number": block_number,
        "block_tag": block_tag,
        "block_time_utc": datetime.fromtimestamp(block_timestamp, timezone.utc).isoformat(timespec="seconds"),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entered_core_market_count": market_count,
        "user_pool_id": pool_id,
        "configuration_status": "existing_configuration_detected" if has_configuration else "empty_membership_default_pool_observed",
        "rpc_source": RPC_URL,
        "scope_note": "Core entered-market membership and selected pool only. Debt, supplied balances, other pools and borrow or liquidation safety are unknown.",
    }


def ignored_env_file(repo_root):
    try:
        rules = {line.strip() for line in (repo_root / ".gitignore").read_text(encoding="utf-8").splitlines()
                 if line.strip() and not line.lstrip().startswith("#")}
    except OSError:
        return False
    return bool({".env", ".env*", "*.env", "**/.env"} & rules)


def binance_credentials(repo_root):
    env_values = {name: os.environ.get(name) for name in SECRET_NAMES}
    env_pair = tuple(env_values[name] for name in SECRET_NAMES)
    if all(env_pair):
        return env_pair

    file_values = {}
    env_path = repo_root / ".env"
    if env_path.is_file() and ignored_env_file(repo_root):
        try:
            lines = env_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            lines = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip().removeprefix("export ").strip()
            if name not in SECRET_NAMES:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            file_values[name] = value
    file_pair = tuple(file_values.get(name) for name in SECRET_NAMES)
    return file_pair if all(file_pair) else None


def quote_result(status, capture_time, latency_ms=None, **fields):
    result = {"status": status, "capture_time_utc": capture_time, "latency_ms": latency_ms}
    result.update(fields)
    return result


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def signed_binance_get(path, query_params, api_key, secret_key):
    timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    query = urlencode(query_params)
    url_path = path + "?" + query
    signature = base64.b64encode(hmac.new(
        secret_key.encode("utf-8"), (timestamp + "GET" + "/build" + url_path).encode("utf-8"), hashlib.sha256
    ).digest()).decode("ascii")
    request = Request(BINANCE_BASE + url_path, headers={
        "X-OC-APIKEY": api_key, "X-OC-TIMESTAMP": timestamp,
        "X-OC-SIGN": signature, "X-OC-NONCE": secrets.token_hex(16),
        "Accept": "application/json",
    }, method="GET")
    started = time.monotonic()
    body, http_status = b"", None
    try:
        with build_opener(NoRedirect()).open(request, timeout=15) as response:
            http_status = response.status
            body = response.read(MAX_QUOTE_RESPONSE_BYTES + 1)
    except HTTPError as error:
        http_status = error.code
        try:
            body = error.read(MAX_QUOTE_RESPONSE_BYTES + 1)
        except OSError:
            body = b""
    except Exception:
        return {"state": "network_error", "capture_time_utc": None,
                "latency_ms": round((time.monotonic() - started) * 1000, 3),
                "http_status": http_status, "payload": None, "error_label": "binance_network_error"}
    capture_time = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    latency = round((time.monotonic() - started) * 1000, 3)
    if len(body) > MAX_QUOTE_RESPONSE_BYTES:
        return {"state": "malformed_response", "capture_time_utc": capture_time, "latency_ms": latency,
                "http_status": http_status, "payload": None, "error_label": "response_too_large"}
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"state": "malformed_response", "capture_time_utc": capture_time, "latency_ms": latency,
                "http_status": http_status, "payload": None, "error_label": "unexpected_payload"}
    if not isinstance(payload, dict):
        return {"state": "malformed_response", "capture_time_utc": capture_time, "latency_ms": latency,
                "http_status": http_status, "payload": None, "error_label": "unexpected_payload"}
    code = payload.get("code")
    business_code = code if isinstance(code, int) and not isinstance(code, bool) else None
    error_label = None if business_code == 0 else BINANCE_ERROR_LABELS.get(business_code, "unmapped_business_error")
    return {"state": "response", "capture_time_utc": capture_time, "latency_ms": latency,
            "http_status": http_status, "business_code": business_code,
            "payload": payload, "error_label": error_label}


def identity_summary(status, result=None, error_label=None):
    result = result or {}
    return {
        "identity_status": status,
        "identity_capture_time_utc": result.get("capture_time_utc"),
        "identity_latency_ms": result.get("latency_ms"),
        "identity_http_status": result.get("http_status"),
        "identity_business_code": result.get("business_code"),
        "identity_error_label": error_label or result.get("error_label"),
    }


def verify_rwa_identity(result):
    if result.get("state") != "response":
        return result.get("state", "malformed_response"), result.get("error_label", "identity_response_invalid")
    if result.get("http_status") is None or not 200 <= result["http_status"] < 300:
        return "http_error", result.get("error_label") or "unexpected_http_status"
    payload = result.get("payload")
    code = payload.get("code") if isinstance(payload, dict) else None
    if not isinstance(code, int) or isinstance(code, bool):
        return "malformed_response", "missing_business_code"
    if code != 0:
        return ("documented_error" if code in BINANCE_ERROR_LABELS else "unmapped_error"), BINANCE_ERROR_LABELS.get(code, "unmapped_business_error")
    rows = payload.get("data")
    if not isinstance(rows, list):
        return "malformed_response", "unexpected_identity_shape"
    matches = 0
    for row in rows:
        if not isinstance(row, dict):
            return "malformed_response", "unexpected_identity_shape"
        ticker, assets = row.get("ticker"), row.get("assets")
        if not isinstance(ticker, str) or not re.fullmatch(r"[A-Za-z0-9.-]{1,24}", ticker) or not isinstance(assets, list):
            return "malformed_response", "unexpected_identity_shape"
        for asset in assets:
            if not isinstance(asset, dict):
                return "malformed_response", "unexpected_identity_shape"
            platform = asset.get("platformId")
            chain = asset.get("binanceChainId")
            contract = asset.get("tokenContractAddress")
            symbol = asset.get("tokenSymbol")
            asset_type = asset.get("assetType")
            if (not isinstance(platform, str) or not isinstance(chain, str)
                    or not isinstance(contract, str) or not re.fullmatch(r"0x[0-9a-fA-F]{40}", contract)
                    or not isinstance(symbol, str) or not re.fullmatch(r"[A-Za-z0-9.-]{1,24}", symbol)
                    or not isinstance(asset_type, int) or isinstance(asset_type, bool)):
                return "malformed_response", "unexpected_identity_asset_shape"
            if (ticker == "NVDA" and platform == "bstock" and chain == "56"
                    and contract.lower() == NVDAB and symbol == "NVDAB" and asset_type == 1):
                matches += 1
    if matches == 1:
        return "verified", None
    if matches > 1:
        return "ambiguous", "multiple_exact_identity_matches"
    return "missing", "exact_nvdab_bstock_identity_not_found"


def request_binance_quote(wallet, units):
    checked_at = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    credentials = binance_credentials(Path(__file__).resolve().parents[1])
    if credentials is None:
        identity = identity_summary("not_checked", error_label="missing_credentials")
        return quote_result("missing_credentials", None, None, error_label="missing_credentials", **identity)
    api_key, secret_key = credentials

    identity_result = signed_binance_get(RWA_SEARCH_PATH, [("keyword", "NVDA"), ("platformId", "bstock")], api_key, secret_key)
    identity_state, identity_error = verify_rwa_identity(identity_result)
    identity = identity_summary(identity_state, identity_result, identity_error)
    if identity_state != "verified":
        return quote_result("identity_failure", None, None, **identity)

    try:
        chain_id = rpc("eth_chainId", [])
        if not isinstance(chain_id, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", chain_id) or int(chain_id, 16) != 56:
            return quote_result("metadata_unavailable", None, None, error_label="bsc_rpc_chain_mismatch", **identity)
        block_hex = rpc("eth_blockNumber", [])
        if not isinstance(block_hex, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", block_hex):
            return quote_result("metadata_unavailable", None, None, error_label="bsc_rpc_invalid_block", **identity)
        block_number = int(block_hex, 16)
        block_tag = hex(block_number)
        nvdab_code = rpc("eth_getCode", ["0x" + NVDAB[2:], block_tag])
        nvdab_decimals_word = rpc("eth_call", [{"to": "0x" + NVDAB[2:], "data": "0x313ce567"}, block_tag])
        usdt_code = rpc("eth_getCode", ["0x" + USDT[2:], block_tag])
        usdt_decimals_word = rpc("eth_call", [{"to": "0x" + USDT[2:], "data": "0x313ce567"}, block_tag])
        block = rpc("eth_getBlockByNumber", [block_tag, False])
        if (not isinstance(nvdab_code, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", nvdab_code)
                or int(nvdab_code[2:] or "0", 16) == 0
                or not isinstance(nvdab_decimals_word, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", nvdab_decimals_word)
                or int(nvdab_decimals_word, 16) != 18
                or not isinstance(usdt_code, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", usdt_code)
                or int(usdt_code[2:] or "0", 16) == 0
                or not isinstance(usdt_decimals_word, str) or not re.fullmatch(r"0x[0-9a-fA-F]{64}", usdt_decimals_word)
                or int(usdt_decimals_word, 16) != 18
                or not isinstance(block, dict) or not isinstance(block.get("timestamp"), str)
                or not re.fullmatch(r"0x[0-9a-fA-F]+", block["timestamp"])):
            return quote_result("metadata_unavailable", None, None, error_label="token_metadata_unverified", **identity)
        amount_raw = int(units * (Decimal(10) ** 18))
        if amount_raw <= 0 or len(str(amount_raw)) > 78:
            return quote_result("invalid_amount", None, None, error_label="raw_amount_out_of_range", **identity)
        block_time = datetime.fromtimestamp(int(block["timestamp"], 16), timezone.utc).isoformat(timespec="seconds")
    except Exception:
        return quote_result("metadata_unavailable", None, None, error_label="bsc_rpc_or_amount_error", **identity)

    params = [
        ("binanceChainId", "56"),
        ("fromTokenAddress", "0x" + NVDAB[2:]),
        ("toTokenAddress", "0x" + USDT[2:]),
        ("amount", str(amount_raw)),
        ("userWalletAddress", wallet),
    ]
    quote_response = signed_binance_get("/api/v1/dex/aggregator/quote", params, api_key, secret_key)
    capture_time = quote_response.get("capture_time_utc", checked_at)
    latency_ms = quote_response.get("latency_ms")
    if quote_response.get("state") != "response":
        return quote_result(quote_response.get("state", "network_error"), capture_time, latency_ms,
                            error_label=quote_response.get("error_label", "binance_network_error"), **identity)
    http_status = quote_response.get("http_status")
    payload = quote_response.get("payload")
    code = payload.get("code") if isinstance(payload, dict) else None
    if not isinstance(code, int) or isinstance(code, bool):
        return quote_result("malformed_response", capture_time, latency_ms, error_label="missing_business_code", http_status=http_status, **identity)
    if code != 0:
        status = "no_route" if code in (40374, 40421, 40441) else ("documented_error" if code in BINANCE_ERROR_LABELS else "unmapped_error")
        return quote_result(status, capture_time, latency_ms, http_status=http_status,
                            business_code=code, error_label=BINANCE_ERROR_LABELS.get(code, "unmapped_business_error"),
                            **({"route_count": 0} if code in (40374, 40421, 40441) else {}), **identity)
    if http_status is None or not 200 <= http_status < 300:
        return quote_result("http_error", capture_time, latency_ms, error_label="unexpected_http_status", http_status=http_status, **identity)
    routes = payload.get("data")
    if not isinstance(routes, list) or any(not isinstance(route, dict) for route in routes):
        return quote_result("malformed_response", capture_time, latency_ms, error_label="unexpected_routes_shape", http_status=http_status, business_code=code, **identity)
    sanitized = []
    review_mode_required = False
    for route in routes:
        vendor, mode = route.get("vendorName"), route.get("executionMode")
        if (not isinstance(vendor, str) or not re.fullmatch(r"[A-Za-z0-9_. -]{1,80}", vendor)
                or mode not in ("SWAP", "RFQ")):
            return quote_result("malformed_response", capture_time, latency_ms, error_label="unexpected_route_fields", http_status=http_status, business_code=code, **identity)
        if route.get("binanceChainId") != "56":
            return quote_result("malformed_response", capture_time, latency_ms, error_label="route_chain_mismatch", http_status=http_status, business_code=code, **identity)
        from_token, to_token = route.get("fromToken"), route.get("toToken")
        if not isinstance(from_token, dict) or not isinstance(to_token, dict):
            return quote_result("malformed_response", capture_time, latency_ms, error_label="route_token_metadata_malformed", http_status=http_status, business_code=code, **identity)
        expected_tokens = ((from_token, NVDAB, "NVDAB"), (to_token, USDT, "USDT"))
        for token, contract, symbol in expected_tokens:
            token_contract = token.get("tokenContractAddress")
            token_symbol = token.get("tokenSymbol")
            token_decimals = token.get("decimal")
            if (not isinstance(token_contract, str) or not re.fullmatch(r"0x[0-9a-fA-F]{40}", token_contract)
                    or token_contract.lower() != contract or token_symbol != symbol):
                return quote_result("malformed_response", capture_time, latency_ms, error_label="route_token_identity_mismatch", http_status=http_status, business_code=code, **identity)
            if token_decimals != "18":
                return quote_result("malformed_response", capture_time, latency_ms, error_label="route_token_decimals_mismatch", http_status=http_status, business_code=code, **identity)
        from_amount, to_amount = route.get("fromTokenAmount"), route.get("toTokenAmount")
        if (not isinstance(from_amount, str) or len(from_amount) > 78 or not re.fullmatch(r"[0-9]+", from_amount)
                or not isinstance(to_amount, str) or len(to_amount) > 78 or not re.fullmatch(r"[0-9]+", to_amount)):
            return quote_result("malformed_response", capture_time, latency_ms, error_label="unexpected_route_amount", http_status=http_status, business_code=code, **identity)
        if from_amount != str(amount_raw):
            return quote_result("malformed_response", capture_time, latency_ms, error_label="route_input_amount_mismatch", http_status=http_status, business_code=code, **identity)
        if int(to_amount) <= 0:
            return quote_result("malformed_response", capture_time, latency_ms, error_label="route_output_amount_nonpositive", http_status=http_status, business_code=code, **identity)
        item = {"vendorName": vendor, "executionMode": mode,
                "fromTokenAmount": from_amount, "toTokenAmount": to_amount}
        if mode == "SWAP":
            review_mode_required = True
        sanitized.append(item)
    result_status = "no_route" if not routes else (
        "route_observed_mode_review_required" if review_mode_required else "route_observed_proceeds_unverified"
    )
    return quote_result(result_status, capture_time, latency_ms, route_count=len(routes), routes=sanitized,
                        token_metadata_block=block_number, token_metadata_block_tag=block_tag,
                        token_metadata_block_time_utc=block_time, request_amount_raw=str(amount_raw),
                        http_status=http_status, business_code=code,
                        error_label=None if routes else "no_route", **identity)


def d(value):
    if value in (None, ""):
        return None
    try:
        result = Decimal(str(value))
        return result if result.is_finite() else None
    except InvalidOperation:
        return None


def raw_units_string(raw, decimals):
    whole, fraction = divmod(raw, 10 ** decimals)
    return str(whole) + ("." + str(fraction).zfill(decimals).rstrip("0") if fraction else "")


def market_rows(data):
    rows = data.get("result", []) if isinstance(data, dict) else []
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise RuntimeError("Venus returned an invalid market list.")
    return rows


def unique_market(rows, address, symbol):
    matches = [row for row in rows if row.get("chainId") == CHAIN
               and row.get("underlyingSymbol") == symbol
               and (row.get("underlyingAddress") or "").lower() == address]
    if len(matches) != 1:
        raise RuntimeError("Venus did not return exactly one verified %s market for BNB Chain." % symbol)
    return matches[0]


def build_scenario(units, cash, data, retrieved_at):
    rows = market_rows(data)
    stock = unique_market(rows, NVDAB, "NVDAB")
    pool = stock.get("poolComptrollerAddress")
    if not pool:
        raise RuntimeError("Venus NVDAB pool identity is unavailable.")
    usdt_matches = [row for row in rows if row.get("chainId") == CHAIN
                    and (row.get("poolComptrollerAddress") or "").lower() == pool.lower()
                    and row.get("underlyingSymbol") == "USDT"
                    and (row.get("underlyingAddress") or "").lower() == USDT]
    if len(usdt_matches) != 1:
        raise RuntimeError("Venus did not return exactly one verified USDT market in the NVDAB pool.")
    usdt = usdt_matches[0]
    if stock.get("isListed") is not True or stock.get("canBeCollateral") is not True:
        raise RuntimeError("NVDAB is not currently listed and enabled as collateral.")
    price_m, decimals = d(stock.get("underlyingPriceMantissa")), d(stock.get("underlyingDecimal"))
    cf, lt = d(stock.get("collateralFactorMantissa")), d(stock.get("liquidationThresholdMantissa"))
    if (stock.get("isPriceInvalid") is True or price_m is None or price_m <= 0
            or price_m != price_m.to_integral_value()):
        raise RuntimeError("Venus NVDAB price is invalid or unavailable.")
    if decimals is None or decimals != 18:
        raise RuntimeError("Venus returned invalid NVDAB decimals.")
    scale = Decimal(10) ** 18
    if (cf is None or lt is None or cf <= 0 or lt <= 0 or cf > scale or lt > scale
            or cf != cf.to_integral_value() or lt != lt.to_integral_value()):
        raise RuntimeError("Venus collateral or liquidation factor is unavailable.")
    cap = d(stock.get("supplyCapsMantissa"))
    token_supply = d(stock.get("totalSupplyMantissa"))
    exchange_rate = d(stock.get("exchangeRateMantissa"))
    if (cap is None or token_supply is None or exchange_rate is None
            or cap < 0 or token_supply < 0 or exchange_rate <= 0
            or any(value != value.to_integral_value() for value in (cap, token_supply, exchange_rate))):
        raise RuntimeError("Venus NVDAB supply-cap data is unavailable.")
    supplied_raw = int(token_supply) * int(exchange_rate) // (10 ** 18)
    headroom_raw = max(int(cap) - supplied_raw, 0)
    headroom_units = raw_units_string(headroom_raw, int(decimals))
    entered_units_raw = int(units * (Decimal(10) ** int(decimals)))
    within_indexed_cap = cap > 0 and entered_units_raw <= headroom_raw
    if usdt.get("isListed") is not True or usdt.get("isBorrowable") is not True:
        raise RuntimeError("Venus USDT borrowing is currently unavailable.")

    # Venus documented mantissa scale: 1e(36 - underlying decimals).
    price = price_m / (Decimal(10) ** (36 - int(decimals)))
    usdt_price_m, usdt_decimals = d(usdt.get("underlyingPriceMantissa")), d(usdt.get("underlyingDecimal"))
    if (usdt.get("isPriceInvalid") is True or usdt_price_m is None or usdt_price_m <= 0
            or usdt_price_m != usdt_price_m.to_integral_value()):
        raise RuntimeError("Venus USDT oracle price is invalid or unavailable.")
    if usdt_decimals is None or usdt_decimals != 18:
        raise RuntimeError("Venus returned invalid USDT decimals.")
    usdt_price = usdt_price_m / (Decimal(10) ** (36 - int(usdt_decimals)))
    borrow_rate = d(usdt.get("borrowApyDecimal"))
    cash_raw = d(usdt.get("cashMantissa"))
    if price <= 0 or usdt_price <= 0 or borrow_rate is None or borrow_rate < 0 or cash_raw is None or cash_raw < 0:
        raise RuntimeError("Venus USDT rate, oracle price or pool cash is unavailable.")
    pool_cash = cash_raw / (Decimal(10) ** int(usdt_decimals))
    collateral_value_usd = units * price
    collateral_value_usdt = collateral_value_usd / usdt_price
    capacity = collateral_value_usdt * cf / scale
    # Venus price mantissas are scaled by 10 ** (36 - token decimals), so raw
    # token amounts cancel both price scales. Keep the ceiling exact in base units.
    cash_units_raw = int(cash * (Decimal(10) ** int(usdt_decimals)))
    required_nvdab_numerator = cash_units_raw * int(usdt_price_m) * (10 ** 18)
    required_nvdab_denominator = int(price_m) * int(cf)
    required_nvdab_raw = (required_nvdab_numerator + required_nvdab_denominator - 1) // required_nvdab_denominator
    required_nvdab_units = raw_units_string(required_nvdab_raw, int(decimals))
    threshold = lt / scale
    liquidation_weighted_usdt = collateral_value_usd * threshold / usdt_price
    health = liquidation_weighted_usdt / cash
    drop = (Decimal(1) - (cash * usdt_price / (collateral_value_usd * threshold))) * 100 if collateral_value_usd * threshold > cash * usdt_price else None
    return {
        "retrieved_at": retrieved_at, "source_url": API_URL, "chain_id": 56,
        "scenario_only": True,
        "assumptions": ["No wallet debt or other collateral", "No E-Mode", "No accrued interest or execution costs", "Market-level snapshot, not a personal safety assessment"],
        "input": {"units": str(units), "cash_usdt": str(cash)},
        "market": {"nvdab_price_usd": str(price), "usdt_oracle_price_usd": str(usdt_price), "collateral_factor": str(cf / scale), "liquidation_threshold": str(threshold), "borrow_apy": str(borrow_rate), "pool_cash_usdt": str(pool_cash), "nvdab_supply_cap_headroom": headroom_units, "nvdab_market": stock.get("address"), "usdt_market": usdt.get("address"), "pool_comptroller": pool, "data_status": "indexed Venus API snapshot, may lag the chain"},
        "borrow": {"nominal_capacity_usdt": str(capacity), "target_feasible_by_collateral": entered_units_raw >= required_nvdab_raw,
                   "target_feasible_by_pool_liquidity": cash <= pool_cash,
                   "entered_units_within_indexed_supply_cap": within_indexed_cap,
                   "minimum_nvdab_for_target": required_nvdab_units,
                   "minimum_within_indexed_supply_cap": cap > 0 and required_nvdab_raw <= headroom_raw,
                   "health_factor": str(health), "price_drop_to_hf_1_percent": str(drop) if drop is not None else None,
                   "interest_30d_usdt": str(cash * borrow_rate * Decimal(30) / Decimal(365)),
                   "interest_90d_usdt": str(cash * borrow_rate * Decimal(90) / Decimal(365)),
                   "interest_note": "Simple interest at the current variable APY, held flat for illustration."},
        "sale": {"status": "unquoted", "message": "No Binance Web3 sell quote is connected. Proceeds are unknown."}
    }


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            try:
                with open("app/index.html", "rb") as page:
                    body = page.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except OSError:
                self.send_error(500)
            return
        if parsed.path != "/api/scenario":
            self.send_error(404)
            return
        query = parse_qs(parsed.query)
        try:
            units = decimal_input(query.get("units", [""])[0], "units")
            cash = decimal_input(query.get("cash", [""])[0], "cash")
            data = fetch_markets()
            result = build_scenario(units, cash, data, datetime.now(timezone.utc).isoformat(timespec="seconds"))
            self.send_json(200, result)
        except ScenarioError as exc:
            self.send_json(400, {"error": {"field": exc.field, "message": exc.message}})
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
            self.send_json(502, {"error": {"field": "service", "message": "Live Venus data is unavailable. No scenario was calculated.", "detail": str(exc)[:180]}})

    def do_POST(self):
        endpoint = urlparse(self.path).path
        if endpoint not in ("/api/balance", "/api/quote", "/api/venus-account"):
            self.send_error(404)
            return
        if endpoint in ("/api/balance", "/api/quote", "/api/venus-account"):
            host = self.headers.get("Host", "").lower()
            origin = self.headers.get("Origin")
            content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if host not in ("127.0.0.1:8000", "localhost:8000"):
                self.send_json(403, {"error": {"field": "quote" if endpoint == "/api/quote" else "wallet", "message": "Local API request rejected for this host."}})
                return
            if origin is not None and origin not in ("http://127.0.0.1:8000", "http://localhost:8000"):
                self.send_json(403, {"error": {"field": "quote" if endpoint == "/api/quote" else "wallet", "message": "Local API request rejected for this origin."}})
                return
            if content_type != "application/json":
                self.send_json(415, {"error": {"field": "quote" if endpoint == "/api/quote" else "wallet", "message": "Local API request requires application/json."}})
                return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                raise ScenarioError("wallet", "Enter a valid public wallet address.")
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(body, dict):
                raise ScenarioError("wallet", "Enter a valid public wallet address.")
            wallet = body.get("wallet", "")
            if not isinstance(wallet, str) or not re.fullmatch(r"0x[0-9a-fA-F]{40}", wallet):
                raise ScenarioError("wallet", "Enter a valid 0x public address.")
            if endpoint == "/api/balance":
                units = decimal_input(body.get("units", ""), "units")
                self.send_json(200, read_wallet_balance(wallet, units))
            elif endpoint == "/api/venus-account":
                self.send_json(200, read_venus_core_account_state(wallet))
            else:
                units = decimal_input(body.get("units", ""), "units")
                self.send_json(200, request_binance_quote(wallet, units))
        except ScenarioError as exc:
            self.send_json(400, {"error": {"field": exc.field, "message": exc.message}})
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError, RuntimeError, ValueError, OSError, OverflowError) as exc:
            # Never include the submitted address or raw RPC error in the response.
            if endpoint == "/api/balance":
                message = "NVDAB balance is unknown. BNB Chain RPC data could not be verified at one block; retry later."
            elif endpoint == "/api/venus-account":
                message = "Venus Core account state is unknown. BNB Chain RPC data could not be verified at one block; retry later."
            else:
                message = "Binance quote status is unknown. No raw response was retained; retry explicitly if needed."
            error_field = "quote" if endpoint == "/api/quote" else "wallet"
            self.send_json(502, {"error": {"field": error_field, "message": message}})

    def log_message(self, fmt, *args):
        # Keep access logs free of entered query amounts.
        if self.path.startswith("/api/"):
            print("%s - read-only API request" % self.address_string())
        else:
            super().log_message(fmt, *args)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Read-only scenario at http://127.0.0.1:8000")
    server.serve_forever()
