# Monday benchmark protocol fixed before the outcome

**Locked:** 2026-10-04 UTC. **Question:** did a tokenized equity's Sunday per-share price contain information about the next regular US stock session beyond the last dated Friday close? This is a descriptive three-asset case study, not a trading backtest or a claim of predictive alpha.

## Frozen sample and clocks

- Assets: NVDA, TSLA and COIN, chosen because [Friday daily closes](../../data/external_reference/2026-10-02-yahoo-close.json) and a complete 40-contract BNB Chain tape at Sunday 12:00 UTC are already recorded. Don't add an asset after seeing Monday's result.
- Sunday anchor: five-minute collector slot `5970384`, starting 2026-10-04 12:00 UTC. Compare bStock and Ondo representations separately, then group by canonical ticker. Per-share token value is `tokenPrice / tokenToShareRatio`, with the ratio and price from that slot's logged sources. A ticker pair is not presumed legally equivalent.
- Prior benchmark: Yahoo Finance's 2026-10-02 daily **regular-session close** for each ticker. It has a session date, not a tick-level update timestamp. Friday after-hours are missing from this protocol and can explain part of any apparent Sunday gap.
- Outcome benchmark: the 2026-10-05 US regular-session **open** and **close**, from dated historical rows at [NVDA](https://finance.yahoo.com/quote/NVDA/history/), [TSLA](https://finance.yahoo.com/quote/TSLA/history/) and [COIN](https://finance.yahoo.com/quote/COIN/history/). Record the retrieval time, exact row date, source URL and any unavailable or revised value. Cross-check against an exchange or issuer source if the value is disputed. Don't invent an intraday trade timestamp from a daily row.
- Session clock: America/New_York under [Nasdaq's published regular hours](https://www.nasdaq.com/market-activity). Holiday and security-specific halt status need separate confirmation before calling 2026-10-05 a normal opening.

## Fixed comparisons

For each of the six token representations, calculate:

1. `friday_to_sunday_pct = 100 * (sunday_per_share / friday_close - 1)`.
2. `friday_to_monday_open_pct = 100 * (monday_open / friday_close - 1)`.
3. `sunday_to_monday_open_pct = 100 * (monday_open / sunday_per_share - 1)`.
4. Whether the **sign** of Friday-to-Sunday matches Friday-to-Monday-open. Report all six rows, including mismatches and nulls, without selecting the best issuer or ticker after observation.

Then report the median absolute Sunday-to-open residual across available rows and the range between bStock and Ondo for each ticker. These are descriptive; six rows from three underlyings are not six independent predictions. A single weekend and three tickers cannot establish repeatability or profitable execution.

## Kill and promotion conditions

- If an outcome row is unavailable or its session date is ambiguous, mark it missing. Don't replace it with a later close while calling it an open.
- If any provider's token price or share ratio is missing at the frozen Sunday slot, keep its row null. Don't substitute a later quote.
- If Sunday signs disagree with Monday open on most available tickers, or residuals are large relative to the observed movement, do not promote a directional edge claim.
- Even if signs match, don't promote a trading product without at least one repeat weekend, comparable Friday after-hours data, amount-specific buy and sell quotes, fees, access checks and a funded or simulated execution path. Monday's daily open can't prove a fill at that price.
- The independent underlying reference-update time remains `null/UNKNOWN` unless a separate source gives an actual dated update. A daily open or close date isn't the Binance feed's reference clock.

**Output target after the session:** `monday_open_benchmark.csv`, `monday_open_results.json` and a short findings note with every excluded row. Keep the Sunday LIVE tape and later historical benchmarks distinct.
