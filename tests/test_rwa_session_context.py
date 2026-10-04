"""Check the explicit New York time boundaries used by EXP-RWA-010."""

import unittest
from datetime import datetime, timezone

from scripts.analyze_rwa import session_context


class SessionContextTest(unittest.TestCase):
    def test_weekend(self):
        self.assertEqual(session_context(datetime(2026, 10, 4, 12, tzinfo=timezone.utc)), "weekend")

    def test_weekday_premarket(self):
        self.assertEqual(session_context(datetime(2026, 10, 5, 12, tzinfo=timezone.utc)), "weekday_premarket")

    def test_weekday_regular(self):
        self.assertEqual(session_context(datetime(2026, 10, 5, 14, tzinfo=timezone.utc)), "weekday_regular")

    def test_weekday_afterhours(self):
        self.assertEqual(session_context(datetime(2026, 10, 5, 21, tzinfo=timezone.utc)), "weekday_afterhours")

    def test_weekday_outside_published_sessions(self):
        self.assertEqual(session_context(datetime(2026, 10, 6, 1, tzinfo=timezone.utc)), "weekday_outside_published_sessions")


if __name__ == "__main__":
    unittest.main()
