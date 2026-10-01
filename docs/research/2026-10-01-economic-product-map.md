# Economic product map for the BNB tokenized-stocks entry

- **Checked:** 2026-10-01
- **Decision:** one active falsification test, no selected product or implementation

## What an eligible user can gain

The [event rules](https://www.bnbchain.org/en/hackathons/tokenized-stocks) require a working Binance Web3 API integration, BNB Chain mainnet spot and a central bStocks, Ondo or xStocks task. They score technical implementation at 30%, originality at 25%, the founder's real Developer Experience Report at 25%, and product/UX at 20%. An agent doesn't earn points merely by predicting profit. The event specifically says agent projects are judged on how well they're built, not on theoretical PnL.

| Possible benefit | Source or observation | Limit for a product claim |
|---|---|---|
| Access while a traditional stock venue is closed | [Binance says](https://www.binance.com/en/academy/articles/what-are-bstocks-a-guide-to-tokenized-stocks-on-binance) eligible users can trade bStocks 24/7 and start with $5 on its own product. | A funded BNB wallet doesn't bypass issuer restrictions. Access is already provided for some eligible Binance users. An on-chain quote may still be unavailable. |
| Retain self-custody and use the position in DeFi | [BNB Chain's bStocks introduction](https://www.bnbchain.org/en/blog/introducing-bstocks-on-bnb-chain-trade-24-7-with-zero-fees-deploy-across-defi-protocols-with-full-self-custody) documents withdrawal to compatible wallets and integrations. | A user must value self-custody and accept its costs and risks. Existing venues and Steward cover much of this. |
| Cash from an existing holding | [Binance's FAQ](https://www.binance.com/en-AE/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38) says bStock dividends are generally reinvested through a multiplier. | Selling part of the holding changes exposure and may cost more than the incremental amount. It's a liquidity choice, not added yield. |
| Better net execution | [Binance Web3 Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) provides amount-specific routes, already ordered by quoted output. | Fees, gas, quote expiry and a real alternative must be measured. Multiple entrants already guard or record quotes. |
| Predictable trading alpha | A [ten-weekend Spot sample](2026-10-01-weekend-crypto-equity-task.md) found BTC and MSTRB moving together; the BTC-to-next-hour MSTRB correlation was only 0.074. | No BNB Chain strategy or net PnL was measured. A reported correlation doesn't support a trading promise. |

The founder's claim that most people can't buy stocks hasn't been verified. Some users are legally ineligible for tokenized securities, and the app can't make them eligible. Others already have small fractional access via Binance or a broker. A first-time onboarding product would need an eligible user, funding route and an observed obstacle. Don't use restricted users as a growth story.

The [Binance Stocks Trading REST API](https://developers.binance.com/en/docs/catalog/advanced-trading-stocks-trading/api/rest-api/market-data) also documents symbol-specific fractional and extended-session flags, a conventional-equity bid/ask endpoint, and bStock mint/redeem data. This is another incumbent for an eligible Binance user. It needs a separate Binance account API key, so its published availability doesn't show what this project or a BNB wallet can access. It weakens a generic "stocks for people who can't buy stocks" pitch and offers a possible reference price only after access, ticker, unit and timestamp are checked.

## The three concrete tasks considered at this gate

| User task | Incumbent / counterevidence | What the product would have to prove | State |
|---|---|---|---|
| Buy a bStock after the US close because BTC or company news moved | Binance Spot and bots are 24/7; [Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) documents persistent news and earnings rules; yostocks and NightDesk publish guarded buy flows. Our ten-weekend sample offers no simple one-hour lead signal. | A real source-timed, size-specific BNB Chain trade with net outcome or risk control that the same user can't already obtain. | Reject as a generic event bot. Keep as an error/session case if another product uses it. |
| Save money by checking a wallet-size quote before signing | The Binance aggregator already ranks routes; [yostocks](https://github.com/yostocks-protocol/yostocks) and [Portir](https://github.com/yeheskieltame/portir) already publish guards; [OneTicker](https://github.com/JemIIahh/oneticker) records size-specific tapes. | A measured route error or cost saving after all fees in the exact same token, side, size and moment. | Retire as standalone. No such measurement exists. |
| Decide whether to take cash from reinvested bStock exposure or leave it compounding | Binance shows the multiplied position and supports manual selling; [Steward](https://github.com/zkasuran/steward-bnb) tracks corporate actions and describes an unsigned payment plan. The measured QQQB multiplier uplift is tiny for a 1,000 USDT holding under a deliberately artificial baseline. | Recover the exact event and eligible wallet position; obtain a real Binance Web3 sell quote; show a meaningful net USDT result and an observed holder's preference. | **Only active falsification test.** Still a niche hypothesis. |

This is a qualitative research ordering, not a scoring exercise or proof of demand. The strongest reason to stop the remaining task is a below-minimum or uneconomic sell quote. The [dated cash-flow note](2026-10-01-dividend-cash-choice.md) gives the calculation and specific gate.

## How Agent Studio could fit without distorting the product

[BNB Agent Studio](https://docs.bnbchain.org/developer-kit/bnbchain-studio/) is a seller-service runtime. It can expose an autonomous, identified corporate-action feed over A2A/MCP/x402; the browser or wallet would remain the user-facing place to decide and sign any mainnet sale. The [hackathon prize](https://www.bnbchain.org/en/hackathons/tokenized-stocks) names identity, runtime and x402 self-funding, not a decorative agent badge.

The proposed service would need to do more than expose `uiMultiplier()`, which is a free read. A valuable output might reconcile an issuer announcement, an on-chain `UIMultiplierUpdated` event, event type, effective time and affected contract, with an explicit confidence state. An agent that buys the artifact could avoid misclassifying a split as income. This is a plausible buyer job, not an observed buyer. The 48-hour managed trial is testnet only. A paid x402 request needs a separate merchant setup; receipt of x402 fees is unrelated to a bStock holder's dividend. No Studio installation, deployment or B402 registration is justified yet.

## Next proof, in order

1. Run the [prepared Dune query](queries/bstock-multiplier-events.sql) manually or use an indexed/archive source for one real multiplier update. The query has not been executed. The [BNB Chain RPC guide](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/) says `eth_getLogs` is disabled on its listed public endpoints, which explains the prior failed attempt. Record event transaction, old/new multiplier, effective time and issuer announcement.
2. With local credentials, make a signed read-only Binance Web3 API request for token context and a sell RFQ at the calculated size. Record the response contract, exact fee and amount fields, time, quote expiry, rejection or minimum. Don't assume the $5 Binance Spot entry minimum applies to the Web3 sell route.
3. Observe an eligible holder attempting the same cash decision through Binance Spot or Agentic Wallet. Ask for the target amount, preferred timing and reaction to the quoted net proceeds. A documented interview or walkthrough is evidence; a presumed persona isn't.
4. If the result survives, write the one-page spec and build a single mainnet spot flow. Then decide whether a paid Studio event feed has a buyer. Keep the founder's DX report as a factual account of these sessions.

The repo must remain private during research and must become public when the founder submits, per the [event rules](https://www.bnbchain.org/en/hackathons/tokenized-stocks). No deployed page, wallet operation or form submission has been made.
