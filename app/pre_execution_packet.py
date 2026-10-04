"""Read-only join of an exact-wallet policy quote, build and simulation.

This packet is an audit aid. It has no transaction, key, signer or broadcast path.
"""

import hashlib
import json

from app.server import USDT


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def assemble(review, dry_run):
    receipt = review.get("receipt") or {}
    reasons = []
    claimed_hash = receipt.get("receipt_sha256")
    unsigned_receipt = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if not claimed_hash or digest(unsigned_receipt) != claimed_hash:
        reasons.append("POLICY_RECEIPT_INVALID")
    if (review.get("decision") != receipt.get("decision") or
            review.get("reason_codes") != receipt.get("reason_codes")):
        reasons.append("POLICY_RESULT_MISMATCH")
    if review.get("origin") != "LIVE_READ_ONLY" or receipt.get("decision") != "ALLOW":
        reasons.append("POLICY_NOT_ALLOW")

    intent = receipt.get("intent") or {}
    security = dry_run.get("security") or {}
    same_action = (
        dry_run.get("origin") == "LIVE_READ_ONLY"
        and str(intent.get("chain_id")) == str(dry_run.get("chain_id")) == "56"
        and intent.get("ticker") == security.get("ticker") == "NVDA"
        and intent.get("provider") == dry_run.get("provider")
        and str(intent.get("contract", "")).lower() == str(security.get("contract", "")).lower()
        and str(intent.get("notional_usd")) == str(dry_run.get("notional_usdt"))
        and dry_run.get("side") == "BUY"
        and str(dry_run.get("source_token", "")).lower() == USDT.lower()
    )
    if not same_action:
        reasons.append("ACTION_EVIDENCE_MISMATCH")

    quote = dry_run.get("quote") or {}
    build = dry_run.get("build") or {}
    simulation = dry_run.get("simulation") or {}
    if quote.get("business_code") != 0 or quote.get("intent_match") is not True:
        reasons.append("EXACT_WALLET_QUOTE_UNVERIFIED")
    if build.get("business_code") != 0 or build.get("quote_build_intent_match") is not True:
        reasons.append("EXACT_WALLET_BUILD_UNVERIFIED")
    if simulation.get("api_business_code") != 0 or simulation.get("predicted_transaction_status") != "SUCCESS":
        reasons.append("EXACT_WALLET_SIMULATION_NOT_PASSED")

    source_quote = (review.get("sources") or {}).get("quote") or {}
    receipt_sources = (receipt.get("evidence") or {}).get("source_response_sha256") or {}
    quote_bound = (quote.get("bound_to_policy") is True and
                   quote.get("sha256") and quote.get("sha256") == source_quote.get("sha256") and
                   quote.get("sha256") == receipt_sources.get("quote") and
                   quote.get("observed_at") == source_quote.get("observed_at"))
    if not quote_bound:
        reasons.append("POLICY_QUOTE_NOT_BOUND_TO_EXECUTION")
    reasons.append("EXPLICIT_HUMAN_APPROVAL_MISSING")
    packet = {
        "state": "BLOCKED", "execution_authorized": False,
        "reason_codes": sorted(set(reasons)),
        "action": {"chain_id": intent.get("chain_id"), "ticker": intent.get("ticker"),
                   "provider": intent.get("provider"), "contract": intent.get("contract"),
                   "side": "BUY", "notional_usdt": intent.get("notional_usd")},
        "policy": {"decision": receipt.get("decision"),
                   "observed_at": receipt.get("timestamp"),
                   "reason_codes": receipt.get("reason_codes"),
                   "receipt_sha256": claimed_hash,
                   "receipt": receipt},
        "exact_wallet_trial": {"stage": dry_run.get("stage"),
                               "quote_observed_at": quote.get("observed_at"),
                               "quote_sha256": quote.get("sha256"),
                               "build_observed_at": build.get("observed_at"),
                               "build_sha256": build.get("sha256"),
                               "simulation_observed_at": simulation.get("observed_at"),
                               "simulation_sha256": simulation.get("sha256"),
                               "predicted_transaction_status": simulation.get("predicted_transaction_status")},
        "boundary": ("One exact-wallet quote joined to the policy and unsigned simulation; "
                     "no signer, broadcast or approved capital action." if quote_bound else
                     "Quote binding unverified; no signer, broadcast or approved capital action."),
    }
    packet["packet_sha256"] = digest(packet)
    return packet
