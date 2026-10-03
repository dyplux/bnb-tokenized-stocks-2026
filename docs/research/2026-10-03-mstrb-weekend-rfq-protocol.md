# Saturday MSTRB quote roundtrip protocol

**Prepared:** 2026-10-03 UTC, before the six planned signed GETs. **Purpose:** test whether a BNB Chain user can obtain amount-sized MSTRB/USDT quotes on a Saturday and measure the indicative buy-to-sell loss at three sizes. This is not an alpha test or a trade.

## Fixed inputs

- BNB Chain ID 56; [Binance public bStock list](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3) identified `MSTRB` as `0xe87afb3076aeb0f9b14e368de8145ae6a2826a14` on 2026-10-03. Canonical USDT is `0x55d398326f99059ff775485246999027b3197955`. Public `eth_call decimals()` returned 18 for each on chain 56 before the calls.
- Use one fresh random temporary address. Check its MSTRB and USDT `balanceOf` by public RPC. It must have zero of both; no private key is generated or used.
- Buy inputs: exactly **25, 100 and 500 USDT** in raw 18-decimal units. For each successful buy, request one inverse MSTRB-to-USDT quote using the `toTokenAmount` raw integer from the selected buy route. Skip the inverse on an error or if no route passes identity checks. Maximum six signed GET quote calls; no retry.

## Selection and capture

Use the existing [sanitized quote probe](../../scripts/probe_binance_quote.py). Accept HTTP 200, business code 0 and a route only when the returned token contracts match the requested direction, both decimals are 18 and `fromTokenAmount` matches the exact input. Select the unique `isBest=true` route. If the flag is absent and there is one route, select that sole route; otherwise mark the case ambiguous and skip its inverse. Preserve capture UTC, latency, route count, vendor, execution mode, raw amounts, `tradeFee`, `estimateGasFee`, `priceImpactPercent` and errors. The [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes `toTokenAmount` as a smallest-unit integer and a per-route quote ID with about 30 seconds TTL; the sanitizer intentionally does not expose quote IDs, so no actual expiry is measured.

## Interpretation

The inverse is a new quote at a later time, not a guaranteed roundtrip execution. Compare `inverse USDT estimate / initial USDT input` only as an indicative, time-separated quote ratio before gas, approvals, price movement and fill. A profitable or unprofitable trade, investor eligibility, issuer redemption, available wallet balance and net PnL cannot be inferred. Record error codes and no-route states; do not store the temporary address, credentials, headers, quote ID or raw response in Git. No build, simulation, approval, signature, broadcast or order.
