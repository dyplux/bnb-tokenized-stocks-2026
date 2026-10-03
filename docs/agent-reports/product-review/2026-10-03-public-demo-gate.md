# Public judge-demo gate

**Date:** 2026-10-03 UTC. **Review:** Plus Sol, read-only. **Implementation:** one bounded Plus Luna slice, followed by coordinator review. **Question:** what prevents the current local app from safely serving a public judge link?

## Observed blockers

The server binds to `127.0.0.1` and accepts POST requests only for localhost `Host` and `Origin` values. This is suitable for the current local prototype, but a browser using a public hostname would receive 403. Client-supplied headers aren't authentication. A direct client can omit `Origin`, and the current quote endpoint has no process-wide request budget or concurrency cap. One accepted click can make one signed RWA identity request and one or two signed quote requests. `ThreadingHTTPServer` can create concurrent handlers while those upstream requests wait. Production also falls back to the ignored repo-root `.env`, and scenario errors can expose truncated upstream exception text.

The [Cloudflare Tunnel guide](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/create-remote-tunnel/) describes routing a public hostname to a local service. The [WAF rate-limit rules](https://developers.cloudflare.com/waf/rate-limiting-rules/) and [Cache Rules](https://developers.cloudflare.com/cache/how-to/cache-rules/settings/) provide separate edge controls. A tunnel alone wouldn't protect Binance quota, keep the local process alive or make the quote response authoritative after expiry.

## Small local slice completed

`app/server.py` now rejects redirects and responses above 2 MiB for its fixed Venus API and BNB RPC destinations, and rejects malformed or non-object JSON. The Venus path also requires a list-shaped `result`. Binance signing and the quote flow were left unchanged. Synthetic redirect and oversized-body cases were added. The full Python 3.9 unit suite passed **37 tests** after fixing a test fixture that failed on Python 3.9. A live public read after the edit returned **51 Venus market rows** and BNB chain ID **56**. No signed Binance request, wallet action, deployment or public link was used for this slice.

## Decision and remaining work

The coordinator accepted the upstream guard because it is useful even if the product changes. Public-host support and deployment remain deferred to the 4 October product checkpoint. If D-017 survives, a judge demo still needs an exact public host/origin configuration, a server-side quote budget and concurrency cap, server-enforced quote expiry, environment-only production secrets, sanitized errors and logs, cache bypass, rate limits, process supervision and a clean signed-out browser pass. None of those controls is present or verified yet. The current process must stay local.

**Limits:** this review did not inspect a public runtime, judge session, holder action, final sale costs or personal Venus borrowing risk. The CLI did not expose the signed-in account email or a reliable remaining quota.
