#!/usr/bin/env python3
"""Make one signed, read-only Binance Web3 RWA search request.

Reads credentials from the process environment or this repository's ignored
.env. Prints only whitelisted fields. It doesn't save the API response.
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


BASE_URL = "https://web3.binance.com/build"
PATH = "/api/v1/dex/market/rwa/search"
ERROR_LABELS = {
    40001: "invalid_parameters",
    40101: "invalid_or_disabled_key",
    40102: "invalid_signature",
    40103: "timestamp_or_replay",
    40104: "permission_missing",
    42900: "rate_limited",
    50000: "server_error",
    50001: "service_unavailable",
}
SAFE_ASSET_FIELDS = (
    "platformId", "binanceChainId", "tokenContractAddress", "tokenSymbol", "assetType"
)


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def credentials():
    values = {}
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, separator, value = line.strip().partition("=")
            name = name.removeprefix("export ").strip()
            if separator and name in {"BINANCE_WEB3_API_KEY", "BINANCE_WEB3_SECRET_KEY"}:
                values[name] = value.strip().strip("\"'")
    key = os.environ.get("BINANCE_WEB3_API_KEY") or values.get("BINANCE_WEB3_API_KEY")
    secret = os.environ.get("BINANCE_WEB3_SECRET_KEY") or values.get("BINANCE_WEB3_SECRET_KEY")
    return key, secret


def business_code(payload):
    if isinstance(payload, dict):
        value = payload.get("code")
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def search_rows(payload, ticker):
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list):
        return None
    rows = []
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("ticker"), str):
            continue
        if item["ticker"].upper() != ticker:
            continue
        assets = item.get("assets")
        if not isinstance(assets, list):
            continue
        rows.append({
            "ticker": item.get("ticker"),
            "company_name": item.get("companyName"),
            "assets": [
                {field: asset[field] for field in SAFE_ASSET_FIELDS if field in asset}
                for asset in assets if isinstance(asset, dict)
            ],
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", help="Exact underlying ticker, for example NVDA")
    parser.add_argument("--platform", choices=("bstock", "ondo"))
    args = parser.parse_args()
    ticker = args.ticker.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.\-]{1,12}", ticker):
        parser.error("ticker must contain 1 to 12 letters, digits, dots or hyphens")
    key, secret = credentials()
    if not key or not secret:
        print(json.dumps({"error": "missing_credentials"}))
        return 2

    query = "keyword=" + quote(ticker, safe="")
    if args.platform:
        query += "&platformId=" + quote(args.platform, safe="")
    path_with_query = "/build" + PATH + "?" + query
    timestamp = now_utc()
    signature = base64.b64encode(hmac.new(
        secret.encode("utf-8"),
        (timestamp + "GET" + path_with_query).encode("utf-8"),
        hashlib.sha256,
    ).digest()).decode("ascii")
    request = Request(
        BASE_URL + PATH + "?" + query,
        headers={
            "X-OC-APIKEY": key,
            "X-OC-TIMESTAMP": timestamp,
            "X-OC-SIGN": signature,
            "Accept": "application/json",
        },
        method="GET",
    )
    started = time.monotonic()
    status = None
    body = b""
    try:
        with urlopen(request, timeout=15) as response:
            status = response.status
            body = response.read()
    except HTTPError as error:
        status = error.code
        body = error.read(65536)
    except (URLError, TimeoutError, OSError):
        print(json.dumps({"ticker": ticker, "error": "network_or_timeout",
                          "latency_ms": round((time.monotonic() - started) * 1000, 1)}))
        return 1

    latency = round((time.monotonic() - started) * 1000, 1)
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(json.dumps({"ticker": ticker, "http_status": status,
                          "latency_ms": latency, "error": "invalid_json"}))
        return 1
    code = business_code(payload)
    result = {"ticker": ticker, "platform_filter": args.platform,
              "requested_at_utc": timestamp, "http_status": status,
              "business_code": code, "latency_ms": latency}
    if status != 200 or code != 0:
        result["error"] = ERROR_LABELS.get(code, "unmapped_api_error")
        print(json.dumps(result))
        return 1
    rows = search_rows(payload, ticker)
    if rows is None:
        result["error"] = "unexpected_data_shape"
        print(json.dumps(result))
        return 1
    result["matches"] = rows
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
