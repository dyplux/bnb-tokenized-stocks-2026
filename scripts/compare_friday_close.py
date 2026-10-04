#!/usr/bin/env python3
"""Compare one LIVE token-price slot with a dated external daily close."""

import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def percent_gap(token_price, ratio, close):
    try:
        price, shares, baseline = (Decimal(str(value)) for value in (token_price, ratio, close))
        if not all(value.is_finite() and value > 0 for value in (price, shares, baseline)):
            return None
        per_share = price / shares
        return per_share, (per_share / baseline - 1) * 100
    except (InvalidOperation, TypeError, ValueError, ZeroDivisionError):
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slot", type=int, required=True, help="frozen five-minute collector slot")
    args = parser.parse_args(argv)
    baseline = json.loads((ROOT / "data/external_reference/2026-10-02-yahoo-close.json").read_text(encoding="utf-8"))
    closes = {row["ticker"]: row for row in baseline["rows"]}
    tape = ROOT / "data/market_hours/2026-10-04.jsonl"
    found = []
    for line in tape.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("origin") != "LIVE" or row.get("slot") != args.slot or row.get("ticker") not in closes:
            continue
        close = closes[row["ticker"]]
        calculation = percent_gap(row.get("token_price_usd"), row.get("token_to_share_ratio"), close["close_usd"])
        if calculation is None:
            continue
        per_share, gap = calculation
        found.append({"token_observed_at": row["observed_at"], "ticker": row["ticker"],
                      "provider": row["provider"], "contract": row["contract"],
                      "token_price_usd": row["token_price_usd"],
                      "token_price_updated_at_ms": row.get("token_price_updated_at_ms"),
                      "token_to_share_ratio": row["token_to_share_ratio"],
                      "token_derived_per_share_usd": str(per_share),
                      "external_session_date": baseline["session_date"],
                      "external_close_usd": close["close_usd"],
                      "external_timestamp_status": baseline["timestamp_status"],
                      "reference_age_seconds": None,
                      "signed_gap_to_friday_close_pct": str(gap),
                      "external_source_url": close["source_url"],
                      "catalog_response_sha256": row.get("catalog_sha256"),
                      "price_response_sha256": row.get("price_response_sha256")})
    found.sort(key=lambda row: (row["ticker"], row["provider"]))
    if len(found) != 6:
        raise SystemExit("expected exactly two provider rows for each of three benchmark tickers; got %s" % len(found))
    target = ROOT / "experiments/EXP-RWA-004"
    with (target / "friday_close_benchmark.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(found[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(found)
    result = {"origin": "LIVE token tape plus separately retrieved Yahoo Finance historical closes",
              "slot": args.slot, "token_observed_at_first": found[0]["token_observed_at"],
              "token_observed_at_last": max(row["token_observed_at"] for row in found),
              "external_session_date": baseline["session_date"], "rows": len(found),
              "reference_age_status": "UNKNOWN", "reference_age_seconds": None,
              "claim_limit": "Session-date close only. Prices are token-derived per-share arithmetic; rights, after-hours benchmark, quote execution and Monday opening outcome remain unverified."}
    (target / "friday_close_benchmark_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
