# Decision log

## D-001: keep the BNB project separate from Bell

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted

The new project has its own repository, data and future deployment. Bell remains the CoinMarketCap hackathon entry. The local repository is on the external SSD because the primary drive had about 12 GiB free, while the SSD had about 345 GiB free at the 2026-10-01 check. The repository stays private during research. The [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks), checked 2026-10-01, requires a public repository at submission.

## D-002: keep product selection open until a quote and incumbent comparison

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional

The first two research passes favor a pre-trade check of issuer, contract, market state and quote. [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) already documents ticker resolution and quote confirmation; [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) already has a stock terminal. Both were checked 2026-10-01. The specific user benefit of another layer has not been measured. A live, same-time quote and task comparison can change or reject this direction.

No implementation decision is recorded here. The eventual product choice must name a user, a task, its evidence, the existing workaround and the result that would disprove the proposed advantage.

## D-003: test H1, don't build yet

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research priority

The [weighted scorecard](../research/idea-scorecard.md) orders H1 representation/quote receipt ahead of H2 temporal availability and H3 error recovery. A separate critical review objected that H1 may duplicate PancakeSwap and Agentic Wallet, and that no live Binance RFQ or human problem has been observed. The objection is retained. Test NVDA in bStocks and Ondo at fixed amounts and times; reject H1 if the extra receipt doesn't change a decision or prevent an identifiable error. xStocks is out of the first slice because documented RWA Data coverage is unclear.

The [RWA Data API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data), checked 2026-10-01, defines `referencePrice` as a conversion from on-chain token price. It must not be presented as an independent equity quote. [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) and [PancakeSwap](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) are the incumbent tasks to compare.

The one-line [hacker application draft](../submission/form-answer.md) is a mentor-routing hypothesis, not final product approval. Agent Studio and B402/x402 are deferred until a concrete user task requires them. No dissent was overridden by the score.

## D-004: founder challenges H1's consumer value and Bell overlap

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** H1 and application wording under review

The founder asked why a common user would need a “pre-trade decision receipt” and noted its similarity to Bell. The concern is material. Bell already checks whether tokenized asset representations are comparable; adding a live RFQ and moving the check closer to purchase may still leave the same product idea with another data field. A common buyer wants a clear outcome for a chosen amount, with a safe next action. No observed task shows that a separate receipt reduces time, prevents a mistake or enables a purchase that an existing flow blocks.

The [PancakeSwap stock terminal](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) already presents issuer options and a trade path. [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) documents ticker resolution, quote and confirmation. These published flows strengthen the founder's objection; they don't prove the live UX is complete. The scorecard's 57/100 was a research ordering and didn't measure common-user value.

Hold the [application draft](../submission/form-answer.md). H1 may continue as a falsification test, but it is no longer a recommended standalone consumer product. Resume product selection by observing one ordinary user's actual purchase task and the same task in incumbent flows. If the only added output is a longer explanation, reject H1. Don't rename the idea or add Agent Studio to disguise the overlap.

## D-005: investigate a blocked exit before selecting a product

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** research priority, no build approval

