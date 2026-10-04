#!/usr/bin/env python3
"""Reproduce the bounded xStock price coverage probe from retained raw bodies."""

import csv
import gzip
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
HASHES = (
    "3b4c01367d92c8c9755b48e8cc9aa7eae7c511f6a53fff010c287a0f2986016e",
    "2a6045957874d92069d9a576dd329c433791b57bcd9509225763ab4cbcbd00d7",
    "fe04c9aa4a2841612cc19e5bf599ee9fca9cb7620e6bedce94cca72aebf2daf0",
    "71c1e83ae2380e9eef4940e7168aa0e2e597bf8b43e66ac20261ff0ca0835e5c",
)


def main():
    manifest = [json.loads(line) for line in (ROOT / "data/market_hours/raw/manifest.jsonl").read_text().splitlines()]
    by_hash = {x["sha256"]: x for x in manifest}
    catalog = json.loads((ROOT / "data/normalized/rwa_catalog.json").read_text())
    listed = {x["contract"]: x for x in catalog["rows"] if x["provider"] == "xstocks_public_listing"}
    rows = []
    for digest in HASHES:
        entry = by_hash[digest]
        body = gzip.open(ROOT / entry["path"], "rb").read()
        if hashlib.sha256(body).hexdigest() != digest:
            raise RuntimeError("raw response hash mismatch")
        payload = json.loads(body)
        observed = datetime.fromisoformat(entry["captured_at"].replace("Z", "+00:00"))
        for item in payload["data"]:
            contract = item["tokenContractAddress"].lower()
            timestamp = item.get("tokenPriceUpdatedAt")
            age = round(observed.timestamp() - timestamp / 1000, 3) if isinstance(timestamp, int) else None
            rows.append({"observed_at": entry["captured_at"], "origin": "LIVE",
                         "ticker": listed[contract]["ticker"], "contract": contract,
                         "provider_listing": "xstocks_public_listing", "api_platform_id": item.get("platformId"),
                         "token_price_usd": item.get("tokenPrice"),
                         "token_price_updated_at": timestamp, "token_price_age_seconds": age,
                         "derived_reference_price_usd": item.get("referencePrice"),
                         "reference_price_updated_at": None, "reference_age_seconds": None,
                         "reference_age_status": "UNKNOWN", "raw_response_sha256": digest})
    rows.sort(key=lambda x: (x["ticker"], x["contract"]))
    if len(rows) != len(listed) or len({x["contract"] for x in rows}) != len(listed):
        raise RuntimeError("probe result doesn't cover every listed xStock once")
    output = ROOT / "experiments/EXP-RWA-001"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "xstock_price_probe.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    ages = [x["token_price_age_seconds"] for x in rows if x["token_price_age_seconds"] is not None]
    bins = Counter("NO_PRICE_OR_TIME" if age is None else "UNDER_1H" if age <= 3600 else
                   "UNDER_24H" if age <= 86400 else "UNDER_7D" if age <= 604800 else "OVER_7D"
                   for age in (x["token_price_age_seconds"] for x in rows))
    result = {"captured_at_range": [min(x["observed_at"] for x in rows), max(x["observed_at"] for x in rows)],
              "requested": len(listed), "returned": len(rows), "with_price_and_token_timestamp": len(ages),
              "age_bins": dict(bins), "median_token_price_age_hours_if_present": round(median(ages) / 3600, 2),
              "raw_response_sha256": list(HASHES), "independent_reference_age_observations": 0,
              "claim_limit": "A returned row can contain null price and timestamp. Token-price time isn't an independent underlying-reference time. No ratio or executable route was established by this probe."}
    (output / "xstock_price_probe_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
