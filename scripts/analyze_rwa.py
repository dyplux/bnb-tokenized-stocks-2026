#!/usr/bin/env python3
"""Analyze live collector records without treating derived reference as a stock quote."""

import csv
import json
from math import ceil
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from datetime import datetime
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "data/market_hours"
CATALOG = ROOT / "data/normalized/rwa_catalog.json"
MARKET_HOURS_SOURCE = "https://www.nasdaq.com/market-activity"


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def decimal(value):
    try:
        result = Decimal(str(value))
        return result if result.is_finite() else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def age_distribution(values):
    """Describe observed token-clock ages; this says nothing about stock reference age."""
    ordered = sorted(values)
    if not ordered:
        return {"count": 0}
    return {
        "count": len(ordered),
        "median_ms": int(median(ordered)),
        "p95_ms_nearest_rank": ordered[ceil(0.95 * len(ordered)) - 1],
        "max_ms": ordered[-1],
        "over_60_seconds": sum(age > 60_000 for age in ordered),
        "over_300_seconds": sum(age > 300_000 for age in ordered),
    }


def session_context(observed):
    """Classify the New York wall clock, without claiming a venue is open."""
    local = observed.astimezone(ZoneInfo("America/New_York"))
    if local.weekday() >= 5:
        return "weekend"
    clock = (local.hour, local.minute)
    if (4, 0) <= clock < (9, 30):
        return "weekday_premarket"
    if (9, 30) <= clock < (16, 0):
        return "weekday_regular"
    if (16, 0) <= clock < (20, 0):
        return "weekday_afterhours"
    return "weekday_outside_published_sessions"


