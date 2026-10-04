import json
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from app.rwa_policy import evaluate


ROOT = Path(__file__).resolve().parents[1]


class PolicyFixtureTest(unittest.TestCase):
    def setUp(self):
        self.intent = {"chain_id": "56", "ticker": "TEST", "provider": "fixture",
                       "contract": "0x" + "1" * 40, "notional_usd": "100"}
        self.evidence = {"chain_id": "56", "ticker": "TEST", "provider": "fixture",
                         "contract": self.intent["contract"], "issuer_verified": True,
                         "eligibility_status": "ELIGIBLE", "eligibility_basis": "synthetic_fixture_only",
                         "eligibility_checked_at": "2026-10-04T00:00:00Z",
                         "token_to_share_ratio": "1", "previous_token_to_share_ratio": "1",
                         "corporate_action_verified": False, "market_status": "regular", "market_reason": None,
                         "token_price_age_ms": 1000,
                         "token_price_age_calculation": "observed_at_minus_tokenPriceUpdatedAt",
                         "reference_price_updated_at": "synthetic", "reference_age_seconds": 10,
                         "reference_age_status": "OBSERVED",
                         "quote_available": True, "price_impact_percent": "0.1", "simulation_passed": True}
        self.mandate = {"max_token_price_age_ms": 60000, "require_independent_reference": True,
                        "max_reference_age_seconds": 60, "max_notional_usd": "200",
                        "max_price_impact_percent": "1", "max_eligibility_age_seconds": 3600}
        self.now = datetime(2026, 10, 4, tzinfo=timezone.utc)

    def run_policy(self):
        return evaluate(self.intent, self.evidence, self.mandate, now=self.now)

    def test_synthetic_baseline_allow(self):
        result = self.run_policy()
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(len(result["receipt_sha256"]), 64)

    def test_quote_without_user_access_needs_human(self):
        self.evidence["eligibility_status"] = "UNKNOWN"
        result = self.run_policy()
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("USER_ELIGIBILITY_UNKNOWN", result["reason_codes"])

    def test_explicit_user_ineligibility_denies(self):
        self.evidence["eligibility_status"] = "INELIGIBLE"
        result = self.run_policy()
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("USER_INELIGIBLE", result["reason_codes"])

    def test_stale_user_access_needs_human(self):
        self.evidence["eligibility_checked_at"] = "2026-10-03T20:00:00Z"
        result = self.run_policy()
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("USER_ELIGIBILITY_STALE", result["reason_codes"])

    def test_live_api_missing_reference_time_needs_human(self):
        self.evidence["reference_price_updated_at"] = None
        self.evidence["reference_age_status"] = "UNKNOWN"
        result = self.run_policy()
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("INDEPENDENT_REFERENCE_TIME_UNKNOWN", result["reason_codes"])

    def test_stale_independent_reference_denies(self):
        self.evidence["reference_age_seconds"] = 61
        result = self.run_policy()
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("INDEPENDENT_REFERENCE_STALE", result["reason_codes"])

    def test_missing_reference_age_needs_human_even_with_timestamp(self):
        self.evidence["reference_age_seconds"] = None
        self.assertIn("INDEPENDENT_REFERENCE_AGE_UNKNOWN", self.run_policy()["reason_codes"])

    def test_reference_requirement_can_be_explicitly_waived(self):
        self.mandate["require_independent_reference"] = False
        self.evidence["reference_price_updated_at"] = None
        self.evidence["reference_age_seconds"] = None
        self.evidence["reference_age_status"] = "UNKNOWN"
        result = self.run_policy()
        self.assertEqual(result["decision"], "ALLOW")
        self.assertFalse(any(code.startswith("INDEPENDENT_REFERENCE_") for code in result["reason_codes"]))

    def test_legacy_token_age_without_observation_clock_needs_human(self):
        self.evidence.pop("token_price_age_calculation")
        result = self.run_policy()
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("TOKEN_PRICE_AGE_PROVENANCE_UNKNOWN", result["reason_codes"])

    def test_future_token_timestamp_needs_human(self):
        self.evidence["token_price_age_ms"] = -1000
        self.assertIn("TOKEN_PRICE_AGE_UNKNOWN", self.run_policy()["reason_codes"])

    def test_corporate_action_fixture_rejects_unverified_ratio_change(self):
        fixtures = json.loads((ROOT / "experiments/EXP-RWA-011/corporate_action_fixtures.json").read_text())
        for case in fixtures["cases"][:3]:
            with self.subTest(case=case["id"]):
                self.evidence["previous_token_to_share_ratio"] = case["before"]["token_to_share_ratio"]
                self.evidence["token_to_share_ratio"] = case["after"]["token_to_share_ratio"]
                result = self.run_policy()
                self.assertEqual(result["decision"], "DENY")
                self.assertIn(case["policy_reason_without_verified_action"], result["reason_codes"])
                for point in ("before", "after"):
                    normalized = Decimal(case[point]["token_price_usd"]) / Decimal(case[point]["token_to_share_ratio"])
                    self.assertEqual(normalized, Decimal(case["normalized_per_share_" + point + "_usd"]))

    def test_synthetic_halt_denies(self):
        self.evidence["market_status"] = "pause"
        self.evidence["market_reason"] = "ASSET_PAUSED"
        result = self.run_policy()
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("ASSET_PAUSED", result["reason_codes"])

    def test_no_quote_denies(self):
        self.evidence["quote_available"] = False
        self.assertIn("NO_EXECUTABLE_QUOTE", self.run_policy()["reason_codes"])

    def test_negative_price_impact_above_magnitude_limit_denies(self):
        self.evidence["price_impact_percent"] = "-1.1"
        result = self.run_policy()
        self.assertEqual(result["decision"], "DENY")
        self.assertIn("PRICE_IMPACT_LIMIT_EXCEEDED", result["reason_codes"])

    def test_nonpositive_impact_limit_needs_human(self):
        self.mandate["max_price_impact_percent"] = "0"
        self.assertIn("PRICE_IMPACT_UNKNOWN", self.run_policy()["reason_codes"])


if __name__ == "__main__":
    unittest.main()
