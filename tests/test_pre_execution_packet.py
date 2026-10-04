"""Synthetic checks for the read-only pre-execution evidence packet."""

import unittest
from datetime import datetime, timezone

from app.pre_execution_packet import assemble, digest
from app.server import USDT

ASSEMBLY_TIME = datetime(2026, 10, 4, 10, 0, 30, tzinfo=timezone.utc)


def examples():
    contract = "0x" + "a" * 40
    receipt = {"decision": "ALLOW", "reason_codes": [],
               "intent": {"chain_id": "56", "ticker": "NVDA", "provider": "bstock",
                          "contract": contract, "notional_usd": "10"},
               "evidence": {"source_response_sha256": {"quote": "same-quote-hash"}}}
    receipt["receipt_sha256"] = digest(receipt)
    review = {"origin": "LIVE_READ_ONLY", "decision": "ALLOW", "reason_codes": [],
              "receipt": receipt, "sources": {"quote": {"sha256": "same-quote-hash",
                                                  "observed_at": "2026-10-04T10:00:00Z"}}}
    dry_run = {"origin": "LIVE_READ_ONLY", "chain_id": "56", "side": "BUY",
               "source_token": USDT, "notional_usdt": "10", "provider": "bstock", "stage": "SIMULATED",
               "security": {"ticker": "NVDA", "contract": contract},
               "quote": {"business_code": 0, "intent_match": True,
                         "bound_to_policy": True, "sha256": "same-quote-hash",
                         "observed_at": "2026-10-04T10:00:00Z"},
               "build": {"business_code": 0, "quote_build_intent_match": True},
               "simulation": {"api_business_code": 0, "predicted_transaction_status": "SUCCESS"}}
    return review, dry_run


class PreExecutionPacketTests(unittest.TestCase):
    def test_even_all_positive_read_only_evidence_does_not_authorize_execution(self):
        review, trial = examples()
        packet = assemble(review, trial, now=ASSEMBLY_TIME)
        self.assertEqual(packet["state"], "BLOCKED")
        self.assertFalse(packet["execution_authorized"])
        self.assertEqual(packet["reason_codes"], ["EXPLICIT_HUMAN_APPROVAL_MISSING"])
        self.assertEqual(packet["packet_sha256"], digest({k: v for k, v in packet.items()
                                                      if k != "packet_sha256"}))
        self.assertEqual(packet["policy"]["receipt_sha256"],
                         digest({k: v for k, v in packet["policy"]["receipt"].items()
                                 if k != "receipt_sha256"}))

    def test_invalid_receipt_mismatched_action_and_failed_simulation_block(self):
        review, trial = examples()
        review["receipt"]["decision"] = "NEED_HUMAN"
        trial["security"]["contract"] = "0x" + "b" * 40
        trial["simulation"]["predicted_transaction_status"] = "FAILED"
        codes = assemble(review, trial, now=ASSEMBLY_TIME)["reason_codes"]
        for code in ("POLICY_RECEIPT_INVALID", "POLICY_NOT_ALLOW",
                     "POLICY_RESULT_MISMATCH", "ACTION_EVIDENCE_MISMATCH",
                     "EXACT_WALLET_SIMULATION_NOT_PASSED"):
            self.assertIn(code, codes)

    def test_separate_quote_cannot_be_treated_as_bound(self):
        review, trial = examples()
        trial["quote"]["sha256"] = "another-quote"
        self.assertIn("POLICY_QUOTE_NOT_BOUND_TO_EXECUTION",
                      assemble(review, trial, now=ASSEMBLY_TIME)["reason_codes"])

    def test_stale_quote_is_explicitly_blocked(self):
        review, trial = examples()
        packet = assemble(review, trial, now=datetime(2026, 10, 4, 10, 2, tzinfo=timezone.utc))
        self.assertIn("QUOTE_TOO_OLD", packet["reason_codes"])
        self.assertEqual(packet["exact_wallet_trial"]["quote_age_seconds_at_assembly"], 120)
        self.assertEqual(packet["exact_wallet_trial"]["provider_quote_expiry"],
                         "NOT_EXPOSED_IN_OBSERVED_ROUTE")

    def test_unknown_or_future_quote_time_is_explicitly_blocked(self):
        review, trial = examples()
        trial["quote"]["observed_at"] = "no timestamp"
        self.assertIn("QUOTE_TIME_UNVERIFIED",
                      assemble(review, trial, now=ASSEMBLY_TIME)["reason_codes"])
        trial["quote"]["observed_at"] = "2026-10-04T10:01:00Z"
        self.assertIn("QUOTE_TIME_IN_FUTURE",
                      assemble(review, trial, now=ASSEMBLY_TIME)["reason_codes"])


if __name__ == "__main__":
    unittest.main()
