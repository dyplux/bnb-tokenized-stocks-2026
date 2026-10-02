# Fractional NVDAB quote for a 100 USDT target

**Observed:** 2026-10-02, 22:08 to 22:10 UTC. **Purpose:** check whether a sale of part of a 1 NVDAB example can be quoted near the same 100 USDT cash target used by the Venus borrow scenario. These are technical reads bound to temporary nonholder addresses. No holder, signer, approval, simulation, trade or loan was involved.

## Bounded reads

The first two direct invocations of the application quote function passed the Python string `"0.43"` where the HTTP handler normally passes a `Decimal`. Each authenticated the exact NVDAB identity, then failed before the Trading API call with the local `bsc_rpc_or_amount_error` label. A separate public BNB RPC read returned chain 56 and a block number. The failure was a probe invocation error, not evidence of a Binance or BNB RPC outage. The corrected third invocation passed `Decimal("0.43")`.

| Read | Result |
|---|---|
| Corrected signed RWA search and 0.43 NVDAB sell quote | Identity verified; one LiquidMesh `SWAP` route; quote captured 22:08:37.136 UTC; quote latency 305.322 ms; metadata block 125369760 |
| Quote amount | `430000000000000000` raw NVDAB units, estimated output `100663406831290082054` raw USDT units, or **100.663406831290082054 USDT before final costs** |
| Separate signed RWA token-price read | HTTP 200, business code 0; 570.429 ms; captured 22:10:08.936 UTC. One exact BNB Chain 56 bStock NVDAB row with `tokenPrice=233.93000000` USD and `tokenPriceUpdatedAt=1790979003633` ms. This was a later price read, not a simultaneous execution benchmark. |

The [Binance Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) accepts a sell-token `amount` in smallest units and labels `toTokenAmount` as estimated output. It has no exact-output cash-target parameter. The [RWA price endpoint](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) offers `tokenPrice` and an update timestamp; that price can seed an amount estimate, but the route quote remains the test of that amount.

## Product consequence and limits

For a 1 NVDAB example, the present UI quotes all 1 NVDAB and compares its output with a 100 USDT loan. That isn't a same-cash comparison. The fractional quote shows that a smaller sale can be quoted close to 100 USDT. A working target-aligned flow must separate **NVDAB holding considered for collateral** from **NVDAB units quoted for sale**, size the latter from live data, then show whether its fresh estimated output reaches the cash target before costs. It must never imply that a target is guaranteed, or that 0.43 is a standing recommendation.

This one quote does not establish net USDT received, allowance, gas paid, available holdings, eligibility, liquidity over time or a user preference for sale versus debt. A price-based seed can miss the target; a live first quote with a bounded second quote is the stronger design candidate. Any extra API calls need an explicit per-click bound and failure state.
