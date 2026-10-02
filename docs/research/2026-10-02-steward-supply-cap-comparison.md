# Same-block Steward Swipe and Venus supply-cap comparison

**Observed:** 2026-10-02, around 01:05 UTC. **Scope:** one public website interaction and read-only BNB Chain calls. This tests a concrete competing output, not adoption or trade execution.

## Public competitor output

The [Steward live dashboard](https://bnb-tokenized-stocks.vercel.app/) was opened in a clean Chrome session. In **Use → Swipe**, the input was NVDAB, 25 units and target health factor 2. After **Quote borrow**, the page showed BNB Chain block **125201341**, collateral value **$5,795.75**, “MAX SAFE BORROW” **$2,028.51** and “FUNDABLE NOW” **$2,028.51**. The visible result cited pool USDT availability and a protocol collateral factor, but no NVDAB supply-cap headroom or deposit-size warning. The [public repository](https://github.com/zkasuran/steward-bnb) describes Swipe as supplying a bStock as Venus collateral and drawing USDT. No wallet was connected and no transaction was submitted. The rest of Steward's feature set was not reassessed here.

## Same-block contract check

At that exact block, the [official BNB Chain RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/) returned `supplyCaps(vNVDAB)=1500000000000000000000`, `vNVDAB.totalSupply()=147996050485`, and `vNVDAB.exchangeRateStored()=10000000018731039135729946976`. The block timestamp was **2026-10-02 01:04:53 UTC**. The [Venus conversion](https://github.com/venusprotocol/venus-protocol-documentation/blob/main/guides/protocol-math.md) yields **20.039492377880186433 NVDAB** of available deposit space at that block. The [Core `mintAllowed` source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol) checks that a proposed new supply keeps the total at or below the cap. Supplying all 25 entered NVDAB would exceed the measured headroom. The observed Steward result did not surface that constraint.

This does not prove that borrowing **$2,028.51** is impossible with a smaller deposit, that a particular holder can borrow, or that Steward would build and execute a 25-unit deposit. Its page was a read-only quote. It is a specific gap in the displayed 25-unit scenario, not proof of a financial loss.

## Breadth and product implication

A separate [Venus market API](https://api.venus.io/markets?chainId=56&limit=100) read with `accept-version: next` at **01:05:38 UTC** showed indexed cap utilization across four Core bStock markets: NVDAB **98.66%**, SKHYB **87.91%**, SPCXB **69.78%**, and TSLAB **50.93%**. These are market snapshots, not a count of affected users. NVDAB is the sharpest observed cap case; one example cannot establish common failure frequency.

Dyplux's current scenario distinguishes nominal collateral capacity from indexed deposit headroom, so the 25-unit case is flagged. That is a measurable difference in what the two screens disclose. A working sell quote, account-wide risk and an observed holder task are still necessary before claiming a better complete cash decision. Do not turn this single competitor omission into a general attack on Steward or a demand claim.
