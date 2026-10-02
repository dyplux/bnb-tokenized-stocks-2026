# Same cash target, two token amounts

**Date:** 2026-10-02. **Decision:** [D-024](../decisions/decision-log.md). This is a display correction to the provisional read-only task, not a new borrowing forecast.

## Screen job

After the user has fetched a Venus market scenario and a Binance candidate sale for the same typed NVDAB amount and USDT target, show one compact line beside the quote summary:

- Candidate NVDAB units quoted for a sale that meets the target **before costs**.
- Collateral-only minimum NVDAB units calculated from the Venus indexed market snapshot for the same target, with **no safety buffer**.

The two source times remain in their existing panels. Keep the main sale card without net proceeds and the borrow result hypothetical. The line must not state that either path can execute, that the wallet owns the typed units, or that the collateral minimum is personally safe. The existing quote mode review still applies.

## Display rule

Only show the line if both current results were fetched for the exact current units and cash inputs, the Venus `retrieved_at` timestamp is no more than five minutes old, the Binance result is `target_quote_observed`, its first route output reaches the target in integer raw units, and the quote hasn't expired. Refresh it when either source arrives second. Clear it on an input edit, quote failure or 20-second expiry. If the final quote misses the target, leave the amounts separate and show the shortfall already present in the quote summary. The five-minute display gate doesn't certify Venus contract state or personal borrowing safety.

Use the same restrained type and spacing as the existing quote summary. Keep exact raw quote units and the exact Venus minimum in the existing evidence panels. Display rounding cannot affect the raw target verdict or the cap check.

## Acceptance

1. A 1 NVDAB / 100 USDT synthetic example with a 0.43 NVDAB candidate and a 0.72 NVDAB isolated minimum shows both amounts in one compact line. It says before costs and no safety buffer.
2. Scenario-first and quote-first interaction orders both show the line when current inputs match.
3. Editing units, cash or wallet, a failed quote, a below-target quote and quote expiry hide the line.
4. Chrome at 320 and 1440 CSS pixels has no page errors or horizontal overflow with the line visible.
5. A stale or malformed Venus retrieval time keeps the combined line hidden while the two individual result panels retain their own timestamps and limits.

The implementation review is recorded in [the 2026-10-02 screen review](2026-10-02-same-cash-screen-review.md).
