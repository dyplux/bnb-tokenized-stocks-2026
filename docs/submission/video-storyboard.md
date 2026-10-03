# Exit Check demo: storyboard and source

**Prepared:** 2026-10-03. **Runtime:** 34 seconds, 16:9, English. **State:** final MP4 rendered and [technical/visual QA](video-qa.md) recorded; judge-accessible publication pending. The [live project form audit](2026-10-01-live-form-audit.md) found a required video URL; the [event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) caps the recommended video at four minutes.

## Audience and verified claim

A self-custodial BNB Chain user considers a small NVDAB purchase. Exit Check asks for a USDC entry quote and an immediate inverse quote for the estimated NVDAB amount, before any signing. The [sanitized record](video-record.json) comes from one continuous local Chrome capture on 3 October. It records 5 USDC, an estimated 0.021265631210341636 NVDAB entry and a separate 5.001168101976778857 USDC inverse estimate at BNB metadata block 125561266. The apparent amount above 5 USDC is **not** a profit: no trade took place and costs remain unverified.

| Time | Scene | Source and constraint |
|---|---|---|
| 0 to 4 s | “Can you see the way out?” | A question, not a measured failure rate. |
| 4 to 16 s | One continuous app capture, click, waiting state and result | System Chrome recording of the actual local build. Public address masked before capture. |
| 16 to 21 s | First quoted direction, 5 USDC to NVDAB | Exact number from `video-record.json`. |
| 21 to 27 s | Immediate inverse quote | Exact number from the same record, with “before unverified costs” and “no trade” visible. |
| 27 to 31 s | “A quote isn't a fill” | Approval, gas, slippage and eligibility remain unknown. |
| 31 to 34 s | Dyplux Exit Check, “Inspect before you sign” | No public URL until one exists and works signed out. |

## Reproduction

The raw `real-app-flow.webm`, captured frames, `record.json`, HTML composition, render script and original generated audio live outside the public repo at `/Volumes/SSD500/Dyplux/exit-check-video-source/`. The video uses the founder's supplied `render(t)` HTML method. The composition loads all recorded app frames and the sanitized record before declaring itself ready, then renders each frame from time alone. Review the full MP4 and a dense contact sheet before sharing. Do not treat the immediate quote as a later-sale guarantee.
