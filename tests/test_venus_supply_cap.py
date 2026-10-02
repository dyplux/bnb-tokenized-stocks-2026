from decimal import Decimal
import unittest
from unittest.mock import patch

from app.server import attach_contract_supply_cap, build_scenario, NVDAB, USDT, CORE_UNITROLLER, V_NVDAB


def markets(cap_raw=1500 * 10 ** 18, address=None):
    stock = {
        "chainId": "56", "underlyingSymbol": "NVDAB", "underlyingAddress": NVDAB,
        "poolComptrollerAddress": CORE_UNITROLLER, "isListed": True,
        "canBeCollateral": True, "underlyingDecimal": 18,
        "underlyingPriceMantissa": str(230 * 10 ** 18),
        "collateralFactorMantissa": str(6 * 10 ** 17),
        "liquidationThresholdMantissa": str(7 * 10 ** 17),
        "supplyCapsMantissa": str(cap_raw),
        "totalSupplyMantissa": str(1480 * 10 ** 8),
        "exchangeRateMantissa": str(10 ** 28),
    }
    if address is not None:
        stock["address"] = address
    usdt = {
        "chainId": "56", "underlyingSymbol": "USDT", "underlyingAddress": USDT,
        "poolComptrollerAddress": CORE_UNITROLLER, "isListed": True,
        "isBorrowable": True, "underlyingDecimal": 18,
        "underlyingPriceMantissa": str(10 ** 18),
        "borrowApyDecimal": "0.05", "cashMantissa": str(1000000 * 10 ** 18),
    }
    return {"result": [stock, usdt]}


