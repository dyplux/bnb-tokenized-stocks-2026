# Three problem hypotheses, 2026-10-01

**Historical first pass:** H1 was challenged by the founder and is no longer a standalone recommendation. The [later competitor and product reset](2026-10-01-product-brainstorm.md) sets the current research priority. Keep the original hypotheses below as an audit trail, not a current build plan.

These are research candidates, not validated user problems. The [event rules](../01-event-rules.md) require BSC mainnet spot, a central bStocks, Ondo or xStocks asset, and a working Binance Web3 API module. The published API contract and product guides were checked on 2026-10-01. Frequency, user harm and demand have not been measured.

## H1. A decision receipt before choosing a stock token

| Question | Current answer |
|---|---|
| User and trigger | A BNB Chain user has 20, 50 or 100 USDT and wants a particular stock exposure, starting with NVDA. They see bStocks and Ondo representations and must choose one before a spot trade. The user type is a hypothesis, not an observed interview. |
| Observable example | [Binance RWA Data](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) documents platform, contract, ratio and price fields. [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) says its terminal puts issuers side by side and shows price options for a ticker. A documented difference in fields is not proof of a user mistake. |
| Frequency and impact | Unknown. Selecting a different contract could change exposure, rights, size or availability, but no mistake rate or cost has been measured. |
| Current workaround | Read issuer documents, compare PancakeSwap quotes and Binance Agentic Wallet, or keep a spreadsheet of contract, terms and timestamps. A user who has already chosen an issuer can use its direct route. |
| Suspected gap | The same-task incumbent comparison hasn't shown a single pre-confirmation record with contract, ratio, documented rights, quote validity and reason for missing data. This is a test question, not an observed failure. |
| Necessary chain and API work | BSC mainnet identifies the contract and spot route. Binance RWA Data would supply current token context; a Binance Trading RFQ quote would supply an executable offer if the account and asset permit. Without a live quote, the product can only describe the asset, which is too close to existing catalogs. |
| Minimum demo | Enter NVDA and a USDT amount, display both supported representations with sources and times, request a quote without order submission, and issue a dated receipt that clearly marks missing fields or unavailable quotes. |
| Risks | No quote or one issuer in the live response; unsupported rights field; jurisdictional constraints; PancakeSwap or Agentic Wallet already shows the answer; `referencePrice` has [unconfirmed provenance](2026-10-01-reference-price-source-audit.md) and cannot yet provide an independent equity benchmark. |
| Differentiation and possible edge | A reproducible decision record with explicit units, issuer terms, quote validity and missing-data handling. Its possible accumulated value is a history of what was visible at decision time, if someone uses it repeatedly. That edge is unproven and copyable. |
| Strongest counterargument and falsifier | Incumbents already let users choose an issuer and quote. Stop H1 if no tested case changes a defensible choice or prevents an identifiable error, or if the incumbents display the same facts before confirmation. |
| New-user effect | Unknown. A clearer decision may help a first buyer, but the flow still assumes a funded wallet and does not itself prove new users joined BSC. |

## H2. Know whether a stock-token quote is available outside market hours

| Question | Current answer |
|---|---|
| User and trigger | A BSC holder wants to buy or rebalance a bStock or Ondo token when the traditional stock market is closed. |
| Observable example | The [event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) proposes a market-hours monitor. The [Binance Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) documents RFQ for equity/RWA. Neither proves a live quote shortage in our account. |
| Frequency and impact | Unknown until repeated quotes at specified times and sizes are collected. A missing quote can block a task; a displayed token price alone cannot measure executable size. |
| Current workaround | Try the swap or Agentic Wallet when needed, or wait for the underlying session to reopen. |
| Suspected gap | A historical availability view might tell users which issuer and size tends to produce an RFQ at a given hour. No such user request or incumbent gap has been observed. |
| Necessary chain and API work | BSC spot token and a real Binance quote response are essential. A price or market-status feed alone cannot establish execution. Any equity benchmark requires a proven independent source; Binance [`referencePrice` provenance is unresolved](2026-10-01-reference-price-source-audit.md). |
| Minimum demo | Show timestamped quote attempts and status for one token and fixed size across an open-market interval and two closed-market intervals; mark failures and timeouts separately. |
| Risks | Rate limits, unavailable quotes, changes in RFQ eligibility and no material time pattern. Polling can consume quota without helping a user. |
| Differentiation and possible edge | A dated availability record by token and size could improve planning. It loses any edge if the current quote suffices or the availability pattern isn't stable. |
| Strongest counterargument and falsifier | The event itself suggests the monitor, so originality is weak. Stop if the repeated observations show no useful difference or incumbents already explain availability at decision time. |
| New-user effect | Weak without a separate onboarding path. This is more likely to help an existing holder than someone new to BSC. |

## H3. Explain why a first stock-token trade cannot proceed

| Question | Current answer |
|---|---|
| User and trigger | A first-time BSC stock-token buyer reaches contract selection or quote and meets an eligibility, token-state, amount, balance or expired-quote problem. |
| Observable example | [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) already documents status checks, quotes, confirmation and order tracking. The exact errors a person sees in a failed task haven't been observed. |
| Frequency and impact | Unknown. Some failures may waste time or cause abandonment, but no rate or abandonment event has been measured. |
| Current workaround | Read the wallet error, consult support or issuer terms, change amount or route, or wait. Doing nothing can be the safe choice. |
| Suspected gap | A specific error could be detected earlier and linked to a safe next action. This cannot be claimed until an error is actually reproduced. |
| Necessary chain and API work | Binance RWA market state and RFQ responses on BSC could reveal a concrete reason. The product must never infer a user's legal eligibility solely from a token quote. |
| Minimum demo | Reproduce one genuine no-quote or invalid-amount response, show its source and time, explain recovery without asking for a signature, and stop safely when the reason is unknown. |
| Risks | No reproducible errors; ambiguous messages; jurisdictional advice risk; existing wallet already handles the case. Fabricating an error for a demo would invalidate the claim. |
| Differentiation and possible edge | A field-tested taxonomy could make the first trade less confusing. It is easy to copy, and its value depends on observed failures. |
| Strongest counterargument and falsifier | Agentic Wallet may already solve the problem. Stop as a standalone product if the same user can recover there without more steps; keep safe error handling as a requirement of any chosen flow. |
| New-user effect | Potentially the strongest of the three, but unverified. A first-trade interface cannot claim new users joined the chain without a measured first-chain interaction and consented product telemetry. |

## Decision at this gate

Investigate H1 first because it has a concrete same-ticker decision and a short quote-only path. H3 is a safety requirement; H2 waits for a repeated availability signal. This is the [subjective scorecard](idea-scorecard.md) result, not final product approval. A failed H1 test can lead to a new research decision, including building none of these ideas.
