#!/usr/bin/env python3
"""Summarize a dated append-only DevEx log without making network requests."""

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def nearest_rank(values, fraction):
    ordered = sorted(values)
    return ordered[max(0, min(len(ordered) - 1, math.ceil(len(ordered) * fraction) - 1))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="UTC date YYYY-MM-DD")
    args = parser.parse_args()
    path = ROOT / "docs/devex/raw" / (args.date + ".jsonl")
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    groups = defaultdict(list)
    for row in records:
        groups[(row.get("endpoint"), row.get("method"))].append(row)
    endpoints = []
    for (endpoint, method), rows in sorted(groups.items()):
        latencies = [float(r["latency_ms"]) for r in rows if isinstance(r.get("latency_ms"), (int, float))]
        http_codes = Counter(str(r.get("http_status")) for r in rows)
        business_codes = Counter(str(r.get("business_code")) for r in rows if "business_code" in r)
        endpoints.append({"endpoint": endpoint, "method": method, "calls": len(rows),
                          "http_status_counts": dict(http_codes), "business_code_counts": dict(business_codes),
                          "schema_mismatches": sum(r.get("schema_mismatch") is True for r in rows),
                          "median_latency_ms": round(statistics.median(latencies), 2) if latencies else None,
                          "p95_latency_ms_nearest_rank": round(nearest_rank(latencies, 0.95), 2) if latencies else None,
                          "max_latency_ms": round(max(latencies), 2) if latencies else None})
    result = {"date": args.date, "snapshot_last_logged_at": max((r.get("timestamp", "") for r in records), default=None),
              "request_count": len(records), "method": "append-only sanitized call ledger, not a controlled load benchmark",
              "endpoints": endpoints,
              "note": "Business rejections can be expected task outcomes; HTTP 200 isn't a successful quote or transaction. No request header, API key or wallet private key is included."}
    target = ROOT / "docs/devex" / (args.date + "-metrics.json")
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"request_count": len(records), "endpoints": len(endpoints),
                      "last_logged_at": result["snapshot_last_logged_at"]}))


if __name__ == "__main__":
    main()
