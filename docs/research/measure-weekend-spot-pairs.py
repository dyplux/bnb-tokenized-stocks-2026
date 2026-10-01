#!/usr/bin/env python3
"""Reproduce a small Binance Spot weekend observation without credentials.

This reads centralized-exchange candles. It does not measure BNB Chain quotes,
execution, fees, stock rights, predictive power or strategy returns.
"""

import csv
import datetime as dt
import json
import statistics
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo


BASE = "https://data-api.binance.vision/api/v3/klines"
SYMBOLS = ("BTCUSDT", "MSTRBUSDT", "COINBUSDT")
NEW_YORK = ZoneInfo("America/New_York")
FIRST_FRIDAY = dt.date(2026, 7, 24)
WEEKENDS = 10
OUT = Path(__file__).with_name("2026-10-01-weekend-spot-pairs.csv")


def fetch_range(symbol: str, start_ms: int, end_ms: int) -> dict[int, list]:
    candles = {}
    cursor = start_ms
    while cursor <= end_ms:
        query = urllib.parse.urlencode(
            {"symbol": symbol, "interval": "1h", "startTime": cursor,
             "endTime": end_ms, "limit": 1000}
        )
        request = urllib.request.Request(
            f"{BASE}?{query}", headers={"User-Agent": "DypluxResearch/1.0"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            page = json.load(response)
        if not isinstance(page, list) or not page:
            break
        for candle in page:
            candles[int(candle[0])] = candle
        cursor = int(page[-1][0]) + 3_600_000
        if len(page) < 1000:
            break
    return candles


def correlation(x: tuple[float, ...], y: tuple[float, ...]) -> float:
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)
    covariance = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
    spread_x = sum((a - mean_x) ** 2 for a in x)
    spread_y = sum((b - mean_y) ** 2 for b in y)
    return covariance / (spread_x * spread_y) ** 0.5


def main() -> None:
    bounds = []
    for week in range(WEEKENDS):
        friday = FIRST_FRIDAY + dt.timedelta(days=7 * week)
        sunday = friday + dt.timedelta(days=2)
        start = dt.datetime.combine(friday, dt.time(20), NEW_YORK)
        end = dt.datetime.combine(sunday, dt.time(20), NEW_YORK)
        bounds.append((friday.isoformat(), int(start.timestamp() * 1000),
                       int(end.timestamp() * 1000)))

    series = {symbol: fetch_range(symbol, bounds[0][1], bounds[-1][2])
              for symbol in SYMBOLS}
    rows = []
    for friday, start, end in bounds:
        record = {"friday_ny": friday, "start_utc": dt.datetime.fromtimestamp(
            start / 1000, dt.timezone.utc).isoformat(),
            "end_utc": dt.datetime.fromtimestamp(
                end / 1000, dt.timezone.utc).isoformat()}
        for symbol in SYMBOLS:
            candles = series[symbol]
            first, last = candles.get(start), candles.get(end)
            hours = [candles.get(start + i * 3_600_000) for i in range(48)]
            prefix = symbol.lower().replace("usdt", "")
            if first is None or last is None or any(c is None for c in hours):
                record[f"{prefix}_open"] = ""
                record[f"{prefix}_end_open"] = ""
                record[f"{prefix}_return_pct"] = ""
                record[f"{prefix}_max_abs_from_open_pct"] = ""
                record[f"{prefix}_quote_volume_usdt"] = ""
                continue
            first_price = float(first[1])
            last_price = float(last[1])
            observed_opens = [float(c[1]) for c in hours] + [last_price]
            record[f"{prefix}_open"] = f"{first_price:.8f}"
            record[f"{prefix}_end_open"] = f"{last_price:.8f}"
            record[f"{prefix}_return_pct"] = f"{(last_price / first_price - 1) * 100:.5f}"
            record[f"{prefix}_max_abs_from_open_pct"] = f"{max(abs(price / first_price - 1) * 100 for price in observed_opens):.5f}"
            record[f"{prefix}_quote_volume_usdt"] = f"{sum(float(c[7]) for c in hours):.2f}"
        rows.append(record)

    with OUT.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"source={BASE} rows={len(rows)} output={OUT.name}")
    for symbol in SYMBOLS:
        prefix = symbol.lower().replace("usdt", "")
        present = [r for r in rows if r[f"{prefix}_return_pct"]]
        print(f"{symbol} available={len(present)}/{len(rows)}")
    for threshold in (1.0, 2.0, 3.0, 5.0):
        reached = sum(float(r["btc_max_abs_from_open_pct"]) >= threshold
                      for r in rows if r["btc_max_abs_from_open_pct"])
        print(f"BTC max absolute move from Friday close >= {threshold:.0f}%: {reached}/{len(rows)} weekends")
    for symbol in SYMBOLS[1:]:
        prefix = symbol.lower().replace("usdt", "")
        paired = [(float(r["btc_return_pct"]), float(r[f"{prefix}_return_pct"]))
                  for r in rows if r["btc_return_pct"] and r[f"{prefix}_return_pct"]]
        if len(paired) < 2:
            continue
        x, y = zip(*paired)
        same_sign = sum((a > 0) == (b > 0) for a, b in paired)
        correlation_value = correlation(x, y) if len(paired) >= 3 else float("nan")
        print(f"{symbol} paired={len(paired)} same_sign={same_sign} "
              f"correlation={correlation_value:.3f} median_quote_volume_usdt="
              f"{statistics.median(float(r[f'{prefix}_quote_volume_usdt']) for r in rows if r[f'{prefix}_quote_volume_usdt']):.2f}")

    for symbol in SYMBOLS[1:]:
        concurrent, btc_leads, stock_leads = [], [], []
        for _, start, _ in bounds:
            btc = series["BTCUSDT"]
            stock = series[symbol]
            btc_prices = [btc.get(start + i * 3_600_000) for i in range(49)]
            stock_prices = [stock.get(start + i * 3_600_000) for i in range(49)]
            if any(c is None for c in btc_prices + stock_prices):
                continue
            btc_hourly = [float(btc_prices[i + 1][1]) / float(btc_prices[i][1]) - 1
                          for i in range(48)]
            stock_hourly = [float(stock_prices[i + 1][1]) / float(stock_prices[i][1]) - 1
                            for i in range(48)]
            concurrent.extend(zip(btc_hourly, stock_hourly))
            btc_leads.extend(zip(btc_hourly[:-1], stock_hourly[1:]))
            stock_leads.extend(zip(btc_hourly[1:], stock_hourly[:-1]))
        def corr_pairs(pairs: list[tuple[float, float]]) -> float:
            left, right = zip(*pairs)
            return correlation(left, right)
        print(f"{symbol} hourly_pairs={len(concurrent)} "
              f"same_hour_corr={corr_pairs(concurrent):.3f} "
              f"btc_leads_one_hour_corr={corr_pairs(btc_leads):.3f} "
              f"stock_leads_one_hour_corr={corr_pairs(stock_leads):.3f}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"measurement failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
