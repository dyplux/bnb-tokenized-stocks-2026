# Sale card clarity slice

**Prepared:** 2026-10-03 UTC. **Decision:** one bounded interface correction to the provisional D-017 task. No new API call or execution path.

## User job

A reader has entered one NVDAB amount and one USDT target. When both the Venus market scenario and a valid Binance target-sized quote exist, they need the estimated sale amount next to the borrow illustration. The current main Sell card still says “Unquoted” after the separate Sale check has returned an estimate. It is easy to miss that the two amounts relate to the same target.

## Display rules

- Change the opening headline to a task question that doesn't imply a safe choice is available. Keep a short, plain statement that sale output is before costs and the Venus result is a market scenario.
- The main Sell card starts with no current estimate and links to the Sale check.
- After a current scenario and a successful target-sized quote match the exact typed units and cash target, show the validated estimated USDT output and candidate NVDAB sale in the main Sell card. Label both as before costs. The quote's source time and route remain in the Sale check evidence below. Never call the amount net proceeds or an executable order.
- If a recent balance read for the same address and inputs shows less NVDAB than the candidate sale, the main card states that the observed balance is too low. The detailed quote remains below as a technical estimate. If no matching fresh balance exists, the main card says balance is unverified.
- Input edit, quote failure, target shortfall, stale scenario or quote expiry removes the main-card estimate. Quote-first and scenario-first orders both work. The borrow card remains a hypothetical market illustration, with no personal safety claim.

## Acceptance

1. With a fresh synthetic scenario, a target-reaching 0.43 NVDAB quote and a 1 NVDAB observed balance, the main card shows an estimated output before costs and the sale candidate beside the borrow result.
2. A fresh 0 or 0.4 NVDAB balance replaces the main-card estimate with an insufficiency state; no viable-looking sale amount remains there.
3. A missing or stale balance is disclosed without pretending ownership. A quote received before the scenario appears when the matching scenario arrives.
4. Editing inputs, request failure, below-target quote and expiry clear the main-card amount. The existing detailed Sale check keeps its own error and evidence states.
5. Browser QA at 320 and 1440 CSS pixels shows no page error or horizontal overflow. No live Binance call is required for this UI slice.

The holder, final-cost, personal Venus-risk and incumbent-comparison gates remain open.
