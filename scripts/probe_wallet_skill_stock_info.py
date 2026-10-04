#!/usr/bin/env python3
"""Bounded public Binance Wallet Skill stock-feed schema probe, with no API key."""

import hashlib
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.rwa_research import DEVEX, append_jsonl, utc_now, write_json  # noqa: E402

BASE = "https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai"
OUT = ROOT / "docs/devex/fixtures/2026-10-04-wallet-skill-nvdaon-stock-info.json"


def main():
    catalog = json.loads((ROOT / "data/market_hours/catalog_latest.json").read_text(encoding="utf-8"))
    matches = [row for row in catalog["rows"] if row.get("provider") == "ondo" and
               row.get("ticker") == "NVDA" and row.get("asset_type") == 1]
    if len(matches) != 1:
        raise RuntimeError("expected one exact NVDAon BSC catalog row")
    contract = matches[0]["contract"]
    request = Request(BASE + "?" + urlencode({"chainId": "56", "contractAddress": contract}),
                      headers={"Accept-Encoding": "identity", "User-Agent": "binance-web3/1.1 (Skill)"})
    started = time.monotonic()
    status, raw, failure = None, b"", None
    try:
        with urlopen(request, timeout=15) as response:
            status, raw = response.status, response.read(100_001)
    except HTTPError as exc:
        status, raw = exc.code, exc.read(100_001)
    except (URLError, TimeoutError, OSError) as exc:
        failure = type(exc).__name__
    at = utc_now()
    try:
        payload = json.loads(raw) if raw and len(raw) < 100_001 else None
    except (ValueError, UnicodeDecodeError):
        payload = None
        failure = "invalid_json"
    data = payload.get("data") if isinstance(payload, dict) else None
    valid = status == 200 and isinstance(data, dict) and payload.get("code") == "000000"
    digest = hashlib.sha256(raw).hexdigest() if raw else None
    append_jsonl(DEVEX / (at[:10] + ".jsonl"), {
        "timestamp": at, "endpoint": BASE, "method": "GET", "experiment_id": "EXP-RWA-010/WALLET-SKILL",
        "expected_behavior": "separate stockInfo and tokenInfo with own as-of fields if exposed",
        "actual_behavior": "success" if valid else "failure", "latency_ms": round((time.monotonic() - started) * 1000, 2),
        "http_status": status, "business_code": payload.get("code") if isinstance(payload, dict) else None,
        "sanitized_request": {"chainId": "56", "contractAddress": contract},
        "sanitized_response": {"data_keys": sorted(data) if isinstance(data, dict) else None,
                               "stock_info_keys": sorted(data.get("stockInfo", {})) if isinstance(data, dict) else None},
        "raw_response_sha256": digest, "schema_mismatch": status == 200 and not valid,
        "error": failure, "market_context": "weekend", "secret_scan": "public_endpoint_no_auth_or_wallet"})
    if not valid:
        raise RuntimeError("Public Wallet Skill stock-info probe failed")
    if b"X-OC-" in raw or b"BINANCE_WEB3_SECRET_KEY" in raw:
        raise RuntimeError("unexpected secret-like content in public response")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_json(OUT, {"origin": "LIVE", "observed_at": at, "source": BASE,
                     "request": {"chainId": "56", "contractAddress": contract},
                     "http_status": status, "business_code": payload["code"],
                     "raw_response_sha256": digest, "response": payload,
                     "reference_price_updated_at": None, "reference_age_seconds": None,
                     "reference_age_status": "UNKNOWN",
                     "limit": "HTTP response time is not stock-feed as-of time. stockInfo.price is distinct from tokenInfo.price in official Skill guidance, but source venue and stock-price timestamp were not present in this response."})
    print(json.dumps({"observed_at": at, "stock_price": data.get("stockInfo", {}).get("price"),
                      "token_price": data.get("tokenInfo", {}).get("price"),
                      "stock_timestamp_fields": [key for key in data.get("stockInfo", {}) if "time" in key.lower() or "date" in key.lower()],
                      "reference_age_status": "UNKNOWN", "sha256": digest}))


if __name__ == "__main__":
    main()
