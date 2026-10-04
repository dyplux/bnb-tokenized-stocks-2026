#!/usr/bin/env python3
"""Read-only integrity audit for the market-hours JSONL tape."""

import argparse
import collections
import gzip
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


MARKET_DIR = Path("data/market_hours")
EXPECTED_AGE_CALCULATION = "observed_at_minus_tokenPriceUpdatedAt"


def _read_jsonl(path):
    rows = []
    problems = []
    if not path.exists():
        return rows, ["missing:{}".format(path)]
    if not path.is_file():
        return rows, ["not_a_file:{}".format(path)]
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    problems.append("{}:{}:{}".format(path, line_number, exc.msg))
                    continue
                if not isinstance(value, dict):
                    problems.append("{}:{}:object_required".format(path, line_number))
                    continue
                rows.append((line_number, value))
    except OSError as exc:
        problems.append("{}:{}".format(path, exc))
    return rows, problems


def _observed_at_ms(value):
    if not isinstance(value, str):
        raise ValueError("observed_at is not a string")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(round(parsed.timestamp() * 1000))


def _recorded_count(path):
    rows, problems = _read_jsonl(path)
    return len(rows), problems


def audit(root, date):
    market_dir = Path(root) / MARKET_DIR
    tape_path = market_dir / (date + ".jsonl")
    manifest_path = market_dir / "raw" / "manifest.jsonl"
    checkpoint_path = market_dir / "checkpoint.json"

    violations = []
    notes = []
    tape, tape_problems = _read_jsonl(tape_path)
    manifest, manifest_problems = _read_jsonl(manifest_path)
    violations.extend(tape_problems)
    violations.extend(manifest_problems)
    if tape_path.exists() and not tape:
        notes.append("empty:{}".format(tape_path))
    if manifest_path.exists() and not manifest:
        notes.append("empty:{}".format(manifest_path))

    manifest_times = []
    for line_number, entry in manifest:
        try:
            manifest_times.append(_observed_at_ms(entry["captured_at"]))
        except (KeyError, TypeError, ValueError):
            violations.append("manifest:{}:captured_at invalid".format(line_number))
    first_raw_capture_ms = min(manifest_times) if manifest_times else None

    def predates_raw_retention(row):
        if first_raw_capture_ms is None:
            return False
        try:
            return _observed_at_ms(row["observed_at"]) < first_raw_capture_ms
        except (KeyError, TypeError, ValueError):
            return False

    checkpoint = {}
    if checkpoint_path.exists():
        try:
            checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            violations.append("checkpoint:{}".format(exc))
    else:
        violations.append("missing:{}".format(checkpoint_path))
    expected_contracts = checkpoint.get("contracts_sampled")
    if not isinstance(expected_contracts, int) or expected_contracts <= 0:
        violations.append("checkpoint:contracts_sampled_required")
        expected_contracts = None

    live_sample_ids = set()
    slots = collections.defaultdict(set)
    current_age_rows = 0
    legacy_age_rows = 0
    legacy_reference_status_missing = 0
    for line_number, row in tape:
        if row.get("origin") == "LIVE":
            sample_id = row.get("sample_id")
            if not sample_id:
                violations.append("tape:{}:LIVE sample_id missing".format(line_number))
            elif sample_id in live_sample_ids:
                violations.append("tape:{}:duplicate LIVE sample_id {}".format(line_number, sample_id))
            else:
                live_sample_ids.add(sample_id)

        slot = row.get("slot")
        contract = row.get("contract")
        if row.get("origin") == "LIVE" and slot is not None and contract is not None:
            slots[slot].add(contract)

        if row.get("independent_reference_timestamp") is None:
            if row.get("reference_price_updated_at") is not None:
                violations.append("tape:{}:reference_price_updated_at must be null".format(line_number))
            if row.get("reference_age_seconds") is not None:
                violations.append("tape:{}:reference_age_seconds must be null".format(line_number))
            if "reference_age_status" not in row and predates_raw_retention(row) and not row.get("token_price_age_calculation"):
                legacy_reference_status_missing += 1
            elif row.get("reference_age_status") != "UNKNOWN":
                violations.append("tape:{}:reference_age_status must be UNKNOWN".format(line_number))

        if row.get("token_price_age_calculation") == EXPECTED_AGE_CALCULATION:
            current_age_rows += 1
            try:
                expected_age = _observed_at_ms(row["observed_at"]) - int(row["token_price_updated_at_ms"])
                actual_age = int(row["token_price_age_ms"])
                if abs(actual_age - expected_age) > 1:
                    violations.append("tape:{}:token_price_age_ms expected {} got {}".format(
                        line_number, expected_age, actual_age))
            except (KeyError, TypeError, ValueError, OverflowError) as exc:
                violations.append("tape:{}:invalid current token age ({})".format(line_number, exc))
        else:
            legacy_age_rows += 1

    partial_initial_slots = []
    complete_slots = []
    if expected_contracts is not None and slots:
        sorted_slots = sorted(slots)
        first_complete_seen = False
        for slot in sorted_slots:
            count = len(slots[slot])
            if not first_complete_seen and count < expected_contracts:
                partial_initial_slots.append({"slot": slot, "distinct_contracts": count})
                continue
            first_complete_seen = True
            complete_slots.append(slot)
            if count != expected_contracts:
                violations.append("slot:{}:expected {} distinct contracts got {}".format(
                    slot, expected_contracts, count))

    manifest_by_hash = {}
    for line_number, entry in manifest:
        digest = entry.get("sha256")
        path_value = entry.get("path")
        if not isinstance(digest, str) or not isinstance(path_value, str):
            violations.append("manifest:{}:sha256 and path required".format(line_number))
            continue
        manifest_by_hash[digest] = (line_number, path_value)

    observed_hashes = {row.get("price_response_sha256") for _, row in tape if row.get("price_response_sha256")}
    legacy_unmanifested_hashes = set()
    verified_raw = 0
    for digest in sorted(observed_hashes):
        entry = manifest_by_hash.get(digest)
        if entry is None:
            digest_rows = [row for _, row in tape if row.get("price_response_sha256") == digest]
            if digest_rows and all(predates_raw_retention(row) for row in digest_rows):
                legacy_unmanifested_hashes.add(digest)
            else:
                violations.append("raw:{}:price_response_sha256 absent from manifest".format(digest))
            continue
        line_number, path_value = entry
        raw_path = Path(path_value)
        if not raw_path.is_absolute():
            raw_path = Path(root) / raw_path
        try:
            with gzip.open(raw_path, "rb") as compressed:
                body = compressed.read()
            actual_digest = hashlib.sha256(body).hexdigest()
            if actual_digest != digest:
                violations.append("manifest:{}:sha256 mismatch for {}".format(line_number, raw_path))
            if actual_digest == digest:
                verified_raw += 1
        except (OSError, EOFError, gzip.BadGzipFile) as exc:
            violations.append("manifest:{}:invalid gzip {} ({})".format(line_number, raw_path, exc))

    gaps_count, gap_problems = _recorded_count(market_dir / "gaps.jsonl")
    errors_count, error_problems = _recorded_count(market_dir / "errors.jsonl")
    notes.extend(gap_problems + error_problems)
    summary = {
        "date": date,
        "ok": not violations,
        "rows": len(tape),
        "live_sample_ids": len(live_sample_ids),
        "slots": len(slots),
        "expected_contracts_per_complete_slot": expected_contracts,
        "complete_slots": len(complete_slots),
        "partial_initial_slots": partial_initial_slots,
        "observed_price_response_hashes": len(observed_hashes),
        "verified_raw_responses": verified_raw,
        "legacy_unmanifested_price_hashes": len(legacy_unmanifested_hashes),
        "legacy_reference_status_missing": legacy_reference_status_missing,
        "current_age_rows_checked": current_age_rows,
        "legacy_age_rows_counted": legacy_age_rows,
        "recorded_gaps": gaps_count,
        "recorded_errors": errors_count,
        "notes": notes,
        "violations": violations,
    }
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="tape date in YYYY-MM-DD form")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path,
                        help="repository root (default: repository containing this script)")
    args = parser.parse_args(argv)
    summary = audit(args.root, args.date)
    print(json.dumps(summary, separators=(",", ":"), sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
