# bStocks country endpoint: bounded source check

**Checked:** 2026-10-03 UTC. Documentary check only; no eligibility decision or API call.

## What the primary sources say

- The [Binance bStocks FAQ](https://www.binance.com/en/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38) says third-party integrations should enforce geographic restrictions and says a public REST country eligibility endpoint exists. Its integration paragraph links to bStocks contact, but doesn't link the endpoint or state its request and response fields.
- The separate [Binance deposit, withdrawal and conversion FAQ](https://www.binance.com/en/support/faq/detail/f0d41139fadc4790bf9a4c0c7bce2e88) repeats the endpoint claim without a route or schema.
- The [Binance Web3 API documentation bundle](https://web3.binance.com/en/dev-docs/llms-full.txt) publishes a list of regions restricted from the Web3 API. That list describes access to the developer portal and API server. It isn't a bStocks investor eligibility response, and it can't substitute for the issuer's stated endpoint.

## Search result and limit

Targeted searches of the current Binance developer and Web3 documentation for `bStocks`, `country eligibility` and `eligibility` did not yield a documented endpoint URL or response schema on 2026-10-03. This is a bounded negative search, not proof that the endpoint doesn't exist. No route was guessed, called or integrated.

A second bounded search on 2026-10-03 checked the official [Stocks Trading REST market-data reference](https://developers.binance.com/en/docs/catalog/advanced-trading-stocks-trading/api/rest-api/market-data). Its documented market routes are exchange information, tokenized assets and latest quote; none is a country eligibility check. These CEX endpoints require a separate `X-MBX-APIKEY` and cannot be treated as the Binance Web3 credential or as evidence that a BNB Chain wallet may trade bStocks. The two Binance FAQs above still give no country route or schema. This adds one checked surface, but doesn't resolve the integration question.

## Consequence for this build

Keep the current read-only prototype. Before a public trade action is exposed, obtain the exact endpoint, schema, allowed integration use and failure behavior from Binance or the issuer, then check an eligible user's jurisdiction without storing that information in the repository. The FAQs also direct third parties to contact bStocks about integration, so the mentor should confirm whether a separate issuer arrangement is required. Wallet possession or access to the Binance Web3 API cannot establish bStocks eligibility. The [mentor question](mentor-questions.md) asks for the route; no message has been sent.
