# Decision log

## D-001: keep the BNB project separate from Bell

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted

The new project has its own repository, data and future deployment. Bell remains the CoinMarketCap hackathon entry. The local repository is on the external SSD because the primary drive had about 12 GiB free, while the SSD had about 345 GiB free at the 2026-10-01 check. The repository stays private during research. The [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks), checked 2026-10-01, requires a public repository at submission.

## D-002: keep product selection open until a quote and incumbent comparison

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional

The first two research passes favor a pre-trade check of issuer, contract, market state and quote. [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) already documents ticker resolution and quote confirmation; [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) already has a stock terminal. Both were checked 2026-10-01. The specific user benefit of another layer has not been measured. A live, same-time quote and task comparison can change or reject this direction.

No implementation decision is recorded here. The eventual product choice must name a user, a task, its evidence, the existing workaround and the result that would disprove the proposed advantage.

## D-003: test H1, don't build yet

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research priority

The [weighted scorecard](../research/idea-scorecard.md) orders H1 representation/quote receipt ahead of H2 temporal availability and H3 error recovery. A separate critical review objected that H1 may duplicate PancakeSwap and Agentic Wallet, and that no live Binance RFQ or human problem has been observed. The objection is retained. Test NVDA in bStocks and Ondo at fixed amounts and times; reject H1 if the extra receipt doesn't change a decision or prevent an identifiable error. xStocks is out of the first slice because documented RWA Data coverage is unclear.

The [RWA Data API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data), checked 2026-10-01, defines `referencePrice` as a conversion from on-chain token price. It must not be presented as an independent equity quote. [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) and [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) are the incumbent tasks to compare.

The one-line [hacker application draft](../submission/form-answer.md) is a mentor-routing hypothesis, not final product approval. Agent Studio and B402/x402 are deferred until a concrete user task requires them. No dissent was overridden by the score.

## D-004: founder challenges H1's consumer value and Bell overlap

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** H1 and application wording under review

The founder asked why a common user would need a “pre-trade decision receipt” and noted its similarity to Bell. The concern is material. Bell already checks whether tokenized asset representations are comparable; adding a live RFQ and moving the check closer to purchase may still leave the same product idea with another data field. A common buyer wants a clear outcome for a chosen amount, with a safe next action. No observed task shows that a separate receipt reduces time, prevents a mistake or enables a purchase that an existing flow blocks.

The [PancakeSwap stock terminal](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) already presents issuer options and a trade path. [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) documents ticker resolution, quote and confirmation. These published flows strengthen the founder's objection; they don't prove the live UX is complete. The scorecard's 57/100 was a research ordering and didn't measure common-user value.

Hold the [application draft](../submission/form-answer.md). H1 may continue as a falsification test, but it is no longer a recommended standalone consumer product. Resume product selection by observing one ordinary user's actual purchase task and the same task in incumbent flows. If the only added output is a longer explanation, reject H1. Don't rename the idea or add Agent Studio to disguise the overlap.
