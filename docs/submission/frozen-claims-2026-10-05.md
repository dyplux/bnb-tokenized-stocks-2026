# Submission claim set, frozen after Monday scoring

**Frozen:** 2026-10-05, after the US regular session close. See the [Monday findings](../../experiments/EXP-RWA-004/monday-findings.md) and the [judge packet](final-review-packet.md).

## Claims supported by observed evidence

- Dyplux reviews one proposed BNB Chain tokenized-equity action before signing. Its deterministic policy returns `ALLOW`, `DENY` or `NEED_HUMAN` with reason codes and a dated receipt.
- A signed route was available for a dated NVDAB read-only review, while issuer stock-reference time, holder eligibility and funded simulation remained unverified. The observed outcome was `NEED_HUMAN`.
- A separate read-only 100 USDT request under a 20 USDT mandate returned a route and was denied with `MANDATE_LIMIT_EXCEEDED`.
- The Sunday-to-Monday benchmark covered NVDA, TSLA and COIN, with two provider representations each. Sunday direction matched the 5 October open for two of three independent tickers; TSLA did not. The six-row median absolute residual was 0.7301%. Classification: `H-RWA-OFFHOURS = SAFETY_ONLY`.
- The public page is a dated evidence packet. A reviewer can run a fresh local read-only review with their own Binance Web3 API credentials.

## Claims outside the evidence

No predictive next-open edge, risk-adjusted return, executable arbitrage, independent issuer stock-reference age, verified buyer eligibility, passing funded simulation, real `ALLOW`, signed capital transaction, broadcast or fill. The green `ALLOW` example is a labelled synthetic policy fixture. The Monday daily open is an external historical bar, not a trade fill or an issuer-reference timestamp.

Only change this claim set for a new dated, verified product or source observation. Keep the frozen experiment artefacts intact.
