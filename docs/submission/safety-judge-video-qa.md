# Two-case safety demo video QA

**Rendered:** 2026-10-04 UTC. **Public film:** [execution-safety-judge-demo.mp4](../media/execution-safety-judge-demo.mp4). **Boundary:** two separate read-only observations, no trade signed or broadcast.

The 60-second film combines a continuous local Chrome capture of an 18:28 UTC NVDAB review with a separately labelled replay of a 19:56 UTC observed mandate denial. The first returned `NEED_HUMAN` with receipt SHA-256 `36b7d5057f2251e8bbb015e29928b7cd95e1674ed86e24c287b799fce6ff1828`. The second returned `DENY` after a 100 USDT request exceeded a 20 USDT cap. The second scene uses element captures from the public dated packet, not footage of the first request. Its truth record is [observed-mandate-deny.json](../judge/observed-mandate-deny.json).

The complete local source is `/Volumes/SSD500/Dyplux/execution-safety-judge-video-source/`. It contains the 135 original app frames, public-page captures, both sanitized truth records, deterministic HTML timeline, renderer, original synthesized music, normalization/encode code, all 1,440 final frames, contact sheets and MP4. The local archive `/Volumes/SSD500/Dyplux/execution-safety-judge-demo-source.zip` is 207 MB; `unzip -tq` reported no errors. Its SHA-256 is `e14aca69f3df76390563b3ec8f7bc480d8a843f5ef89089d792fcea2765df0d3`. The standalone MP4 also sits in `/Volumes/SSD500/Dyplux/`.

| Check | Observed result |
|---|---|
| Source boundary | First 18:28 UTC live local read-only result and second 19:56 UTC dated replay are labelled separately. The synthetic `ALLOW` fixture is absent. |
| Evidence | Source page and local truth records show `NEED_HUMAN` and `DENY`. A quote is presented as a route, never as eligible access or a fill. |
| Frames | Chrome rendered 1,440 of 1,440 expected 24 fps frames with zero page errors. Preview frames and dense 2 fps contact sheets were inspected for scene order, text visibility and blank cards. |
| Video | 1920 × 1080 H.264, 24 fps, exactly 60.000 seconds, 1,440 encoded frames. |
| Audio | Original synthesized music, two-pass normalization and AAC encoding. Automated decoded level check: mean −14.1 dB and peak −1.3 dB. Subjective full-length listening remains an editorial check. |
| MP4 SHA-256 | `d4d3530e120477fa73d8dd9d4a2938f4ca8872ca00f03ee6ac35c2147795a6e4`, identical in source, public-repo copy and local standalone copy before deployment. |

The film doesn't prove independent stock-reference freshness, user eligibility, passing funded simulation, a capital transaction, or an economic advantage. The public receipt hash verifies the published decision body's internal consistency; the signed API response bodies named by its source hashes remain local. Monday's preregistered observation and any later authorized trade require a separate evidence cut before changing the claims.
