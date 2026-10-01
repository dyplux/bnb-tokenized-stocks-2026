# Project status

**Updated:** 2026-10-01
**Phase:** research gate and API feasibility
**Product selected:** no; a sourced event-to-spot-action task is the next research test
**Application code:** none
**Deployment:** none

## Completed

- First-pass documentary deliverables are complete: official rules, source ledger, [three explicit hypotheses](research/hypotheses.md), substitute map, prior-winner sample, skills scouting, API map, weighted recommendation, dissent and a provisional one-line application answer. This is a research handoff, not product approval.
- Read the founder's operating manual and the supplied Super Grok research as an unverified lead.
- Checked the [official hackathon page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) on 2026-10-01. Rules are recorded in [01-event-rules.md](01-event-rules.md).
- Two separate, read-only research passes mapped problems, substitutes, event rules and documented API surfaces. Their [problem report](agent-reports/problem-scout/2026-10-01-problems-and-substitutes.md) and [event/API report](agent-reports/event-api/2026-10-01-rules-and-api.md) are evidence leads. Product claims remain provisional until their source and runtime behavior are checked.
- A [Sol critical review](agent-reports/product-review/2026-10-01-critical-synthesis.md) challenged the early product recommendation. The [problem brief](research/problem-brief.md), [alternative map](research/alternatives-map.md), [scorecard](research/idea-scorecard.md) and [API map](api-map.md) record the narrowed test and counterevidence.
- Prepared a [one-line draft](submission/form-answer.md) for the founder's hacker application. It is for mentor routing and has not been submitted.
- Opened a separate repository on the external SSD. Bell was not changed for this project.
- Reopened product scouting after the founder's Bell objection. The [dated brainstorm](research/2026-10-01-product-brainstorm.md) checks incumbent flows and public entrant repositories, rejects another generic buy/comparison/collateral interface, and puts a holder's blocked exit first for falsification. Entrant README claims weren't independently run.
- Reopened the selection after the founder identified the event's cash-market-closure problem as central. The [off-hours reset](research/2026-10-01-off-hours-reset.md) compares three user tasks and gives a cited public event leading to a bounded spot action priority for research. [D-006](decisions/decision-log.md) supersedes D-005's priority. No technical path or demand has been proved.
- Found one concrete replay source: a Tesla 8-K accepted at 20:38:50 UTC on 2026-09-29, after the regular New York close. A dated CMC metadata extract identifies separate TSLAB and TSLAon BNB Chain contracts. Historical quote availability and execution weren't captured. This Tuesday event doesn't prove a unique weekend advantage against a broker that offers eligible stocks during weekday extended hours.
- Mapped [user access, net economic edge and Agent Studio](research/2026-10-01-economic-edge-and-agent-studio.md). The strongest distinct access interval is Friday 20:00 to Sunday 20:00 New York time for an eligible user with stablecoins, but no live quote, profitable trade or observed user has been recorded. Binance's own research reports much of the Monday gap priced into bStocks during the prior weekend; its figures are not our PnL measurement. D-007 requires real amount-specific quotes and cost accounting before any economic claim. Agent Studio's documented paid seller runtime is an optional service test, not the mainnet trading agent.
- Checked only the presence of credential fields in the root workspace `.env` on 2026-10-01. `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` are empty or missing there. The secret shown earlier in chat was truncated, so an authenticated Binance Web3 quote cannot be requested from this environment yet. No credential value was printed or committed.
- Inspected selected public competitor source files. NightDesk's seller builds price/session reports from Binance public RWA endpoints, while Portir's news guard reads Yahoo headlines and optional CoinDesk. Portir's code fails open to the price Guard if headlines or the model are unavailable. These are code observations, not reproduced trades or proof that our alternative improves outcomes.

## Current decision

The old H1/H2/H3 scores were a subjective research ordering, not demand evidence. The founder challenged H1's similarity to Bell and then rejected blocked-exit recovery as the main direction. [D-006](decisions/decision-log.md) prioritizes a public event after cash close leading to a bounded, amount-specific BNB Chain spot action. Public entrants already cover weekend price monitors, baskets and basic earnings rules, so the exact workflow must be compared. No live Binance quote or observed user task exists, so no implementation is approved. The `referencePrice` field is derived from token price and cannot be used as an independent TradFi benchmark.

[D-007](decisions/decision-log.md) narrows the possible advantage to a person who is eligible to trade, already has BNB Chain funds and lacks a comparable weekend stock route. Access may be useful even when it produces no trading profit. A price edge must survive actual bid/ask, slippage, fees and a valid exit. The paid Agent Studio idea has a 30-second RFQ-expiry problem and overlap with an existing entrant's seller; it remains optional until tested. Binance Agentic Wallet's current documentation already describes earnings/news watchers that can act under a user mandate. This is a published claim, not an observed run, and makes a generic event-to-order product insufficiently distinct.

## Blockers and next work

1. Identify an eligible user's current alternative in the Friday 20:00 to Sunday 20:00 ET window; find one genuine weekend public-company event for a BNB-listed token. The Tuesday Tesla filing remains a source-pipeline replay.
2. Confirm Binance API scope and quota without exposing credentials. Run a read-only RWA lookup and two amount-specific closed-session RFQs only if permitted, then record redacted cost fields, expiry, latency and errors for the Developer Experience Report. No order or funds at this gate.
3. Compare that exact task against StockAnalyst, NightDesk, PARALLAX, Portir and Binance Agentic Wallet. Reject the concept if it adds only a news summary or generic quote.
4. Test Agent Studio locally or on testnet only if the event-to-quote job has a distinct buyer and can beat RFQ expiry. Revise the one-line hacker application answer only when the task has a credible advantage. The founder submits it; no form has been submitted here. Write a one-page spec after the gate passes. No app code, DNS work or deployment now.

## Resume

Open `/Volumes/SSD500/Dyplux/bnb-tokenized-stocks-2026`, read this file, [01-event-rules.md](01-event-rules.md), the [decision log](decisions/decision-log.md) and the [off-hours reset](research/2026-10-01-off-hours-reset.md). Recheck the official page if the date has changed. Then pick up item 1 above. `git status --short` shows local changes; `gh repo view dyplux/bnb-tokenized-stocks-2026` checks the remote after initial push. The primary workstation disk is constrained; keep large artifacts on the SSD.
