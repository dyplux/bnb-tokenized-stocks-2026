"""A later token price must never be normalized with the baseline catalog ratio."""

import unittest

from scripts.analyze_rwa import ratio_from_price_cycle


class AlignedRatioTests(unittest.TestCase):
    def test_ratio_comes_from_price_cycle(self):
        self.assertEqual(str(ratio_from_price_cycle({"token_to_share_ratio": "1.25"})), "1.25")

    def test_missing_cycle_ratio_stays_unknown(self):
        self.assertIsNone(ratio_from_price_cycle({"token_price_usd": "100"}))
        self.assertIsNone(ratio_from_price_cycle(None))


if __name__ == "__main__":
    unittest.main()
