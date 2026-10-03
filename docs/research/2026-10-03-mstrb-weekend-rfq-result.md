# Saturday MSTRB quote roundtrip, three sizes

**Observed:** 2026-10-03 14:15:07 to 14:15:10 UTC, Saturday. **Method:** [fixed protocol](2026-10-03-mstrb-weekend-rfq-protocol.md). A fresh temporary address had zero USDT and MSTRB balance on BNB Chain 56. Six signed Binance Web3 Trading API `GET /api/v1/dex/aggregator/quote` requests returned HTTP 200 and business code 0. Each response had one LiquidMesh `SWAP` route marked `isBest=true`. No wallet signing, swap, approval or order took place.

| USDT input | Quoted MSTRB bought | Inverse USDT estimate | Indicative ratio | Buy / sell latency |
|---:|---:|---:|---:|---:|
| 25 | 0.154225813083690279 | 24.938734772286846208 | 99.754939% | 727 / 297 ms |
| 100 | 0.616481109458514946 | 99.686876790020221504 | 99.686877% | 479 / 368 ms |
| 500 | 3.081146400362247958 | 498.232401150336897888 | 99.646480% | 307 / 343 ms |

The inverse request used the raw MSTRB output of the immediately preceding buy quote. The six selected routes returned the exact requested input amounts and the expected token contracts with 18 decimals. Each response reported `estimateGasFee=450000`; the `tradeFee` fields ranged from 0.02254513 to 0.02398203. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) labels `tradeFee` an estimated network fee in USD and `estimateGasFee` an estimate in the chain's smallest unit. It doesn't make clear whether either amount has already been deducted from `toTokenAmount`. The observed gas value also hasn't been reconciled with a built transaction or actual payment. The route quote ID was deliberately stripped, so actual expiry wasn't tested.

**What this proves:** the configured Binance Web3 API returned amount-sized MSTRB/USDT buy and sell estimates on BNB Chain during this Saturday interval. The observed estimates are below the starting USDT amount by about 0.25%, 0.31% and 0.35%, respectively, before any additional execution costs. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes these fields as quotes, not completed trades.

**What remains unknown:** the nonholder address cannot establish whether an eligible user could complete either leg, what the final all-in cost would be, whether a quote would survive signing, or whether this provides an economic edge over another venue. A later inverse quote isn't a guaranteed roundtrip. No user task or holder demand was observed. This result supports weekend technical access and leaves [D-033](../decisions/decision-log.md) unchanged.

**Provenance:** public [Binance bStock identity list](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3), BNB Chain public RPC chain and `balanceOf` reads, and the [sanitized local probe](../../scripts/probe_binance_quote.py). The six sanitized outputs were retained outside Git for this session. No credential, address, quote ID, raw API response or signed header is in this report.
