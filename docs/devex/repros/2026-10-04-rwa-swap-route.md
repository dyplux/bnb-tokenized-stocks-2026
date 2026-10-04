# RWA quote returns SWAP despite RFQ-only wording

**Observed:** at 2026-10-04 10:53:50 UTC, signed read-only `GET /api/v1/dex/aggregator/quote` for 10 USDC into NVDAB on BNB Chain returned business code 0, one LiquidMesh route and `executionMode=SWAP`. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says equity/RWA tokens always return `RFQ` in the `/quote` response. The general trading introduction allows a broader path, so the exact route rule is unclear.

The [request fixture](../fixtures/2026-10-04-rwa-quote-swap-request.json) records the amount and contracts while omitting the ephemeral wallet and all signed headers. The [raw response fixture](../fixtures/2026-10-04-rwa-quote-swap-raw.json) retains the complete response body, SHA-256 `3490bd8510993795a19591e174a5b4d9512dad736e709639ca37e0fb60e78b4c`. The API echoed 18 USDC decimals and the intended raw amount. This was a quote, not a built or executed transaction.

**Suggested documentation correction:** define which equity/RWA token/provider/vendor combinations may return `SWAP` or `RFQ`, and make the `/quote`, `/swap` and RFQ-order descriptions consistent. Clients should branch on the returned `executionMode` rather than hard-code `RFQ` for every tokenized stock.
