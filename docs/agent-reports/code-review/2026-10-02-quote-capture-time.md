# Read-only quote flow review, 2 October 2026

**Objective:** find concrete bugs in the local Binance Web3 quote path before a first authenticated call.

## Work and evidence

Luna read `app/server.py`, `app/index.html` and `docs/product/binance-quote-gate.md` without external API calls. It found that `signed_binance_get()` used the authentication timestamp from before the request as `capture_time_utc`, while the interface labelled it as a captured quote. The server now records local UTC time after the HTTP response body is read. Network failures with no response have a null capture time. The interface labels both fields as **local response received**, so they aren't mistaken for upstream market-data timestamps.

The reviewer also observed that `/api/quote` returns HTTP 200 for structured states such as `missing_credentials` and `no_route`. The coordinator kept that response contract for this read-only status lookup: the browser reads `data.status` and displays each state explicitly, and an empty route isn't represented as a zero-price sale. A future external API consumer would need a documented status contract before this endpoint is exposed. No public API or deployment exists now.

## Local verification and limits

An in-memory response delayed by 20 ms produced `capture_time_utc` after the signed `X-OC-TIMESTAMP`; an in-memory network error returned a null capture time. Python syntax parsing and `git diff --check` passed. No authenticated request, real Binance response, wallet action or holder observation was made. These checks prove the local timestamp behavior only.

**Sources:** inspected local code and [Binance Web3 authentication documentation](https://web3.binance.com/en/dev-docs/authentication), checked 2026-10-02. The documentation establishes the signing timestamp's purpose; the local review establishes the display bug.

**Model usage visible in CLI:** Luna review reported 33,821 tokens; bounded edit reported 22,282 tokens. Account quota balance wasn't visible.

**Next:** obtain the complete private Web3 key pair, then make the permitted RWA identity read and one holder-sized sell quote under the [quote gate](../../product/binance-quote-gate.md). Keep source freshness separate from local response time.
