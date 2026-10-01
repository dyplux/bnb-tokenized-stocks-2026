# Off-hours product reset

**Checked:** 2026-10-01  
**Status:** research priority, no approved build  
**Prompt:** the founder rejected blocked-exit recovery because the [event brief](https://www.bnbchain.org/en/hackathons/tokenized-stocks) opens with a cash-market closure and asks what a tokenized-stock product can do while that market is closed.

## The specific job

An eligible person who already has a BNB Chain wallet and stablecoins follows one listed company. That company publishes material public information after the regular US cash session closes. The person wants to know what was published, whether a tokenized representation can be bought or sold **now** for a chosen amount, what the executable quote costs, and how to act within a limit they set. The workflow must also explain a missing route and let the person wait for the next session. This is a hypothesis about a user job, not observed demand.

The [event](https://www.bnbchain.org/en/hackathons/tokenized-stocks) explicitly invites market-hours products, earnings agents and working spot execution on BNB Smart Chain mainnet. It scores technical implementation at 30%, originality at 25%, the team's real Developer Experience Report at 25%, and product UX at 20%. The [SEC submissions API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) publishes company filing history without an API key and says submissions generally appear with a short processing delay. An [8-K Item 2.02 example](https://www.sec.gov/Archives/edgar/data/104169/000010416925000069/0000104169-25-000069-index.htm) links to the company's earnings release as Exhibit 99.1. Filing availability does not prove the first public announcement will reach EDGAR first. The [SEC access policy](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) requires a declared User-Agent and fair request rate.

The Binance [RWA Data API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) can identify the token and market state. The [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) documents stock quote routes. Transaction simulation and wallet execution need separate feasibility checks. `referencePrice` in the RWA documentation is calculated from the token price, so it cannot establish a gap to an independent cash-equity quote. A last cash close, if shown, needs its own sourced timestamp and correct unit. No trading edge or Monday outcome is inferred from a gap.

## One real after-close event to replay

The [SEC Tesla submissions record](https://data.sec.gov/submissions/CIK0001318605.json), read with a declared User-Agent on 2026-10-01, lists an 8-K accepted on **2026-09-29 at 20:38:50 UTC**, which was **16:38:50 New York time**, after the regular cash close. The [filing](https://www.sec.gov/Archives/edgar/data/1318605/000162828026063820/tsla-20260929.htm) reports three credit facilities totaling US$30 billion in commitments and says no loans were outstanding under them as of 29 September. The record is a real source and timestamp for a demo replay. It doesn't tell us whether a trader should buy or sell.

The [dated CMC metadata extract](2026-09-30-tsla-contract-map.json) maps the Tesla name to two BNB Chain contracts: TSLAB `0x5b1910eaad6450e50f816082aa078c41f10c292f` and TSLAon `0x2494b603319d4d9f9715c9f4496d9e0364b59d93`. These are distinct issuer representations. The contracts and current trading status require confirmation against issuer or Binance sources before product use. No historical 20:38 spot quote or executed swap was captured, so the candidate replay proves an event, not an available trading opportunity.

This Tesla event occurred on a Tuesday. [Robinhood's 24 Hour Market](https://robinhood.com/us/en/support/articles/24hour-market/) documents trading from Sunday 20:00 to Friday 20:00 New York time for eligible stocks, so a Tuesday after-close use case is not by itself a unique weekend reason to use tokenized stocks. A stricter user-value test is a Friday 20:00 to Sunday 20:00 New York window, or a documented asset or jurisdiction that the user's existing broker cannot serve. The Tuesday filing is a data-pipeline replay, not the product's demand proof.

## Three off-hours hypotheses

| Hypothesis | User action and possible demo | Best published substitute | Main disproof |
|---|---|---|---|
| A. Public event to bounded spot action | User chooses one company and amount. A cited 8-K or issuer release appears after cash close. The app identifies the linked bStock or Ondo token, obtains an amount-specific quote, simulates it, and prepares a capped buy or sell for explicit approval. If the route fails, the user can wait. | [BNB's own StockAnalyst example](https://github.com/bnb-chain/stockanalyst-agent-demo) handles sourced analysis; [Portir](https://github.com/yeheskieltame/portir) checks news before buying; [PARALLAX](https://github.com/rishu4436/parallax/blob/main/docs/STRATEGIES.md) lists earnings jobs. | Existing entrants already complete the same event-to-executable-order task; primary event data arrives too late; or no route can be simulated or executed. |
| B. Weekend order with a cash-close cap | User sets a price cap on a selected token and sees a live quote while US cash is closed. | [NightDesk](https://github.com/PhiBao/nightdesk) already describes limit-at-reference, alert-at-open and guarded fill; [OneTicker](https://github.com/JemIIahh/oneticker) describes an off-hours tape. | Direct entrant overlap is already strong. |
| C. First stock purchase from fiat while cash is closed | User funds a wallet and buys a tokenized stock in one journey. | [Binance Connect Buy Any Token](https://developers.binance.com/en/docs/products/connect-2.0/buy-any-token/1.buy-any-token) documents a fiat entry flow; [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) already shows stock discovery and swap. | The partner/onramp path may not be available through hackathon credentials, and wallet restrictions may prevent a credible end-to-end demo before 11 October. |

**Ordering:** investigate A first. This is a task-based choice, not a demand score or claim of originality proven across every entrant. B is too close to public entrants. C has a hard integration dependency. A's differentiator would be the trace from a public company event to a real BNB Chain execution decision, with source, quote, simulation and user-controlled cap. A news summary alone would not count.

## A narrow first slice

Use one listed company whose tokenized representation has a documented BNB Chain contract and one verifiable public filing released outside the regular cash session. The user chooses the company, direction and maximum spend. The interface displays the source and publication time, token and issuer, live quote time, amount received, estimated slippage and a simulation result. The user may approve one spot action or decline. The model may summarize the filing and cite exact source text; deterministic code owns token resolution, quote math, caps and order state. No autonomous trade is approved by a model's sentiment. Agent Studio is useful only if a persistent watcher is proven necessary and feasible.

This first slice doesn't promise card onboarding, profit, real-time SEC first publication, or an independent cash reference from Binance `referencePrice`. It also doesn't assume an Ondo or bStock route is open outside cash hours. A quote or simulation failure is a valid outcome only if the application reports it clearly and lets the person decide what to do next.

## Evidence gate before a spec

1. Confirm one company, direct event source, publication timestamp and BNB Chain token contract. Check whether the event reached the source while cash was closed. Find a true weekend example or document why the eligible user's broker alternative remains unavailable.
2. Compare this exact task in StockAnalyst, PARALLAX, Portir and Binance Agentic Wallet. Record which step each actually completes in code or a live demo, separating README claims from observed behavior.
3. With an authorized Binance API key, take one read-only RWA lookup and one size-specific quote during a closed cash session. Capture redacted payload fields, errors, latency and whether transaction simulation is supported. No trade or funds at this gate.
4. Show the proposed result to an eligible person or replay the same task against the incumbent products. If this product adds only a longer news summary or a generic quote screen, reject A.

**Unresolved:** eligible customer behavior, issuer release timeliness, SEC filing delay for the chosen company, Binance API credential scope and quota, live closed-session route, independent cash-close source, wallet approval path and whether a pre-submission mainnet action can be demonstrated safely. The founder's hacker application answer remains open until at least the first technical probe and direct competitor task comparison.
