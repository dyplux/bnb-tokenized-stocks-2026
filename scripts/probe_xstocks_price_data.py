#!/usr/bin/env python3
"""Read and log the public xStocks price-data schema without assuming its clock."""

import argparse
import gzip
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.rwa_research import DEVEX, RAW, append_jsonl, utc_now  # noqa: E402

BASE = "https://api.xstocks.fi/api/v2/public/assets"
SYMBOLS = ("NVDAx", "AAPLx")
EXPERIMENT = "EXP-RWA-010/XSTOCKS-REFERENCE-CLOCK"


def clock_fields(value, prefix="", depth=0):
    """Report candidate clock fields by path; assign no reference meaning."""
    if depth > 5:
        return {}
    found = {}
    if isinstance(value, dict):
        for key, item in value.items():
            path = (prefix + "." if prefix else "") + str(key)
            if any(term in str(key).lower() for term in ("time", "date", "asof", "updated", "source")):
                if isinstance(item, (str, int, float, type(None))):
                    found[path] = item
            if isinstance(item, (dict, list)):
                found.update(clock_fields(item, path, depth + 1))
    elif isinstance(value, list):
        for index, item in enumerate(value[:3]):
            found.update(clock_fields(item, f"{prefix}[{index}]", depth + 1))
    return found


def fetch(symbol):
    if symbol not in SYMBOLS:
        raise ValueError("Unsupported symbol")
    url = f"{BASE}/{symbol}/price-data"
    started = time.monotonic()
    status, raw, error = None, b"", None
    try:
        with urlopen(Request(url, headers={"Accept": "application/json",
                                               "User-Agent": "Dyplux reference-clock research/1.0"}),
                     timeout=15) as response:
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
    digest = hashlib.sha256(raw).hexdigest() if raw else None
    if raw and not error:
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
        append_jsonl(RAW / "manifest.jsonl", {"captured_at": at, "endpoint": url,
                     "experiment_id": EXPERIMENT, "sha256": digest,
                     "path": str(target.relative_to(ROOT)), "origin": "LIVE"})
    clocks = clock_fields(payload)
    data = payload.get("data") if isinstance(payload, dict) else None
    append_jsonl(DEVEX / (at[:10] + ".jsonl"), {
        "timestamp": at, "endpoint": url, "method": "GET", "experiment_id": EXPERIMENT,
        "expected_behavior": "inspect whether stock-reference price has independent source and as-of",
        "actual_behavior": "json_received" if isinstance(payload, dict) else "no_json",
        "latency_ms": round((time.monotonic() - started) * 1000, 2),
        "http_status": status, "raw_response_sha256": digest,
        "sanitized_request": {"symbol": symbol},
        "sanitized_response": {"top_keys": sorted(payload) if isinstance(payload, dict) else None,
                               "data_keys": sorted(data) if isinstance(data, dict) else None,
                               "candidate_clock_paths": sorted(clocks)},
        "schema_mismatch": status == 200 and not isinstance(payload, dict),
        "error": error, "market_context": "US stock session not checked by this probe",
        "documentation_issue": None, "suggested_improvement": None,
        "secret_scan": "public_endpoint_no_auth_or_wallet"})
    return {"symbol": symbol, "observed_at": at, "http_status": status,
            "response_sha256": digest,
            "top_keys": sorted(payload) if isinstance(payload, dict) else None,
            "data_keys": sorted(data) if isinstance(data, dict) else None,
            "candidate_clock_fields": clocks, "error": error}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbols", nargs="*", help="NVDAx or AAPLx; defaults to both")
    args = parser.parse_args()
    for symbol in args.symbols or SYMBOLS:
        print(json.dumps(fetch(symbol), sort_keys=True))


if __name__ == "__main__":
    main()
