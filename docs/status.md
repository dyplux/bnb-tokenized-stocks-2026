# Project status

**Updated:** 2026-10-01
**Phase:** research gate and API feasibility
**Product selected:** no; H1 is a provisional test candidate
**Application code:** none
**Deployment:** none

## Completed

- First-pass documentary deliverables are complete: official rules, source ledger, up to three hypotheses, substitute map, prior-winner sample, skills scouting, API map, weighted recommendation, dissent and a provisional one-line application answer. This is a research handoff, not product approval.
- Read the founder's operating manual and the supplied Super Grok research as an unverified lead.
- Checked the [official hackathon page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) on 2026-10-01. Rules are recorded in [01-event-rules.md](01-event-rules.md).
- Two separate, read-only research passes mapped problems, substitutes, event rules and documented API surfaces. Their [problem report](agent-reports/problem-scout/2026-10-01-problems-and-substitutes.md) and [event/API report](agent-reports/event-api/2026-10-01-rules-and-api.md) are evidence leads. Product claims remain provisional until their source and runtime behavior are checked.
- A [Sol critical review](agent-reports/product-review/2026-10-01-critical-synthesis.md) challenged the early product recommendation. The [problem brief](research/problem-brief.md), [alternative map](research/alternatives-map.md), [scorecard](research/idea-scorecard.md) and [API map](api-map.md) record the narrowed test and counterevidence.
- Prepared a [one-line draft](submission/form-answer.md) for the founder's hacker application. It is for mentor routing and has not been submitted.
- Opened a separate repository on the external SSD. Bell was not changed for this project.

## Current decision

Three problem hypotheses were compared. H1, a pre-trade decision receipt for bStocks and Ondo, is the first research test at 57/100 on an explicitly subjective scorecard. H2 scored 50/100 and H3 43/100. Those numbers do not validate user demand. H1 has no live Binance quote or observed user task, so no implementation is approved. The `referencePrice` field is derived from token price and cannot be used as an independent TradFi benchmark.

## Blockers and next work

1. Confirm safe Binance API account scope and quota without exposing credentials. Run only narrow RWA Data and quote probes, with no order or money. Record actual onboarding, payload fields, latency and errors for the Developer Experience Report.
2. Compare the exact ticker, size, time and task in PancakeSwap and Agentic Wallet. Observe whether a candidate receipt changes the decision. Seek one consented user task if feasible.
3. Check the founder's eligibility and the private application fields before the founder submits the provisional line. The one-line answer may change with evidence.
4. Approve or reject H1 against the stop rule. Write a one-page spec only if the research gate passes. Do not start app code, DNS work or deployment now.

## Resume

Open `/Volumes/SSD500/Dyplux/bnb-tokenized-stocks-2026`, read this file, [01-event-rules.md](01-event-rules.md), the [decision log](decisions/decision-log.md) and the dated research reports. Recheck the official page if the date has changed. Then pick up item 1 above. `git status --short` shows local changes; `gh repo view dyplux/bnb-tokenized-stocks-2026` checks the remote after initial push. The primary workstation disk is constrained; keep large artifacts on the SSD.
