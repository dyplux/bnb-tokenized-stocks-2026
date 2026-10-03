#!/usr/bin/env python3
"""Bounded, read-only NVDAB holder/Core debt overlap probe.

The Binance holder list is sampled once. Every account-level contract read is
made against one pinned BNB Smart Chain block. No address, credential, signed
request, or raw response is printed or written.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.server import (  # noqa: E402
    CORE_UNITROLLER,
    NVDAB,
    RPC_URL,
    V_NVDAB,
    USDT,
    binance_credentials,
    rpc,
    signed_binance_get,
)


BINANCE_PATH = "/api/v1/dex/market/token/holder"
BINANCE_CHAIN = "56"
V_USDT = "0xfd5840cd36d94d7229439859c0112a4185bc0255"

ADDRESS_RE = re.compile(r"0x[0-9a-fA-F]{40}\Z")
WORD_RE = re.compile(r"0x[0-9a-fA-F]{64}\Z")
HEX_RE = re.compile(r"0x[0-9a-fA-F]*\Z")

BALANCE_OF = "70a08231"
GET_ASSETS_IN = "abfceffc"
GET_ACCOUNT_SNAPSHOT = "c37f68e2"
UNDERLYING = "6f307dc3"
COMPTROLLER = "5fe3b567"


def address(value):
    if not isinstance(value, str) or not ADDRESS_RE.fullmatch(value):
        raise ValueError("invalid address")
    return value.lower()


def address_word(value):
    return address(value)[2:].rjust(64, "0")


def call(to, selector, account=None, block_tag=None):
    data = "0x" + selector
    if account is not None:
        data += address_word(account)
    result = rpc("eth_call", [{"to": address(to), "data": data}, block_tag])
    if not isinstance(result, str) or not HEX_RE.fullmatch(result) or len(result) % 64 != 2:
        raise ValueError("malformed eth_call result")
    return result


def one_word(result):
    if not WORD_RE.fullmatch(result):
        raise ValueError("malformed uint256 result")
    return int(result, 16)


def snapshot_borrow(result):
    raw = result[2:]
    if len(raw) < 4 * 64 or len(raw) % 64:
        raise ValueError("malformed vUSDT snapshot")
    words = [int(raw[index * 64:(index + 1) * 64], 16) for index in range(4)]
    if words[0] != 0:
        raise ValueError("vUSDT snapshot error")
    return words[2]


def returned_address(result, expected):
    if not WORD_RE.fullmatch(result) or result[2:26] != "0" * 24:
        raise ValueError("malformed address result")
    if result[-40:].lower() != expected[2:]:
        raise ValueError("contract identity mismatch")


def code_at(target, block_tag):
    result = rpc("eth_getCode", [address(target), block_tag])
    if not isinstance(result, str) or not HEX_RE.fullmatch(result) or result == "0x":
        raise ValueError("missing contract code")
    if int(result[2:] or "0", 16) == 0:
        raise ValueError("missing contract code")


def validate_contracts(block_tag):
    for target in (CORE_UNITROLLER, V_NVDAB, V_USDT):
        code_at(target, block_tag)
    returned_address(call(V_NVDAB, UNDERLYING, block_tag=block_tag), NVDAB)
    returned_address(call(V_NVDAB, COMPTROLLER, block_tag=block_tag), CORE_UNITROLLER)
    returned_address(call(V_USDT, UNDERLYING, block_tag=block_tag), USDT)
    returned_address(call(V_USDT, COMPTROLLER, block_tag=block_tag), CORE_UNITROLLER)


def decode_assets(result):
    if not HEX_RE.fullmatch(result):
        raise ValueError("malformed assets result")
    raw = result[2:]
    if len(raw) < 128 or len(raw) % 64 or int(raw[:64], 16) != 32:
        raise ValueError("malformed assets ABI header")
    count = int(raw[64:128], 16)
    if count > 64 or len(raw) != 128 + count * 64:
        raise ValueError("assets array outside bounds")
    markets = []
    for index in range(count):
        word = raw[128 + index * 64:192 + index * 64]
        if word[:24] != "0" * 24:
            raise ValueError("malformed market address")
        markets.append("0x" + word[24:].lower())
    if len(set(markets)) != len(markets):
        raise ValueError("duplicate market address")
    return markets


def holder_rows(payload):
    if not isinstance(payload, dict) or payload.get("code") != 0:
        raise ValueError("invalid Binance business response")
    data = payload.get("data")
    if isinstance(data, dict):
        for key in ("list", "rows", "holders", "data"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    if not isinstance(data, list) or len(data) > 100:
        raise ValueError("invalid Binance holder list")
    result = []
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("malformed Binance holder row")
        candidate = None
        for key in ("holderWalletAddress",):
            if key in row:
                candidate = row[key]
                break
        result.append(address(candidate))
    return result


def zero_counts(limit, block=None):
    result = {
        "checked": 0,
        "vToken_positive": 0,
        "NVDAB_entered": 0,
        "USDT_debt_positive": 0,
        "both": 0,
        "sole_entered_NVDAB_and_USDT_debt": 0,
        "both_EOA": 0,
        "both_contract": 0,
        "errors": 0,
    }
    result["limit"] = limit
    result["chain_id"] = 56
    if block is not None:
        result["block"] = block
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=15, help="top holder rows to inspect (1-15)")
    args = parser.parse_args()
    if not 1 <= args.limit <= 15:
        parser.error("--limit must be between 1 and 15")

    result = zero_counts(args.limit)
    auth = binance_credentials(Path(__file__).resolve().parents[1])
    if auth is None:
        result["errors"] = 1
        result["error"] = "missing_credentials"
        print(json.dumps(result, sort_keys=True))
        return 2

    try:
        api_key, secret_key = auth
        response = signed_binance_get(
            BINANCE_PATH,
            [("binanceChainId", BINANCE_CHAIN), ("tokenContractAddress", V_NVDAB)],
            api_key,
            secret_key,
        )
        if not isinstance(response, dict) or response.get("state") != "response":
            raise ValueError("Binance request failed")
        if response.get("http_status") != 200:
            raise ValueError("Binance HTTP response failed")
        accounts = holder_rows(response.get("payload"))[:args.limit]

        chain_id = rpc("eth_chainId", [])
        if not isinstance(chain_id, str) or not HEX_RE.fullmatch(chain_id):
            raise ValueError("malformed chain id")
        if int(chain_id, 16) != 56:
            raise ValueError("wrong chain")
        block_hex = rpc("eth_blockNumber", [])
        if not isinstance(block_hex, str) or not HEX_RE.fullmatch(block_hex):
            raise ValueError("malformed block number")
        block = int(block_hex, 16)
        if block <= 0 or block.bit_length() > 256:
            raise ValueError("invalid block number")
        result["block"] = block
        validate_contracts(hex(block))

        for account in accounts:
            result["checked"] += 1
            try:
                balance = one_word(call(V_NVDAB, BALANCE_OF, account, hex(block)))
                markets = decode_assets(call(CORE_UNITROLLER, GET_ASSETS_IN, account, hex(block)))
                debt = snapshot_borrow(call(V_USDT, GET_ACCOUNT_SNAPSHOT, account, hex(block)))
                has_vtoken = balance > 0
                entered = V_NVDAB in markets
                has_debt = debt > 0
                if has_vtoken and entered and has_debt:
                    code = rpc("eth_getCode", [account, hex(block)])
                    if not isinstance(code, str) or not HEX_RE.fullmatch(code):
                        raise ValueError("malformed account code")
                    result["both"] += 1
                    result["sole_entered_NVDAB_and_USDT_debt"] += int(markets == [V_NVDAB])
                    if code == "0x" or int(code[2:] or "0", 16) == 0:
                        result["both_EOA"] += 1
                    else:
                        result["both_contract"] += 1
                result["vToken_positive"] += int(has_vtoken)
                result["NVDAB_entered"] += int(entered)
                result["USDT_debt_positive"] += int(has_debt)
            except Exception:
                result["errors"] += 1
        result["note"] = "USDT debt is account-level overlap; it does not show NVDAB alone backs the debt."
        result["rpc_source"] = RPC_URL
        print(json.dumps(result, sort_keys=True))
        return 1 if result["errors"] else 0
    except Exception:
        result["errors"] = 1
        result["error"] = "malformed_or_unavailable_response"
        print(json.dumps(result, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
