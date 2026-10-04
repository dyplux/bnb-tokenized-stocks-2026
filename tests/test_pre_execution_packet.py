"""Synthetic checks for the read-only pre-execution evidence packet."""

import unittest

from app.pre_execution_packet import assemble, digest
from app.server import USDT


def examples():
    contract = "0x" + "a" * 40
    receipt = {"decision": "ALLOW", "reason_codes": [],
               "intent": {"chain_id": "56", "ticker": "NVDA", "provider": "bstock",
                          "contract": contract, "notional_usd": "10"}}
    receipt["receipt_sha256"] = digest(receipt)
    review = {"origin": "LIVE_READ_ONLY", "decision": "ALLOW", "reason_codes": [],
              "receipt": receipt}
    dry_run = {"origin": "LIVE_READ_ONLY", "chain_id": "56", "side": "BUY",
               "source_token": USDT, "notional_usdt": "10", "provider": "bstock", "stage": "SIMULATED",
               "security": {"ticker": "NVDA", "contract": contract},
               "quote": {"business_code": 0, "intent_match": True},
               "build": {"business_code": 0, "quote_build_intent_match": True},
               "simulation": {"api_business_code": 0, "predicted_transaction_status": "SUCCESS"}}
    return review, dry_run


class PreExecutionPacketTests(unittest.TestCase):
    def test_even_all_positive_read_only_evidence_does_not_authorize_execution(self):
        review, trial = examples()
        packet = assemble(review, trial)
        self.assertEqual(packet["state"], "BLOCKED")
        self.assertFalse(packet["execution_authorized"])
        self.assertEqual(packet["reason_codes"], ["EXPLICIT_HUMAN_APPROVAL_MISSING",
                                                  "POLICY_QUOTE_NOT_BOUND_TO_EXECUTION"])
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
        codes = assemble(review, trial)["reason_codes"]
        for code in ("POLICY_RECEIPT_INVALID", "POLICY_NOT_ALLOW",
                     "POLICY_RESULT_MISMATCH", "ACTION_EVIDENCE_MISMATCH",
                     "EXACT_WALLET_SIMULATION_NOT_PASSED"):
            self.assertIn(code, codes)


if __name__ == "__main__":
    unittest.main()
