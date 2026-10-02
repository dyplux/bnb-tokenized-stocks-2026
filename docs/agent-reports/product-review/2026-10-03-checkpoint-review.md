# Pre-checkpoint review of D-017

**Reviewed:** 2026-10-02 UTC (2026-10-03 Lisbon). **Role:** bounded Plus Sol, read-only review of the [event rules](../../01-event-rules.md), [product spec](../../product/one-page-spec.md), [readiness gates](../../submission/readiness-gates.md), [Core risk analysis](../../research/2026-10-02-account-wide-risk-feasibility.md), [unsigned swap build](../../research/2026-10-02-first-live-swap-build.md) and D-017 to D-023 in the [decision log](../../decisions/decision-log.md). No new API call, holder session or product test was performed in this review.

## Recommendation

The existing signed Binance identity and target-sized quote path, plus one unsigned SWAP build, support a reproducible technical prototype. They do not establish settled net proceeds, a personally safe Venus loan or improved comprehension for an eligible holder. Keep the sell-or-borrow product hypothesis at the 4 October checkpoint only if a holder task can be observed before submission and the interface continues to suppress executable and personal-safety claims. Otherwise retire that product claim.

| Keep condition | Retire condition |
|---|---|
| One clean same-input run reproduces identity, bounded two-quote sizing, quote expiry, target gap and separate Venus state with source times. | The quote path cannot be reproduced or needs an unsupported net-proceeds assumption. |
| A consenting eligible holder can try the same cash task in the existing venue, Venus and the app before final evidence capture. | No holder task is available before the delivery window, or the existing flow gives the same answer as clearly. |
| Borrowing remains an isolated market illustration unless account-wide post-action safety is validated. | The interface implies a personal safe amount or liquidation threshold from market factors or current net cushions alone. |

## Two different proofs

**Without a holder:** capture a single sanitized same-input run: exact NVDAB identity, target-sized Binance candidate, corresponding unsigned build, Venus cap and market state at a stated block, and the actual UI's unknown states. This proves integration coherence and reproducibility only.

**With a holder:** observe one consenting eligible NVDAB owner with a real or clearly hypothetical cash need, an amount no greater than the observed balance, a fresh holder-sized quote, current Venus state and the same task in the incumbent interfaces. Record what they would do and which evidence changed their understanding. No trade, deposit or loan is required.

**Fallback:** if the holder proof fails, consider only a clearly labelled Binance bStock quote/build and Venus readiness diagnostic as a narrower candidate. It still needs a central user task and a working judge path. Preserve the DX evidence if even that gate fails. Unknowns remain allowance, cost scope, execution, populated-account correctness, demand, judge access and form receipts.
