# Route response mode, Sunday matrix

**Observed:** 2026-10-04 14:34 UTC. **Method:** signed read-only Binance Web3 RWA catalog and price, four `/underlying-market` calls and eight `/aggregator/quote` calls. Two tickers, two providers, buy and sell, approximately 100 USDT per direction. A temporary unfunded wallet was used and not retained. Full bounded observations and raw response hashes are in [the matrix](../../experiments/EXP-RWA-009/route_semantics_matrix.json).

| Security | Provider | API market status | Buy | Sell |
|---|---|---|---|---|
| NVDA | bStock | null, `openState=true` | `SWAP`, one route | `SWAP`, one route |
| NVDA | Ondo | `offhours`, `openState=true` | `SWAP`, one route | `SWAP`, one route |
| TSLA | bStock | null, `openState=true` | `SWAP`, one route | `SWAP`, one route |
| TSLA | Ondo | `offhours`, `openState=true` | `SWAP`, one route | no route, business `40374` |

The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes equity/RWA routing as `RFQ`. The [Trading introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) also describes bStock `SWAP`. These eight Sunday responses are enough to require a client to read the returned `executionMode`; they aren't enough to claim a documentation defect or universal SWAP behavior. No Monday regular-session row exists yet. Re-run the same script during the preregistered Monday window with `--label regular-session` and compare *observed* market states, route counts and mode. The label alone is not evidence that the US market is open.

No quote here establishes holder eligibility, final execution cost, fill, price discrepancy or tradability. The TSLAon sell result is size, time and wallet-context specific.
