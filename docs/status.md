# Project status

**Updated:** 2026-10-01
**Phase:** research gate and API feasibility
**Product selected:** no; H1 is challenged as a standalone product
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

## Current decision

Three problem hypotheses were compared. H1, a pre-trade decision receipt for bStocks and Ondo, ranked first at 57/100 on a subjective research scorecard. H2 scored 50/100 and H3 43/100. The founder then challenged H1's similarity to Bell and its value for an ordinary buyer. [Decision D-004](decisions/decision-log.md) puts both H1 as a standalone product and the application wording on hold. No live Binance quote or observed user task exists, so no implementation is approved. The `referencePrice` field is derived from token price and cannot be used as an independent TradFi benchmark.

## Blockers and next work

1. Map one ordinary buyer's concrete goal and safe next action. Compare the same ticker, amount and time in PancakeSwap and Agentic Wallet. Seek one consented user task if feasible. Reject a separate product if the receipt only adds reading.
2. Confirm safe Binance API account scope and quota without exposing credentials. Run only narrow RWA Data and quote probes if they can answer a decision question, with no order or money. Record actual onboarding, payload fields, latency and errors for the Developer Experience Report.
3. Revise the one-line hacker application answer only when a distinct outcome for the target user is clear. The founder submits it; this repository has not submitted a form.
4. Approve or reject a product against the event gates. Write a one-page spec only if the research gate passes. Do not start app code, DNS work or deployment now.

## Resume

Open `/Volumes/SSD500/Dyplux/bnb-tokenized-stocks-2026`, read this file, [01-event-rules.md](01-event-rules.md), the [decision log](decisions/decision-log.md) and the dated research reports. Recheck the official page if the date has changed. Then pick up item 1 above. `git status --short` shows local changes; `gh repo view dyplux/bnb-tokenized-stocks-2026` checks the remote after initial push. The primary workstation disk is constrained; keep large artifacts on the SSD.
