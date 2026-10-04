#!/usr/bin/env python3
"""Summarize live Sunday token-price movement without claiming a stock benchmark."""

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
TAPE = ROOT / "data/market_hours/2026-10-04.jsonl"
OUTPUT = ROOT / "experiments/EXP-RWA-004"
SLOT_SECONDS = 300  # The current collector is configured for five-minute slots.
MAX_WITHIN_SLOT_SKEW_SECONDS = 60


def main():
    grouped = defaultdict(list)
    for line in TAPE.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("origin") == "LIVE" and row.get("token_price_usd") is not None:
            grouped[row["contract"]].append(row)
    summaries = []
    for contract, observations in grouped.items():
        observations.sort(key=lambda row: row["observed_at"])
        prices = [Decimal(str(row["token_price_usd"])) for row in observations]
        updated = [row.get("token_price_updated_at_ms") for row in observations
                   if isinstance(row.get("token_price_updated_at_ms"), int)]
        low, high = min(prices), max(prices)
        summaries.append({"ticker": observations[0]["ticker"], "provider": observations[0]["provider"],
                          "contract": contract, "sample_count": len(observations),
                          "first_observed_at": observations[0]["observed_at"],
                          "last_observed_at": observations[-1]["observed_at"],
                          "first_token_price_usd": str(prices[0]), "last_token_price_usd": str(prices[-1]),
                          "min_token_price_usd": str(low), "max_token_price_usd": str(high),
                          "observed_token_price_range_pct": str((high - low) / low * 100) if low > 0 else None,
                          "token_price_timestamp_changed": len(set(updated)) > 1,
                          "reference_price_updated_at": None, "reference_age_seconds": None,
                          "reference_age_status": "UNKNOWN"})
    summaries.sort(key=lambda row: (row["ticker"], row["provider"]))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "sunday_token_price_ranges.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summaries[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)
    slots_by_contract = {
        contract: {row["slot"]: row for row in observations if isinstance(row.get("slot"), int)}
        for contract, observations in grouped.items()
    }
    candidate_slots = sorted(set.intersection(*(set(rows) for rows in slots_by_contract.values()))) if slots_by_contract else []
    common_slots = []
    for slot in candidate_slots:
        times = [datetime.fromisoformat(rows[slot]["observed_at"].replace("Z", "+00:00"))
                 for rows in slots_by_contract.values()]
        if (max(times) - min(times)).total_seconds() <= MAX_WITHIN_SLOT_SKEW_SECONDS:
            common_slots.append(slot)
    common_window = []
    if len(common_slots) >= 2:
        for contract, by_slot in slots_by_contract.items():
            rows = [by_slot[slot] for slot in common_slots]
            prices = [Decimal(str(row["token_price_usd"])) for row in rows]
            low, high = min(prices), max(prices)
            common_window.append({"ticker": rows[0]["ticker"], "provider": rows[0]["provider"],
                                  "contract": contract, "sample_count": len(rows),
                                  "first_observed_at": rows[0]["observed_at"],
                                  "last_observed_at": rows[-1]["observed_at"],
                                  "token_price_range_pct": str((high - low) / low * 100) if low > 0 else None})
        common_window.sort(key=lambda row: (row["ticker"], row["provider"]))
        with (OUTPUT / "common_window_ranges.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(common_window[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(common_window)
    original = [row for row in summaries if row["sample_count"] >= 10]
    result = {"origin": "LIVE", "date_utc": "2026-10-04", "contract_count": len(summaries),
              "first_observed_at": min(row["first_observed_at"] for row in summaries),
              "last_observed_at": max(row["last_observed_at"] for row in summaries),
              "contracts_with_at_least_10_samples": len(original),
              "token_price_timestamp_changed_count": sum(row["token_price_timestamp_changed"] for row in original),
              "median_observed_token_price_range_pct_for_10_sample_set":
                  str(median(Decimal(row["observed_token_price_range_pct"]) for row in original)) if original else None,
              "common_window_slot_count": len(common_slots),
              "common_window_slot_seconds": SLOT_SECONDS,
              "common_window_max_within_slot_skew_seconds": MAX_WITHIN_SLOT_SKEW_SECONDS,
              "common_window_first_slot": common_slots[0] if common_slots else None,
              "common_window_last_slot": common_slots[-1] if common_slots else None,
              "common_window_first_slot_at": datetime.fromtimestamp(common_slots[0] * SLOT_SECONDS, timezone.utc).isoformat() if common_slots else None,
              "common_window_last_slot_at": datetime.fromtimestamp(common_slots[-1] * SLOT_SECONDS, timezone.utc).isoformat() if common_slots else None,
              "common_window_contract_count": len(common_window),
              "median_token_price_range_pct_same_slots":
                  str(median(Decimal(row["token_price_range_pct"]) for row in common_window)) if common_window else None,
              "independent_reference_age_observations": 0,
              "claim_limit": "Short Sunday window, token prices only. No independent stock reference, fills, prediction or repeatability across weekends."}
    (OUTPUT / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
