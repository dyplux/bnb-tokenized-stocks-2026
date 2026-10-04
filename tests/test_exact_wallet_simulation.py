"""Synthetic checks for the read-only exact-wallet transaction boundary."""

import tempfile
import unittest
from pathlib import Path

from scripts.prepare_exact_wallet_simulation import public_demo_address, unsigned_tx_is_exact
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


if __name__ == "__main__":
    unittest.main()
