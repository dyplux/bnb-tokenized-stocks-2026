#!/usr/bin/env python3
"""Score the frozen Sunday token rows against dated Monday daily stock bars."""

import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments/EXP-RWA-004"


def positive_decimal(value):
    try:
        number = Decimal(str(value))
        return number if number.is_finite() and number > 0 else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def pct(change_from, change_to):
    return (change_to / change_from - 1) * 100 if change_from and change_to else None


def direction(value):
    return (value > 0) - (value < 0) if value is not None else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outcome_json", type=Path, help="dated external daily rows; never an issuer reference clock")
    args = parser.parse_args()
    source = json.loads(args.outcome_json.read_text(encoding="utf-8"))
    if source.get("session_date") != "2026-10-05" or not source.get("retrieved_at") or not source.get("publisher"):
        raise SystemExit("outcome must identify the 2026-10-05 session, retrieval time and publisher")
    outcomes = {}
    for item in source.get("rows", []):
        ticker = item.get("ticker")
        if ticker in outcomes:
            raise SystemExit("duplicate outcome ticker: %s" % ticker)
        if ticker not in {"COIN", "NVDA", "TSLA"} or not item.get("source_url"):
            raise SystemExit("unfrozen ticker or missing direct source URL")
        outcomes[ticker] = item
    if not any(positive_decimal(item.get("open_usd")) for item in outcomes.values()):
        raise SystemExit("no dated Monday opening value; don't generate an outcome from missing data")
    with (EXPERIMENT / "friday_close_benchmark.csv").open(newline="", encoding="utf-8") as stream:
        frozen = list(csv.DictReader(stream))
    if len(frozen) != 6 or {row["ticker"] for row in frozen} != {"COIN", "NVDA", "TSLA"}:
        raise SystemExit("Sunday's frozen six-row sample isn't available")
    scored = []
    for row in frozen:
        external = outcomes.get(row["ticker"], {})
        friday = positive_decimal(row["external_close_usd"])
        sunday = positive_decimal(row["token_derived_per_share_usd"])
        monday_open = positive_decimal(external.get("open_usd"))
        monday_close = positive_decimal(external.get("close_usd"))
        sunday_move = pct(friday, sunday)
        open_move = pct(friday, monday_open)
        residual = pct(sunday, monday_open)
        scored.append({
            "ticker": row["ticker"], "provider": row["provider"], "contract": row["contract"],
            "sunday_origin": "LIVE", "sunday_observed_at": row["token_observed_at"],
            "sunday_slot": 5970384, "sunday_per_share_arithmetic_usd": str(sunday) if sunday else None,
            "friday_session_date": row["external_session_date"], "friday_close_usd": str(friday) if friday else None,
            "monday_session_date": source["session_date"],
            "monday_open_usd": str(monday_open) if monday_open else None,
            "monday_close_usd": str(monday_close) if monday_close else None,
            "friday_to_sunday_pct": str(sunday_move) if sunday_move is not None else None,
            "friday_to_monday_open_pct": str(open_move) if open_move is not None else None,
            "sunday_to_monday_open_pct": str(residual) if residual is not None else None,
            "direction_match": direction(sunday_move) == direction(open_move) if open_move is not None and sunday_move is not None else None,
            "external_source_url": external.get("source_url"),
            "external_retrieved_at": source["retrieved_at"],
            "external_timestamp_status": "SESSION_DATE_ONLY_NO_INDEPENDENT_TRADE_TIMESTAMP",
            "issuer_reference_age_status": "UNKNOWN",
        })
    scored.sort(key=lambda item: (item["ticker"], item["provider"]))
    destination = EXPERIMENT / "monday_open_benchmark.csv"
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(scored[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(scored)
    residuals = [abs(Decimal(row["sunday_to_monday_open_pct"])) for row in scored
                 if row["sunday_to_monday_open_pct"] is not None]
    by_ticker = {}
    for ticker in ("COIN", "NVDA", "TSLA"):
        pair = [row for row in scored if row["ticker"] == ticker]
        values = [positive_decimal(row["sunday_per_share_arithmetic_usd"]) for row in pair]
        by_ticker[ticker] = {
            "issuer_values_usd": {row["provider"]: row["sunday_per_share_arithmetic_usd"] for row in pair},
            "sunday_issuer_range_usd": str(max(values) - min(values)) if all(values) else None,
        }
    result = {
        "sample_rows": 6, "independent_underlyings": 3, "outcome_source": source["publisher"],
        "outcome_session_date": source["session_date"], "outcome_retrieved_at": source["retrieved_at"],
        "available_open_rows": sum(row["monday_open_usd"] is not None for row in scored),
        "direction_match_rows": sum(row["direction_match"] is True for row in scored),
        "direction_mismatch_rows": sum(row["direction_match"] is False for row in scored),
        "median_absolute_sunday_to_open_residual_pct": str(median(residuals)) if residuals else None,
        "by_ticker": by_ticker,
        "reference_price_updated_at": None, "reference_age_status": "UNKNOWN",
        "claim_limit": "One weekend, three dependent underlyings, external session-date bars, no Friday after-hours baseline, trade fill or issuer-reference timestamp. No predictive alpha or executable profit is established.",
    }
    (EXPERIMENT / "monday_open_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"available_open_rows": result["available_open_rows"],
                      "median_absolute_residual_pct": result["median_absolute_sunday_to_open_residual_pct"]}))


if __name__ == "__main__":
    main()
