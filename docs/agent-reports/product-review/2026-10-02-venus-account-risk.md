# Venus account-risk review

**Objective:** test whether the provisional sell-or-borrow product can estimate risk after a new NVDAB supply and USDT borrow. **Role:** bounded read-only Sol CLI review on 2026-10-02. No code, API call or holder session was delegated.

## Work and sources

The reviewer read the [one-page spec](../../product/one-page-spec.md), [existing account boundary](../../research/2026-10-01-venus-account-state-boundary.md), local server and three official Venus v10.3.0 source files: [PolicyFacet](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol), [MarketFacet](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/MarketFacet.sol) and [ComptrollerLens](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Lens/ComptrollerLens.sol). Those files were fetched on 2 October. The review used no browser or credentials.

## Facts and inference

PolicyFacet provides separate current account borrowing-power and liquidation-liquidity reads. MarketFacet provides effective factors tied to the account's pool. ComptrollerLens uses bounded oracle prices for the collateral-factor path and spot prices for the liquidation-threshold path. The public hypothetical method has no new-supply parameter. Source-level details and caveats are in the [feasibility note](../../research/2026-10-02-account-wide-risk-feasibility.md).

**Inference:** current aggregate net cushions plus exact marginal NVDAB and USDT values might support a post-action cushion estimate, but do not provide gross debt/collateral, a health factor or a token-specific liquidation price. The reviewer recommended a current-account notice as the smallest possible next slice, followed by a full forecast only if a holder case and contract checks justify it.

## Counterargument, dissent and decision impact

A current-account notice alone doesn't finish the user's sell-or-borrow task. The reviewer agreed that the candidate remains weak without a signed sale quote and account-aware result. The coordinator accepts the limit and keeps the [D-017](../../decisions/decision-log.md) stop rule. No new risk calculation is approved for the interface from this source review alone.

## Unknowns and next step

The deployed facets and oracle paths still need a fixed-block check. No nonempty consenting account, E-Mode case, post-deposit result or Venus UI comparison has been observed. CLI remaining quota was not shown; its token count was not retained from the truncated terminal output. The next useful gate is the permitted signed Binance Web3 quote and a holder task, then a bounded current-account read if the candidate survives.
