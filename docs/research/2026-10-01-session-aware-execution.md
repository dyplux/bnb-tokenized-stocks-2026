# Session-aware bStock execution: research test

**Checked:** 2026-10-01 UTC
**Status:** provisional test, not a selected product or a claim of trading profit

## User task and economic result

An eligible person already holds USDT on BNB Smart Chain and wants to buy or sell a specific bStock while the US cash market is closed. Before signing, they need to know whether the actual wallet-size route is reasonably priced, how much token they receive or USDT they recover, and when the quote expires. The useful action is to sign within a user-set cost limit, choose a better executable route if one exists, or wait. A bad route avoided can save money relative to that route. It doesn't create a predictive trading edge.

This user segment is narrower than “anyone who can't buy stocks.” [Binance says eligible users already trade bStocks 24/7 on Binance Spot](https://www.binance.com/en/academy/articles/what-are-bstocks-a-guide-to-tokenized-stocks-on-binance), with fractional exposure from US$5; [its August announcement added bStocks Spot bots](https://www.binance.com/en/support/announcement/detail/ae96da838d754f91bced1501de728f03). bStocks are certificates that give economic exposure, not direct share ownership. Ineligible people cannot become eligible merely by using a BNB Chain wallet. [The issuer FAQ says third-party integrators must apply geographic controls](https://www.binance.com/en-AE/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38). The product would serve an eligible self-custody user who has funds on-chain and values execution control, not a person seeking to bypass restrictions.

## Why a same-token benchmark is worth testing

The [Binance Spot order-book endpoint](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#order-book) exposes bids, asks, quantities and an update ID for `MSTRBUSDT`. It has no server event timestamp in its documented response, so local request start/end times have to bound freshness. A comparable [Binance Web3 aggregator quote](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) is amount-specific, wallet-bound for RWA RFQ routes and has an approximately 30-second route ID lifetime. Both must refer to the **same MSTRB token**, unit and side. The spot book is an indicative reference for a self-custody wallet, not automatically an executable alternative for that wallet. Fees, gas, withdrawal/deposit steps and eligibility matter before describing savings.

At 12:45:46.872 to 12:45:48.014 UTC, a read-only Spot `MSTRBUSDT` depth response had best bid 154.84 USDT for 1.906 MSTRB and best ask 154.86 for 4.300 MSTRB. A [DEX Screener pair response](https://docs.dexscreener.com/api/reference) for the BNB Chain MSTRB/USDT pool, received at 12:45:48.233 UTC, displayed `priceUsd=154.72`, about 0.08% below the Spot bid. This DEX figure is an index price, **not an amount-specific quote** and its underlying observation time was not established. At 12:46:40 UTC, Binance's [public token dynamic surface](https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai?chainId=56&contractAddress=0xe87afb3076aeb0f9b14e368de8145ae6a2826a14) showed `tokenInfo.price=154.8`, `sharesMultiplier=1`, `openState=true` and `stockInfo.price=null`. That later website response cannot be combined into a trade or arbitrage claim. The first attempt to fetch it used an incorrect path and returned HTTP 404; this was our probe error, not a Binance API failure.

The purpose of this snapshot is to show which fields exist and what cannot be inferred from them. It records no Binance Web3 RFQ, on-chain fill, CEX trade or user outcome.

## Existing products already cover much of the flow

The [Binance Web3 aggregator](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) sorts vendor routes by quoted output and already provides route IDs. [yostocks source](https://github.com/yostocks-protocol/yostocks/blob/main/apps/agent/yo.mjs) requests wallet quotes, selects the best passing quote and rejects prices more than 1% away from a reference. Its reference uses `stockInfo.price` when present and otherwise an Ondo token price. The Ondo fallback may update through weekends; there is no observed false rejection. Binance Spot already offers 24/7 bStocks and bot services to eligible users. A generic weekend alert, route selector or 1% guard would repeat existing work.

A distinct result would require showing that a same-token, same-side, size-aware benchmark catches a materially bad **BNB Chain route** that those flows accept, or that it makes an eligible user's on-chain action measurably clearer or cheaper. The benchmark must not compare a bStock with a different issuer's wrapper as though they were fungible. When the spot book is stale, token unit is uncertain, a quote has expired, or the user is ineligible, the app should state that it cannot assess or execute. It should never issue an automated trade recommendation from BTC correlation alone.

Small orders make the bar harder: an illustrative 0.5% improvement on a 100 USDT order is 0.50 USDT **before** network and transaction costs. If the actual fees exceed that amount, the route change doesn't save money. This is arithmetic for a proposed decision rule, not an observed opportunity.

## Required measurement before product selection

1. Confirm one eligible user scenario and issuer terms. Record why this person uses BNB Chain instead of Binance Spot or their broker. No identity or private wallet information belongs in the repo.
2. During a Friday 20:00 to Sunday 20:00 New York window, request signed read-only Web3 quotes for the same MSTRB contract and wallet at 25, 100 and 500 USDT, both directions where possible. Capture local start/end times, server timestamp if returned, route/vendor, quoted output, fees, gas estimate, expiry and redacted errors. Never reuse a 30-second route ID for a later decision.
3. Capture the same-token Spot depth immediately around each RFQ and calculate the book's size-weighted indicative buy or sell price, explicitly accounting for the fact that a BNB wallet cannot directly lift CEX offers. Compare two actually available BNB routes if the API returns them.
4. Run the exact task in Binance Wallet and yostocks if possible. Record the decision made, steps, stale or missing state, and whether our proposed check changes it. One counterexample where an incumbent already handles the case defeats the novelty claim.
5. Reject this direction if the RFQ is unavailable, if cost differences don't survive all-in costs, if the benchmark cannot stay fresh, or if an incumbent already gives the same practical answer. If the only benefit is a nicer receipt, it overlaps Bell.

## Agent Studio boundary

[Current BNB Agent Studio](https://docs.bnbchain.org/developer-kit/bnbchain-studio/quickstart/) is well suited to a paid seller that delivers durable analysis over A2A/MCP/x402, with testnet identity and a managed trial. A dated, contract-specific **historical execution-quality report** could be durable; a live wallet RFQ cannot, because it is wallet-bound and expires quickly. We have no buyer who has agreed to pay for such a report, and NightDesk already offers paid session context. Studio remains an optional, separately falsified service. The main product would need its own Binance Web3 API integration and user-controlled mainnet execution. No Studio install, registration or payment is justified at this gate.

For the hackathon's Studio special, a demo would have to show a real separate buyer request, an ERC-8004 agent identity, a runtime that continues the job without an open terminal, an x402-funded dependency or fee path, and a returned analysis artifact. The current quickstart's managed BNB deployment is a 48-hour **testnet** trial; it isn't the mainnet spot execution path. Building these parts just to qualify for US$2,000 would consume the remaining window without demonstrating the user's core benefit.

## Decision

The ten-weekend BTC/MSTRB observation supports choosing MSTRB as a liquid candidate for a quote test, but its weak next-hour lead signal offers no measured alpha. The official 24/7 Spot and bot products remove a broad “weekend access” advantage for eligible Binance users. This leaves a narrower hypothesis: protect a self-custody user's exact on-chain execution. It has a clear falsification path and remains **unvalidated** until signed Web3 quotes and an incumbent task comparison exist.
