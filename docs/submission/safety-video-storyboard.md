# Execution Safety demo: source and storyboard

**Prepared:** 2026-10-04 UTC. **State:** rendered and visually reviewed; [30-second MP4](../media/execution-safety-demo.mp4) is part of the public judge page. This replaces the retired [Exit Check storyboard](video-storyboard.md). Format: 30 seconds, 16:9, English, no investment or execution claim. The project form needs a video URL; the organiser's [event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) recommends less than four minutes.

## Viewer and claim

One agent builder is about to approve a tokenized-equity purchase. A Binance Web3 route may be available while the evidence required to let an agent sign is missing. Dyplux checks that exact action and returns a reasoned, hashed decision receipt. In the [4 October live local capture](safety-video-record.json), a 100 USDT NVDAB review returned `NEED_HUMAN`. The route was `QUOTED` in `SWAP` mode; the independent stock-reference time and holder eligibility were unknown, and a funded simulation had not run. No transaction was signed or broadcast.

The source is one continuous local Chrome recording of the real safety screen, with three still frames from that same capture. The sanitized record contains every quantity and result that may appear in the film, including the capture time and artifact hashes. The video may crop or animate those pixels, but must not turn a separate read-only quote into a fill or show a synthetic `ALLOW` as a real outcome.

| Time | On-screen idea | Visual proof and boundary |
|---|---|---|
| 0–3 s | “Would you let it sign?” | Question on a Dyplux title plate; no fictional price or return. |
| 3–14 s | “100 USDT into NVDAB” | Continuous 11.08-second real local app capture: selected representation, amount, click, waiting state, result. Label **LIVE READ-ONLY, 4 OCT**. |
| 14–17.5 s | “A route came back” | Real evidence row, `QUOTED` and `SWAP`. Quote is indicative and from a temporary unfunded address. |
| 17.5–22.5 s | “Three facts still missing” | From the real result: independent stock-reference time `UNKNOWN`, holder eligibility `UNKNOWN`, simulation `NOT_RUN`. The app capture includes the other two reason codes. |
| 22.5–26 s | “NEED HUMAN” | Actual policy result and decision receipt hash from the same captured request. The app's next action is issuer/access and reference verification, then a funded simulation and separate approval. |
| 26–30 s | “Check before signing” | Dyplux Execution Safety, public judge URL and repository. State **NO TRADE SIGNED**. |

## Proof and cut rules

- The [truth record](safety-video-record.json) dates the live result to `2026-10-04T18:28:18Z`, records five actual reason codes, one quoted route and a matched fixed-block multiplier. These are a single read-only app result, not a funded wallet preflight.
- The app's `NEED_HUMAN` is the honest product moment. The public [observed judge packet](../judge/observed-unsafe.json) is a different 15:57 UTC request. Never splice its numbers or hash into the 18:28 capture without showing a new date and source.
- The public [synthetic `ALLOW` fixture](../judge/synthetic-safe.json) demonstrates policy branch behavior only. Omit it from this short film to keep the outcome unambiguous; judges can inspect it on the site.
- Do not show an order, wallet signature, payment, stock-market reference age, eligibility pass, realized saving or Monday result. A route and zero-page-error capture don't establish any of those.
- The last frame must link to the [public judge page](https://dyplux.github.io/bnb-tokenized-stocks-2026/) and [repository](https://github.com/dyplux/bnb-tokenized-stocks-2026). Check both without authentication before publishing the film.

## Render gate

Keep the source and render in the Dyplux SSD project area. Preserve the HTML, capture, stills, audio source, record and render script together. Before publishing, inspect a dense contact sheet, listen to the whole cut, verify every displayed number against the record, check that `LIVE READ-ONLY` and `NO TRADE SIGNED` are legible, and ensure the film matches the public build. A new mainnet proof may warrant a separate later cut; it mustn't be implied by this one.

The [QA record](safety-video-qa.md) documents the rendered file, source path, visual inspection and boundaries. Subjective audio listening remains a separate editorial check before using this film as the final form video.
