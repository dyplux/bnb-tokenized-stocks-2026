# Monday opening capture audit

**Audited:** 2026-10-05 19:00 UTC. **Observation window:** 13:20 to 13:45 UTC. This is a capture-quality report, not the preregistered outcome analysis. The [frozen protocol](monday-open-protocol.md), Sunday sample and scorer remain unchanged.

| Source | Recorded coverage | Raw-response check | Errors and gaps |
|---|---|---|---|
| `PRIMARY`, local signed collector | Five complete five-minute slots at 13:20, 13:25, 13:30, 13:35 and 13:40 UTC, each with 40 contracts and all six frozen contracts | All five unique price-response hashes referenced by the window rows resolve to matching retained gzip bodies | No window slot missing |
| `FALLBACK`, local signed collector | 25 complete one-minute slots, 13:20 through 13:44 UTC; 150 of 150 expected contract rows, all with token price and share ratio | 50 of 50 raw-manifest entries resolve to matching gzip bodies | Zero error rows, zero gap rows; 139 health snapshots, none flagged an unhealthy collector or watchdog |
| `FALLBACK`, [GitHub run 37313747181](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions/runs/37313747181) | 25 complete one-minute slots; 150 public Binance contract observations and 75 Yahoo chart responses | 225 of 225 manifest entries resolve to matching gzip bodies; GitHub artifact digest `sha256:8bc62479331d24e5a2fe475b5af49e471085c2fd40bf31e0d25e337621e68f0f` | Zero error rows, zero gap rows; workflow succeeded |
| `FALLBACK`, [GitHub run 37316841008](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions/runs/37316841008) | Started at 13:26:44 UTC; 18 complete minutes from 13:27 through 13:44 UTC, with 108 public Binance and 54 Yahoo observations | 162 of 162 manifest entries resolve to matching gzip bodies; GitHub artifact digest `sha256:82c061de43d5d4cb15fb155da175371457b77a8b4a94093318b70acd7f2f3bda` | One explicit start-late gap covering seven early minutes; no API error rows. Workflow failed its full-window completeness gate as designed. |

The primary collector remained alive after the window. At 18:55 UTC it reported 15,556 unique LIVE observations overall, 40 contracts in the latest cycle and zero consecutive failures. The two-contract underlying watch last succeeded at 18:30 UTC.

The successful public run has a Yahoo response for every ticker and minute. At the exact 13:30 UTC request, the three responses contained no usable latest bar; the raw responses were retained. A first regular-session intraday bar appeared in the 13:31 capture. These minute bars are supporting observations. They aren't substituted for the dated daily regular-session open or close required by the frozen scorer.

## Derived-summary defect

The local fallback's `finished.json` was written by a version that applied the **public-run** completeness calculation to a **local** run. It therefore says all public slots were missing, even though its own `slots.jsonl` has 25 complete local slots, `observations.jsonl` has all 150 contract rows, and its error and gap logs are empty. The original `finished.json` remains preserved. The status command now reports `MONDAY_LOCAL_CAPTURE_COMPLETE=YES` from the actual local slot rows and labels the window `CLOSED`; its `MONDAY_OPEN_READY=NO` only means the scheduled process has naturally ended. The code path for future local summaries was corrected without changing any observation or frozen experiment input.

## Next gate

Wait for a dated 2026-10-05 **daily regular-session** row with open and close for NVDA, TSLA and COIN. Confirm the session date and values from the source before running the unchanged scorer. The public close fallback is scheduled at 20:09 and 20:27 UTC; those runs are supporting sources until their artifacts are inspected. No off-hours directional result is claimed in this audit.
