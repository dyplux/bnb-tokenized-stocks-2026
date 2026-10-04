#!/usr/bin/env python3
"""Check token-derived referencePrice arithmetic in one complete LIVE slot."""

import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def formula_check(row):
    try:
        price = Decimal(str(row["token_price_usd"]))
        ratio = Decimal(str(row["token_to_share_ratio"]))
        reference = Decimal(str(row["derived_reference_price_usd"]))
        if not all(value.is_finite() and value > 0 for value in (price, ratio, reference)):
            raise ValueError("positive finite values required")
        calculated = price / ratio
        delta = abs(calculated - reference)
        precision = Decimal(1).scaleb(reference.as_tuple().exponent)
    except (KeyError, TypeError, InvalidOperation, ValueError, ZeroDivisionError):
        return {"formula_state": "MISSING_OR_INVALID", "calculated_per_share_usd": None,
                "absolute_delta_usd": None, "reported_precision_usd": None}
    return {"formula_state": "MATCH_AT_REPORTED_PRECISION" if delta <= precision / 2 else "MISMATCH",
            "calculated_per_share_usd": str(calculated), "absolute_delta_usd": str(delta),
            "reported_precision_usd": str(precision)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="UTC date, YYYY-MM-DD")
    args = parser.parse_args(argv)
    tape = ROOT / "data/market_hours" / (args.date + ".jsonl")
    grouped = defaultdict(dict)
    for line in tape.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("origin") == "LIVE" and isinstance(row.get("slot"), int):
            grouped[row["slot"]][row["contract"]] = row
    expected = json.loads((ROOT / "data/market_hours/checkpoint.json").read_text(encoding="utf-8"))["contracts_sampled"]
    slots = [slot for slot, rows in grouped.items() if len(rows) == expected]
    if not slots:
        raise SystemExit("no complete LIVE slot to audit")
    slot = max(slots)
    output_rows = []
    for row in sorted(grouped[slot].values(), key=lambda value: (value["ticker"], value["provider"])):
        output_rows.append({"observed_at": row["observed_at"], "slot": slot, "ticker": row["ticker"],
                            "provider": row["provider"], "contract": row["contract"],
                            "token_price_usd": row.get("token_price_usd"),
                            "token_to_share_ratio": row.get("token_to_share_ratio"),
                            "api_reference_price_usd": row.get("derived_reference_price_usd"),
                            "catalog_response_sha256": row.get("catalog_sha256"),
                            "price_response_sha256": row.get("price_response_sha256"),
                            **formula_check(row)})
    target = ROOT / "experiments/EXP-RWA-002"
    target.mkdir(parents=True, exist_ok=True)
    with (target / "reference_formula_audit.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    counts = {state: sum(row["formula_state"] == state for row in output_rows)
              for state in ("MATCH_AT_REPORTED_PRECISION", "MISMATCH", "MISSING_OR_INVALID")}
    result = {"date_utc": args.date, "slot": slot, "contract_count": len(output_rows),
              "first_observed_at": min(row["observed_at"] for row in output_rows),
              "last_observed_at": max(row["observed_at"] for row in output_rows),
              "formula": "token_price_usd / token_to_share_ratio",
              "counts": counts,
              "claim_limit": "Catalog and price responses were separate calls in one collector cycle. This checks token-derived arithmetic only; it is not an independent stock quote or proof of economic rights."}
    (target / "reference_formula_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
