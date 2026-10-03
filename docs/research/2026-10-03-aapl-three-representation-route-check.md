# One Apple amount, three token representations

**Observed:** 2026-10-03, 22:38 to 22:41 UTC. **Task:** ask the Binance Web3 API whether a self-custodial BNB Chain wallet can obtain a current quote to spend exactly 5 USDC on a tokenized Apple representation. This was a bounded read-only research check, not a transaction or eligibility test.

## Identity observations

Three signed RWA search GETs for NVDA, MSTR and AAPL returned HTTP 200 and business code 0. Their exact-ticker rows listed Ondo and bStock representations but no xStock representation on chain 56. The AAPL request began at 22:40:02.702 UTC and took 1059.6 ms.

The separate public Binance [stock detail list](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=2), read at about 22:39 UTC, returned 269 type-2 rows, of which 130 carried `chainId=56`. It listed AAPLx on BNB Chain at `0x9d275685dc284c8eb1c79f6aba7a63dc75ec890a`. The count is a snapshot of this public endpoint, not a claim that 130 xStocks have liquid Binance Web3 routes. The discrepancy between signed search and public listing is a developer integration finding. It does not prove the token is absent from every RWA API route.

## Same-size quote observations

The existing [sanitized probe](../../scripts/probe_binance_quote.py) made one signed, read-only Trading API GET per representation on chain 56, using the same public wallet address, exact 5 USDC raw input and pinned USDC contract. The address, keys, signed headers, quote IDs and raw responses were not retained.

| Input to output | UTC request start | HTTP / business code | Sanitized result | Latency |
|---|---|---|---|---:|
| 5 USDC to AAPLx | 22:40:20.880 | 200 / `40374` | `rwa_no_vendor_liquidity`, zero routes | 531.819 ms |
| 5 USDC to AAPLon | 22:40:34.842 | 200 / `40368` | `ondo_stablecoin_pair_not_supported`, zero routes | 376.971 ms |
| 5 USDC to AAPLB | 22:40:41.951 | 200 / `0` | One LiquidMesh `SWAP` estimate of `0.014996395333461012 AAPLB`; reported `tradeFee` was `0.02958762` USD and `estimateGasFee` was `450000` | 378.069 ms |

The AAPLon and AAPLB contract addresses came from the signed AAPL RWA search. The AAPLx address came from the public Binance type-2 list. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) labels output and network fees as estimates. These three requests were separated by seconds, not simultaneous or executable orders. They prove only different responses for this exact provider, pair, size and time. An unsupported USDC pair does not mean another stablecoin pair is unsupported. A `40374` does not mean AAPLx is untradeable on every venue.

## Product implication and counterevidence

This is a real difference a user could encounter when the same ticker has several tokens. It supports showing `no route`, `pair unsupported` and `quote returned` as distinct states. It does **not** justify presenting AAPLB as the right choice: the founder's issuer eligibility is unconfirmed and no swap, approval, gas payment, price comparison, final cost or future exit was observed.

The inspected [Yostocks buy scan](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/apps/agent/yo.mjs#L94-L105) already seeks several BSC representations and selects a guarded quote. Its full live path was not run here. The three-route observation is useful for the Developer Experience Report and for judging any product hypothesis, but a generic route screener would overlap this incumbent. A next product decision must identify a user action that the incumbent cannot already support.
