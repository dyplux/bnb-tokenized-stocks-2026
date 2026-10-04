#!/usr/bin/env python3
"""Quote and build one CBRSB route without signing or broadcasting a transaction."""

import hashlib
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, QUOTE, SWAP_BUILD, write_json  # noqa: E402


def main():
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text(encoding="utf-8"))
    target = next(row for row in catalog["rows"] if row["ticker"] == "CBRS"
                  and row["provider"] == "bstock" and row["asset_type"] == 1)
    wallet = "0x" + secrets.token_hex(20)
    amount = str(100 * 10**18)
    common = [("binanceChainId", "56"), ("fromTokenAddress", USDT),
              ("toTokenAddress", target["contract"]), ("amount", amount),
              ("userWalletAddress", wallet)]
    api = Api()
    quote, quote_at, quote_hash = api.get(
        QUOTE, common, "EXP-RWA-009/BUILD", "fresh CBRSB route with quoteId",
        {"market": "weekend", "action": "read_only_quote"}, allow_error=True,
    )
    routes = quote.get("data") if quote.get("code") == 0 and isinstance(quote.get("data"), list) else []
    route = routes[0] if routes and isinstance(routes[0], dict) else {}
    result = {"observed_at": quote_at, "origin": "LIVE", "stage": "QUOTE_ONLY",
              "ticker": "CBRS", "provider": "bstock", "contract": target["contract"],
              "notional": "100 USDT", "wallet": "ephemeral_unfunded_not_stored",
              "quote": {"business_code": quote.get("code"), "business_message": quote.get("msg"),
                        "route_count": len(routes), "vendor": route.get("vendorName"),
                        "execution_mode": route.get("executionMode"),
                        "raw_response_sha256": quote_hash},
              "build": None,
              "limit": "Read-only quote/build. No signature, approval, simulation, broadcast, fill, eligibility check or profit claim."}
    if route.get("quoteId"):
        build, at, raw_hash = api.get(
            SWAP_BUILD, common + [("quoteId", route["quoteId"]), ("slippagePercent", "0.5")],
            "EXP-RWA-009/BUILD", "unsigned CBRSB swap build from unexpired quote",
            {"market": "weekend", "action": "read_only_build"}, allow_error=True,
        )
        data = build.get("data") if isinstance(build.get("data"), dict) else {}
        tx = data.get("tx") if isinstance(data.get("tx"), dict) else {}
        rfq = data.get("rfq") if isinstance(data.get("rfq"), dict) else {}
        calldata = tx.get("data") if isinstance(tx.get("data"), str) else None
        result["stage"] = "BUILD_SUCCEEDED" if build.get("code") == 0 else "BUILD_FAILED"
        result["build"] = {"observed_at": at, "business_code": build.get("code"),
                           "business_message": build.get("msg"), "execution_mode": data.get("executionMode"),
                           "vendor": (data.get("routerResult") or {}).get("vendorName"),
                           "tx_present": bool(tx), "tx_to": tx.get("to"),
                           "calldata_present": bool(calldata), "calldata_bytes": (len(calldata) - 2) // 2 if calldata else None,
                           "calldata_sha256": hashlib.sha256(calldata.encode()).hexdigest() if calldata else None,
                           "rfq_present": bool(rfq), "rfq_keys": sorted(rfq),
                           "gas_limit": tx.get("gas"), "gas_price_wei": tx.get("gasPrice"),
                           "raw_response_sha256": raw_hash}
    target_path = ROOT / "experiments/EXP-RWA-009/cbrsb_unsigned_build.json"
    write_json(target_path, result)
    print(json.dumps({"stage": result["stage"], "quote_routes": len(routes),
                      "quote_mode": route.get("executionMode"),
                      "build_code": (result["build"] or {}).get("business_code"),
                      "build_mode": (result["build"] or {}).get("execution_mode"),
                      "tx_present": (result["build"] or {}).get("tx_present"),
                      "rfq_present": (result["build"] or {}).get("rfq_present")}))


if __name__ == "__main__":
    main()
