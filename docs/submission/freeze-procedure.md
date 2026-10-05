# Final submission freeze procedure

Last verified: 2026-10-05. Scope: planned October 11 freeze. Canonical owner/source: [event rules](../01-event-rules.md), [judge guide](../../JUDGE.md), [frozen claims](frozen-claims-2026-10-05.md). Supersedes: none. Status: CURRENT; no release or tag exists yet.

1. Clone the public repository into a clean directory, run no-secret replay and `python3 -m unittest discover -s tests -q`.
2. Verify observed receipt hashes with the canonical JSON algorithm in `app/rwa_policy.py`. Check synthetic fixture labels and fail-closed cases.
3. Record full-history secret scan result and any unresolved historical PII findings. Do not call the repository secure solely because a regex scanner found no credential.
4. Check public judge URL, receipt downloads, final video URL and GitHub links while signed out. Confirm HTTPS and the final deploy corresponds to the intended commit.
5. Freeze the final founder-reviewed DevEx cut and compute its hash. Confirm form fields and submit only under explicit founder action/authorization.
6. Create a submission manifest with `SUBMISSION_SHA`, `SUBMISSION_TAG`, SHA-256 for README, JUDGE, public judge-page asset, final video, observed receipt files and DevEx cut; include test command/result, deployment status and form confirmation references.
7. Only after all gates pass, tag the exact commit, create a GitHub Release if authorized, clone the tag afresh and rerun verification. Preserve the Pages URL as fallback during any separate domain transition.

**Not yet frozen:** `SUBMISSION_SHA`, `SUBMISSION_TAG`, final video, final DevEx form and submission confirmations. The current 60-second film is a verified fallback. The video specialist receives the [evidence handoff](video-specialist-evidence-handoff.md) after claims are frozen.
