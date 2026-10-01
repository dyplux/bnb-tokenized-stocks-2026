# Weekend move and cash-market reopen screen, 1 October 2026

## Product question

Does the direction of a bStock's weekend move provide a simple directional edge during the first hour around the US cash-market reopening? This is a bounded screening exercise for the founder's economic-edge question, not a backtested trading system or evidence of a profitable BNB Chain spot trade.

## Sources and calculation

- Public Binance Spot `GET /api/v3/klines` hourly bars for `NVDABUSDT`, `TSLABUSDT`, `MSTRBUSDT`, `SPYBUSDT` and `QQQBUSDT`, fetched 1 October 2026 around 18:16 UTC from `https://api.binance.com`. Query parameters were `interval=1h`, `startTime=2026-07-01T00:00:00Z`, `endTime=2026-10-01T16:00:00Z`, `limit=1000`, paginated by the next hourly open time. This is the [Binance public Spot market-data surface](https://developers.binance.com/en/docs/products/spot/rest-api); no API key was used.
- The [Nasdaq 2026 holiday calendar](https://www.nasdaq.com/market-activity/stock-market-holiday-schedule) marks Friday 3 July and Monday 7 September as closed. Excluded the Monday 6 July long-weekend case and Monday 7 September holiday case so that each included Friday 20:00 UTC and Monday 13:00 UTC bracketed an ordinary cash-market weekend during daylight-saving time.
- For each included Monday, `weekend_return = open(Monday 13:00 UTC) / open(previous Friday 20:00 UTC) - 1`. `reopen_hour_return = open(Monday 14:00 UTC) / open(Monday 13:00 UTC) - 1`. The Monday 13:00 to 14:00 bar straddles the 13:30 UTC US cash open. `Monday_to_20UTC_return` uses the Monday 20:00 bar open as its endpoint. All returns below are tokenized-stock **CEX Spot** prices, not underlying shares or BNB Chain executable quotes.
- Counted quote-asset volume in the weekend interval from the same hourly bars. Bars with missing boundaries or nonpositive prices were excluded. No liquidity threshold was applied; SPYB had some very thin early weekends. The five symbols share the same market dates and are **not independent observations** for a statistical significance claim.

## Result

| Spot symbol | Included weekends | Same direction in reopen hour | Opposite direction | Zero | Pearson r: weekend vs reopen hour | Median absolute weekend move | Median weekend quote volume |
|---|---:|---:|---:|---:|---:|---:|---:|
| NVDABUSDT | 11 | 5 | 6 | 0 | -0.043 | 0.720% | 1.62m USDT |
| TSLABUSDT | 11 | 6 | 5 | 0 | -0.123 | 0.814% | 1.82m USDT |
| MSTRBUSDT | 11 | 5 | 6 | 0 | +0.130 | 0.879% | 3.97m USDT |
| SPYBUSDT | 11 | 6 | 4 | 1 | -0.117 | 0.311% | 1.71m USDT |
| QQQBUSDT | 11 | 6 | 5 | 0 | -0.179 | 0.591% | 6.69m USDT |
| **Pooled counts, not independent** | **55** | **28** | **26** | **1** | **not pooled** | **not pooled** | **not pooled** |

The sampled weekends are the Mondays 13, 20 and 27 July; 3, 10, 17, 24 and 31 August; and 14, 21 and 28 September 2026. All five symbols returned hourly bars at the four required boundaries on these dates. The Pearson numbers are descriptive for eleven observations per asset. No model was fitted, parameter optimized or holdout reserved.

## Interpretation and limits

This screen offers no support for a rule such as "buy when the bStock rose over the weekend" or its simple reversal. Counts are near even and correlations are small and mixed across the five symbols. This does **not** prove that no conditional, event-specific or longer-horizon edge exists.

It also doesn't measure actual bid/ask, fees, gas, funding, route availability, slippage, taxes, legal access, BNB Chain transaction outcomes or a Binance Web3 API quote. A Monday 13:00 to 14:00 bar includes 30 minutes before and 30 minutes after the traditional opening bell, so it isn't a pure post-open response. The sample starts after bStock listings, has only eleven ordinary weekends, and may contain related moves across the five assets. Do not turn this into a PnL or predictive claim. A useful product must still name a user's specific action and demonstrate a Web3 API result that an incumbent flow misses.
