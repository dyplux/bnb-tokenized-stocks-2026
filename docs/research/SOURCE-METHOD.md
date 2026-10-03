# Source method for product research

**Updated:** 2026-10-03 UTC. This method supplements the Dyplux research desk's `METODO.md`. Use it before proposing a tokenized-stock feature.

## Ask one decision question

Write the user, moment, amount, venue and action before searching. For this sprint: a person with 5 USDC in a self-custodied BNB Chain wallet considers a tokenized equity outside regular US hours. Can they see a current entry and exit route and the costs before risking the position?

The event's story gives us a setting. It doesn't prove a user problem, a profitable strategy or a missing product.

## Run five source lanes in order

| Lane | Where to look | What it can establish | What it can't establish |
|---|---|---|---|
| Official rules and API | Event page, Binance Web3 docs, issuer terms | Eligibility, endpoint contract, submission constraints | Live liquidity or independent demand |
| Direct product | Open the supplier and closest substitutes, use the same amount and session | Visible workflow and observed failure | Behavior outside the observed wallet, region and time |
| Builder friction | GitHub issues, release notes, developer forums, public DX logs | A specific reported failure and its reproduction steps | Population frequency or an untested general rule |
| Market observation | Dated quotes, receipts, chain data, Dune query with raw result | What happened at a specified time and amount | Future fill, profit or user intent |
| News and research | Issuer announcements, broker changes, SEC/Nasdaq publications | What changed and when | Product demand without observed behavior |

Search forums for exact tasks and error codes, not only broad words like `RWA`. Useful queries include `sell quote market closed`, `316008 tokenized stock`, `reference price stale`, `liquidity after hours`, `redemption eligibility EEA` and `wallet quote expiry`. Open the original issue or post. Record its date, product version, amount, chain, location if stated, and whether the author reproduced it. A search result or model summary is a lead only.

## Record a claim, then try to break it

Each candidate claim gets one row in [the evidence ledger](evidence-ledger.csv): URL, event date, check date, direct observation or inference, source strength, counterevidence and next check. Preserve these distinctions:

- **Issuer promise:** direct mint/redemption terms can differ by asset and user eligibility.
- **Venue availability:** a route may fail even while an issuer says the asset is transferable 24/7.
- **Quote:** an estimate for a specified wallet, size and moment. It isn't a fill or a guaranteed resale value.
- **On-chain receipt:** proves the transaction occurred; it doesn't prove a customer wanted the task or made money.
- **Competitor self-report:** valuable for a reproducible pain point, weaker than our own repeated observation.

Read field semantics in the raw provider documentation. The [official Binance tokenized-securities skill](https://github.com/binance/binance-skills-hub/blob/main/skills/binance-web3/binance-tokenized-securities-info/SKILL.md) says `tokenInfo.volume24h` is US stock volume, while on-chain buy/sell volume comes from another endpoint. It also warns that holder counts can aggregate chains and token/share multipliers can change. A plausible field name isn't a measurement definition.

Reject attractive but irrelevant leads explicitly. On 3 October, a personal-CLI scout returned [Binance Skills Hub #316](https://github.com/binance/binance-skills-hub/issues/316), [#331](https://github.com/binance/binance-skills-hub/issues/331) and [Nautilus Trader #4410](https://github.com/nautechsystems/nautilus_trader/issues/4410). #316 concerns metadata/docs, so it is tangential to our decision. #331 is a synthetic Base transaction example; #4410 concerns a centralized Binance WebSocket signer. Neither proves BNB tokenized-stock exit friction. This source audit keeps the model's leads from becoming product facts.

## Decide in a bounded session

Test the same decision in two closest products. Capture the exact screen or response, UTC time, amount and missing fields. Then write one of three outcomes: gap observed, gap absent, or gap unverified. A claim of originality needs the first. If access prevents the test, a prototype can proceed under the deadline, but its gap remains unverified in the README and submission.

The current CLI research pass used roughly 89,804 tokens for three low-yield leads. Further searches should be narrowly scoped to one source or one exact question. Read public sources directly before launching another model scout.
