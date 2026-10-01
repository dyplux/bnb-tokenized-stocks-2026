# Product reset after the founder's Bell objection

**Checked:** 2026-10-01  
**Decision:** one research priority, no approved product or build

## What changed

The initial pre-trade receipt repeats Bell's comparison job. Moving it closer to a swap doesn't establish a new user outcome. The public entrant field is also more crowded than the first substitute map showed. The [event](https://www.bnbchain.org/en/hackathons/tokenized-stocks) gives 25% to originality and 20% to product quality. It requires a working Binance Web3 API integration, a central bStocks/Ondo/xStocks use case, spot on BNB Smart Chain mainnet, and a public repository at submission. The deadline is 2026-10-11 12:00 UTC. These are event rules, not evidence of demand.

## Existing products, checked from public sources

These repositories describe projects for this hackathon. A README is evidence of what its author claims and of published code structure, not evidence of adoption or an independently successful trade. Their submission status wasn't verified.

| Product | Publicly described task and evidence | Consequence for our idea |
|---|---|---|
| [PancakeSwap Stock Terminal](https://blog.pancakeswap.finance/articles/pancakeswap-your-go-to-guide-to-trade-rwas) | Official guide shows stock discovery, issuer choices, swap and positions | A catalog or issuer choice screen alone adds little. |
| [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) | Official stock flow resolves a ticker, checks state, quotes, confirms and follows the order | A general buy assistant duplicates an existing flow. |
| [PARALLAX](https://github.com/rishu4436/parallax) | README and code describe three-issuer quotes, simulation, execution and order polling | The first receipt and route comparison idea has a direct entrant. |
| [OneTicker](https://github.com/JemIIahh/oneticker) | README describes normalized routes, gates, an off-hours tape and MCP; it explicitly says no funded mainnet trade yet | A safer quote or market-hours monitor also has a direct entrant. |
| [yostocks](https://github.com/yostocks-protocol/yostocks) | README gives a Telegram buy/sell flow, alerts, strategies and linked mainnet transaction hashes; its [DX log](https://github.com/yostocks-protocol/yostocks/blob/main/DX_LOG.md) reports an Ondo sell refused outside US market hours | Buying, selling and notification already exist. A refused exit may be a narrower unresolved task, but their observations need independent reproduction. |
| [Portir](https://github.com/yeheskieltame/portir) | README and repository describe stock purchases, recurring plans, sell rules, portfolio and a Venus LoanGuard | First purchase, DCA and collateral rescue are crowded. Mainnet execution and cloud-region limits remain qualified in its README. |
| [Steward](https://github.com/zkasuran/steward-bnb) | README and repository describe a post-holding ledger, dividend/split adjustment and Venus borrow sizing | A generic ownership or collateral dashboard duplicates it. The README says its Binance Web3 API client still uses a keyless mock. |
| [NightDesk](https://github.com/PhiBao/nightdesk) and [EquityMux](https://github.com/tang-vu/equitymux) | Session-aware trading and normalized issuer comparison respectively | More evidence that another price/rights screen is a weak bet. |

No product site above was independently exercised with a funded wallet. Three entrant site URLs were not accessible through the browsing tool, so the comparison rests on official incumbent material, public repositories and their own stated limits. The stronger claims in entrant DX logs are leads for our own probe, not our measurements.

## Three user jobs worth comparing

### A. First purchase readiness

**Person and trigger:** An eligible newcomer chooses one stock but has no funded BNB Chain wallet. They need the right asset, network, payment token and gas before they can buy.

**Evidence:** [Binance's stock flow](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) lists USDT and native gas as prerequisites. [Trust Wallet](https://trustwallet.com/buy-crypto) and [Binance Buy Any Token](https://developers.binance.com/en/docs/products/connect-2.0/buy-any-token/1.buy-any-token) already offer funding routes. PancakeSwap, yostocks and Portir cover much of the purchase task. We haven't observed a novice fail at this exact step.

**Judgment:** Reject a checklist or buy screen. Reopen only if a same-task test finds a broken handoff that a one-screen flow demonstrably fixes. A fiat-to-stock promise needs an actual compliant onramp, not a deep link.

### B. Exit or redemption recovery

**Person and trigger:** A holder wants stablecoins for a token they already own. A sell quote is missing or a direct redemption is unavailable. They need to know which path is actually possible today and what to do next.

**Evidence:** [Ondo](https://ondo.finance/ondo-stocks) says a person can acquire a token on a secondary market without completing issuer onboarding, but holding it doesn't make that person eligible to redeem directly. Most direct redemptions operate 24/5 and can pause; secondary trading depends on the venue. [Binance's bStocks FAQ](https://www.binance.com/en-AU/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38) describes pauses and eligibility controls. The [yostocks DX log](https://github.com/yostocks-protocol/yostocks/blob/main/DX_LOG.md) reports an Ondo after-hours sell refusal even while buying quoted. That is the competitor's observation, not ours.

**Proposed one-screen outcome:** For one held contract and amount, show (1) recognized token and source, (2) current secondary sell quote or exact failure, (3) issuer redemption status and a link to the issuer's own eligibility check, and (4) one safe next action. An unknown cause stays unknown. The app mustn't infer legal eligibility from a wallet address, guarantee an exit or suggest a switch to another security as an equivalent redemption.

**API and chain role:** BNB Chain supplies the held contract and balance. Binance Web3 RWA Data supplies current token identity and state; Trading API would supply a live token-to-stablecoin sell quote, if the account and route permit. Issuer documents supply redemption conditions. A quote isn't an executed sale.

**Substitute and counterargument:** yostocks already sells and reports failures; Ondo has issuer guidance. A separate recovery screen is useful only if it names a cause and action that those surfaces leave unclear. We have no measured failure frequency or human task observation.

**Falsifier:** Reproduce one real blocked exit read-only. Give the same scenario to an eligible tester using issuer, wallet and DEX interfaces. Reject this product if that person reaches the correct action without extra help, or if our API cannot distinguish the failure safely.

**Judgment:** First research test. No build approval yet.

### C. Stock-backed borrowing safety

**Person and trigger:** A holder has borrowed against a bStock on Venus or Lista; a price or protocol change approaches liquidation.

**Evidence:** [Lista](https://blog.lista.org/introducing-bstocks-as-collateral) says six initial bStocks can be collateral for stablecoin loans. [Venus's July report](https://community.venus.io/t/venus-monthly-report-july-2026/5896) reports tokenized-stock collateral and 38 SKHYB suppliers at July's end. That count shows a real market, not a mass consumer problem. Portir's LoanGuard and Steward's borrow view are direct entrant substitutes; Venus and Lista have their own position interfaces.

**Judgment:** Reject a generic health dashboard or rescue agent as the first product. Reopen only if a specific cross-protocol failure is observed and a safer action can be demonstrated without misleading liquidation advice.

## Current recommendation and dissent

Investigate **B, exit or redemption recovery**, with one held Ondo token and one bStock as a controlled comparison. This is a user action after ownership, so it is distinct from Bell's pre-trade comparability check. The objection remains strong: issuer guidance and existing sellers may already be sufficient. A and C aren't build candidates today. The two read-only researchers differed: the acquisition researcher preferred testing purchase readiness, while the lifecycle researcher preferred collateral health. The coordinator gives priority to the narrower exit task because their suggested products face direct public entrants and because issuer rules make a concrete exit constraint possible. This ordering is a research decision, not a demand score or a forecast of judging.

## Next evidence gate

1. Read one real BNB Chain holding and request a sell quote for a fixed token and amount, without an order. Record timestamp, route, status, error body with secrets removed, latency and an issuer source. Repeat once in and once out of US market hours only if permitted by quota.
2. Compare the same blocked-exit task in Ondo, Binance Wallet and a current swap interface. Record the exact next action each explains. Keep geography and account eligibility explicit without storing personal identifiers.
3. Ask a small number of consenting eligible users what they would do from that state. Record behavior and time, not praise or intent. If the incumbent path already works, reject B and revisit the problem instead of renaming it.
4. Only after that gate, write a one-page spec and revise the mentor-routing line. Do not build an app or add Agent Studio for a hypothetical need.

**Unknowns:** live Binance quote permissions and quota, exact RWA status fields, the frequency of blocked exits, whether an Ondo secondary sell failure reproduces for our route, and whether a separate recovery tool beats issuer and wallet interfaces.
