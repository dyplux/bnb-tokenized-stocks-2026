#!/usr/bin/env python3
"""Bounded, read-only NVDAB holder risk-parity probe."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_nvdab_holder_debt as holder  # noqa: E402
import probe_venus_core_parity as parity  # noqa: E402


MAX_HOLDERS = 15


def output(status, block=None, counts=None, parity_result=None):
    counts = counts or {
        "ranked_considered": 0,
        "inspected": 0,
        "vNVDAB_positive": 0,
        "vNVDAB_entered": 0,
        "vUSDT_debt_positive": 0,
        "state_candidate_found": 0,
    }
    result = dict(counts)
    result.update({"block": block, "status": status})
    if parity_result is not None:
        result.update(parity_result)
    print(json.dumps(result, sort_keys=True))


def main():
    counts = {
        "ranked_considered": 0,
        "inspected": 0,
        "vNVDAB_positive": 0,
        "vNVDAB_entered": 0,
        "vUSDT_debt_positive": 0,
        "state_candidate_found": 0,
    }
    block = None
    auth = holder.binance_credentials(Path(__file__).resolve().parents[1])
    if auth is None:
        output("missing_credentials", counts=counts)
        return 2

    try:
        api_key, secret_key = auth
        response = holder.signed_binance_get(
            holder.BINANCE_PATH,
            [("binanceChainId", holder.BINANCE_CHAIN), ("tokenContractAddress", holder.V_NVDAB)],
            api_key,
            secret_key,
        )
        if not isinstance(response, dict) or response.get("state") != "response" or response.get("http_status") != 200:
            raise ValueError("holder ranking unavailable")
        accounts = holder.holder_rows(response.get("payload"))[:MAX_HOLDERS]
        counts["ranked_considered"] = len(accounts)

        chain_id = holder.rpc("eth_chainId", [])
        if not isinstance(chain_id, str) or int(chain_id, 16) != 56:
            raise ValueError("wrong chain")
        block_hex = holder.rpc("eth_blockNumber", [])
        if not isinstance(block_hex, str) or not holder.HEX_RE.fullmatch(block_hex):
            raise ValueError("invalid block")
        block = int(block_hex, 16)
        if block <= 0 or block.bit_length() > 256:
            raise ValueError("invalid block")
        tag = hex(block)
        holder.validate_contracts(tag)

        candidate = None
        selected_markets = None
        for account in accounts:
            counts["inspected"] += 1
            try:
                balance = holder.one_word(holder.call(holder.V_NVDAB, holder.BALANCE_OF, account, tag))
                markets = holder.decode_assets(holder.call(holder.CORE_UNITROLLER, holder.GET_ASSETS_IN, account, tag))
                debt = holder.snapshot_borrow(holder.call(holder.V_USDT, holder.GET_ACCOUNT_SNAPSHOT, account, tag))
                has_balance = balance > 0
                entered = holder.V_NVDAB in markets
                has_debt = debt > 0
                counts["vNVDAB_positive"] += int(has_balance)
                counts["vNVDAB_entered"] += int(entered)
                counts["vUSDT_debt_positive"] += int(has_debt)
                if has_balance and entered and has_debt and 1 <= len(markets) <= 5:
                    candidate = account
                    selected_markets = markets
                    counts["state_candidate_found"] = 1
                    break
            except Exception:
                raise ValueError("holder read failed")

        if candidate is None:
            output("no_state_candidate", block=block, counts=counts)
            return 1

        parity.BLOCK = block
        parity.TAG = tag
        parity.calls = 0
        markets = parity.assets_in(candidate)
        if markets != selected_markets:
            raise ValueError("market list changed")
        pool_id = parity.one(parity.CORE, "73769099", candidate)
        spot = parity.returned_address(parity.CORE, "7dc0d1d0")
        bounded = parity.returned_address(parity.CORE, "d7c46d2d")
        vai = parity.returned_address(parity.CORE, "9254f5e5")
        if int(spot, 16) == 0 or int(bounded, 16) == 0:
            raise ValueError("missing oracle")

        snapshots = {}
        for market in markets:
            raw = parity.eth_call(market, "c37f68e2", candidate)
            if len(raw) < 128 or len(raw) % 32:
                raise ValueError("malformed snapshot")
            snapshots[market] = parity.words(raw[:128], 4)
        if any(snapshot[0] for snapshot in snapshots.values()):
            raise ValueError("snapshot error")
        vai_repay = parity.one(vai, "78c2f922", candidate) if int(vai, 16) else 0
        borrowing, used_cf, vai_cf = parity.calculate(candidate, markets, snapshots, 0, bounded, vai_repay)
        liquidation, used_lt, vai_lt = parity.calculate(candidate, markets, snapshots, 1, spot, vai_repay)
        deployed_borrow = parity.words(parity.eth_call(parity.CORE, "528a174c", candidate), 3)
        deployed_liquidation = parity.words(parity.eth_call(parity.CORE, "5ec88c79", candidate), 3)
        if parity.calls > 35:
            raise ValueError("parity read bound exceeded")

        borrowing_exact = borrowing == deployed_borrow
        liquidation_exact = liquidation == deployed_liquidation
        mismatch = (
            not borrowing_exact
            or not liquidation_exact
            or deployed_borrow[0] != 0
            or deployed_liquidation[0] != 0
        )
        result = {
            "entered_markets": len(markets),
            "active_markets_borrowing": used_cf,
            "active_markets_liquidation": used_lt,
            "emode_pool_id": pool_id,
            "vai_nonzero": bool(vai_cf or vai_lt),
            "borrowing_power_exact": borrowing_exact,
            "liquidation_threshold_exact": liquidation_exact,
            "borrowing_power_delta": [a - b for a, b in zip(borrowing, deployed_borrow)],
            "liquidation_threshold_delta": [a - b for a, b in zip(liquidation, deployed_liquidation)],
            "parity_rpc_calls": parity.calls,
        }
        output("mismatch" if mismatch else "ok", block=block, counts=counts, parity_result=result)
        return 1 if mismatch else 0
    except Exception:
        output("error", block=block, counts=counts)
        return 1


if __name__ == "__main__":
    sys.exit(main())
