# Bounded repository hardening plan

Last verified: 2026-10-05. Scope: Tokenized Stocks public repository. Canonical owner/source: current repo and frozen [Monday findings](../../experiments/EXP-RWA-004/monday-findings.md). Supersedes: none. Status: CURRENT.

## P0

1. Fix the broken `docs/status.md` reference in AGENTS.md; use `STATUS.md`.
2. Retire future cron execution of the completed Monday fallback, preserving manual dispatch and all historical evidence.
3. Give judges one short entry point, the real/synthetic distinction, proof paths and a reproducible clean clone.
4. Scan full Git history for secrets and private identifiers; stop if a live secret is found.
5. Freeze exact files and hashes only after public deployment and CI can be verified.

## P1

Add concise institutional knowledge, machine-readable program requirements, an Agent Studio spike plan and a final freeze procedure. These record evidence and do not expand the product.

## Do not touch

The preregistered protocol, Friday baseline, outcome fixtures, scorer, Monday results, receipts, collector tape and prior workflow history remain byte-stable. No mass directory moves, application refactor, DNS change, new deploy, capital action or form submission. The founder's visual prototype `app/budget-preview.html` is an unrelated untracked file and must remain unstaged.

The founder-named deep research report was not located in this workspace at audit time; its conclusions in the attached request are treated as direction, not as a sourced report quotation.
