#!/usr/bin/env python3
"""Check whether Sunday's two no-route results depend on the requested USDT size."""

import json
import secrets
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.server import USDT  # noqa: E402
from scripts.rwa_research import Api, QUOTE, write_json  # noqa: E402


def main():
    coverage = json.loads((ROOT / "experiments/EXP-RWA-009/weekend_route_coverage_100usdt.json").read_text())
    missing = [row for row in coverage["rows"] if row["route_count"] == 0]
    if {(row["provider"], row["ticker"]) for row in missing} != {("bstock", "AAOI"), ("ondo", "MSTR")}:
        raise RuntimeError("the frozen 100 USDT no-route set changed")
    api = Api()
    wallet = "0x" + secrets.token_hex(20)
    output = ROOT / "experiments/EXP-RWA-009/weekend_missing_route_size_probe.json"
    rows = json.loads(output.read_text())["rows"] if output.exists() else []
    seen = {(row["contract"], row["input_usdt"]) for row in rows}
    for target in missing:
        for usdt in (10, 100, 1000):
            if (target["contract"], usdt) in seen:
                continue
            payload, at, digest = api.get(
                QUOTE, [("binanceChainId", "56"), ("fromTokenAddress", USDT),
                        ("toTokenAddress", target["contract"]), ("amount", str(usdt * 10**18)),
                        ("userWalletAddress", wallet)],
                "EXP-RWA-009/MISSING-SIZE", "read-only quote for a previously unquoted stock token",
                {"market": "weekend", "ticker": target["ticker"],
                 "provider": target["provider"], "task": "buy_%s_usdt" % usdt},
                allow_error=True,
            )
            routes = payload.get("data") if isinstance(payload.get("data"), list) else []
            rows.append({"observed_at": at, "origin": "LIVE", "provider": target["provider"],
                         "ticker": target["ticker"], "contract": target["contract"],
                         "input_usdt": usdt, "business_code": payload.get("code"),
                         "business_message": payload.get("msg"), "route_count": len(routes),
                         "execution_modes": [r.get("executionMode") for r in routes if isinstance(r, dict)],
                         "raw_response_sha256": digest})
            seen.add((target["contract"], usdt))
            write_json(output, {"source_100_usdt_probe": "weekend_route_coverage_100usdt.json",
                                "wallet": "ephemeral_unfunded_not_stored", "rows": rows,
                                "limit": "Sequential indicative quotes, no user eligibility, transaction build, simulation, fill or final cost."})
            time.sleep(0.7)
    print(json.dumps({"requests": len(rows), "results": [
        {"provider": row["provider"], "ticker": row["ticker"], "input_usdt": row["input_usdt"],
         "business_code": row["business_code"], "route_count": row["route_count"]}
        for row in rows]}))


if __name__ == "__main__":
    main()
