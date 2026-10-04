#!/usr/bin/env python3
"""Simulate one unfunded CBRSB route off-chain; no signing or broadcasting."""

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
    common = [("binanceChainId", "56"), ("fromTokenAddress", USDT),
              ("toTokenAddress", target["contract"]), ("amount", str(100 * 10**18)),
              ("userWalletAddress", wallet)]
    api = Api()
    quote, quote_at, quote_hash = api.get(
        QUOTE, common, "EXP-RWA-009/SIMULATE", "fresh 100 USDT CBRSB route",
        {"market": "weekend", "action": "read_only_quote"}, allow_error=True,
    )
    routes = quote.get("data") if quote.get("code") == 0 and isinstance(quote.get("data"), list) else []
    route = routes[0] if routes and isinstance(routes[0], dict) else {}
    result = {"origin": "LIVE", "observed_at": quote_at, "notional": "100 USDT",
              "asset": "CBRSB", "wallet": "ephemeral_unfunded_not_stored",
              "quote": {"business_code": quote.get("code"), "route_count": len(routes),
                        "execution_mode": route.get("executionMode"), "raw_response_sha256": quote_hash},
              "build": None, "simulation": None,
              "limit": "Off-chain simulation with unfunded ephemeral wallet. No approval, signature, broadcast or fill; no eligibility or investment conclusion."}
    if route.get("quoteId") and route.get("executionMode") == "SWAP":
        build, build_at, build_hash = api.get(
            SWAP_BUILD, common + [("quoteId", route["quoteId"]), ("slippagePercent", "0.5")],
            "EXP-RWA-009/SIMULATE", "unsigned swap transaction",
            {"market": "weekend", "action": "read_only_build"}, allow_error=True,
        )
        data = build.get("data") if isinstance(build.get("data"), dict) else {}
        tx = data.get("tx") if isinstance(data.get("tx"), dict) else {}
        result["build"] = {"observed_at": build_at, "business_code": build.get("code"),
                           "business_message": build.get("msg"),
                           "execution_mode": data.get("executionMode"),
                           "tx_present": bool(tx), "raw_response_sha256": build_hash}
        if (build.get("code") == 0 and data.get("executionMode") == "SWAP"
                and tx.get("from", "").lower() == wallet.lower()
                and all(tx.get(key) for key in ("to", "data"))):
            calldata = tx["data"]
            if not calldata.startswith("0x") or len(calldata) > 40_000:
                raise RuntimeError("unexpected calldata shape")
            sim, sim_at, sim_hash = api.post_simulation(
                {"binanceChainId": "56", "evmTx": {
                    "from": wallet, "to": tx["to"], "value": tx.get("value") or "0", "data": calldata,
                }}, "EXP-RWA-009/SIMULATE", "off-chain outcome for unfunded CBRSB swap",
                {"market": "weekend", "action": "off_chain_simulation"}, allow_error=True,
            )
            outcome = sim.get("data") if isinstance(sim.get("data"), dict) else {}
            result["simulation"] = {"observed_at": sim_at, "business_code": sim.get("code"),
                                    "business_message": sim.get("msg"),
                                    "predicted_status": outcome.get("status"),
                                    "fail_reason": outcome.get("failReason"),
                                    "balance_change_count": len(outcome.get("balanceChanges") or []),
                                    "allowance_change_count": len(outcome.get("allowanceChanges") or []),
                                    "calldata_sha256": hashlib.sha256(calldata.encode()).hexdigest(),
                                    "raw_response_sha256": sim_hash}
    write_json(ROOT / "experiments/EXP-RWA-009/cbrsb_unfunded_simulation.json", result)
    print(json.dumps({"quote_routes": len(routes),
                      "build_code": (result["build"] or {}).get("business_code"),
                      "simulation_code": (result["simulation"] or {}).get("business_code"),
                      "predicted_status": (result["simulation"] or {}).get("predicted_status")}))


if __name__ == "__main__":
    main()
