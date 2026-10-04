# Sunday token prices against the prior Friday close

**Comparison time:** 2026-10-04 12:00 UTC. **Sources:** one complete LIVE Binance Web3 collector slot and Yahoo Finance's historical daily close for Friday 2 October. The [external benchmark record](../../data/external_reference/2026-10-02-yahoo-close.json) preserves the three source URLs, prices, session date and retrieval time. Yahoo's pages reported [NVDA $233.95](https://finance.yahoo.com/quote/NVDA/history/), [TSLA $370.59](https://finance.yahoo.com/quote/TSLA/history/) and [COIN $183.00](https://finance.yahoo.com/quote/COIN/history/?p=COIN) for the 2 October daily close. [Nasdaq's published session hours](https://www.nasdaq.com/market-activity) identify 16:00 ET as the regular close. This is a historical daily bar, not a tick-level stock quote with a separately verified timestamp.

| Stock | Friday close, USD | bStock token-derived per share | Ondo token-derived per share | Gaps to Friday close |
|---|---:|---:|---:|---:|
| NVDA | 233.95 | 234.477524 | 234.825 | +0.2255%, +0.3740% |
| TSLA | 370.59 | 371.36 | 371.665 | +0.2078%, +0.2901% |
| COIN | 183.00 | 185.34 | 185.425 | +1.2787%, +1.3251% |

The [six-row calculation](../../experiments/EXP-RWA-004/friday_close_benchmark.csv) divides each live token price by its same-cycle `tokenToShareRatio`, then compares that arithmetic per-share value with the external daily close. Both Binance raw-response hashes and the source page are recorded per row. The [result manifest](../../experiments/EXP-RWA-004/friday_close_benchmark_results.json) freezes collector slot `5970384`. No raw token ticker was treated as proof of equal rights.

**Interpretation:** the six Sunday values were above those three Friday regular-session closes. This demonstrates a dated cross-source difference, not mispricing or a user edge. Friday after-hours trades, spread, route fees, issuer rights, market access and a Monday stock opening price were not included. Yahoo's daily row has a session date but no independent tick timestamp; `reference_age_seconds` stays null and `reference_age_status` stays `UNKNOWN`. The close is a research benchmark, not a replacement for a timed reference field in the Binance API or a live product feed.

**Next falsification step:** retain the weekend tape through the next regular session, obtain a dated Monday stock benchmark from an independent source, then compare the Sunday token values with the Monday outcome. Even a correct directional match in one weekend would need repeats and executable quotes before any performance claim.
