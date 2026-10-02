"""Synthetic parser checks only; these fixtures are not live Binance API evidence."""
from datetime import datetime, timezone
from decimal import Decimal
import unittest
from unittest.mock import MagicMock, patch

from app.server import NVDAB, USDT, request_binance_quote, signed_binance_get


WALLET = "0x" + "1" * 40
AMOUNT_RAW = "1000000000000000000"


def identity_response(contract=NVDAB):
    return {
        "state": "response", "http_status": 200, "business_code": 0,
        "capture_time_utc": "2026-10-02T02:00:00.000Z", "latency_ms": 12,
        "payload": {"code": 0, "data": [{"ticker": "NVDA", "assets": [{
            "platformId": "bstock", "binanceChainId": "56",
            "tokenContractAddress": contract, "tokenSymbol": "NVDAB", "assetType": 1,
        }]}]},
    }


def quote_response(from_amount=AMOUNT_RAW):
    return {
        "state": "response", "http_status": 200, "business_code": 0,
        "capture_time_utc": "2026-10-02T02:00:01.000Z", "latency_ms": 24,
        "payload": {"code": 0, "data": [{
            "quoteId": "synthetic-private-id", "vendorName": "PcsXRfq",
            "executionMode": "RFQ", "binanceChainId": "56",
            "fromTokenAmount": from_amount, "toTokenAmount": "200000000000000000000",
            "fromToken": {"tokenContractAddress": NVDAB, "tokenSymbol": "NVDAB", "decimal": "18"},
            "toToken": {"tokenContractAddress": USDT, "tokenSymbol": "USDT", "decimal": "18"},
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


class BinanceQuoteFlowTests(unittest.TestCase):
    def test_identical_same_millisecond_requests_have_distinct_nonces(self):
        response = MagicMock(status=200)
        response.read.return_value = b'{"code":0,"data":[]}'
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value = response
        fixed_time = datetime(2026, 10, 2, 2, 0, tzinfo=timezone.utc)
        with patch("app.server.datetime") as clock, \
             patch("app.server.secrets.token_hex", side_effect=["a" * 32, "b" * 32]), \
             patch("app.server.build_opener", return_value=opener):
            clock.now.return_value = fixed_time
            first = signed_binance_get("/api/v1/dex/market/rwa/search", [("keyword", "NVDA")], "dummy-key", "dummy-secret")
            second = signed_binance_get("/api/v1/dex/market/rwa/search", [("keyword", "NVDA")], "dummy-key", "dummy-secret")
        self.assertEqual(first["state"], "response")
        self.assertEqual(second["state"], "response")
        headers = [dict((key.lower(), value) for key, value in call.args[0].header_items())
                   for call in opener.open.call_args_list]
        self.assertEqual(headers[0]["x-oc-sign"], headers[1]["x-oc-sign"])
        self.assertEqual([item["x-oc-nonce"] for item in headers], ["a" * 32, "b" * 32])

    def test_synthetic_exact_identity_and_rfq_route_are_sanitized(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response()]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["status"], "route_observed_proceeds_unverified")
        self.assertEqual(result["identity_status"], "verified")
        self.assertEqual(result["route_count"], 1)
        self.assertEqual(result["request_amount_raw"], AMOUNT_RAW)
        self.assertEqual(result["routes"][0]["toTokenAmount"], "200000000000000000000")
        self.assertNotIn("quoteId", result["routes"][0])
        self.assertEqual(signed.call_count, 2)
        self.assertEqual(signed.call_args_list[1].args[1][-1], ("userWalletAddress", WALLET))

    def test_wrong_identity_blocks_rpc_and_quote(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", return_value=identity_response("0x" + "2" * 40)) as signed, \
             patch("app.server.rpc") as rpc:
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["status"], "identity_failure")
        self.assertEqual(result["identity_status"], "missing")
        signed.assert_called_once()
        rpc.assert_not_called()

    def test_mismatched_route_amount_is_not_shown(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response("2")]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["status"], "malformed_response")
        self.assertEqual(result["error_label"], "route_input_amount_mismatch")
        self.assertNotIn("routes", result)


if __name__ == "__main__":
    unittest.main()
