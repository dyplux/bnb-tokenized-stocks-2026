# Monday outcome operations

**Prepared:** 2026-10-04 UTC. This is an execution checklist for the [locked protocol](monday-open-protocol.md), not a change to its sample, baseline, thresholds or interpretation.

The separate [opening-window fallback](monday-fallback-operations.md) records operational backup observations. It doesn't write to the primary tape or feed the frozen scorer automatically.

## Before and during the US regular session, 5 October

Before entering an outcome, check the frozen inputs with `shasum -a 256 experiments/EXP-RWA-004/monday-open-protocol.md experiments/EXP-RWA-004/friday_close_benchmark.csv data/external_reference/2026-10-02-yahoo-close.json`. Their 4 October SHA-256 values are, in that order, `081838ce5c3d8f34f6858f1c9c9a6e7b9da6e6ba861c610345b78ee14b2ad16a`, `3931d82c2ea5403c7d50f818c34fd5f2f3758459a9d8cb762521473bb04fe910` and `1c2c0f8b0e1a683ab45e5f4b961631ba7be39a7503ba8805b97d209f2c0b9b3e`. If one differs, inspect the committed frozen version before scoring; don't silently adopt a changed baseline. This is an integrity check, not a change to the protocol.

The scorer is also frozen before Monday's observation: `shasum -a 256 scripts/score_monday_benchmark.py` must return `921c2c20a513a61bf1b73a320e2f3784c16d4af810f1e1ad2a0c909126f11208`. Do not change its comparisons after seeing the outcome.

1. Run `python3 scripts/rwa_research.py health`. Confirm a live PID, last successful 40-contract cycle, zero overdue state and the separate two-contract underlying watch. Don't start another collector while the existing process is healthy.
2. Run `python3 scripts/audit_market_tape.py 2026-10-05` after the first complete Monday slot. Record `complete_slots`, `recorded_gaps`, `recorded_errors` and `violations`. Missing Saturday observations remain missing; don't backfill them as LIVE.
3. Record the market session from the official [Nasdaq hours](https://www.nasdaq.com/market-activity) and [holiday calendar](https://www.nasdaq.com/market-activity/stock-market-holiday-schedule). The expected regular open is 09:30 New York time, 13:30 UTC on 5 October. If a source reports a halt, holiday or changed session for NVDA, TSLA or COIN, mark that ticker's opening outcome uncertain and retain the original row.

## After dated historical rows are available

1. Open the 5 October history rows for [NVDA](https://finance.yahoo.com/quote/NVDA/history/), [TSLA](https://finance.yahoo.com/quote/TSLA/history/) and [COIN](https://finance.yahoo.com/quote/COIN/history/). Capture publisher, UTC retrieval time, exact session date, open, close and each direct URL in a new JSON file based on [the input template](monday-outcome-input-template.json). A row unavailable or ambiguously dated keeps explicit JSON `null` values, not text placeholders. The scorer rejects malformed non-null prices before writing results.
2. Inspect the three source rows, then run `python3 scripts/score_monday_benchmark.py <dated-outcome-json>`. The script writes all six frozen representation rows to `monday_open_benchmark.csv` and summary arithmetic to `monday_open_results.json`. It rejects an all-missing open. It cannot verify the publisher's numbers for us.
3. Review every mismatch and null against the [locked comparison and promotion conditions](monday-open-protocol.md). Write the findings note with all six rows, the Friday after-hours sensitivity, amount-specific route costs and access limits. Classify H-RWA-OFFHOURS as `PROMOTE`, `SAFETY_ONLY` or `KILL` without changing H-RWA-SAFETY as the product core.

A daily stock bar has a session date, not the issuer's independent stock-reference update timestamp. Keep `reference_price_updated_at=null` and `reference_age_status=UNKNOWN` unless a separate permitted source supplies that specific clock. Neither a directional match nor a quote proves a fill or trading profit.
