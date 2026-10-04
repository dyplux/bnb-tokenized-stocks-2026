# Execution Safety demo video QA

**Recorded and rendered:** 2026-10-04 UTC. **Product state shown:** real local, read-only safety check. **Public film:** [execution-safety-demo.mp4](../media/execution-safety-demo.mp4).

The source folder is `/Volumes/SSD500/Dyplux/execution-safety-video-source/`. It contains the Chrome recording, stills, sanitized [truth record](safety-video-record.json), `video.html` with a deterministic `render(t)` path, `render.py`, generated music source, 720 rendered frames, the final MP4 and a dense contact sheet. A local source archive and a convenient MP4 copy sit directly in `/Volumes/SSD500/Dyplux/`; they aren't public repository assets.

The source archive is `execution-safety-demo-source.zip`, 115 MB. Its SHA-256 is `0293a83181de91a7f32bf8e1d1a7c10288a8e9f04efe67499184c3c562194aa5`; archive integrity passed `unzip -tq`.

| Check | Observed result |
|---|---|
| Application capture | One continuous 11.08-second Chrome recording of the 18:28 UTC NVDAB request; no page errors reported |
| Policy and receipt | `NEED_HUMAN`; actual SHA-256 receipt `36b7d5057f2251e8bbb015e29928b7cd95e1674ed86e24c287b799fce6ff1828` |
| Evidence boundary | Route `QUOTED` in `SWAP` mode; independent reference time and holder eligibility unknown; simulation `NOT_RUN`; no signature, broadcast or fill |
| Video stream | 1920 × 1080, 24 fps, H.264, exactly 30.000 seconds, 720 expected and rendered frames, no missing frame |
| Audio stream | AAC. Automated level check: mean about -14.5 dB, peak about -1.3 dB. Subjective full-length listening remains an editorial check. |
| Visual inspection | Dense 2 fps contact sheet checked for scene order, readable read-only and no-trade labels, crop continuity and blank frames. Browser renderer reported zero page errors. |
| MP4 SHA-256 | `a3caf8d54d964570fb8dfb769ba8f8dbe74a6b8b1eae8ab93101938f55369352` |
| Local judge page | Chrome at 1440 px and 390 px: HTTP 200, MP4 HTTP 200 `video/mp4`, no JavaScript page errors or horizontal overflow, observed receipt hash matched |
| Published judge page | The same two Chrome viewport checks passed after Pages deployment of `7723ed7`; the public MP4 returned HTTP 200 `video/mp4` and its bytes matched the local SHA-256. Python CI and Pages deployment both succeeded for that commit. |

The public judge page's observed receipt is from a **different 15:57 UTC request**. The film uses only the 18:28 capture and says so in the [storyboard](safety-video-storyboard.md). Its quoted route is not an eligible or executable fill. The synthetic `ALLOW` fixture is not shown as a real outcome. This film is suitable as a dated safety-product walkthrough; it does not satisfy the mainnet execution blocker.
