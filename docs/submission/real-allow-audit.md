# Can a real action reach ALLOW?

**Checked:** 2026-10-04 UTC. **Scope:** one BNB Chain spot purchase under [policy 0.6.0](../../app/rwa_policy.py). This is an audit of the current evidence, not a request to trade.

## Result

No observed purchase can honestly receive `ALLOW` or `ALLOW_PENDING_SIGNATURE` today. The [15:57 UTC NVDAB receipt](../judge/observed-unsafe.json) is a real dated API evaluation and returns `NEED_HUMAN` for five reason codes: `INDEPENDENT_REFERENCE_TIME_UNKNOWN`, `ISSUER_UNVERIFIED`, `MARKET_STATE_UNKNOWN`, `SIMULATION_UNVERIFIED` and `USER_ELIGIBILITY_UNKNOWN`. Its quote is real; its access, stock clock and funded execution aren't proven. The public [synthetic safe fixture](../judge/synthetic-safe.json) demonstrates the passing code path only and is labelled synthetic in the judge page.

## Bounded candidate check

| Candidate | Observed evidence | Remaining gate |
|---|---|---|
| NVDAB | 10 USDT exact-wallet quote, matching unsigned build, fixed-block multiplier, off-chain simulation | bStock user and asset access unknown; demo wallet unfunded; predicted simulation `FAILED`; independent stock clock missing; route target provenance incomplete. [Selection record](demo-asset-selection.md). |
| NVDAon | 10 USDT exact-wallet quote, unsigned build and off-chain simulation | Demo wallet unfunded; predicted simulation `FAILED`; independent stock clock missing; this specific token's current EEA terms and founder eligibility aren't verified. Ondo's [general eligibility page](https://docs.ondo.finance/ondo-stocks/eligibility) restricts EEA users to qualified/professional categories, while its later [EU announcement](https://ondo.finance/blog/ondo-eu-regulatory-approval) says retail access has been approved. A broad announcement doesn't decide this person's access to NVDAon through this route. |
| AAPLx or NVDAx | Public BNB Chain listing and signed price rows | The bounded Binance Web3 quote checks returned no route. [Route record](demo-asset-selection.md). |
| wPOPMTx or wTCENTx | Public indexed USDT pair | Both exact-wallet 10 USDT Binance Web3 quotes returned business `40374`, so no build or simulation followed. [Fallback record](../research/2026-10-04-xstock-route-fallback.md). |

The current live [safety service](../../app/safety_service.py) deliberately sets `eligibility_status=UNKNOWN`, `issuer_verified=false`, `simulation_passed=false` and independent reference age `UNKNOWN` unless those facts have been established by separate evidence. Changing these fields just to produce an `ALLOW` receipt would fabricate a safe case. An explicit mandate waiver of stock-reference time would still leave issuer access and funded simulation unresolved. `ALLOW_PENDING_SIGNATURE` would imply all non-signature gates passed; that isn't the observed state.

## Submission treatment

Use the real `NEED_HUMAN` receipt as the main case and the [19:56 UTC mandate denial](../judge/observed-mandate-deny.json) as the second safety behavior. That live read-only request returned a signed route, but the 100 USDT action exceeded its 20 USDT mandate and the policy returned `DENY`; receipt SHA-256 `a720aa7010b3287cf75f450b8cc2501a75a1465db37e56c7ffd751196b4626e8`. The public JSON has been scanned against the local `.env`, and its receipt hash was verified before publication. Keep the synthetic `ALLOW` fixture visible only as a policy demonstration. The [official event rules](../01-event-rules.md) require a working Binance Web3 API integration, public repository, judge-accessible demo or instructions, and a Developer Experience Report; the track also asks teams to demonstrate the flow with small live amounts. A submission without an approved mainnet trade can satisfy the listed form materials and show the working read-only API flow, but may lose technical or product credit for the missing live amount. Don't call the build execution-complete or promise a prize result.

Only a dated issuer or venue basis for the exact person, asset and action, a funded passing exact-wallet simulation, source-verified route target and fresh policy evidence could make a later purchase eligible for `ALLOW`. Signing and broadcast would still require explicit human approval for that exact packet. Monday's off-hours result doesn't change these gates or the existence of the safety product.
