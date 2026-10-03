"""Synthetic pre-entry quote checks. These are not live route observations."""
from decimal import Decimal
import unittest
from unittest.mock import patch

from app.server import NVDAB, USDC, request_entry_exit_check


WALLET = "0x" + "1" * 40
FIVE_USDC = "5000000000000000000"
NVDAB_OUTPUT = "21307880000000000"


def identity_response(contract=NVDAB):
    return {
        "state": "response", "http_status": 200, "capture_time_utc": "2026-10-03T19:00:00.000Z",
        "payload": {"code": 0, "data": [{"ticker": "NVDA", "assets": [{
            "platformId": "bstock", "binanceChainId": "56", "tokenContractAddress": contract,
            "tokenSymbol": "NVDAB", "assetType": 1,
        }]}]},
    }


def route_response(from_contract, from_symbol, to_contract, to_symbol, input_raw, output_raw):
    return {
        "state": "response", "http_status": 200, "capture_time_utc": "2026-10-03T19:00:01.000Z",
        "latency_ms": 300, "payload": {"code": 0, "data": [{
            "quoteId": "synthetic-secret-id", "vendorName": "LiquidMesh", "executionMode": "SWAP",
            "binanceChainId": "56", "fromTokenAmount": input_raw, "toTokenAmount": output_raw,
            "fromToken": {"tokenContractAddress": from_contract, "tokenSymbol": from_symbol, "decimal": "18"},
            "toToken": {"tokenContractAddress": to_contract, "tokenSymbol": to_symbol, "decimal": "18"},
            "tradeFee": "0.0123",
        }]},
    }


def rpc_reply(method, params):
    if method == "eth_chainId":
        return "0x38"
    if method == "eth_blockNumber":
        return "0x775f514"
    if method == "eth_getCode":
        return "0x6000"
    if method == "eth_call":
        return "0x" + format(18, "064x")
    if method == "eth_getBlockByNumber":
        return {"timestamp": "0x68de5a00"}
    raise AssertionError("Unexpected RPC call: " + method)


class EntryExitCheckTests(unittest.TestCase):
    def test_two_routes_use_exact_entry_output_and_sanitize_response(self):
        entry = route_response(USDC, "USDC", NVDAB, "NVDAB", FIVE_USDC, NVDAB_OUTPUT)
        exit_quote = route_response(NVDAB, "NVDAB", USDC, "USDC", NVDAB_OUTPUT, "5002414580000000000")
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), entry, exit_quote]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_entry_exit_check(WALLET, Decimal("5"))
        self.assertEqual(result["status"], "BOTH_ROUTES_QUOTED")
        self.assertEqual(result["entry"]["estimated_output"], "0.02130788")
        self.assertEqual(result["exit"]["input_amount"], "0.02130788")
        self.assertEqual(result["exit"]["estimated_output"], "5.00241458")
        self.assertEqual(signed.call_count, 3)
        self.assertEqual(signed.call_args_list[2].args[1][-2], ("amount", NVDAB_OUTPUT))
        self.assertNotIn("quoteId", str(result))
        self.assertNotIn(WALLET, str(result))

    def test_missing_inverse_route_is_distinct_from_entry_failure(self):
        entry = route_response(USDC, "USDC", NVDAB, "NVDAB", FIVE_USDC, NVDAB_OUTPUT)
        no_exit = {"state": "response", "http_status": 200,
                   "capture_time_utc": "2026-10-03T19:00:02.000Z",
                   "payload": {"code": 40374, "data": []}}
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), entry, no_exit]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_entry_exit_check(WALLET, Decimal("5"))
        self.assertEqual(result["status"], "EXIT_UNAVAILABLE")
        self.assertIsNotNone(result["entry"])
        self.assertIsNone(result["exit"])
        self.assertEqual(result["reason"], "rwa_no_vendor_liquidity")

    def test_wrong_identity_stops_before_chain_and_quotes(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", return_value=identity_response("0x" + "2" * 40)) as signed, \
             patch("app.server.rpc") as rpc:
            result = request_entry_exit_check(WALLET, Decimal("5"))
        self.assertEqual(result["status"], "CHECK_INCOMPLETE")
        self.assertEqual(result["reason"], "exact_nvdab_bstock_identity_not_found")
        signed.assert_called_once()
        rpc.assert_not_called()

    def test_mismatched_entry_amount_never_triggers_inverse_quote(self):
        entry = route_response(USDC, "USDC", NVDAB, "NVDAB", "4000000000000000000", NVDAB_OUTPUT)
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), entry]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_entry_exit_check(WALLET, Decimal("5"))
        self.assertEqual(result["status"], "CHECK_INCOMPLETE")
        self.assertEqual(result["reason"], "route_amount_mismatch")
        self.assertIsNone(result["entry"])
        self.assertEqual(signed.call_count, 2)


if __name__ == "__main__":
    unittest.main()
