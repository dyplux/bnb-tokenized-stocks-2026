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
