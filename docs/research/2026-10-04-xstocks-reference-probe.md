# xStocks public price source: documented, response unavailable here

**Checked:** 2026-10-04 17:21 to 17:24 UTC. **Question:** can an independent source provide a stock-reference price with its own as-of timestamp for the NVDA safety review?

The [official xStocks developer guide](https://docs.xstocks.fi/developers) says public `GET /public/assets/{symbol}/price-data` can return prices sourced from cached on-chain providers and Nasdaq or Blue Ocean. It does not, by that statement alone, guarantee a separate source timestamp or real-time access in this environment. The [API changelog](https://docs.xstocks.fi/changelog) identifies the v2 public endpoint.

The bounded [probe](../../scripts/probe_xstocks_price_data.py) attempted `NVDAx` and `AAPLx` at `api.xstocks.fi` without authentication or wallet input. Both requests timed out after 15 seconds, with no HTTP status or response body. A separate six-second HEAD request to `api.xstocks.fi` and `api.backed.fi` also timed out. Both attempted reads are in the sanitized DevEx log with exact UTC time and error type; there is no fixture or observed price to interpret. No endpoint was retried repeatedly.

The BNB Chain AAPLx and NVDAx contracts in our signed catalog also returned no Binance Web3 route for the tested amounts. A 17:18 UTC [DEX Screener token-pairs query](https://docs.dexscreener.com/api/reference) returned zero indexed BSC pairs for each exact contract. An empty index response doesn't prove the absence of all liquidity.

**Decision:** `reference_price_updated_at=null`, `reference_age_seconds=null`, `reference_age_status=UNKNOWN` stay unchanged for the bStock and Ondo review. A price from a different issuer must also be checked for underlying security, share ratio, source semantics and licensing before it can serve as an independent benchmark. Retry the documented public endpoint only if access changes or a mentor supplies a reliable path. This probe neither clears a trade nor changes the frozen Monday experiment.
