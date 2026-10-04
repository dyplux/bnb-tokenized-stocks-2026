# A Friday late-session bar changes Sunday's apparent gap

**Retrieved:** 2026-10-04 UTC. **Session reconstructed:** Friday 2026-10-02, 16:00 to before 20:00 New York time. This is an exploratory sensitivity check beside the [frozen Monday protocol](../../experiments/EXP-RWA-004/monday-open-protocol.md); it doesn't replace that protocol's regular-close baseline.

The [bounded backfill script](../../scripts/backfill_friday_afterhours.py) requested three Yahoo Finance historical 1-minute series with `includePrePost=true`. It kept the last non-null bar in the stated Friday late session for [COIN](https://query1.finance.yahoo.com/v8/finance/chart/COIN?period1=1790970900&period2=1790985900&interval=1m&includePrePost=true), [NVDA](https://query1.finance.yahoo.com/v8/finance/chart/NVDA?period1=1790970900&period2=1790985900&interval=1m&includePrePost=true) and [TSLA](https://query1.finance.yahoo.com/v8/finance/chart/TSLA?period1=1790970900&period2=1790985900&interval=1m&includePrePost=true). The [backfilled source ledger](../../data/external_reference/2026-10-02-yahoo-afterhours-bars.json) retains retrieval times, endpoint URLs, response hashes, bar counts and exact timestamps. These bars are historical external data, not observations that our collector made live on Friday.

| Asset | Friday regular close | Last available late-session bar | Sunday bStock vs bar | Sunday Ondo vs bar |
|---|---:|---:|---:|---:|
| COIN | $183.00 | $183.2397 at 19:59:50 ET | +1.1462% | +1.1926% |
| NVDA | $233.95 | $234.2218 at 19:59:58 ET | +0.1092% | +0.2575% |
| TSLA | $370.59 | $371.4476 at 19:59:59 ET | -0.0236% | +0.0585% |

The Sunday token-derived per-share values come from the same fixed 12:00 UTC LIVE slot used in the [six-row comparison](../../experiments/EXP-RWA-004/friday_afterhours_sensitivity.csv). The median absolute gap across those six dependent representations shrinks from **0.3320%** against Friday's regular close to **0.1834%** against the late-session bars. TSLA bStock even changes sign, from slightly above the regular close to slightly below the late-session bar. COIN remains more than 1.1% above both baselines.

**Interpretation:** Friday's 16:00 close alone overstates at least part of the apparent weekend move. The Yahoo bar timestamps aren't issuer reference-price update times or guaranteed last trades; the two token issuers aren't assumed economically equivalent. No Monday open, executable spread, filled order or predictive edge follows from this sensitivity check. A future product that describes an off-hours gap must specify which prior session and data source it means.
