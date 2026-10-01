# Binance DeFi positions as a possible account read

**Checked:** 2026-10-02. Documentation review only. No authenticated request or holder account was observed.

## Documented facts

- The [Get DeFi Positions endpoint](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/defi-data) is a signed `POST /build/api/v1/defi/data/position/list`. It accepts up to three addresses and can restrict results to BNB Smart Chain with `binanceChainIds: ["56"]`.
- Binance's [supported-protocol matrix](https://web3.binance.com/en/dev-docs/products/defi-api/supported-chains) lists `venus` in position coverage on BNB Smart Chain. The endpoint groups results by address, protocol, pool and position. `tokenList` can contain `supply` and `borrow` entries; `tokenAmount` is human-readable, not a smallest-unit integer.
- The response has a server timestamp. The documented schema doesn't provide a per-position BNB block number or guarantee that the server timestamp is the source observation time.
- The example contains `positionCollectionDetail.healthFactor` for Lista DAO. Collection metadata may be null. This example doesn't establish a Venus health-factor field or its calculation.
- Binance's transaction-build list includes Venus deposit, redeem and claim. It doesn't list a Venus borrow builder. The current product is read-only regardless.

## Product inference and limits

An observed Venus position could help identify existing supply and debt before displaying a cash-choice scenario. It can't by itself prove post-deposit borrowing capacity, liquidation safety, or a user's eligibility to trade bStocks. A response needs protocol ID, chain, pool and token contracts checked against Venus on-chain state at a nearby block. Missing or stale positions must remain an unknown state, not a zero debt claim.

The signed DeFi read is a candidate after the existing RWA identity and sell-quote gate. First use one consenting holder's public address and `binanceChainIds: ["56"]`; record redacted fields, latency, scope and any mismatch in the Developer Experience Report. Do not add the call to the UI or claim it works before that observation. The project has no complete local Binance Web3 key pair as of this check.
