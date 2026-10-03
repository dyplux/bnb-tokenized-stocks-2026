# Plus Sol checkpoint evidence review

**Reviewed:** 2026-10-03 UTC. Read-only review of the cited local evidence.

## Evidence packet for 2026-10-04 12:00 UTC

### Exact user task

**[Hypothesis]** The target user is an eligible self-custody NVDAB holder who needs a chosen amount of USDT and is deciding whether to:

- sell enough NVDAB for that cash target, or
- supply NVDAB to Venus and borrow the same USDT amount without accepting intolerable debt and liquidation risk.

The intended result is a source-dated, same-cash comparison. The user makes the decision and the app executes nothing. No consenting holder has confirmed this task. [One-page spec](../../product/one-page-spec.md)

**[Inference]** The current workaround is to obtain sale information from Binance or another trading venue, obtain borrowing information from Steward or Venus, and reconcile the amounts, costs, remaining exposure, debt, and risk manually. D-017 selected the product only as a provisional read-only slice. [D-017](../../decisions/decision-log.md)

### What current evidence proves

**[Fact]**

- Signed Binance RWA identity and quote requests worked. An unsigned LiquidMesh SWAP payload was built for a temporary nonholder address. This proves a working technical Binance Web3 integration, not holder utility or execution. [Readiness gates](../../submission/readiness-gates.md)
- For the illustrative 100 USDT target, the quote estimate was `100.000443760010104468 USDT`, but the transaction minimum at 0.5% slippage was only `99.500441541210053945 USDT`. The estimated output therefore cannot be presented as guaranteed receipt of 100 USDT. [Cost boundary](../../research/2026-10-03-binance-sale-cost-boundary.md)
- One public Venus Core account produced exact matches for both deployed current-risk tuples. This validates one current-state arithmetic path. [Venus parity result](../../research/2026-10-03-venus-core-bounded-arithmetic-parity.md)
- Steward’s public UI produced a live NVDAB borrowing plan. For 1 NVDAB, it showed `82.09` fundable at target health factor 2.0 and `102.62` at 1.6. [Steward observation](../../research/2026-10-03-steward-live-swipe-same-task.md)
- The observation protocol records zero eligible-holder sessions. Product readiness remains “Not ready.” [Readiness gates](../../submission/readiness-gates.md)

### What the evidence cannot prove

**[Unknown]**

- Whether a consenting eligible holder has this task or would change an action after using the comparison.
- Holder-specific net sale proceeds, including actual fill, gas used, approval requirements, and final wallet balance.
- A safe personal post-supply and post-borrow result. The parity case does not cover post-action state, E-Mode, nonzero VAI debt, or a bStock holder. [Venus limitations](../../research/2026-10-03-venus-core-bounded-arithmetic-parity.md)
- Whether the combined comparison is clearer or more useful than completing the task through existing tools.
- Product demand, financial advantage, or readiness for public deployment or submission.

### Strongest competitor counterexample

**[Fact]** Steward is a working borrow-side substitute, not merely source-code overlap. Its public flow already turns NVDAB units and a chosen health factor into a live fundable amount, and its 1.6-health-factor result exceeded the project’s illustrative 100 USDT need. No wallet or transaction was involved, so this was still a default scenario rather than a personal result. [D-036](../../decisions/decision-log.md)

**[Inference]** A generic NVDAB borrowing-capacity card would duplicate Steward. The only remaining proposed distinction is placing a target-sized sale estimate beside the borrowing path. That distinction remains unproven unless it changes a consenting holder’s decision.

### Predetermined keep or retire criteria

**Keep the cash-choice claim only if all three D-033 gates are satisfied by the checkpoint:**

1. An observed task from a consenting eligible holder.
2. Defensible sale-cost treatment, including the transaction minimum, BNB gas, possible approval, freshness, and missing-field failure behavior.
3. A safe account-specific risk boundary for the holder’s borrowing path.

[D-033](../../decisions/decision-log.md) and [D-034](../../decisions/decision-log.md) make these conditions explicit. The original stop rule also requires retirement if the comparison remains unsafe or incumbents provide the same decision with equal clarity. [Product stop rule](../../product/one-page-spec.md)

### Checkpoint decision if no holder task exists

**Recommendation:** Retire the D-017 sell-or-borrow cash-choice claim at 2026-10-04 12:00 UTC if no consenting eligible-holder task has been observed. Record the gate failure plainly. Do not relabel technical integration evidence as product validation.

This decision does not select a replacement product. It does not reopen the founder-rejected exit-recovery fallback. There are **no new product feature changes before the checkpoint**, as required by D-033 and D-036.

### Strongest argument against this recommendation

The project already has a successful signed Binance quote path, a same-target display, and a bounded Venus implementation. Steward’s exercised flow did not request a cash target or place a target-sized sale quote beside its borrow plan. That leaves a technically credible and potentially useful difference. However, without a consenting holder task, there is no evidence that the difference changes a real decision, and the predetermined gate requires that evidence rather than technical plausibility alone.
