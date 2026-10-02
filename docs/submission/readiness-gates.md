# Submission readiness gates

**Checked:** 2026-10-02. **Deadline:** 2026-10-11 12:00 UTC, per the [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks). This is an internal checklist, not a claim that an entry has been submitted. Recheck the [live forms](2026-10-01-live-form-audit.md) before sending anything.

| Gate | Current evidence | State | Next proof and owner |
|---|---|---|---|
| Hacker registration | A [non-binding one-line answer](form-answer.md) is ready. No registration receipt is recorded. | Unconfirmed | Founder confirms any existing registration or completes the [registration form](https://forms.gle/NEmy3FxYc4f5Dua47), confirms eligibility and keeps account UID/contact details outside Git. Record only that a receipt was seen. |
| Web3 credentials | The ignored project `.env` and process environment had no complete Binance Web3 key and secret at the 2026-10-02 presence check. | Blocked on founder input | Founder places a fresh full pair in the ignored `.env`. Agent checks presence without printing values and confirms permitted scope before a read-only request. |
| Required Binance integration | The app has signed RWA identity search and one-quote code. [Synthetic checks](../research/2026-10-02-binance-quote-flow-local-qa.md) passed, but no authenticated call has run. | Unproved | Agent obtains one successful signed search and a permitted holder-sized quote or a precise no-route response, with UTC time, HTTP/business codes, latency and redacted fields in the [DX log](../dx/field-log.md). No order at this gate. |
| Product decision | [D-017](../decisions/decision-log.md) allows a read-only slice. A 1 NVDAB deposit fits the measured Core cap at block 125263488, but sale proceeds and personal loan safety remain unknown. | Provisional | Agent and founder apply the [4 October checkpoint](../decisions/decision-log.md): keep, redesign or retire this candidate after the quote and same-task observation. The cap alone cannot pass it. |
| Eligible holder task | The [observation protocol](../research/2026-10-01-holder-cash-task-protocol.md) records zero sessions. | Missing | Founder finds one consenting eligible holder. Agent observes the same cash task in the existing venue and this app without recording identity or address in Git. |
| Working judge path | The local app runs a Venus scenario and optional BNB Chain reads; the sell side remains unquoted. [README](../../README.md) has local instructions. | Incomplete | Agent finishes the chosen task with real permitted data, failure states and source times, then repeats it in a clean session. A scenario alone is not a functional cash choice. |
| Developer Experience Report | The [field log](../dx/field-log.md) records actual local work and separates documentation issues from live API errors. No signed-call metrics or completed form receipt exist. | Incomplete | Agent organizes observed details; founder supplies first-hand account/setup ratings and submits the [DX form](https://forms.gle/EUQ39xf54GHjC2ys5) before the project form. Do not invent timings, liquidity or slippage. |
| Public evidence and video | The repository is private. No final demo video or judge-accessible URL is recorded. The [live project form audit](2026-10-01-live-form-audit.md) found its video URL field required, while the event page says optional. | Missing | After the product gate, agent prepares a video of at most four minutes and a reproducible judge path. Founder authorizes making the separate repo public; check both links while signed out and keep them accessible through judging. |
| Final project submission | No submission receipt is recorded. The [live form audit](2026-10-01-live-form-audit.md) lists ten fields and requires confirmation that the DX form was sent. | Unconfirmed | Founder checks for an existing receipt; otherwise supplies contact and prize-receiving wallet/UID privately, rechecks the form, then submits the [project form](https://forms.gle/yToDUzaDMwWnq6R6A) after DX. Save only a non-sensitive receipt status. |

## Order of work

1. Recover the credential pair and perform the read-only signed integration, recording what actually happens.
2. Observe one eligible holder's cash decision and apply the D-017 stop rule. Reassess on 4 October even if either input is still missing.
3. Complete and review the chosen product path, README and DX evidence. Build the video from the real final behavior.
4. With founder authorization, expose the separate repo and judge path. Submit DX first, then the project form before the deadline.

Keep Bell, private keys, account UID and participant details out of this repository. Agent Studio remains outside the submission unless an autonomous task with a distinct user survives the product decision.
