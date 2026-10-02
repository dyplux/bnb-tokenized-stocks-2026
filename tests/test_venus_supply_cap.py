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

    def test_zero_cap_disables_supply_in_core_policy(self):
        result = build_scenario(Decimal("1"), Decimal("100"), markets(cap_raw=0), "2026-10-02T00:00:00Z")
        self.assertEqual(Decimal(result["market"]["nvdab_supply_cap_headroom"]), Decimal("0"))
        self.assertFalse(result["borrow"]["entered_units_within_indexed_supply_cap"])


if __name__ == "__main__":
    unittest.main()
