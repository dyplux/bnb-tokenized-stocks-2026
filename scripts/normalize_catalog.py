#!/usr/bin/env python3
"""Group catalog representations without claiming legal or economic equivalence."""

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/normalized/rwa_catalog.json"
SECURITIES = ROOT / "data/normalized/canonical_securities.json"
REPRESENTATIONS = ROOT / "data/normalized/provider_representations.json"


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    representations = []
    for row in source["rows"]:
        ticker = str(row["ticker"]).upper().strip()
        asset_type = row.get("asset_type")
        key = f"{ticker}:TYPE-{asset_type if asset_type is not None else 'UNKNOWN'}"
        representation = {**row, "canonical_security_key": key,
                          "identity_status": "PROVISIONAL_TICKER_AND_ASSET_TYPE",
                          "economic_equivalence_verified": False,
                          "provider_identity_status": "PLATFORM_ID_NOT_LEGAL_ISSUER"}
        representations.append(representation)
        grouped[key].append(representation)
    securities = []
    for key, items in sorted(grouped.items()):
        names = sorted({x["underlying_name"] for x in items if x.get("underlying_name")})
        securities.append({"canonical_security_key": key, "ticker": items[0]["ticker"],
                           "asset_type": items[0].get("asset_type"),
                           "underlying_name_candidate": names[0] if len(names) == 1 else None,
                           "name_conflict": len(names) > 1,
                           "identity_status": "PROVISIONAL_TICKER_AND_ASSET_TYPE",
                           "isin_or_legal_identifier": None,
                           "economic_equivalence_verified": False,
                           "providers": sorted({x["provider"] for x in items}),
                           "representation_contracts": sorted(x["contract"] for x in items)})
    common = {"captured_at": source["captured_at"], "source_sha256": source["raw_response_sha256"],
              "method": "ticker plus asset type groups candidates only; no ISIN, redemption or rights match"}
    save(SECURITIES, {**common, "rows": securities})
    save(REPRESENTATIONS, {**common, "rows": representations})
    print(json.dumps({"canonical_candidates": len(securities), "representations": len(representations),
                      "cross_provider_candidates": sum(len(x["providers"]) > 1 for x in securities),
                      "name_conflicts": sum(x["name_conflict"] for x in securities)}))


if __name__ == "__main__":
    main()
