"""Deterministic, read-only RWA execution policy. Never signs a transaction."""

import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

VERSION = "0.3.0"


def number(value):
    try:
        candidate = Decimal(str(value))
        return candidate if candidate.is_finite() else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def reference_freshness_guard(evidence, mandate):
    """Return a reason and severity for an independently timed reference.

    A token-price timestamp never satisfies this guard. Callers can explicitly
    waive the independent reference when their mandate doesn't use one.
    """
    if mandate.get("require_independent_reference") is False:
        return None
    if evidence.get("reference_price_updated_at") is None or evidence.get("reference_age_status") != "OBSERVED":
        return "INDEPENDENT_REFERENCE_TIME_UNKNOWN", "NEED_HUMAN"
    age = number(evidence.get("reference_age_seconds"))
    limit = number(mandate.get("max_reference_age_seconds"))
    if age is None or age < 0 or limit is None or limit <= 0:
        return "INDEPENDENT_REFERENCE_AGE_UNKNOWN", "NEED_HUMAN"
    if age > limit:
        return "INDEPENDENT_REFERENCE_STALE", "DENY"
    return None


def eligibility_guard(evidence, mandate, now):
    """Require a dated, caller-verified access decision for this intended user.

    A quote response and a country-level indication don't verify a wallet or person.
    The caller must validate the issuer's access evidence before setting ELIGIBLE.
    """
    status = evidence.get("eligibility_status")
    if status == "INELIGIBLE":
        return "USER_INELIGIBLE", "DENY"
    if status != "ELIGIBLE":
        return "USER_ELIGIBILITY_UNKNOWN", "NEED_HUMAN"
    basis = evidence.get("eligibility_basis")
    checked_at = evidence.get("eligibility_checked_at")
    max_age = number(mandate.get("max_eligibility_age_seconds"))
    if not isinstance(basis, str) or not basis.strip() or not isinstance(checked_at, str) or max_age is None or max_age <= 0:
        return "USER_ELIGIBILITY_PROVENANCE_UNKNOWN", "NEED_HUMAN"
    try:
        checked = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
        age = (now - checked).total_seconds() if checked.tzinfo is not None else None
    except (ValueError, TypeError):
        age = None
    if age is None or age < 0:
        return "USER_ELIGIBILITY_PROVENANCE_UNKNOWN", "NEED_HUMAN"
    if Decimal(str(age)) > max_age:
        return "USER_ELIGIBILITY_STALE", "NEED_HUMAN"
    return None


