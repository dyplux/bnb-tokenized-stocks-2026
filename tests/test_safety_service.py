"""Synthetic contract tests for the local read-only judge flow."""

import unittest

from app.safety_service import multiplier, review, validate
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
            data = [{"isBest": True, "executionMode": "SWAP", "vendorName": "TestVendor",
                     "priceImpactPercent": "0.01"}]
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

    def test_mandate_denies_even_with_route(self):
        result = review({"provider": "bstock", "notional_usdt": "100",
                         "max_notional_usdt": "20", "max_price_impact_percent": "0.5"},
                        api=FakeApi(), rpc=fake_rpc)
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("MANDATE_LIMIT_EXCEEDED", result["reason_codes"])

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
