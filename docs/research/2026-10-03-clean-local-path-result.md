# Clean local read-only path result

**Observed:** 2026-10-03 00:19:43 to 00:19:53 UTC. **Method:** one clean Chromium context at 375 CSS pixels, following the [predefined protocol](2026-10-03-clean-local-path-protocol.md). The local server served the unmodified application. A new temporary address was generated for the run and is omitted here. There was no wallet signer or known holder position.

| Browser step | Visible result | Limit |
|---|---|---|
| 1 NVDAB, 100 USDT Venus scenario | HTTP 200; indexed snapshot retrieved at 00:19:44 UTC; 1 NVDAB was within recorded Core supply-cap headroom at BNB block 125387245; isolated collateral-only minimum appeared as about 0.7107 NVDAB | Market scenario and fixed-block cap check, not a personal deposit or loan approval |
| Optional NVDAB balance | HTTP 200; 0 NVDAB at BNB block 125387250 | The temporary address cannot support the candidate sale; it doesn't represent a consenting holder |
| Optional Core account state | HTTP 200; no entered Core markets, default pool, zero borrowing-power and liquidation-threshold states at block 125387253 | Empty/default account path only, no populated risk position or post-action forecast |
| One target-sized Binance action | Local `POST /api/quote` HTTP 200; candidate sale `0.426220421663874222 NVDAB`; UI rounded output to about `100.00 USDT` before costs; estimated network fee displayed as `0.01902543 USD` | The exact raw output and individual Binance response times weren't retained in this browser log; no sale executed |

The page showed the candidate sale beside the isolated Venus minimum for the same 100 USDT target. It also said the candidate sale exceeded the observed zero balance and withheld a conditional remainder. No horizontal overflow or page error occurred at 375 CSS pixels. The live browser made one request to each local endpoint: `/api/scenario`, `/api/balance`, `/api/venus-account` and `/api/quote`; all returned HTTP 200. No endpoint was retried. The request-start age rule did not expire the quote during this short run.

The target-sized server path calls one signed RWA identity search, then one 1 NVDAB probe and, because the displayed candidate differs from 1 NVDAB, one candidate quote. **Three signed Binance Web3 GETs are inferred from that inspected code branch and the visible outcome**. They weren't instrumented separately in this browser run, so individual upstream HTTP statuses, business codes, route mode, exact output and latencies shouldn't be backfilled from the local HTTP 200. The browser script also read collapsed evidence fields with `inner_text`, which returned blanks; that is a local capture gap, not a Binance omission. The earlier live quote observations establish that LiquidMesh SWAP has appeared on this pair, not that this run used the same route.

There was no approval, unsigned transaction build, simulation, signature, broadcast, fill or incurred network fee. This run proves the local read-only path can display coherent live inputs and a safe zero-balance warning. It doesn't pass the D-017 holder, net-proceeds, personal Venus-risk or incumbent-comparison gates.
