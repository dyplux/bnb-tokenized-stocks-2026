# Current Venus Core risk notice, bounded slice

**Decision context:** D-017 permits a read-only cash-choice prototype. Signed Binance RWA search and quote succeeded on 2026-10-02. The [source review](../research/2026-10-02-account-wide-risk-feasibility.md) and [deployed selector read](../research/2026-10-02-venus-deployed-risk-read.md) support a narrow current-account notice, but no consenting holder case or post-deposit forecast exists.

## User task

A person enters a public BNB Chain address to see whether that account already has Venus Core borrowing or liquidation shortfall before considering the separate NVDAB collateral illustration. The existing Venus scenario remains market-level. This notice observes only current aggregate Core results at one block.

## Data and UI

- Reuse the optional `/api/venus-account` request and its existing wallet input. After chain 56, Unitroller code, entered markets and selected pool are checked at one block, call `getBorrowingPower(address)` selector `0x528a174c` and `getAccountLiquidity(address)` selector `0x5ec88c79` on the same Unitroller and block. Their deployed routing and three-word ABI were observed on 2026-10-02. [PolicyFacet source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol) defines the first with collateral-factor weighting and the second with liquidation-threshold weighting.
- Decode exactly three 32-byte unsigned words: error, liquidity, shortfall. Reject a nonzero error or malformed result. Reject both liquidity and shortfall positive in one result. Classify each as `cushion`, `shortfall`, or `zero` without converting undocumented raw units to USD.
- In the optional panel, show two short lines: current Core borrowing-power state and current Core liquidation-threshold state, with the existing block and time. Use plain descriptions, such as “Positive current cushion”, “Current shortfall”, or “Zero reported”. Keep them separate from the hypothetical borrow card.
- A Core RPC failure leaves these states Unknown and does not replace them with indexed Venus API values. Do not return the wallet address, market addresses, raw balances, debt or signed headers in the JSON or logs.

## Acceptance

1. Both reads use the same pinned block as Core membership and pool selection.
2. Malformed three-word data, nonzero error code or internally inconsistent values fail closed.
3. Empty account returns two `zero` states; a synthetic account with nonzero results displays the corresponding state, without a health factor or USD amount.
4. The UI has clear loading, error and Unknown states in the existing optional section. A failed read cannot display stale prior results.
5. The main sell and borrow decision remains unquoted/illustrative, and the notice says a current net cushion is not a post-deposit borrowing or liquidation forecast.
6. Relevant local tests cover exact ABI, same-block calls and error states. A public zero/Treasury read may verify runtime response shape; it cannot replace a consenting holder task.

No transaction, deposit, borrow, order, DNS or deploy belongs in this slice. The 4 October product checkpoint remains in force.