def evaluate(intent, evidence, mandate, now=None):
    """Return a fail-closed decision for one planned BSC spot action.

    Required evidence is intentionally strict. Missing values produce NEED_HUMAN.
    ALLOW means policy checks passed, not that a trade has executed or is profitable.
    """
    now = now or datetime.now(timezone.utc)
    reasons, checks = [], {}

    def deny(code):
        reasons.append(code)
        checks[code] = "DENY"

    def uncertain(code):
        reasons.append(code)
        checks[code] = "NEED_HUMAN"

    if str(intent.get("chain_id")) != "56" or str(evidence.get("chain_id")) != "56":
        deny("CHAIN_MISMATCH")
    if not intent.get("ticker") or intent.get("ticker") != evidence.get("ticker"):
        deny("ASSET_IDENTITY_MISMATCH")
    if intent.get("provider") != evidence.get("provider") or intent.get("contract", "").lower() != evidence.get("contract", "").lower():
        deny("TOKEN_IDENTITY_MISMATCH")
    if evidence.get("issuer_verified") is not True:
        uncertain("ISSUER_UNVERIFIED")
    eligibility_result = eligibility_guard(evidence, mandate, now)
    if eligibility_result is not None:
        code, severity = eligibility_result
        (deny if severity == "DENY" else uncertain)(code)

    ratio = number(evidence.get("token_to_share_ratio"))
    previous = number(evidence.get("previous_token_to_share_ratio"))
    if ratio is None or ratio <= 0:
        uncertain("SHARE_RATIO_UNKNOWN")
    elif previous is not None and ratio != previous:
        if evidence.get("corporate_action_verified") is not True:
            deny("UNVERIFIED_RATIO_CHANGE")
        else:
            uncertain("CORPORATE_ACTION_REVIEW")
    if evidence.get("market_status") in ("pause", "halted") or evidence.get("market_reason") == "ASSET_PAUSED":
        deny("ASSET_PAUSED")
    elif evidence.get("market_status") in ("closed", "offhours", "overnight"):
        uncertain("UNDERLYING_MARKET_NOT_REGULAR")
    elif evidence.get("market_status") != "regular":
        uncertain("MARKET_STATE_UNKNOWN")

    price_age = evidence.get("token_price_age_ms")
    max_age = mandate.get("max_token_price_age_ms")
    if evidence.get("token_price_age_calculation") != "observed_at_minus_tokenPriceUpdatedAt":
        uncertain("TOKEN_PRICE_AGE_PROVENANCE_UNKNOWN")
    if not isinstance(price_age, int) or price_age < 0 or not isinstance(max_age, int) or max_age <= 0:
        uncertain("TOKEN_PRICE_AGE_UNKNOWN")
    elif price_age > max_age:
        deny("TOKEN_PRICE_STALE")
    reference_result = reference_freshness_guard(evidence, mandate)
    if reference_result is not None:
        code, severity = reference_result
        (deny if severity == "DENY" else uncertain)(code)

    requested = number(intent.get("notional_usd"))
    limit = number(mandate.get("max_notional_usd"))
    if requested is None or requested <= 0 or limit is None or limit <= 0:
        uncertain("MANDATE_AMOUNT_UNKNOWN")
    elif requested > limit:
        deny("MANDATE_LIMIT_EXCEEDED")
    impact = number(evidence.get("price_impact_percent"))
    max_impact = number(mandate.get("max_price_impact_percent"))
    if evidence.get("quote_available") is False:
        deny("NO_EXECUTABLE_QUOTE")
    elif evidence.get("quote_available") is not True:
        uncertain("QUOTE_UNVERIFIED")
    if impact is None or max_impact is None or max_impact <= 0:
        uncertain("PRICE_IMPACT_UNKNOWN")
    elif abs(impact) > max_impact:
        deny("PRICE_IMPACT_LIMIT_EXCEEDED")
    if evidence.get("simulation_passed") is not True:
        uncertain("SIMULATION_UNVERIFIED")

    decision = "DENY" if "DENY" in checks.values() else ("NEED_HUMAN" if reasons else "ALLOW")
    receipt = {
        "policy_version": VERSION, "timestamp": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "decision": decision, "reason_codes": sorted(set(reasons)), "checks": checks,
        "intent": {k: intent.get(k) for k in ("chain_id", "ticker", "provider", "contract", "notional_usd")},
        "mandate": {k: mandate.get(k) for k in (
            "max_token_price_age_ms", "require_independent_reference", "max_reference_age_seconds",
            "max_notional_usd", "max_price_impact_percent", "max_eligibility_age_seconds")},
        "evidence": {k: evidence.get(k) for k in (
            "chain_id", "ticker", "provider", "contract", "issuer_verified",
            "eligibility_status", "eligibility_basis", "eligibility_checked_at", "token_to_share_ratio",
            "previous_token_to_share_ratio", "corporate_action_verified", "market_status", "market_reason",
            "token_price_age_ms", "token_price_age_calculation", "reference_price_updated_at",
            "reference_age_seconds", "reference_age_status", "quote_available",
            "price_impact_percent", "simulation_passed", "source_response_sha256")},
    }
    encoded = json.dumps(receipt, sort_keys=True, separators=(",", ":"), default=str).encode()
    receipt["receipt_sha256"] = hashlib.sha256(encoded).hexdigest()
    return receipt
