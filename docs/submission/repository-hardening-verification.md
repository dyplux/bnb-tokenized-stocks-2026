# Repository hardening verification, 5 October 2026

Last verified: 2026-10-05 22:00 UTC. Scope: local commit `e1c2582ab0592811eaf9df0e35be8cc60402ae69` and existing public Pages site. Canonical owner/source: commands below, [CI incident](2026-10-05-final-commit-ci.md). Supersedes: none. Status: CURRENT; public push/deploy not performed.

## Local and clean-clone gates

| Command or probe | Result |
|---|---|
| `git diff --cached --check` before commit | Exit 0. |
| `python3 -m unittest discover -s tests -q` | 134 tests, 0 failures, local and clean clone. Added deterministic same-input receipt check and timeout/5xx/malformed source fail-closed cases. |
| `ruby -e ... YAML.safe_load(...)` for four registry YAML files | All four parsed as mappings. |
| Local Markdown link checker on README, AGENTS, PROJECT_CONTEXT, JUDGE, knowledge, new submission/product/DevEx docs | 151 local links checked, 0 missing. |
| Clean local `git clone --no-hardlinks`, `cp .env.example .env`, `python3 app/safety_server.py` | Setup, unit tests and HTTP probes completed in 0.79 seconds on this Mac, including clone. This is not a cross-platform benchmark. |
| `GET /`, `GET /api/dated-example` in clean clone | HTTP 200, dated `NEED_HUMAN`, canonical receipt SHA-256 verified. |
| `POST /api/safety-check` with valid request but no API credentials | HTTP 503 with setup instruction; no decision receipt. |
| Signed-out urllib fetch of public Pages index, two observed receipt JSON files and MP4 | All HTTP 200; all four response bodies matched local `/docs` SHA-256 values. The live site still reflects the previous public commit until a permitted push/deploy. |

## Full Git history scan

`git rev-list --objects --all` plus `git cat-file --batch` scanned 1,531 text/small blobs across all reachable commits. Two MP4 blobs over 3 MB were excluded from text regex matching and identified separately. Patterns included Cloudflare, Binance, GitHub and OpenAI token formats, PEM private keys, private/secret/seed assignments, Bearer headers, UID assignments, personal emails and local user-directory paths. **No credential or UID pattern matched.** Two historical blobs contained a local personal path: old `docs/status.md` and `docs/submission/video-qa.md`. They remain in history; no rewrite or credential rotation is indicated by this regex result alone. A scanner miss remains possible.

## External gate

Public `main` is still `2a100478dbcefe366953878104b9be136936d404`; local hardening is `e1c2582ab0592811eaf9df0e35be8cc60402ae69`. No push, DNS change, Pages deployment, form submission, release, tag or capital action was made in this phase. Earlier CI attempts for `2a10047` ended before runner assignment; the [incident record](2026-10-05-final-commit-ci.md) contains exact run IDs and job states. A runner-backed Python run and Pages deployment for the final submission SHA remain unverified.