The [dated brainstorm](../research/2026-10-01-product-brainstorm.md) found public hackathon entrants covering issuer comparison and routing ([PARALLAX](https://github.com/rishu4436/parallax), [OneTicker](https://github.com/JemIIahh/oneticker)), consumer buying and selling ([yostocks](https://github.com/yostocks-protocol/yostocks), [Portir](https://github.com/yeheskieltame/portir)), and post-hold/collateral tasks ([Steward](https://github.com/zkasuran/steward-bnb), Portir). Their READMEs establish public claims and some source code, not adoption or independently reproduced outcomes. Another pre-trade receipt is rejected as a standalone direction.

[Ondo's own terms](https://ondo.finance/ondo-stocks) distinguish owning a secondary-market token from eligibility to redeem directly. Its normal direct redemption and secondary trading have different hours and conditions. [yostocks's DX log](https://github.com/yostocks-protocol/yostocks/blob/main/DX_LOG.md) reports an after-hours sell refusal even when a buy quote succeeded, but this has not been reproduced by us. A holder asking whether they can exit a specific position today is a narrower possible job than choosing among wrappers. Research it first. The core dissent is that Ondo, wallets and yostocks may already give the correct next action. A quote failure may also be too rare to warrant an app.

Reject the exit direction if a same-task comparison shows that an incumbent already identifies the cause and action, or if Binance API status and sell quotes cannot support a safe diagnosis. No application answer or build is approved. Keep Agent Studio optional; the extra prize alone isn't a product reason.

## D-006: make the closed-market interval the product research priority

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research priority; supersedes D-005's priority

The founder rejected blocked-exit recovery as too remote from the event's opening problem. The [official brief](https://www.bnbchain.org/en/hackathons/tokenized-stocks) asks for useful actions while tokenized stocks trade and the regular US cash market is closed. The [off-hours reset](../research/2026-10-01-off-hours-reset.md) compares three related jobs. Generic weekend monitors and limit-at-reference orders already have public entrants. The first research test is a public company event after the close, linked to a specific tokenized stock, an amount-specific Binance Web3 API spot quote and a capped user decision.

This is a correction to research direction, not evidence of user demand or implementation approval. A cited filing may not be the first public release; a route may be unavailable outside cash hours; the RWA `referencePrice` is not an independent traditional share quote. The product must work honestly through those states. A source summary or a generic quote is insufficient. No autonomous investment decision is authorized. D-005 remains as a documented rejected research priority and may become an error state inside another product if observed.

## D-007: test access and net execution before claiming an economic edge

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research gate; extends D-006

The founder wants a product that gives an eligible user a real economic advantage and asks whether BNB Agent Studio helps. The [economic edge and Agent Studio map](../research/2026-10-01-economic-edge-and-agent-studio.md) separates a documented closed-hours access window from a measured price or profit advantage. [Robinhood](https://robinhood.com/us/en/support/articles/investing-on-weekends/) says eligible stock trading runs Sunday 20:00 through Friday 20:00 ET; [Binance](https://www.binance.com/en-NG/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38) describes 24/7 bStocks secondary trading for eligible users. The strongest distinct window is Friday 20:00 to Sunday 20:00 ET, provided an actual BNB Chain quote and the user's eligibility are confirmed.

[Binance Research](https://www.binance.com/en/research/analysis/stock-price-discovery-moves-on-chain) reports that a median 92% of the Monday price gap was already reflected in bStocks over seven weekends to 2026-07-28. This is sponsor research and not a reproduced trader return. It argues against advertising a simple weekend arbitrage. The app must compare amount-specific executable quotes and all-in costs before claiming price advantage.

The [current Agent Studio quickstart](https://docs.bnbchain.org/developer-kit/bnbchain-studio/quickstart/) supports a paid seller agent and a managed 48-hour testnet trial. The [Binance Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) binds RWA quotes to the signing wallet and an approximately 30-second quote ID. A paid event-to-quote service is only a technical option until it proves it can return a still-valid quote and improves a task that NightDesk's published seller does not already solve. Do not add Studio for a prize badge. Mainnet spot execution remains a separate product path. No build or application-answer change is approved by this decision.

**Additional counterevidence, checked the same day:** the [Binance Agentic Wallet stock guide](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) publishes examples of persistent earnings-reaction and news-driven trading rules. It says off-chain data requires an added source or Skill. We have not run these examples, but a plain event-to-order agent would overlap the official product on paper. The same-task review must find a measurable missing input, cost or route outcome before this candidate can enter build.

## D-008: shift the weekend trigger test from SEC filings to BTC-linked equity

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research priority; supersedes D-006's SEC-weekend trigger

The [SEC operating-hours guide](https://www.sec.gov/submit-filings/filer-support-resources/how-do-i-guides/understand-edgar-its-three-websites) says EDGAR is closed on weekends. That defeats a normal weekend service driven by new SEC filings. The [weekend research note](../research/2026-10-01-weekend-crypto-equity-task.md) measures ten Binance Spot windows: MSTRB and BTC moved in the same direction in eight, with a 0.883 correlation of 48-hour returns. [Strategy's own description](https://www.strategy.com/strategy) makes the economic link intelligible. A public pair index showed substantially more MSTRB/USDT BNB Chain liquidity than COINB/USDT at one timestamp. Neither measure proves a Binance Web3 quote or net edge.

Research priority: test an eligible holder's BTC-move-to-MSTRB action during Friday 20:00 to Sunday 20:00 ET. The user must see what MSTRB has already priced, a fresh amount-specific BNB Chain quote and full costs before a bounded decision. A BTC alert or price chart alone overlaps the Binance Agentic Wallet's documented automation. Reject if the official tool already completes the same job with equivalent clarity, the RFQ is unavailable or too costly, or no eligible user wants separate Strategy equity exposure. Agent Studio remains a conditional paid analysis surface with a real buyer; it cannot be the user's mainnet signing wallet or sell an expiring RFQ as a durable report.

**Frequency check:** the same ten-weekend hourly sample crossed 2% away from Friday's BTC opening price once and 3% zero times. A product predicated on a dramatic weekend BTC shock is therefore a weak standalone bet on current evidence. The task remains a falsification test, not a product selection.

## D-009: test wallet-size execution quality, not a weekend alpha claim

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research gate; narrows D-008

The [execution research note](../research/2026-10-01-session-aware-execution.md) combines three pieces of counterevidence. [Binance already offers eligible users 24/7 bStocks Spot trading](https://www.binance.com/en/academy/articles/what-are-bstocks-a-guide-to-tokenized-stocks-on-binance) and [Spot bots](https://www.binance.com/en/support/announcement/detail/ae96da838d754f91bced1501de728f03). Our ten-weekend sample finds little one-hour BTC lead over MSTRB. [yostocks source](https://github.com/yostocks-protocol/yostocks/blob/main/apps/agent/yo.mjs) already quotes, selects a route and applies a 1% reference guard. Consequently, generic closed-hours access, BTC-trigger automation and a simple price guard are not sufficient product advantages.

The remaining test is for an **eligible self-custody user with BNB Chain funds**: can a fresh, same-MSTRB, same-side, size-aware comparison expose a materially poor on-chain execution route or a missing-risk state before the user signs? A centralized Spot book is only an indicative benchmark for this user, not an executable BNB alternative. The [Web3 RFQ](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) is wallet-bound and short-lived. The initial public Spot/DEX snapshot doesn't prove a profitable spread or even an amount-specific route. Do not select or build this product until a signed Web3 quote and an incumbent task comparison show a practical difference. Do not describe bypassing bStock location restrictions as onboarding. Agent Studio remains conditional on a separately useful paid analysis job.

## D-010: retire the generic quote guard and test a dividend cash-flow choice

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** provisional research priority, no build approval; supersedes D-009's priority

The [cash-flow research note](../research/2026-10-01-dividend-cash-choice.md) records the latest direct competitor review. [yostocks](https://github.com/yostocks-protocol/yostocks), [Portir](https://github.com/yeheskieltame/portir) and [NightDesk](https://github.com/PhiBao/nightdesk) already publish wallet quote guards or session-aware trading flows. [OneTicker](https://github.com/JemIIahh/oneticker) publishes size-specific quote tapes. We haven't run these products end to end, but the overlap is sufficient to stop treating a generic guard or tape as a distinct build target.

[Binance's bStocks FAQ](https://www.binance.com/en-AE/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38) says dividends are reinvested into exposure through a multiplier and don't arrive as cash. Its [September announcement](https://www.binance.com/en/support/announcement/detail/7df43402f0094e79b293bd7fbb574474) describes actual dividend processing for QQQB, METAB, AVGOB and STXB. At 13:31 UTC, the public Binance list showed QQQB multiplier `1.000724838657573033`; a read-only chain call at 13:32 UTC matched it. This is a current multiplier, not a reconstructed dividend event or a user's entitlement.

The provisional user task is to convert a **verified increment of existing bStock exposure** into USDT only when a wallet-bound sell quote clears a user-defined net proceeds floor. This would give a cash-flow choice, not extra yield or arbitrage. The objection is severe: under the artificial assumption of an initial multiplier of exactly 1, a current 1,000 USDT QQQB position has only about 0.7243 USDT of cumulative multiplier-related exposure. The actual sell minimum and costs are unknown, and the previous event multiplier hasn't been recovered. The target user may need a much larger position or a longer accumulation period. An eligible holder may already sell manually through Binance or Agentic Wallet.

Build remains blocked until an actual event, wallet position, signed read-only Binance Web3 API sell RFQ, minimum and net proceeds have been measured. A consenting eligible holder must confirm this is a task they would use. Reject the idea if the amounts are too small, if entitlement can't be proved safely, or if an incumbent already supports the same cost-aware action. Agent Studio has a plausible event-feed seller role but no buyer; it remains outside the first slice. The founder's earlier request to research before coding is preserved.

## D-011: stop treating dividend cash-out as the leading consumer product

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted research correction; no product approved

The [access and event-index check](../research/2026-10-01-access-and-event-index-check.md) strengthens the case against D-010's ordinary-holder fit. QQQB's illustrative multiplier increment on a 1,000 USDT holding is about 0.7243 USDT before costs under an artificial acquisition assumption. SQQQB's larger illustration belongs to a daily -3x inverse ETF with a poor long-hold fit. Public indexer pagination didn't recover the September multiplier event. Ondo already documents direct 24/7 mint and redemption for six assets, with eligibility conditions, so weekend access by itself isn't novel. A holder may be able to sell a fraction manually in an existing venue.

Retire dividend cash-out as the active product recommendation. Keep the Dune event query as research infrastructure, not a reason to ship a dividend app. There is now **no selected product**. The next bounded decision is a same-task comparison for an eligible small BNB Chain wallet: find one concrete occasion when its desired stock action is unavailable, materially costly or unclear in an incumbent flow; request one signed read-only Web3 quote for the same asset, side and size; record the action and net result the proposed product would change. A quote alone doesn't pass this gate. If no such task appears, stop rather than repackage a generic guard as an edge. Agent Studio remains a separate technical prize opportunity only when a useful paid autonomous job is identified.

## D-012: withdraw the categorical reference-price provenance claim

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted source correction; does not approve a product

The [official-source audit](../research/2026-10-01-reference-price-source-audit.md) found that Binance's RWA API labels `referencePrice` an underlying reference, while its Wallet Skills guide gives a formula based on token price and share multiplier. The RWA example values don't satisfy that formula. D-003 and several early research notes said the field was definitively derived from the token price; that provenance claim is withdrawn. The reverse claim, that it is a fresh independent share quote, is also unsupported. Until Binance supplies the upstream source and as-of time, product copy may only call it an unverified reference field. No premium, discount or trading-edge calculation may use it as an independent equity benchmark.

## D-013: keep trade-error diagnosis as a product state, not the main idea

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted research filter; no product approved

The [wallet failure-state audit](../research/2026-10-01-stock-trade-failure-audit.md) found documented remedies for minimum amount, wrong stablecoin, gas, market hours, thin liquidity and pending orders in MetaMask, Phantom and Blockchain.com. Binance's Trading API also publishes specific RWA quote error codes. These are useful for clear recovery states, but the documentation doesn't show an unmet task or an economic improvement from another generic explainer. A gasless first purchase would require a paymaster sponsor and route compatibility that this project doesn't have. Keep these states in a future product only where a real participant and quote reveal a gap. Continue the small-wallet same-task gate from D-011; do not approve an error dashboard as a substitute for it.

## D-014: a liquid-pool size alert is a weak consumer hook

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted research filter; no product approved

The [fixed-block NVDAB pool quote](../research/2026-10-01-nvdab-sized-pool-quote.md) measured 25, 100, 500 and 2,000 USDT inputs against the same PancakeSwap V3 pool at BNB block 125141674. Independent read-only buy and reverse sell quotes differed by 0.499416% to 0.502656% before gas and transaction execution. The pool charges 0.25% per direction; the percentage difference between the smallest and largest cases was only about 0.324 basis points. This one pool doesn't establish a general market result, but it weakens the proposed consumer story that sizing an ordinary NVDAB purchase creates a large hidden execution penalty.

Do not build a generic price-impact alert from this result. The next gate remains a real eligible person's task and a same-time signed Binance Web3 quote, with an incumbent comparison. A smaller pool or another route may behave differently; such a case needs evidence that the user could actually encounter and act on it. The on-chain Quoter call is not the hackathon Web3 integration.

## D-015: do not promote Venus collateral monitoring without an observed divergence

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted research filter; no product approved

The [Venus bStock oracle check](../research/2026-10-01-venus-bstock-oracle-check.md) found about $658,016 of indexed supply across four bStock collateral markets and 101 market supplier records, not necessarily distinct users. Venus documents a Protection Mode that can make borrow-power and liquidation prices differ. At BNB block 125144831, the live configuration enabled bounded pricing for all four, but Protection Mode was inactive and the bounded prices equalled spot. No affected borrower or missed incumbent warning was observed.

Keep the oracle distinction as a possible future state, but do not build a general collateral agent or paid Agent Studio monitor from a dormant state. A build would require an active divergence or a consenting borrower's task, a safe action that changes as a result, and the mandatory Binance Web3 API integration serving that task. This check supplies none of those gates.

## D-016: reject a simple weekend-direction trading claim

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** accepted research filter; no product approved

The [public Spot weekend screen](../research/2026-10-01-weekend-reopen-screen.md) compared eleven ordinary weekends for each of five bStocks between July and September 2026. Of 55 asset-weekend observations, weekend and Monday 13:00-to-14:00 UTC directions matched 28 times, differed 26 times and were flat once. Per-asset Pearson correlations were small and mixed. The five assets share dates, and this CEX sample has no BNB Chain quote, fees or actual fills.

Do not pitch a generic weekend-momentum or weekend-reversal agent as an economic edge. A later event-specific strategy would need a fixed trigger, separate evaluation sample and executable net outcome, plus a reason the existing Binance Spot bots or Agentic Wallet don't provide the same task. The next product gate remains an observed eligible user's action and a signed Web3 API response.

## D-017: select a provisional sell-or-borrow cash decision

**Date:** 2026-10-01
**Owner:** Dyplux
**Status:** approved for one read-only vertical slice; no market launch or economic claim

The founder asked for a useful financial decision rather than another Bell-style comparability receipt. An eligible holder of a bStock on BNB Chain who needs USDT can sell part of the token or supply it as Venus collateral and borrow. Those actions leave different stock exposure, debt and liquidation risk. The [Venus observation](../research/2026-10-01-venus-bstock-oracle-check.md) found four live bStock collateral markets with about $658,016 of indexed supply and 101 market supplier records on 1 October; this is use of the markets, not proof of demand for a comparison. Venus documents that borrowing accrues interest and can lead to liquidation. At 19:12 UTC, its public market API showed a 5.0119% variable vUSDT borrow APY; this is a dated snapshot, not a future rate. See the [spec](../product/one-page-spec.md).

The [Steward Swipe code](https://github.com/zkasuran/steward-bnb/blob/a1ae5cf4153e370d16ef9dd1cd85cb116f0412ba/apps/web/app/api/use/swipe/route.ts) calculates a bStock-backed borrow from live Venus state; its inspected endpoint doesn't request a sell quote. [Portir's loan page](https://github.com/yeheskieltame/portir/blob/761f0df0e04d9fa46f0007cf69c9558ecd434161/apps/web/app/loans/page.tsx) supports a testnet lending flow and displays mainnet Venus markets, while its separate [buy route](https://github.com/yeheskieltame/portir/blob/761f0df0e04d9fa46f0007cf69c9558ecd434161/apps/web/app/api/buy/route.ts) isn't a same-cash-goal sell comparison. We read these paths, not every possible screen, and didn't run either app. The narrow gap is a side-by-side choice for one cash need using a real Binance Web3 sell quote and account-aware Venus risk, with both sources and times visible. A borrow-only card or quote-only guard would duplicate competitors.

**CEO decision:** one bounded implementation may begin from the spec while the complete Web3 secret is being recovered. The absence of a live signed response is a hard gate for calling the result functional, publishing it or submitting it. The absence of a consenting eligible holder's task remains a gate for claiming useful demand. If the signed sell quote is unavailable, fee units cannot be reconciled, or the same-cash-goal comparison doesn't change a defensible choice against the incumbents, retire the product. Do not add Agent Studio without an autonomous job and buyer. The sample may illustrate mechanics with live public data, but it must never impersonate a wallet position or an executed loan.

## D-018: keep D-017 conditional after same-block competitor review

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** provisional, no release approval

A [read-only product critique](../agent-reports/product-review/2026-10-02-d017-rubric-gate.md) found that D-017 could still be two familiar workflows placed side by side for an unobserved audience. It has no signed Binance Web3 quote, personal Venus risk result or holder session. The coordinator accepts that objection and does not call the candidate the strongest submission yet.

The later [same-block Steward check](../research/2026-10-02-steward-supply-cap-comparison.md) supplies one concrete contrast: Steward's live Swipe output labelled a 25 NVDAB, HF 2 scenario “FUNDABLE NOW” at BNB block 125201341 without showing that the Core NVDAB market had only 20.039492377880186433 NVDAB of remaining supply-cap room at that block. Our read-only scenario flags that entered amount. This is a disclosed precondition difference for one case; it is not proof that all of the competitor's borrowing outputs are wrong, or that our combined cash-choice product changes a real action.

**CEO decision:** continue D-017 only through its existing signed-quote and eligible-holder gates. Keep the cap check visible, but do not add a broad competitor attack or claim that a 100 USDT loan is impossible when fewer NVDAB units might be supplied. Reassess this provisional choice after one same-task participant observation and a permitted signed Binance response, or at the 4 October checkpoint if either remains missing. A safe, working sale-versus-loan comparison must determine the final product direction; the cap example alone does not.

## D-019: restrict the NVDAB onboarding claim after the cap screen

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** applies to the provisional D-017 slice; no new product approved

The [fixed-block screen](../research/2026-10-02-bstock-collateral-cap-screen.md) found only `11.416397078470495107 NVDAB` of Core supply-cap headroom at 07:11 UTC, `0.7611%` of the cap. The three other listed bStock collateral markets had more room at that block, but their wallet-sized Binance Web3 sell routes and same-task users haven't been checked. The Venus `supplierCount` fields and CMC's NVDAB holder display don't measure a shared eligible user population.

**CEO decision:** keep NVDAB as a controlled test case for one cash target, with its cap limitation visible. Don't describe this slice as broad borrower onboarding or count all NVDAB holders as addressable borrowers. Don't switch the active build to another bStock solely because its cap has more room. At the 4 October checkpoint, reject the NVDAB version if the cap has closed or the signed quote and holder-task evidence remain unavailable; compare any replacement against the same user task, integration and risk gates before authorizing code.

## D-020: technical Binance quote passes, holder cash decision remains open

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** continue bounded D-017 validation; no release approval

The [first live signed quote](../research/2026-10-02-first-live-binance-quote.md) returned one LiquidMesh `SWAP` route for a 1 NVDAB to USDT request, with HTTP 200 and business code 0. A second technical read returned estimated output and fee fields. The app checked exact token identity and on-chain decimals before the first quote. The request used a temporary nonholder address, so no signer, balance, eligibility, order, fill or real cash need was observed. The [Trading API endpoint reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says RWA always uses RFQ, while the [introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) allows bStock SWAP. The live route matches the latter and leaves execution semantics for review.

**CEO decision:** the missing-key blocker is closed for signed RWA search and technical quote reads. Show the validated output only as a short-lived estimate in the separate Sale check; keep the main sale card unquoted and no net-proceeds or borrow recommendation. The argument against D-017 remains material: a quote and a Venus market scenario may still be two existing workflows beside one another. The next decisive evidence is one consenting eligible holder's same cash task, a holder-sized fresh quote, account-wide Venus risk and an incumbent comparison. At the 4 October checkpoint, keep or retire the candidate against those gates. Do not add Agent Studio or claim a winning product from this technical success.

The later [near-time route control](../research/2026-10-02-live-route-control.md) found a 20.8697-basis-point arithmetic difference between one Binance quote and one isolated PancakeSwap pool quote for 1 NVDAB. A subsequent Binance response named Elfomofi as its LiquidMesh route segment, and the estimate had already changed. This is evidence that route selection can matter, not a measured user saving or proof that our app improves an incumbent. It does not alter the holder and account-risk gates above.

## D-021: show current Core states without forecasting a new loan

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** bounded read-only notice accepted; no release approval

The [Venus source review](../research/2026-10-02-account-wide-risk-feasibility.md) identified separate current aggregate borrowing-power and liquidation-threshold reads. The [runtime check](../research/2026-10-02-current-core-risk-runtime.md) confirmed the deployed empty/default response and the browser display, but did not observe a consenting holder or populated risk position.

**CEO decision:** expose only current cushion, shortfall or zero labels in the optional Core panel, tied to one BNB block. Do not convert raw values to undocumented USD amounts or imply a health factor, safe deposit, executable borrowing capacity or liquidation price. Keep the market-level scenario and sell estimate separate. The 4 October checkpoint and holder, cost and incumbent gates in D-017 and D-020 remain open.

## D-022: unsigned LiquidMesh transaction build passes one technical path

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** technical construction verified; no holder sale or release approval

The bounded [read-only build](../research/2026-10-02-first-live-swap-build.md) took one fresh 1 NVDAB LiquidMesh `SWAP` quote into `GET /swap`. Both signed GET requests returned HTTP 200/business code 0. The response contained an unsigned `tx` with the temporary sender, nonempty calldata, a 450000 gas limit, a separate gas price and a minimum receive amount. In this route, the quote's `estimateGasFee=450000` matched the built transaction's gas limit; it was not a paid wei fee. The address had no known holdings, allowance or signer, and no simulation or broadcast occurred.

**CEO decision:** mark the SWAP transaction-construction path observed for one technical request. Keep the main sale card Unquoted and the separate quote indicative. A constructed transaction cannot establish net proceeds, a fill, eligibility or the holder's cash choice. The holder task, allowance, execution-cost interpretation, account-wide Venus risk and incumbent comparison remain the release gates. The 4 October D-017 checkpoint stays in force.

## D-023: quote a candidate partial sale against the cash target

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** approved for one read-only implementation slice; no release approval

The current interface compares a quote for every typed NVDAB unit with a loan for the entered USDT cash target. For a 1 NVDAB holding and a 100 USDT need, that can put a roughly 234 USDT sale beside a 100 USDT loan. The [fractional technical quote](../research/2026-10-02-fractional-target-quote.md) returned an estimated 100.663406831290082054 USDT for 0.43 NVDAB at 22:08 UTC, before final costs. The [Binance quote reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) only accepts a sell-token input amount; it has no exact-output cash-target parameter.

**CEO decision:** treat typed NVDAB units as the amount available for the collateral scenario. A bounded read-only quote flow may use one fresh quote to estimate a candidate fraction to sell for the same USDT target, then quote that fraction once. Show the candidate units, final estimated output, target gap and both response times. If there is no first route, no second route, or the estimate remains below target, report that state and stop. At most two Trading API quote calls may follow one identity check per click. Do not show a guaranteed cash amount, net proceeds or a recommendation. The holder, costs, account-risk and incumbent gates remain unchanged. If the extra quote calls cannot be bounded and explained in the DX report, stop this implementation.

## D-024: put the two token amounts beside one cash target

**Date:** 2026-10-02
**Owner:** Dyplux
**Status:** approved for a small local display slice; no release approval

The [target-sized live browser path](../dx/field-log.md) returned a 0.427027364860048582 NVDAB candidate for a 100 USDT target, while the Venus market result puts its isolated collateral-only minimum inside the longer borrow card. A reviewer has to connect those amounts manually. The two readings have separate source times and different risk meanings.

**CEO decision:** show one compact same-target line only when a current Venus scenario and a current Binance candidate quote match the same typed inputs. Call the sell amount an estimate before costs and the borrow amount an isolated minimum without a safety buffer. Hide the line on a shortfall, error, changed input or expired quote. [The spec](../product/same-cash-amounts-spec.md) defines those states. This doesn't change D-017's holder, personal-risk, cost or incumbent gates.

## D-025: show the quoted network fee without inventing net proceeds

**Date:** 2026-10-02 UTC (2026-10-03 Lisbon)
**Owner:** Dyplux
**Status:** bounded local display slice completed; no release approval

The [Binance Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api), checked 2026-10-02 UTC, describes `tradeFee` as an estimated network fee in USD and allows null. The live NVDAB quote had a value, but the app discarded it. Neither that field nor the unsigned build establishes whether an ERC-20 approval or other execution costs are included.

**CEO decision:** retain a validated nonnegative decimal fee estimate from the final target-sized route and display it beside the estimated USDT output. Null or malformed values become Unavailable. Never subtract it from the token output, call the result net proceeds or treat the fee as paid. Clear it on input changes, request errors and expiry. This improves cost visibility without changing the D-017 holder and personal-risk gates. The [Plus Sol checkpoint review](../agent-reports/product-review/2026-10-03-checkpoint-review.md) still finds usefulness unproved.


## D-026: show only a conditional remaining balance

**Date:** 2026-10-02 UTC (2026-10-03 Lisbon)
**Owner:** Dyplux
**Status:** bounded UI slice completed; no release approval

The [D-017 spec](../product/one-page-spec.md) asks for remaining token units beside a partial sale. The existing optional BNB Chain balance read and Binance candidate quote can support exact arithmetic, but neither proves that a sale executes. The [slice](../product/remaining-units-slice.md) shows the remainder only for a matching wallet, matching inputs, a recent balance block and local receipt, and an unexpired target-reaching quote. It shows an insufficiency warning instead of a negative remainder.

**CEO decision:** keep the result in the separate Sale check, explicitly conditional, with the balance block. The main Sell card remains Unquoted. Synthetic Chrome QA at 320 and 1440 CSS pixels and 35 local tests passed; no holder or live quote was used for this increment. The 4 October product checkpoint and all holder, fee and personal-risk gates remain open.

## D-027: after-hours route availability is observed once

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** one technical uncertainty narrowed; no release approval

The [pre-registered probe](../research/2026-10-03-weekend-quote-protocol.md) made one signed, read-only request at 00:02 UTC on Saturday, 20:02 Friday in New York, after Nasdaq's published late-session end. The [result](../research/2026-10-03-after-friday-close-quote.md) was HTTP 200/business code 0, with one LiquidMesh SWAP estimate for 1 NVDAB. Its estimated output was 234.581506161816758656 USDT before final costs. A temporary nonholder address supplied the API's required wallet field. No wallet signed or traded.

**CEO decision:** count this as one positive technical quote-availability observation after the published Friday late session. Don't call it proof of executable weekend access, a price edge or a better cash choice. Preserve the 4 October D-017 checkpoint. The consenting holder, existing-venue, final-cost and personal Venus-risk gates still decide whether to keep, redesign or retire the product.

## D-028: measure quote display time from the local request

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** bounded freshness fix completed; no release approval

The [Binance Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes a roughly 30-second `quoteId` TTL. The app's earlier 20-second UI timer began only after the server had finished identity, RPC and quote calls. A slow request could therefore display an estimate beyond that vendor window.

**CEO decision:** start the conservative 20-second display window when the browser sends the local request. Expire a slower response as soon as it arrives. The [slice](../product/quote-age-slice.md) passed synthetic delayed-response checks and 35 local tests without a live API call. This closes one stale-display path; it doesn't change the D-017 holder, executable cost or personal risk gates.

## D-029: show a guarded sale estimate in the main comparison

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** bounded interface slice completed; product gate open

The [clean local browser path](../research/2026-10-03-clean-local-path-result.md) returned a target-sized estimate, but the main Sell card still said Unquoted. A [Plus Sol product review](../agent-reports/product-review/2026-10-03-clean-path-gate.md) identified this as a misleading first impression. No holder, net proceeds or personal post-deposit risk was observed.

**CEO decision:** supersede D-026's main-card display restriction for a current, input-matched, target-reaching quote and Venus scenario. Show the estimate beside the borrow illustration, labelled before costs. If a fresh matching public balance is below the candidate, suppress the main-card amount and show insufficiency. Mark absent or stale balance unverified. Expire and clear on input change or failure. The [slice](../product/sale-card-clarity-slice.md) passed synthetic browser states and 35 local tests. This improves legibility only; D-017's holder, cost, personal-risk and incumbent gates remain open.

## D-030: gate account-specific post-action risk on deployed parity

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** research gate open; no personal forecast approved

The [Plus Sol review](../agent-reports/product-review/2026-10-03-venus-post-action-gate.md) checked Venus's current aggregate risk methods against its source and E-Mode documentation. The public hypothetical method has no new-supply parameter. A local estimate of post-supply and post-borrow net cushions is possible in principle only with same-block account state, effective factors, both oracle paths, exact vToken rounding and protocol gates. The deployed source and a populated-account parity case are still unverified.

**CEO decision:** keep the existing current-state notice and isolated market illustration. Do not show a personal health factor, liquidation price or safe borrowing amount. Permit a bounded read-only provenance and parity study; add a conditional net-cushion result only after it reproduces deployed behavior and can be explained to an eligible holder. If those gates remain open at the 4 October checkpoint, narrow or retire the cash-choice claim under D-017.

**2026-10-03 source update:** the [Venus source trail](../research/2026-10-03-venus-current-facet-boundary.md) identifies the exact live facet address in official documentation, VIP-640 and the deployment list, with v10.3.0 as its linked source. Compiler-level bytecode equality and populated-account arithmetic remain unverified. This narrows the provenance uncertainty but does not change the decision.

## D-031: keep same-cash differentiation as a testable gap

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** provisional until the 4 October product checkpoint

The [same-cash incumbent check](../agent-reports/product-review/2026-10-03-same-cash-incumbents.md) inspected Steward's Swipe route, Portir's buy route, Venus guides and Binance Agentic Wallet's market-order reference. The inspected sources don't show one guided target-sized sale versus borrow comparison. Steward already covers much of the borrow task, and Binance Agentic Wallet covers sale quotes. No competitor or holder workflow was exercised end to end.

**CEO decision:** treat the remaining gap as a hypothesis, not a product advantage. Keep D-017 only through the 4 October checkpoint. Don't broaden scope because a feature is absent from a README. Require a consenting holder's same-cash task, defensible cost interpretation and account-specific risk boundary before claiming an actionable comparison. Narrow or retire the cash-choice claim if those gates cannot be met.

## D-032: keep the judge demo local until quota controls exist

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** public deployment blocked; one reusable hardening slice accepted

The [public-demo review](../agent-reports/product-review/2026-10-03-public-demo-gate.md) found that localhost-only routing prevents a public browser path and that the signed Binance quote endpoint has no abuse budget or concurrency bound. Edge rate limits alone wouldn't stop distributed quota use. A small local code slice now bounds and validates public Venus and BNB RPC responses and refuses redirects, with 37 Python 3.9 unit tests passing and one successful public-read smoke check.

**CEO decision:** keep the app bound to loopback and the repository private. Implement public-host routing, server-side quota controls and process supervision only if the 4 October product checkpoint keeps this task. Do not expose the current server through a tunnel or place Binance credentials into a public process yet. The founder's specific authorization is required for deployment, DNS, repo publication and submission.

**2026-10-03 implementation update:** the process now enforces a small quote budget and accepts an explicitly configured HTTPS Host and matching Origin for a future reverse proxy. This preparation happened before the checkpoint because it doesn't expose the server, change the product or consume an API call. The process remains bound to loopback and no public origin is configured by default. Public deployment, process supervision, edge controls and the product decision remain blocked. The local Python 3.9 suite passed 49 tests.

**2026-10-03 GET error correction:** `/api/scenario` now sends only the stable 502 service message when a Venus read fails, without raw exception detail. A synthetic secret-marker regression and the full 50-test Python 3.9 suite passed locally. This is a disclosure fix, not a change to D-017 or permission to deploy.

## D-033: record the product stop recommendation before the checkpoint

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** D-017 provisional until 2026-10-04 12:00 UTC

The [Plus Sol stop review](../agent-reports/product-review/2026-10-03-d017-stop-review.md) recommends retiring D-017 because the current app can't establish a holder's safe cash choice, and recommends revisiting exit recovery. The strongest counterargument is the observed signed quote path and a same-cash display that inspected incumbents don't show. The fallback also lacks an observed holder task.

**CEO decision:** hold the final keep/retire judgment until the dated checkpoint, while making no further D-017 product feature changes beforehand. Require an observed consenting holder task, defensible sale-cost treatment and an account-specific risk boundary to keep the cash-choice claim. If those gates fail, retire that claim. The reviewer's exit-recovery fallback is not selected: the founder rejected it as the main direction, and no new holder evidence changes that. This records the reviewer's recommendation and the coordinator's narrower timing judgment without artificial consensus.

## D-034: keep the cash target conditional on transaction minimum

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** safety wording corrected; no new sale feature approved

The [same-cash technical check](../research/2026-10-03-target-minimum-check.md) made one signed identity search, two signed quotes and one unsigned `/swap` build. For a 100 USDT target, the candidate's quote estimated 100.000443760010104468 USDT, while its 0.5% slippage minimum was 99.500441541210053945 USDT. The request used a nonholder address and did not sign, simulate or broadcast.

**CEO decision:** keep the app's existing quote comparison explicitly labelled **before costs** and add a visible warning that the built minimum can be below the target. Do not treat a target-sized estimate as guaranteed cash or implement an automatic slippage buffer before the D-017 checkpoint. A future actionable target verdict needs a fresh built minimum, explicit slippage choice, allowance and cost treatment, and a holder task. This finding strengthens the existing cost gate; it does not select a different product.

## D-035: nonempty Core state narrows ABI uncertainty only

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** technical observation; D-030 and D-033 unchanged

A [bounded public read](../research/2026-10-03-populated-core-account-read.md) found one governance account with five entered Venus Core markets. At block 125402171, the deployed Core returned error 0, positive liquidity and no shortfall for both current risk selectors; the app displayed `cushion` for both. The account's NVDAB balance was zero. The address was not retained.

**CEO decision:** treat this as evidence for the nonempty ABI and current-state label path, not for source arithmetic parity or a bStock holder task. Keep the proposed post-action account forecast out of the UI. The 4 October cash-choice checkpoint still requires a consenting holder, defensible sale costs and a personal-risk boundary.

**2026-10-03 source correction:** the [bounded parity review](../agent-reports/product-review/2026-10-03-venus-parity-source-correction.md) found that the v10.3.0 Lens adds `vaiController.getVAIRepayAmount(account)`, not the raw `mintedVAIs(account)` proposed in an earlier Plus Sol draft. The latter can omit accrued interest. No such local calculation was implemented. Exact parity remains open; D-030 and D-033 stay unchanged.

**2026-10-03 bounded parity update:** a [reproducible read-only probe](../research/2026-10-03-venus-core-bounded-arithmetic-parity.md) exactly matched both deployed current-risk tuples for one nonempty Core account at block 125405244. The account used pool 0, one active market and zero VAI repayment, so E-Mode, nonzero VAI and post-action cases remain open. This narrows the arithmetic uncertainty but doesn't approve a personal forecast or change the 4 October product gate.

## D-036: narrow the differentiation claim after live Steward use

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** read-only competitor evidence; D-033 unchanged

The [live Steward Swipe check](../research/2026-10-03-steward-live-swipe-same-task.md) exercised its public `Use` flow with 1 NVDAB. It displayed $82.09 fundable at target HF 2.0 and $102.62 at HF 1.6, at BNB blocks 125408210 and 125408215. The latter exceeds the 100 USDT illustrative cash need. The observed flow did not ask for a cash target or show a matched sale quote. No wallet was connected, and its $0 existing debt was a default scenario.

**CEO decision:** treat Steward as a working borrow-side substitute, not only a code-level overlap. Keep the same-cash sale comparison as an unproven difference that must matter to a consenting holder. Make no D-017 product feature change before the 4 October 12:00 UTC checkpoint. D-031's source-only note remains historical; this live observation supersedes its statement that no competitor runtime task had been exercised.

**2026-10-03 source update:** verified Binance accounts also announced a [bStocks DeFi Center](../research/2026-10-03-binance-bstocks-defi-substitute.md) with lending and borrowing access. This adds a first-party discovery route to the incumbent set. The sources don't show a completed NVDAB loan or same-cash sale comparison, so they don't prove full task equivalence. D-033's checkpoint and the need for a holder walkthrough remain unchanged.

## D-037: account overlap confirms use of collateral and debt, not a cash task

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** read-only evidence; D-033 unchanged

The [bounded probe](../research/2026-10-03-nvdab-holder-debt-overlap.md) used one signed Binance holder ranking and one pinned BNB block. Among the first 15 of 48 ranked vNVDAB holders, nine had entered vNVDAB as Core collateral and had positive stored vUSDT debt. All nine had other entered markets; eight were EOAs and one was a contract.

**CEO decision:** treat this as evidence that NVDAB collateral membership and USDT debt coexist in some accounts. Don't infer that NVDAB alone backs their debt, that an EOA is a person, or that a holder wants the app's sell-or-borrow comparison. The 4 October checkpoint still requires an observed consenting holder task, defensible sale costs and a personal-risk boundary. The research probe adds no D-017 product feature.

## D-038: DeFi Positions coverage is context, not a risk forecast

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** read-only API evidence; D-033 unchanged

The [signed coverage read](../research/2026-10-03-binance-defi-positions-coverage.md) returned NVDAB in a Venus `supply` group and USDT in a Venus `borrow` group for a selected public account. The probe didn't retain whether they belonged to the same pool or position. The response wasn't reconciled to the exact Core pool or BNB block used for candidate selection. It contains current positions, not a post-supply or post-borrow simulation.

**CEO decision:** record DeFi Positions as a technically working research surface, but don't integrate it into the D-017 app before the 4 October checkpoint. It can't replace a consenting holder task or prove a safe personal cash choice. A later use would require pool, contract, amount and freshness reconciliation with on-chain Core reads.

## D-039: public NVDAB holder current-risk parity narrows one technical gap

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** read-only evidence; D-033 unchanged

The [bounded parity probe](../research/2026-10-03-nvdab-holder-current-risk-parity.md) used one signed holder ranking and fixed BNB block 125421781. The first selected public account had entered vNVDAB, positive stored vUSDT debt and three entered markets. Its two active markets produced exact three-word matches for both deployed Core current-risk calls. No account identifier, signed payload or raw position was retained in Git.

**CEO decision:** use this result only to support the current-risk arithmetic for this observed account. It doesn't establish a safe post-action borrow, NVDAB's isolated contribution to account borrowing power, user demand or sale proceeds. Do not add a D-017 product feature before the 4 October 12:00 UTC checkpoint. The consenting holder, cost and personal-risk conditions in D-033 remain open.

## D-040: separate technical quotes from the track's live demo direction

**Date:** 2026-10-03
**Owner:** Dyplux
**Status:** delivery requirement recheck; no transaction authorized

The [official track](https://www.bnbchain.org/en/hackathons/tokenized-stocks), rechecked 2026-10-03, permits spot on BNB Smart Chain mainnet and directs teams to dry-run with the Transaction API while building, then demonstrate with small live amounts. The repo has a signed Binance quote and an unsigned `/swap` construction for a temporary nonholder address, but no Transaction API simulation or signed mainnet execution.

**CEO decision:** make the live-amount gap explicit in the [readiness gates](../submission/readiness-gates.md). A read-only estimate cannot be described as an executed cash-out or as a complete live demo. Decide the product at the 4 October checkpoint first. Any small transaction later needs a concrete wallet, amount, spend cap, expected fee, failure-recovery path and specific founder authorization; don't use a public holder's assets. If the chosen product cannot produce a permitted mainnet task, report the gap rather than imply that a quote satisfies this direction.
