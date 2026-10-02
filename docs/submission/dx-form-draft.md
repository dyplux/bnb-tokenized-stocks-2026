# Developer Experience Report answer draft

**Prepared:** 2026-10-02 for the [official DX form](https://forms.gle/EUQ39xf54GHjC2ys5). This is a copy aid, not a submitted report. The [live form audit](2026-10-01-live-form-audit.md) and [field log](../dx/field-log.md) are the evidence record. Recheck every field before submission. `FOUNDER` means the answer requires first-hand input or a private value. `LATER` means the build still needs an observation. No key, UID, wallet address or private contact belongs in this file.

## 1. Submission details

| Item | Draft answer | State |
|---|---|---|
| 2. Team or project name | Final project name, same in all forms | FOUNDER |
| 3. Contact email | Enter directly in the form | FOUNDER |
| 4. Public repository URL | `https://github.com/dyplux/bnb-tokenized-stocks-2026` after the founder authorizes publication and a signed-out check passes | LATER |
| 5. Binance Web3 API modules or tools | Select **RWA Data API** and **Trading API**. Two signed RWA searches and five read-only quotes ran on 2 October. Public BNB Chain RPC and Venus/Pancake data were separate integrations, not Binance Web3 API modules. | READY |
| 6. Team size | Select from actual human contributors. Agents aren't people on the team. | FOUNDER |
| 7. Most experienced team member's Web3 experience | Select the true category. | FOUNDER |
| 8. Prior Binance Web3 API use | Select from actual prior experience. | FOUNDER |

## 2. Onboarding

| Item | Draft answer | State |
|---|---|---|
| 10. Docs to first successful call | First success: **2026-10-02 18:27:43.513 UTC**. The first docs-open time wasn't captured, so don't infer a form category from the dates alone. | FOUNDER |
| 11. Time to working portal key | The founder created the key, but portal start and finish times weren't recorded. | FOUNDER |
| 12. Overall onboarding rating | Select a first-hand rating. | FOUNDER |
| 13. Where stuck | Suggested factual text: “The complete secret didn't reach the remote development environment at first. Once both values were in the Git-ignored local `.env`, the first signed RWA search returned HTTP 200 and business code 0. This was our credential-transfer setup, not a measured portal outage.” | READY, founder review |
| 14. Unexpectedly slow step | Suggested text: “We had to check the signing path and raw token units against the docs. The full secret was initially unavailable in the remote environment, so live verification waited until 2 October. We didn't time those separate setup steps.” | READY, founder review |
| 15. `llms.txt` or `llms-full.txt` fed to an AI agent | The project used the documentation as a source, but the team hasn't recorded whether either file was fed to an agent as a single input. Choose the accurate option. | FOUNDER |
| 16. AI agent mistake, optional | “An early code draft used Spot-style `X-MBX-*` headers and wrong parameter names. Review against the Web3 authentication and Trading API references corrected it to `X-OC-*` before any live call. This was our generated-code error, not an API failure.” | READY |

## 3. Documentation issues

| Item | Draft answer | State |
|---|---|---|
| 18. Documentation rating | Select a first-hand rating. | FOUNDER |
| 19. Errors found | “The Get Aggregated Quote reference says equity/RWA routes always return `RFQ`, but a signed 1 NVDAB to USDT request returned `LiquidMesh` with `executionMode=SWAP` on 2 October. The same reference describes `amount=1000000` as 1 USDT at six decimals while its example response labels that USDT token `decimal: 18`. We checked NVDAB and BNB Chain USDT decimals on-chain instead of copying the example.” See the [live quote](../research/2026-10-02-first-live-binance-quote.md). | READY |
| 20. Missing or under-documented topics | “Please define bStock route selection and execution-mode guarantees, the source and as-of time of RWA `referencePrice`, and the precise unit and cost scope of `estimateGasFee` and `toTokenAmount` for stock routes.” Source provenance and costs remain unresolved. | READY |
| 21. Examples runnable as written | Select **I did not try the examples** if the founder didn't run any verbatim. We wrote and checked a separate client; don't call that a verbatim example test. | FOUNDER |
| 22. Failed examples, optional | Leave blank unless a verbatim example was actually run and failed. | FOUNDER |
| 23. Most useful documentation page, optional | [Authentication](https://web3.binance.com/en/dev-docs/authentication) was used to correct the signed request; founder can choose it. | FOUNDER |

## 4. API pitfalls

| Item | Draft answer | State |
|---|---|---|
| 25. Reliability rating | Select a first-hand rating. Six successful read-only calls aren't enough to score broad reliability objectively. | FOUNDER |
| 26. Edge cases or unexpected behavior | “A bStock quote returned `SWAP` despite the RFQ-only sentence in the endpoint reference. The route carried a short-lived estimate; we kept its mode visible and didn't treat it as an executable order. We observed no nonzero API business code.” | READY |
| 27. Unclear error messages | “None observed in the seven signed calls. Each returned HTTP 200 and business code 0. The route-mode and decimal issues were documentation inconsistencies, not error messages.” | READY |
| 28. Slow endpoints, optional | “No endpoint was clearly too slow in this small sample. The two RWA searches took 1051.8 and 651.814 ms. Recorded quote calls took 315.419, 303.133, 847.939 and 833.917 ms; the fourth quote latency wasn't captured.” | READY |
| 29. Rate limits | Select **No** if no later limit occurs. None was observed in the six recorded calls. | READY at current evidence |
| 30. Rate-limit detail, optional | Leave blank unless a real limit is observed later. | LATER |
| 31. Signing difficulties, optional | “The first local draft used the wrong Binance header family. We corrected the `/build` path and `X-OC-*` signature before calling the API. Once the complete pair was present, signed RWA search and quote requests succeeded; no live signature rejection occurred.” | READY |
| 32. Data not trusted or reconciled, optional | “We didn't use `referencePrice` as an independent share quote because its upstream source and as-of time weren't established. We also withheld net sale proceeds: the quote estimated buy-token units, but final gas and execution costs weren't observed.” | READY |

## 5. AI stack feedback

| Item | Draft answer | State |
|---|---|---|
| 34. AI stack used | Select **None of the above** unless Agentic Wallet, Wallet Skills, Wallet Skills CLI or BNB Agent Studio is actually integrated before submission. A general coding assistant doesn't count as one of these choices. | READY at current build |
| 35. AI execution-layer rating | Select **N/A, did not use it** while item 34 is None. | READY at current build |
| 36 to 39. AI stack successes, failures, gaps, Agent Studio | Leave optional answers blank unless an official AI product is actually used. | LATER |

## 6. Tokenized-stock specifics

| Item | Draft answer | State |
|---|---|---|
| 41. Platforms | Select **bStocks**. The build used NVDAB. Don't imply an executed trade. | READY |
| 42. Liquidity depth | “For 1 NVDAB, five read-only Binance Web3 quote requests each returned one LiquidMesh SWAP route. We didn't measure depth across sizes or execute a trade, so this can't establish available depth or a fill.” | READY, may expand |
| 43. Slippage at trade sizes used | “No trade was executed, so realized slippage wasn't measured. The quote output is an estimate. One same-size technical control found a 20.8697-basis-point gap versus one isolated PancakeSwap pool quote near the same time; those are different routes and not a slippage measurement.” See [route control](../research/2026-10-02-live-route-control.md). | READY, may expand |
| 44. Outside traditional market hours | “At 17:15 New York time on Friday 2 October, after the regular US equity close, a signed read-only Binance Web3 quote for 1 NVDAB to USDT returned HTTP 200, business code 0 and one LiquidMesh SWAP route in 833.917 ms. Some traditional late sessions remained open then. We didn't test weekend availability, execution, fill or spread.” See [after-close observation](../research/2026-10-02-after-regular-close-quote.md). | READY for this bounded observation |
| 45. On-chain versus underlying reference, optional | “We didn't calculate a premium or discount. The RWA `referencePrice` source and as-of time weren't established, so it wasn't used as an independent equity benchmark.” | READY |
| 46. bStocks versus Ondo/xStock, optional | “The current build tested NVDAB only. We didn't run a same-ticker, same-time representation comparison.” | READY |

## 7. Redesign and future use

| Item | Draft answer | State |
|---|---|---|
| 48. First-five-minute redesign | “Put a copyable signed RWA search and bStock quote example on the landing path, with `X-OC-*` headers, the exact `/build` signing path, an explicit BNB Chain token-decimals check and expected response mode. A developer could then prove access before building UI.” | READY |
| 49. Requested endpoints or tooling | “Add source and as-of timestamps for `referencePrice`, explicit bStock SWAP/RFQ route semantics, and machine-readable units for gas, fee and estimated received amount.” | READY |
| 50. One biggest time-saver | “A current bStock quote example and reference that agree on SWAP versus RFQ. We spent review time protecting the product from the conflicting route statements and a misleading token-decimals example; we didn't measure that time in minutes.” | READY |
| 51. Keep building on the API | Select from actual intention after the product decision. | FOUNDER |
| 52. Why, optional | Explain the decision selected for item 51, grounded in observed integration and product fit. | FOUNDER |
| 53. Final remarks, optional | “The first signed reads succeeded without a live auth or rate-limit error. Please reconcile the route-mode and quote example discrepancies so builders can present bStock routes accurately.” | READY |

## Before sending

Replace all `FOUNDER` and `LATER` fields that are required, or state honestly that the measurement wasn't made. Recheck the live form and [submission gates](readiness-gates.md). The founder supplies private fields directly to Google Forms and decides ratings. Submit this DX form before ticking the DX confirmation in the final project form. No form submission or receipt is recorded here.
