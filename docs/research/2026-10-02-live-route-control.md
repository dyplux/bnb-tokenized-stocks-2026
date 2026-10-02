# Live NVDAB route control, 2 October 2026

## Question and method

Does the first live Binance Web3 NVDAB sell estimate have a plausible price relative to one independently callable BNB Chain pool? This is a technical control, not a best-execution study or a user task.

At BNB block `125343736`, timestamp 2026-10-02 18:53:21 UTC, the public QuoterV2 at `0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997` was called through `eth_call` with `quoteExactInputSingle` for exactly 1 NVDAB to BNB Chain USDT, fee tier 2500 and no price limit. The [PancakeSwap mainnet deployment](https://github.com/pancakeswap/pancake-v3-contracts/blob/main/deployments/bscMainnet.json) identifies that QuoterV2; the [prior pool check](2026-10-01-nvdab-sized-pool-quote.md) verified the token contracts and 0.25% fee tier. The call returned `234299608428871275878` raw USDT units, or **234.299608428871275878 USDT** at 18 decimals. It is a quote against one fixed pool state, not a transaction or a multi-pool best route.

The signed [Binance Trading API quote](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) for the same contracts, chain and raw 1 NVDAB input arrived at 18:53:23.435 UTC after 847.939 ms. It returned HTTP 200, business code 0, one LiquidMesh `SWAP` route and `234788583615476721962` raw estimated USDT units, or **234.788583615476721962 USDT**. The arithmetic difference was **0.488975186605446084 USDT**, or **20.8696544516 basis points** relative to the PancakeSwap pool quote. Binance did not give the pool's fixed block in this recorded output. The two estimates are close in time, but they are not same-block or executed outcomes.

A further signed quote at 18:53:40.851 UTC returned one LiquidMesh `SWAP` route with `234704136820000000000` raw estimated USDT units. Its `dexRouterList` named **Elfomofi** for 100% of that route. No route address, quote ID, wallet address, signed header, order or calldata was retained. The changed output across roughly 17 seconds shows why the earlier 20.87-basis-point gap must not be advertised as a stable saving. The route name does not independently validate its pool, liquidity, token approval or execution safety.

## Decision impact

The Binance estimate is of the expected order of magnitude and can differ from a single PancakeSwap pool quote. This supports an amount-specific route check as a real technical capability. It does **not** show an unmet user problem: an eligible holder may already obtain the Binance quote directly, and no participant has compared it with borrowing for the same cash need. A temporary nonholder address cannot prove sale execution or final received USDT. Keep the main product gate and the 4 October review in place.
