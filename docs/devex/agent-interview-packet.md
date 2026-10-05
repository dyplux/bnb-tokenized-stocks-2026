# Agent integration interview packet

Last verified: 2026-10-05. Scope: preparation for founder-authored final DevEx report. Canonical owner/source: [sanitized fixed cut](2026-10-04-evidence-summary.md), [repros](repros/), [metrics](2026-10-04-metrics.json). Supersedes: none. Status: CURRENT.

The project used AI coding/research agents. Ask the agents or inspect their contemporaneous work logs, then corroborate every answer with a dated log, sanitized request/response, official documentation and reproduction. Don't invent human developer experience or convert a model's recollection into fact.

| Question | Evidence packet to inspect |
|---|---|
| Which documentation assumption first failed? | [`offhours` enum](repros/2026-10-04-market-status-enum.md), documented RWA enum. |
| Which behavior required inference? | [RFQ/SWAP wording](repros/2026-10-04-rwa-swap-route.md), Trading reference and introduction. |
| Which issue was our own bug? | [USDC decimals](repros/2026-10-04-bsc-usdc-decimals.md) and [age clock](repros/2026-10-04-token-age-clock.md). |
| Which endpoint caused retries or batching? | [100-address HTTP 414](repros/2026-10-04-rwa-price-url-limit.md), fixed-call metrics. |
| Which successful response was semantically unsafe? | [Unfunded simulation prediction](repros/2026-10-04-unsigned-build-simulation.md), [quote/access boundary](repros/2026-10-04-bstock-eligibility-documentation-gap.md). |
| Which field or sentence would have prevented work? | [Independent reference-clock audit](repros/2026-10-04-independent-reference-clock.md), [gas-unit ambiguity](repros/2026-10-04-quote-gas-units.md). |
| What workaround did we implement? | 35-address batches and explicit `UNKNOWN` reference age; verify in code and dated results. |
| What must another coding agent know first? | [Evidence model](../knowledge/evidence-model.md) and [security boundaries](../knowledge/security-wallet-policy.md). |

For each answered question record agent/task/date, exact source excerpt or path, competing interpretation, reproduction command, observed impact, confidence and founder review status. The fixed metrics cut spans 611 requests and mixed workloads; it isn't a reliability benchmark.
