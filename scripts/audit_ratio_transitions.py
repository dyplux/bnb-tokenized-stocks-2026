#!/usr/bin/env python3
"""Find observed token/share ratio changes in the LIVE collector tape."""

import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "data/market_hours"
OUTPUT = ROOT / "experiments/EXP-RWA-011"


def ratio(value):
    try:
        result = Decimal(str(value))
        return result if result.is_finite() and result > 0 else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def transitions(observations):
    events = []
    previous = None
    missing = 0
    for row in sorted(observations, key=lambda item: item["observed_at"]):
        current = ratio(row.get("token_to_share_ratio"))
        if current is None:
            missing += 1
            continue
        if previous is not None and current != ratio(previous.get("token_to_share_ratio")):
            before = ratio(previous["token_to_share_ratio"])
            events.append({"ticker": row["ticker"], "provider": row["provider"],
                           "contract": row["contract"], "before_observed_at": previous["observed_at"],
                           "after_observed_at": row["observed_at"],
                           "before_ratio": str(before), "after_ratio": str(current),
                           "ratio_change_pct": str((current / before - 1) * 100),
                           "before_catalog_sha256": previous.get("catalog_sha256"),
                           "after_catalog_sha256": row.get("catalog_sha256"),
                           "issuer_event_verified": False,
                           "interpretation": "ratio_change_candidate_not_corporate_action_proof"})
        previous = row
    return events, missing


def main():
    by_contract = defaultdict(list)
    observations = 0
    for path in sorted(MARKET.glob("20??-??-??.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row.get("origin") == "LIVE" and row.get("sample_id"):
                by_contract[row["contract"]].append(row)
                observations += 1
    if not observations:
        raise SystemExit("no LIVE tape observations")
    events, missing = [], 0
    for rows in by_contract.values():
        found, absent = transitions(rows)
        events.extend(found)
        missing += absent
    events.sort(key=lambda row: (row["after_observed_at"], row["contract"]))
    fields = ["ticker", "provider", "contract", "before_observed_at", "after_observed_at",
              "before_ratio", "after_ratio", "ratio_change_pct", "before_catalog_sha256",
              "after_catalog_sha256", "issuer_event_verified", "interpretation"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "live_ratio_changes.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(events)
    result = {"origin": "LIVE collector tape", "observations": observations,
              "contracts": len(by_contract), "ratio_change_candidates": len(events),
              "rows_without_valid_ratio": missing,
              "first_observed_at": min(row["observed_at"] for rows in by_contract.values() for row in rows),
              "last_observed_at": max(row["observed_at"] for rows in by_contract.values() for row in rows),
              "claim_limit": "A ratio transition is a candidate event, not proof of a split, rebase or issuer notice. No pre-collector history is reconstructed."}
    (OUTPUT / "live_ratio_changes_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
