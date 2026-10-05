# Video specialist evidence handoff

**Prepared:** 2026-10-04 UTC. **Updated:** 2026-10-05 after the market close. **State:** claims frozen; source inventory ready. The existing 60-second film is the verified public fallback. This file records evidence and source locations for the later submission video.

## Source material

| Item | Location | Integrity or status |
|---|---|---|
| Public judge page | https://dyplux.github.io/bnb-tokenized-stocks-2026/ | Dated examples and judge instructions |
| Public repository | https://github.com/dyplux/bnb-tokenized-stocks-2026 | Code, receipts and reproducibility steps |
| Public 60-second fallback | https://dyplux.github.io/bnb-tokenized-stocks-2026/media/execution-safety-judge-demo.mp4 | SHA-256 `d4d3530e120477fa73d8dd9d4a2938f4ca8872ca00f03ee6ac35c2147795a6e4` |
| Original 18:28 UTC capture | `/Volumes/SSD500/Dyplux/execution-safety-video-source/real-safety-flow.webm` | SHA-256 `70d899564c4f74279f2e3a8eeefd9bd31ad81c10d84d022bf855314739858c7c` |
| Original capture project | `/Volumes/SSD500/Dyplux/execution-safety-video-source/` | WebM, raw stills, first truth record, capture and render scripts |
| Original capture archive | `/Volumes/SSD500/Dyplux/execution-safety-live-capture-source.zip` | SHA-256 `a53002415784f950b1e1c16f43f78b5f1e2c4986155f5a47a0c259ee4dbc2c63`; ZIP integrity checked on 2026-10-04 |
| Composite film project | `/Volumes/SSD500/Dyplux/execution-safety-judge-video-source/` | `frames-app/`, separate denial stills and truth record, `video.html`, renderer and final frames |
| Composite project archive | `/Volumes/SSD500/Dyplux/execution-safety-judge-demo-source.zip` | SHA-256 `e14aca69f3df76390563b3ec8f7bc480d8a843f5ef89089d792fcea2765df0d3`; archive integrity checked on 2026-10-04; raw WebM is in the separate original capture project |
| Factual four-minute script | [final-four-minute-narrative.md](final-four-minute-narrative.md) | Draft screen order; final off-hours sentence reflects `SAFETY_ONLY` |
| Frozen Monday outcome and claim limits | [Findings](../../experiments/EXP-RWA-004/monday-findings.md) and [claim set](frozen-claims-2026-10-05.md) | 2026-10-05 daily rows and unchanged scorer; no predictive edge |

## What the footage shows

| Observation | Time | Decision and proof | Capture boundary |
|---|---|---|---|
| NVDAB live local read-only review | 2026-10-04 18:28:18 UTC | `NEED_HUMAN`; receipt SHA-256 `36b7d5057f2251e8bbb015e29928b7cd95e1674ed86e24c287b799fce6ff1828`; [truth record](safety-video-record.json) | One continuous Chrome capture in the original capture project |
| Separate NVDAB read-only request with 100 USDT proposed and a 20 USDT mandate cap | 2026-10-04 19:56:35 UTC | `DENY`, including `MANDATE_LIMIT_EXCEEDED`; receipt SHA-256 `a720aa7010b3287cf75f450b8cc2501a75a1465db37e56c7ffd751196b4626e8`; [truth record](../judge/observed-mandate-deny.json) | Dated replay assembled from separate captures, labelled as such in the fallback film |

The public [synthetic `ALLOW` fixture](../judge/synthetic-safe.json) demonstrates a policy branch only. It isn't footage of a real purchase. The observed quote doesn't prove user eligibility, funded simulation, signature, broadcast or fill. Neither observation establishes the age of an independent underlying stock reference. The token-price update clock and underlying-reference clock must remain separate.

## Claim freeze gate

The unchanged [preregistered scorer](../../scripts/score_monday_benchmark.py) produced the [Monday benchmark](../../experiments/EXP-RWA-004/monday_open_results.json). Classification is `SAFETY_ONLY`: two of three independent tickers matched Sunday direction, TSLA missed, and execution prerequisites weren't shown. The final script changes only the off-hours sentence. The safety product and its observed `NEED_HUMAN` and `DENY` cases stand independently of the result.

The claim set is frozen, so the final video may be handed to the specialist. Preserve the two capture dates and the replay label when reusing footage. See [film QA](safety-judge-video-qa.md) for frame, audio and public-download checks.
