#!/usr/bin/env python3
"""Build a dated, static judge packet without credentials or trading access."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.rwa_policy import evaluate

OUT = ROOT / "docs/judge"
SOURCE = ROOT / "app/fixtures/safety-nvdab-2026-10-04.json"


def write(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    observed = json.loads(SOURCE.read_text(encoding="utf-8"))
    if observed.get("origin") != "DATED_REPLAY" or observed.get("decision") != "NEED_HUMAN":
        raise ValueError("Observed fixture must remain a dated, uncertain result")
    write("observed-unsafe.json", observed)

    now = datetime(2026, 10, 4, 16, 45, tzinfo=timezone.utc)
    contract = "0x" + "1" * 40
    intent = {"chain_id": "56", "ticker": "TEST", "provider": "fixture",
              "contract": contract, "notional_usd": "10"}
    mandate = {"max_token_price_age_ms": 60000, "require_independent_reference": True,
               "max_reference_age_seconds": 60, "max_notional_usd": "10",
               "max_price_impact_percent": "0.5", "max_eligibility_age_seconds": 3600}
    evidence = {"chain_id": "56", "ticker": "TEST", "provider": "fixture", "contract": contract,
                "issuer_verified": True, "eligibility_status": "ELIGIBLE",
                "eligibility_basis": "SYNTHETIC_FIXTURE_ONLY",
                "eligibility_checked_at": "2026-10-04T16:44:00Z",
                "token_to_share_ratio": "1", "previous_token_to_share_ratio": "1",
                "market_status": "regular", "market_reason": None,
                "token_price_age_ms": 1000,
                "token_price_age_calculation": "observed_at_minus_tokenPriceUpdatedAt",
                "reference_price_updated_at": "SYNTHETIC_FIXTURE_ONLY",
                "reference_age_seconds": 10, "reference_age_status": "OBSERVED",
                "quote_available": True, "quote_identity_match": True,
                "quote_execution_mode": "SWAP", "quote_vendor": "SYNTHETIC_FIXTURE_ONLY",
                "price_impact_percent": "0.1", "simulation_passed": True,
                "source_response_sha256": "SYNTHETIC_FIXTURE_ONLY"}
    safe = evaluate(intent, evidence, mandate, now=now)
    if safe["decision"] != "ALLOW":
        raise ValueError("Synthetic policy fixture no longer allows")
    write("synthetic-safe.json", {"origin": "SYNTHETIC_POLICY_FIXTURE",
                                  "disclosure": "Every input is synthetic. No issuer access, funded simulation or trade is proven.",
                                  "receipt": safe})
    print("Wrote one observed NEED_HUMAN replay and one labelled synthetic ALLOW fixture")


if __name__ == "__main__":
    main()
