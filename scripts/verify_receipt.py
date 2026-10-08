#!/usr/bin/env python3
"""Verify a Praeva receipt offline without claiming authenticity."""

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path


SUPPORTED_POLICY_VERSION = "0.6.0"
SHA256_RE = re.compile(r"[0-9a-f]{64}")
RECEIPT_KEYS = {
    "policy_version", "timestamp", "decision", "reason_codes", "checks",
    "intent", "mandate", "evidence", "receipt_sha256",
}
INTENT_KEYS = {"chain_id", "ticker", "provider", "contract", "notional_usd"}
MANDATE_KEYS = {
    "max_token_price_age_ms", "require_independent_reference",
    "max_reference_age_seconds", "max_notional_usd",
    "max_price_impact_percent", "max_eligibility_age_seconds",
    "require_onchain_multiplier", "max_onchain_multiplier_age_seconds",
}
EVIDENCE_KEYS = {
    "chain_id", "ticker", "provider", "contract", "issuer_verified",
    "eligibility_status", "eligibility_basis", "eligibility_checked_at",
    "token_to_share_ratio", "previous_token_to_share_ratio",
    "corporate_action_verified", "onchain_ui_multiplier",
    "onchain_new_ui_multiplier", "onchain_multiplier_block",
    "onchain_multiplier_block_timestamp", "onchain_multiplier_effective_at",
    "market_status", "market_reason", "market_open_state",
    "token_price_age_ms", "token_price_age_calculation",
    "reference_price_updated_at", "reference_age_seconds",
    "reference_age_status", "token_price_usd", "reported_reference_price_usd",
    "stock_feed_price_usd", "stock_feed_price_asof", "quote_available",
    "quote_identity_match", "quote_execution_mode", "quote_vendor",
    "quote_observed_at", "price_impact_percent", "simulation_passed",
    "source_observed_at", "source_response_sha256",
}


class ReceiptError(ValueError):
    pass


def reject_constant(value):
    raise ReceiptError(f"non-finite number: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReceiptError(f"duplicate key: {key}")
        result[key] = value
    return result


def load_json(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
        return json.loads(text, object_pairs_hook=unique_object,
                          parse_constant=reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, ReceiptError) as exc:
        raise ReceiptError(str(exc)) from exc


def extract_receipt(document):
    if not isinstance(document, dict):
        raise ReceiptError("top-level JSON must be an object")
    receipt = document.get("receipt", document)
    if not isinstance(receipt, dict):
        raise ReceiptError("receipt must be an object")
    missing = RECEIPT_KEYS - receipt.keys()
    if missing:
        raise ReceiptError("receipt missing required fields: " + ", ".join(sorted(missing)))
    if not isinstance(receipt["decision"], str) or receipt["decision"] not in {"ALLOW", "DENY", "NEED_HUMAN"}:
        raise ReceiptError("decision must be ALLOW, DENY, or NEED_HUMAN")
    if not isinstance(receipt["policy_version"], str):
        raise ReceiptError("policy_version must be a string")
    if not isinstance(receipt["timestamp"], str):
        raise ReceiptError("timestamp must be a string")
    if not isinstance(receipt["reason_codes"], list) or not all(
            isinstance(value, str) for value in receipt["reason_codes"]):
        raise ReceiptError("reason_codes must be an array of strings")
    if not isinstance(receipt["checks"], dict) or not all(
            isinstance(key, str) and isinstance(value, str) and value in {"DENY", "NEED_HUMAN"}
            for key, value in receipt["checks"].items()):
        raise ReceiptError("checks must map strings to DENY or NEED_HUMAN")
    if not isinstance(receipt["receipt_sha256"], str) or not SHA256_RE.fullmatch(
            receipt["receipt_sha256"]):
        raise ReceiptError("receipt_sha256 must be 64 lowercase hexadecimal characters")
    for key in ("intent", "mandate", "evidence"):
        if not isinstance(receipt[key], dict):
            raise ReceiptError(f"{key} must be an object")
    parse_timestamp(receipt["timestamp"])
    return receipt


def canonical_sha256(receipt):
    body = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True, allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def replay_context_complete(receipt):
    return (INTENT_KEYS <= receipt["intent"].keys()
            and MANDATE_KEYS <= receipt["mandate"].keys()
            and EVIDENCE_KEYS <= receipt["evidence"].keys())


def parse_timestamp(value):
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReceiptError("timestamp must be ISO 8601") from exc
    if timestamp.tzinfo is None:
        raise ReceiptError("timestamp must include a timezone")
    return timestamp


def load_kernel():
    path = Path(__file__).resolve().parents[1] / "app" / "rwa_policy.py"
    spec = importlib.util.spec_from_file_location("praeva_rwa_policy", path)
    if spec is None or spec.loader is None:
        raise ReceiptError("policy kernel couldn't be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(path, expected_sha256=None):
    receipt = extract_receipt(load_json(path))
    calculated = canonical_sha256(receipt)
    recorded = receipt["receipt_sha256"]
    expected = expected_sha256.lower() if expected_sha256 else None
    integrity_match = calculated == recorded and (expected is None or calculated == expected)
    result = {
        "integrity": "INTEGRITY_MATCH" if integrity_match else "INTEGRITY_MISMATCH",
        "replay": "REPLAY_UNAVAILABLE",
        "policy": "POLICY_VERSION_SUPPORTED",
        "calculated_sha256": calculated,
        "recorded_sha256": recorded,
        "expected_sha256": expected,
        "integrity_scope": "canonical receipt consistency, not authenticity",
        "replay_scope": "same-kernel replay at the saved timestamp",
    }
    if receipt["policy_version"] != SUPPORTED_POLICY_VERSION:
        result["policy"] = "POLICY_VERSION_UNSUPPORTED"
        return result, 4
    if not replay_context_complete(receipt):
        return result, 3 if not integrity_match else 0
    kernel = load_kernel()
    if kernel.VERSION != receipt["policy_version"]:
        result["policy"] = "POLICY_VERSION_UNSUPPORTED"
        return result, 4
    replayed = kernel.evaluate(receipt["intent"], receipt["evidence"],
                               receipt["mandate"], now=parse_timestamp(receipt["timestamp"]))
    result["replay"] = "REPLAY_MATCH" if replayed == receipt else "REPLAY_MISMATCH"
    return result, 0 if integrity_match and result["replay"] == "REPLAY_MATCH" else 3


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verify canonical receipt integrity and replay policy 0.6.0 offline.")
    parser.add_argument("receipt", help="receipt JSON or wrapper containing a receipt")
    parser.add_argument("--expected-sha256", metavar="HEX",
                        help="externally obtained expected canonical SHA-256")
    args = parser.parse_args(argv)
    if args.expected_sha256 and not SHA256_RE.fullmatch(args.expected_sha256.lower()):
        parser.error("--expected-sha256 must be 64 hexadecimal characters")
    try:
        result, exit_code = verify(args.receipt, args.expected_sha256)
    except (ReceiptError, TypeError, ValueError, AttributeError, OverflowError, RecursionError) as exc:
        print(json.dumps({"status": "INVALID_RECEIPT", "error": str(exc)},
                         sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
