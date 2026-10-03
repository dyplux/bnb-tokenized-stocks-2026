# bStock collateral-cap screen

**Observed:** BNB Smart Chain block `125250140`, `2026-10-02 07:11:07 UTC`. **Question:** can the current NVDAB sell-or-borrow example plausibly onboard many new Venus borrowers while its Core supply cap is nearly full?

The [Venus public markets API](https://api.venus.io/markets?chainId=56&limit=100), requested with `accept-version: next`, identified the four Core bStock vToken addresses. At one block on the [BNB Chain public RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/), read `Core.supplyCaps(vToken)`, `vToken.totalSupply()` and `vToken.exchangeRateStored()`. All four underlying tokens were listed by the API with 18 decimals. For each row, supplied underlying base units are `floor(totalSupply × exchangeRateStored / 10^18)` and headroom is `cap − supplied`. This is the [Venus cap-check method](2026-10-02-venus-supply-cap-headroom.md), not a transaction simulation.

| Core market | vToken address | Cap, underlying units | Headroom, underlying units | Cap remaining |
|---|---|---:|---:|---:|
| vNVDAB | `0xEb8Ca841cBe1BC4832A10b15c7dAB1081eDaD371` | 1,500 | 11.416397078470495107 | 0.7611% |
| vSKHYB | `0x3E281461efb3D53EC20DB207674373Ed8Ef3BbA9` | 375 | 45.337526763415091317 | 12.0900% |
| vSPCXB | `0xC36dFaCc7a125859C106F29b9F2d874CCF29A55A` | 2,000 | 604.409747038441480668 | 30.2205% |
| vTSLAB | `0x97421799419Eb782628e73e7220d8E0A207469a3` | 236 | 115.813591054868217468 | 49.0736% |

At approximately 02:36 UTC on the same date, the Venus API's `supplierCount` fields were 26, 16, 40 and 19 for these markets, respectively. They weren't sampled at the fixed block, may count market suppliers rather than unique people and don't measure demand for our product. At the same time, [CoinMarketCap's NVDAB page](https://coinmarketcap.com/currencies/nvidia-tokenized-bstocks/) displayed roughly 135,000 token holders. That page didn't expose a comparable holder methodology in this review. Dividing a CMC holder display by a Venus market count would be unsound, and neither number measures eligible users wanting a USDT loan.

## Product implication

NVDAB still supports a small isolated cash-target illustration while the cap has headroom, but **0.76% remaining** is a weak basis for a broad onboarding promise. Between the 00:59 UTC and 07:11 UTC fixed-block reads, NVDAB headroom fell from `20.039492377880186433` to `11.416397078470495107` units. We didn't attribute that change to particular accounts or transactions. The app already fetches an indexed cap snapshot and flags an input above headroom; the index can lag, so a current contract read and Venus transaction checks remain necessary before action.

Other bStock markets have more cap room in this one snapshot. Choosing one as a substitute would require a permitted Binance Web3 sell quote, holder task, issuer restrictions and account-risk validation for that asset. This screen doesn't validate those alternatives. It strengthens the scheduled 4 October product checkpoint: if NVDAB headroom closes or the quote or holder gate fails, don't claim that the existing sell-or-borrow prototype is a functional mass-user product.

## Targeted NVDAB recheck

At BNB Chain block `125263488`, `2026-10-02 08:51:16 UTC`, the local fixed-block contract reader returned `11.416397078470495107 NVDAB` of Core supply-cap headroom. It checked chain 56, deployed Core and vNVDAB code, pinned underlying, supply cap, vToken supply, stored exchange rate and block time through the [BNB Chain public RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/). A 1 NVDAB deposit still fits the measured cap alone. The value is unchanged from the earlier fixed-block read, but a later transaction can change it; this is not a simulation or a borrowing approval. The signed Binance route and holder task remain unobserved.

At block `125335595`, `2026-10-02 17:52:17 UTC`, the same reader returned `11.416397058476516341 NVDAB` of headroom. One NVDAB still fits this cap check. The small change does not identify a supplier, prove that a deposit will execute, or replace the missing signed quote and holder task.

At block `125394235`, `2026-10-03 01:12:12 UTC`, the same pinned public-RPC reader returned `11.416397058476516341 NVDAB` of headroom. Its one-NVDAB check passed. This is a dated cap precondition only. It doesn't establish an eligible holder, remaining cap at transaction time, market entry, USDT borrowing capacity or safe account-level risk.
