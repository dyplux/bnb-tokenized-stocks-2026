"""Synthetic fixed-block checks for the unsigned demo-wallet readiness read."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.pre_execution_packet import digest
from scripts.read_demo_wallet_state import read_state, word


class DemoWalletStateTests(unittest.TestCase):
    def test_address_word_requires_public_evm_address(self):
        self.assertEqual(word("0x" + "a" * 40), "0" * 24 + "a" * 40)
        with self.assertRaises(ValueError):
            word("not-an-address")

    def test_read_only_balance_result_never_authorizes_execution(self):
        wallet = "0x" + "a" * 40
        packet = {"state": "BLOCKED", "execution_authorized": False,
                  "exact_wallet_trial": {"quote_sha256": "synthetic-quote-hash"}}
        packet["packet_sha256"] = digest(packet)
        route = {"approveTarget": "0x" + "b" * 40}
        tx = {"gas": "450000", "gasPrice": "1000000000"}

        def fake_rpc(calls, block, experiment, **kwargs):
            if calls[0]["method"] == "eth_blockNumber":
                return [{"id": 1, "result": "0x1"}], b"", "2026-10-04T17:00:00Z", "head-hash"
            results = {10: hex(0), 11: "0x1234", 12: hex(0), 13: hex(0),
                       14: hex(18), 15: {"timestamp": hex(1791133200)}}
            return [{"id": key, "result": value} for key, value in results.items()], b"", "2026-10-04T17:00:01Z", "state-hash"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "packet.json"
            path.write_text(json.dumps(packet))
            with patch("scripts.read_demo_wallet_state.public_demo_address", return_value=wallet), \
                 patch("scripts.read_demo_wallet_state.route_from_packet", return_value=(route, tx, str(10**19))):
                state = read_state(packet_path=path, rpc=fake_rpc)
        self.assertFalse(state["has_input_balance"])
        self.assertTrue(state["approval_needed"])
        self.assertFalse(state["has_gas_ceiling"])
        self.assertTrue(state["router_has_code"])
        self.assertFalse(state["execution_authorized"])
        self.assertNotIn(wallet, json.dumps(state))


if __name__ == "__main__":
    unittest.main()
