#!/usr/bin/env python3
"""Bounded Yahoo historical bar backfill for a supplementary Sunday sensitivity check."""

import csv
import hashlib
import json
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
NY = ZoneInfo("America/New_York")
DESTINATION = ROOT / "data/external_reference/2026-10-02-yahoo-afterhours-bars.json"
SUNDAY = ROOT / "experiments/EXP-RWA-004/friday_close_benchmark.csv"
SENSITIVITY = ROOT / "experiments/EXP-RWA-004/friday_afterhours_sensitivity.csv"


def query(ticker):
    start = int(datetime(2026, 10, 2, 15, 55, tzinfo=NY).timestamp())
    end = int(datetime(2026, 10, 2, 20, 5, tzinfo=NY).timestamp())
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/%s"
           "?period1=%d&period2=%d&interval=1m&includePrePost=true") % (ticker, start, end)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urlopen(request, timeout=20) as response:
        body = response.read(2_000_001)
    if len(body) > 2_000_000:
        raise RuntimeError("historical response exceeded size limit")
    payload = json.loads(body)
    result = payload["chart"]["result"][0]
    if result["meta"].get("exchangeTimezoneName") != "America/New_York":
        raise RuntimeError("unexpected historical bar timezone")
    stamps = result.get("timestamp") or []
    closes = result["indicators"]["quote"][0].get("close") or []
    if len(stamps) != len(closes):
        raise RuntimeError("historical timestamp and close arrays differ")
    bars = []
    for stamp, close in zip(stamps, closes):
        instant = datetime.fromtimestamp(stamp, NY)
        if instant.date().isoformat() == "2026-10-02" and (16, 0) <= (instant.hour, instant.minute) < (20, 0) and close is not None:
            bars.append((instant, Decimal(str(close))))
    if not bars:
        raise RuntimeError("no non-null after-hours close bars")
    last_at, last_value = bars[-1]
    return {"ticker": ticker, "origin": "BACKFILLED", "publisher": "Yahoo Finance",
            "session_date": "2026-10-02", "bar_interval": "1m", "session_filter": "16:00 to before 20:00 America/New_York",
            "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "source_url": url, "raw_response_sha256": hashlib.sha256(body).hexdigest(),
            "non_null_afterhours_bars": len(bars), "last_bar_time_new_york": last_at.isoformat(),
            "last_bar_close_usd": str(last_value),
            "timestamp_limit": "Historical one-minute bar timestamp, not a last-trade, issuer reference, or execution clock"}


def main():
    rows = []
    for ticker in ("COIN", "NVDA", "TSLA"):
        rows.append(query(ticker))
        time.sleep(0.5)
    DESTINATION.write_text(json.dumps({"origin": "BACKFILLED", "rows": rows,
        "claim_limit": "Supplementary historical after-hours bar check; not the preregistered regular-close baseline or an issuer reference clock."},
        indent=2, sort_keys=True) + "\n", encoding="utf-8")
    by_ticker = {row["ticker"]: row for row in rows}
    with SUNDAY.open(newline="", encoding="utf-8") as stream:
        sunday = list(csv.DictReader(stream))
    sensitivity = []
    for row in sunday:
        bar = by_ticker[row["ticker"]]
        prior = Decimal(bar["last_bar_close_usd"])
        sunday_value = Decimal(row["token_derived_per_share_usd"])
        sensitivity.append({"ticker": row["ticker"], "provider": row["provider"],
                            "sunday_token_per_share_arithmetic_usd": str(sunday_value),
                            "sunday_observed_at": row["token_observed_at"],
                            "friday_afterhours_bar_close_usd": str(prior),
                            "friday_afterhours_bar_time_new_york": bar["last_bar_time_new_york"],
                            "signed_gap_pct": str((sunday_value / prior - 1) * 100),
                            "origin": "LIVE Sunday token plus BACKFILLED Friday external bar",
                            "source_url": bar["source_url"], "raw_response_sha256": bar["raw_response_sha256"],
                            "issuer_reference_age_status": "UNKNOWN"})
    sensitivity.sort(key=lambda row: (row["ticker"], row["provider"]))
    with SENSITIVITY.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(sensitivity[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(sensitivity)
    print(json.dumps({"afterhours_bars": {row["ticker"]: row["non_null_afterhours_bars"] for row in rows},
                      "last_bar_times": {row["ticker"]: row["last_bar_time_new_york"] for row in rows},
                      "sensitivity_rows": len(sensitivity)}))


if __name__ == "__main__":
    main()