class VenusSupplyCapTests(unittest.TestCase):
    def test_headroom_uses_vtoken_exchange_rate_and_underlying_decimals(self):
        with patch("app.server.rpc", side_effect=AssertionError("pure calculation called RPC")):
            result = build_scenario(Decimal("1"), Decimal("100"), markets(), "2026-10-02T00:00:00Z")
        self.assertEqual(Decimal(result["market"]["nvdab_supply_cap_headroom"]), Decimal("20"))
        self.assertTrue(result["borrow"]["entered_units_within_indexed_supply_cap"])

    def test_entered_units_above_headroom_are_flagged(self):
        result = build_scenario(Decimal("25"), Decimal("100"), markets(), "2026-10-02T00:00:00Z")
        self.assertFalse(result["borrow"]["entered_units_within_indexed_supply_cap"])
        self.assertTrue(result["borrow"]["target_feasible_by_collateral"])
        self.assertEqual(Decimal(result["borrow"]["minimum_nvdab_for_target"]), Decimal("0.724637681159420290"))
        self.assertTrue(result["borrow"]["minimum_within_indexed_supply_cap"])

    def test_minimum_uses_exact_base_unit_ceiling_at_cap_boundary(self):
        at_cap = build_scenario(Decimal("25"), Decimal("2760"), markets(), "2026-10-02T00:00:00Z")
        over_cap = build_scenario(Decimal("25"), Decimal("2760.000000000000000001"), markets(), "2026-10-02T00:00:00Z")
        self.assertEqual(at_cap["borrow"]["minimum_nvdab_for_target"], "20")
        self.assertTrue(at_cap["borrow"]["minimum_within_indexed_supply_cap"])
        self.assertEqual(over_cap["borrow"]["minimum_nvdab_for_target"], "20.000000000000000001")
        self.assertFalse(over_cap["borrow"]["minimum_within_indexed_supply_cap"])

    def test_zero_cap_disables_supply_in_core_policy(self):
        result = build_scenario(Decimal("1"), Decimal("100"), markets(cap_raw=0), "2026-10-02T00:00:00Z")
        self.assertEqual(Decimal(result["market"]["nvdab_supply_cap_headroom"]), Decimal("0"))
        self.assertFalse(result["borrow"]["entered_units_within_indexed_supply_cap"])
        self.assertFalse(result["borrow"]["minimum_within_indexed_supply_cap"])

    def test_rejects_non_integer_price_mantissa_before_exact_raw_math(self):
        data = markets()
        data["result"][0]["underlyingPriceMantissa"] = "230000000000000000000.5"
        with self.assertRaisesRegex(RuntimeError, "NVDAB price"):
            build_scenario(Decimal("1"), Decimal("100"), data, "2026-10-02T00:00:00Z")

    def test_rejects_wrong_decimals_for_pinned_nvdab(self):
        data = markets()
        data["result"][0]["underlyingDecimal"] = 17
        with self.assertRaisesRegex(RuntimeError, "NVDAB decimals"):
            build_scenario(Decimal("1"), Decimal("100"), data, "2026-10-02T00:00:00Z")

    @staticmethod
    def contract_rpc(total_supply="0x" + format(1480 * 10 ** 8, "064x"), exchange_rate="0x" + format(10 ** 28, "064x"), chain="0x38", underlying=None):
        underlying = underlying or ("0x" + "0" * 24 + NVDAB[2:])
        calls = {
            ("eth_chainId",): chain,
            ("eth_blockNumber",): "0x100",
            ("eth_getCode", CORE_UNITROLLER, "0x100"): "0x6000",
            ("eth_getCode", V_NVDAB, "0x100"): "0x6000",
            ("eth_call", V_NVDAB, "0x6f307dc3", "0x100"): underlying,
            ("eth_call", CORE_UNITROLLER, "0x02c3bcbb" + V_NVDAB[2:].rjust(64, "0"), "0x100"): "0x" + format(1500 * 10 ** 18, "064x"),
            ("eth_call", V_NVDAB, "0x18160ddd", "0x100"): total_supply,
            ("eth_call", V_NVDAB, "0x182df0f5", "0x100"): exchange_rate,
            ("eth_getBlockByNumber", "0x100", False): {"timestamp": "0x68d1e000"},
        }

        def fake_rpc(method, params):
            if method == "eth_chainId":
                return calls[(method,)]
            if method == "eth_blockNumber":
                return calls[(method,)]
            if method == "eth_getCode":
                return calls[(method, params[0], params[1])]
            if method == "eth_call":
                return calls[(method, params[0]["to"], params[0]["data"], params[1])]
            return calls[(method, params[0], params[1])]
        return fake_rpc

    def test_contract_cap_success_uses_one_fixed_block_and_computes_booleans(self):
        rpc = self.contract_rpc()
        with patch("app.server.rpc", side_effect=rpc) as mocked:
            result = attach_contract_supply_cap(build_scenario(Decimal("1"), Decimal("100"), markets(address=V_NVDAB), "2026-10-02T00:00:00Z"))
        cap = result["contract_cap"]
        self.assertEqual(cap["status"], "verified")
        self.assertEqual(cap["headroom"], "20")
        self.assertTrue(cap["typed_amount_within_headroom"])
        self.assertTrue(cap["minimum_collateral_within_headroom"])
        self.assertEqual(cap["block_number"], 256)
        self.assertIsNotNone(cap["block_time_utc"])
        self.assertIsNotNone(cap["received_at_utc"])
        block_tags = [call.args[1][-1] for call in mocked.call_args_list if call.args[0] in ("eth_getCode", "eth_call")]
        self.assertTrue(block_tags and all(tag == "0x100" for tag in block_tags))

    def test_contract_cap_malformed_uint256_is_unavailable(self):
        rpc = self.contract_rpc(total_supply="0x1")
        with patch("app.server.rpc", side_effect=rpc):
            result = attach_contract_supply_cap(build_scenario(Decimal("1"), Decimal("100"), markets(address=V_NVDAB), "2026-10-02T00:00:00Z"))
        self.assertEqual(result["contract_cap"]["status"], "unavailable")
        self.assertIsNone(result["contract_cap"]["typed_amount_within_headroom"])

    def test_contract_cap_zero_exchange_rate_is_unavailable(self):
        rpc = self.contract_rpc(exchange_rate="0x" + "0" * 64)
        with patch("app.server.rpc", side_effect=rpc):
            result = attach_contract_supply_cap(build_scenario(Decimal("1"), Decimal("100"), markets(address=V_NVDAB), "2026-10-02T00:00:00Z"))
        self.assertEqual(result["contract_cap"]["status"], "unavailable")

    def test_contract_cap_mismatched_indexed_market_is_unavailable_without_rpc(self):
        with patch("app.server.rpc", side_effect=AssertionError("mismatched market called RPC")):
            result = attach_contract_supply_cap(build_scenario(Decimal("1"), Decimal("100"), markets(address=USDT), "2026-10-02T00:00:00Z"))
        self.assertEqual(result["contract_cap"]["status"], "unavailable")

    def test_contract_cap_wrong_chain_is_unavailable(self):
        with patch("app.server.rpc", side_effect=self.contract_rpc(chain="0x1")):
            result = attach_contract_supply_cap(build_scenario(Decimal("1"), Decimal("100"), markets(address=V_NVDAB), "2026-10-02T00:00:00Z"))
        self.assertEqual(result["contract_cap"]["status"], "unavailable")

    def test_contract_cap_mismatched_underlying_is_unavailable(self):
        other = "0x" + "0" * 24 + USDT[2:]
        with patch("app.server.rpc", side_effect=self.contract_rpc(underlying=other)):
            result = attach_contract_supply_cap(build_scenario(Decimal("1"), Decimal("100"), markets(address=V_NVDAB), "2026-10-02T00:00:00Z"))
        self.assertEqual(result["contract_cap"]["status"], "unavailable")

    def test_contract_cap_rpc_failure_falls_back_without_passing(self):
        with patch("app.server.rpc", side_effect=RuntimeError("synthetic RPC failure")):
            result = attach_contract_supply_cap(build_scenario(Decimal("25"), Decimal("100"), markets(address=V_NVDAB), "2026-10-02T00:00:00Z"))
        self.assertEqual(result["contract_cap"]["status"], "unavailable")
        self.assertIsNone(result["contract_cap"]["minimum_collateral_within_headroom"])


if __name__ == "__main__":
    unittest.main()
