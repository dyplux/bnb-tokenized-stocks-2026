# Unsigned bStock build and off-chain simulation, 4 October 2026

**Experiment:** EXP-RWA-009. **Origin:** LIVE signed Binance Web3 API calls between 13:19 and 13:21 UTC. No user key, approval, signature, order submission or on-chain broadcast was used.

## Reproduction

Run `python3 scripts/probe_swap_build.py` and `python3 scripts/probe_swap_simulation.py` with a locally configured Binance Web3 API key. Each script creates a fresh temporary, unfunded wallet address and discards it. Both request a 100 USDT to CBRSB quote on BSC. The build uses the quote's `quoteId` within its documented ~30-second lifetime and a 0.5% maximum slippage input. The simulation submits the unsigned `tx` payload to the off-chain simulation endpoint. Request credentials, wallet and transient quote ID aren't stored in committed artifacts.

The [build result](../../../experiments/EXP-RWA-009/cbrsb_unsigned_build.json) records one `LiquidMesh` route, `executionMode=SWAP`, a successful unsigned build, `tx` present and 2,564 bytes of calldata. The [simulation result](../../../experiments/EXP-RWA-009/cbrsb_unfunded_simulation.json) records a second successful build and a successful **API call** to `/api/v1/dex/pre-transaction/simulate`. Its predicted **transaction outcome** was `FAILED`, with `execution reverted: BEP20: transfer amount exceeds balance`. The API result and predicted transaction result must be displayed separately.

The local raw-response manifest keys each request by SHA-256. The retained raw bodies remain outside Git because they include a temporary wallet address, quote identifiers and unsigned calldata. Sanitized per-call request and response shapes, timing, HTTP and business codes are in `docs/devex/raw/2026-10-04.jsonl`.

## Documentation conflict

The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api), checked 4 October 2026, says equity/RWA routes always return `RFQ` under the quote and build response descriptions. Two live CBRSB quotes and builds instead returned `SWAP` with an EVM `tx`. Earlier NVDAB quotes had the same discrepancy. The [Trading introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) already describes bStock SWAP. Suggested correction: describe both route types, the vendor and liquidity conditions that select them, and the correct client action for each. Don't require an RFQ signing path merely because the token is an equity representation.

The quote's `estimateGasFee=450000` matches the built transaction's `gas=450000`, while the build separately reports `gasPrice=60792248` wei. This supports interpreting the quote field as a gas-limit estimate for this route, rather than a fee already denominated in wei. Confirm the units in the [Trading API schema](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api); don't display `450000` as a monetary gas cost. No gas was paid.

## Boundary

This is a 100 USDT route for an unfunded, ephemeral address. The failure is expected from missing balance. It doesn't establish that a funded person in any jurisdiction may trade CBRSB, that approvals would succeed, or that an order would fill at the quoted amount. The build only produces unsigned transaction data. The off-chain simulation doesn't submit it to BSC.
