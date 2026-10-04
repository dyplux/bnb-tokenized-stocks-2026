#!/usr/bin/env python3
"""Compare Sunday quote-implied entry price with quote token metadata, without new calls."""

import gzip
import json
import statistics
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.rwa_research import write_json  # noqa: E402


def decimal_field(obj, key):
    value = obj.get(key)
    if value is None:
        raise ValueError("missing %s" % key)
    return Decimal(str(value))


def main():
    source = json.loads((ROOT / "experiments/EXP-RWA-009/weekend_route_coverage_100usdt.json").read_text(encoding="utf-8"))
    rows = []
    for record in source["rows"]:
        if record["route_count"] != 1:
            continue
        digest = record["raw_response_sha256"]
        with gzip.open(ROOT / "data/market_hours/raw" / (digest + ".json.gz"), "rt", encoding="utf-8") as stream:
            payload = json.load(stream)
        quote = payload["data"][0]
        from_token, to_token = quote["fromToken"], quote["toToken"]
        input_tokens = decimal_field(quote, "fromTokenAmount") / (Decimal(10) ** int(from_token["decimal"]))
        output_tokens = decimal_field(quote, "toTokenAmount") / (Decimal(10) ** int(to_token["decimal"]))
        source_usd = decimal_field(from_token, "tokenUnitPrice")
        indicative_usd = decimal_field(to_token, "tokenUnitPrice")
        if min(input_tokens, output_tokens, source_usd, indicative_usd) <= 0:
            raise ValueError("nonpositive price or token amount in %s" % digest)
        implied_usd = input_tokens * source_usd / output_tokens
        deviation = (implied_usd / indicative_usd - 1) * 100
        rows.append({"provider": record["provider"], "ticker": record["ticker"],
                     "contract": record["contract"], "observed_at": record["observed_at"],
                     "origin": "LIVE_QUOTE_DERIVED", "input_usdt": str(input_tokens),
                     "output_token_estimate": str(output_tokens),
                     "quote_source_usdt_usd": str(source_usd),
                     "quote_indicative_token_usd": str(indicative_usd),
                     "quote_implied_entry_usd_per_token": str(implied_usd),
                     "implied_vs_indicative_percent": str(deviation.quantize(Decimal("0.000001"))),
                     "reported_price_impact_percent": quote.get("priceImpactPercent"),
                     "estimated_network_fee_usd": quote.get("tradeFee"),
                     "raw_response_sha256": digest})
    def group(provider):
        values = [float(r["implied_vs_indicative_percent"]) for r in rows if r["provider"] == provider]
        return {"count": len(values), "median_percent": statistics.median(values),
                "min_percent": min(values), "max_percent": max(values),
                "over_one_percent": sum(v > 1 for v in values)}
    result = {"source": str(source.get("last_observed_at")), "scope": "100 USDT Sunday quotes, one route each",
              "formula": "(input_USDT * quote.fromToken.tokenUnitPrice / estimated_output_token) / quote.toToken.tokenUnitPrice - 1",
              "groups": {p: group(p) for p in ("bstock", "ondo")}, "rows": rows,
              "limit": "Both prices come from the same API quote. This isn't an independent stock-reference gap, an issuer-normalized spread, a fill, or an all-in cost. Network fee is an estimate; gas, approvals, eligibility and slippage remain unverified."}
    write_json(ROOT / "experiments/EXP-RWA-009/quote_vs_metadata_100usdt.json", result)
    print(json.dumps(result["groups"]))


if __name__ == "__main__":
    main()
