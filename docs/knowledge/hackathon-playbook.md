# Evidence-first hackathon playbook

Last verified: 2026-10-05. Scope: reusable Dyplux process; event-specific rules expire. Canonical owner/source: [project decision log](../decisions/decision-log.md), [Monday protocol](../../experiments/EXP-RWA-004/monday-open-protocol.md), [judge guide](../../JUDGE.md). Supersedes: none. Status: CURRENT.

Research → hypothesis → preregistration → dated data → kill/promote → smallest build → mechanical verification → judge path → deployment check → exact freeze.

1. A judge should understand the task in 30 seconds. Deeper inspection should reveal more evidence for the same claim, not a new story.
2. Use a sponsor integration because it supplies a required input or action. Map each use to code and a captured observation, not a logo.
3. Record negative experimental results. Monday's two-of-three independent directional matches didn't meet the frozen promotion gate, so `SAFETY_ONLY` is the honest result.
4. Separate real, replayed, simulated and synthetic states. A real API envelope, a simulation prediction and an on-chain transaction are distinct events.
5. Keep raw/sanitized fixtures, retrieval time, source URL, method and hash. A clean clone must reproduce the no-secret path.
6. Version the policy and decision receipt. Never weaken a safety gate to obtain a greener demo.
7. Before submission, bind public URL, demo video, DevEx cut and receipts to one SHA/tag. Verify signed-out access from a clean environment.

This is a process record, not evidence that every final submission step is complete. The [freeze procedure](../submission/freeze-procedure.md) names remaining gates.
