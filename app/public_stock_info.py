"""Public, read-only Binance Wallet Skill stock-info source for Ondo tokens."""

import gzip
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from app.server import NoRedirect
from scripts.rwa_research import DEVEX, RAW, ROOT, append_jsonl, utc_now

BASE = "https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai"


def fetch(contract, experiment="H-RWA-SAFETY/PRODUCT"):
    if not isinstance(contract, str) or len(contract) != 42 or not contract.startswith("0x") or any(
            char not in "0123456789abcdefABCDEF" for char in contract[2:]):
        raise ValueError("expected exact EVM contract")
    url = BASE + "?" + urlencode({"chainId": "56", "contractAddress": contract})
    request = Request(url, headers={"Accept-Encoding": "identity", "User-Agent": "binance-web3/1.1 (Skill)"})
    started = time.monotonic()
    status, raw, error = None, b"", None
    try:
        with build_opener(NoRedirect()).open(request, timeout=15) as response:
            status, raw = response.status, response.read(100_001)
    except HTTPError as exc:
        status, raw = exc.code, exc.read(100_001)
    except (URLError, TimeoutError, OSError) as exc:
        error = type(exc).__name__
    at = utc_now()
    if len(raw) > 100_000:
        error = "response_too_large"
    try:
        payload = json.loads(raw) if raw and not error else None
    except (UnicodeDecodeError, ValueError):
        payload, error = None, "invalid_json"
    data = payload.get("data") if isinstance(payload, dict) else None
    valid = status == 200 and isinstance(data, dict) and payload.get("code") == "000000"
    digest = hashlib.sha256(raw).hexdigest() if raw else None
    if raw and b"X-OC-" not in raw and b"BINANCE_WEB3_SECRET_KEY" not in raw:
        RAW.mkdir(parents=True, exist_ok=True)
        target = RAW / (digest + ".json.gz")
        if not target.exists():
            with tempfile.NamedTemporaryFile(dir=str(RAW), delete=False) as stream:
                temporary = Path(stream.name)
            try:
                with gzip.open(temporary, "wb") as stream:
                    stream.write(raw)
                os.replace(str(temporary), str(target))
            finally:
                temporary.unlink(missing_ok=True)
        append_jsonl(RAW / "manifest.jsonl", {"captured_at": at, "endpoint": BASE,
                     "experiment_id": experiment, "sha256": digest,
                     "path": str(target.relative_to(ROOT)), "origin": "LIVE"})
    elif raw:
        raise RuntimeError("public response secret scan failed")
    append_jsonl(DEVEX / (at[:10] + ".jsonl"), {
        "timestamp": at, "endpoint": BASE, "method": "GET", "experiment_id": experiment,
        "expected_behavior": "separate stockInfo price and its own as-of field if available",
        "actual_behavior": "success" if valid else "failure",
        "latency_ms": round((time.monotonic() - started) * 1000, 2), "http_status": status,
        "business_code": payload.get("code") if isinstance(payload, dict) else None,
        "sanitized_request": {"chainId": "56", "contractAddress": contract},
        "sanitized_response": {"data_keys": sorted(data) if isinstance(data, dict) else None,
                               "stock_info_keys": sorted(data.get("stockInfo", {})) if isinstance(data, dict) else None},
        "raw_response_sha256": digest, "schema_mismatch": status == 200 and not valid,
        "error": error, "market_context": "public_ondo_stock_info",
        "documentation_issue": "No stock-price as-of timestamp in observed response" if valid else None,
        "suggested_improvement": "Expose stockInfo.price feed source and as-of timestamp" if valid else None,
        "secret_scan": "public_endpoint_no_auth_or_wallet"})
    if not valid:
        raise RuntimeError("Public Ondo stock-info source unavailable")
    return data, at, digest
