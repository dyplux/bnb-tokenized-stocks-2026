# NVDAB cash choice, bounded feasibility check

**Checked:** 2026-10-01. **Status:** market-level research scenario, no wallet, quote or loan. This is input to [D-017](../decisions/decision-log.md), not a user outcome.

## Observed inputs

- At 17:54 UTC the [Venus public market API](https://api.venus.io/markets?chainId=56&limit=100) reported vNVDAB indexed supply of about $341,944, 26 market supplier records, a 60% collateral factor and a 70% liquidation threshold. Its bStock borrow switch was disabled; a supported stablecoin may still be borrowed against supplied NVDAB. The [fixed-block oracle read](2026-10-01-venus-bstock-oracle-check.md) at BNB block 125144831 gave $230.8251696741065 per NVDAB and no active bounded-price divergence. Indexed suppliers needn't be unique borrowers.
- A second read of the same public Venus market API around 19:12 UTC showed vUSDT `borrowApy` of 5.01191213086323874% and indexed available vUSDT liquidity of about $45.03 million. This is a changing market rate and an indexed estimate. The [Venus rate model](https://docs-v4.venus.io/risk/interest-rate-model) is variable, and [Venus's lending documentation](https://docs-v4.venus.io/technical-reference/reference-isolated-pools/vtoken/vtoken) says debt accrues interest and can be liquidated beyond the account threshold.
- [Steward Swipe](https://github.com/zkasuran/steward-bnb/blob/a1ae5cf4153e370d16ef9dd1cd85cb116f0412ba/apps/web/app/api/use/swipe/route.ts) already returns market-level borrow capacity, and [Portir loans](https://github.com/yeheskieltame/portir/blob/761f0df0e04d9fa46f0007cf69c9558ecd434161/apps/web/app/loans/page.tsx) covers lending and a guard. Neither inspected path presents a Binance Web3 sell quote beside a loan for the same cash target. This is a code-scope observation, not proof of a missing feature everywhere.

## One transparent example

Assume exactly **1 NVDAB** at the observed Venus price, no other collateral or debt, no E-Mode, no interest yet and no execution costs. The market-level collateral value is $230.83. At a 60% factor, nominal borrow capacity from this one asset is $138.50. A $100 vUSDT debt would have a nominal liquidation-weighted value of $161.58 and a health ratio of about **1.62**. If the oracle price alone fell while debt stayed $100, a fall of about **38.1%** would bring this simplified ratio to 1.0. Interest, E-Mode, other positions, protocol changes and oracle protections can move that boundary. A $100 loan at the observed 5.0119% rate would accrue about $0.41 in 30 days under a flat-rate simple-interest illustration. The actual future charge is unknown.

The alternative sale would reduce stock exposure but has **no measured proceeds yet**. The prior [Pancake pool quote](2026-10-01-nvdab-sized-pool-quote.md) measures a different route at a fixed block, not a Binance Web3 wallet-bound sell quote. We cannot say which path yields more useful cash or is preferable. A real same-target quote and account-wide Venus state are required.

## Product consequence

The comparison could matter because its two paths leave different exposure and debt. The existing market use makes the instrument real, but the user need and benefit remain unobserved. Build only a read-only, clearly sourced first slice. If the sell route is absent, personal borrow safety can't be calculated, or a holder reaches the same choice in existing interfaces, retire it. No automatic borrowing or trading follows from these numbers.
