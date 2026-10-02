import json
import unittest
from unittest.mock import patch

from app.server import read_venus_core_account_state


WALLET = "0x1111111111111111111111111111111111111111"
MARKETS = (
    "2222222222222222222222222222222222222222",
    "3333333333333333333333333333333333333333",
)


def abi_address_array(addresses):
    words = ["%064x" % 32, "%064x" % len(addresses)]
    words.extend(("0" * 24) + address for address in addresses)
    return "0x" + "".join(words)


def abi_three_words(error, liquidity, shortfall):
    return "0x" + "".join("%064x" % word for word in (error, liquidity, shortfall))


def rpc_responses(entered_result, pool_result, borrowing_result=None, liquidity_result=None):
    def fake_rpc(method, params):
        if method == "eth_chainId":
            return "0x38"
        if method == "eth_blockNumber":
            return "0x1234"
        if method == "eth_getCode":
            return "0x6000"
        if method == "eth_call":
            data = params[0]["data"]
            if data.startswith("0xabfceffc"):
                return entered_result
            if data.startswith("0x73769099"):
                return pool_result
            if data.startswith("0x528a174c"):
                return borrowing_result or abi_three_words(0, 0, 0)
            if data.startswith("0x5ec88c79"):
                return liquidity_result or abi_three_words(0, 0, 0)
        if method == "eth_getBlockByNumber":
            return {"timestamp": "0x65a00000"}
        raise AssertionError("unexpected RPC call: %s" % method)

    return fake_rpc


class VenusAccountStateTests(unittest.TestCase):
    def test_reads_nonempty_two_market_array_and_uint96_pool(self):
        entered_result = abi_address_array(MARKETS)
        pool_id = 7

        with patch(
            "app.server.rpc",
            side_effect=rpc_responses(entered_result, "0x%064x" % pool_id),
        ) as mocked_rpc:
            result = read_venus_core_account_state(WALLET)

        self.assertEqual(result["configuration_status"], "existing_configuration_detected")
        self.assertEqual(result["entered_core_market_count"], 2)
        self.assertEqual(result["user_pool_id"], pool_id)
        self.assertEqual(result["borrowing_power_state"], "zero")
        self.assertEqual(result["liquidation_threshold_state"], "zero")
        self.assertNotIn("wallet", result)
        serialized = json.dumps(result).lower()
        self.assertNotIn(WALLET.lower(), serialized)
        for market in MARKETS:
            self.assertNotIn(market, serialized)
        self.assertEqual(mocked_rpc.call_count, 8)

    def test_reads_current_risk_states_at_same_block_without_raw_values(self):
        block_tag = "0x1234"
        with patch(
            "app.server.rpc",
            side_effect=rpc_responses(
                abi_address_array(()), "0x" + ("0" * 64),
                abi_three_words(0, 0, 9), abi_three_words(0, 4, 0),
            ),
        ) as mocked_rpc:
            result = read_venus_core_account_state(WALLET)

        self.assertEqual(result["borrowing_power_state"], "shortfall")
        self.assertEqual(result["liquidation_threshold_state"], "cushion")
        risk_calls = [call for call in mocked_rpc.call_args_list if call.args[0] == "eth_call"]
        self.assertEqual([call.args[1][1] for call in risk_calls], [block_tag] * 4)
        serialized = json.dumps(result).lower()
        self.assertNotIn("0000000000000000000000000000000000000000000000000000000000000009", serialized)

    def test_rejects_nonzero_error_malformed_and_inconsistent_risk_results(self):
        cases = (
            (abi_three_words(1, 0, 0), "nonzero error"),
            ("0x00", "three-word ABI response was malformed"),
            (abi_three_words(0, 1, 1), "inconsistent liquidity and shortfall"),
        )
        for risk_result, message in cases:
            with self.subTest(message=message), patch(
                "app.server.rpc",
                side_effect=rpc_responses(
                    abi_address_array(()), "0x" + ("0" * 64), risk_result, abi_three_words(0, 0, 0)
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, message):
                    read_venus_core_account_state(WALLET)

    def test_rejects_duplicate_market_response(self):
        duplicate_result = abi_address_array((MARKETS[0], MARKETS[0]))

        with patch(
            "app.server.rpc",
            side_effect=rpc_responses(duplicate_result, "0x" + ("0" * 64)),
        ) as mocked_rpc:
            with self.assertRaisesRegex(RuntimeError, "contained duplicates"):
                read_venus_core_account_state(WALLET)

        self.assertEqual(mocked_rpc.call_count, 4)


if __name__ == "__main__":
    unittest.main()
