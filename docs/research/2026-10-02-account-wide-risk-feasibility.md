# Account-wide Venus risk feasibility

**Checked:** 2026-10-02. **Method:** read-only source review of the [Venus Core PolicyFacet v10.3.0](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol), [MarketFacet v10.3.0](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/MarketFacet.sol) and [ComptrollerLens v10.3.0](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Lens/ComptrollerLens.sol). A bounded Sol CLI reviewer inspected those files and the local spec. No new live contract call, holder position or signed Binance response was used. The source version is not proof that every currently deployed selector has the same implementation.

## What the source establishes

- `PolicyFacet.getBorrowingPower(account)` computes a current aggregate net position using collateral-factor weights. `getAccountLiquidity(account)` computes another using liquidation-threshold weights. Each returns an error code, liquidity and shortfall. The result is a **net cushion**, not gross collateral and debt totals.
- `MarketFacet.getEffectiveLtvFactor(account, vToken, weightingStrategy)` chooses a factor for the account's selected Core/E-Mode pool. A market-level base collateral factor cannot stand in for this account-specific value when its pool differs.
- In `ComptrollerLens._calculateAccountPosition`, the collateral-factor path uses `deviationBoundedOracle.getBoundedPricesView` with separate collateral and debt prices. The liquidation-threshold path uses `oracle.getUnderlyingPrice`. One spot price cannot safely represent both paths when bounded pricing differs.
- `getHypotheticalAccountLiquidity` accepts hypothetical redemption and borrowing, with no new-supply argument. `mintAllowed` separately checks listing, pauses and supply cap. `borrowAllowed` checks pauses, pool permission, membership, borrow cap, bounded prices and collateral shortfall. A displayed cushion cannot certify a transaction.

## Feasible estimate, still unproved in a holder case

An account-aware **post-action net-cushion estimate** appears mathematically possible: at one BNB Chain block, read both current aggregate results, the account's effective NVDAB collateral and liquidation factors, the corresponding NVDAB and USDT on-chain oracle prices, and the exact raw deposit and borrow amounts. Convert each current `(liquidity, shortfall)` pair to a signed net, add the marginal NVDAB collateral value and subtract the USDT debt value using Venus's integer truncation. This is an inference from the reviewed code, not an implemented or validated product result.

The aggregate net values alone cannot yield a conventional health factor, gross debt, gross collateral, or the price drop at which a specific account would be liquidated. A full forecast would need account positions and policy checks. A new supply also needs the market to be entered as collateral; minted vToken rounding, changing oracle prices, accrued interest, cap consumption and a later execution block can change the outcome. The existing [indexed scenario](../../app/server.py) deliberately lacks these inputs and remains hypothetical.

## Product decision for the next slice

The current optional Core read reports entered-market count and selected pool. If the signed Binance sale path succeeds, a small follow-up may show the **current** aggregate borrowing and liquidation cushions with block, source and error state, while keeping post-deposit personal feasibility unknown. Do not build or display a post-action personal forecast yet. First verify live facet routing and ABI against the deployed Unitroller, then reproduce a nonempty consenting holder case against Venus's own interface. The quote and holder gates in [D-017](../decisions/decision-log.md) still decide whether this product should continue before the 11 October deadline.
