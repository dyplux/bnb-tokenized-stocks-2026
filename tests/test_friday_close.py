"""Arithmetic and missing-value checks for the external close comparison."""

import unittest
from decimal import Decimal

from scripts.compare_friday_close import percent_gap


class FridayCloseTest(unittest.TestCase):
    def test_share_ratio_applied_before_gap(self):
        per_share, gap = percent_gap("200", "2", "100")
        self.assertEqual(per_share, Decimal("100"))
        self.assertEqual(gap, Decimal("0"))

    def test_positive_and_negative_gaps(self):
        self.assertEqual(percent_gap("102", "1", "100")[1], Decimal("2.00"))
        self.assertEqual(percent_gap("98", "1", "100")[1], Decimal("-2.00"))

    def test_invalid_inputs_have_no_gap(self):
        self.assertIsNone(percent_gap("100", None, "100"))
        self.assertIsNone(percent_gap("100", "0", "100"))


if __name__ == "__main__":
    unittest.main()
