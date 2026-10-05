# Monday open benchmark: safety finding, no directional edge

**Outcome session:** 2026-10-05, US regular session. **Retrieved:** 2026-10-05 20:09 UTC, after the 20:00 UTC close. **Decision:** `H-RWA-OFFHOURS = SAFETY_ONLY`.

The [protocol](monday-open-protocol.md), Friday close baseline, Sunday 12:00 UTC slot `5970384`, three tickers, six provider rows and [scorer](../../scripts/score_monday_benchmark.py) were frozen before the outcome. Their SHA-256 values remained unchanged before scoring. The [dated outcome input](monday-outcome-yahoo-2026-10-05.json), [six-row benchmark](monday_open_benchmark.csv) and [machine result](monday_open_results.json) retain the arithmetic and source fields.

| Underlying | Yahoo 5 Oct open | Yahoo 5 Oct close | Sunday bStock per share | Sunday Ondo per share | Sunday direction vs open |
|---|---:|---:|---:|---:|---|
| [COIN](https://finance.yahoo.com/quote/COIN/history/) | $187.14 | $188.22 | $185.34 | $185.425 | Match, both providers |
| [NVDA](https://finance.yahoo.com/quote/NVDA/history/) | $236.07 | $238.90 | $234.4775 | $234.825 | Match, both providers |
| [TSLA](https://finance.yahoo.com/quote/TSLA/history/) | $368.80 | $378.73 | $371.36 | $371.665 | Mismatch, both providers |

The Yahoo historical rows each carried `session_date=2026-10-05`, `America/New_York` and a regular-session open and close. The exact chart URLs, UTC retrieval times, original float values and raw-response SHA-256 hashes are in the outcome input. Values above are rounded to cents for display; scoring used the recorded cent values. No date or value was ambiguous in two same-publisher reads, so no alternate publisher or methodology replaced the frozen source. The daily rows provide a session date, not the issuer's independent stock-reference update time. That field remains `UNKNOWN`.

Four of six provider rows match direction, representing **two of three independent underlyings**. TSLA pointed up in both Sunday representations relative to Friday's $370.59 regular close, then opened down at $368.80. The median absolute Sunday-to-open residual is **0.7301%** across six provider rows. TSLA's two residuals were -0.6894% and -0.7709%, larger in magnitude than its -0.4830% Friday-to-open move. COIN's residuals were +0.9712% and +0.9249%; NVDA's were +0.6792% and +0.5302%. The provider rows share the same underlying outcome and are not six independent predictions. No frozen row was excluded or substituted.

The [preregistered promotion condition](monday-open-protocol.md) requires more than matching signs: another weekend, comparable Friday after-hours prices, amount-specific buy and sell routes, costs, access checks and a funded or simulated execution path. Those conditions aren't met. A [separate Friday after-hours sensitivity](friday_afterhours_sensitivity.csv) exists but does not replace the frozen regular-close baseline. The observations therefore support showing market state, timestamp provenance and uncertainty before an agent signs. They do **not** support a predictive next-open, executable spread, profitable trade or fill claim.

`SAFETY_ONLY` retains the off-hours context as an input to the Dyplux Execution Safety Layer. It does not add an off-hours intelligence or trading feature. `H-RWA-SAFETY` remains the product core; its `NEED_HUMAN` and `DENY` outcomes require no price prediction.
