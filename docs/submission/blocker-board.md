# Submission blocker board

**Checked:** 2026-10-04 UTC. **Deadline:** 2026-10-11 12:00 UTC.

| BLOCKER | OWNER | EVIDENCE NEEDED | DEADLINE | STATUS |
|---|---|---|---|---|
| Canonical demo asset | Dyplux | [Dated comparison](demo-asset-selection.md) selects NVDAB for technical preflight; issuer and user access still need a dated basis. Two [wrapped xStock fallbacks](../research/2026-10-04-xstock-route-fallback.md) had indexed USDT pairs but no 10 USDT Binance Web3 route. | 2026-10-05 | TECHNICAL TARGET SELECTED, ACCESS OPEN |
| Funded exact-wallet simulation | Dyplux | Same wallet and quote proven; [fixed-block funding read](../product/demo-wallet-state-2026-10-04.md) found zero USDT, BNB and allowance. The 17:49 fresh packet bound the built EVM call to the simulation request, checked the build's 0.5% slippage and positive minimum received, then predicted `FAILED`. Passing funded simulation and full approval gas estimate remain. New packets reject quotes older than 60 seconds; provider expiry wasn't exposed in the observed route. | 2026-10-06 | BUILD BOUNDS CHECKED, WALLET UNFUNDED |
| Mainnet proof | Dyplux + founder | `ALLOW` policy, passing simulation, specific human approval, transaction hash and before/after balances | 2026-10-07 | NOT AUTHORIZED |
| Public repository | Dyplux | Final tracked and history secret scan, public visibility, signed-out access | 2026-10-05 | VERIFIED: public HTTP 200, bounded secret scan; keep available through judging |
| Public judge path | Dyplux | Stable page, dated/live evidence, receipt download, status, repo and judge instructions | 2026-10-06 | VERIFIED DATED PACKET: Chrome desktop/mobile, both receipt hashes, no page errors or horizontal overflow; no public live API service |
| Agentic Wallet path | Dyplux | Official login eligibility or a documented Wallet Skills integration that invokes the same policy | 2026-10-06 | READ-ONLY TOOL EXISTS |
| BNB Agent Studio path | Dyplux | Minimum real identity/runtime integration using the safety or rebalancing core | 2026-10-07 | OFFICIAL PATH MAPPED; no runtime deployed or buyer observed |
| Final DevEx report | Dyplux + founder | [Current 53-item answer map](dx-form-safety-answer-map.md), reproducible observations, Monday regular-session cut and founder review of private or subjective answers | 2026-10-08 | FACTUAL DRAFT READY; FOUNDER AND MONDAY PENDING |
| Final product demo | Dyplux | [Dated real read-only video](safety-video-qa.md) and public judge link; safe `ALLOW` remains a labelled synthetic fixture. Editorial audio check and any later mainnet proof must be separate. | 2026-10-09 | READ-ONLY FILM RENDERED; NO EXECUTION PROOF |
