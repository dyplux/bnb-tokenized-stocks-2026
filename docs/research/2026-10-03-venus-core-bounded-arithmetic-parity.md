# Venus Core current-state arithmetic, one bounded account

**Observed:** 2026-10-03 02:34 UTC, BNB Chain block 125405244. Read-only. No wallet connection, signature, transaction or Binance key was used.

## Reproduction

Run `python3 scripts/probe_venus_core_parity.py` from the project root. The standalone Python 3.9 script uses the fourth public account in the [Venus governance voters response](https://api.venus.io/governance/voters?limit=5&page=0) as an ephemeral technical sample. It pins the current BNB block, makes at most 35 public RPC requests and prints no account or market address. Governance voters are a discovery source only; they aren't a list of bStock holders or evidence of product demand. The ordering may change, so a later run can inspect a different account.

The optional `--voter-index` argument selects entries 0 through 4; the default remains index 3. A [bounded follow-up](2026-10-03-venus-parity-sample-bound.md) found three empty Core accounts and one account outside the script's five-market limit. It added no personal-risk evidence.

For each entered market, the script reads the vToken account snapshot, effective collateral factor and liquidation threshold, bounded collateral/debt prices, and spot price at the same block. It applies the multiplication and integer truncation order in the [Venus v10.3.0 ComptrollerLens](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Lens/ComptrollerLens.sol). It reads `vaiController.getVAIRepayAmount(account)` when a controller is configured. This corrects an earlier Plus Sol draft that proposed raw `mintedVAIs(account)`. The [VAIController source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Tokens/VAI/VAIController.sol) can add accrued interest to that raw amount.

The deployed vToken calls in this sample returned six 32-byte words for `getAccountSnapshot`. The Lens source consumes the first four declared return values. The script does the same and counts the two extra words per market without assigning them undocumented meaning.

A first draft of the probe sent vToken and oracle calls to Core Unitroller and compared one raw collateral/debt pair with a net-risk tuple. It was rejected in review before execution. The corrected script targets each returned contract, computes both strategies separately, and compares the exact three-integer net tuples.

## Observed result

| Check | Result |
|---|---:|
| Entered Core markets | 5 |
| Markets with nonzero supply or debt used in both paths | 1 |
| User pool ID | 0 |
| VAI repay amount nonzero | no |
| Borrowing-power reference | positive cushion |
| Liquidation-threshold reference | positive cushion |
| Exact three-integer match, borrowing-power path | yes, delta `[0, 0, 0]` |
| Exact three-integer match, liquidation path | yes, delta `[0, 0, 0]` |
| Public RPC requests | 27 |

This is one exact arithmetic parity case against deployed **current** risk-state calls. It doesn't prove byte-for-byte source equality, E-Mode selection, the nonzero VAI path, or any post-supply/post-borrow state. The earlier [governance-account sample](2026-10-03-populated-core-account-read.md) had zero NVDAB; since its address wasn't retained, this run doesn't prove it inspected the same account or a bStock holder. The [D-030](../decisions/decision-log.md) personal-risk forecast gate remains closed. The [D-033](../decisions/decision-log.md) product checkpoint still requires a consenting holder task, defensible sale costs and a safe account-specific risk boundary.
