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
from decimal import Decimal, InvalidOperation
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


def token_address(token):
    return str(token.get("tokenContractAddress", "")).lower() if isinstance(token, dict) else ""


def unsigned_tx_fingerprint(chain_id, tx):
    """Hash the exact unsigned EVM call without retaining wallet or calldata."""
    fields = {"chain_id": str(chain_id), "from": tx["from"].lower(),
              "to": tx["to"].lower(), "value": str(tx.get("value") or "0"),
              "data": tx["data"].lower()}
    return hashlib.sha256(json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def route_base_matches(route, source, destination, raw_amount):
    return (isinstance(route, dict) and str(route.get("binanceChainId")) == "56" and
            token_address(route.get("fromToken")) == source.lower() and
            token_address(route.get("toToken")) == destination.lower() and
            str(route.get("fromTokenAmount")) == str(raw_amount))


def route_matches_intent(route, source, destination, raw_amount):
    if not route_base_matches(route, source, destination, raw_amount):
        return False
    try:
        output = Decimal(str(route.get("toTokenAmount")))
    except (InvalidOperation, TypeError, ValueError):
        return False
    return (output.is_finite() and output > 0 and
            ADDRESS.fullmatch(str(route.get("approveTarget", ""))) is not None)


def build_matches_quote(data, route, wallet, source, destination, raw_amount):
    if not isinstance(data, dict):
        return False
    result = data.get("routerResult")
    tx = data.get("tx")
    if not unsigned_tx_is_exact(tx, wallet):
        return False
    return (route_base_matches(result, source, destination, raw_amount) and
            result.get("router") == route.get("router") and
            str(result.get("toTokenAmount")) == str(route.get("toTokenAmount")) and
            tx["to"].lower() == str(route.get("approveTarget", "")).lower() and
            str(tx.get("value") or "0") == "0")


def run(provider="bstock", wallet=None, api=None, route_context=None):
    if provider not in ("bstock", "ondo"):
        raise ValueError("Only NVDA bStock/Ondo supported")
    wallet = wallet or public_demo_address()
    if not ADDRESS.fullmatch(wallet):
        raise ValueError("Invalid public demo address")
    api = api or Api()
    result = {"origin": "LIVE_READ_ONLY", "provider": provider,
              "chain_id": "56", "side": "BUY", "source_token": USDT,
              "notional_usdt": "10",
              "wallet": "public_demo_address_not_retained", "stage": "CATALOG",
              "quote": None, "build": None, "simulation": None,
              "decision": "NOT_APPROVED",
              "limits": "No issuer eligibility, funded fill, signature, broadcast, or policy ALLOW is established."}
    symbol = "NVDAB" if provider == "bstock" else "NVDAon"
    raw_amount = str(10 * 10**18)
    if route_context is None:
        catalog, at, catalog_hash = api.get(
            TOKENS, [("binanceChainId", "56")], EXPERIMENT,
            "exact BSC NVDA representation for dry run", {"provider": provider})
        rows = [normalize(row) for row in catalog["data"]]
        selected = [row for row in rows if row and row["asset_type"] == 1 and
                    row["ticker"] == "NVDA" and row["provider"] == provider and
                    row["token_symbol"] == symbol]
        if len(selected) != 1:
            raise RuntimeError("Exactly one NVDA contract required")
        contract = selected[0]["contract"]
        result["security"] = {"ticker": "NVDA", "symbol": symbol, "contract": contract,
                              "catalog_observed_at": at, "catalog_sha256": catalog_hash}
    else:
        if (route_context.get("wallet", "").lower() != wallet.lower() or
                route_context.get("provider") != provider or
                route_context.get("ticker") != "NVDA" or
                route_context.get("symbol") != symbol or
                route_context.get("raw_amount") != raw_amount or
                route_context.get("quote_business_code") != 0 or
                not ADDRESS.fullmatch(str(route_context.get("contract", ""))) or
                not route_context.get("quote_sha256") or
                not route_context.get("quote_observed_at")):
            raise ValueError("Policy route context does not match exact wallet and action")
        contract = route_context["contract"]
        result["security"] = {"ticker": "NVDA", "symbol": symbol, "contract": contract,
                              "catalog_observed_at": route_context.get("catalog_observed_at"),
                              "catalog_sha256": route_context.get("catalog_sha256")}
    common = [("binanceChainId", "56"), ("fromTokenAddress", USDT),
              ("toTokenAddress", contract), ("amount", raw_amount),
              ("userWalletAddress", wallet)]
    if route_context is None:
        quote, at, digest = api.get(
            QUOTE, common, EXPERIMENT, "10 USDT exact-wallet quote",
            {"provider": provider, "step": "quote"}, allow_error=True)
        routes = quote.get("data") if quote.get("code") == 0 and isinstance(quote.get("data"), list) else []
        route = next((row for row in routes if isinstance(row, dict) and row.get("isBest") is True),
                     next((row for row in routes if isinstance(row, dict)), {}))
        quote_code = quote.get("code")
    else:
        route = route_context.get("route") or {}
        routes = [route] if route else []
        at, digest = route_context["quote_observed_at"], route_context["quote_sha256"]
        quote_code = route_context["quote_business_code"]
    quote_exact = route_matches_intent(route, USDT, contract, raw_amount)
    result["quote"] = {"observed_at": at, "business_code": quote_code,
                       "route_count": len(routes), "execution_mode": route.get("executionMode"),
                       "vendor": route.get("vendorName"), "intent_match": quote_exact,
                       "sha256": digest, "bound_to_policy": route_context is not None}
    result["stage"] = "QUOTE"
    if not quote_exact or not route.get("quoteId") or route.get("executionMode") != "SWAP":
        return result
    build, at, digest = api.get(
        SWAP_BUILD, common + [("quoteId", route["quoteId"]), ("slippagePercent", "0.5")],
        EXPERIMENT, "unsigned exact-wallet swap build from fresh quote",
        {"provider": provider, "step": "build"}, allow_error=True)
    data = build.get("data") if isinstance(build.get("data"), dict) else {}
    tx = data.get("tx") if isinstance(data.get("tx"), dict) else {}
    exact = build_matches_quote(data, route, wallet, USDT, contract, raw_amount)
    result["build"] = {"observed_at": at, "business_code": build.get("code"),
                       "execution_mode": data.get("executionMode"),
                       "unsigned_tx_present": bool(tx), "quote_build_intent_match": exact,
                       "tx_to": tx.get("to") if exact else None,
                       "calldata_sha256": hashlib.sha256(tx["data"].encode()).hexdigest() if exact else None,
                       "unsigned_tx_fingerprint": unsigned_tx_fingerprint("56", tx) if exact else None,
                       "sha256": digest}
    result["stage"] = "BUILD"
    if build.get("code") != 0 or data.get("executionMode") != "SWAP" or not exact:
        return result
    simulation_request = {"binanceChainId": "56", "evmTx": {"from": wallet, "to": tx["to"],
                                                          "value": tx.get("value") or "0", "data": tx["data"]}}
    simulation, at, digest = api.post_simulation(
        simulation_request,
        EXPERIMENT, "off-chain simulation of exact unsigned transaction",
        {"provider": provider, "step": "simulation"}, allow_error=True)
    outcome = simulation.get("data") if isinstance(simulation.get("data"), dict) else {}
    result["simulation"] = {"observed_at": at, "api_business_code": simulation.get("code"),
                            "predicted_transaction_status": outcome.get("status"),
                            "unsigned_tx_fingerprint": unsigned_tx_fingerprint(
                                simulation_request["binanceChainId"], simulation_request["evmTx"]),
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
