#!/usr/bin/env python3
"""Capture one live policy review and a separate exact-wallet dry run, read-only."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.pre_execution_packet import assemble  # noqa: E402
from app.safety_service import review  # noqa: E402
from scripts.prepare_exact_wallet_simulation import run  # noqa: E402
from scripts.rwa_research import write_json  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("bstock", "ondo"), default="bstock")
    args = parser.parse_args()
    action = {"provider": args.provider, "notional_usdt": "10",
              "max_notional_usdt": "10", "max_price_impact_percent": "0.5"}
    result = assemble(review(action), run(provider=args.provider))
    write_json(ROOT / "data/market_hours" /
               ("pre_execution_packet_" + args.provider + ".json"), result)
    print(json.dumps({"state": result["state"], "reason_codes": result["reason_codes"],
                      "packet_sha256": result["packet_sha256"]}))


if __name__ == "__main__":
    main()
