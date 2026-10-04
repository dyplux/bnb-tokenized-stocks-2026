"""Synthetic ratio-change boundaries for the passive live-tape audit."""

import unittest

from scripts.audit_ratio_transitions import transitions


def row(at, value):
    return {"observed_at": at, "ticker": "TEST", "provider": "ondo",
            "contract": "0x" + "1" * 40, "token_to_share_ratio": value,
            "catalog_sha256": at}


class RatioTransitionTest(unittest.TestCase):
    def test_unchanged_numeric_ratio_is_not_an_event(self):
        found, missing = transitions([row("2026-10-04T10:00:00Z", "1"),
                                      row("2026-10-04T10:05:00Z", "1.000")])
        self.assertEqual(found, [])
        self.assertEqual(missing, 0)

    def test_change_is_candidate_without_issuer_proof(self):
        found, missing = transitions([row("2026-10-04T10:00:00Z", "1"),
                                      row("2026-10-04T10:05:00Z", "2")])
        self.assertEqual(missing, 0)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["ratio_change_pct"], "100")
        self.assertFalse(found[0]["issuer_event_verified"])

    def test_missing_ratio_is_counted_without_fabricated_transition(self):
        found, missing = transitions([row("2026-10-04T10:00:00Z", "1"),
                                      row("2026-10-04T10:05:00Z", None),
                                      row("2026-10-04T10:10:00Z", "1")])
        self.assertEqual(found, [])
        self.assertEqual(missing, 1)


if __name__ == "__main__":
    unittest.main()
