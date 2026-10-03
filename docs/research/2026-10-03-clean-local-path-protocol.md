# Clean local read-only path protocol

**Prepared:** 2026-10-03 UTC, before the browser run. **State:** one bounded run completed at 00:19 UTC. See the [separate result](2026-10-03-clean-local-path-result.md); this protocol retains the method defined before the run.

## Question

Can a clean local browser complete the current NVDAB 1-unit, 100-USDT cash scenario using live Venus and BNB Chain reads plus the signed Binance Web3 target-sized quote path, after the quote-age change?

## Fixed method

Run the documented local server once and open the page in a clean Chromium context at 375 CSS pixels. Generate a new temporary address for this technical check. Enter 1 NVDAB and a 100 USDT target. Request the Venus scenario, optional balance, Core account state and one partial-sale estimate in that order. The quote action may make one signed RWA search and at most two signed Trading API quote GETs. Do not make a transaction build, approval, simulation, signature, broadcast or trade. Don't repeat a failed quote solely to obtain a better result.

Record UTC time, visible states, source times and BNB blocks, whether the same-cash line or insufficiency warning appears, and any page error or horizontal overflow. Keep the address, credentials, signed headers, `quoteId`, raw responses and screenshots with wallet data out of Git. Record Binance call count as observed; the public Venus and RPC reads are separate.

## Interpretation

A zero or unknown temporary balance is expected to prevent a holder claim. A successful technical quote and working browser path don't establish an eligible holder task, execution, net proceeds, personal post-deposit safety, incumbent advantage or user demand. A failure is a dated DX observation with its error state, not an excuse to fabricate a demo.
