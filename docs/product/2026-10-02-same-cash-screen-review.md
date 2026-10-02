# Same-cash screen review

**Date:** 2026-10-02
**Scope:** already implemented display slice only

## Result

The screen shows one compact combined line only when the current typed NVDAB and USDT inputs match both results, Venus `retrieved_at` is no more than five minutes old, the successful Binance target-sized candidate reaches or exceeds the target in raw units, and the 20-second quote is still valid. The line is cleared on input edit, failure, below-target output or expiry.

The line compares the candidate NVDAB amount with the Venus collateral-only minimum for the same cash target. It is labelled before costs and no safety buffer. It does not prove wallet ownership, execution, net proceeds or personal borrowing safety.

## QA evidence

- Synthetic Chrome browser QA at 320 and 1440 CSS pixels passed with no horizontal overflow or page error.
- Scenario-first and quote-first orders passed.
- Stale or malformed Venus time, below-target output, wallet edit, HTTP 502 quote failure and quote expiry passed.
- The full local unit suite passed: 32 tests.
- Inline JavaScript `node --check` passed.
- `git diff --check` passed.

No additional live Binance call was made for this QA. The earlier live browser read recorded 22 signed GET calls in total and used a temporary nonholder. It observed a candidate of `0.427027364860048582` NVDAB for a 100 USDT target, displayed as about `100.00 USDT`. No screenshot or raw response was retained.

## Readiness boundary

This slice is product-not-ready evidence. There is no consenting holder observation, no verified net proceeds result and no personal borrow-safety result. The live candidate remains a technical estimate before costs, not a fill or sale instruction.

Sources: [same-cash amounts spec](same-cash-amounts-spec.md), [project status](../status.md), [DX field log](../dx/field-log.md), [readiness gates](../submission/readiness-gates.md).
