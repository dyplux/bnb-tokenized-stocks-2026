from email.message import Message
from io import BytesIO
import json
import time
import unittest
from unittest.mock import Mock, patch

from app.server import Handler, QuoteRequestBudget, protected_post_allowed, public_origin_config


WALLET = "0x" + "1" * 40


class QuoteSafetyTests(unittest.TestCase):
    def test_public_origin_config_accepts_single_https_origin(self):
        self.assertEqual(public_origin_config("https://demo.example.com:8443"), ("https://demo.example.com:8443", True))

    def test_public_origin_config_rejects_non_origin_values(self):
        for value in ("http://demo.example.com", "https://demo.example.com/path", "https://demo.example.com?x=1", "https://demo.example.com?", "https://demo.example.com#", "https://user@demo.example.com", "https://*.example.com", "https://-bad.example.com", "https://bad..example.com", "https://demo.example.com,https://other.example.com"):
            self.assertEqual(public_origin_config(value), (None, False))

    def test_public_pair_is_accepted_and_requires_exact_origin(self):
        with patch.dict("os.environ", {"DYPLUX_PUBLIC_ORIGIN": "https://demo.example.com"}, clear=True):
            self.assertEqual(protected_post_allowed("demo.example.com", "https://demo.example.com"), (True, None))
            self.assertEqual(protected_post_allowed("demo.example.com", None)[0], False)
            self.assertEqual(protected_post_allowed("demo.example.com", "https://other.example.com")[0], False)

    def test_invalid_public_origin_fails_closed(self):
        with patch.dict("os.environ", {"DYPLUX_PUBLIC_ORIGIN": "http://demo.example.com"}, clear=True):
            self.assertEqual(protected_post_allowed("127.0.0.1:8000", None)[0], False)

    def test_unset_public_origin_preserves_localhost_policy(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(protected_post_allowed("127.0.0.1:8000", None), (True, None))
            self.assertEqual(protected_post_allowed("localhost:8000", "http://localhost:8000"), (True, None))
            self.assertFalse(protected_post_allowed("demo.example.com", None)[0])

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

    def make_handler(self, payload, host="127.0.0.1:8000", origin=None):
        body = json.dumps(payload).encode("utf-8")
        headers = Message()
        headers["Host"] = host
        if origin is not None:
            headers["Origin"] = origin
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(body))
        handler = Handler.__new__(Handler)
        handler.path = "/api/quote"
        handler.headers = headers
        handler.rfile = BytesIO(body)
        handler.send_json = Mock()
        return handler

    def test_public_origin_rejections_happen_before_quote_call(self):
        with patch.dict("os.environ", {"DYPLUX_PUBLIC_ORIGIN": "https://demo.example.com"}, clear=True), \
             patch("app.server.request_target_sized_quote") as request_quote:
            for origin in (None, "https://other.example.com"):
                handler = self.make_handler({"wallet": WALLET, "units": "1", "cash": "100"}, host="demo.example.com", origin=origin)
                Handler.do_POST(handler)
                self.assertEqual(handler.send_json.call_args.args[0], 403)
        request_quote.assert_not_called()

    def test_public_origin_accepts_quote_with_matching_host_and_origin(self):
        handler = self.make_handler(
            {"wallet": WALLET, "units": "1", "cash": "100"},
            host="demo.example.com", origin="https://demo.example.com",
        )
        with patch.dict("os.environ", {"DYPLUX_PUBLIC_ORIGIN": "https://demo.example.com"}, clear=True), \
             patch("app.server.request_target_sized_quote", return_value={"status": "ok"}) as request_quote:
            Handler.do_POST(handler)
        handler.send_json.assert_called_once_with(200, {"status": "ok"})
        request_quote.assert_called_once()

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

    def test_scenario_error_does_not_expose_exception_detail(self):
        marker = "SYNTHETIC_SECRET_MARKER"
        handler = Handler.__new__(Handler)
        handler.path = "/api/scenario?units=1&cash=100"
        handler.send_json = Mock()

        with patch("app.server.fetch_markets", side_effect=RuntimeError(marker)):
            Handler.do_GET(handler)

        status, payload = handler.send_json.call_args.args
        self.assertEqual(status, 502)
        self.assertNotIn(marker, json.dumps(payload))
        self.assertNotIn("detail", payload["error"])


if __name__ == "__main__":
    unittest.main()
