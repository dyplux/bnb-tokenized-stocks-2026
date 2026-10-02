# Read-only Binance Web3 quote probe

**Prepared:** 2026-10-01. **Live result:** the application path returned a signed NVDAB/USDT LiquidMesh `SWAP` quote on 2026-10-02; see the [dated observation](2026-10-02-first-live-binance-quote.md). The separate command below hasn't been run live.

The [Trading API guide](https://web3.binance.com/en/dev-docs/llms-full.txt) documents `GET /api/v1/dex/aggregator/quote` on `https://web3.binance.com/build`. `userWalletAddress` is required for RFQ routes, and the `amount` parameter is an integer in the sell token's smallest unit. The route's `quoteId` lasts about 30 seconds. The [authentication guide](https://web3.binance.com/en/dev-docs/authentication) requires `X-OC-APIKEY`, `X-OC-TIMESTAMP` and `X-OC-SIGN`, with `/build` included in the signed path. The application path authenticated and parsed one NVDAB SWAP route on 2026-10-02. The standalone probe command remains unrun live.

[`scripts/probe_binance_quote.py`](../../scripts/probe_binance_quote.py) makes one opt-in signed GET for BNB Chain ID 56. It requires token contracts, a positive **raw** sell amount and the actual public wallet address to which an RFQ would be bound. It doesn't build, sign or submit a swap. Credentials must be in the process environment or the repo-root `.env`, which `.gitignore` excludes. Don't paste a secret into a shell argument, issue report or chat. The command's output omits the wallet, signature, request URL, quote ID and raw API message.

```sh
python3 scripts/probe_binance_quote.py \
  --from-token <BNB_CHAIN_BSTOCK_CONTRACT> \
  --to-token <BNB_CHAIN_USDT_CONTRACT> \
  --amount-raw <POSITIVE_INTEGER_IN_TOKEN_BASE_UNITS> \
  --wallet <PUBLIC_EVM_WALLET_ADDRESS>
```

Use the exact token contract and holder amount under investigation. The command can probe either buy or sell by setting the input and output contracts in the appropriate order. The FAQ's multiplied display balance isn't interchangeable with the raw token amount. The [BEP-677 specification](https://github.com/bnb-chain/BEPs/blob/master/BEPs/BEP-677.md) and the [mentor question](mentor-questions.md) leave the RFQ unit interpretation to confirm before any holder-specific decision. Don't infer a dividend from a current multiplier alone.

The sanitized JSON records UTC capture time, latency, HTTP and business codes, route count, and at most three routes with `executionMode`, quoted input/output amounts and fee fields if present. The [detailed execution guide](https://web3.binance.com/en/dev-docs/llms-full.txt) says an Ondo token uses RFQ, an xStock uses SWAP, and a bStock can return both modes in one response. Any future build must follow the returned mode per route; a bStock ticker alone doesn't decide the signing and settlement path. Treat fee-field units and which charges are included as unconfirmed until a live payload and current schema are checked. A successful response wouldn't establish a fill, final net proceeds, investor eligibility or profit. An empty route list or an error is a useful result to record in the workspace Developer Experience worklog, with the private address removed.

**Review finding:** the first Luna draft had Spot-style `X-MBX-*` headers, a millisecond integer timestamp, a `chainId` parameter and wrong token metadata names. The coordinator corrected these against the Trading API documentation before any network request. This is a concrete reason to check generated integrations against the official schema, and the corrected code is still unverified against a live signed response.

**Second static review, 2026-10-01:** the API map had incorrectly asserted that all equity/RWA routes use RFQ. Binance's [Trading API introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) distinguishes LiquidMesh SWAP from PcsXRfq RFQ for bStocks. The current [endpoint reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) still says equity/RWA routes always use RFQ. These official statements conflict. No quote was requested during that review; the [2026-10-02 live request](2026-10-02-first-live-binance-quote.md) later returned SWAP for one technical NVDAB quote.

**Documentary error review, 2026-10-01:** the [official Trading API error table](https://web3.binance.com/en/dev-docs/llms-full.txt) distinguishes Ondo market closed (`40367`), bStock market closed (`40369`), unsupported stablecoin pairs (`40368` or `40370`), no RWA vendor liquidity (`40374`) and an Ondo order below its USD minimum (`40375`). The probe now maps these business codes to fixed labels. It still omits the raw API `msg`, so a `40375` result records that a minimum blocked the quote but **not** the numeric threshold returned in that message. The exact minimum must be captured separately from a safely redacted live response if it matters to the product. No such response has been observed here.
