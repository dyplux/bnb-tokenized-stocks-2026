# Venus Core parity: VAI debt source correction

**Checked:** 2026-10-03 UTC. **Role:** coordinator source review. No account transaction, wallet signature or product code change occurred.

## Source finding

The [Venus v10.3.0 ComptrollerLens](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Lens/ComptrollerLens.sol) calls `vaiController.getVAIRepayAmount(account)` after its entered-market loop when the VAI controller address is nonzero. This amount enters `sumBorrowPlusEffects` for both borrowing-power and liquidation-threshold strategies. The [v10.3.0 VAIController source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Tokens/VAI/VAIController.sol) starts with `comptroller.mintedVAIs(account)` and adds newly calculated interest from the minter index. The two values needn't match.

The bounded Plus Sol draft reviewed on this date proposed adding `mintedVAIs(account)` directly. That instruction is **incorrect** as an exact parity method. It wasn't implemented in the app. The app currently reads only the deployed Core's three-word current risk tuples and displays their signs. It doesn't compute a personal post-action risk forecast.

## Corrected parity boundary

At one pinned BNB Chain block, read `getAssetsIn(account)`, each market's account snapshot, both effective factor strategies, both required oracle price paths and the Core's reference tuples. Read `vaiController()` from the Core. If it is nonzero, query that controller's `getVAIRepayAmount(account)` at the **same block** and add the returned integer after the market loop. Preserve Solidity's multiplication and truncation order. A comparison against `mintedVAIs` alone may agree for an account with no accrued VAI interest and still fail as a general method.

The public governance account previously observed at block 125402171 had five entered markets and positive risk states, but its address and raw balances weren't retained. That observation verifies the nonempty ABI/display path only. A subsequent [bounded parity case](../../research/2026-10-03-venus-core-bounded-arithmetic-parity.md) reproduced both current-state tuples for one pool-0 account. Deployed bytecode equality, a consenting NVDAB holder and a safe post-action forecast remain unproved. This source correction changes the method, not the [D-030 gate](../../decisions/decision-log.md) or the [D-033 product checkpoint](../../decisions/decision-log.md).
