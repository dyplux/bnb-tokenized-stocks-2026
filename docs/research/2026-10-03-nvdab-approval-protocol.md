# Read-only NVDAB approval construction protocol

**Prepared:** 2026-10-03 UTC before the call. **Purpose:** find out whether the Binance Web3 approval builder accepts the observed LiquidMesh `SWAP` vendor for NVDAB, and what spender, gas limit and gas price it returns for the previous 100 USDT candidate size. This is one signed GET only, with no wallet signature or transaction.

## Fixed request

- Chain ID `56`.
- Token contract NVDAB `0x02fca66c1d1afb4e2a7884261eb00f63598a7436`, already verified in the dated signed RWA search.
- `approveAmount=426034167623447674` raw NVDAB units, the [previous 100 USDT candidate](2026-10-03-target-minimum-check.md). This historical candidate isn't a fresh quote.
- `vendor=LiquidMesh`, the vendor returned by the observed route.
- Endpoint: signed Binance Web3 Trading API `GET /api/v1/dex/aggregator/approve-transaction`. No retry.

## Capture and boundary

Record UTC, HTTP and business code, latency, returned transaction count, `dexContractAddress`, `gasLimit` and `gasPrice`. Verify any calldata has ERC-20 `approve(address,uint256)` selector `0x095ea7b3`, the same spender and exact raw amount. Do not save calldata, signature, headers, credentials or wallet address. If response shape is unexpected or the vendor is rejected, record that and stop.

The [official reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says the vendor selects the route-specific spender, and calls the returned gas limit a ceiling. A successful builder response does not establish that a particular holder needs approval, has enough BNB, can complete the route or pays the full limit. No signed wallet approval or broadcast is in scope.
