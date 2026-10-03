# Exit Check: local live browser observation

**Observed:** 2026-10-03 21:56 to 21:57 UTC. **Scope:** read-only local app check on BNB Chain with a zero-balance demo address. The address, signed headers, credentials, quote IDs and raw provider payloads were not retained in this record. No approval, simulation, transaction, fill or paid fee occurred.

## What the app actually returned

| Run | Input | Entry estimate | Immediate inverse estimate | Metadata block | Result |
|---|---:|---:|---:|---:|---|
| HTTP POST to local `/api/entry-check`, 21:56 UTC | 5 USDC | 0.021265135976590076 NVDAB | 4.999141361542456679 USDC | 125560056 | `BOTH_ROUTES_QUOTED` |
| Chrome interaction with the current page, 21:57 UTC | 5 USDC | 0.021266896156929527 NVDAB | 4.999747069061797768 USDC | 125560256 | “Both routes quoted” |
| Continuous Chrome video capture, 22:05 UTC | 5 USDC | 0.021265631210341636 NVDAB | 5.001168101976778857 USDC | 125561266 | `BOTH_ROUTES_QUOTED` |

The first run's entry quote was received at 21:56:14.354 UTC in 312.937 ms; the inverse was received at 21:56:14.747 UTC in 392.236 ms. Their displayed network-fee estimates were USD 0.01874094 and USD 0.01881643. The second run's entry and inverse quotes were displayed at 21:57:44 and 21:57:45 UTC. Its displayed network-fee estimates were USD 0.01884053 and USD 0.01845249. Both runs displayed LiquidMesh `SWAP` routes. The Chrome screen labelled the inverse output as an estimate before unverified costs. These are two independent, expiring quote pairs. The second isn't the realized outcome of the first.

The page loaded in system Chrome at 1440 and 375 CSS pixels. The request completed in the UI, with no page errors or horizontal overflow in either viewport. The packaged Playwright Chromium binary was missing, so the first browser launch failed before an app request; using installed system Chrome resolved the local QA setup issue. Private screenshots live outside Git under a private SSD capture directory; the address was masked before capture. A later continuous 10.64-second system Chrome capture is under the founder's private SSD video-source directory, together with its sanitized [record](../submission/video-record.json). Its entry and inverse quotes were captured at 22:05:19.040 and 22:05:19.358 UTC, with displayed network-fee estimates of USD 0.01891553 and USD 0.01963035. The browser reported zero page errors. Inspect these files before any external use.

**Method and limits:** each run used the app's exact RWA identity check, same-block token metadata and two signed Binance Web3 quotes. Three runs account for nine signed read-only calls. Individual upstream responses for app-path calls weren't retained. A successful route estimate doesn't establish geographic eligibility, executable exit, future price, complete costs or profit. The 20-second on-screen validity window isn't an exchange guarantee. The final inverse estimate exceeded the initial 5 USDC in that one recorded pair; it doesn't establish a profit because no trade or settled amount exists.
