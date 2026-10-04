#!/usr/bin/env python3
"""Capture one exact-wallet policy quote, unsigned build and simulation."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.pre_execution_packet import assemble  # noqa: E402
from app.safety_service import review  # noqa: E402
from scripts.prepare_exact_wallet_simulation import public_demo_address, run  # noqa: E402
from scripts.rwa_research import write_json  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("bstock", "ondo"), default="bstock")
    args = parser.parse_args()
    action = {"provider": args.provider, "notional_usdt": "10",
              "max_notional_usdt": "10", "max_price_impact_percent": "0.5"}
    wallet = public_demo_address()
    policy, route_context = review(action, quote_wallet=wallet, return_route_context=True)
    trial = run(provider=args.provider, wallet=wallet, route_context=route_context)
    result = assemble(policy, trial)
    write_json(ROOT / "data/market_hours" /
               ("pre_execution_packet_" + args.provider + ".json"), result)
    print(json.dumps({"state": result["state"], "reason_codes": result["reason_codes"],
                      "packet_sha256": result["packet_sha256"]}))


if __name__ == "__main__":
    main()
