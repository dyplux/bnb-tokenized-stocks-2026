from email.message import Message
from io import BytesIO
import json
import time
import unittest
from unittest.mock import Mock, patch

from app.server import Handler, QuoteRequestBudget


WALLET = "0x" + "1" * 40


class QuoteSafetyTests(unittest.TestCase):
    def test_budget_allows_six_then_rejects_until_window_rolls(self):
        budget = QuoteRequestBudget()

        for current in range(6):
            self.assertEqual(budget.try_acquire(now=float(current)), "accepted")
            budget.release()
        self.assertEqual(budget.try_acquire(now=5.0), "rate_limited")
        self.assertEqual(budget.try_acquire(now=60.0), "accepted")
        budget.release()

    def test_budget_has_one_nonblocking_active_request_and_does_not_consume_busy(self):
        budget = QuoteRequestBudget()

        self.assertEqual(budget.try_acquire(now=0.0), "accepted")
        self.assertEqual(budget.try_acquire(now=1.0), "busy")
        budget.release()

        for current in range(1, 6):
            self.assertEqual(budget.try_acquire(now=float(current)), "accepted")
            budget.release()
        self.assertEqual(budget.try_acquire(now=6.0), "rate_limited")

    def make_handler(self, payload):
        body = json.dumps(payload).encode("utf-8")
        headers = Message()
        headers["Host"] = "127.0.0.1:8000"
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(body))
        handler = Handler.__new__(Handler)
        handler.path = "/api/quote"
        handler.headers = headers
        handler.rfile = BytesIO(body)
        handler.send_json = Mock()
        return handler

    def test_invalid_input_does_not_consume_budget(self):
        budget = QuoteRequestBudget()
        handler = self.make_handler({"wallet": WALLET, "units": "1", "cash": "0"})

        with patch("app.server.quote_request_budget", budget), \
             patch("app.server.request_target_sized_quote") as request_quote:
            Handler.do_POST(handler)

        handler.send_json.assert_called_once_with(
            400, {"error": {"field": "cash", "message": "Enter an amount greater than zero."}}
        )
        request_quote.assert_not_called()
        self.assertEqual(budget.try_acquire(now=0.0), "accepted")
        budget.release()

    def test_handler_rejects_budget_excess_with_stable_429_without_calling_api(self):
        budget = QuoteRequestBudget()
        now = time.monotonic()
        for _ in range(6):
            self.assertEqual(budget.try_acquire(now=now), "accepted")
            budget.release()
        handler = self.make_handler({"wallet": WALLET, "units": "1", "cash": "100"})

        with patch("app.server.quote_request_budget", budget), \
             patch("app.server.request_target_sized_quote") as request_quote:
            Handler.do_POST(handler)

        handler.send_json.assert_called_once_with(
            429,
            {"error": {"field": "quote", "message": "Quote request limit reached. No quote was used."}},
        )
        request_quote.assert_not_called()
        self.assertNotIn(WALLET, json.dumps(handler.send_json.call_args.args))

    def test_handler_releases_active_gate_after_quote_error(self):
        budget = QuoteRequestBudget()
        handler = self.make_handler({"wallet": WALLET, "units": "1", "cash": "100"})
        request_quote = Mock(side_effect=[RuntimeError("synthetic failure"), {"status": "ok"}])

        with patch("app.server.quote_request_budget", budget), \
             patch("app.server.request_target_sized_quote", request_quote):
            Handler.do_POST(handler)
            Handler.do_POST(self.make_handler({"wallet": WALLET, "units": "1", "cash": "100"}))

        self.assertEqual(handler.send_json.call_args.args[0], 502)
        self.assertEqual(request_quote.call_count, 2)


if __name__ == "__main__":
    unittest.main()
