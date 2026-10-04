# Developer Experience form: safety-product answer map

**Form rechecked:** 2026-10-04 UTC. The public [Developer Experience form](https://forms.gle/EUQ39xf54GHjC2ys5) still exposes 53 items, including seven section headers and 46 questions. Its introduction says vague, perfunctory or AI-generated reports aren't accepted. This file is a **fact-check and copy aid for the founder**, not a submitted first-hand report. The founder must review every answer and enter private fields and subjective ratings personally. The [current evidence summary](dx-form-current.md), [17:25 UTC metrics cut](../devex/2026-10-04-metrics.json), [sanitized call ledger](../devex/raw/2026-10-04.jsonl) and [dated reproductions](../devex/2026-10-04-evidence-summary.md) support the objective statements below. Numbers after that cut are labelled separately. Monday's regular-session evidence must be added before submission.

`FOUNDER` requires a first-hand or private answer. `MEASURED` is a proposed factual answer to review. `PENDING` needs the final build or Monday observation. Don't copy a `PENDING` line into the form as if it had happened. Only questions marked required in the live form are labelled `*` here.

## 1. Submission details

| Item | State | Answer or founder action |
|---|---|---|
| 2. Project name* | FOUNDER | Use the final safety-product name, identical in the registration, DevEx and project forms. Current repo working name: Dyplux Execution Safety Layer for Tokenized Equities. |
| 3. Contact email* | FOUNDER | Enter privately in the form; keep it out of Git. |
| 4. Public repository URL* | MEASURED | `https://github.com/dyplux/bnb-tokenized-stocks-2026`. Check signed-out access again at submission. |
| 5. Web3 API modules/tools used* | MEASURED | Select **RWA Data API**, **Trading API** and **Transaction API**. These have signed observed calls. Earlier separate research also used General/Market and DeFi reads; select those only if reporting every development call, with that distinction. Do not select Agentic Wallet, Wallet Skills or Agent Studio as integrated products. A public endpoint described by Wallet Skills was called directly, but the skill wasn't installed. |
| 6. Team size* | FOUNDER | Founder said this is a solo developer project; confirm whether the form counts any other actual human contributor. AI agents aren't team members. |
| 7. Most experienced member's Web3 tenure* | FOUNDER | Select the true tenure category. No duration was measured in this repo. |
| 8. Prior Web3 API use* | FOUNDER | Select the true category from personal history. The current project can't prove earlier experience. |

## 2. Onboarding

| Item | State | Answer or founder action |
|---|---|---|
| 10. Docs to first successful call* | FOUNDER | First signed success was logged on 2 October at 18:27:43.513 UTC. Docs-open time wasn't recorded; choose the interval from memory, not from this timestamp alone. |
| 11. Portal key creation time* | FOUNDER | Start and completion times weren't captured. Choose the remembered interval. |
| 12. Onboarding rating* | FOUNDER | Personal 1–5 rating. |
| 13. Exact stuck step* | MEASURED, founder review | The complete secret didn't initially reach the remote development environment. Once the ignored local `.env` held both values, the first signed RWA search returned HTTP 200 and business code 0. This was credential transfer, not an observed portal outage. |
| 14. Unexpectedly slow step* | MEASURED, founder review | Checking signature headers, BSC token decimals and the first response fields took extra work. No timed duration was recorded for those steps. |
| 15. `llms.txt` use* | FOUNDER | Choose based on whether either file was actually fed to a coding agent as one input. Reading linked docs individually isn't the same claim. |
| 16. AI coding mistake | MEASURED, founder review | An early draft used Spot-style `X-MBX-*` headers; it was corrected to Web3 `X-OC-*` before the first live call. An early quote ladder used six-decimal units for an 18-decimal BSC USDC token and was quarantined. These were our integration mistakes. |

## 3. Documentation

| Item | State | Answer or founder action |
|---|---|---|
| 18. Documentation rating* | FOUNDER | Personal 1–5 rating. |
| 19. Documentation errors* | MEASURED, founder review | The [RWA reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) omits the observed `offhours` market value. The [Trading endpoint reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says equity/RWA routes are RFQ while seven of eight Sunday provider-side cases returned `SWAP`; the Trading introduction already mentions bStock SWAP. A documented 100-address price GET returned HTTP 414 at about 4,597 URL characters. Keep the route wording as a documentation conflict, not a proven backend defect. |
| 20. Missing topics* | MEASURED, founder review | The independently sourced stock-reference timestamp, `referencePrice` provenance, bStock country-eligibility endpoint path/schema, RWA route expiry and `estimateGasFee` units need explicit documentation. The [eligibility documentation check](../devex/repros/2026-10-04-bstock-eligibility-documentation-gap.md) also shows why the Web3 API service-region list cannot replace the asset-specific check. [Other repros and exact questions](../devex/mentor-questions.md). |
| 21. Code examples runnable* | FOUNDER | Select **I did not try the examples** unless a verbatim example was run. A separate client isn't a verbatim example test. |
| 22. Failed examples | FOUNDER | Leave blank unless a specific verbatim example failed; name its URL and exact fix if it did. |
| 23. Most useful page | FOUNDER | The [authentication page](https://web3.binance.com/en/dev-docs/authentication) corrected the signed headers. Select it only if it was most useful firsthand. |

## 4. API pitfalls

| Item | State | Answer or founder action |
|---|---|---|
| 25. Reliability rating* | FOUNDER | Personal 1–5 rating. The 17:25 cut has 484 mixed research/collector calls and no observed HTTP 429; it isn't a controlled reliability benchmark. |
| 26. Edge cases* | MEASURED, founder review | A Sunday signed 488-row catalog included `offhours` for 31 Ondo assets. NVDA `/underlying-market` gave `openState=true` with Ondo `offhours` and bStock null status. Some indexed xStock wrappers had USDT pairs but exact-wallet aggregator quotes returned `40374`. A quote isn't issuer access or a fill. |
| 27. Unclear error messages* | MEASURED, founder review | `40374` says insufficient liquidity but doesn't distinguish an unsupported wrapper/vendor route from a missing on-chain pool. Two wrapped xStock 10 USDT calls returned it despite separately indexed USDT pairs. This doesn't establish that the API should have routed them. The exact request and response hashes are [recorded](../research/2026-10-04-xstock-route-fallback.md). |
| 28. Slow endpoints | MEASURED, founder review | At the 17:25 mixed-workload cut, signed `/tokens` had 2,193.37 ms median and 3,875.75 ms nearest-rank p95. Don't call that unacceptable latency without a user-task threshold. |
| 29. Rate limits* | MEASURED | Select **No** if the final ledger still has no HTTP 429. None appeared in the 17:25, 484-call cut. |
| 30. Rate-limit detail | PENDING | Leave blank if no rate limit is observed through submission. |
| 31. Signing/auth problems | MEASURED, founder review | The first code draft used the wrong header family; this was fixed before a live signed request. No live signature-rejection incident is recorded. |
| 32. Data not reconciled | MEASURED, founder review | `tokenPriceUpdatedAt` is a token clock, not an independent stock clock. In 40 same-cycle contracts, `referencePrice` matched token price divided by share ratio at reported precision, but its upstream source and stock as-of time remain unknown. The policy therefore keeps reference age `UNKNOWN`. |

## 5. AI stack

| Item | State | Answer or founder action |
|---|---|---|
| 34. AI stack used* | MEASURED | **None of the above** for the current public build. A local read-only JSON policy tool and Agent Studio feasibility probe aren't an installed Wallet Skill or deployed Studio runtime. Re-evaluate only after a working integration. |
| 35. AI execution rating* | MEASURED | **N/A, did not use it**, unless item 34 changes after a real runtime trial. |
| 36–39. What worked, failed, missing, Studio experience | PENDING | Leave optional fields blank while no official AI runtime has been used. Don't claim the special-prize integration from local scaffolding. |

## 6. Tokenized stocks

| Item | State | Answer or founder action |
|---|---|---|
| 41. Platforms worked with* | MEASURED, founder review | bStocks and Ondo were used in signed quotes and safety reviews. xStocks were used in signed price and no-route checks, with two wrapped-token quote rejections. Select all three only if “worked with” includes read-only development; no platform had a filled trade. |
| 42. Liquidity depth* | MEASURED, founder review | A Sunday 100 USDT indicative Binance Web3 quote check returned routes for 38 of 40 monitored bStock/Ondo contracts. Two returned `40374`; one AAOI result later changed with size/time. This measures route availability for those requests, not executable depth or inventory. The wrapped xStock fallback returned no aggregator route at 10 USDT despite two separately indexed USDT pairs. |
| 43. Slippage at sizes used* | MEASURED, founder review | **No realized slippage was measured:** no trade was filled. The unsigned NVDAB build requested a 0.5% slippage limit and exposed a positive minimum receive amount; that is a bound, not a result. Quotes at 10, 100, 1,000 and 10,000 USDC exist for two assets, but sequential estimates aren't executions. |
| 44. Outside market hours* | MEASURED, Monday pending | The 40-contract live Sunday tape sampled at five-minute slots, with 4,076 unique observations by 19:00 UTC and zero consecutive collection failures. Token-price timestamps moved for the monitored assets, but no independent underlying-stock as-of time was returned. Market-state fields differed by provider. The preregistered Monday comparison isn't scored yet; don't claim a weekend trading edge. |
| 45. On-chain versus stock reference | MEASURED | No independently timestamped stock reference was available for a defensible live premium/discount. Forty same-cycle `referencePrice` values matched token-price/share-ratio arithmetic; this doesn't prove upstream stock-source provenance. |
| 46. Provider differences | MEASURED | bStock and Ondo quotes for NVDA existed, but issuer rights and user eligibility differ and aren't resolved by ticker. Of 130 public BSC xStock listings, 77 had null token-price/time fields in the signed price probe; 36 of 53 timestamped rows were over seven days old on Sunday. The wrapper route check is separate. No legal or economic equivalence is claimed. |

## 7. Redesign

| Item | State | Answer or founder action |
|---|---|---|
| 48. First five minutes* | MEASURED, founder review | Put one copyable BSC tokenized-stock read-only example on the docs landing path: key setup, exact `X-OC-*` signing, current 18-decimal USDT units, a real quote response, observed route modes, business-error interpretation and a link to build/simulation. Distinguish API success from simulated transaction success. |
| 49. Requested tooling* | MEASURED, founder review | Publish stock-reference source/as-of time, bStock country-eligibility endpoint path and scope, explicit RWA route expiry, vendor support for wrapped xStocks, and a price-batch method that avoids the observed 100-address HTTP 414. |
| 50. One time-saving change* | MEASURED, founder review | Publish the country-eligibility endpoint URL and schema, with a self-custody example. Its absence is the current reason an otherwise quotable NVDAB action can't be cleared for an eligible-person mainnet demo. This is a blocker observation, not a measured number of hours lost. |
| 51. Continue building?* | FOUNDER | Select the actual intention after the final build and Monday measurement. |
| 52. Why? | FOUNDER | Explain the chosen item 51 answer from firsthand product plans. |
| 53. Final remarks | MEASURED, founder review | The signed RWA, Trading and Transaction endpoints supplied enough data to build a fail-closed pre-signing receipt. The missing issuer-access and independent stock-clock fields keep the current real action in `NEED_HUMAN`; the public judge demo shows that limit. |

## Before submission

Reopen the live form, revise every answer against the final build, add Monday results only after the frozen protocol scores them, and replace all `FOUNDER` and required `PENDING` items. The founder submits the DX form **before** the project form. No form submission receipt exists in this repository.
