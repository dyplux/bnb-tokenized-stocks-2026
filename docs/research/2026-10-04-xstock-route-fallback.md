# BSC xStock fallback: indexed pairs and exact-wallet routes

**Measured:** 2026-10-04 18:56 to 18:57 UTC. **Decision:** no xStock fallback is cleared for the 10 USDT mainnet demo. This is a bounded route check, not a conclusion that xStocks lack BSC liquidity.

## What was checked

The [public Binance listing snapshot](../../data/normalized/xstocks_public.json) contains 130 BSC xStock-labelled contracts. Five calls to DEX Screener's documented [BSC token-pairs API](https://docs.dexscreener.com/api/reference) checked each listed address. All five returned HTTP 200. The [dated allowlisted response record](../../experiments/EXP-RWA-009/xstock_dex_coverage_2026-10-04.json) has request counts, response hashes and three matched pairs. DEX Screener is an indexer, not a complete pool census or an execution simulator.

| Listed token | Indexed pair at that moment | Indexed liquidity / 24h volume | Signed Binance Web3 10 USDT exact-wallet quote |
|---|---|---|---|
| SPCXx | Uniswap pair against an unrelated token labelled `比特币` | $800.27 / $0.67 | Not requested: unsuitable USDT demo pair |
| wPOPMTx | PancakeSwap pair against BSC USDT | $61,459.85 / $244,153.56 | Business `40374`, zero routes |
| wTCENTx | PancakeSwap pair against BSC USDT | $415,835.63 / $111,553.03 | Business `40374`, zero routes |

The two wrapped-token quotes used the existing public demo wallet, BSC chain ID 56, exact listed contracts and 10 × 10^18 raw USDT units. They were signed read-only API calls through the DevEx wrapper. [Their dated results](../../experiments/EXP-RWA-009/wrapped_xstock_fallback_2026-10-04.json) record response hashes and the provider's `Insufficient liquidity for a quote` message. The raw signed responses stay in ignored local storage. This is **Binance Web3 route unavailability for those two requests**, not proof that a direct PancakeSwap transaction would fail or be lawful.

## Why the wrappers need another check

The [xStocks wrapper guide](https://docs.xstocks.fi/developers/wrapped-xstocks) says wrapped xStocks use ERC-4626 shares and warns that the wrapper exchange rate is accounting data, not a standalone price feed. It also warns against assuming an old wrapper version is safe for valuation. Our public listing labels wPOPMTx and wTCENTx as wrappers, but their `asset_type` is null and we haven't confirmed either contract's underlying `asset()`, current-wrapper status, live conversion rate, asset-specific terms or user eligibility. The [ERC-4626 standard](https://eips.ethereum.org/EIPS/eip-4626) requires `asset()` and defines `convertToAssets()` as an idealized conversion, not a fill or a share price. A displayed DEX pair cannot clear those gates.

## Product decision

Keep NVDAB as the **technical preflight target only** because its Binance Web3 quote, unsigned build and off-chain simulation chain has been observed. Keep NVDAon as a second technical route with separate issuer conditions. The xStock fallback remains open for a later direct-route and wrapper audit, but neither wrapped candidate replaces the canonical demo asset today. Do not fund a wallet based on indexed liquidity or an API error message. The unresolved issuer and person eligibility gate applies to every provider independently.
