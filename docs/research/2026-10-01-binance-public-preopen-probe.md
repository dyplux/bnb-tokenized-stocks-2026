# Binance public pre-open probe

**Observed:** 2026-10-01 11:33 to 11:40 UTC, 07:33 to 07:40 New York time
**Purpose:** identify candidate bStock contracts and check whether one quoted price represents an executable amount
**Auth:** none; no Binance Web3 developer key used
**Scope:** two different public surfaces. Do not compare their prices across the seven-minute gap or treat either as a BNB Chain RFQ.

## Public bStock identification

A read-only GET to the Binance website's public [bStock list endpoint](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3) returned HTTP 200, business code `000000`, and 87 rows at the 11:33 UTC request. Three rows had `chainId=56`:

| Ticker | Symbol | Contract | Multiplier in response |
|---|---|---|---:|
| NVDA | NVDAB | `0x02fca66c1d1afb4e2a7884261eb00f63598a7436` | `1.000778223752807865` |
| AAPL | AAPLB | `0x431a3bee82e2ca41e49895cbece5bb0f76a89b7a` | `1.000603906075632366` |
| TSLA | TSLAB | `0x5b1910eaad6450e50f816082aa078c41f10c292f` | `1.000000000000000000` |

The website endpoint is on a Binance domain, but it is distinct from the signed Binance Web3 developer API required by the hackathon. These contracts are candidates to check against the issuer and the signed RWA Data API before allowing a user action. The list response does not establish that any route will execute.

At 11:33:22 UTC, the public [dynamic endpoint for NVDAB](https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai?chainId=56&contractAddress=0x02fca66c1d1afb4e2a7884261eb00f63598a7436) and [TSLAB](https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai?chainId=56&contractAddress=0x5b1910eaad6450e50f816082aa078c41f10c292f) returned `statusInfo.openState=true` and `reasonCode=TRADING`. `stockInfo.price` and `statusInfo.marketStatus` were null in both responses. `tokenInfo.price` was 230.38915489013389860165 for NVDAB and 356.12 for TSLAB. Those token prices are informational fields; the response contains no amount-specific RFQ or independent cash-equity price. Null reference data is absent, not zero.

## Separate Binance Spot order-book snapshot

The [public Binance Spot market-data base URL](https://developers.binance.com/en/docs/products/spot/rest-api) permits keyless market reads. At 11:40:29 and 11:40:30 UTC, `GET /api/v3/depth?symbol=<pair>&limit=20` returned these CEX Spot books:

| Pair | UTC | Best bid × quantity | Best ask × quantity | Book update ID |
|---|---|---:|---:|---:|
| NVDAB/USDT | 11:40:29 | 230.11 × 14.806 | 230.12 × 15.119 | 126235407 |
| TSLAB/USDT | 11:40:30 | 356.40 × 0.083 | 356.41 × 0.520 | 142431137 |

A local Decimal calculation bought the quantity obtainable for 100 USDT at the asks and then valued an immediate sale of that same quantity at the bids in the **same static book**. For NVDAB it gave 0.43455588 tokens, a 230.1200 weighted buy price and 99.9957 USDT of hypothetical sale proceeds, a 0.0043 USDT book-only round-trip difference. For TSLAB it gave 0.28057574 tokens, a 356.4100 weighted buy price and 99.9867 USDT of hypothetical sale proceeds, a 0.0133 USDT difference. Both 100 USDT asks were fully covered within the 20 levels read.

This calculation excludes fees, changes during execution, account eligibility, transfers, funding, slippage beyond the snapshot and all BNB Chain RFQ costs. It is not a completed trade, not a profit backtest and not proof that the Web3 API can fill the order. The first TSLAB top ask read at 11:39:47 had only 0.028 tokens; at 11:40:30 it had 0.520. This single minute shows why a standing top-of-book quantity cannot be reused as a later quote.

## What changes next

1. Use the candidate contracts to request signed Binance Web3 RWA details when complete local credentials are available. Record field whitelist, status, timestamp, errors and latency.
2. Capture Web3 RFQs for the **same wallet, asset and amount** in a closed US cash session. Observe quote availability, output quantity, quote expiry and fees; do not use the separate CEX book as the execution proof.
3. Recheck weekend conditions rather than extrapolating Thursday pre-open liquidity. The user's economic edge requires a real alternative and net cost comparison.

**Developer Experience note:** the public BAPI and Spot requests succeeded with no account key. The signed Binance Web3 developer integration remains untested because the local key and secret fields are empty. That is a credential prerequisite, not an API error.
