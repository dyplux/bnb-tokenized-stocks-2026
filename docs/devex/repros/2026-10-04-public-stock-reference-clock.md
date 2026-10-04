# Public stock price has no independent clock in two observed payloads

**Observed:** 2026-10-04 12:17:49 UTC, from retained response fixture file times. **Surface:** Binance public website BAPI, separate from the signed Binance Web3 developer API. Read-only GET to `/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai?chainId=56&contractAddress=<public token contract>`. Two sanitized call records were appended to [the DevEx log](../raw/2026-10-04.jsonl); latency wasn't measured.

| Contract | Raw response fixture | SHA-256 of response bytes | Observed price fields |
|---|---|---|---|
| AAPLon `0x390a684ef9cade28a7ad0dfa61ab1eb3842618c4` | [`AAPLon`](../fixtures/2026-10-04-public-dynamic-aaplon.json) | `92f53d8be4b17608ef1e468fda267976be401bbdf736647c768d85e12fd6a071` | `tokenInfo.price=334.530599865358401842`, `sharesMultiplier=1.003376073740221058`, `stockInfo.price=333.405` |
| NVDAB `0x02fca66c1d1afb4e2a7884261eb00f63598a7436` | [`NVDAB`](../fixtures/2026-10-04-public-dynamic-nvdab.json) | `18c3c79d84a8a4b9d02df8c2ab53c7105f4aa4707e4d1384820ca2671d3cdf52` | `tokenInfo.price=234.79257907464625320765`, `sharesMultiplier=1.000778223752807865`, `stockInfo.price=null` |

For AAPLon, `tokenInfo.price / sharesMultiplier = 333.4049999999999999995`, equal to the displayed `stockInfo.price` at its precision. This arithmetic doesn't prove which upstream feed determined the token price. Neither observed response includes a timestamp for `stockInfo.price`, an independent underlying reference update, or a reference age. The signed [RWA price documentation](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) separately defines its `referencePrice` as derived from token price and its `tokenPriceUpdatedAt` as the token's update time. Don't transfer an update clock between these two API surfaces.

The AAPLon payload also reports `marketStatus=offhours`, `nextOpenTime=1791158700000` (2026-10-05 00:05 UTC) and `nextCloseTime=1791158100000` (2026-10-04 23:55 UTC). The named close precedes the named open by ten minutes. Without public documentation for this BAPI field's semantics, record it as an ordering ambiguity, not a proven scheduling error. A consumer mustn't derive the US equity market session from these two fields alone.

**Suggested developer-doc change:** expose and define an independent underlying price timestamp and source if the price is meant to represent a traditional-equity reference. If `stockInfo.price` is calculated from token price or inherits its oracle's time, state that explicitly. Define what `nextOpenTime` and `nextCloseTime` mean during `offhours`, including whether they refer to separate venues or sessions.
