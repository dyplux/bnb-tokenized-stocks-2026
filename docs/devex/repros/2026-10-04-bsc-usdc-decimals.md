# Successful quote for the wrong economic size

**Observed:** 2026-10-04. A first eight-call read-only ladder intended to quote 10, 100, 1,000 and 10,000 USDC against MSTRB and NVDAB used `amount = size × 10^6`. All eight calls returned business code 0 and a route, but a subsequent sanitized live quote showed BSC USDC `fromToken.decimal=18`, `fromTokenAmount=10000000`. The input was 0.00000000001 USDC, not 10 USDC. Those observations are preserved as [`invalid_input_units_2026-10-04.csv`](../../../experiments/EXP-RWA-009/invalid_input_units_2026-10-04.csv) and must never be cited as size-depth evidence.

The [Trading API documentation](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says `amount` is the token's smallest unit, but its example uses a 6-decimal USDT. That example is not a substitute for reading the actual chain/token metadata. The API did not reject the tiny input and returned a valid route. A successful business code alone cannot validate the intended economic amount.

**Correction:** `scripts/quote_depth.py` now scales BSC USDC by `10^18`, checks the response's `fromToken.decimal` and echoed raw input, and writes the corrected results to [`quote_depth.csv`](../../../experiments/EXP-RWA-009/quote_depth.csv). The eight corrected calls were made at 10:36:14 to 10:36:17 UTC, all with business code 0 and one route. They remain estimates from an ephemeral nonholder address, without a build, simulation, signature or fill.

**Suggested improvement:** make the quote documentation state that token decimals are chain-specific and show BSC USDC/USDT examples alongside the existing 6-decimal example. A response field carrying parsed human input amount would make accidental micro-quotes easier to catch.
