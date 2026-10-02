# Builder report: current Core risk notice

**Date:** 2026-10-02. **Role:** bounded code writer. **Task:** implement the [approved slice](../../product/current-core-risk-notice-spec.md), without a new trade or risk forecast.

## Work and evidence

- Updated `app/server.py`, `app/index.html` and `tests/test_venus_account_state.py` with strict three-word ABI decoding, same-block reads, fail-closed errors, state classification and Unknown UI behavior.
- Used the existing [Venus source review](../../research/2026-10-02-account-wide-risk-feasibility.md) and [deployed selector observation](../../research/2026-10-02-venus-deployed-risk-read.md). No new external source was opened for this code task.
- Four focused Python tests, a Python compile check, JavaScript syntax check and `git diff --check` passed before handoff.

## Inference, limits and recommendation

The local tests exercise the ABI and error boundary with mocked RPC responses. They cannot establish a real holder's debt, health factor or safety after a new deposit. The writer made no live API calls. The coordinator should review the code and copy, then perform a narrow public read and browser check before merging. No disagreement with the bounded spec was raised. Existing separate changes to `AGENTS.md` and the spec were left untouched.
