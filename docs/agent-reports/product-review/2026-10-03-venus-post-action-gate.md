# Venus post-action risk gate

**Date:** 2026-10-03 UTC. **Role:** Plus Sol, read-only. **Question:** can this product show an account-specific result after a proposed NVDAB supply and USDT borrow before the 11 October deadline?

## Evidence reviewed

The reviewer read the [one-page spec](../../product/one-page-spec.md), [account-state boundary](../../research/2026-10-01-venus-account-state-boundary.md), [account-wide feasibility note](../../research/2026-10-02-account-wide-risk-feasibility.md), [deployed risk read](../../research/2026-10-02-venus-deployed-risk-read.md) and current [status](../../status.md). It checked the [Venus Core PolicyFacet source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol) and [E-Mode documentation](https://docs-v4.venus.io/whats-new/e-mode) on 2026-10-03. It made no code edit, holder lookup, signed API request or contract call. The CLI did not expose a reliable remaining quota or the signed-in email.

## Finding

Venus's `getBorrowingPower(account)` and `getAccountLiquidity(account)` return two current aggregate net states using different factors and price paths. They are not gross collateral, debt, health factor or liquidation price. `getHypotheticalAccountLiquidity` models redemption and borrowing but has no new-supply input. A wallet's outside NVDAB balance cannot be inserted into that function as if it were supplied collateral.

A read-only post-action estimate is technically plausible: at one block, read both current net states, entered markets, selected E-Mode pool, effective NVDAB collateral and liquidation factors, bounded and ordinary oracle prices, exact proposed supply and borrow amounts, vToken conversion, cap headroom, pool cash and relevant pauses. Then apply Venus's integer operation order separately to the two net states. The result could be labelled only as estimated post-action **net cushions at that block**, conditional on NVDAB entering collateral and on the separate supply and borrow succeeding. It couldn't certify either transaction or describe a safe loan.

The deployed risk facet has returned the expected three-word tuple for empty/default accounts, but its bytecode has not been matched to the reviewed source. No populated account has been used to reproduce the arithmetic or E-Mode selection. The present app reads current net states as labels and leaves the borrow scenario isolated. The reviewer recommends a populated-account parity check and deployed-source check before any personal estimate. A public populated account would narrow technical uncertainty, but wouldn't establish consent, eligibility, demand or the user's decision. No address was obtained in this review.

## Counterargument and decision impact

Even perfect local arithmetic would combine proposed supply, market entry and borrow as if no block state changed between them. Approval, accrual, oracle movement, caps and transaction policy could change the result. The strongest defensible claim would remain a dated conditional estimate, not a promise of execution or future safety.

The coordinator keeps the [D-017](../../decisions/decision-log.md) cash-choice task provisional. A personal post-action result is not approved for display. A bounded deployed-source and populated-account parity study can continue without a transaction; if it cannot be completed promptly, the 4 October checkpoint must narrow or retire the cash-choice claim instead of presenting the isolated scenario as personal guidance.