def main():
    samples = []
    for path in sorted(MARKET.glob("20??-??-??.jsonl")):
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if row.get("origin") == "LIVE" and row.get("sample_id"):
                    samples.append(row)
    by_id = {row["sample_id"]: row for row in samples}
    samples = sorted(by_id.values(), key=lambda x: (x["observed_at"], x["contract"]))

    freshness = []
    ages_by_status = defaultdict(list)
    ages_by_provider = defaultdict(list)
    ages_by_session = defaultdict(list)
    market_review = Counter()
    future_token_timestamps = 0
    for row in samples:
        status = row.get("market_status") or "unknown"
        observed = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
        token_updated = row.get("token_price_updated_at_ms")
        age = int(observed.timestamp() * 1000) - token_updated if isinstance(token_updated, int) else None
        if isinstance(age, int) and age < 0:
            future_token_timestamps += 1
        session = session_context(observed)
        review = "UNKNOWN" if status == "unknown" else (
            "POTENTIAL_CONFLICT" if status == "regular" and session == "weekend" else
            "PLAUSIBLE_NOT_PROVEN" if session == "weekend" else "CALENDAR_AND_VENUE_UNVERIFIED")
        market_review[(session, status, review)] += 1
        if isinstance(age, int) and age >= 0:
            ages_by_status[status].append(age)
            ages_by_provider[row["provider"]].append(age)
            ages_by_session[session].append(age)
        freshness.append({
            "observed_at": row["observed_at"], "origin": row["origin"], "ticker": row["ticker"],
            "provider": row["provider"], "contract": row["contract"], "market_status": status,
            "token_price_updated_at_ms": row.get("token_price_updated_at_ms"),
            "token_price_age_ms": age, "legacy_collector_token_price_age_ms": row.get("token_price_age_ms"),
            "token_price_age_status": "UNKNOWN" if age is None else ("FUTURE_TIMESTAMP" if age < 0 else "OBSERVED"),
            "token_price_updated_at": row.get("token_price_updated_at", row.get("token_price_updated_at_ms")),
            "reference_price_updated_at": row.get("reference_price_updated_at"),
            "reference_age_seconds": row.get("reference_age_seconds"),
            "reference_age_status": row.get("reference_age_status", "UNKNOWN"),
            "market_session_context": session, "market_state_review": review,
            "independent_reference_timestamp": row.get("independent_reference_timestamp"),
            "independent_reference_age_ms": row.get("independent_reference_age_ms"),
            "reference_semantics": "derived_from_token_price_in_current_API_docs",
            "raw_price_response_sha256": row.get("price_response_sha256"),
        })
    reference = ROOT / "experiments/EXP-RWA-010"
    write_csv(reference / "reference_freshness.csv", list(freshness[0]) if freshness else [
        "observed_at", "origin", "ticker", "provider", "contract", "market_status",
        "token_price_updated_at_ms", "token_price_age_ms", "legacy_collector_token_price_age_ms",
        "token_price_age_status", "token_price_updated_at",
        "reference_price_updated_at", "reference_age_seconds", "reference_age_status",
        "market_session_context", "market_state_review", "independent_reference_timestamp",
        "independent_reference_age_ms", "reference_semantics", "raw_price_response_sha256"], freshness)
    results = {
        "sample_count": len(samples), "first_observed_at": samples[0]["observed_at"] if samples else None,
        "last_observed_at": samples[-1]["observed_at"] if samples else None,
        "origin": "LIVE only; no Saturday backfill",
        "reference_timestamp_availability": {
            "independent_reference_age_observations": sum(row.get("reference_age_seconds") is not None for row in samples),
            "unknown_reference_age_rows": sum(row.get("reference_age_seconds") is None for row in samples),
            "documented_field_available": False,
        },
        "token_price_freshness": {"age_calculation": "observed_at minus tokenPriceUpdatedAt, recomputed from raw timestamps for every row",
                                  "median_nonnegative_age_ms_by_api_market_status": {k: int(median(v)) for k, v in ages_by_status.items()},
                                  "median_nonnegative_age_ms_by_session_context": {k: int(median(v)) for k, v in ages_by_session.items()},
                                  "age_distribution_by_provider": {k: age_distribution(v) for k, v in sorted(ages_by_provider.items())},
                                  "with_timestamp": sum(row.get("token_price_updated_at_ms") is not None for row in samples),
                                  "future_timestamp_rows": future_token_timestamps},
        "market_state_correctness": {"basis": "Nasdaq published premarket 04:00 to 09:30, regular 09:30 to 16:00 and after-hours 16:00 to 20:00 ET; no holiday, early-close, security halt or venue validation",
                                     "published_hours_source": MARKET_HOURS_SOURCE,
                                     "review_counts": [{"market_session_context": k[0], "api_status": k[1],
                                                        "review": k[2], "count": v} for k, v in sorted(market_review.items())],
                                     "independent_validation": False},
        "status_counts": dict(Counter(row.get("market_status") or "unknown" for row in samples)),
        "conclusion": "The API supplies tokenPriceUpdatedAt, not an independently sourced stock-reference timestamp. Independent reference freshness is unmeasured.",
        "source": "https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data",
    }
    # Compare only identical ticker-minute slots with both providers present.
    # This reduces universe bias, but it doesn't make the instruments equivalent.
    paired_slots = defaultdict(dict)
    for row in freshness:
        if row["provider"] in {"bstock", "ondo"} and row["token_price_age_status"] == "OBSERVED":
            paired_slots[(row["observed_at"][:16], row["ticker"])][row["provider"]] = row
    paired = [slot for slot in paired_slots.values() if {"bstock", "ondo"} <= slot.keys()]
    results["token_price_freshness"]["matched_ticker_minute_slots"] = {
        "pair_count": len(paired),
        "tickers": sorted({slot["bstock"]["ticker"] for slot in paired}),
        "basis": "same ticker and UTC minute, independent token update clocks; no economic equivalence inferred",
        "by_provider": {
            provider: age_distribution([slot[provider]["token_price_age_ms"] for slot in paired])
            for provider in ("bstock", "ondo")
        },
    }
    (reference / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    latest = {}
    for row in samples:
        latest[row["contract"]] = row
    audit = []
    for row in catalog["rows"]:
        price_row = latest.get(row["contract"])
        price = decimal(price_row.get("token_price_usd")) if price_row else None
        ratio = decimal(row.get("token_to_share_ratio"))
        per_share = price / ratio if price is not None and ratio is not None and ratio > 0 else None
        audit.append({
            "captured_at": catalog["captured_at"], "source": row["source"], "ticker": row["ticker"],
            "provider": row["provider"], "contract": row["contract"], "decimals": row.get("decimals"),
            "token_to_share_ratio": str(ratio) if ratio is not None else None,
            "ratio_captured_at": catalog["captured_at"], "ratio_source_sha256": catalog["raw_response_sha256"],
            "listed_multiplier_raw": row.get("listed_multiplier_raw"),
            "token_price_usd_latest": str(price) if price is not None else None,
            "price_observed_at": price_row.get("observed_at") if price_row else None,
            "price_response_sha256": price_row.get("price_response_sha256") if price_row else None,
            "per_share_math_usd": str(per_share) if per_share is not None else None,
            "normalization_state": "mixed_time_arithmetic_not_equivalence" if per_share is not None else "ratio_or_price_unverified",
            "rights_and_corporate_action_verified": False,
        })
    write_csv(ROOT / "experiments/EXP-RWA-002/share_ratio_audit.csv", list(audit[0]) if audit else [], audit)
    by_security = defaultdict(dict)
    for row in catalog["rows"]:
        if row["provider"] in ("bstock", "ondo") and row.get("asset_type") == 1:
            by_security[row["ticker"]][row["provider"]] = row
    pairs = []
    for ticker, providers in sorted(by_security.items()):
        if not all(p in providers for p in ("bstock", "ondo")):
            continue
        b, o = providers["bstock"], providers["ondo"]
        pb, po = decimal(b.get("token_price_usd")), decimal(o.get("token_price_usd"))
        rb, ro = decimal(b.get("token_to_share_ratio")), decimal(o.get("token_to_share_ratio"))
        if None in (pb, po, rb, ro) or min(pb, po, rb, ro) <= 0:
            continue
        nb, no = pb / rb, po / ro
        pairs.append({"captured_at": catalog["captured_at"], "ticker": ticker,
                      "bstock_contract": b["contract"], "ondo_contract": o["contract"],
                      "bstock_token_price_usd": str(pb), "ondo_token_price_usd": str(po),
                      "bstock_ratio": str(rb), "ondo_ratio": str(ro),
                      "raw_gap_pct": str(abs(pb - po) / min(pb, po) * 100),
                      "normalized_gap_pct": str(abs(nb - no) / min(nb, no) * 100),
                      "normalized_bstock_usd": str(nb), "normalized_ondo_usd": str(no),
                      "equivalence_verified": False, "executable_spread_verified": False})
    write_csv(ROOT / "experiments/EXP-RWA-002/share_ratio_pairs.csv", list(pairs[0]) if pairs else [], pairs)
    ratio_summary = {"captured_at": catalog["captured_at"], "signed_stock_pairs": len(pairs),
                     "raw_gap_over_10pct": sum(decimal(x["raw_gap_pct"]) > 10 for x in pairs),
                     "raw_over_10pct_but_normalized_under_2pct": sum(
                         decimal(x["raw_gap_pct"]) > 10 and decimal(x["normalized_gap_pct"]) < 2 for x in pairs),
                     "largest_raw_gaps": sorted(pairs, key=lambda x: decimal(x["raw_gap_pct"]), reverse=True)[:8],
                     "claim_limit": "Catalog prices are a snapshot. Ratio arithmetic doesn't verify economic rights, redemption or executable spread."}
    (ROOT / "experiments/EXP-RWA-002/results.json").write_text(
        json.dumps(ratio_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    quotes_path = ROOT / "experiments/EXP-RWA-009/quote_depth.csv"
    if quotes_path.exists():
        with quotes_path.open(newline="", encoding="utf-8") as stream:
            quotes = list(csv.DictReader(stream))
        impacts = [decimal(x["price_impact_percent_reported"]) for x in quotes
                   if x.get("price_impact_percent_reported")]
        quote_summary = {"quote_count": len(quotes), "contracts": sorted({x["contract"] for x in quotes}),
                         "sizes_usdc": sorted({int(x["size_usdc"]) for x in quotes}),
                         "input_units_verified_count": sum(x["input_units_verified"] == "True" for x in quotes),
                         "route_count": sum(int(x["route_count"]) for x in quotes),
                         "reported_price_impact_range_pct": [str(min(impacts)), str(max(impacts))] if impacts else None,
                         "fills_observed": 0, "holder_eligibility_verified": False,
                         "claim_limit": "Read-only short-lived quote estimates from an ephemeral nonholder; no settled execution, final fee or exit route is proved."}
        (ROOT / "experiments/EXP-RWA-009/results.json").write_text(
            json.dumps(quote_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"samples": len(samples), "catalog_rows": len(audit),
                      "reference_age_observations": results["reference_timestamp_availability"]["independent_reference_age_observations"],
                      "with_per_share_math": sum(row["per_share_math_usd"] is not None for row in audit),
                      "signed_stock_pairs": len(pairs)}))


if __name__ == "__main__":
    main()
