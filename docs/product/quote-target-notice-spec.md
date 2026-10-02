# Quote estimate against the cash target

**Decision context:** D-017 asks for the same USDT cash need on both paths. The local Sale check currently shows an estimated quote output but leaves the user to compare it mentally with the cash target. Changing the target doesn't clear the old quote. The sale remains unquoted as net proceeds; this slice only makes the indicative comparison honest and removes stale state.

## User task and view

After entering NVDAB units, a USDT target and a public address, the user requests one read-only Binance quote. For each validated route, the Sale check shows whether its **estimated** USDT output is below, exactly at, or above the entered target **before execution costs**. The output amount, route mode, response time and 20-second expiry remain visible. The main sale card stays Unquoted.

## Acceptance

1. The quote action refuses an invalid, zero, over-precise or out-of-range cash target before calling `/api/quote`, with an inline cash-field error. Use the server's 18-decimal and 1e15-USDT bounds.
2. Compare the integer raw `toTokenAmount` against the entered target converted to 18-decimal base units. Do not use floating-point rounding to decide above or below.
3. The per-route text says **estimated output** relative to the target **before costs**. It must never say proceeds, profit, feasible trade or recommendation.
4. Editing the cash target hides the old quote, invalidates a pending response and prevents the 20-second expiry timer from changing a newer result.
5. Failure, no route and expiry leave no active target verdict. The existing identity, token, amount and freshness gates remain in place.
6. Local scripted browser checks cover below target, above target, cash edit during a pending quote and invalid target. No live Binance call or holder wallet is needed for this UI slice.

Only `app/index.html` should need code changes. Keep no new dependency or production deploy. README copy should be corrected after review to say an **estimated output** may appear, never confirmed proceeds.

## Local review on 2026-10-02

The change uses integer raw units for the target verdict and leaves the main sale card Unquoted. Scripted Chrome runs at 320 and 1440 CSS pixels used intercepted synthetic quote responses, with no Binance request. At both widths, a 50 USDT estimate appeared below a 100 USDT target, above a 25 USDT target and exactly at a 50 USDT target. Changing the target hid the previous quote. A zero target blocked the quote request, showed the cash-field error and focused that field. Editing the target during a pending response discarded that response. A controlled browser clock confirmed that the old expiry timer left a newer quote alone, then the newer quote lost its verdict and estimate at 20 seconds. Neither viewport overflowed.

The inline JavaScript parsed with Node. All 26 local Python tests passed. These are UI and local-code checks using invented responses; they do not prove a holder sale, final costs or that the product changes a user's decision. The first real signed quote and separate unsigned SWAP build are documented in the dated research files.
