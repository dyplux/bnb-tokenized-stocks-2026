# Binance Web3 signing preflight

**Checked:** 2026-10-01 22:36 UTC. **Runtime status:** no request with a real Binance Web3 key. The repo-root `.env` was absent and the process had neither `BINANCE_WEB3_API_KEY` nor `BINANCE_WEB3_SECRET_KEY` at the presence-only check. No value was printed.

## Source contract

The [official authentication guide](https://web3.binance.com/en/dev-docs/authentication), last modified on 2026-10-01 when checked, requires `X-OC-APIKEY`, millisecond UTC `X-OC-TIMESTAMP` and Base64 HMAC-SHA256 `X-OC-SIGN`. The signed pre-hash is `timestamp + method + requestPath + body`; for GET, body is empty. The URL and signed path must both include `/build`. The [RWA search reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) lists `keyword` and optional `platformId=bstock`, with ticker and asset identity fields. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) lists a signed quote for a chain, exact token contracts, raw sell amount and wallet address; a route is an estimate, not a fill.

## Dry run

Imported `app/server.py` and replaced its HTTP opener with an in-memory reply. With dummy credentials `example-key` and `example-secret`, `signed_binance_get()` constructed `/build/api/v1/dex/market/rwa/search?keyword=NVDA&platformId=bstock`. Independently recomputing HMAC from the URL path and the timestamp in the request header matched `X-OC-SIGN`. The dummy response parsed to `state=response`. This checks internal path/signature agreement only. It cannot prove Binance accepts the key, timestamp, permission, query or response parser.

## Next permitted call

Once complete credentials are placed in the ignored private `.env`, make one signed RWA search for NVDA/bstock. Record UTC start/end, HTTP and business code, latency, exact matching asset identity and any redacted failure in the [DX log](../dx/field-log.md). Do not log headers, secret, signed URL or full payload. A quote is a separate explicit step after the identity result has been inspected.
