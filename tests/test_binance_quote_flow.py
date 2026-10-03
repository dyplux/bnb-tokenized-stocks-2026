"""Synthetic parser checks only; these fixtures are not live Binance API evidence."""
from datetime import datetime, timezone
from decimal import Decimal
from io import BytesIO
import json
import unittest
from urllib.error import HTTPError
from unittest.mock import MagicMock, patch

from app.server import NVDAB, USDT, fetch_markets, request_binance_quote, request_target_sized_quote, rpc, signed_binance_get


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


def quote_response(from_amount=AMOUNT_RAW, trade_fee=None):
    return {
        "state": "response", "http_status": 200, "business_code": 0,
        "capture_time_utc": "2026-10-02T02:00:01.000Z", "latency_ms": 24,
        "payload": {"code": 0, "data": [{
            "quoteId": "synthetic-private-id", "vendorName": "PcsXRfq",
            "executionMode": "RFQ", "binanceChainId": "56",
            "fromTokenAmount": from_amount, "toTokenAmount": "200000000000000000000",
            "fromToken": {"tokenContractAddress": NVDAB, "tokenSymbol": "NVDAB", "decimal": "18"},
            "toToken": {"tokenContractAddress": USDT, "tokenSymbol": "USDT", "decimal": "18"},
            "tradeFee": trade_fee,
        }]},
    }


def sized_quote_response(from_amount, output_raw="200000000000000000000", trade_fee=None):
    response = quote_response(from_amount, trade_fee)
    response["payload"]["data"][0]["toTokenAmount"] = output_raw
    return response


