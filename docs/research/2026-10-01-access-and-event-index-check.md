# Access and event-index check

**Checked:** 2026-10-01 UTC
**Question:** Does a small eligible holder gain a distinct cash or weekend action from the dividend idea, and can its historical multiplier be recovered without a paid indexer?

## Primary-source facts

- [Ondo Stocks](https://ondo.finance/ondo-stocks), checked 2026-10-01, says its secondary tokens can trade 24/7 where venues operate. Direct mint and redemption normally run 24/5. Six assets, NVDAon, SPYon, CRCLon, TSLAon, QQQon and GOOGLon, have 24/7 direct mint and redemption, subject to halts and eligibility. Direct access requires onboarding and KYC. Holding a token doesn't confer direct redemption eligibility.
- The [xStocks FAQ](https://docs.xstocks.fi/docs/frequently-asked-questions), checked 2026-10-01, says the issuer sets no minimum for secondary trading, while direct issuance or redemption has a $5,000 minimum and KYC. This is an access distinction, not evidence that a given BNB Chain venue has an executable quote.
- [ProShares' SQQQ page](https://www.proshares.com/our-etfs/leveraged-and-inverse/sqqq), checked 2026-10-01, defines a daily -3x Nasdaq-100 objective and warns that longer holding periods can diverge from that objective. The public SQQQB multiplier from the [dividend cash-flow check](2026-10-01-dividend-cash-choice.md) therefore can't make it a representative long-hold income example.
- The [BNBScan developer page](https://bnbscan.com/developer), checked 2026-10-01, advertises a transaction query API. It is an independent explorer, not BscScan or an official BNB Chain service. Its stated anonymous rate limit differs between its developer and API documentation; the lower stated limit is the safe assumption for this experiment.

## Bounded public indexer attempt

On 2026-10-01, a read-only BNB RPC `eth_getBlockByNumber` timestamp search put UTC midnight on 2026-09-23 at block **123465319** and UTC midnight on 2026-09-24 at **123657250**. These are search boundaries, not event results. A BNBScan query for SQQQB around that interval returned zero rows. Pagination of its recent contract transactions returned 100 rows at offset 100 and 41 at offset 300, all on 2026-09-29 or 30; offset 500 returned zero. Those responses don't establish complete historical coverage. The public RPC's broad `eth_getLogs` and historical `eth_call` errors are documented in [status](../status.md).

No `UIMultiplierUpdated` event was recovered. The [prepared Dune query](queries/bstock-multiplier-events.sql) remains unrun and is the next source for that exact question. No Binance Web3 signed quote or wallet history was requested here.

## Product implication and falsifier

**Inference:** 24/7 access alone has weak differentiation, since Ondo already exposes six direct 24/7 assets and multiple secondary venues. A small holder's dividend cash-out looks economically thin in the QQQB illustration, while the larger SQQQB multiplier belongs to a daily inverse leveraged fund. This doesn't rule out other assets or amounts. It does mean this candidate has no defensible ordinary-user hero case yet.

**Unknown:** previous multiplier, event type and timestamp, a real holder's pre-event balance, an eligible wallet's executable sale and all-in costs, and whether the holder wants this action. A verified event, wallet-specific gain large enough to clear costs and a same-task gap against an existing wallet would reopen the candidate. Until then, keep Agent Studio out: its paid event service has no identified buyer.
