# Private repository prepublication preflight

**Checked:** 2026-10-03 UTC. **Scope:** local Git repository and current private GitHub visibility. No publication or deploy occurred.

## Observations

- [O] `gh repo view dyplux/bnb-tokenized-stocks-2026` reported `PRIVATE`, default branch `main`. The local worktree was clean before this note.
- [O] `.env` is ignored by `.gitignore`; `git check-ignore -v .env` named that rule. At the scan, 128 tracked files included `.env.example`, but no `.env`, `auth.json`, PEM or `.key` path. No tracked path with those names appeared in `git log --all --name-only`.
- [O] `git log --all --format` returned only `Dyplux <admin@dyplux.com>` as commit author. A current-tree filename scan for `Diogo`, `Kitra`, `Lanoar` and email-shaped strings returned no file.
- [O] A local read-only scan inspected 559 unique Git blobs up to 5 MiB each across all refs. It printed only counts and paths, never matching values. It found zero matches for four limited patterns: `BX-` UUID-style Binance API keys, `cfut_` Cloudflare tokens, PEM private-key headers and `sk-` OpenAI-style secrets.

## Boundary

This is a limited pattern scan, not proof that history contains no secret or personal data. It cannot detect an unlabelled Binance secret, an arbitrary wallet mnemonic, credentials in omitted blobs over 5 MiB, or a key stored outside Git. Before making the repository public, repeat a comprehensive secret and personal-data review on the final commit and history, inspect generated media and screenshots, and get the founder's specific publication authorization. The product decision, public-host controls, video and judge path remain separate gates in [readiness](readiness-gates.md).

## Later history scan, 2026-10-03 UTC

- [O] `gh repo view` still reported `PRIVATE`, default branch `main`. All commit authors across local refs were `Dyplux <admin@dyplux.com>`.
- [O] A read-only scan inspected **593 unique Git blobs** across local refs, with none over its 10 MB limit. It found zero matches for Binance `BX-` UUID keys, `cfut_` tokens, OpenAI-style `sk-` keys, GitHub tokens, AWS access-key IDs, Google API keys, Slack tokens and PEM private-key headers. It printed no matched values.
- [O] A personal-name marker matched one historical blob: this preflight file itself, because its earlier paragraph lists names searched. No personal marker was found in the other 592 blobs by those exact patterns. A filename-history scan found `.env.example` and `tests/test_binance_credentials.py`; `.env.example` has two empty credential assignments. It found no historical `.env`, `auth.json`, PEM or `.key` path.

This extends the earlier pattern scan but remains a bounded prepublication check. It doesn't detect every possible secret or prove that screenshots, generated assets or a future commit are clear. Repeat it on the final public candidate before changing repository visibility.

## Full local-ref pass after commit `a61c956`, 2026-10-03 UTC

- [O] `gh repo view` still reported `PRIVATE` on `main`. The worktree was clean at the start of this pass.
- [O] A read-only Python scan enumerated all 1,431 objects reachable from local refs and inspected all **616 unique blobs**. None exceeded its 10 MB limit. It printed counts and paths only, never matched values.
- [O] Zero blobs matched the scanned provider-token prefixes, PEM private-key headers or personal email domains. Eight historical blobs matched a broad sensitive-assignment pattern; a second masked classification found all eight were environment-variable lookups in `app/server.py` or `scripts/probe_binance_quote.py`, not literal assignments.
- [O] The local Git history contains 140 distinct paths. The sensitive-name path scan found only `.env.example`, whose assignments were previously checked as empty. No real `.env`, credential JSON, PEM, wallet key or certificate path appeared under those patterns.

The scan is broader than the 593-blob pass above, but pattern matching cannot prove that arbitrary unlabeled secrets, private data or future demo assets are absent. Check the **final** commit and any video, screenshots and deploy configuration before the founder authorizes public visibility. No visibility setting was changed.

## Current-head recheck after `e8e8ede`, 2026-10-03 UTC

- [O] The GitHub repository remains private on `main`. The local worktree was clean before the scan.
- [O] A read-only pass traversed 1,528 reachable Git objects and inspected all **656 unique blobs**. None exceeded 10 MB. It printed aggregate counts only, never candidate values.
- [O] Zero blobs matched the scanned Binance `BX-` UUID key, Cloudflare `cfut_` token, OpenAI-style `sk-` key, GitHub token, AWS key ID, Google API key, Slack token, PEM private-key header or personal email-domain patterns. These patterns don't detect arbitrary unlabeled secrets.
- [O] The only sensitive-name path in current files or path history was `.env.example`; its credential assignments are empty. `.env` remains ignored. All reachable commits have the intended Dyplux author identity.

This is a bounded history check on the current private head, not final publication clearance. Repeat it after the final app, media and deployment configuration exist, inspect screenshots and generated assets separately, and obtain the founder's specific authorization before changing visibility.
