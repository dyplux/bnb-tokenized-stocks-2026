# Problem brief, 2026-10-01

## User and task under investigation

A BNB Chain user wants to buy a specific tokenized stock exposure with a fixed amount, for example 50 USDT of NVDA, and needs to choose the correct representation and know whether a spot quote is available before confirming. The candidate comparison is between bStocks and Ondo on BNB Smart Chain. This user and task are hypotheses. No user interview or completed session has been observed.

## Evidence available

- The [event track](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=tracks), checked 2026-10-01, explicitly centers bStocks, Ondo and xStocks, BSC mainnet and spot activity. This proves event fit, not demand.
- [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), checked 2026-10-01, already documents ticker lookup, status, quote and confirmation for stock tokens. [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas), checked the same day, already offers a multi-issuer stock trading flow. These are substantial substitutes.
- A separate internal market snapshot found very different indexed swap counts for distinct NVDA token contracts. That is a lead for choosing test cases, not evidence of people, available liquidity or demand for this product. The new project needs its own reproducible observations before publishing numbers.
- [Binance RWA Data documentation](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data), checked 2026-10-01, exposes platform, underlying, token price, token-to-share ratio and market information. Its `referencePrice` is converted from the on-chain token price. It is not an independent equity quote.

## Candidate failure to test

The same ticker may lead to different contracts, issuers, ratios, rights, availability and quotes. A clear decision receipt could put those differences in one place before confirmation. Documentation does not establish that the existing flows fail to show the information or that a user changes a choice after seeing it.

The primary proposed output is a dated receipt for the user's ticker and amount: platform and contract, ratio and issuer terms where documented, market state, source times, a live quote or explicit unavailability, and the reason the comparison is incomplete. It must say which facts are API observations and which come from issuer documents.

## Alternatives and counterevidence

The user can use PancakeSwap, Binance Agentic Wallet, an issuer's own flow, a spreadsheet, a script, a conventional broker, or wait until the underlying market opens. [Alternatives map](alternatives-map.md) records the workflow and the precise gap still to test. The strongest counterargument is that a new receipt adds text without changing any decision.

## Decision-changing observation

For NVDA, AAPL and TSLA, compare 20, 50 and 100 USDT at one open-market interval and two closed-market intervals. Capture the same task in the candidate flow, PancakeSwap and Agentic Wallet. Record the displayed contract, ratio, status, quote, validity, costs and recovery from missing data. Stop the hypothesis if no cell changes a reasonable choice or prevents an identifiable error, or if an incumbent already gives the same pre-confirmation answer. No trading is needed for this test.

Frequency of the task, user pain, eligible jurisdictions, quote coverage and willingness to use an additional product remain unknown. A social post or holder count cannot fill those gaps.
