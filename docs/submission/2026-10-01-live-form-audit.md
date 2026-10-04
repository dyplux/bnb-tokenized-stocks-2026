# Live submission-form audit, 1 October 2026

**Read-only check:** Opened the public [project submission form](https://forms.gle/yToDUzaDMwWnq6R6A), [Developer Experience Report form](https://forms.gle/EUQ39xf54GHjC2ys5) and [hacker registration form](https://forms.gle/NEmy3FxYc4f5Dua47) on 1 October 2026. Read the embedded Google Forms item metadata and visible descriptions. No form was filled or submitted. Field order and requirements can change; recheck before submission.

## Critical correction

The [event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) calls a demo video of at most four minutes strongly recommended but optional. The **current project submission form marks `Demo video URL` required**. Plan to deliver a judge-accessible video URL of at most four minutes. Treat the live form as the immediate submission constraint while asking organizers to resolve the inconsistency if needed. A missing video could block form submission even if the event copy says optional.

## Submission form: 10 items

| # | Field | Required | Preparation |
|---:|---|---|---|
| 1 | Team or project name | yes | Match the registration and DX report. |
| 2 | Contact email | yes | Use the same address in all three forms; founder confirms it. |
| 3 | Wallet address (ERC-20) | yes | The description allows a Binance UID instead. Founder supplies the receiving address or UID privately; never put a UID in Git. |
| 4 | Telegram handle | no | Founder decides whether to include it. |
| 5 | What did you build? | yes | State user, task, Binance Web3 API modules actually called and stock tokens actually used. |
| 6 | Which tracks are you applying for? | yes | Main track. Select Agentic Wallet or Agent Studio only if a working integration merits it. |
| 7 | Public repository URL | yes | Make this project's repo public at submission, after review; keep it accessible through judging. |
| 8 | Demo video URL | **yes in live form** | At most four minutes; confirm a signed-out judge can open it. |
| 9 | Deployed link, or instructions a judge can run | yes | A live URL is preferred; a reproducible local path is accepted by the field description. |
| 10 | Developer Experience Report | yes | Checkbox confirms the separate report has already been submitted. Without it, the project is not scored. |

The form introduction says one submission per team and deadline **Sunday 11 October 2026, 12:00 UTC**. A public repo, live demo or judge instructions, video URL and completed DX report should be ready before opening the final form.

## Developer Experience Report: 53 items, seven sections

The report includes 46 questions after seven section headers. The required fields are extensive and demand original experience rather than a generic narrative:

1. **Submission details, items 2-8:** team/project name, same contact email, public repo URL, API modules or tools actually called, team size, Web3 experience and prior Binance Web3 API use.
2. **Onboarding, items 10-16:** time from docs to first successful call, key creation time, onboarding rating, exact blocked step, unexpectedly slow step, whether `llms.txt` was used, and optional agent error detail. The form offers `We never got a fully successful call` as a time choice; that is a factual fallback, not the target outcome.
3. **Documentation, items 18-23:** rating, specific errors, missing topics, whether examples ran as written, failed example changes, and most useful page.
4. **API pitfalls, items 25-32:** reliability rating, observed edge cases, unclear errors, endpoint latency, rate-limit observation, signing difficulties and data that could not be reconciled. Do not present our unexecuted research probe as a measured API error.
5. **AI stack, items 34-39:** tools actually used, execution-layer rating including an N/A choice, successes, failures, gaps and optional Agent Studio experience.
6. **Tokenized stocks, items 41-46:** platforms actually used; required free-text answers for liquidity depth, slippage and off-hours behavior; optional reference-price gaps and wrapper differences. If a quantity wasn't observed, say so explicitly rather than inventing it. Public CEX and DEX research measurements are distinct from signed Web3 API quotes and fills.
7. **Redesign, items 48-53:** first-five-minute developer experience, requested endpoints or tooling, single biggest time-saving change, continuation intention and optional final remarks. Recommendations must flow from actual work.

The separate [DX field log](../dx/field-log.md) maps observations to these sections. It starts incomplete. The contact email, account details, wallet address and UID remain out of the repository.

## Registration form: seven items

Team/project name and contact email are required; Telegram is optional. It asks for the Binance UID **or email of the account that created the Web3 API key** to route elevated limits, team size, a nonbinding one-line build idea and an eligibility confirmation. The founder handles account identity and eligibility. The current [one-line draft](form-answer.md) is exploratory and hasn't been submitted here. The three forms must use the same project name and contact email.

## Sequence and open checks

1. Finish a working product with a genuine Binance Web3 API call and a documented judge path.
2. Capture actual API steps, errors, responses, liquidity and market-hours observations in the DX log without headers, secrets or private wallet data.
3. Prepare a video under four minutes and verify the URL without an authenticated session.
4. Review repository contents for secrets and make the project repo public when the founder authorizes submission.
5. Submit the DX Report first, then the project form. Founder supplies the contact email and prize-receiving wallet address or UID through the forms, not through committed files.

**As of this 1 October audit, not yet proven:** any successful Binance Web3 API request, final product name, deployed URL, video, public repo, completed report or submitted form. Signed RWA search and quote calls were later observed on 2 October; see the [DX log](../dx/field-log.md).

**2 October read-only recheck:** the public DX form still exposed 53 items through its embedded form metadata. The required questions and choices used in the [answer draft](dx-form-draft.md) were read again. No answer was entered or submitted. Recheck the live form before final submission.

**3 October read-only recheck:** both public Google Forms loaded without signing in. The [DX form](https://forms.gle/EUQ39xf54GHjC2ys5) still exposed **53 items**, with the same seven section headers and required questions mapped in the draft. The [project form](https://forms.gle/yToDUzaDMwWnq6R6A) still exposed **10 items** and still marked `Demo video URL`, `Public repository URL`, `Deployed link, or instructions a judge can run`, and `Developer Experience Report` as required. The [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview) still listed the lock at **11 October 2026, 12:00 UTC** and called a video of four minutes or less strongly recommended but optional. The form's required video field remains the immediate submission constraint. No field was filled or submitted.

**4 October read-only recheck:** both Forms returned HTTP 200 without signing in. The embedded public metadata still contained 53 DX items and ten project items. Project item 6 offers Main track and the two special-prize choices; item 8 requires a video URL; item 10 requires the separate DX form to have been submitted. [Current-product DX map](dx-form-safety-answer-map.md) and [project answer map](project-form-safety-answer-map.md) replace the retired Exit Check copy aid. No form was filled or submitted during this check.
