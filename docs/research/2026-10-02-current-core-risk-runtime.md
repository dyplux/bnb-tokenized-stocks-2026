# Current Venus Core risk-state runtime check

**Date:** 2026-10-02 UTC. **Scope:** public BNB Chain RPC, read-only calls, no Binance credential or transaction.

The application read `getBorrowingPower(address)` and `getAccountLiquidity(address)` through the Venus Core Unitroller at the same pinned block as `getAssetsIn(address)` and `userPoolId(address)`. The [implementation spec](../product/current-core-risk-notice-spec.md) records the selectors, three-word ABI and fail-closed handling. The [Venus PolicyFacet source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol) supplies the distinction between borrowing-power and liquidation-threshold weighting.

| Read | BNB block | Block time UTC | Core borrowing-power state | Core liquidation-threshold state | Entered Core markets | Pool |
|---|---:|---|---|---|---:|---:|
| Zero address, technical placeholder | 125365389 | 2026-10-02 21:35:47 | zero | zero | 0 | 0 |
| Documented Venus Treasury address | 125365393 | 2026-10-02 21:35:49 | zero | zero | 0 | 0 |

A local Chrome run then opened the app at 320 and 1440 CSS pixels, entered the zero address and requested the optional Core read. At blocks 125365781 and 125365785 respectively, both states displayed **Zero reported**. Neither width had horizontal overflow or a page error. The browser used the public RPC; it did not request a Binance quote.

These observations verify the deployed ABI's empty/default path and the local display. The Treasury's separate vNVDAB balance does not make it entered collateral. Neither address is a consenting holder case or a populated borrow position. No gross debt, health factor, post-deposit risk, account-wide recommendation, transaction or user outcome was tested. A real holder's task and account state remain open gates.
