# Failure modes to avoid repeating

Last verified: 2026-10-05. Scope: observed and explicitly labelled fixture-driven safety lessons. Canonical owner/source: [safety evidence](../research/2026-10-04-safety-evidence.md), [DevEx lessons](devex-lessons.md), [Monday result](../../experiments/EXP-RWA-004/monday-findings.md). Supersedes: none. Status: CURRENT.

| Failure mode | Cause / detection | Current rule / mechanical check |
|---|---|---|
| Displayed spread called arbitrage | Different representations and amount-specific costs; [quote ladder](../../experiments/EXP-RWA-009/results.json). | Normalize exposure and check executable route/cost before any edge claim. |
| Stale provider rows treated as equivalent | [Matched ticker-minute audit](../../experiments/EXP-RWA-010/results.json) exposed different token clocks. | Carry per-source times; no synthetic same-time join. |
| Quote treated as eligibility | [Observed routes](../devex/repros/2026-10-04-bstock-eligibility-documentation-gap.md) came without holder proof. | Access gate stays unknown until independently verified. |
| Token timestamp treated as stock-reference timestamp | [Field audit](../devex/repros/2026-10-04-independent-reference-clock.md) found no independent clock. | Separate fields; reference age `UNKNOWN`. |
| API 200 treated as executable success | [Simulation repro](../devex/repros/2026-10-04-unsigned-build-simulation.md) predicted failure. | Inspect nested simulation state; failure blocks signer. |
| Route-target bytecode treated as trusted provenance | [Execution-target read](../product/2026-10-04-execution-target-read.md) cannot establish authorization alone. | Allowlist and provenance review are separate gates. |
| Current multiplier equality treated as history | [Current fixed-block audit](../../experiments/EXP-RWA-011/onchain_multiplier_audit.json) lacks before/after event history. | Label corporate-action scenarios synthetic; require dated issuer and chain history for live claim. |
| Six provider rows treated as six independent outcomes | [Monday scorer](../../experiments/EXP-RWA-004/monday-findings.md) has three shared underlyings. | Count independent tickers for direction; retain six rows for residuals. |
| Synthetic ALLOW called observed | [Judge page](../../JUDGE.md) includes a green fixture. | Always label synthetic and keep observed outcomes separate. |
| Old product directions contaminate submission | [Decision log](../decisions/decision-log.md) includes retired alternatives. | Frozen claims file controls public narrative. |
| Our decimals or clock bug blamed on provider | [Units](../devex/repros/2026-10-04-bsc-usdc-decimals.md) and [clock](../devex/repros/2026-10-04-token-age-clock.md) repros traced both locally. | Test token decimals and event-time arithmetic before an external defect report. |
