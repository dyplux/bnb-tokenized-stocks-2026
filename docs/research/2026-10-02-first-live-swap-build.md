# First live Binance Web3 bStock SWAP build

**Observed:** 2026-10-02 21:50:27 UTC. **Scope:** one signed quote followed by one signed `GET /swap`; no approval request, wallet signature, simulation, order or broadcast.

## Method and sanitized result

The existing server signing helper used the ignored project credentials for one 1 NVDAB to BNB Chain USDT quote bound to a fresh temporary nonholder address. The script accepted only one chain-56 LiquidMesh `SWAP` route with the exact 1e18-unit input, expected NVDAB/USDT contracts and 18-decimal metadata. It passed that route's short-lived `quoteId` to `/swap` in memory, with the same address, contracts and amount and `slippagePercent=0.5`. The address, quote ID, signed URL, headers and calldata were not printed or saved.

| Step | HTTP / business code | Latency | Selected fields |
|---|---|---:|---|
| `/quote` | 200 / 0 | 771.321 ms | One LiquidMesh `SWAP` route; `estimateGasFee=450000`; `tradeFee=0.03371889` USD estimate |
| `/swap` | 200 / 0 | 394.610 ms | `routerResult` matched vendor, input and estimated output from the quote; `tx` was present with sender matching the temporary address and nonempty calldata. `tx.gas=450000`, `tx.gasPrice=107761879` wei and `tx.minReceiveAmount=232977404098026021909` raw USDT units. No `rfq` object. |

The [Trading API introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) documents this quote-to-swap path for bStock LiquidMesh. The [endpoint reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) calls `tx.gas` a gas-limit estimate and `gasPrice` wei. In this response, quote `estimateGasFee` exactly matched `tx.gas`, so treating `450000` as a paid wei fee would be wrong for this observation. `tradeFee` remains an estimated network fee in USD. The built transaction also supplies a minimum receive at the requested slippage, not a guaranteed final amount.

## What remains unproved

The temporary address had no known NVDAB balance, BNB for gas, signer or allowance. A successful build does not show that it would pass `eth_call`, be accepted on-chain, settle, or deliver the quoted USDT. The quote expires quickly. No holder's need or alternative venue was observed. The app's main sale card remains Unquoted and no sell-versus-borrow recommendation follows from this test.
