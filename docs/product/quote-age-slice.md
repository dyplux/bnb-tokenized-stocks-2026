# Quote-age display slice

**Prepared and implemented:** 2026-10-03 UTC. **Scope:** local browser timing only; no new Binance API call or trade.

## Observed gap

The [Binance Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api), checked 2026-10-03, says each `quoteId` has a TTL of about 30 seconds. The app currently starts a 20-second display timer only after `POST /api/quote` reaches the browser. RWA identity, RPC metadata and up to two signed quotes happen before that response. A slow request could leave a displayed estimate older than the stated API TTL.

## Change

Start the existing 20-second display window when the user sends the local quote request. On a successful response, subtract the elapsed request time from that window. If no time remains, show the expired state immediately and don't leave a usable sale amount, fee, same-cash line or conditional remainder on screen. Keep the response's capture time and route details as historical evidence, labelled expired. The clock is the browser's monotonic timer, so a user clock mismatch can't extend the window. This conservative rule may expire a quote before its vendor TTL; a new click asks for fresh data.

## Acceptance

1. A quick response remains visible for at most 20 seconds after the request began, including request latency.
2. A response arriving after 20 seconds is expired before the page paints a usable estimate.
3. Input edit, request error and repeated click still clear the prior quote and timer.
4. No signed API call or new server field is added. The main Sell card remains Unquoted.

This change reduces a freshness error. It doesn't establish execution, net proceeds, holder eligibility or a safe loan.

## Local check

The existing 35 local tests and inline JavaScript syntax check passed. A headless Chrome check at 320 CSS pixels intercepted every `/api/*` call and advanced the browser's monotonic clock after receiving a synthetic quote. A 21-second elapsed request produced the expired state synchronously, with no usable estimate or conditional remainder. A 17-second elapsed request showed the estimate for about three remaining seconds, then expired. Neither case produced a page error or horizontal overflow. The test used fixture data only; no signed Binance call, holder position or transaction occurred.
