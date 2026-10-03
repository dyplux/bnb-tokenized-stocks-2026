# Pre-entry exit check: first vertical slice

**Approved for read-only build:** 2026-10-03 under [D-048](../decisions/decision-log.md). **User:** a self-custodial BNB Chain wallet holder considering a small NVDAB spot purchase with USDC. **Trigger:** before signing a swap, especially outside regular US equity hours. **Task:** see the current buy estimate and a separate, size-matched inverse sell estimate for the same token and address.

## One screen

Input: USDC amount and public wallet address. Fixed first asset: verified NVDAB on BNB Chain mainnet. A 5 USDC amount is the default, not a minimum or recommendation. Submit explicitly. Show two steps in reading order: `USDC -> NVDAB` and `quoted NVDAB -> USDC`. Show contract identity, the local receipt time of both quotes, estimated outputs and each vendor's reported network fee. Show a plain state: `BOTH ROUTES QUOTED`, `ENTRY UNAVAILABLE`, `EXIT UNAVAILABLE`, or `CHECK INCOMPLETE`. Show exact missing items: wallet eligibility, approval cost, slippage minimum, gas payment, fill and future exit price. Expire the visible result after 20 seconds from request start.

The inverse quote is a **hypothetical immediate quote** before any buy. It does not prove that a later sell will be possible or profitable. Don't calculate or name a tradeable spread. The product never decides to buy, signs a transaction, checks a legal declaration or claims that the issuer permits the user.

## Data path and states

1. Validate 0x public address and a positive USDC amount with at most 18 decimals. Hard cap the first slice at 100 USDC to contain API use and misleading large-size extrapolation.
2. Resolve the pinned NVDA bStock identity via signed Binance Web3 RWA search, reject missing/ambiguous contract, symbol or chain. Check the token contracts and decimals on BNB Chain at a recorded block.
3. Request a signed Binance Web3 Trading quote for that exact USDC amount to NVDAB. Validate chain, token addresses, decimals, input amount and positive output. Treat any error or malformed route as `ENTRY UNAVAILABLE` or `CHECK INCOMPLETE`, with the reason.
4. Quote the estimated NVDAB output back to USDC with the same wallet. Validate identically. A missing route becomes `EXIT UNAVAILABLE`; network, identity or malformed data becomes `CHECK INCOMPLETE`.
5. Return only a small sanitized response. No quote ID, raw signed headers, API secret, wallet address, raw vendor response, transaction payload or persistent quote storage.

Use the existing signed GET helper, request budget, identity validator and 18-decimal arithmetic. Avoid a new dependency. The old Venus scenario remains accessible under a clearly labeled research route while the main page presents only this user task.

## Acceptance criteria

1. The main page asks for amount and address, and shows the exact issuer, contract and BNB Chain before the request.
2. Both valid quotes produce the two estimated amounts and timestamps in one compact view, with cost fields labelled as estimates or unknown.
3. No buy route and no inverse sell route produce different, understandable outcomes. Malformed or unavailable provider responses never look like a successful quote.
4. Changing either input clears the prior outcome, and the result expires within 20 seconds of request start.
5. The API remains read-only, rate-limited, server-side authenticated and local-only until deployment security is reviewed.
6. The README gives a clean-start command and distinguishes this flow from the archived Venus research panel. The DX log records real calls and errors without secrets.

## Out of scope now

Wallet connection, approval, transaction simulation, trade execution, cross-issuer ranking, Agent Studio, alerts, PnL, profit forecasts and a public subdomain. A funded mainnet demonstration needs a separate access and transaction review. These limits don't delay building the read-only path.

**Main measure:** whether the screen gives a distinct, usable answer for the same size and moment where a plain buy quote cannot. If the answer is just a longer quote card, D-048 should be retired.
