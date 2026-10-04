#!/usr/bin/env python3
"""Read-only CBRS spot check: two prices and four bounded route requests."""

import json
import secrets
import sys
from decimal import Decimal, ROUND_DOWN
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, PRICE, QUOTE, write_json  # noqa: E402


def main():
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text(encoding="utf-8"))
    targets = [row for row in catalog["rows"] if row["ticker"] == "CBRS"
               and row["provider"] in ("bstock", "ondo") and row["asset_type"] == 1]
    if len(targets) != 2 or {row["provider"] for row in targets} != {"bstock", "ondo"}:
        raise RuntimeError("CBRS catalog doesn't contain exactly one stock representation per provider")
    targets.sort(key=lambda row: row["provider"])
    api = Api()
    addresses = ",".join(row["contract"] for row in targets)
    payload, price_at, price_hash = api.get(
        PRICE, [("binanceChainId", "56"), ("tokenContractAddresses", addresses)],
        "EXP-RWA-008/CBRS", "same-time token prices for two CBRS representations",
        "weekend_exploratory",
    )
    prices = {str(row.get("tokenContractAddress", "")).lower(): row for row in payload["data"]}
    wallet = "0x" + secrets.token_hex(20)
    rows = []
    for target in targets:
        contract = target["contract"]
        price = prices.get(contract, {})
        ratio = Decimal(str(target["token_to_share_ratio"]))
        if ratio <= 0:
            raise RuntimeError("invalid CBRS token/share ratio")
        decimals = int(target["decimals"])
        for side in ("buy_100_usdt", "sell_0_1_share_arithmetic"):
            if side == "buy_100_usdt":
                source, destination = USDT, contract
                amount = str(100 * 10**18)
            else:
                source, destination = contract, USDT
                amount = str(int((Decimal("0.1") / ratio * 10**decimals).to_integral_value(rounding=ROUND_DOWN)))
            quote, at, raw_hash = api.get(
                QUOTE,
                [("binanceChainId", "56"), ("fromTokenAddress", source),
                 ("toTokenAddress", destination), ("amount", amount), ("userWalletAddress", wallet)],
                "EXP-RWA-008/CBRS", "amount-specific CBRS route or explicit failure",
                {"ticker": "CBRS", "provider": target["provider"], "side": side,
                 "market": "weekend"}, allow_error=True,
            )
            routes = quote.get("data") if quote.get("code") == 0 and isinstance(quote.get("data"), list) else []
            first = routes[0] if routes and isinstance(routes[0], dict) else {}
            rows.append({
                "observed_at": at, "origin": "LIVE", "provider": target["provider"],
                "contract": contract, "side": side, "input_raw": amount,
                "input_decimals_expected": 18 if side == "buy_100_usdt" else decimals,
                "input_raw_echoed": first.get("fromTokenAmount"),
                "input_decimals_echoed": (first.get("fromToken") or {}).get("decimal"),
                "business_code": quote.get("code"), "business_message": quote.get("msg"),
                "route_count": len(routes), "vendor": first.get("vendorName"),
                "execution_mode": first.get("executionMode"),
                "output_raw": first.get("toTokenAmount"),
                "output_decimals_echoed": (first.get("toToken") or {}).get("decimal"),
                "price_impact_percent_reported": first.get("priceImpactPercent"),
                "trade_fee_reported": first.get("tradeFee"),
                "gas_fee_reported": first.get("estimateGasFee"),
                "raw_response_sha256": raw_hash,
            })
    price_rows = []
    for target in targets:
        price = prices.get(target["contract"], {})
        token_price = price.get("tokenPrice")
        ratio = Decimal(str(target["token_to_share_ratio"]))
        price_rows.append({
            "provider": target["provider"], "contract": target["contract"],
            "token_price_usd": token_price, "token_price_updated_at_ms": price.get("tokenPriceUpdatedAt"),
            "token_to_share_ratio_catalog": target["token_to_share_ratio"],
            "ratio_catalog_captured_at": catalog["captured_at"],
            "per_share_arithmetic_usd": str(Decimal(str(token_price)) / ratio) if token_price else None,
            "reference_price_updated_at": None, "reference_age_status": "UNKNOWN",
        })
    result = {
        "observed_at": price_at, "origin": "LIVE", "ticker": "CBRS",
        "question": "Does the apparent same-ticker catalog gap survive same-time token pricing and bounded read-only routes?",
        "price_raw_response_sha256": price_hash, "prices": price_rows, "quotes": rows,
        "limit": "Different issuer rights, ratios and eligibility aren't verified. Quotes are ephemeral, wallet-bound estimates for a nonholder. No fill, arbitrage or profit is established.",
    }
    target = ROOT / "experiments/EXP-RWA-008/cbrs_sunday_probe.json"
    write_json(target, result)
    print(json.dumps({"observed_at": price_at, "route_counts": [row["route_count"] for row in rows],
                      "business_codes": [row["business_code"] for row in rows]}))


if __name__ == "__main__":
    main()
