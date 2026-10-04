import gzip
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_market_tape.py"
SPEC = importlib.util.spec_from_file_location("audit_market_tape", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class AuditMarketTapeTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.market = self.root / "data" / "market_hours"
        (self.market / "raw").mkdir(parents=True)
        (self.market / "checkpoint.json").write_text(json.dumps({"contracts_sampled": 2}), encoding="utf-8")

    def tearDown(self):
        self.tempdir.cleanup()

    def write_fixture(self, rows, manifest_entries=(), gaps=None, errors=None):
        tape = self.market / "2026-10-04.jsonl"
        tape.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        (self.market / "raw" / "manifest.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in manifest_entries), encoding="utf-8")
        if gaps is not None:
            (self.market / "gaps.jsonl").write_text("".join(json.dumps(row) + "\n" for row in gaps), encoding="utf-8")
        if errors is not None:
            (self.market / "errors.jsonl").write_text("".join(json.dumps(row) + "\n" for row in errors), encoding="utf-8")

    def row(self, slot, contract, sample_id, digest=None, age_marker=True, age=1000):
        row = {
            "origin": "LIVE", "slot": slot, "contract": contract, "sample_id": sample_id,
            "independent_reference_timestamp": None, "reference_price_updated_at": None,
            "reference_age_seconds": None, "reference_age_status": "UNKNOWN",
            "observed_at": "2026-10-04T10:00:01.000Z", "token_price_updated_at_ms": 1791108001000,
        }
        if digest:
            row["price_response_sha256"] = digest
        if age_marker:
            row.update({"token_price_age_calculation": AUDIT.EXPECTED_AGE_CALCULATION,
                        "token_price_age_ms": age})
        return row

    def test_valid_tape_counts_partial_slots_legacy_rows_and_recorded_files(self):
        body = b'{"ok":true}'
        compressed = gzip.compress(body)
        digest = hashlib.sha256(body).hexdigest()
        raw_path = self.market / "raw" / (digest + ".json.gz")
        raw_path.write_bytes(compressed)
        manifest = {"path": str(raw_path), "sha256": digest, "captured_at": "2026-10-04T10:01:00Z"}
        rows = [self.row(1, "a", "one", digest, age_marker=True, age=0),
                self.row(2, "a", "three", digest, age_marker=False),
                self.row(2, "b", "four", digest, age_marker=True, age=0)]
        self.write_fixture(rows, [manifest], gaps=[{"slot": 3}], errors=[{"error": "timeout"}])
        result = AUDIT.audit(self.root, "2026-10-04")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["partial_initial_slots"], [{"slot": 1, "distinct_contracts": 1}])
        self.assertEqual(result["legacy_age_rows_counted"], 1)
        self.assertEqual(result["recorded_gaps"], 1)
        self.assertEqual(result["recorded_errors"], 1)

    def test_detects_duplicate_sample_and_bad_current_age(self):
        rows = [self.row(1, "a", "same", age_marker=True, age=0), self.row(2, "b", "same", age_marker=True, age=99)]
        self.write_fixture(rows)
        result = AUDIT.audit(self.root, "2026-10-04")
        self.assertFalse(result["ok"])
        self.assertTrue(any("duplicate LIVE" in item for item in result["violations"]))
        self.assertTrue(any("token_price_age_ms" in item for item in result["violations"]))

    def test_detects_missing_manifest_hash_and_corrupt_gzip(self):
        body = b"not gzip"
        path = self.market / "raw" / "body.json.gz"
        path.write_bytes(body)
        digest = hashlib.sha256(body).hexdigest()
        self.write_fixture([self.row(1, "a", "one", digest)], [{"path": str(path), "sha256": digest,
                                                                  "captured_at": "2026-10-04T09:59:00Z"}])
        result = AUDIT.audit(self.root, "2026-10-04")
        self.assertFalse(result["ok"])
        self.assertTrue(any("invalid gzip" in item for item in result["violations"]))

    def test_pre_retention_missing_hash_and_reference_status_are_reported_as_legacy(self):
        old = self.row(1, "a", "old", "legacy-hash", age_marker=False)
        del old["reference_age_status"]
        body = b'{"ok":true}'
        digest = hashlib.sha256(body).hexdigest()
        raw_path = self.market / "raw" / (digest + ".json.gz")
        raw_path.write_bytes(gzip.compress(body))
        current = self.row(2, "a", "new", digest, age=0)
        self.write_fixture([old, current], [{"path": str(raw_path), "sha256": digest,
                                             "captured_at": "2026-10-04T10:01:00Z"}])
        result = AUDIT.audit(self.root, "2026-10-04")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["legacy_reference_status_missing"], 1)
        self.assertEqual(result["legacy_unmanifested_price_hashes"], 1)
        self.assertEqual(result["verified_raw_responses"], 1)

    def test_post_retention_missing_hash_and_reference_status_fail(self):
        body = b'{"ok":true}'
        digest = hashlib.sha256(body).hexdigest()
        raw_path = self.market / "raw" / (digest + ".json.gz")
        raw_path.write_bytes(gzip.compress(body))
        bad = self.row(1, "a", "new", "missing-hash")
        del bad["reference_age_status"]
        self.write_fixture([bad], [{"path": str(raw_path), "sha256": digest,
                                    "captured_at": "2026-10-04T09:59:00Z"}])
        result = AUDIT.audit(self.root, "2026-10-04")
        self.assertFalse(result["ok"])
        self.assertTrue(any("reference_age_status" in item for item in result["violations"]))
        self.assertTrue(any("absent from manifest" in item for item in result["violations"]))

    def test_missing_tape_and_manifest_are_clear_failures(self):
        result = AUDIT.audit(self.root, "2026-10-04")
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing:" in item for item in result["violations"]))


if __name__ == "__main__":
    unittest.main()
