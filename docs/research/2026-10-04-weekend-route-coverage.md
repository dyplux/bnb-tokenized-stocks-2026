# Weekend route coverage for the monitored stock universe

**Question:** can the Binance Web3 aggregator return a 100 USDT buy route for each BSC stock representation already sampled by the 40-contract collector on Sunday? **Measurement:** 4 October 2026, about 13:25 to 13:26 UTC. One sequential signed quote request per contract, using one temporary, unfunded address. [Full normalized results](../../experiments/EXP-RWA-009/weekend_route_coverage_100usdt.json) and [reproduction script](../../scripts/probe_route_coverage.py).

| Provider | Contracts queried | At least one route | No route | Returned route mode |
|---|---:|---:|---:|---|
| bStock | 35 | 34 | 1 | 34 `SWAP` |
| Ondo | 5 | 4 | 1 | 4 `SWAP` |
| Total | 40 | 38 | 2 | 38 `SWAP` |

The two no-route responses were AAOI bStock and MSTR Ondo. Both returned business code `40374` with a message to decrease transaction size or try later. They are amount-specific responses, not proof of permanent unavailability. Each quote was requested at 100 USDT in the API-confirmed 18-decimal BSC USDT contract. The 40 requests were sequential, so they aren't a simultaneous market snapshot. This established universe has all 35 signed bStock equity rows plus the five selected Ondo tickers AAPL, NVDA, TSLA, COIN and MSTR. It excludes other Ondo stocks and xStocks; no inference about their coverage follows.

This shows that tokenized-equity **quotes** remain available through much of the monitored BSC universe during the Sunday US equity-market closure. It doesn't show that a person can legally acquire each product, that a funded wallet can pass approvals and simulation, that a quote will survive its short lifetime, or that a trade will settle. Issuer rights and an independent underlying price timestamp are unresolved. A 100 USDT quote isn't an alpha signal.

## Follow-up on the two missing routes

At 14:08 to 14:10 UTC, a bounded [size probe](../../experiments/EXP-RWA-009/weekend_missing_route_size_probe.json) requested 10, 100 and 1,000 USDT buy quotes for AAOI bStock and MSTR Ondo using the same signed API and an unfunded temporary address. AAOI returned one `SWAP` route at **all three sizes**, including the 100 USDT size that had failed in the earlier coverage run. Its earlier no-route result was therefore time-sensitive; these sequential calls don't isolate the cause of recovery. MSTR Ondo returned business code `40374` and no route at **all three sizes** in this later window. That doesn't prove it has no liquidity on another venue or at another time. The follow-up made no trade and didn't establish investor eligibility.

## Indicative price versus quoted entry

A [local calculation](../../experiments/EXP-RWA-009/quote_vs_metadata_100usdt.json) reuses the retained quote bodies without another API request. It converts the 100 USDT input to USD with that quote's `fromToken.tokenUnitPrice`, divides by its estimated output token quantity, then compares the implied entry price per token with that same quote's `toToken.tokenUnitPrice`. These are two fields within one API quote, not an independent stock price.

For the 34 routed bStocks, the median implied entry premium was +0.1015%, ranging from -0.1804% to +0.4159%. For the four routed Ondo tokens, the median was +0.0092%, with one NVDA response at +1.6193%. That NVDA response reported `priceImpactPercent=0.0125115040`. Price impact and the entry-versus-indicative comparison answer different questions; don't relabel one as the other. The quoted network fee was an estimate, and the calculation isn't an all-in trade cost. There were no fills or wallet approvals.

For product selection, the result weakens a simplistic “the market is closed, so nothing can be quoted” premise. The sharper problem is deciding what can responsibly be acted on when quotes exist but independent issuer-reference freshness and user eligibility can't be established from the current response. [OneTicker](2026-10-04-gateway-substitute-audit.md) already offers a generic market gate, so this observation alone doesn't justify another gateway. The next discriminator is whether a narrow workflow can return a useful, provable next action to a real user without pretending these unknowns are known.
