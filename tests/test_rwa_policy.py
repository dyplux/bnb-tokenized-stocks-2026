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
                         "token_to_share_ratio": "1", "previous_token_to_share_ratio": "1",
                         "corporate_action_verified": False, "market_status": "regular", "market_reason": None,
                         "token_price_age_ms": 1000, "independent_reference_timestamp": "synthetic",
                         "quote_available": True, "price_impact_percent": "0.1", "simulation_passed": True}
        self.mandate = {"max_token_price_age_ms": 60000, "max_notional_usd": "200",
                        "max_price_impact_percent": "1"}
        self.now = datetime(2026, 10, 4, tzinfo=timezone.utc)

    def run_policy(self):
        return evaluate(self.intent, self.evidence, self.mandate, now=self.now)

    def test_synthetic_baseline_allow(self):
        result = self.run_policy()
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(len(result["receipt_sha256"]), 64)

    def test_live_api_missing_reference_time_needs_human(self):
        self.evidence["independent_reference_timestamp"] = None
        result = self.run_policy()
        self.assertEqual(result["decision"], "NEED_HUMAN")
        self.assertIn("INDEPENDENT_REFERENCE_TIME_UNKNOWN", result["reason_codes"])

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


if __name__ == "__main__":
    unittest.main()
