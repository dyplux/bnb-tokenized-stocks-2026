# Populated Venus Core account, read-only boundary

**Observed:** 2026-10-03 02:11:44 UTC, BNB Chain block 125402171. This was a bounded public technical check. It did not involve a consenting holder, wallet connection, Binance credential, signature or transaction. No candidate address or raw account response was retained in the repository.

## Method and result

The [official Venus API reference](https://docs-v4.venus.io/services/api), checked on 2026-10-03, documents unauthenticated governance voters but no indexed lending-account endpoint. The [official subgraph guide](https://docs-v4.venus.io/services/subgraphs), checked on the same date, points to a BNB Chain Core Pool subgraph through The Graph gateway, which requires an API key. This check did not create or use one.

One `GET /governance/voters?limit=5&page=0` returned five public governance accounts. The existing `read_venus_core_account_state` routine read them sequentially through the official BNB public RPC and stopped at the first nonempty Core position, candidate four. The first three had no entered Core markets, default pool 0 and zero for both aggregate risk states. At block 125402171, the fourth had **five entered Core markets**, pool 0 and `cushion` for both borrowing-power and liquidation-threshold states.

Two direct `eth_call` reads repeated `getBorrowingPower(address)` and `getAccountLiquidity(address)` at that same block. Both returned a valid three-word tuple with error code 0, positive liquidity and zero shortfall. Those raw-state signs agree with the app's two `cushion` labels. A separate same-block NVDAB `balanceOf` returned zero. The public governance list was only a way to discover a technical account; it is not a list of bStock holders or a measure of demand.

## What remains open

This confirms that the current Core ABI and display handle one nonzero account state. It does **not** independently reproduce Venus's borrowing-power arithmetic, verify E-Mode factor selection, match deployed facet bytecode to source, calculate post-supply or post-borrow risk, or prove a holder's cash decision. Since no account identifier was committed, another reviewer cannot directly replay this exact address from this note; the bounded method can be repeated against the current governance list, whose ordering may change.

The [D-030 risk gate](../decisions/decision-log.md) stays closed. A populated technical account reduces the empty-only coverage gap, while the account-specific forecast and the consenting bStock holder task remain unverified.
