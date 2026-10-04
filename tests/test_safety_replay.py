"""The offline example must remain a labelled, authentic dated receipt."""

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "app/fixtures/safety-nvdab-2026-10-04.json"


class SafetyReplayTests(unittest.TestCase):
    def test_example_is_dated_and_receipt_hash_matches(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(data["origin"], "DATED_REPLAY")
        self.assertEqual(data["captured_origin"], "LIVE_READ_ONLY")
        self.assertEqual(data["decision"], "NEED_HUMAN")
        self.assertIn("INDEPENDENT_REFERENCE_TIME_UNKNOWN", data["reason_codes"])
        self.assertIsNone(data["receipt"]["evidence"]["reference_price_updated_at"])
        receipt = dict(data["receipt"])
        expected = receipt.pop("receipt_sha256")
        encoded = json.dumps(receipt, sort_keys=True, separators=(",", ":"), default=str).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), expected)

    def test_example_contains_no_wallet_or_signing_material(self):
        data = FIXTURE.read_text(encoding="utf-8")
        for forbidden in ("private_key", "quoteId", "userWalletAddress", "X-OC-APIKEY", "X-OC-SIGN"):
            self.assertNotIn(forbidden, data)


if __name__ == "__main__":
    unittest.main()
