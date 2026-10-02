#!/usr/bin/env python3
"""Read-only Binance Web3 quote probe.

The returned quote is an estimate, not a guarantee; a route may expire in
approximately 30 seconds. No profit, net proceeds, or eligibility has been
established. Raw/UI bStock units require mentor confirmation.

This is a single opt-in GET request for research. It never places an order,
signs a wallet transaction, retries, or writes to disk.
"""

import argparse
import base64
import hashlib
import hmac
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.server import binance_credentials


API_BASE = "https://web3.binance.com/build"
REQUEST_PATH = "/build/api/v1/dex/aggregator/quote"
CHAIN_ID = "56"
ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
RAW_AMOUNT_RE = re.compile(r"^[0-9]+$")
ROUTE_FIELDS = {
    "vendorName",
    "fromTokenAmount",
    "toTokenAmount",
    "tradeFee",
    "estimateGasFee",
    "priceImpactPercent",
    "executionMode",
    "isBest",
}
TOKEN_FIELDS = {"tokenSymbol", "decimal", "tokenContractAddress"}
ERROR_LABELS = {
    40001: "invalid_request_parameters",
    40101: "invalid_or_disabled_api_key",
    40102: "signature_mismatch_or_missing",
    40103: "timestamp_expired_or_replayed_request",
    40104: "api_key_permission_missing",
    40301: "region_restricted",
    40302: "vpn_restricted",
    40303: "unusual_ip",
    40366: "ondo_order_above_vendor_maximum",
    40367: "ondo_underlying_market_not_tradable",
    40368: "ondo_stablecoin_pair_not_supported",
    40369: "bstock_underlying_market_not_tradable",
    40370: "bstock_pair_not_supported",
    40374: "rwa_no_vendor_liquidity",
    40375: "ondo_order_below_usd_minimum",
    42900: "rate_limit_exceeded",
    50000: "internal_server_error",
    50001: "service_temporarily_unavailable",
}


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def output(result, exit_code=0):
    sys.stdout.write(json.dumps(result, separators=(",", ":"), sort_keys=True) + "\n")
    raise SystemExit(exit_code)


def base_result(capture_time):
    return {
        "capture_time_utc": capture_time,
        "latency_ms": None,
        "http_status": None,
        "route_count": 0,
        "routes": [],
    }


def fail(capture_time, error_kind, *, http_status=None, business_code=None, latency_ms=None):
    result = base_result(capture_time)
    result.update({"error_kind": error_kind, "latency_ms": latency_ms, "http_status": http_status})
    if isinstance(business_code, int) and not isinstance(business_code, bool):
        result["business_code"] = business_code
        result["api_error_label"] = ERROR_LABELS.get(business_code, "unmapped_business_error")
    output(result, 1)


def parse_args():
    parser = argparse.ArgumentParser(description="One read-only Binance Web3 quote probe")
    parser.add_argument("--from-token", dest="from_token")
    parser.add_argument("--to-token", dest="to_token")
    parser.add_argument("--amount-raw", dest="amount_raw")
    parser.add_argument("--wallet")
    args = parser.parse_args()
    capture_time = utc_now()

    missing = [name for name in ("from-token", "to-token", "amount-raw", "wallet") if getattr(args, name.replace("-", "_")) is None]
    if missing:
        fail(capture_time, "invalid_arguments")
    if not ADDRESS_RE.fullmatch(args.from_token) or not ADDRESS_RE.fullmatch(args.to_token) or not ADDRESS_RE.fullmatch(args.wallet):
        fail(capture_time, "invalid_address")
    if args.from_token.lower() == args.to_token.lower():
        fail(capture_time, "same_tokens")
    if not RAW_AMOUNT_RE.fullmatch(args.amount_raw) or len(args.amount_raw) > 78 or int(args.amount_raw) <= 0:
        fail(capture_time, "invalid_amount")
    return args, capture_time


def business_code(payload):
    if isinstance(payload, dict) and isinstance(payload.get("code"), int) and not isinstance(payload.get("code"), bool):
        return payload["code"]
    return None


def find_routes(payload):
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not isinstance(data, list) or not all(isinstance(route, dict) for route in data):
        return None
    return data


def sanitize_token(value):
    if not isinstance(value, dict):
        return None
    result = {key: value[key] for key in TOKEN_FIELDS if key in value and isinstance(value[key], (str, int)) and not isinstance(value[key], bool)}
    return result or None


def sanitize_route(route):
    result = {}
    for key in ROUTE_FIELDS:
        value = route.get(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            if value is not None:
                result[key] = value
    for key in ("fromToken", "toToken"):
        token = sanitize_token(route.get(key))
        if token is not None:
            result[key] = token
    return result


def main():
    args, capture_time = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    auth = binance_credentials(repo_root)
    if auth is None:
        fail(capture_time, "missing_credentials")
    api_key, secret_key = auth

    query = urlencode(
        [
            ("binanceChainId", CHAIN_ID),
            ("fromTokenAddress", args.from_token),
            ("toTokenAddress", args.to_token),
            ("amount", args.amount_raw),
            ("userWalletAddress", args.wallet),
        ]
    )
    timestamp = utc_now()
    signing_string = timestamp + "GET" + REQUEST_PATH + "?" + query
    signature = base64.b64encode(hmac.new(secret_key.encode("utf-8"), signing_string.encode("utf-8"), hashlib.sha256).digest()).decode("ascii")
    request = Request(
        API_BASE + "/api/v1/dex/aggregator/quote?" + query,
        headers={
            "X-OC-APIKEY": api_key,
            "X-OC-TIMESTAMP": timestamp,
            "X-OC-SIGN": signature,
            "Accept": "application/json",
        },
        method="GET",
    )

    started = time.monotonic()
    response = None
    payload = None
    status = None
    try:
        with urlopen(request, timeout=15) as response_handle:
            response = response_handle.read()
            status = response_handle.status
    except HTTPError as error:
        status = error.code
        try:
            response = error.read()
        except OSError:
            response = b""
    except (URLError, TimeoutError, OSError):
        latency_ms = round((time.monotonic() - started) * 1000, 3)
        fail(capture_time, "network_error", latency_ms=latency_ms)
    latency_ms = round((time.monotonic() - started) * 1000, 3)
    try:
        payload = json.loads(response.decode("utf-8"))
    except (AttributeError, UnicodeDecodeError, json.JSONDecodeError):
        fail(capture_time, "unexpected_payload", http_status=status, latency_ms=latency_ms)

    code = business_code(payload)
    if status is None or status < 200 or status >= 300:
        fail(capture_time, "http_error", http_status=status, business_code=code, latency_ms=latency_ms)
    if code is None:
        fail(capture_time, "unexpected_payload", http_status=status, latency_ms=latency_ms)
    if code != 0:
        fail(capture_time, "business_error", http_status=status, business_code=code, latency_ms=latency_ms)
    routes = find_routes(payload)
    if routes is None:
        fail(capture_time, "unexpected_payload", http_status=status, business_code=code, latency_ms=latency_ms)

    result = base_result(capture_time)
    result.update({"error_kind": "none", "latency_ms": latency_ms, "http_status": status, "route_count": len(routes), "routes": [sanitize_route(route) for route in routes[:3]]})
    if code is not None:
        result["business_code"] = code
    output(result)


if __name__ == "__main__":
    main()
