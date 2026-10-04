"""Detect a live collector process stuck inside one collection attempt."""

import unittest
from datetime import datetime, timezone

from scripts.rwa_research import collecting_stalled


class CollectorHealthTest(unittest.TestCase):
    def test_collecting_stalled_after_limit(self):
        now = datetime(2026, 10, 4, 12, 10, tzinfo=timezone.utc).timestamp()
        state = {"state": "collecting", "last_attempt_at": "2026-10-04T12:08:20Z"}
        self.assertTrue(collecting_stalled(state, now))

    def test_active_collecting_or_running_is_not_stalled(self):
        now = datetime(2026, 10, 4, 12, 10, tzinfo=timezone.utc).timestamp()
        self.assertFalse(collecting_stalled({"state": "collecting", "last_attempt_at": "2026-10-04T12:09:00Z"}, now))
        self.assertFalse(collecting_stalled({"state": "running"}, now))

    def test_missing_collecting_start_is_unhealthy(self):
        now = datetime(2026, 10, 4, 12, 10, tzinfo=timezone.utc).timestamp()
        self.assertTrue(collecting_stalled({"state": "collecting"}, now))


if __name__ == "__main__":
    unittest.main()
