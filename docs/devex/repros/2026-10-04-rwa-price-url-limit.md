# Documented 100-address batch returns HTTP 414

**Observed:** at 2026-10-04 10:56:41 UTC, a signed `GET /api/v1/dex/market/rwa/price` with 100 BNB Chain contract addresses returned HTTP 414 and no response body. The encoded request URL was 4,597 characters. The [RWA Data reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) documents a maximum of 100 addresses per request but doesn't state a smaller URL-length limit.

The [sanitized request fixture](../fixtures/2026-10-04-rwa-price-100-addresses-414.json) contains the 100 public contract addresses and the HTTP result, without the API key or signed headers. Four subsequent batches of 35, 35, 35 and 25 addresses all returned business code 0 and 130 rows total. The periodic collector uses 40 addresses in one batch and has succeeded. The exact safe maximum wasn't measured.

**Suggested documentation correction:** state the practical URL-length limit for this GET endpoint, or support a POST body for large batches. Clients should keep their batches below the observed 100-address failure and retry smaller batches after HTTP 414.
