"""Synthetic arithmetic boundaries for the read-only reference formula audit."""

import unittest

from scripts.audit_reference_formula import formula_check


class ReferenceFormulaTest(unittest.TestCase):
    def test_reported_precision_match(self):
        row = {"token_price_usd": "100", "token_to_share_ratio": "3",
               "derived_reference_price_usd": "33.333333"}
        self.assertEqual(formula_check(row)["formula_state"], "MATCH_AT_REPORTED_PRECISION")

    def test_material_mismatch(self):
        row = {"token_price_usd": "100", "token_to_share_ratio": "2",
               "derived_reference_price_usd": "49.9"}
        self.assertEqual(formula_check(row)["formula_state"], "MISMATCH")

    def test_missing_or_zero_ratio(self):
        self.assertEqual(formula_check({"token_price_usd": "100"})["formula_state"], "MISSING_OR_INVALID")
        self.assertEqual(formula_check({"token_price_usd": "100", "token_to_share_ratio": "0",
                                        "derived_reference_price_usd": "50"})["formula_state"], "MISSING_OR_INVALID")


if __name__ == "__main__":
    unittest.main()
