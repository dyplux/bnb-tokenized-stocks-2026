#!/usr/bin/env python3
"""Read one APRO NVDAB/USD oracle round on BNB Chain at a fixed block."""

import json
import sys
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RPC = "https://bsc-dataseed.binance.org/"
FEED = "0x310EFC9Fefe89B8085F89E91Ac782Bef6416499E"
SELECTORS = {"decimals": "0x313ce567", "description": "0x7284e416", "latestRoundData": "0xfeaf968c"}


def utc(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace("+00:00", "Z")


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    request = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.load(response)
    if "error" in payload or not isinstance(payload.get("result"), (str, dict)):
        raise RuntimeError("RPC failed: " + str(payload.get("error"))[:160])
    return payload["result"]


def call(selector, block_tag):
    result = rpc("eth_call", [{"to": FEED, "data": selector}, block_tag])
    if not isinstance(result, str) or not result.startswith("0x"):
        raise RuntimeError("invalid eth_call result")
    return result


def words(hex_result):
    raw = bytes.fromhex(hex_result[2:])
    if len(raw) % 32:
        raise RuntimeError("invalid ABI word length")
    return [int.from_bytes(raw[i:i + 32], "big") for i in range(0, len(raw), 32)]


def description(hex_result):
    raw = bytes.fromhex(hex_result[2:])
    offset = int.from_bytes(raw[:32], "big")
    length = int.from_bytes(raw[offset:offset + 32], "big")
    return raw[offset + 32:offset + 32 + length].decode("utf-8")


def main():
    block_number = rpc("eth_blockNumber", [])
    if not isinstance(block_number, str):
        raise RuntimeError("missing block number")
    block = rpc("eth_getBlockByNumber", [block_number, False])
    if not isinstance(block, dict):
        raise RuntimeError("missing block header")
    raw = {name: call(selector, block_number) for name, selector in SELECTORS.items()}
    round_words = words(raw["latestRoundData"])
    if len(round_words) != 5:
        raise RuntimeError("latestRoundData must have five ABI words")
    round_id, unsigned_answer, started_at, updated_at, answered_in_round = round_words
    answer = unsigned_answer - (1 << 256) if unsigned_answer >= 1 << 255 else unsigned_answer
    decimals = words(raw["decimals"])[0]
    block_time = int(block["timestamp"], 16)
    if not 0 < updated_at <= block_time or decimals > 36 or answer <= 0:
        raise RuntimeError("oracle fields failed basic sanity checks")
    result = {
        "captured_at": utc(datetime.now(timezone.utc).timestamp()),
        "origin": "LIVE_ONCHAIN_READ_ONLY", "chain_id": 56, "rpc": RPC,
        "feed_contract": FEED, "feed_docs": "https://docs.apro.com/en/data-push/price-feed-contract",
        "abi_docs": "https://docs.apro.com/en/data-push/evm-guides/price-feed-api-reference",
        "description": description(raw["description"]), "decimals": decimals,
        "block_number": int(block_number, 16), "block_hash": block["hash"],
        "block_timestamp": utc(block_time), "round_id": str(round_id),
        "answer_raw": str(answer), "answer_scaled": str(Decimal(answer).scaleb(-decimals)),
        "started_at": utc(started_at), "updated_at": utc(updated_at),
        "age_seconds_at_block": block_time - updated_at,
        "answered_in_round": str(answered_in_round),
        "raw_eth_call_results": raw,
        "semantic_limit": "NVDAB/USD tokenized-equity oracle update, not an independent NVDA stock-trade or Binance issuer-reference timestamp",
    }
    destination = ROOT / "data/external_reference/2026-10-04-apro-nvdab.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("description", "answer_scaled", "updated_at", "age_seconds_at_block", "block_number")}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        raise SystemExit(1)
