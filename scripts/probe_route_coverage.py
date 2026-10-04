#!/usr/bin/env python3
"""One-time weekend quote coverage of the 40 watched BSC stock contracts."""

import json
import secrets
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, QUOTE, TICKERS, utc_now, write_json  # noqa: E402


def main():
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text(encoding="utf-8"))
    selected = [row for row in catalog["rows"] if row["asset_type"] == 1 and
                (row["provider"] == "bstock" or (row["provider"] == "ondo" and row["ticker"] in TICKERS))]
    selected.sort(key=lambda row: (row["provider"], row["ticker"], row["contract"]))
    if len(selected) != 40 or len({row["contract"] for row in selected}) != 40:
        raise RuntimeError("expected the established 40-contract stock universe")
    wallet = "0x" + secrets.token_hex(20)
    api = Api()
    output = ROOT / "experiments/EXP-RWA-009/weekend_route_coverage_100usdt.json"
    rows = []
    for index, target in enumerate(selected, 1):
        quote, at, digest = api.get(
            QUOTE, [("binanceChainId", "56"), ("fromTokenAddress", USDT),
                    ("toTokenAddress", target["contract"]), ("amount", str(100 * 10**18)),
                    ("userWalletAddress", wallet)],
            "EXP-RWA-009/COVERAGE", "one bounded 100 USDT quote per monitored stock contract",
            {"market": "weekend", "ticker": target["ticker"],
             "provider": target["provider"], "task": "buy_100_usdt"}, allow_error=True,
        )
        routes = quote.get("data") if isinstance(quote.get("data"), list) else []
        rows.append({"observed_at": at, "origin": "LIVE", "provider": target["provider"],
                     "ticker": target["ticker"], "contract": target["contract"],
                     "business_code": quote.get("code"), "business_message": quote.get("msg"),
                     "route_count": len(routes), "vendors": [r.get("vendorName") for r in routes if isinstance(r, dict)],
                     "execution_modes": [r.get("executionMode") for r in routes if isinstance(r, dict)],
                     "raw_response_sha256": digest})
        write_json(output, {"started_at": rows[0]["observed_at"], "last_observed_at": at,
                            "expected_contracts": 40, "completed_contracts": index,
                            "input": "100 USDT, Binance BSC USDT 18 decimal units",
                            "wallet": "ephemeral_unfunded_not_stored", "rows": rows,
                            "limit": "Sequential, temporary-wallet quotes. No investor eligibility, build, approval, simulation, fill, final fees or executable-spread claim."})
        if index < len(selected):
            time.sleep(0.65)
    counts = {provider: {"contracts": sum(r["provider"] == provider for r in rows),
                         "routed": sum(r["provider"] == provider and r["route_count"] > 0 for r in rows),
                         "codes": dict(Counter(str(r["business_code"]) for r in rows if r["provider"] == provider))}
              for provider in ("bstock", "ondo")}
    print(json.dumps({"completed_at": utc_now(), "counts": counts}))


if __name__ == "__main__":
    main()
