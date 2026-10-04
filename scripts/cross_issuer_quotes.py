#!/usr/bin/env python3
"""Same-input cross-provider quote check; no trade or arbitrage assertion."""

import csv
import json
import secrets
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.server import USDT
from scripts.rwa_research import Api, QUOTE


def number(value):
    try:
        result = Decimal(str(value))
        return result if result.is_finite() else None
    except (InvalidOperation, ValueError, TypeError):
        return None


def main():
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text(encoding="utf-8"))
    targets = [row for row in catalog["rows"] if row["ticker"] in ("NVDA", "MSTR") and row["asset_type"] == 1
               and row["provider"] in ("bstock", "ondo", "xstocks_public_listing")]
    targets.sort(key=lambda row: (row["ticker"], row["provider"]))
    api = Api()
    wallet = "0x" + secrets.token_hex(20)
    size, raw = 100, str(100 * 10 ** 18)
    results = []
    for target in targets:
        params = [("binanceChainId", "56"), ("fromTokenAddress", USDT),
                  ("toTokenAddress", target["contract"]), ("amount", raw),
                  ("userWalletAddress", wallet)]
        payload, at, digest = api.get(QUOTE, params, "EXP-RWA-008",
                                      "same-input provider quote or documented error",
                                      {"ticker": target["ticker"], "provider": target["provider"], "size_usdt": size},
                                      allow_error=True)
        routes = payload.get("data") if payload.get("code") == 0 and isinstance(payload.get("data"), list) else []
        route = routes[0] if routes and isinstance(routes[0], dict) else {}
        from_token = route.get("fromToken") if isinstance(route.get("fromToken"), dict) else {}
        to_token = route.get("toToken") if isinstance(route.get("toToken"), dict) else {}
        units_ok = str(from_token.get("decimal")) == "18" and str(route.get("fromTokenAmount")) == raw
        output_decimals = to_token.get("decimal")
        output_raw = number(route.get("toTokenAmount"))
        ratio = number(target.get("token_to_share_ratio"))
        shares = None
        if units_ok and output_raw is not None and str(output_decimals).isdigit() and ratio is not None and ratio > 0:
            shares = output_raw / (Decimal(10) ** int(output_decimals)) * ratio
        gross = Decimal(size) / shares if shares is not None and shares > 0 else None
        results.append({
            "observed_at": at, "origin": "LIVE", "ticker": target["ticker"], "provider": target["provider"],
            "contract": target["contract"], "input_token": "USDT", "input_size": size, "input_raw": raw,
            "business_code": payload.get("code"), "route_count": len(routes), "units_verified": units_ok,
            "output_raw": route.get("toTokenAmount"), "output_decimals": output_decimals,
            "token_to_share_ratio": target.get("token_to_share_ratio"),
            "math_shares_received": str(shares) if shares is not None else None,
            "gross_usdt_per_math_share": str(gross) if gross is not None else None,
            "trade_fee_usd_reported": route.get("tradeFee"),
            "price_impact_percent_reported": route.get("priceImpactPercent"),
            "vendor": route.get("vendorName"), "mode": route.get("executionMode"),
            "raw_response_sha256": digest,
            "limits": "read_only_quote; ratio_math_not_rights_equivalence; no_gas_or_roundtrip_or_fill",
        })
        print(json.dumps({"ticker": target["ticker"], "provider": target["provider"],
                          "code": payload.get("code"), "routes": len(routes), "units_verified": units_ok}), flush=True)
    destination = ROOT / "experiments/EXP-RWA-008/cross_issuer_quotes.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
