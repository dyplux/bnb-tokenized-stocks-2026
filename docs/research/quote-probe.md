# Read-only Binance Web3 quote probe

**Prepared:** 2026-10-01. **Live result:** none. The private repo has no local Binance Web3 credentials or measured RFQ yet.

The [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) documents `GET /api/v1/dex/aggregator/quote` on `https://web3.binance.com/build`. For an RWA route it requires a wallet address, and the `amount` parameter is an integer in the sell token's smallest unit. The route's `quoteId` lasts about 30 seconds. The [authentication headers](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) use `X-OC-APIKEY`, `X-OC-TIMESTAMP` and `X-OC-SIGN`. These are documented expectations; this project's signing and response parsing have not been confirmed by a live request.

[`scripts/probe_binance_quote.py`](../../scripts/probe_binance_quote.py) makes one opt-in signed GET for BNB Chain ID 56. It requires token contracts, a positive **raw** sell amount and the actual public wallet address to which an RFQ would be bound. It doesn't build, sign or submit a swap. Credentials must be in the process environment or the repo-root `.env`, which `.gitignore` excludes. Don't paste a secret into a shell argument, issue report or chat. The command's output omits the wallet, signature, request URL, quote ID and raw API message.

```sh
python3 scripts/probe_binance_quote.py \
  --from-token <BNB_CHAIN_BSTOCK_CONTRACT> \
  --to-token <BNB_CHAIN_USDT_CONTRACT> \
  --amount-raw <POSITIVE_INTEGER_IN_TOKEN_BASE_UNITS> \
  --wallet <PUBLIC_EVM_WALLET_ADDRESS>
```

Use the exact token contract and holder amount under investigation. The FAQ's multiplied display balance isn't interchangeable with the raw token amount. The [BEP-677 specification](https://github.com/bnb-chain/BEPs/blob/master/BEPs/BEP-677.md) and the [mentor question](mentor-questions.md) leave the RFQ unit interpretation to confirm before any holder-specific decision. Don't infer a dividend from a current multiplier alone.

The sanitized JSON records UTC capture time, latency, HTTP and business codes, route count, and at most three routes with quoted input/output units and fee fields. `toTokenAmount` is an estimate in output-token base units. `tradeFee` is the API's estimated network fee in USD; `estimateGasFee` is a gas estimate in the chain's smallest unit. These fields cannot be subtracted from each other without conversion and confirmation of any other route costs. A successful response wouldn't establish a fill, final net proceeds, investor eligibility or profit. An empty route list or an error is a useful result to record in the workspace Developer Experience worklog, with the private address removed.

**Review finding:** the first Luna draft had Spot-style `X-MBX-*` headers, a millisecond integer timestamp, a `chainId` parameter and wrong token metadata names. The coordinator corrected these against the Trading API documentation before any network request. This is a concrete reason to check generated integrations against the official schema, and the corrected code is still unverified against a live signed response.
