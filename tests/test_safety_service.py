"""Synthetic contract tests for the local read-only judge flow."""

import unittest
import io
import json
from contextlib import redirect_stdout
from unittest.mock import patch

from app.safety_service import multiplier, review, validate
from app.server import USDT
from scripts.safety_agent_tool import main as agent_tool_main
from scripts.rwa_research import PRICE, QUOTE, TOKENS, UNDERLYING_MARKET

CONTRACT = "0x02fca66c1d1afb4e2a7884261eb00f63598a7436"
ONDO_CONTRACT = "0xa9ee28c80f960b889dfbd1902055218cba016f75"


class FakeApi:
    def get(self, path, params, *args, **kwargs):
        if path == TOKENS:
            data = [{"binanceChainId": "56", "tokenContractAddress": CONTRACT,
                     "platformId": "bstock", "underlyingTicker": "NVDA", "assetType": 1,
                     "tokenSymbol": "NVDAB", "tokenToShareRatio": "1", "statusInfo": {"marketStatus": "offhours"}}]
        elif path == PRICE:
            data = [{"tokenContractAddress": CONTRACT, "tokenPrice": "100",
                     "referencePrice": "100", "tokenPriceUpdatedAt": 1791111000000}]
        elif path == UNDERLYING_MARKET:
            data = {"statusInfo": {"marketStatus": "offhours", "openState": True},
                    "marketData": {"referencePrice": "100"}}
        elif path == QUOTE:
            query = dict(params)
            data = [{"isBest": True, "executionMode": "SWAP", "vendorName": "TestVendor",
                     "priceImpactPercent": "0.01", "binanceChainId": "56",
                     "fromToken": {"tokenContractAddress": USDT},
                     "toToken": {"tokenContractAddress": query["toTokenAddress"]},
                     "fromTokenAmount": query["amount"], "toTokenAmount": "100000000000000000"}]
        else:
            raise AssertionError("unexpected endpoint")
        return {"code": 0, "data": data}, "2026-10-04T10:10:00.000Z", "synthetic-hash"


class FakeOndoApi(FakeApi):
    def get(self, path, params, *args, **kwargs):
        result, at, digest = super().get(path, params, *args, **kwargs)
        if path == TOKENS:
            result["data"][0].update({"tokenContractAddress": ONDO_CONTRACT,
                                       "platformId": "ondo", "tokenSymbol": "NVDAon"})
        elif path == PRICE:
            result["data"][0]["tokenContractAddress"] = ONDO_CONTRACT
        return result, at, digest


class FakeWrongQuoteApi(FakeApi):
    def get(self, path, params, *args, **kwargs):
        result, at, digest = super().get(path, params, *args, **kwargs)
        if path == QUOTE:
            result["data"][0]["toToken"]["tokenContractAddress"] = ONDO_CONTRACT
        return result, at, digest


class FakeZeroOutputQuoteApi(FakeApi):
    def get(self, path, params, *args, **kwargs):
        result, at, digest = super().get(path, params, *args, **kwargs)
        if path == QUOTE:
            result["data"][0]["toTokenAmount"] = "0"
        return result, at, digest


def fake_rpc(calls, block, experiment):
    methods = [row["method"] for row in calls]
    if methods == ["eth_blockNumber"]:
        return [{"id": 1, "result": "0x1"}], b"", "2026-10-04T10:10:00Z", "head-hash"
    if methods == ["eth_getBlockByNumber"]:
        return [{"id": 2, "result": {"timestamp": "0x6a621638"}}], b"", "2026-10-04T10:10:00Z", "block-hash"
    return [{"id": 10, "result": hex(10**18)}, {"id": 11, "result": hex(10**18)},
            {"id": 12, "result": "0x0"}], b"", "2026-10-04T10:10:00Z", "values-hash"


