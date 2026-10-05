# Product thesis

Last verified: 2026-10-05. Scope: Tokenized Stocks product core. Canonical owner/source: [safety spec](../product/safety-one-page-spec.md), [observed findings](../research/2026-10-04-safety-evidence.md), [frozen claims](../submission/frozen-claims-2026-10-05.md). Supersedes: the provisional comparison/edge ideas in the [decision log](../decisions/decision-log.md). Status: CURRENT.

The user is an analyst or autonomous agent preparing one tokenized-equity purchase on BNB Chain. A route may exist while the reference clock, investor access, multiplier history or executable result is unknown. The user needs a bounded decision before signing, with exactly which evidence passed or failed.

BNB Chain matters because the proposed token, multiplier state, route and potential transaction live there. Signed Binance Web3 API reads supply asset and amount-specific data; fixed-block RPC independently checks bStock scaling. [The judge path](../../JUDGE.md) shows a real quoted purchase that ended `NEED_HUMAN` and a real mandate breach that ended `DENY`.

The product doesn't predict Monday open, promise profitable spreads, certify backing, establish legal eligibility or execute a trade. A reusable post-hack kernel could accept an intent and evidence bundle, apply a versioned deterministic policy and emit a receipt before a separate signer acts. That reuse is an architecture hypothesis, not an implemented Set and Earn agent.
