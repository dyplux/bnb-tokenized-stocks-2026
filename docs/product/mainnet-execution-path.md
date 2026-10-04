# BSC tiny-capital execution path

**State, 2026-10-04:** prepared protocol, **not approved or executed**. The current product screen is read-only. It neither accepts a wallet nor builds, signs or broadcasts a transaction. A live `NEED_HUMAN` decision cannot advance to signing.

## Intended single-action sequence

1. **Intent.** The user names the exact BSC contract, side, funding token, amount and a maximum spend/impact. The app checks chain 56 and canonical security. Invalid or missing fields stop before any API call.
2. **Policy.** Fetch fresh signed Binance RWA data, a fixed-block bStock multiplier where applicable, an amount-specific route and independent stock-reference time if a permitted source supplies it. Distinguish the token clock from the stock clock. An unverified holder or jurisdiction, unknown market state, pending multiplier, missing route or stale source cannot silently pass.
3. **Quote.** Request a route for the *same* wallet, contract, side and amount that would later execute. Record route mode, vendor, quote expiry, minimum received, fees and raw response hash. A quote from the temporary research wallet is not reusable here.
4. **Build.** Use the Binance Web3 unsigned transaction builder for the chosen route. Compare returned chain, token addresses, router, spender, amounts and calldata target with the approved intent. Never let an agent silently substitute a route or increase an allowance.
5. **Simulate.** Simulate the exact unsigned transaction from the funded intended wallet. Capture success/failure, balance, allowance and gas estimate. The research simulation from an unfunded wallet predicted `FAILED`; it cannot count as this gate.
6. **Human approval.** Present the exact transaction summary and maximum possible cost. The founder must explicitly approve this specific broadcast after viewing the policy receipt and simulation. A prior instruction to prepare this path is not approval to spend.
7. **Bounded signer.** Only after approval, use a separate signer process with chain 56, one wallet, allowlisted USDT and stock contract, allowlisted router/spender, a tiny explicit notional ceiling, finite deadline, limited allowance, gas ceiling and nonce check. The signer rechecks all bounds against the unsigned payload. No private key is sent to the browser, model, DevEx log or repository.
8. **Broadcast and verify.** Submit once, wait for the receipt, confirm transaction status and actual token balance changes at the approved wallet. Record the transaction hash and pre/post balances with timestamps. A reverted transaction is a failed attempt, not a fill. Reconcile actual spend, gas, tokens received and effective price with the estimate.

## Current gates

| Gate | State | Evidence needed |
|---|---|---|
| Exact security and amount | Working read-only | Live catalog and local input validation |
| Quote for temporary unfunded wallet | Working read-only | Signed API response, not investor access |
| Eligible intended holder | Unknown | Issuer access decision for the actual person and wallet. For Ondo, resolve the [conflicting general and asset-level EEA descriptions](../research/2026-10-04-issuer-access-gate.md) using current NVDAon final terms, KID and venue terms. |
| Independent stock reference clock | Unknown | Permitted source with explicit venue and as-of time, or a formally different mandate |
| Exact-wallet build and funded simulation | Unrun | Same-wallet route, unsigned build, successful simulation |
| Human approval | Pending | Approval of one bounded transaction |
| Bounded signer and pre/post proof | Unbuilt | Reviewable code and one approved tiny-capital execution |

The first funded amount should be the smallest permitted by a real route and within the founder's approximately €10 test budget. A successful quote alone doesn't establish that minimum. No purchase is needed for the Sunday research collector or Monday experiment.
