# Venus market API version check

**Checked:** 2026-10-01 23:50 UTC, 2026-10-02 in Lisbon. Public read-only API calls; no account or secret was used.

## Source and observation

The [Venus API documentation](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/services/api.md) says indexed market responses can lag chain state. Its current `stable` market response carries an HTTP `Warning: 299` asking callers to use `accept-version: next`. The documentation says `stable` and `next` may have different schemas and that `next` isn't a permanent schema identifier.

Two `GET https://api.venus.io/markets?chainId=56&limit=100` reads used explicit `accept-version` headers. Both returned HTTP 200. `stable` returned the migration warning and 55 market rows; `next` returned no warning and 51 rows. The `next` top-level response omitted the `tokens` field present in `stable`. The app reads `result`, not `tokens`.

Each response had one NVDAB market and the same Core Pool USDT market. The existing `build_scenario()` completed for 1 NVDAB and a 100 USDT target on both responses with the same nominal capacity. This is an API shape and code-path check, not a personal borrowing or liquidity-safety result. The raw indexed snapshots weren't retained, so these figures aren't publication receipts.

## Change and boundary

The app's `fetch_markets()` now sends `accept-version: next` explicitly. One post-change public request completed the same scenario, with Python syntax and diff checks passing. The app still validates required market fields and fails if a future response removes them. It doesn't yet monitor future `Warning` headers; check the live API before the final demo and remove or revise the header if Venus promotes `next`. On-chain state remains the authority for balances, debt, prices and transaction safety.
