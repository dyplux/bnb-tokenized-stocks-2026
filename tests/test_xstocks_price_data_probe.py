"""The public price-data probe must not infer a reference clock from fetch time."""

import unittest

from scripts.probe_xstocks_price_data import clock_fields


class XStocksPriceDataProbeTests(unittest.TestCase):
    def test_candidate_paths_are_observations_only(self):
        payload = {"data": {"price": 200, "market": {"source": "Nasdaq",
                                                   "asOf": "2026-10-02T20:00:00Z"},
                            "tokenPriceUpdatedAt": "2026-10-04T17:00:00Z"}}
        self.assertEqual(clock_fields(payload), {
            "data.market.source": "Nasdaq",
            "data.market.asOf": "2026-10-02T20:00:00Z",
            "data.tokenPriceUpdatedAt": "2026-10-04T17:00:00Z"})


if __name__ == "__main__":
    unittest.main()
