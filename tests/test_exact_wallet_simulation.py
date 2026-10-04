"""Synthetic checks for the read-only exact-wallet transaction boundary."""

import tempfile
import unittest
from pathlib import Path

from app.server import USDT
from scripts.prepare_exact_wallet_simulation import (
    build_matches_quote, public_demo_address, route_matches_intent, run, unsigned_tx_is_exact,
)
from scripts.rwa_research import SWAP_BUILD, next_cycle_delay


class BuildOnlyApi:
    def __init__(self, route, wallet):
        self.route = route
        self.wallet = wallet
        self.calls = []

    def get(self, path, params, *args, **kwargs):
        self.calls.append(path)
        if path != SWAP_BUILD:
            raise AssertionError("A bound route must not request another catalog or quote")
        return {"code": 0, "data": {"executionMode": "SWAP",
                                    "routerResult": self.route,
                                    "tx": {"from": self.wallet, "to": self.route["approveTarget"],
                                           "value": "0", "data": "0x1234"}}}, "2026-10-04T10:10:01Z", "build-hash"

    def post_simulation(self, payload, *args, **kwargs):
        self.calls.append("simulation")
        return {"code": 0, "data": {"status": "SUCCESS"}}, "2026-10-04T10:10:02Z", "sim-hash"


class ExactWalletBoundaryTests(unittest.TestCase):
    def test_bound_route_builds_and_simulates_without_a_second_quote(self):
        wallet = "0x" + "a" * 40
        stock = "0x" + "2" * 40
        router = "0x" + "3" * 40
        route = {"binanceChainId": "56", "fromToken": {"tokenContractAddress": USDT},
                 "toToken": {"tokenContractAddress": stock},
                 "fromTokenAmount": str(10 * 10**18), "toTokenAmount": "100",
                 "approveTarget": router, "router": "usdt--stock", "quoteId": "fixture-id",
                 "executionMode": "SWAP", "vendorName": "fixture"}
        context = {"wallet": wallet, "provider": "bstock", "ticker": "NVDA",
                   "symbol": "NVDAB", "contract": stock,
                   "raw_amount": str(10 * 10**18), "quote_business_code": 0,
                   "quote_observed_at": "2026-10-04T10:10:00Z", "quote_sha256": "quote-hash",
                   "catalog_observed_at": "2026-10-04T10:09:59Z", "catalog_sha256": "catalog-hash",
                   "route": route}
        api = BuildOnlyApi(route, wallet)
        outcome = run(provider="bstock", wallet=wallet, api=api, route_context=context)
        self.assertEqual(api.calls, [SWAP_BUILD, "simulation"])
        self.assertTrue(outcome["quote"]["bound_to_policy"])
        self.assertEqual(outcome["simulation"]["predicted_transaction_status"], "SUCCESS")
        self.assertEqual(outcome["decision"], "NOT_APPROVED")
        with self.assertRaises(ValueError):
            run(provider="bstock", wallet="0x" + "b" * 40, api=api, route_context=context)

    def test_only_public_address_is_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text("BNB_STOCKS_DEMO_PRIVATE_KEY=synthetic-secret\n"
                            "BNB_STOCKS_DEMO_ADDRESS=0x" + "a" * 40 + "\n")
            self.assertEqual(public_demo_address(path), "0x" + "a" * 40)

    def test_missing_or_invalid_address_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text("BNB_STOCKS_DEMO_ADDRESS=bad\n")
            with self.assertRaises(ValueError):
                public_demo_address(path)

    def test_unsigned_transaction_requires_exact_wallet_and_hex_calldata(self):
        wallet = "0x" + "a" * 40
        tx = {"from": wallet, "to": "0x" + "b" * 40, "data": "0x1234"}
        self.assertTrue(unsigned_tx_is_exact(tx, wallet))
        self.assertFalse(unsigned_tx_is_exact({**tx, "from": "0x" + "c" * 40}, wallet))
        self.assertFalse(unsigned_tx_is_exact({**tx, "data": "0xzzzz"}, wallet))
        self.assertFalse(unsigned_tx_is_exact({**tx, "data": "0x123"}, wallet))

    def test_collector_retries_slot_crossed_during_successful_call(self):
        self.assertEqual(next_cycle_delay(10, 300, 11 * 300 + 2), 0.1)
        self.assertEqual(next_cycle_delay(10, 300, 10 * 300 + 2), 298)

    def test_quote_and_build_must_match_exact_intent(self):
        wallet = "0x" + "a" * 40
        usdt, stock, router = "0x" + "1" * 40, "0x" + "2" * 40, "0x" + "3" * 40
        route = {"binanceChainId": "56", "fromToken": {"tokenContractAddress": usdt},
                 "toToken": {"tokenContractAddress": stock}, "fromTokenAmount": "100",
                 "toTokenAmount": "25",
                 "approveTarget": router, "router": "usdt--stock"}
        tx = {"from": wallet, "to": router, "data": "0x1234", "value": "0"}
        build = {"routerResult": {key: route[key] for key in
                                  ("binanceChainId", "fromToken", "toToken", "fromTokenAmount", "toTokenAmount", "router")},
                 "tx": tx}
        self.assertTrue(route_matches_intent(route, usdt, stock, "100"))
        self.assertTrue(build_matches_quote(build, route, wallet, usdt, stock, "100"))
        for key, wrong in (("binanceChainId", "1"), ("fromTokenAmount", "101"),
                           ("toTokenAmount", "0"),
                           ("toToken", {"tokenContractAddress": usdt})):
            self.assertFalse(route_matches_intent({**route, key: wrong}, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "routerResult":
                                             {**build["routerResult"], "toTokenAmount": "24"}},
                                             route, wallet, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "tx": {**tx, "to": stock}},
                                             route, wallet, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "tx": {**tx, "value": "1"}},
                                             route, wallet, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "routerResult":
                                             {**build["routerResult"], "router": "wrong"}},
                                             route, wallet, usdt, stock, "100"))


if __name__ == "__main__":
    unittest.main()
