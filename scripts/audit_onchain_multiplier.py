#!/usr/bin/env python3
"""Read BEP-677 multiplier state at one fixed BSC block for monitored bStocks."""

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.rwa_research import DEVEX, append_jsonl, utc_now, write_json  # noqa: E402

RPC = "https://bsc-dataseed.bnbchain.org"
SELECTORS = {"uiMultiplier": "0xa60bf13d", "newUIMultiplier": "0xdc767007", "effectiveAt": "0x97a4064f"}


def rpc_batch(calls, block, experiment, expected_behavior="fixed-block read-only multiplier values",
              market_context="fixed_block_corporate_action_audit"):
    body = json.dumps(calls, separators=(",", ":")).encode()
    started = time.monotonic()
    status, raw, error = None, b"", None
    try:
        with urlopen(Request(RPC, data=body, headers={"Content-Type": "application/json"}), timeout=15) as response:
            status, raw = response.status, response.read(1_000_001)
    except HTTPError as exc:
        status, raw = exc.code, exc.read(1_000_001)
    except (URLError, TimeoutError, OSError) as exc:
        error = type(exc).__name__
    at = utc_now()
    digest = hashlib.sha256(raw).hexdigest() if raw else None
    try:
        payload = json.loads(raw) if raw and len(raw) <= 1_000_000 else None
    except json.JSONDecodeError:
        payload, error = None, "invalid_json"
    success = status == 200 and isinstance(payload, (dict, list))
    append_jsonl(DEVEX / (at[:10] + ".jsonl"), {
        "timestamp": at, "endpoint": RPC, "method": "POST eth_call JSON-RPC batch",
        "experiment_id": experiment, "expected_behavior": expected_behavior,
        "actual_behavior": "success" if success else "failure",
        "latency_ms": round((time.monotonic() - started) * 1000, 2), "http_status": status,
        "sanitized_request": {"method_count": len(calls), "block": block,
                              "methods": sorted({c["method"] for c in calls})},
        "sanitized_response": {"row_count": len(payload) if isinstance(payload, list) else 1 if isinstance(payload, dict) else 0,
                               "error_count": sum(bool(item.get("error")) for item in payload) if isinstance(payload, list) else bool(payload.get("error")) if isinstance(payload, dict) else None},
        "raw_response_sha256": digest, "schema_mismatch": status == 200 and not success,
        "error": error, "market_context": market_context,
        "secret_scan": "public_rpc_no_auth_headers_or_wallet_key",
    })
    if not success:
        raise RuntimeError("BSC RPC failed: HTTP %s, %s" % (status, error))
    return payload, raw, at, digest


def call(method, params, id_):
    return {"jsonrpc": "2.0", "id": id_, "method": method, "params": params}


def main():
    catalog = json.loads((ROOT / "data/market_hours/catalog_latest.json").read_text(encoding="utf-8"))
    stocks = sorted((r for r in catalog["rows"] if r["provider"] == "bstock" and r["asset_type"] == 1),
                    key=lambda r: (r["ticker"], r["contract"]))
    if len(stocks) != 35:
        raise RuntimeError("expected exactly 35 monitored bStocks in latest catalog")
    head, head_raw, head_at, head_hash = rpc_batch([call("eth_blockNumber", [], 1)], "latest", "EXP-RWA-002/011/ONCHAIN")
    block = head[0]["result"]
    header, header_raw, _, header_hash = rpc_batch([call("eth_getBlockByNumber", [block, False], 2)], block, "EXP-RWA-002/011/ONCHAIN")
    block_timestamp = int(header[0]["result"]["timestamp"], 16)
    replies = {}
    raw_batches = [{"request": [call("eth_blockNumber", [], 1)], "response": head},
                   {"request": [call("eth_getBlockByNumber", [block, False], 2)], "response": header}]
    for offset in range(0, len(stocks), 5):
        batch = stocks[offset:offset + 5]
        calls = []
        for index, stock in enumerate(batch):
            for field, selector in SELECTORS.items():
                identifier = (offset + index) * 3 + list(SELECTORS).index(field) + 10
                calls.append(call("eth_call", [{"to": stock["contract"], "data": selector}, block], identifier))
                replies[identifier] = (stock, field)
        result, raw, at, digest = rpc_batch(calls, block, "EXP-RWA-002/011/ONCHAIN")
        if not isinstance(result, list) or len(result) != len(calls):
            raise RuntimeError("unexpected RPC batch shape")
        raw_batches.append({"request": calls, "response": result, "observed_at": at, "sha256": digest})
    values = {stock["contract"]: {} for stock in stocks}
    for item in raw_batches[2:]:
        for response in item["response"]:
            stock, field = replies[response["id"]]
            try:
                values[stock["contract"]][field] = int(response["result"], 16)
            except (KeyError, TypeError, ValueError):
                values[stock["contract"]][field] = None
    rows = []
    for stock in stocks:
        state = values[stock["contract"]]
        ui = state.get("uiMultiplier")
        nxt = state.get("newUIMultiplier")
        effective = state.get("effectiveAt")
        onchain = Decimal(ui) / Decimal(10**18) if ui is not None else None
        api_ratio = Decimal(str(stock["token_to_share_ratio"]))
        rows.append({"ticker": stock["ticker"], "contract": stock["contract"],
                     "catalog_ratio": str(api_ratio), "catalog_captured_at": catalog["captured_at"],
                     "onchain_ui_multiplier": str(onchain) if onchain is not None else None,
                     "matches_catalog_exactly": onchain == api_ratio if onchain is not None else None,
                     "new_ui_multiplier": str(Decimal(nxt) / Decimal(10**18)) if nxt is not None else None,
                     "effective_at_unix": effective,
                     "has_pending_change": effective > block_timestamp if effective is not None else None,
                     "read_error": any(state.get(field) is None for field in SELECTORS)})
    raw_path = ROOT / "data/external_reference/2026-10-04-bstock-multiplier-rpc-raw.json"
    write_json(raw_path, {"source": RPC, "block": block, "block_timestamp_unix": block_timestamp,
                          "captured_at": head_at, "batches": raw_batches})
    output = {"origin": "LIVE_FIXED_BLOCK", "rpc": RPC, "block": block,
              "block_timestamp": datetime.fromtimestamp(block_timestamp, timezone.utc).isoformat(),
              "catalog_captured_at": catalog["captured_at"], "catalog_sha256": catalog["raw_response_sha256"],
              "raw_fixture": str(raw_path.relative_to(ROOT)), "raw_fixture_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
              "contracts": len(rows), "read_errors": sum(r["read_error"] for r in rows),
              "exact_matches": sum(r["matches_catalog_exactly"] is True for r in rows),
              "pending_changes": sum(r["has_pending_change"] is True for r in rows),
              "rows": rows,
              "limit": "BEP-677 UI multiplier is on-chain display scaling, not proof of backing, holder rights, corporate action dates or future ratios. Catalog and fixed block are close but not atomic."}
    write_json(ROOT / "experiments/EXP-RWA-011/onchain_multiplier_audit.json", output)
    print(json.dumps({k: output[k] for k in ("block", "contracts", "read_errors", "exact_matches", "pending_changes")}))


if __name__ == "__main__":
    main()
