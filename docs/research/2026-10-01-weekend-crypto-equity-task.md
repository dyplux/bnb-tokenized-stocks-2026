# Weekend crypto-to-equity task

**Checked:** 2026-10-01 UTC
**Decision:** a narrower, provisional research priority; no product or trading edge approved

## Why the earlier filing trigger is weak on weekends

The [SEC says EDGAR processes filings Monday to Friday, 06:00 to 22:00 New York time](https://www.sec.gov/submit-filings/filer-support-resources/how-do-i-guides/understand-edgar-its-three-websites). It is closed on Saturdays and Sundays. A primary SEC filing therefore cannot be the normal fresh trigger during the Friday 20:00 to Sunday 20:00 ET interval where [Robinhood says its eligible stock market is shut](https://robinhood.com/us/en/support/articles/investing-on-weekends/). A company can issue a press release or another event on a weekend, but no frequency or reliable feed has been measured. The dated Tesla 8-K remains a weekday source-pipeline replay, not evidence for a weekend product.

## A more frequent observable trigger

[Strategy describes MSTR as amplified Bitcoin exposure](https://www.strategy.com/strategy), while the [Binance public bStock list](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3), read at 11:55 UTC, lists BNB Chain `MSTRB` at `0xe87afb3076aeb0f9b14e368de8145ae6a2826a14` and `COINB` at `0x585bde7c54abb5ccd7791f923d6c2187635f3952`. Its public dynamic surface returned `openState=true` and `reasonCode=TRADING` for both at 11:55 UTC. It returned no stock cash-market price. These website responses do not establish a wallet-size executable Web3 quote.

The possible user task is narrow: an eligible person with BNB Chain stablecoins sees a large Bitcoin move after their stock broker closes and wants to change exposure to the exact tokenized Strategy share before the next stock session. The app would show what the token has already priced, the current BNB Chain quote for that person's amount, total execution cost and a user-set cap. The action could be buy, reduce or wait. A crypto holder who only wants Bitcoin can already trade Bitcoin around the clock; this task is for someone who deliberately wants the separate Strategy equity exposure. We have not observed that user.

## Ten-weekend market observation

The reproducible [script](measure-weekend-spot-pairs.py) queried the [Binance Spot public hourly candle API](https://developers.binance.com/en/docs/products/spot/rest-api) at `data-api.binance.vision` for `BTCUSDT`, `MSTRBUSDT` and `COINBUSDT`. The [CSV](2026-10-01-weekend-spot-pairs.csv) covers ten Friday 20:00 ET to Sunday 20:00 ET windows from 2026-07-24 through 2026-09-27. A return uses the first hourly open at each boundary. The 48 hourly quote-volume fields are summed for each weekend. All three symbols have all ten boundaries and hours.

| Spot observation across ten weekends | MSTRB | COINB |
|---|---:|---:|
| Same return direction as BTC | 8/10 | 8/10 |
| Pearson correlation of 48-hour returns with BTC | 0.883 | 0.900 |
| Simple slope of token weekend return on BTC weekend return | 1.821 | 1.375 |
| Median absolute token weekend return | 1.551% | 0.503% |
| Median 48-hour Spot quote volume | 5.65m USDT | 0.44m USDT |

BTC's median absolute 48-hour return in these ten windows was 0.470%. The simple slopes describe this sample and are **not** forecast coefficients. These are centralized Binance Spot prices and volumes. They say nothing about the same user's BNB Chain RFQ, slippage, fees, gas, exit, access or net PnL. A ten-weekend correlation also cannot show which market moved first. The two sign disagreements for each token are counterexamples to a deterministic BTC trigger.

Using only the hourly opening prices in each window, BTC moved at least 1% away from its Friday 20:00 ET starting price in six of ten weekends, at least 2% in one, and never 3% or 5%. This is a small historical sample; the threshold counts make a product that waits for a dramatic weekend BTC shock look infrequent. An ordinary 1% trigger may occur more often, but no evidence says acting on it makes money after costs.

Across 480 paired hourly returns, the same-hour correlation was 0.815 for BTC/MSTRB and 0.755 for BTC/COINB. The correlation between BTC's return in one hour and the token's return in the **next** hour was only 0.074 for MSTRB and 0.055 for COINB; the reverse lead values were 0.010 and 0.026. This simple aggregate check finds no compelling one-hour BTC lead for the tokens in this sample. It does not test minute-level lead, non-linear strategies or net returns. A BTC-lag alpha story needs an out-of-sample strategy and executable BNB Chain costs before it can be claimed.

At 11:58 UTC, the [DEX Screener token-pair API](https://docs.dexscreener.com/api/reference) returned one indexed PancakeSwap BNB Chain pair per contract: MSTRB/USDT at about US$366,468 reported pool liquidity and US$308,372 24-hour volume, COINB/USDT at about US$2,793 and US$4,932 respectively. This is a third-party pool index, not complete route liquidity or an executable quote. The large difference makes MSTRB a better first amount-specific route test than COINB. No live trade was made.

## Product boundary and falsification

A BTC-triggered buy/sell rule by itself overlaps the [Binance Agentic Wallet's published ongoing strategy examples](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) and the hackathon's own cross-asset portfolio idea. Public [PARALLAX](https://github.com/rishu4436/parallax/blob/main/docs/STRATEGIES.md), [NightDesk](https://github.com/PhiBao/nightdesk) and [Portir](https://github.com/yeheskieltame/portir) materials don't describe a BTC-to-MSTRB task in the pages checked, but absence from those pages is no proof of novelty. The next comparison must use the same trigger, same size, same wallet and same end action.

The proposed benefit is **access to a separate equity exposure during a closed stock session with a sized BNB Chain execution path**. We have measured neither positive trading alpha nor a meaningful user time saving. If the on-chain RFQ is unavailable, uneconomic at small sizes, or indistinguishable from the current Agentic Wallet flow, reject this candidate. If the token reacts at once to BTC, a claimed lag strategy also fails. A special app for rare large shocks is a poor bet on this ten-weekend sample. The [Binance RWA `referencePrice` definition](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) is derived from the on-chain token price and cannot supply an independent US share benchmark.

## Agent Studio role under test

The [current Studio quickstart](https://docs.bnbchain.org/developer-kit/bnbchain-studio/quickstart/) builds a seller service with A2A, MCP and x402. A possible job is a timestamped, contract-specific BTC/MSTRB movement and market-state packet for another agent. Any paid packet must deliver something beyond a free price query, such as a trustworthy, size-aware execution assessment, and an identified buyer must value it. A Web3 RFQ lives about 30 seconds and is bound to the eventual wallet signer, so it should be requested in the user's own transaction flow after any paid analysis. The Studio seller has no authority to sign the user's MSTRB order. A persistent paid service remains optional until its buyer, runtime and payment path are demonstrated.

The earlier Binance Skills Hub [bStock AI Trading Competition reference](https://github.com/binance/binance-skills-hub/blob/main/skills/binance-web3/binance-agentic-wallet/references/campaign.md) is explicitly expired since 2026-09-01. It is not the current hackathon's scoring or a current reward path.

## Next evidence gate

1. Confirm bStock issuer terms and precise location eligibility for the candidate user and token.
2. During the next Friday 20:00 to Sunday 20:00 ET window, collect timestamp-matched BNB Chain MSTRB RFQs for 25, 100 and 500 USDT, in both directions where possible. Record route, expiry, quoted output, slippage, fees, gas and failures. A Spot CEX book or pool TVL cannot substitute.
3. Compare the same BTC move and amount with the official Agentic Wallet and at least one entrant. Record whether our flow changes a decision or reduces steps without hiding risk.
4. Only then decide whether to select a product, write a one-page spec and build a thin slice. If Agent Studio has no separate buyer job, leave it out.
