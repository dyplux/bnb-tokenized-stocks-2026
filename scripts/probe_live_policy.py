#!/usr/bin/env python3
"""Run the read-only policy against one frozen LIVE tape slot, with no invented gates."""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.rwa_policy import evaluate
MANDATE = {"max_token_price_age_ms": 60000, "require_independent_reference": True,
           "max_reference_age_seconds": 60, "max_notional_usd": "100",
           "max_price_impact_percent": "1"}


def probe(row):
    observed = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
    intent = {"chain_id": "56", "ticker": row["ticker"], "provider": row["provider"],
              "contract": row["contract"], "notional_usd": "100"}
    evidence = {"chain_id": row["chain_id"], "ticker": row["ticker"],
                "provider": row["provider"], "contract": row["contract"],
                "issuer_verified": None, "token_to_share_ratio": row.get("token_to_share_ratio"),
                "previous_token_to_share_ratio": None, "corporate_action_verified": None,
                "market_status": row.get("market_status"), "market_reason": row.get("market_reason"),
                "token_price_age_ms": row.get("token_price_age_ms"),
                "token_price_age_calculation": row.get("token_price_age_calculation"),
                "reference_price_updated_at": row.get("reference_price_updated_at"),
                "reference_age_seconds": row.get("reference_age_seconds"),
                "reference_age_status": row.get("reference_age_status", "UNKNOWN"),
                "quote_available": None, "price_impact_percent": None,
                "simulation_passed": None, "source_response_sha256": row.get("price_response_sha256")}
    receipt = evaluate(intent, evidence, MANDATE, now=observed)
    return {"ticker": row["ticker"], "provider": row["provider"], "contract": row["contract"],
            "observed_at": row["observed_at"], "decision": receipt["decision"],
            "reason_codes": receipt["reason_codes"], "policy_version": receipt["policy_version"],
            "receipt_sha256": receipt["receipt_sha256"],
            "catalog_response_sha256": row.get("catalog_sha256"),
            "price_response_sha256": row.get("price_response_sha256")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slot", type=int, required=True)
    args = parser.parse_args(argv)
    tape = ROOT / "data/market_hours/2026-10-04.jsonl"
    rows = [json.loads(line) for line in tape.read_text(encoding="utf-8").splitlines()]
    selected = [row for row in rows if row.get("origin") == "LIVE" and row.get("slot") == args.slot]
    expected = json.loads((ROOT / "data/market_hours/checkpoint.json").read_text(encoding="utf-8"))["contracts_sampled"]
    if len(selected) != expected or len({row["contract"] for row in selected}) != expected:
        raise SystemExit("selected slot is not a complete, unique LIVE universe")
    decisions = [probe(row) for row in selected]
    decisions.sort(key=lambda row: (row["ticker"], row["provider"]))
    reasons = Counter(reason for result in decisions for reason in result["reason_codes"])
    output = {"origin": "LIVE tape with SYNTHETIC 100 USD intent; no holder, quote, simulation or trade",
              "slot": args.slot, "contract_count": len(decisions), "mandate": MANDATE,
              "decision_counts": dict(Counter(row["decision"] for row in decisions)),
              "reason_counts": dict(sorted(reasons.items())), "rows": decisions,
              "claim_limit": "This is a fail-closed offline capability audit. Unknown issuer access, reference time, quote, impact and simulation weren't filled with assumptions. No user benefit or executable action is proved."}
    target = ROOT / "experiments/EXP-RWA-010/live_policy_probe.json"
    target.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("slot", "contract_count", "decision_counts", "reason_counts")}, sort_keys=True))


if __name__ == "__main__":
    main()
