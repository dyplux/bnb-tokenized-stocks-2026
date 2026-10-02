# First live Binance Web3 bStock quote

**Observed:** 2026-10-02 18:34 to 18:35 UTC. **Scope:** read-only technical probe, not a holder session, executable order or trade.

## Inputs and method

The local [quote path](../../app/server.py) searched the signed Binance RWA endpoint for exact NVDA/bstock/BNB Chain/NVDAB identity, read both token contracts and their 18-decimal metadata at BNB block `125341267`, then requested a signed `GET /api/v1/dex/aggregator/quote` for 1 NVDAB to BNB Chain USDT. It used a fresh random public address with no known holder or signer. No wallet private key was created, and no `/swap`, approval, order or broadcast was requested. The address, signed headers and quote ID were omitted from the output.

The first application-path response had HTTP 200, business code 0 and one route. Identity search took 651.814 ms; quote took 315.419 ms. The quote arrived at 18:34:51.838 UTC. The route reported `LiquidMesh`, `executionMode=SWAP`, raw input `1000000000000000000` NVDAB units and raw estimated output `234648094092315526998` USDT units. The application deliberately returned `route_observed_mode_review_required` and no net sale proceeds.

A second signed quote at 18:35:28.067 UTC checked the selected cost fields. It returned HTTP 200, business code 0 in 303.133 ms, one LiquidMesh `SWAP` route, the same raw input and raw estimated output `234646962292722258753` USDT units. Both token metadata objects reported 18 decimals. The route reported `tradeFee="0.01800319"`, `estimateGasFee="450000"`, `priceImpactPercent="0.0000039004"`, and null `feeAmount`, `feeToken` and `actualSwapAmount`. The API server timestamp was `1790966128035` ms. The second quote did not repeat the on-chain metadata read, so the earlier block is not its atomic source block.

## Interpretation and limits

- The documented [quote reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says RWA routes always return `RFQ`; this live NVDAB response returned `SWAP`. The [Trading API introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) allows bStock SWAP routes. The app's review-required state is therefore warranted. This is a documentation contradiction observed against a live response, not proof that the route can be executed.
- With 18 decimals, the second raw output represents **234.646962292722258753 USDT estimated buy-token units**. It is not final received USDT. The quote has an approximately 30-second ID lifetime; neither response is current after that window.
- The reference calls `tradeFee` an estimated network fee in USD and `estimateGasFee` gas in the chain's smallest unit. The returned `450000` doesn't by itself give a paid gas cost or settled proceeds. The null fee fields mean no custom referral fee was supplied, not that execution has no costs.
- A random nonholder address proves only a technical read path. It cannot establish balance, wallet eligibility, user need, executable allowance, a safe Venus loan, fill, profit or a meaningful sell-versus-borrow decision.

**Next proof:** observe a consenting eligible holder's real cash task, request the same amount for their public wallet, and compare a fresh quote with their actual borrowing state and alternatives. Confirm route execution semantics with the Binance team before presenting SWAP as an actionable route.

## Local display slice

After the live observation, the server began exposing `estimated_output_usdt` alongside the validated raw route fields. The separate Sale check displays an approximate estimated amount, mode and response time; the main cash-choice card remains **Unquoted** and shows no net proceeds. The displayed estimate clears after 20 seconds. Five targeted synthetic quote-flow tests passed. A Chrome run with an intercepted synthetic quote at 320 CSS pixels showed the estimate and mode-review label, no horizontal overflow or page error, and the expiry state after 20 seconds. This browser run did not call Binance or validate a holder task.
