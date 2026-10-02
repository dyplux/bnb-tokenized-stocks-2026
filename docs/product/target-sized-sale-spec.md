# Candidate partial sale for one cash need

**Decision:** [D-023](../decisions/decision-log.md). The existing read-only app is a provisional product. This slice corrects its cash-basis mismatch. It doesn't approve a launch or a trade.

## User task

A person considers up to a typed number of NVDAB units as Venus collateral and needs a typed USDT amount. The Sale check should request a quote for a **candidate fraction** of that amount, near the same USDT target. The borrow scenario continues to use all typed units. Both paths must say what they measured, and neither may claim executable proceeds or personal loan safety.

## Bounded quote path

1. Validate wallet, typed NVDAB units and USDT target. Verify the NVDAB identity and BNB Chain token metadata once.
2. Ask Binance for one quote using `min(typed_units, 1 NVDAB)` as a bounded probe amount. Use its integer raw output to calculate a candidate sale amount by ceiling division: `candidate_raw = ceil(probe_raw * target_raw / probe_output_raw)`. Clamp the candidate to the entered NVDAB units. If the first quote already uses all entered units and is below target, stop with a visible shortfall. If the candidate equals the probe amount, use that fresh quote without another call.
3. Otherwise request one more quote for that candidate amount. The second response is the displayed candidate result, even if it misses the target. No third quote or retry loop runs automatically. Each quote has its own capture time and route mode. A failed or malformed second quote must not silently reuse the first result as a target-sized quote.
4. Show candidate NVDAB input, estimated USDT output, target relation before costs and the source times. Show that the typed holding is a scenario input, not a verified wallet balance. The main Sale card remains Unquoted for net proceeds.

The quote endpoint is input-sized per the [official Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api). One 0.43 NVDAB technical read near a 100 USDT target is documented in the [dated probe](../research/2026-10-02-fractional-target-quote.md). It is not a stable conversion rate.

## Acceptance

1. One identity search and at most two Trading API quote calls per click, with no transaction build, approval, signature or broadcast.
2. All candidate calculations use integer raw units and cap the sale amount at the typed NVDAB amount. Invalid, zero, missing, mismatched or out-of-range route output fails closed.
3. For a synthetic 1 NVDAB / 100 USDT case, a 234 USDT full-unit probe leads to a roughly 0.42735 NVDAB second quote; the borrow illustration still uses 1 NVDAB.
4. If a full-holding quote is below target, report the shortage before costs. If the target-sized quote is below target, report that shortage and permit an explicit fresh retry. Never infer net proceeds or give a sell recommendation.
5. No-route, API error, stale response, amount mismatch and identity failure produce distinct visible states. The existing quote invalidation when cash or units change still works.
6. The README and DX log explain the extra signed call count and quote validity. Browser checks cover a target-sized success, shortfall, second-call failure and a target edit during a pending response.
