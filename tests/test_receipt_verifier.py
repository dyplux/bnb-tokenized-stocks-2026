import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_receipt.py"
NEED_HUMAN = ROOT / "docs" / "judge" / "observed-unsafe.json"
DENY = ROOT / "docs" / "judge" / "observed-mandate-deny.json"
ALLOW = ROOT / "docs" / "judge" / "synthetic-safe.json"


def digest(receipt):
    body = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


class ReceiptVerifierTest(unittest.TestCase):
    def run_path(self, path, expected=None):
        command = [sys.executable, str(SCRIPT), str(path)]
        if expected is not None:
            command.extend(["--expected-sha256", expected])
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                   timeout=10, check=False)
        self.assertLessEqual(len(completed.stdout), 4096)
        self.assertEqual(completed.stderr, "")
        return completed.returncode, json.loads(completed.stdout)

    def run_document(self, document, expected=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            if isinstance(document, str):
                path.write_text(document, encoding="utf-8")
            else:
                path.write_text(json.dumps(document), encoding="utf-8")
            return self.run_path(path, expected)

    def test_wrong_field_types_produce_invalid_receipt_without_traceback(self):
        for field, value in [("decision", []), ("checks", {"X": []}), ("timestamp", "")]:
            receipt = copy.deepcopy(self.load(NEED_HUMAN)["receipt"])
            receipt[field] = value
            code, result = self.run_document(receipt)
            self.assertEqual((code, result["status"]), (2, "INVALID_RECEIPT"))

    def test_json_numeric_overflow_produces_invalid_receipt(self):
        document = json.dumps(self.load(NEED_HUMAN)["receipt"]).replace('"100"', '1e999', 1)
        self.assertIn("1e999", document)
        code, result = self.run_document(document)
        self.assertEqual((code, result["status"]), (2, "INVALID_RECEIPT"))

    def load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_observed_need_human_wrapper_matches(self):
        code, result = self.run_path(NEED_HUMAN)
        self.assertEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MATCH")
        self.assertEqual(result["replay"], "REPLAY_MATCH")
        self.assertIn("not authenticity", result["integrity_scope"])

    def test_observed_deny_wrapper_matches(self):
        code, result = self.run_path(DENY)
        self.assertEqual((code, result["replay"]), (0, "REPLAY_MATCH"))

    def test_synthetic_allow_wrapper_matches(self):
        code, result = self.run_path(ALLOW)
        self.assertEqual((code, result["replay"]), (0, "REPLAY_MATCH"))

    def test_direct_receipt_matches(self):
        receipt = self.load(NEED_HUMAN)["receipt"]
        code, result = self.run_document(receipt)
        self.assertEqual((code, result["integrity"]), (0, "INTEGRITY_MATCH"))

    def test_amount_tampering_is_integrity_mismatch(self):
        document = self.load(NEED_HUMAN)
        document["receipt"]["intent"]["notional_usd"] = "101"
        code, result = self.run_document(document)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MISMATCH")

    def test_reason_code_tampering_is_integrity_mismatch(self):
        document = self.load(NEED_HUMAN)
        document["receipt"]["reason_codes"].append("MADE_UP")
        code, result = self.run_document(document)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MISMATCH")

    def test_rehashed_version_tampering_is_unsupported(self):
        receipt = copy.deepcopy(self.load(NEED_HUMAN)["receipt"])
        receipt["policy_version"] = "9.9.9"
        receipt["receipt_sha256"] = digest(receipt)
        code, result = self.run_document(receipt)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MATCH")
        self.assertEqual(result["policy"], "POLICY_VERSION_UNSUPPORTED")

    def test_wrong_external_expected_hash_is_integrity_mismatch(self):
        code, result = self.run_path(NEED_HUMAN, "0" * 64)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MISMATCH")

    def test_external_expected_hash_accepts_known_receipt(self):
        expected = self.load(NEED_HUMAN)["receipt"]["receipt_sha256"]
        code, result = self.run_path(NEED_HUMAN, expected)
        self.assertEqual((code, result["integrity"]), (0, "INTEGRITY_MATCH"))

    def test_rehashed_tampering_is_caught_by_external_hash(self):
        receipt = copy.deepcopy(self.load(NEED_HUMAN)["receipt"])
        original = receipt["receipt_sha256"]
        receipt["intent"]["notional_usd"] = "101"
        receipt["receipt_sha256"] = digest(receipt)
        code, result = self.run_document(receipt, original)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MISMATCH")

    def test_rehashed_decision_tampering_replay_mismatches(self):
        receipt = copy.deepcopy(self.load(NEED_HUMAN)["receipt"])
        receipt["decision"] = "ALLOW"
        receipt["receipt_sha256"] = digest(receipt)
        code, result = self.run_document(receipt)
        self.assertNotEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MATCH")
        self.assertEqual(result["replay"], "REPLAY_MISMATCH")

    def test_invalid_json_is_invalid_receipt(self):
        code, result = self.run_document("{broken")
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "INVALID_RECEIPT")

    def test_nonfinite_number_is_invalid_receipt(self):
        code, result = self.run_document('{"receipt":{"amount":NaN}}')
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "INVALID_RECEIPT")

    def test_duplicate_key_is_invalid_receipt(self):
        code, result = self.run_document('{"receipt":{},"receipt":{}}')
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "INVALID_RECEIPT")

    def test_invalid_shape_is_invalid_receipt(self):
        code, result = self.run_document({"receipt": []})
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "INVALID_RECEIPT")

    def test_missing_projection_context_is_replay_unavailable_and_successful(self):
        receipt = copy.deepcopy(self.load(NEED_HUMAN)["receipt"])
        del receipt["evidence"]["simulation_passed"]
        receipt["receipt_sha256"] = digest(receipt)
        code, result = self.run_document(receipt)
        self.assertEqual(code, 0)
        self.assertEqual(result["integrity"], "INTEGRITY_MATCH")
        self.assertEqual(result["replay"], "REPLAY_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
