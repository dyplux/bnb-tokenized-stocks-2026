"""The live-policy probe must not fill missing live gates with synthetic success."""

import unittest

from scripts.probe_live_policy import probe


class LivePolicyProbeTest(unittest.TestCase):
    def test_unknown_live_gates_need_human(self):
        row = {"observed_at": "2026-10-04T12:00:00Z", "chain_id": "56", "ticker": "TEST",
               "provider": "bstock", "contract": "0x" + "1" * 40, "token_to_share_ratio": "1",
               "market_status": "regular", "market_reason": None, "token_price_age_ms": 1000,
               "token_price_age_calculation": "observed_at_minus_tokenPriceUpdatedAt",
               "reference_price_updated_at": None, "reference_age_seconds": None,
               "reference_age_status": "UNKNOWN", "catalog_sha256": "a", "price_response_sha256": "b"}
        result = probe(row)
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("INDEPENDENT_REFERENCE_TIME_UNKNOWN", result["reason_codes"])
        self.assertIn("QUOTE_UNVERIFIED", result["reason_codes"])
        self.assertIn("SIMULATION_UNVERIFIED", result["reason_codes"])


if __name__ == "__main__":
    unittest.main()
