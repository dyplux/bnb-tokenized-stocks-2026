#!/usr/bin/env python3
"""Read-only exact-wallet quote, unsigned build and off-chain simulation.

Reads only the public demo address from the ignored .env. It has no signing,
RPC send or broadcast path. A successful simulation is not trade approval.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, QUOTE, SWAP_BUILD, TOKENS, normalize, write_json  # noqa: E402

OUT = ROOT / "data/market_hours"
ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\Z")
EXPERIMENT = "EXP-RWA-009/EXACT-WALLET-DRY-RUN"


def public_demo_address(path=ROOT / ".env"):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("BNB_STOCKS_DEMO_ADDRESS="):
            value = line.partition("=")[2].strip()
            if not ADDRESS.fullmatch(value):
                raise ValueError("Invalid public demo address")
            return value
    raise ValueError("Public demo address missing from ignored .env")


def unsigned_tx_is_exact(tx, wallet):
    if not isinstance(tx, dict) or tx.get("from", "").lower() != wallet.lower():
        return False
    if not ADDRESS.fullmatch(str(tx.get("to", ""))):
        return False
    calldata = tx.get("data")
    return (isinstance(calldata, str) and calldata.startswith("0x") and
            2 < len(calldata) <= 40_000 and len(calldata) % 2 == 0 and
            bool(re.fullmatch(r"0x[0-9a-fA-F]+", calldata)))


def run(provider="bstock", wallet=None, api=None):
    if provider not in ("bstock", "ondo"):
        raise ValueError("Only NVDA bStock/Ondo supported")
    wallet = wallet or public_demo_address()
    if not ADDRESS.fullmatch(wallet):
        raise ValueError("Invalid public demo address")
    api = api or Api()
    result = {"origin": "LIVE_READ_ONLY", "provider": provider,
              "wallet": "public_demo_address_not_retained", "stage": "CATALOG",
              "quote": None, "build": None, "simulation": None,
              "decision": "NOT_APPROVED",
              "limits": "No issuer eligibility, funded fill, signature, broadcast, or policy ALLOW is established."}
    catalog, at, catalog_hash = api.get(
        TOKENS, [("binanceChainId", "56")], EXPERIMENT,
        "exact BSC NVDA representation for dry run", {"provider": provider})
    rows = [normalize(row) for row in catalog["data"]]
    symbol = "NVDAB" if provider == "bstock" else "NVDAon"
    selected = [row for row in rows if row and row["asset_type"] == 1 and
                row["ticker"] == "NVDA" and row["provider"] == provider and
                row["token_symbol"] == symbol]
    if len(selected) != 1:
        raise RuntimeError("Exactly one NVDA contract required")
    contract = selected[0]["contract"]
    result["security"] = {"ticker": "NVDA", "symbol": symbol, "contract": contract,
                          "catalog_observed_at": at, "catalog_sha256": catalog_hash}
    common = [("binanceChainId", "56"), ("fromTokenAddress", USDT),
              ("toTokenAddress", contract), ("amount", str(10 * 10**18)),
              ("userWalletAddress", wallet)]
    quote, at, digest = api.get(
        QUOTE, common, EXPERIMENT, "10 USDT exact-wallet quote",
        {"provider": provider, "step": "quote"}, allow_error=True)
    routes = quote.get("data") if quote.get("code") == 0 and isinstance(quote.get("data"), list) else []
    route = next((row for row in routes if isinstance(row, dict) and row.get("isBest") is True),
                 routes[0] if routes else {})
    result["quote"] = {"observed_at": at, "business_code": quote.get("code"),
                       "route_count": len(routes), "execution_mode": route.get("executionMode"),
                       "vendor": route.get("vendorName"), "sha256": digest}
    result["stage"] = "QUOTE"
    if not route.get("quoteId") or route.get("executionMode") != "SWAP":
        return result
    build, at, digest = api.get(
        SWAP_BUILD, common + [("quoteId", route["quoteId"]), ("slippagePercent", "0.5")],
        EXPERIMENT, "unsigned exact-wallet swap build from fresh quote",
        {"provider": provider, "step": "build"}, allow_error=True)
    data = build.get("data") if isinstance(build.get("data"), dict) else {}
    tx = data.get("tx") if isinstance(data.get("tx"), dict) else {}
    exact = unsigned_tx_is_exact(tx, wallet)
    result["build"] = {"observed_at": at, "business_code": build.get("code"),
                       "execution_mode": data.get("executionMode"),
                       "unsigned_tx_present": bool(tx), "exact_wallet_and_shape": exact,
                       "tx_to": tx.get("to") if exact else None,
                       "calldata_sha256": hashlib.sha256(tx["data"].encode()).hexdigest() if exact else None,
                       "sha256": digest}
    result["stage"] = "BUILD"
    if build.get("code") != 0 or data.get("executionMode") != "SWAP" or not exact:
        return result
    simulation, at, digest = api.post_simulation(
        {"binanceChainId": "56", "evmTx": {"from": wallet, "to": tx["to"],
                                          "value": tx.get("value") or "0", "data": tx["data"]}},
        EXPERIMENT, "off-chain simulation of exact unsigned transaction",
        {"provider": provider, "step": "simulation"}, allow_error=True)
    outcome = simulation.get("data") if isinstance(simulation.get("data"), dict) else {}
    result["simulation"] = {"observed_at": at, "api_business_code": simulation.get("code"),
                            "predicted_transaction_status": outcome.get("status"),
                            "fail_reason": outcome.get("failReason"), "sha256": digest}
    result["stage"] = "SIMULATED"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("bstock", "ondo"), default="bstock")
    args = parser.parse_args()
    result = run(provider=args.provider)
    write_json(OUT / ("exact_wallet_simulation_" + args.provider + ".json"), result)
    print(json.dumps({"stage": result["stage"], "provider": args.provider,
                      "route_count": (result["quote"] or {}).get("route_count"),
                      "build_code": (result["build"] or {}).get("business_code"),
                      "predicted_status": (result["simulation"] or {}).get("predicted_transaction_status"),
                      "decision": result["decision"]}))


if __name__ == "__main__":
    main()
