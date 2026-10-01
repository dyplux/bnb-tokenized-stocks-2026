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

## D-005: investigate a blocked exit before selecting a product

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** research priority, no build approval

The [dated brainstorm](../research/2026-10-01-product-brainstorm.md) found public hackathon entrants covering issuer comparison and routing ([PARALLAX](https://github.com/rishu4436/parallax), [OneTicker](https://github.com/JemIIahh/oneticker)), consumer buying and selling ([yostocks](https://github.com/yostocks-protocol/yostocks), [Portir](https://github.com/yeheskieltame/portir)), and post-hold/collateral tasks ([Steward](https://github.com/zkasuran/steward-bnb), Portir). Their READMEs establish public claims and some source code, not adoption or independently reproduced outcomes. Another pre-trade receipt is rejected as a standalone direction.

[Ondo's own terms](https://ondo.finance/ondo-stocks) distinguish owning a secondary-market token from eligibility to redeem directly. Its normal direct redemption and secondary trading have different hours and conditions. [yostocks's DX log](https://github.com/yostocks-protocol/yostocks/blob/main/DX_LOG.md) reports an after-hours sell refusal even when a buy quote succeeded, but this has not been reproduced by us. A holder asking whether they can exit a specific position today is a narrower possible job than choosing among wrappers. Research it first. The core dissent is that Ondo, wallets and yostocks may already give the correct next action. A quote failure may also be too rare to warrant an app.

Reject the exit direction if a same-task comparison shows that an incumbent already identifies the cause and action, or if Binance API status and sell quotes cannot support a safe diagnosis. No application answer or build is approved. Keep Agent Studio optional; the extra prize alone isn't a product reason.

## D-006: make the closed-market interval the product research priority

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research priority; supersedes D-005's priority

The founder rejected blocked-exit recovery as too remote from the event's opening problem. The [official brief](https://www.bnbchain.org/en/hackathons/tokenized-stocks) asks for useful actions while tokenized stocks trade and the regular US cash market is closed. The [off-hours reset](../research/2026-10-01-off-hours-reset.md) compares three related jobs. Generic weekend monitors and limit-at-reference orders already have public entrants. The first research test is a public company event after the close, linked to a specific tokenized stock, an amount-specific Binance Web3 API spot quote and a capped user decision.

This is a correction to research direction, not evidence of user demand or implementation approval. A cited filing may not be the first public release; a route may be unavailable outside cash hours; the RWA `referencePrice` is not an independent traditional share quote. The product must work honestly through those states. A source summary or a generic quote is insufficient. No autonomous investment decision is authorized. D-005 remains as a documented rejected research priority and may become an error state inside another product if observed.
