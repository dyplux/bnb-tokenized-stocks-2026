# Project brief

**Updated:** 2026-10-06. Brand and frozen Monday outcome updated; dated source evidence is unchanged.

**Product core:** Praeva by Dyplux, a deterministic pre-signing safety layer for autonomous tokenized-equity agents.

**Owner:** Dyplux

**Deadline:** 2026-10-11 12:00 UTC

## User task

A self-custodial BNB Chain user proposes one bounded spot tokenized-equity action. The current read-only screen checks the exact security, representation, market state, reference-time evidence, current bStock multiplier where relevant, holder-access evidence, an amount-specific route and the user's mandate. It records simulation as unverified and returns `ALLOW`, `DENY` or `NEED_HUMAN` with reason codes and a dated receipt. A separate local packet attempts an exact-wallet unsigned build and off-chain simulation. The [one-page spec](product/safety-one-page-spec.md) defines this slice.

The need is supported by six [dated technical observations](research/2026-10-04-safety-evidence.md), including missing independent stock-reference time, an undocumented `offhours` state and a displayed cross-issuer gap without a corresponding executable route. These don't prove user demand, a safe funded trade or financial benefit. [D-063](decisions/decision-log.md) records the founder's decision to freeze the safety layer as the product core. Earlier Exit Check and exact-budget ideas are retained as research history, not the active submission.

## Working surface and limits

The local [one-action screen](../app/safety.html) uses signed Binance Web3 RWA and Trading data, a fixed-block BNB Chain multiplier read for bStocks, and a deterministic [policy](../app/rwa_policy.py). The [public judge packet](https://dyplux.github.io/bnb-tokenized-stocks-2026/) shows a dated observed `NEED_HUMAN` decision and a plainly labelled synthetic `ALLOW` fixture. It isn't a public live signed-API service. [Judge instructions](submission/safety-judge-run.md) explain the credentialed local live path.

An exact-wallet 10 USDT NVDAB preflight has returned an unsigned build and an off-chain simulation, but the demo wallet has zero USDT and BNB, and the simulation predicted `FAILED`. The user's issuer access and independent stock-reference time remain unverified. No transaction has been signed or broadcast. [Asset selection](submission/demo-asset-selection.md), the [bounded execution protocol](product/mainnet-execution-path.md), and the [blocker board](submission/blocker-board.md) hold the current gate.

The five-minute, 40-contract collector is separate from the frozen experiment. Monday's [preregistered market-open experiment](../experiments/EXP-RWA-004/monday-open-protocol.md) concluded [SAFETY_ONLY](../experiments/EXP-RWA-004/monday-findings.md): off-hours uncertainty supports the safety review, with no predictive-alpha claim. Current collector health and the second hackathon are in [STATUS.md](../STATUS.md).

## Submission boundary

The [official event rules](01-event-rules.md) require a BNB Chain mainnet tokenized-stock project with a Binance Web3 API integration, a public repository, a judge path and a Developer Experience Report. The live form also asks for a demo video URL. The public repository and dated judge path exist. A funded mainnet action, final video, final DevEx report and form submission remain open. Do not describe the synthetic safe case as a real fill or claim the Agentic Wallet or Agent Studio special without an actual integration.
