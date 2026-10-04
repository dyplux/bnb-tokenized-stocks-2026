#!/usr/bin/env python3
"""Bounded read-only USD-size quote ladder. Estimates are not executable fills."""

import csv
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.server import USDC
from scripts.rwa_research import Api, QUOTE, append_jsonl, utc_now

SIZES_USDC = (10, 100, 1000, 10000)
TICKERS = ("NVDA", "MSTR")
USDC_DECIMALS = 18


def main():
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text(encoding="utf-8"))
    targets = [row for row in catalog["rows"] if row["ticker"] in TICKERS and row["provider"] == "bstock"]
    targets.sort(key=lambda row: row["ticker"])
    if len(targets) != len(TICKERS):
        raise RuntimeError("missing BSC bStock targets in catalog")
    wallet = "0x" + secrets.token_hex(20)
    api = Api()
    results = []
    for target in targets:
        for size in SIZES_USDC:
            input_raw = str(size * 10 ** USDC_DECIMALS)
            params = [("binanceChainId", "56"), ("fromTokenAddress", USDC),
                      ("toTokenAddress", target["contract"]), ("amount", input_raw),
                      ("userWalletAddress", wallet)]
            payload, at, raw_hash = api.get(QUOTE, params, "EXP-RWA-009/008",
                                            "quote with route, fees and price impact or documented error",
                                            {"ticker": target["ticker"], "size_usdc": size, "market": "weekend"},
                                            allow_error=True)
            code = payload.get("code")
            routes = payload.get("data") if code == 0 and isinstance(payload.get("data"), list) else []
            best = routes[0] if routes and isinstance(routes[0], dict) else {}
            from_token = best.get("fromToken") if isinstance(best.get("fromToken"), dict) else {}
            to_token = best.get("toToken") if isinstance(best.get("toToken"), dict) else {}
            units_verified = str(from_token.get("decimal")) == str(USDC_DECIMALS) and str(best.get("fromTokenAmount")) == input_raw
            row = {
                "observed_at": at, "origin": "LIVE", "chain_id": "56", "ticker": target["ticker"],
                "provider": target["provider"], "contract": target["contract"], "input_token": "USDC",
                "size_usdc": size, "input_amount_raw": input_raw, "input_decimals": USDC_DECIMALS,
                "quote_from_token_decimals": from_token.get("decimal"),
                "quote_to_token_decimals": to_token.get("decimal"),
                "input_units_verified": units_verified, "http_or_business_code": code, "route_count": len(routes),
                "vendor": best.get("vendorName"), "mode": best.get("executionMode"),
                "from_token_amount_raw": best.get("fromTokenAmount"),
                "to_token_amount_raw": best.get("toTokenAmount"), "trade_fee_reported": best.get("tradeFee"),
                "estimated_gas_fee_reported": best.get("estimateGasFee"),
                "price_impact_percent_reported": best.get("priceImpactPercent"),
                "response_sha256": raw_hash, "wallet": "ephemeral_nonholder_not_recorded",
                "interpretation": "read_only_estimate_no_fill_or_eligibility" if units_verified else "quote_input_units_or_route_unverified",
            }
            results.append(row)
            append_jsonl(ROOT / "data/market_hours/quote_depth_2026-10-04.jsonl", row)
            print(json.dumps({"ticker": row["ticker"], "size_usdc": size, "business_code": code,
                              "routes": len(routes), "observed_at": at}), flush=True)
    destination = ROOT / "experiments/EXP-RWA-009/quote_depth.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
