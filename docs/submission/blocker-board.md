# Submission readiness board

**Checked:** 2026-10-04 UTC. **Deadline:** 2026-10-11 12:00 UTC.

The working safety product, public repository, judge path, video and DevEx report form the submission path. One dated operator-authorized SPYon purchase is now proven and indexed in the [final proof](final-proof-2026-10-09.md). General autonomous trading, universal signer enforcement and production-feed guarantees remain outside the proof.

| BLOCKER | OWNER | EVIDENCE NEEDED | DEADLINE | STATUS |
|---|---|---|---|---|
| Canonical demo asset for optional trade | Dyplux | [Dated comparison](demo-asset-selection.md) selects NVDAB for technical preflight; issuer and user access still need a dated basis. Two [wrapped xStock fallbacks](../research/2026-10-04-xstock-route-fallback.md) had indexed USDT pairs but no 10 USDT Binance Web3 route. | 2026-10-05 | OPTIONAL EXECUTION GATE: TECHNICAL TARGET SELECTED, ACCESS OPEN |
| Funded exact-wallet simulation for optional trade | Dyplux | Same wallet and quote proven; [fixed-block funding read](../product/demo-wallet-state-2026-10-04.md) found zero USDT, BNB and allowance. The 17:49 fresh packet bound the built EVM call to the simulation request, checked the build's 0.5% slippage and positive minimum received, then predicted `FAILED`. Passing funded simulation and full approval gas estimate remain. New packets reject quotes older than 60 seconds; provider expiry wasn't exposed in the observed route. | 2026-10-06 | OPTIONAL EXECUTION GATE: WALLET UNFUNDED |
| Mainnet proof | Dyplux + founder | Private-wrapper `ALLOW`, verified route, real-state RPC pass, Binance success, specific operator authorization, approval and swap hashes, two signatures, two dispatches and gas receipt | 2026-10-09 | PROVEN FOR ONE BOUNDED SPYon ACTION; NOT GENERAL AUTONOMOUS TRADING |
| Public repository | Dyplux | Final tracked and history secret scan, public visibility, signed-out access | 2026-10-05 | VERIFIED: public HTTP 200, bounded secret scan; keep available through judging |
| Public judge path | Dyplux | Stable page, dated/live evidence, receipt download, status, repo and judge instructions | 2026-10-06 | VERIFIED: two observed cases and one synthetic fixture; local Chrome at 1440, 390 and 320 px passed; deployed page, JavaScript and denial receipt checked after `c32153a` |
| Agentic Wallet path | Dyplux | Official login eligibility or a documented Wallet Skills integration that invokes the same policy | 2026-10-06 | READ-ONLY TOOL EXISTS |
| BNB Agent Studio path | Dyplux | [Compact proof](agent-studio-evidence.md), testnet identity, managed replay, x402 settlement and new-process recovered explanation. | 2026-10-09 | DATED PROOF; ORIGINAL PROCESS CONTINUITY AND COMPLETE AUTONOMOUS LOOP UNPROVEN |
| Final DevEx report | Dyplux + founder | [Current 53-item answer map](dx-form-safety-answer-map.md), reproducible observations, Monday regular-session cut and founder review of private or subjective answers | 2026-10-08 | FACTUAL DRAFT READY; FOUNDER AND MONDAY PENDING |
| Final product demo | Dyplux | The [120-second film](https://praeva.dyplux.com/media/praeva-bnb-hack-final-v2.mp4) predates the live SPYon proof. The console retains static NEED_HUMAN, historical DENY and synthetic ALLOW cases. | 2026-10-09 | VIDEO PREDATES LIVE PURCHASE; ROOT PROOF PACKET IS CURRENT |
