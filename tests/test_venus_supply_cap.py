from decimal import Decimal
import unittest

from app.server import build_scenario, NVDAB, USDT, CORE_UNITROLLER


def markets(cap_raw=1500 * 10 ** 18):
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


if __name__ == "__main__":
    unittest.main()
