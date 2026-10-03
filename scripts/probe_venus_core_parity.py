#!/usr/bin/env python3
"""Ephemeral, read-only Venus Core current-state parity probe."""
import json
import re
import urllib.request

RPC = "https://bsc-dataseed.bnbchain.org"
API = "https://api.venus.io/governance/voters?limit=5&page=0"
CORE = "0xfd36e2c2a6789db23113685031d7f16329158384"
BLOCK = None
TAG = None
SCALE = 10 ** 18
calls = 0


def request(url, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Accept": "application/json", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = response.read(2 * 1024 * 1024 + 1)
        if len(payload) > 2 * 1024 * 1024:
            raise ValueError("oversized public response")
        return json.loads(payload)


def rpc(method, params):
    global calls
    calls += 1
    if calls > 35:
        raise RuntimeError("read bound exceeded")
    obj = request(RPC, {"jsonrpc": "2.0", "id": calls, "method": method, "params": params})
    if not isinstance(obj, dict) or "error" in obj or "result" not in obj:
        error = obj.get("error", {}) if isinstance(obj, dict) else {}
        code = error.get("code") if isinstance(error, dict) else None
        message = error.get("message", "") if isinstance(error, dict) else ""
        message = re.sub(r"0x[0-9a-fA-F]{40,}", "[hex redacted]", str(message))[:120]
        raise RuntimeError("RPC failed, code=%s, message=%s" % (code, message))
    return obj["result"]


def address(value):
    if not isinstance(value, str) or len(value) != 42 or not value.startswith("0x"):
        raise ValueError("invalid address")
    bytes.fromhex(value[2:])
    return value.lower()


def aword(value):
    return address(value)[2:].rjust(64, "0")


def iword(value):
    if not isinstance(value, int) or value < 0 or value >= 2 ** 256:
        raise ValueError("invalid uint256")
    return format(value, "064x")


def eth_call(to, selector, *args):
    calldata = "0x" + selector + "".join(aword(a) if isinstance(a, str) else iword(a) for a in args)
    result = rpc("eth_call", [{"to": address(to), "data": calldata}, TAG])
    if not isinstance(result, str) or not result.startswith("0x"):
        raise ValueError("invalid eth_call return")
    raw = bytes.fromhex(result[2:])
    if len(raw) % 32:
        raise ValueError("invalid ABI return length")
    return raw


def words(raw, size):
    if len(raw) != size * 32:
        raise ValueError("unexpected ABI words")
    return tuple(int.from_bytes(raw[i * 32:(i + 1) * 32], "big") for i in range(size))


def one(to, selector, *args):
    return words(eth_call(to, selector, *args), 1)[0]


def returned_address(to, selector):
    value = one(to, selector)
    if value >= 2 ** 160:
        raise ValueError("invalid returned address")
    return "0x" + format(value, "040x")


def assets_in(account):
    raw = eth_call(CORE, "abfceffc", account)
    if len(raw) < 64 or int.from_bytes(raw[:32], "big") != 32:
        raise ValueError("invalid array header")
    count = int.from_bytes(raw[32:64], "big")
    if count > 5 or len(raw) != 64 + count * 32:
        raise ValueError("array outside bounded sample")
    result = []
    for idx in range(count):
        word = raw[64 + idx * 32:96 + idx * 32]
        if word[:12] != bytes(12):
            raise ValueError("invalid array address")
        result.append(address("0x" + word[12:].hex()))
    if len(result) != len(set(result)):
        raise ValueError("duplicate market")
    return result


def calculate(account, markets, snapshots, strategy, price_oracle, vai_repay):
    collateral = debt = 0
    used = 0
    for market in markets:
        _, balance, borrow, exchange = snapshots[market]
        factor = one(CORE, "19ef3e8b", account, market, strategy)
        if balance == 0 and borrow == 0:
            continue
        used += 1
        if strategy == 0:
            collateral_price, debt_price = words(eth_call(price_oracle, "88142b6b", market), 2)
        else:
            collateral_price = debt_price = one(price_oracle, "fc57d4df", market)
        if collateral_price == 0 or debt_price == 0:
            raise ValueError("missing oracle price")
        weighted_exchange = factor * exchange // SCALE
        token_to_denom = weighted_exchange * collateral_price // SCALE
        collateral += token_to_denom * balance // SCALE
        debt += debt_price * borrow // SCALE
    debt += vai_repay
    result = (0, collateral - debt, 0) if collateral > debt else (0, 0, debt - collateral)
    return result, used, vai_repay


def main():
    global BLOCK, TAG
    if int(rpc("eth_chainId", []), 16) != 56:
        raise RuntimeError("wrong chain")
    BLOCK = int(rpc("eth_blockNumber", []), 16)
    TAG = hex(BLOCK)
    response = request(API)
    account = address(response["result"][3]["address"])
    markets = assets_in(account)
    pool_id = one(CORE, "73769099", account)
    spot = returned_address(CORE, "7dc0d1d0")
    bounded = returned_address(CORE, "d7c46d2d")
    vai = returned_address(CORE, "9254f5e5")
    if int(spot, 16) == 0 or int(bounded, 16) == 0:
        raise RuntimeError("missing oracle")
    snapshots = {}
    snapshot_extra_words = 0
    for index, market in enumerate(markets):
        raw = eth_call(market, "c37f68e2", account)
        if len(raw) < 128 or len(raw) % 32:
            raise ValueError("market snapshot %d returned %d bytes, prefix=%s" % (index, len(raw), raw[:4].hex()))
        snapshot_extra_words += len(raw) // 32 - 4
        snapshots[market] = words(raw[:128], 4)
    if any(snapshot[0] for snapshot in snapshots.values()):
        raise ValueError("market snapshot error")
    vai_repay = one(vai, "78c2f922", account) if int(vai, 16) else 0
    borrowing, used_cf, vai_cf = calculate(account, markets, snapshots, 0, bounded, vai_repay)
    liquidation, used_lt, vai_lt = calculate(account, markets, snapshots, 1, spot, vai_repay)
    deployed_borrow = words(eth_call(CORE, "528a174c", account), 3)
    deployed_liquidation = words(eth_call(CORE, "5ec88c79", account), 3)
    print(json.dumps({
        "block": BLOCK, "entered_markets": len(markets), "pool_id": pool_id,
        "used_cf": used_cf, "used_lt": used_lt,
        "snapshot_extra_words": snapshot_extra_words,
        "vai_repay_nonzero": bool(vai_cf or vai_lt), "rpc_calls": calls,
        "borrowing_power_exact": borrowing == deployed_borrow,
        "liquidation_threshold_exact": liquidation == deployed_liquidation,
        "borrowing_reference_cushion": deployed_borrow[1] > 0 and deployed_borrow[2] == 0,
        "liquidation_reference_cushion": deployed_liquidation[1] > 0 and deployed_liquidation[2] == 0,
        "borrowing_power_delta": [a - b for a, b in zip(borrowing, deployed_borrow)],
        "liquidation_threshold_delta": [a - b for a, b in zip(liquidation, deployed_liquidation)],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
