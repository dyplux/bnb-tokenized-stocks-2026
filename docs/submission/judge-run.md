# Judge walkthrough: Exit Check

**Historical draft:** Exit Check was retired. Use the [current Execution Safety judge guide](safety-judge-run.md). The instructions below record the earlier prototype and aren't the current submission path.

## Task and setup

The task is to inspect a possible small NVDAB purchase before signing it. The user enters the USDC size and a public BNB Chain address. Exit Check asks Binance Web3 for an entry quote, then asks for an immediate inverse quote on the estimated NVDAB output. The two directions are separate observations. A successful inverse quote doesn't guarantee a later exit or net proceeds.

Run from this repository's root with Python 3.9 or newer:

```sh
python3 app/server.py
```

Open `http://127.0.0.1:8000`. Set `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` in the process environment or in a local `.env` file that Git ignores. Use your own valid Web3 API credentials. The app has no third-party Python package dependency and sends signed API requests from the local server. It never asks for a wallet private key, signature or approval.

## One-minute path

1. Keep the default `5` USDC amount. Enter a public `0x` BNB Chain address. A zero-balance address may receive quotes; this is a read-only route check, not proof of a tradeable position.
2. Select **Check both routes**. The server verifies the pinned NVDA bStock identity and NVDAB and USDC contracts at one BNB Chain block. It then requests the entry quote and its immediate inverse for the same estimated token quantity.
3. Read the result. **Both routes quoted** gives two estimated outputs, the route vendors, request times and any provider-reported network-fee estimates. **Entry route unavailable** and **Exit route unavailable** are distinct. **Check incomplete** means identity, contract metadata or the provider response failed verification.
4. Change the amount or address to clear the result. Any visible result expires 20 seconds after its request began. A new click makes new signed calls; the local server accepts at most six quote checks per rolling minute and one at a time.

## Evidence and limits

The [3 October current-build observation](../research/2026-10-03-exit-check-live-browser.md) records three 5 USDC entry and inverse checks from the local app, including a continuous browser capture with a sanitized [record](video-record.json). Those checks verify the local read-only path on that date. They don't validate a later sell, issuer eligibility or paid costs. The [DX field log](../dx/field-log.md) records actual API experiences and missing observations. The [spec](../product/pre-entry-exit-spec.md) explains each state and deliberate exclusions.

The initial screen doesn't connect a wallet or execute a swap. Approval cost, gas payment, slippage minimum, actual fill and future exit availability are unknown. The archived Venus research panel is at `/venus-scenario` and isn't part of this entry task. The app binds to localhost until a separate deployment review and authorization.
