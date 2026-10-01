# Binance RWA reference-price source audit

**Checked:** 2026-10-01. **Method:** read official documentation only; no authenticated request or live price was collected.

## What the sources actually say

| Source | Published statement or example | Limit |
|---|---|---|
| [RWA Data API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) | The price endpoint says it returns an on-chain price and an underlying reference price. The `underlying-market` example repeats `marketData.referencePrice`. | It doesn't identify an upstream exchange or vendor, quote timestamp, update cadence, rights or licensing for the reference. The response `timestamp` is a server response time, not an explicitly documented underlying quote time. |
| [Wallet Skills guide in the official docs bundle](https://web3.binance.com/en/dev-docs/llms-full.txt) | Its Ondo section says `referencePrice = tokenPrice / sharesMultiplier`. | If the formula describes the RWA API field, it isn't an independent price. The guide doesn't explicitly reconcile its formula with the RWA endpoint example. |
| RWA API's SEDGon example | `tokenPrice=61.89`, `tokenToShareRatio=1.003701`, `referencePrice=61.746364`. | `61.89 / 1.003701 = 61.6617897`, which differs from the displayed reference by `0.0845743` or about `0.137%` of the displayed reference. An illustrative example may combine rounded or asynchronous values; it cannot settle provenance. |

## Decision consequence

The earlier claim that the RWA API **defines** `referencePrice` as derived from token price was too strong. Independence is also unproved. The safe product treatment is **source unknown**: never label this field a live NYSE/Nasdaq price or advertise a discount, premium or arbitrage from it. A conventional-equity comparison needs an independently documented source, matched share units, a source quote time, and a same-time executable BNB Chain quote. The Web3 Trading API documentation also doesn't establish the units or inclusions of quote fee fields in the available summary, so an all-in execution-cost promise awaits a live schema and payload review.

**Question for Binance mentor:** For `GET /api/v1/dex/market/rwa/price` and `/underlying-market`, what source and as-of timestamp populate `referencePrice` for bStocks and Ondo? Is it computed from `tokenPrice` and `tokenToShareRatio`, or independently sourced from a conventional-equity market? How may third-party apps display it?

This is a documentation question. It isn't a complaint about a measured live API response.
