# Provisional safety core: one action review

**Decision:** founder promoted `H-RWA-SAFETY` to `PRODUCT_CORE_PROVISIONAL` on 4 October 2026. [Evidence report](../research/2026-10-04-safety-evidence.md). This replaces the retired sell-or-borrow and Exit Check proposals as the active build slice. `H-RWA-OFFHOURS` remains an independent Monday experiment.

## User, trigger and job

A BNB Chain stock-token buyer or the developer of a trading agent has selected one NVDA representation and a USDT amount. Before signing, they need to know which evidence supports that exact action, what remains unknown, and whether their stated mandate blocks it. The first screen is a **read-only pre-trade review** for NVDA on BSC mainnet, with bStock or Ondo as the representation. The existing workaround is a wallet quote, issuer terms and separate on-chain checks. No independent user preference has yet been observed.

## Single-screen flow

1. Choose NVDAB or NVDAon, enter 10 to 1,000 USDT, and set a maximum permitted notional and price impact. The screen names the exact contract and explains that no wallet connection or order occurs.
2. On one explicit click, the server retrieves a signed Binance RWA catalog and token price, a size-specific read-only USDT buy quote, and, for NVDAB, a fixed-block on-chain UI multiplier. Every source, capture time and failure is retained without keys or signature headers. A failed source becomes `UNKNOWN`, never a fabricated pass.
3. The deterministic policy evaluates canonical ticker and exact contract, market status, token-price clock, independent stock-reference clock, current multiplier and pending change, issuer and user eligibility, quote, price impact, simulation and mandate. It returns `ALLOW`, `DENY` or `NEED_HUMAN`, reason codes and a hashed decision receipt. A public anonymous check normally needs human review because user eligibility and wallet simulation aren't verified. `ALLOW` means the supplied evidence passed this policy, not that a trade succeeded.
4. The screen groups the output into **decision**, **why**, **evidence**, and **what to do next**. It exposes unknowns and the receipt JSON. It has no dashboard, ranking, profit prediction, wallet signing or transaction button.

## Evidence boundaries and recovery

`tokenPriceUpdatedAt` dates the token price only. Until an independently sourced stock-reference timestamp exists, `reference_price_updated_at=null`, `reference_age_seconds=null`, `reference_age_status=UNKNOWN`. The UI may show a reported `referencePrice` but cannot call it independently fresh. Unknown enum values, including the observed undocumented `offhours`, cannot default to open. A quote does not verify jurisdiction or issuer eligibility. A response with `executionMode=SWAP` is displayed as observed; RFQ semantics are not assumed. A missing or nonmatching multiplier, missing route, stale price, API error or simulation gap gets its own explicit reason and retry or verification step.

## Acceptance criteria

1. A clean local judge session selects one NVDA representation and amount, runs one check and sees the exact contract, source time, route mode and receipt without founder guidance.
2. The screen uses real signed Binance Web3 reads and live BSC reads. It neither broadcasts nor asks for a private key. Its server limits input size and rate.
3. The policy never treats `offhours`, an undocumented market status, a missing stock-reference timestamp, a successful quote, or an unfunded simulation as proof of execution safety.
4. NVDAB's live multiplier is pinned to a BSC block and compared with the same check's signed catalog ratio. A mismatch denies; unavailable or scheduled state needs human review.
5. A notional above the user's bound denies even if the API returns a quote. Missing API/RPC data produces a visible error or `NEED_HUMAN`, never a success-looking blank.
6. Receipt reason codes and evidence hashes can be reproduced from the recorded response fixtures. The README names the exact local command and limitations.

**Primary measure:** whether a reviewer can correctly identify one blocking fact and the next verification action from the screen in under two minutes. This is a usability target, not measured adoption. **Demo sentence:** “Ask to buy one NVDA token representation; get the exact facts that permit, block or defer the action before signing.”
