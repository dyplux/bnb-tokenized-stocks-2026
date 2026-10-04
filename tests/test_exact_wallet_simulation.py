"""Synthetic checks for the read-only exact-wallet transaction boundary."""

import tempfile
import unittest
from pathlib import Path

from scripts.prepare_exact_wallet_simulation import (
    build_matches_quote, public_demo_address, route_matches_intent, unsigned_tx_is_exact,
)
from scripts.rwa_research import next_cycle_delay


class ExactWalletBoundaryTests(unittest.TestCase):
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
                 "approveTarget": router, "router": "usdt--stock"}
        tx = {"from": wallet, "to": router, "data": "0x1234", "value": "0"}
        build = {"routerResult": {key: route[key] for key in
                                  ("binanceChainId", "fromToken", "toToken", "fromTokenAmount", "router")},
                 "tx": tx}
        self.assertTrue(route_matches_intent(route, usdt, stock, "100"))
        self.assertTrue(build_matches_quote(build, route, wallet, usdt, stock, "100"))
        for key, wrong in (("binanceChainId", "1"), ("fromTokenAmount", "101"),
                           ("toToken", {"tokenContractAddress": usdt})):
            self.assertFalse(route_matches_intent({**route, key: wrong}, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "tx": {**tx, "to": stock}},
                                             route, wallet, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "tx": {**tx, "value": "1"}},
                                             route, wallet, usdt, stock, "100"))
        self.assertFalse(build_matches_quote({**build, "routerResult":
                                             {**build["routerResult"], "router": "wrong"}},
                                             route, wallet, usdt, stock, "100"))


if __name__ == "__main__":
    unittest.main()
