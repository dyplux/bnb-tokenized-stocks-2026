#!/usr/bin/env python3
"""Two bounded, read-only sell quotes for equivalent *arithmetic* NVDA share sizes.

No holding, eligibility, completed sale, or economic equivalence is inferred.
"""

import csv
import json
import secrets
import sys
from decimal import Decimal, ROUND_DOWN
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, QUOTE, append_jsonl  # noqa: E402


def main():
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text())
    targets = [row for row in catalog["rows"]
               if row["ticker"] == "NVDA" and row["provider"] in ("bstock", "ondo")]
    if len(targets) != 2 or {r["provider"] for r in targets} != {"bstock", "ondo"}:
        raise RuntimeError("expected exactly one bStock and one Ondo NVDA contract")
    targets.sort(key=lambda row: row["provider"])
    wallet = "0x" + secrets.token_hex(20)
    api = Api()
    rows = []
    for target in targets:
        ratio = Decimal(str(target["token_to_share_ratio"]))
        decimals = int(target["decimals"])
        share_target = Decimal("0.1")
        raw = int((share_target / ratio * (10 ** decimals)).to_integral_value(rounding=ROUND_DOWN))
        params = [("binanceChainId", "56"), ("fromTokenAddress", target["contract"]),
                  ("toTokenAddress", USDT), ("amount", str(raw)),
                  ("userWalletAddress", wallet)]
        payload, observed_at, response_hash = api.get(
            QUOTE, params, "EXP-RWA-009/sell-side",
            "quote a tokenized NVDA sell to USDT or return a specific route error",
            {"ticker": "NVDA", "provider": target["provider"], "market": "weekend"},
            allow_error=True,
        )
        code = payload.get("code")
        routes = payload.get("data") if code == 0 and isinstance(payload.get("data"), list) else []
        best = routes[0] if routes and isinstance(routes[0], dict) else {}
        from_token = best.get("fromToken") if isinstance(best.get("fromToken"), dict) else {}
        to_token = best.get("toToken") if isinstance(best.get("toToken"), dict) else {}
        row = {
            "observed_at": observed_at, "origin": "LIVE", "ticker": "NVDA",
            "provider": target["provider"], "contract": target["contract"],
            "catalog_ratio_captured_at": catalog["captured_at"],
            "token_to_share_ratio": str(ratio), "target_economic_shares_arithmetic": str(share_target),
            "input_token_raw": str(raw), "input_decimals": decimals,
            "output_token": "USDT", "business_code": code,
            "business_message": payload.get("msg") if isinstance(payload.get("msg"), str) else None,
            "route_count": len(routes), "vendor": best.get("vendorName"),
            "execution_mode": best.get("executionMode"),
            "echoed_from_token_raw": best.get("fromTokenAmount"),
            "echoed_from_token_decimals": from_token.get("decimal"),
            "input_units_verified": str(from_token.get("decimal")) == str(decimals)
                                    and str(best.get("fromTokenAmount")) == str(raw),
            "output_token_raw": best.get("toTokenAmount"),
            "echoed_to_token_decimals": to_token.get("decimal"),
            "trade_fee_reported": best.get("tradeFee"),
            "gas_fee_reported": best.get("estimateGasFee"),
            "price_impact_percent_reported": best.get("priceImpactPercent"),
            "response_sha256": response_hash,
            "limit": "read_only_ephemeral_nonholder_no_fill_or_eligibility",
        }
        rows.append(row)
        append_jsonl(ROOT / "data/market_hours/sell_quote_probe_2026-10-04.jsonl", row)
        print(json.dumps({"provider": row["provider"], "code": code,
                          "route_count": len(routes), "observed_at": observed_at}), flush=True)
    destination = ROOT / "experiments/EXP-RWA-009/sell_side_quote.csv"
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
