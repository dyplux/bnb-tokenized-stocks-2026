# NVDAB cap pressure: what the public reads establish

**Checked:** 2026-10-03 UTC. **Question:** did the near-full Venus Core vNVDAB supply cap prevent real users from depositing?

## Observed

- [P] The local fixed-block reader queried deployed BNB Chain Core and vNVDAB contracts through the [public BNB Chain RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/). At block `125411406`, `2026-10-03 03:21:01 UTC`, cap headroom was `11.416397058476516341 NVDAB`. A one-unit amount fit the cap arithmetic at that block. The same value was observed at blocks `125335595` and `125394235` in the [earlier screen](2026-10-02-bstock-collateral-cap-screen.md). This measures one contract precondition, not a successful deposit.
- [P] The [Venus BNB Core vToken reference](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/technical-reference/reference-core-pool/vtoken.md), checked 2026-10-03, says ERC-20 `mint(uint256)` can return a nonzero protocol error code without an EVM revert. Transaction success alone therefore cannot classify a mint as successful. Source behavior still has to be checked against the deployed implementation for any specific receipt.
- [O] A bounded search of public explorers and the configured public RPC did not yield a reliable list of failed vNVDAB mint calls. The BNB public RPC's `eth_getLogs` limitation was recorded in the [account-source check](2026-10-03-populated-account-source-check.md). A missing result from these routes is not evidence that there were no attempts.

## Prepared measurement

The [Dune query](queries/nvdab-mint-call-outcomes.sql) isolates calls to the pinned vNVDAB address with the `mint(uint256)` selector for a fixed 28-hour window. It returns call and transaction success flags, raw output and revert fields for at most 200 rows. The selector is computed from the function signature within Dune. [Dune's BNB trace schema](https://github.com/duneanalytics/docsV2/blob/master/data-tables/evm-blockchains/raw-data/chains/bnb-chain-bsc/traces.md) describes these columns; [DuneSQL documentation](https://docs.dune.com/query-engine/Functions-and-operators/varbinary) defines the byte-prefix and Keccak functions. **The query has not been run or syntax-checked in Dune.** If its schema differs from the current catalog, correct it after preserving the exact error.

A returned zero code can support a completed call only when the trace and receipt match the deployed ABI and logs. A nonzero code or revert needs the relevant Venus error/log context before it can be attributed to the cap. Routed calls and `mintBehalf` may require separate inspection. Even confirmed failed mints would count transactions, not consenting users or demand for this product.

## Product consequence

[I] The near-full cap remains a constraint on scale, but no observed failed-deposit demand changes D-017. The 4 October 12:00 UTC holder, sale-cost and personal-risk checkpoint in [D-033](../decisions/decision-log.md) remains the decision gate. The query can inform later market selection; it cannot replace that gate.
