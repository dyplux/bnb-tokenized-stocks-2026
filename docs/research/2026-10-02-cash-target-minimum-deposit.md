# Minimum collateral for one cash target

**Checked:** 2026-10-02. **Scope:** read-only Venus market illustration. No wallet position, deposit, borrow, Binance Web3 response or executed trade was observed.

## Why this calculation was added

At BNB block 125201341, the [Steward scenario check](2026-10-02-steward-supply-cap-comparison.md) showed 25 NVDAB entered while Venus Core had 20.039492377880186433 NVDAB of supply-cap headroom. The entered 25-unit deposit exceeded that headroom. It didn't follow that a smaller deposit couldn't support the user's cash target. The earlier Dyplux warning needed to distinguish those cases.

## Method

The indexed [Venus markets API](https://api.venus.io/markets?chainId=56&limit=100) supplies NVDAB and Core USDT price mantissas, the NVDAB base collateral factor and the supply cap. [Venus's collateral documentation](https://docs-v4.venus.io/guides/liquidation) describes the factor as the share of supplied asset value counted toward borrowing power. Price mantissas use `10^(36 - underlying decimals)` scaling in the [protocol math guide](https://github.com/venusprotocol/venus-protocol-documentation/blob/main/guides/protocol-math.md).

For one isolated NVDAB deposit and a target stated in USDT base units, the exact lower bound is:

```text
required_nvdab_raw = ceil(
    cash_usdt_raw * usdt_price_mantissa * 10^18
    / (nvdab_price_mantissa * collateral_factor_mantissa)
)
```

The server uses integer division with a ceiling, then compares `required_nvdab_raw` with `headroom_raw`. It also compares the **entered** NVDAB units with that same headroom. Both pinned assets require 18 decimals; noninteger oracle or factor mantissas are rejected. The displayed token amount is formatted from raw integer units, without rounding it down for presentation. The test fixture gives 20 NVDAB exactly for a 2,760 USDT target; increasing the target by one USDT base unit requires 20.000000000000000001 NVDAB and fails a 20-unit cap.

This is a lower bound at the indexed base factor, with no interest, safety buffer, gas, fees, E-Mode or existing account debt. It isn't a recommended deposit. The indexed cap may lag the chain. A borrower also needs adequate USDT pool cash, a working market and a safe account-wide state. The comparison never tells a user that they can execute a loan.

## Local observation

At about **01:36 UTC** on 2026-10-02, local Chrome at 375 and 1440 CSS pixels fetched the current Venus market scenario for **25 NVDAB** entered and a **100 USDT** target. The app displayed an exact collateral-only minimum of **0.718945909667247557 NVDAB**. It labelled the entered 25 units above indexed headroom and the smaller minimum within it. Neither viewport had a JavaScript page error or horizontal overflow. The live indexed inputs can change; this observation isn't a fixed-block contract result or a holder test.

**Clock correction:** the local server log showed 02:36 in Lisbon summer time (WEST, UTC+1). The first report called that value UTC. The time above is the converted UTC observation.

The sale path remained **Unquoted**. A separate, permitted signed Binance Web3 quote and account-wide Venus risk assessment remain gates for an actual sell-or-borrow decision.