class SafetyServiceTests(unittest.TestCase):
    def test_invalid_amount_never_calls_api(self):
        with self.assertRaises(ValueError):
            validate({"provider": "bstock", "notional_usdt": "NaN",
                      "max_notional_usdt": "100", "max_price_impact_percent": "0.5"})

    def test_wallet_secret_field_rejected_before_api(self):
        with self.assertRaises(ValueError):
            validate({"provider": "bstock", "notional_usdt": "100",
                      "max_notional_usdt": "100", "max_price_impact_percent": "0.5",
                      "private_key": "synthetic-do-not-use"})

    def test_agent_tool_deny_is_a_receipt_not_transport_failure(self):
        request = {"provider": "bstock", "notional_usdt": "100",
                   "max_notional_usdt": "20", "max_price_impact_percent": "0.5"}
        output = io.StringIO()
        with patch("sys.stdin", io.TextIOWrapper(io.BytesIO(json.dumps(request).encode()))), redirect_stdout(output):
            code = agent_tool_main(review_fn=lambda data: review(data, api=FakeApi(), rpc=fake_rpc))
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("MANDATE_LIMIT_EXCEEDED", result["reason_codes"])

    def test_offhours_and_unknown_reference_need_human(self):
        result = review({"provider": "bstock", "notional_usdt": "100",
                         "max_notional_usdt": "100", "max_price_impact_percent": "0.5"},
                        api=FakeApi(), rpc=fake_rpc)
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("UNDERLYING_MARKET_NOT_REGULAR", result["reason_codes"])
        self.assertIn("INDEPENDENT_REFERENCE_TIME_UNKNOWN", result["reason_codes"])
        self.assertEqual(result["view"]["reference_age_status"], "UNKNOWN")
        self.assertEqual(result["view"]["execution_mode"], "SWAP")
        self.assertEqual(result["view"]["multiplier_integrity"], "MATCHED_FIXED_BLOCK")
        self.assertEqual(len(result["receipt"]["receipt_sha256"]), 64)

    def test_exact_wallet_route_context_is_internal_and_bound(self):
        wallet = "0x" + "a" * 40
        request = {"provider": "bstock", "notional_usdt": "100",
                   "max_notional_usdt": "100", "max_price_impact_percent": "0.5"}
        public = review(request, api=FakeApi(), rpc=fake_rpc)
        self.assertNotIn("route_context", public)
        result, context = review(request, api=FakeApi(), rpc=fake_rpc,
                                 quote_wallet=wallet, return_route_context=True)
        self.assertEqual(context["wallet"], wallet)
        self.assertEqual(context["raw_amount"], str(100 * 10**18))
        self.assertEqual(context["quote_sha256"], result["sources"]["quote"]["sha256"])
        self.assertEqual(context["route"]["toToken"]["tokenContractAddress"], CONTRACT)
        with self.assertRaises(ValueError):
            review(request, api=FakeApi(), rpc=fake_rpc, return_route_context=True)

    def test_mandate_denies_even_with_route(self):
        result = review({"provider": "bstock", "notional_usdt": "100",
                         "max_notional_usdt": "20", "max_price_impact_percent": "0.5"},
                        api=FakeApi(), rpc=fake_rpc)
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("MANDATE_LIMIT_EXCEEDED", result["reason_codes"])

    def test_mismatched_route_is_not_actionable(self):
        result = review({"provider": "bstock", "notional_usdt": "100",
                         "max_notional_usdt": "100", "max_price_impact_percent": "0.5"},
                        api=FakeWrongQuoteApi(), rpc=fake_rpc)
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("QUOTE_INTENT_MISMATCH", result["reason_codes"])
        self.assertEqual(result["view"]["route"], "MISMATCH")
        self.assertFalse(result["receipt"]["evidence"]["quote_identity_match"])

    def test_zero_output_route_is_not_actionable(self):
        result = review({"provider": "bstock", "notional_usdt": "100",
                         "max_notional_usdt": "100", "max_price_impact_percent": "0.5"},
                        api=FakeZeroOutputQuoteApi(), rpc=fake_rpc)
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("QUOTE_INTENT_MISMATCH", result["reason_codes"])

    def test_untimed_stock_feed_never_populates_reference_age(self):
        result = review({"provider": "ondo", "notional_usdt": "100",
                         "max_notional_usdt": "100", "max_price_impact_percent": "0.5"},
                        api=FakeOndoApi(), stock_info=lambda contract: (
                            {"ticker": "NVDA", "symbol": "NVDAon", "stockInfo": {"price": "101"}},
                            "2026-10-04T10:10:00.000Z", "synthetic-stock-hash"))
        self.assertEqual(result["view"]["stock_feed_price_usd"], "101")
        self.assertIsNone(result["view"]["stock_feed_price_asof"])
        self.assertIn("INDEPENDENT_REFERENCE_TIME_UNKNOWN", result["reason_codes"])
        self.assertEqual(result["receipt"]["evidence"]["reference_age_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
