#!/usr/bin/env python3
"""Bounded read-only RFQ/SWAP response matrix; no trade, signature, or wallet ownership."""

import argparse
import json
import secrets
import sys
import time
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, PRICE, QUOTE, TOKENS, UNDERLYING_MARKET, normalize, write_json  # noqa: E402

OUT = ROOT / "experiments/EXP-RWA-009/route_semantics_matrix.json"
ASSETS = ("NVDA", "TSLA")
PROVIDERS = ("bstock", "ondo")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", choices=("weekend", "regular-session", "after-hours"), required=True)
    args = parser.parse_args()
    api = Api()
    catalog, catalog_at, catalog_hash = api.get(
        TOKENS, [("binanceChainId", "56")], "EXP-RWA-009/ROUTE-MODE",
        "canonical bStock/Ondo catalog for route semantics matrix", args.label)
    rows = [normalize(row) for row in catalog["data"]]
    selected = [row for row in rows if row and row["asset_type"] == 1 and
                row["provider"] in PROVIDERS and row["ticker"] in ASSETS]
    if len(selected) != 4:
        raise RuntimeError("expected exact NVDA and TSLA bStock/Ondo four-contract matrix")
    contracts = ",".join(row["contract"] for row in selected)
    prices, price_at, price_hash = api.get(
        PRICE, [("binanceChainId", "56"), ("tokenContractAddresses", contracts)],
        "EXP-RWA-009/ROUTE-MODE", "live sizing input for both sides", args.label)
    price_by_contract = {str(row.get("tokenContractAddress", "")).lower(): row for row in prices["data"]}
    wallet = "0x" + secrets.token_hex(20)
    output = {"experiment": "EXP-RWA-009/ROUTE-MODE", "origin": "LIVE_READ_ONLY",
              "requested_session_label": args.label, "catalog_observed_at": catalog_at,
              "catalog_response_sha256": catalog_hash, "price_observed_at": price_at,
              "price_response_sha256": price_hash, "wallet": "temporary_unfunded_not_retained",
              "rows": [], "limit": "A quote mode is only a response field. No eligibility, holder balance, final route cost, build, simulation, signature, trade or documentation defect is established."}
    if OUT.exists():
        previous = json.loads(OUT.read_text())
        if isinstance(previous.get("rows"), list):
            output["rows"] = previous["rows"]
    for target in sorted(selected, key=lambda row: (row["ticker"], row["provider"])):
        contract = target["contract"]
        price = price_by_contract.get(contract, {})
        try:
            token_price = Decimal(str(price.get("tokenPrice")))
            if token_price <= 0:
                raise ValueError("non-positive token price")
        except Exception:
            token_price = None
        market, market_at, market_hash = api.get(
            UNDERLYING_MARKET, [("binanceChainId", "56"), ("tokenContractAddress", contract)],
            "EXP-RWA-009/ROUTE-MODE", "same-time market status for route interpretation",
            {"label": args.label, "ticker": target["ticker"], "provider": target["provider"]},
            allow_error=True)
        state = market.get("data", {}).get("statusInfo") if isinstance(market.get("data"), dict) else {}
        state = state if isinstance(state, dict) else {}
        for side in ("BUY", "SELL"):
            if side == "SELL" and token_price is None:
                continue
            raw_amount = 100 * 10**18 if side == "BUY" else int(Decimal("100") / token_price * Decimal(10**18))
            source, destination = (USDT, contract) if side == "BUY" else (contract, USDT)
            quote, at, digest = api.get(
                QUOTE, [("binanceChainId", "56"), ("fromTokenAddress", source),
                        ("toTokenAddress", destination), ("amount", str(raw_amount)),
                        ("userWalletAddress", wallet)],
                "EXP-RWA-009/ROUTE-MODE", "bounded buy/sell quote mode comparison",
                {"label": args.label, "ticker": target["ticker"], "provider": target["provider"], "side": side},
                allow_error=True)
            routes = quote.get("data") if isinstance(quote.get("data"), list) else []
            output["rows"].append({"observed_at": at, "origin": "LIVE", "requested_session_label": args.label,
                                   "ticker": target["ticker"], "provider": target["provider"], "contract": contract,
                                   "side": side, "input": "100_USDT" if side == "BUY" else "about_100_USDT_of_token",
                                   "raw_input_amount": str(raw_amount), "token_price_for_sizing": str(token_price) if token_price else None,
                                   "market_status": state.get("marketStatus"), "open_state": state.get("openState"),
                                   "market_status_response_sha256": market_hash, "market_observed_at": market_at,
                                   "business_code": quote.get("code"), "route_count": len(routes),
                                   "execution_modes": [row.get("executionMode") for row in routes if isinstance(row, dict)],
                                   "vendors": [row.get("vendorName") for row in routes if isinstance(row, dict)],
                                   "raw_response_sha256": digest})
            output["last_observed_at"] = at
            write_json(OUT, output)
            time.sleep(0.7)
    print(json.dumps({"last_observed_at": output.get("last_observed_at"),
                      "total_rows": len(output["rows"]),
                      "new_rows": sum(row["requested_session_label"] == args.label for row in output["rows"])}))


if __name__ == "__main__":
    main()
