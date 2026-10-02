# Synthetic Binance quote-flow QA

**Checked:** 2026-10-02. **Scope:** local in-memory tests and current documentation. No live Binance Web3 API request, credential, wallet or trade was used.

The [authentication guide](https://web3.binance.com/en/dev-docs/authentication) still requires a signed request path containing `/build`. The [RWA search reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) still documents `keyword`, `platformId`, ticker, chain, contract and asset type. The [aggregated quote reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) still documents raw integer token amounts, wallet address for RFQ routes, token metadata and per-route output. These pages were rechecked on 2 October. They don't prove the runtime response for NVDAB.

The new [synthetic tests](../../tests/test_binance_quote_flow.py) replace the signed HTTP helper and BNB RPC with in-memory replies. An exact NVDA/bstock/NVDAB identity leads to one RFQ route; the app response contains the observed vendor and raw amounts but strips the synthetic `quoteId`. A wrong contract blocks the quote and RPC calls. A route whose input amount differs from the requested amount is rejected rather than displayed. All three new cases passed as part of 14 local tests.

These fixtures are invented solely to exercise code paths. No Binance response, fee, spread, latency, quote availability or successful authentication is inferred from them. The first permitted signed RWA search and quote remain the release gate in [the quote plan](../product/binance-quote-gate.md).
