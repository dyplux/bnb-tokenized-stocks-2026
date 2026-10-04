#!/usr/bin/env python3
"""Read public BNB Chain balances and allowance for a dated unsigned packet."""

import gzip
import hashlib
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.pre_execution_packet import digest  # noqa: E402
from app.server import USDT  # noqa: E402
from scripts.audit_onchain_multiplier import call, rpc_batch  # noqa: E402
from scripts.prepare_exact_wallet_simulation import (  # noqa: E402
    ADDRESS, build_matches_quote, public_demo_address, route_matches_intent,
)
from scripts.rwa_research import write_json  # noqa: E402

PACKET = ROOT / "data/market_hours/pre_execution_packet_bstock.json"
OUT = ROOT / "data/market_hours/demo_wallet_state.json"
EXPERIMENT = "H-RWA-SAFETY/DEMO-WALLET-STATE"


def read_raw(sha):
    if not isinstance(sha, str) or len(sha) != 64:
        raise ValueError("Missing response digest")
    path = ROOT / "data/market_hours/raw" / (sha + ".json.gz")
    body = gzip.open(path, "rb").read(1_000_001)
    if hashlib.sha256(body).hexdigest() != sha:
        raise ValueError("Retained response digest mismatch")
    return json.loads(body)


def word(address):
    if not ADDRESS.fullmatch(address):
        raise ValueError("Invalid public address")
    return address[2:].lower().rjust(64, "0")


def route_from_packet(packet, wallet):
    action = packet["action"]
    quote_sha = packet["exact_wallet_trial"]["quote_sha256"]
    if quote_sha != packet["policy"]["receipt"]["evidence"]["source_response_sha256"]["quote"]:
        raise ValueError("Policy and build do not share a quote")
    quote = read_raw(quote_sha)
    amount = str(int(Decimal(action["notional_usdt"]) * Decimal(10**18)))
    routes = quote.get("data") if quote.get("code") == 0 else []
    matching = [item for item in routes if route_matches_intent(
        item, USDT, action["contract"], amount)]
    route = next((item for item in matching if item.get("isBest") is True),
                 matching[0] if matching else None)
    if route is None:
        raise ValueError("No exact quote in retained response")
    built = read_raw(packet["exact_wallet_trial"]["build_sha256"])
    if built.get("code") != 0 or not build_matches_quote(
            built.get("data"), route, wallet, USDT, action["contract"], amount):
        raise ValueError("Unsigned build no longer matches retained quote")
    return route, built["data"]["tx"], amount


def read_state(packet_path=PACKET, rpc=rpc_batch):
    packet = json.loads(Path(packet_path).read_text())
    claimed = packet.get("packet_sha256")
    if claimed != digest({k: v for k, v in packet.items() if k != "packet_sha256"}):
        raise ValueError("Packet digest mismatch")
    if packet.get("state") != "BLOCKED" or packet.get("execution_authorized") is not False:
        raise ValueError("Only a blocked unsigned packet may be inspected")
    wallet = public_demo_address()
    route, tx, amount = route_from_packet(packet, wallet)
    spender = route["approveTarget"]
    expected = "fixed-block public wallet balances, allowance and approval-target code"
    head, _, at, _ = rpc([call("eth_blockNumber", [], 1)], "latest", EXPERIMENT,
                         expected_behavior=expected, market_context="demo_wallet_read_only_preflight")
    block = head[0]["result"]
    requests = [
        call("eth_getBalance", [wallet, block], 10),
        call("eth_getCode", [spender, block], 11),
        call("eth_call", [{"to": USDT, "data": "0x70a08231" + word(wallet)}, block], 12),
        call("eth_call", [{"to": USDT, "data": "0xdd62ed3e" + word(wallet) + word(spender)}, block], 13),
        call("eth_call", [{"to": USDT, "data": "0x313ce567"}, block], 14),
        call("eth_getBlockByNumber", [block, False], 15),
    ]
    rows, _, _, response_hash = rpc(requests, block, EXPERIMENT,
                                   expected_behavior=expected, market_context="demo_wallet_read_only_preflight")
    values = {int(row["id"]): row["result"] for row in rows}
    if set(values) != {10, 11, 12, 13, 14, 15}:
        raise ValueError("Incomplete fixed-block wallet state")
    decimals = int(values[14], 16)
    if decimals != 18:
        raise ValueError("USDT decimals differ from the quoted 18-decimal input")
    bnb_wei = int(values[10], 16)
    usdt_units = int(values[12], 16)
    allowance_units = int(values[13], 16)
    gas_limit, gas_price = int(tx["gas"]), int(tx["gasPrice"])
    if gas_limit <= 0 or gas_price <= 0:
        raise ValueError("Unsigned build has no positive gas bound")
    gas_ceiling_wei = gas_limit * gas_price
    result = {"origin": "LIVE_READ_ONLY", "observed_at": at,
              "block": int(block, 16),
              "block_timestamp": datetime.fromtimestamp(int(values[15]["timestamp"], 16), timezone.utc).isoformat(),
              "wallet": "public_demo_address_not_retained", "route_response_sha256": packet["exact_wallet_trial"]["quote_sha256"],
              "rpc_response_sha256": response_hash, "input_usdt_units": amount,
              "usdt_balance_units": str(usdt_units), "usdt_allowance_units": str(allowance_units),
              "bnb_balance_wei": str(bnb_wei), "gas_ceiling_wei": str(gas_ceiling_wei),
              "router_has_code": values[11] not in ("0x", "0x0", "0x00"),
              "has_input_balance": usdt_units >= int(amount),
              "approval_needed": allowance_units < int(amount),
              "has_gas_ceiling": bnb_wei >= gas_ceiling_wei,
              "execution_authorized": False,
              "limits": "Fixed-block public balance and allowance read. The quote is dated and may expire; no eligibility, price, signature or fill is established."}
    return result


if __name__ == "__main__":
    result = read_state()
    write_json(OUT, result)
    print(json.dumps({k: result[k] for k in (
        "block", "has_input_balance", "approval_needed", "has_gas_ceiling",
        "router_has_code", "execution_authorized")}))
