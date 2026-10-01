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

## Current decision

The old H1/H2/H3 scores were a subjective research ordering, not demand evidence. The founder challenged H1's similarity to Bell and then rejected blocked-exit recovery as the main direction. [D-006](decisions/decision-log.md) prioritizes a public event after cash close leading to a bounded, amount-specific BNB Chain spot action. Public entrants already cover weekend price monitors, baskets and basic earnings rules, so the exact workflow must be compared. No live Binance quote or observed user task exists, so no implementation is approved. The `referencePrice` field is derived from token price and cannot be used as an independent TradFi benchmark.

## Blockers and next work

1. Choose one public after-close company event and verify its source, timestamp and BNB Chain token contract. Compare the full event-to-order task against StockAnalyst, PARALLAX, Portir and Binance Agentic Wallet.
2. Confirm Binance API scope and quota without exposing credentials. Run a read-only RWA lookup and one amount-specific closed-session quote only if permitted. Record redacted fields, latency and errors for the Developer Experience Report. No order or funds at this gate.
3. Observe a consented eligible user's next action from that event, or compare a faithfully replayed task in incumbent interfaces. Reject the concept if it only adds a news summary or generic quote.
4. Revise the one-line hacker application answer only when this task has a credible advantage. The founder submits it; no form has been submitted here. Write a one-page spec after the gate passes. No app code, DNS work or deployment now.

## Resume

Open `/Volumes/SSD500/Dyplux/bnb-tokenized-stocks-2026`, read this file, [01-event-rules.md](01-event-rules.md), the [decision log](decisions/decision-log.md) and the [off-hours reset](research/2026-10-01-off-hours-reset.md). Recheck the official page if the date has changed. Then pick up item 1 above. `git status --short` shows local changes; `gh repo view dyplux/bnb-tokenized-stocks-2026` checks the remote after initial push. The primary workstation disk is constrained; keep large artifacts on the SSD.
