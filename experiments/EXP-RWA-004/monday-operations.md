# Monday outcome operations

**Prepared:** 2026-10-04 UTC. This is an execution checklist for the [locked protocol](monday-open-protocol.md), not a change to its sample, baseline, thresholds or interpretation.

## Before and during the US regular session, 5 October

1. Run `python3 scripts/rwa_research.py health`. Confirm a live PID, last successful 40-contract cycle, zero overdue state and the separate two-contract underlying watch. Don't start another collector while the existing process is healthy.
2. Run `python3 scripts/audit_market_tape.py 2026-10-05` after the first complete Monday slot. Record `complete_slots`, `recorded_gaps`, `recorded_errors` and `violations`. Missing Saturday observations remain missing; don't backfill them as LIVE.
3. Record the market session from the official [Nasdaq hours](https://www.nasdaq.com/market-activity) and [holiday calendar](https://www.nasdaq.com/market-activity/stock-market-holiday-schedule). The expected regular open is 09:30 New York time, 13:30 UTC on 5 October. If a source reports a halt, holiday or changed session for NVDA, TSLA or COIN, mark that ticker's opening outcome uncertain and retain the original row.

## After dated historical rows are available

1. Open the 5 October history rows for [NVDA](https://finance.yahoo.com/quote/NVDA/history/), [TSLA](https://finance.yahoo.com/quote/TSLA/history/) and [COIN](https://finance.yahoo.com/quote/COIN/history/). Capture publisher, UTC retrieval time, exact session date, open, close and each direct URL in a new JSON file based on [the input template](monday-outcome-input-template.json). A row unavailable or ambiguously dated keeps null values.
2. Inspect the three source rows, then run `python3 scripts/score_monday_benchmark.py <dated-outcome-json>`. The script writes all six frozen representation rows to `monday_open_benchmark.csv` and summary arithmetic to `monday_open_results.json`. It rejects an all-missing open. It cannot verify the publisher's numbers for us.
3. Review every mismatch and null against the [locked comparison and promotion conditions](monday-open-protocol.md). Write the findings note with all six rows, the Friday after-hours sensitivity, amount-specific route costs and access limits. Classify H-RWA-OFFHOURS as `PROMOTE`, `SAFETY_ONLY` or `KILL` without changing H-RWA-SAFETY as the product core.

A daily stock bar has a session date, not the issuer's independent stock-reference update timestamp. Keep `reference_price_updated_at=null` and `reference_age_status=UNKNOWN` unless a separate permitted source supplies that specific clock. Neither a directional match nor a quote proves a fill or trading profit.
