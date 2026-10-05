# Execution Safety submission review packet

**Prepared:** 2026-10-04 UTC. **State:** current build packet for founder review, not a submitted entry. The retired Exit Check draft remains in Git history.

## What a judge can inspect

| Surface | Link | What it proves |
|---|---|---|
| Public judge page | https://dyplux.github.io/bnb-tokenized-stocks-2026/ | Dated examples, decision reasons, receipt download, limits and local-run path |
| Public repository | https://github.com/dyplux/bnb-tokenized-stocks-2026 | Deterministic policy, signed Binance Web3 integration, source code and [README](../../README.md) |
| Local live run | [Safety judge guide](safety-judge-run.md) | With the judge's own Binance Web3 credentials, one read-only stock-token action can be reviewed without a wallet key |
| Public fallback film | https://dyplux.github.io/bnb-tokenized-stocks-2026/media/execution-safety-judge-demo.mp4 | 60 seconds showing two separately dated read-only outcomes; [QA and limits](safety-judge-video-qa.md) |
| DevEx record | [4 October evidence summary](../devex/2026-10-04-evidence-summary.md) | Sanitized calls, raw-response reproductions and our own integration mistakes |

The working name is **Dyplux Execution Safety Layer for Tokenized Equities**. A person or agent proposes a stock-token purchase on BNB Chain. The local screen uses signed Binance Web3 RWA Data and Trading reads, checks the bStock multiplier at a fixed BNB Chain block when relevant, and applies a deterministic mandate before any signature. It returns `ALLOW`, `DENY` or `NEED_HUMAN` with reason codes and a SHA-256 receipt. The public page is a dated evidence packet; its examples don't call a hosted API.

## What has been observed

| Case | Observation | Boundary |
|---|---|---|
| `NEED_HUMAN` | An 18:28 UTC 4 October NVDAB read-only check received a quote but lacked independent stock-reference time, verified holder access and funded simulation. [Truth record](safety-video-record.json). | A quote isn't permission or a fill. |
| `DENY` | A separate 19:56 UTC 4 October NVDAB request proposed 100 USDT under a 20 USDT mandate. The policy returned `MANDATE_LIMIT_EXCEEDED` despite a route. [Truth record](../judge/observed-mandate-deny.json). | The public example is a dated replay. |
| `ALLOW` | A labelled [synthetic fixture](../judge/synthetic-safe.json) exercises the permissive policy branch. | It isn't an observed eligible trade. |

The [fixed 19:35 UTC DevEx export](../devex/2026-10-04-metrics.json) contains 611 logged calls, including 516 signed Binance Web3 calls. Four reproducible findings are the undocumented `offhours` enum, absence of an observed independent stock-reference as-of time, a 100-address price GET returning HTTP 414, and stock-token `SWAP` routes alongside broad RFQ wording in one reference page. The [current DX draft](dx-form-current.md) records the scope and counterevidence. Counts are a dated cut of mixed research and local product calls, not user traffic or a reliability benchmark.

No funded stock-token transaction, verified holder eligibility, passing funded simulation, signature, broadcast or fill is claimed. A real `NEED_HUMAN` remains a successful safety outcome when a required fact is unavailable. The absence of a capital trade doesn't change the documented product core. The optional execution gates are on the [blocker board](blocker-board.md).

## Remaining submission sequence

1. Use the [Monday findings](../../experiments/EXP-RWA-004/monday-findings.md) and [frozen claims](frozen-claims-2026-10-05.md): `H-RWA-OFFHOURS=SAFETY_ONLY`. Keep the Sunday anchor, protocol and scorer frozen; no directional edge enters the submission.
2. Recheck the final README, public page, video and receipt URLs without login. The existing 60-second film is a fallback. The [video evidence handoff](video-specialist-evidence-handoff.md) provides clean footage and hashes to the specialist after the claim set is frozen.
3. Founder reviews the [53-item DX answer map](dx-form-safety-answer-map.md), supplies private and subjective fields directly, and submits the [Developer Experience Report](https://forms.gle/EUQ39xf54GHjC2ys5). Keep a non-sensitive record of completion.
4. Founder confirms the final project name, contact and prize wallet or UID privately, then uses the [current project answer map](project-form-safety-answer-map.md) to submit the [project form](https://forms.gle/yToDUzaDMwWnq6R6A). Its DX confirmation must reflect an actual submitted report. Do not select an Agentic Wallet or Agent Studio special prize without a working integration.

The [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview) lists the submission lock as 11 October 2026, 12:00 UTC. The [4 October form audit](2026-10-01-live-form-audit.md) found a required video URL field even though the event page describes the video as optional. Recheck the live form before sending it. No submission receipt is recorded here.
