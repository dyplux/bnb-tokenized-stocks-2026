# Exit Check demo: storyboard before capture

**Prepared:** 2026-10-03. **Format:** about 55 seconds, 16:9, English, intended for a judge-accessible video URL. **State:** plan only. No video, current-UI capture or `record.json` exists yet. The [live project form audit](2026-10-01-live-form-audit.md) found a required video URL; the [event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) caps the recommended video at four minutes.

## One audience and one claim

A self-custodial BNB Chain user considers a small NVDAB purchase. The video should show that the app asks for a quote in both directions before the user signs. The immediate inverse quote is only a current estimate. The video must not suggest that the later exit, profit, eligibility or execution has been proved.

## Arc

The hook is the user's decision. The product appears as a response to that decision. The proof is a continuous capture of the actual current screen and its real Binance Web3 result. The final card points to the judge-run instructions and public repository after those links exist.

| Approximate time | Screen and action | On-screen words | Required proof |
|---|---|---|---|
| 0 to 6 s | Plain dark frame, one question | “What if you can buy, but can't get a quote to leave?” | Framed as a question, not a measured failure rate. |
| 6 to 15 s | Actual app: NVDAB issuer and contract, 5 USDC input and public address entered | “Check before signing” | Capture the final local build, no private key, email or API key visible. |
| 15 to 31 s | One unbroken submit action. Show the app's real waiting state and returned result. Cut dead time if needed; don't accelerate an invented response. | No extra claim over the active UI | The actual response must be saved in a sanitized `record.json` with source times, status and amounts. |
| 31 to 44 s | Focus on entry and inverse quote, then the provider and BNB metadata receipt | “Two directions, one amount” | Values, route mode, issuer and timestamps match the captured result exactly. If the inverse route fails, show the real failure state instead of a fabricated success. |
| 44 to 51 s | Focus on the list of costs and access questions that remain unknown | “A quote isn't a fill” | Screen itself labels approval, gas, slippage, eligibility and execution as unknown. |
| 51 to 55 s | Exit Check mark and public repo or judge path | “Inspect before you sign” | Show the exact URL only after it is public and reachable without a logged-in session. |

## Capture gate

Run the final project locally and save one sanitized response record. Check the screen output against that record. Keep a dense contact sheet of the eventual render. Do not use the earlier 3 October 5 USDC research quote as though it came from this new interface. A recorded API failure is a legitimate demo state if explained, but the form must not claim a successful dual-route walkthrough unless one was captured. Store video source and render outside the public repo until inspected for secrets and personal data.
