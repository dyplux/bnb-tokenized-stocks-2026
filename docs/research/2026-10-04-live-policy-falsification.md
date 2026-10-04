# What the current policy can decide from live RWA data

**Probe:** 2026-10-04 12:00 UTC, 40 LIVE BNB Chain stock-token rows in collector slot `5970384`. [The reproducible offline output](../../experiments/EXP-RWA-010/live_policy_probe.json) passes each row to policy version 0.2.0 with a **synthetic** 100 USD intent and a 60-second maximum token-price age. It never signs, quotes, simulates, uses a holder wallet or sends a trade. The policy receives unknown values for issuer verification, independent reference time, route, price impact and simulation, because those facts weren't present in the tape.

| Result | Contracts | Main reason |
|---|---:|---|
| `DENY` | 3 | COINB, GOOGLB and MRVLB token timestamps were 65.6 to 79.6 seconds old, above the synthetic 60-second mandate. |
| `NEED_HUMAN` | 37 | The data lacks at least one required gate. |
| `ALLOW` | 0 | No row had enough verified evidence to authorize an action. |

Across all 40, independent stock-reference time, issuer access, quote, impact and simulation were unverified. Thirty-five bStock rows had no market status; five Ondo rows reported `offhours`. These counts describe this one API snapshot and the deliberately strict mandate. A longer token-age limit would change the three denials, but it wouldn't resolve the missing access, route, simulation or reference evidence. The probe doesn't measure real users' preferences.

**Product consequence:** the deterministic policy is a useful internal guard and evidence receipt, but a standalone automatic “safe to trade” decision cannot be demonstrated from the current tape. If this becomes a user product, it needs an independently useful next action, a permitted issuer route, amount-specific quotes, correct gas units and transaction simulation. Another option is a read-only explanation of why an attempted route can't proceed. Both need comparison against existing stock terminals before selection. A synthetic `ALLOW` fixture doesn't satisfy the hackathon's real workflow bar.

The [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) documents signed `priceImpactPercent` values. Policy version 0.2.0 was tightened during this review to cap the **absolute magnitude**, so a negative value beyond a positive mandate limit cannot pass the guard. That is a code-level safety correction, not evidence that any of the 40 rows had a live impact value.
