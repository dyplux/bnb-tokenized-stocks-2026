# Read-only Binance Web3 RWA search probe

**Prepared:** 2026-10-01. **Live result:** none. The complete Web3 secret isn't available in this repository's ignored `.env`.

The [RWA Data reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) documents `GET /api/v1/dex/market/rwa/search` with a required `keyword` and an optional `platformId`. The [authentication guide](https://web3.binance.com/en/dev-docs/authentication) requires the `/build` prefix in the signed request path. These are documented expectations. We haven't confirmed the response with this project's credentials.

[`scripts/probe_binance_rwa.py`](../../scripts/probe_binance_rwa.py) makes one signed, read-only request for an exact underlying ticker. It reads `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` from process variables or the repo-root `.env`, which Git ignores. It prints latency, HTTP and business codes, plus a small allowlist of matching asset fields. It doesn't log credentials, headers or the raw response.

```sh
python3 scripts/probe_binance_rwa.py NVDA
python3 scripts/probe_binance_rwa.py NVDA --platform bstock
```

The result may establish API access and show whether Binance currently lists an issuer representation on BNB Chain. It doesn't establish that a wallet can trade it, that an off-hours route exists, that a price is executable, or that any user has an economic edge. Search returns token identity fields; a later size-specific quote is a separate call. The old workspace-root token-list draft isn't used here because it made a categorical provenance claim about `referencePrice` that our [source audit](2026-10-01-reference-price-source-audit.md) withdrew.

When credentials are available, make one call for the chosen ticker and record its UTC time, latency, codes and redacted asset fields in the [DX field log](../dx/field-log.md). Don't backfill these values from documentation. No retry loop or trade is part of this probe.
