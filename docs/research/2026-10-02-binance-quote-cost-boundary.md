# Binance Web3 quote cost boundary

**Checked:** 2026-10-02. **Method:** official documentation review against the [sanitized live quote](2026-10-02-first-live-binance-quote.md). No new signed request or transaction.

| Field or step | Official description | What the live NVDAB read establishes |
|---|---|---|
| `toTokenAmount` | [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api): estimated buy-token amount in smallest units, returned by the vendor | The observed 18-decimal raw output is an estimated USDT amount, not settled proceeds. |
| `tradeFee` | Same reference: estimated network fee in USD, nullable | The observed `0.01800319` is labelled a network-fee estimate. The docs don't establish that subtracting it from `toTokenAmount` gives net USDT, or whether it includes approval. |
| `estimateGasFee` | Same reference: estimated gas in the chain's smallest unit, with example `150000` | The observed value `450000` has no measured transaction gas used or gas price alongside it. Do not label it a paid fee or convert it to USDT. The wording and magnitude leave its precise unit unclear for this route. |
| `feeAmount` and `feeToken` | Same reference: populated for an enabled custom referral fee | Both were null in the observed request, which supplied no custom referral fee. This doesn't establish zero venue, gas or execution costs. |
| `executionMode` | [Trading API introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction): bStocks may return LiquidMesh `SWAP` or PcsXRfq `RFQ`; SWAP follows quote, build swap, sign, broadcast | The NVDAB quote returned LiquidMesh `SWAP`. The [endpoint reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) still says RWA always RFQ. The route mode is observed; its actual transaction path wasn't run. |

**Decision:** keep the main sale card Unquoted and the separate Sale check as a short-lived *estimated output* with review-required mode. No net-proceeds number or sell-versus-borrow recommendation can be calculated from these fields alone. A same-wallet, same-amount holder quote, execution-path clarification and observed costs are needed before changing that claim. The [mentor question](mentor-questions.md) asks specifically about the SWAP path, included fees, approval gas and the `450000` unit; it hasn't been sent.