def two_route_quote_response(from_amount, first_output, second_output):
    response = sized_quote_response(from_amount, first_output)
    second = dict(response["payload"]["data"][0])
    second["vendorName"] = "SecondVendor"
    second["toTokenAmount"] = second_output
    response["payload"]["data"].append(second)
    return response


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
    def test_public_fetches_reject_redirects(self):
        opener = MagicMock()
        redirect = HTTPError("https://example.invalid", 302, "redirect", {"Location": "https://evil.invalid"}, BytesIO())
        opener.open.side_effect = redirect
        with patch("app.server.build_opener", return_value=opener):
            with self.assertRaises(HTTPError):
                fetch_markets()
            with self.assertRaisesRegex(RuntimeError, "RPC request failed"):
                rpc("eth_chainId", [])
        redirect.close()
        self.assertEqual(opener.open.call_count, 2)

    def test_public_fetches_reject_oversized_bodies(self):
        response = MagicMock(status=200)
        response.read.return_value = b"{" + b"a" * (2 * 1024 * 1024) + b"}"
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value = response
        with patch("app.server.build_opener", return_value=opener):
            with self.assertRaisesRegex(RuntimeError, "size limit"):
                fetch_markets()
            with self.assertRaisesRegex(RuntimeError, "RPC request failed"):
                rpc("eth_chainId", [])
        self.assertEqual(response.read.call_args.args, (2 * 1024 * 1024 + 1,))

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
        self.assertEqual(result["routes"][0]["estimated_output_usdt"], "200")
        self.assertNotIn("quoteId", result["routes"][0])
        self.assertEqual(signed.call_count, 2)
        self.assertEqual(signed.call_args_list[1].args[1][-1], ("userWalletAddress", WALLET))

    def test_target_quote_preserves_valid_trade_fee_without_subtracting_it(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response(), sized_quote_response("500000000000000000", trade_fee="0.01800319")]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("100"))
        self.assertEqual(result["routes"][0]["network_fee_usd_estimate"], "0.01800319")
        self.assertEqual(result["routes"][0]["estimated_output_usdt"], "200")

    def test_target_quote_maps_null_trade_fee_to_unknown(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response(), sized_quote_response("500000000000000000", trade_fee=None)]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("100"))
        self.assertIsNone(result["routes"][0]["network_fee_usd_estimate"])

    def test_target_quote_maps_malformed_trade_fee_to_unknown(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response(), sized_quote_response("500000000000000000", trade_fee="-0.01")]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("100"))
        self.assertIsNone(result["routes"][0]["network_fee_usd_estimate"])

    def test_wrong_identity_blocks_rpc_and_quote(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", return_value=identity_response("0x" + "2" * 40)) as signed, \
             patch("app.server.rpc") as rpc:
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["status"], "identity_failure")
        self.assertEqual(result["identity_status"], "missing")
        signed.assert_called_once()
        rpc.assert_not_called()

    def test_synthetic_swap_route_keeps_output_indicative_and_requires_review(self):
        response = quote_response()
        route = response["payload"]["data"][0]
        route["executionMode"] = "SWAP"
        route["vendorName"] = "LiquidMesh"
        route["toTokenAmount"] = "234646962292722258753"
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), response]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["status"], "route_observed_mode_review_required")
        self.assertEqual(result["routes"][0]["estimated_output_usdt"], "234.646962292722258753")
        self.assertNotIn("quoteId", result["routes"][0])

    def test_estimated_output_keeps_all_token_digits(self):
        response = quote_response()
        response["payload"]["data"][0]["toTokenAmount"] = "1234567890123456789012345678901234567890"
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), response]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["routes"][0]["estimated_output_usdt"], "1234567890123456789012.34567890123456789")

    def test_mismatched_route_amount_is_not_shown(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response("2")]), \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_binance_quote(WALLET, Decimal("1"))
        self.assertEqual(result["status"], "malformed_response")
        self.assertEqual(result["error_label"], "route_input_amount_mismatch")
        self.assertNotIn("routes", result)

    def test_target_quote_uses_one_identity_and_two_quotes(self):
        candidate_raw = "500000000000000000"
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response(), two_route_quote_response(candidate_raw, "150000000000000000000", "50000000000000000000")]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("100"))
        self.assertEqual(result["status"], "target_quote_observed")
        self.assertEqual(result["quote_count"], 2)
        self.assertEqual(result["candidate_sale_raw"], candidate_raw)
        self.assertEqual(result["entered_holding_raw"], AMOUNT_RAW)
        self.assertEqual(result["identity_status"], "verified")
        self.assertEqual(result["identity_business_code"], 0)
        self.assertEqual(result["routes"][0]["target_relation"], "above_target")
        self.assertEqual(result["routes"][1]["target_relation"], "below_target")
        self.assertNotIn("target_relation", result)
        self.assertNotIn("quoteId", result["routes"][0])
        self.assertEqual(signed.call_count, 3)
        self.assertEqual([call.args[0] for call in signed.call_args_list], [
            "/api/v1/dex/market/rwa/search",
            "/api/v1/dex/aggregator/quote",
            "/api/v1/dex/aggregator/quote",
        ])
        self.assertEqual(signed.call_args_list[1].args[1][-2], ("amount", AMOUNT_RAW))
        self.assertEqual(signed.call_args_list[2].args[1][-2], ("amount", candidate_raw))

    def test_full_holding_shortfall_stops_before_second_quote(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response()]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("201"))
        self.assertEqual(result["status"], "target-unreachable-before-costs")
        self.assertEqual(result["quote_count"], 1)
        self.assertEqual(signed.call_count, 2)

    def test_candidate_is_capped_at_entered_holding(self):
        holding = Decimal("0.25")
        holding_raw = "250000000000000000"
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), sized_quote_response(holding_raw, "50000000000000000000")]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, holding, Decimal("100"))
        self.assertEqual(result["candidate_sale_raw"], holding_raw)
        self.assertEqual(result["quote_count"], 1)
        self.assertEqual(signed.call_count, 2)

    def test_second_quote_failure_is_not_replaced_by_probe(self):
        failure = {"state": "network_error", "capture_time_utc": "2026-10-02T02:00:02.000Z", "latency_ms": 5,
                   "error_label": "binance_network_error"}
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response(), failure]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("100"))
        self.assertEqual(result["status"], "target_quote_failure")
        self.assertEqual(result["quote_count"], 2)
        self.assertNotIn("routes", result)
        self.assertEqual(signed.call_count, 3)

    def test_invalid_cash_does_not_sign(self):
        with patch("app.server.signed_binance_get") as signed:
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("0"))
        self.assertEqual(result["status"], "invalid_input")
        signed.assert_not_called()

    def test_target_output_never_leaks_quote_id(self):
        with patch("app.server.binance_credentials", return_value=("dummy-key", "dummy-secret")), \
             patch("app.server.signed_binance_get", side_effect=[identity_response(), quote_response(), sized_quote_response("500000000000000000")]) as signed, \
             patch("app.server.rpc", side_effect=rpc_reply):
            result = request_target_sized_quote(WALLET, Decimal("1"), Decimal("100"))
        self.assertEqual(result["status"], "target_quote_observed")
        self.assertNotIn("quoteId", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
