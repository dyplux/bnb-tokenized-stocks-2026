# Steward Swipe, live borrow plan for the same cash task

**Observed:** 2026-10-03 at 02:57 UTC  
**Method:** clean headless Chrome session on the [public Steward dashboard](https://bnb-tokenized-stocks.vercel.app/). Opened `Use`, selected NVDAB, entered 1 unit, changed target health factor and pressed `Quote borrow`. No wallet was connected and no transaction was sent. The [public repository](https://github.com/zkasuran/steward-bnb) links the deployed dashboard.

## Visible output

| Input | BNB block | Collateral value | Max safe borrow | Fundable now | Health factor |
|---|---:|---:|---:|---:|---:|
| 1 NVDAB, target HF 2.0 | 125408210 | $234.56 | $82.09 | $82.09 | 2.00 |
| 1 NVDAB, target HF 1.6 | 125408215 | $234.56 | $102.62 | $102.62 | 1.60 |

The block timestamps were read separately from the [BNB Chain public RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/): 02:57:02 and 02:57:04 UTC. Steward also displayed a $140.73 protocol borrow cap, $0 existing USDT debt and about $43.7 million of pool USDT availability in both results. Its screen says the figures are plan-only and that its reference data may be live Binance RWA data or a labelled mock. This observation did not independently confirm which reference mode was active.

## What this changes

[O] Steward already gives a live, adjustable NVDAB borrow plan. At target HF 1.6, its visible amount exceeds the 100 USDT cash target used in our illustrative task. A generic borrow-capacity card would duplicate this experience.

[O] In the exercised `Use` flow, no field requested a USDT cash target and no target-sized Binance sale quote appeared beside the borrow plan. This is a bounded screen observation, not proof that the whole product lacks such a path.

[?] The page had no connected holder account. Its $0 existing debt is a default scenario, not a measured personal position. No deposit, loan, sale, approval, execution cost or user decision was observed.

[I] The remaining same-cash comparison hypothesis is narrower than the earlier source-only check suggested. To demonstrate useful differentiation, an eligible holder must complete the same task in both tools and explain what decision changes after real sale costs and personal Venus risk are shown. This observation does not approve a product change before the 4 October checkpoint.
