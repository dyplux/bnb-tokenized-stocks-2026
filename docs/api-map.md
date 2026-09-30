# Binance API map, documentary stage

**Checked:** 2026-10-01. The endpoints and field descriptions below come from official documentation. No authenticated request, live response, quote, order or transaction has been observed by this new project.

| Surface | Documented use for H1 | Known constraint | Next observation |
|---|---|---|---|
| [RWA Data API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) | Search tokenized stocks, get underlying profile, price and underlying-market context. | Documentation lists `platformId` values `ondo` and `bstock`. Token data, ratios and timestamps need live validation. | Probe one NVDA token per supported platform and record redacted fields and latency. |
| `referencePrice` in RWA Data | Per-share equivalent converted from token's on-chain price. | It is **not** an independent conventional equity quote. Subtracting it from `tokenPrice` doesn't establish a discount or arbitrage. | If a comparison requires a TradFi benchmark, find a licensed independent source and reconcile unit and time. |
| [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) | Request a spot RFQ quote for a fixed token and amount. | Equity/RWA execution is documented as RFQ. Quote availability, fields, limits and expiry remain unknown. Order submission requires EIP-712 signing. | Request one quote without signing or submitting an order, if the account scope permits. |
| [Transaction API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/transaction-api) | Possible transaction simulation. | `evmTx` simulation has not been shown to simulate the same RFQ operation. | Check compatibility before claiming any simulation in the product. |
| [API authentication](https://web3.binance.com/en/dev-docs/authentication) | Signed server-side calls with account credentials. | A no-wallet-signature demo still needs HMAC API authentication. | Verify least-permission scope and quota privately; never put keys or signed headers in repo or logs. |
| [Agentic Wallet stock flow](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) | Incumbent baseline and possible optional integration. | Already resolves ticker and documents quote, confirmation and tracking. | Observe same task before adding any agent interface. |
| [BNB Agent Studio](https://www.bnbchain.org/en/bnb-agent-studio) | Optional persistent agent runtime or identity if it materially improves the task. | Special prize alone does not establish user value; no agent or interoperation observed. | Defer until a task needs persistence or an agent identity. |

The initial research test can end at a quote and dated decision receipt. It must not imply execution, backing certification, independent exchange-price comparison or profitability. Record real onboarding, errors, latency and field availability contemporaneously for the mandatory Developer Experience Report.
