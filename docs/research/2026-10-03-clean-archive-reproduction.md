# Clean archive reproduction

**Checked:** 2026-10-03 01:42 UTC
**Source commit:** `36130dc`

## Method and observed result

The coordinator exported `git archive HEAD` into a temporary directory on the SSD. The archive had no `.env`. The process environment had all `BINANCE_WEB3_*` variables removed. From that directory, `python3 app/server.py` bound to `127.0.0.1:8000`; the process was stopped after the reads and the temporary directory was removed.

| Request | Observed result |
|---|---|
| `GET /` | HTTP 200, 54,651 HTML bytes, title present |
| `GET /api/scenario?units=1&cash=100` | HTTP 200, live Venus response, `retrieved_at=2026-10-03T01:42:14+00:00`, keys include `market`, `borrow`, `sale`, `contract_cap`, `source_url` |
| `POST /api/quote` with valid JSON and a zero-address technical placeholder | HTTP 200, `status=missing_credentials`, `identity_status=not_checked`; no signed Binance request was attempted |

The clean checkout starts and presents the public-data scenario without a private key. The signed sale estimate correctly requires a user's own Binance Web3 credentials. This probe didn't use a holder, assess an account-specific Venus position, test a public deployment or complete the cash decision. It doesn't replace the earlier credentialed local browser path.
