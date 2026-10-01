# Tokenized-stock trade failure states across wallets

**Checked:** 2026-10-01. **Scope:** published first-party support and API documentation. No wallet session, signed Web3 quote or user interview was performed.

## Published failure states

| User task and source | Published failure or prerequisite | What a BNB Chain product could observe | Counterevidence |
|---|---|---|---|
| Buy an Ondo stock in [MetaMask on BNB Chain](https://support.metamask.io/manage-crypto/trade/real-world-assets/) | Below $5 gets no quote; USDT is the recommended input; BNB gas, market hours and regional eligibility matter. Its guide also says a prior CowSwap stablecoin approval can interfere with an Ondo swap and may need revocation. | Exact asset/amount, public wallet gas and allowance, quote result, documented market status. Eligibility needs a verified method; a wallet address alone isn't enough. | MetaMask already publishes each remedy. Its CowSwap-specific approval interaction hasn't been shown to affect Binance Web3 routes. |
| Swap a token in [Phantom](https://help.phantom.com/articles/36290759987987) | Missing liquidity or a size too large can leave no quote. The help page suggests reducing size, waiting or trying another venue. Its [stock guide](https://help.phantom.com/articles/44063915243283) already explains issuer-specific hours. | A same-asset, same-size quote check on BNB could measure availability. | This is a Solana wallet's support flow; it doesn't measure a BNB stock user's problem or prove our fix is better. |
| Follow a tokenized-stock order in [Blockchain.com](https://support.blockchain.com/hc/en-us/articles/22706829372316-Frequently-Asked-Questions-FAQ) | A CoWSwap order may be pending until matched or expired; weekend quotes may be less favorable. Its FAQ explains where to see the status and what happens to funds. | A route-specific status for an order our app actually initiated. | The FAQ already explains the normal states. Binance Web3 RFQ has a different order and settlement path. |
| Buy from stablecoins with no BNB | MetaMask's guide requires native gas. BNB Chain's [paymaster docs](https://docs.bnbchain.org/bnb-smart-chain/developers/paymaster/overview/) describe sponsored EOA transactions, and say Bitget Wallet already integrates sponsorship. | A gas balance can be read; a specific approval or swap may be eligible only after a paymaster checks its policy. | We have no sponsor account, policy, funded budget or demonstrated compatibility with the Binance Web3 route. Gasless onboarding can't be promised. |

The [Binance Trading API error table](https://web3.binance.com/en/dev-docs/llms-full.txt) separately identifies Ondo market closed `40367`, bStock market closed `40369`, unsupported pairs `40368`/`40370`, no RWA vendor liquidity `40374` and Ondo minimum `40375`. These codes are documentary expectations; [our probe](quote-probe.md) has not received any of them. A `40369` can coexist with Binance's public claim of 24/7 bStock Spot trading because the API route and exchange venue are different. It doesn't prove every on-chain vendor is closed.

## Product consequence

**Inference:** a generic error explainer or gas checklist would restate published wallet guidance and would not give the ordinary holder the economic edge requested by the founder. Keep the distinct codes as honest states in whichever product passes the user-task gate. A focused recovery product would need a witnessed failure that the existing wallet doesn't resolve, an API-supported next action, and a measured improvement in completion or cost. None is available yet.

**Next observation:** in an eligible participant's real workflow, record the exact asset, contract, side, amount, UTC time and existing wallet outcome. Use one permitted signed Binance Web3 quote for the same task. The test can falsify a proposed intervention, but an API error by itself doesn't establish demand or a winning product.
