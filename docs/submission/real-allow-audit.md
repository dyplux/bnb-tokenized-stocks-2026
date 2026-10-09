# Can a real action reach ALLOW?

**Checked:** 2026-10-09 UTC. **Scope:** dated BNB Chain spot purchase evidence plus the historical [policy 0.6.0](../../app/rwa_policy.py) cases. This is an audit of the evidence, not a request to trade.

## Result

The [9 October live SPYon packet](../judge/live/spyon-purchase-2026-10-09.json) records one operator-authorized purchase that reached private-wrapper `ALLOW`, passed real-state RPC and Binance checks, and settled. The earlier [15:57 UTC NVDAB receipt](../judge/observed-unsafe.json) remains a historical `NEED_HUMAN` result. The public [synthetic safe fixture](../judge/synthetic-safe.json) remains a code-path demonstration. The live packet supports one bounded action, not general autonomous trading, universal signer enforcement or a production-feed guarantee.

## Bounded candidate check

| Candidate | Observed evidence | Remaining gate |
|---|---|---|
| NVDAB | 10 USDT exact-wallet quote, matching unsigned build, fixed-block multiplier, off-chain simulation | bStock user and asset access unknown; demo wallet unfunded; predicted simulation `FAILED`; independent stock clock missing; route target provenance incomplete. [Selection record](demo-asset-selection.md). |
| NVDAon | 10 USDT exact-wallet quote, unsigned build and off-chain simulation | Demo wallet unfunded; predicted simulation `FAILED`; independent stock clock missing; this specific token's current EEA terms and founder eligibility aren't verified. Ondo's [general eligibility page](https://docs.ondo.finance/ondo-stocks/eligibility) restricts EEA users to qualified/professional categories, while its later [EU announcement](https://ondo.finance/blog/ondo-eu-regulatory-approval) says retail access has been approved. A broad announcement doesn't decide this person's access to NVDAon through this route. |
| AAPLx or NVDAx | Public BNB Chain listing and signed price rows | The bounded Binance Web3 quote checks returned no route. [Route record](demo-asset-selection.md). |
| wPOPMTx or wTCENTx | Public indexed USDT pair | Both exact-wallet 10 USDT Binance Web3 quotes returned business `40374`, so no build or simulation followed. [Fallback record](../research/2026-10-04-xstock-route-fallback.md). |

The current live [safety service](../../app/safety_service.py) deliberately sets `eligibility_status=UNKNOWN`, `issuer_verified=false`, `simulation_passed=false` and independent reference age `UNKNOWN` unless those facts have been established by separate evidence. Changing these fields just to produce an `ALLOW` receipt would fabricate a safe case. An explicit mandate waiver of stock-reference time would still leave issuer access and funded simulation unresolved. `ALLOW_PENDING_SIGNATURE` would imply all non-signature gates passed; that isn't the observed state.

## Submission treatment

Keep the historical `NEED_HUMAN`, historical mandate `DENY` and synthetic `ALLOW` cases visible in the console. Add the [9 October live proof](../judge/live/spyon-purchase-2026-10-09.json) as a separate dated artifact. The [official event rules](../01-event-rules.md) require a working Binance Web3 API integration, public repository, judge-accessible demo or instructions, and a Developer Experience Report. The live proof improves the main-track evidence, but it does not establish general autonomous trading or promise a prize result.

Only a dated issuer or venue basis for the exact person, asset and action, a funded passing exact-wallet simulation, source-verified route target and fresh policy evidence could make a later purchase eligible for `ALLOW`. Signing and broadcast would still require explicit human approval for that exact packet. Monday's off-hours result doesn't change these gates or the existence of the safety product.
