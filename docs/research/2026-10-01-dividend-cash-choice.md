# Research gate: turning reinvested bStock exposure into cash

- **Checked:** 2026-10-01, 13:31 to 13:32 UTC for the public multiplier reads
- **State:** product hypothesis, no build or trading approval
- **User:** an eligible BNB Chain bStock holder who wants some spendable USDT from an existing holding

## The observable problem

[Binance's bStocks FAQ](https://www.binance.com/en-AE/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38) says net dividends are generally reinvested through a multiplier. The holder's raw on-chain amount stays constant, the displayed exposure rises, and no separate cash arrives. This is an economic design choice by the issuer, not a missed payment. A holder who wants cash must sell part of the position. Selling decreases future stock exposure and may incur spread, gas, tax consequences and other costs.

The [18 September Binance announcement](https://www.binance.com/en/support/announcement/detail/7df43402f0094e79b293bd7fbb574474) named four affected bStocks. It set record snapshots at 21 September 00:00 UTC for AVGOB, QQQB and METAB and at 24 September 00:00 UTC for STXB. It said on-chain holders would receive a multiplier adjustment, while conversion and transfers could pause. These are issuer statements. We haven't reconstructed each contract's multiplier event or a wallet's entitlement.

The [BEP-677 scaled UI specification](https://github.com/bnb-chain/BEPs/blob/master/BEPs/BEP-677.md) defines `uiAmount = rawAmount × uiMultiplier / 1e18`. Standard BEP-20 transfers use raw amounts. Optional UI conversion helpers round down, so repeated conversion is not a sound accounting method. Any app must keep raw amounts as its ledger and separate dividend changes from stock splits and transfers. The specification alone doesn't prove that each deployed bStock supports every optional helper.

## A dated public measurement

At 13:31 UTC, the [public Binance bStock list](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3) returned these BNB Chain contracts and multipliers. At 13:32 UTC, a read-only `eth_call` to QQQB's `uiMultiplier()` at `https://bsc-dataseed.binance.org/` returned the same integer as the Binance list: `1000724838657573033` (18 decimals).

| bStock | Contract | Multiplier in public list |
|---|---|---:|
| QQQB | `0x205812cdbed920aff76c6580abd681a46d11efc7` | 1.000724838657573033 |
| METAB | `0x7425889fe94f9d693e8daefe88bcced6acfef4c0` | 1.000548290410744950 |
| AVGOB | `0x76682c454467b3a1150ad8b6a92fc5ee2c21d7ed` | 1.001269208611258122 |
| STXB | `0x2e065f65f1699964f4092de1d39a8efe6c8d6f32` | 1.000559247178444730 |

**What the measurement does not establish:** the previous multiplier, the change attributed to the September event, a particular holder's record-date balance, the token price at distribution, or a wallet-size sell quote. A public RPC returned `-32005 limit exceeded` for a 5,000-block log query and `-32000 missing trie node` for historical `eth_call` requests during the earlier read-only attempt. [BNB Chain's RPC documentation](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/) explicitly says `eth_getLogs` is disabled on the listed public mainnet endpoints. A suitable event index or archive source is needed. Repeating broad log scans on that public endpoint isn't a useful next step.

### Economic size before fees

The following is **arithmetic, not a measured dividend or trade**. Suppose a wallet bought QQQB when its multiplier was exactly 1, kept the same raw amount, and the current position is worth the value in the first column. The current uplift relative to that starting multiplier is `position value × (M - 1) / M`, with `M = 1.000724838657573033`. Price changes, actual purchase time, previous multiplier, taxes, spread, gas and trade minimums are excluded.

| Current position value | Illustrative cumulative uplift |
|---:|---:|
| 100 USDT | 0.0724 USDT |
| 1,000 USDT | 0.7243 USDT |
| 5,000 USDT | 3.6216 USDT |
| 10,000 USDT | 7.2431 USDT |

Under those assumptions a 5 USDT sale would require a position of about 6,903 USDT. Binance's [$5 fractional entry description](https://www.binance.com/en/academy/articles/what-are-bstocks-a-guide-to-tokenized-stocks-on-binance) concerns buying on its product; it is **not** a verified Binance Web3 API sell minimum. This calculation challenges a product for casual $100 holders. A useful cash-out may require a larger account, a long accumulation period or a different asset. There is no extra yield from selling: the user converts part of existing equity exposure into USDT.

### Screen for a larger, still unverified increment

At 14:05 UTC on 2026-10-01, a second read of the [public Binance bStock list](https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3) returned 87 BNB Chain rows. SQQQB had the highest listed multiplier, 1.009841016242566331; SOXSB was next at 1.009026219854107205. The [21 September Binance announcement](https://www.binance.bh/en/support/announcement/detail/7ddb0038f14e4fa08f4cbbd7dd29d00f) names both, plus MUUB and TQQQB, for net dividend reinvestment. It sets record snapshots for SOXSB/MUUB at 22 September 00:00 UTC and TQQQB/SQQQB at 23 September 00:00 UTC. These are leveraged and inverse ETF representations, so a larger multiplier does not imply a better investment or a higher net return.

At a later 2026-10-01 source check, [ProShares' own distribution table](https://www.proshares.com/our-etfs/find-leveraged-and-inverse-etfs?benchmark=&etftype=&product=Product+Overview+&search=+&strategy=Fixed+Income) listed SQQQ's underlying distribution as **$0.473413 per share**, with ex/record date 23 September and payable date 29 September 2026. This confirms an underlying cash distribution with matching calendar context. It doesn't establish the bStock issuer's net reinvestment amount, withholding, multiplier before the update, the wallet's eligibility or the transaction that changed the contract. The Binance snapshot at 23 September 00:00 UTC is an issuer rule and shouldn't be silently equated with the underlying fund's record date.

There is a stronger product objection. [ProShares defines SQQQ](https://www.proshares.com/our-etfs/leveraged-and-inverse/sqqq) as a fund targeting **-3x the Nasdaq-100's daily performance** and warns that returns over longer holding periods may diverge materially from that daily target. A long-term "live on the dividend" persona is therefore a poor fit for SQQQB. Its 1.009841 multiplier made it useful for a magnitude screen, not a recommended holding or the product's default example. QQQB is unleveraged, but its illustrated 1,000 USDT uplift is only about 0.7243 USDT before costs. Until an economically meaningful unleveraged case and a holder task are observed, the cash-flow hypothesis is weak for a common user.

At 14:16 UTC, a read-only `eth_call` to SQQQB's `uiMultiplier()` at `0x25e572b466d152604d9e6c3e53b432b978825342` returned `1009841016242566331`, matching the website list. This confirms the current multiplier on-chain, but still doesn't identify the event that produced it.

For SQQQB, the same deliberately artificial `M0 = 1` calculation gives about 9.745 USDT on a 1,000 USDT current position and 0.975 USDT on a 100 USDT position, before every execution cost. The current multiplier may aggregate more than one event. No event-specific or holder-specific income has been measured. The eight announced contracts are in the [manual Dune event query](queries/bstock-multiplier-events.sql); its results are pending. This screen slightly improves the cash-out size for a larger position but does not pass the product gate.

At 14:24 UTC, the separate [Binance Spot exchange-info response](https://api.binance.com/api/v3/exchangeInfo?symbol=SQQQBUSDT) reported `SQQQBUSDT` as `TRADING` with a 5 USDT `NOTIONAL.minNotional` and a 0.01 bStock limit-order quantity step. A sequential [depth response](https://api.binance.com/api/v3/depth?symbol=SQQQBUSDT&limit=5) showed top bid/ask of 34.68/34.70 USDT. The depth response gave an update ID but no server event timestamp. This establishes an incumbent **CEX** constraint at that read, not the minimum, spread or fill on the required BNB Chain Web3 route. Under the artificial `M0 = 1` example, a 500 USDT current position contains about 4.873 USDT of uplift, below that CEX minimum even before fees. A 1,000 USDT position is above it, but its actual on-chain quote remains unknown.

## What exists already

| Existing flow | What it does | Gap that remains to test |
|---|---|---|
| [Binance Spot and bStocks](https://www.binance.com/en/academy/articles/what-are-bstocks-a-guide-to-tokenized-stocks-on-binance) | Eligible users can trade bStocks 24/7 and see the multiplied balance. | A holder can sell manually. We haven't found a documented choice to sell only a verified post-distribution increment with a cost floor. Absence from the pages checked isn't proof it doesn't exist elsewhere. |
| [Steward](https://github.com/zkasuran/steward-bnb) | Its public repo describes a position ledger, corporate-action detection and a Paycheck payment plan. The [corporate-action source](https://github.com/zkasuran/steward-bnb/blob/master/packages/sdk/src/ledger/corporate-actions.ts) labels positive unexplained balance gaps. The [Paycheck source](https://github.com/zkasuran/steward-bnb/blob/master/packages/agent/src/paycheck.ts) builds unsigned b402 payment material and explicitly sends nothing. | A mainnet sale of the verified incremental bStock exposure with net USDT proceeds is not shown in those files. We haven't run the competitor or proven its ledger wrong. |
| [Portir](https://github.com/yeheskieltame/portir) | Public source offers a sell rule on a testnet token when a price crosses a threshold. | Its inspected rule is price triggered and uses a testnet stock, not an observed mainnet dividend cash-out. Other code may cover more. |
| [Binance Agentic Wallet](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) | Its documented flow can sell part of a tokenized stock position. | A generic sell can implement the result manually. We need proof that tracking the multiplier and all-in cost changes a real user's decision. |

The separate [Portir](https://github.com/yeheskieltame/portir), [OneTicker](https://github.com/JemIIahh/oneticker), [yostocks](https://github.com/yostocks-protocol/yostocks) and [NightDesk](https://github.com/PhiBao/nightdesk) repositories already publish quote guards, price references, tapes or session-aware agents. Their repo descriptions are claims, not observed product performance. They make the previous generic execution guard weak as a standalone submission.

## Candidate user flow and its decision rule

1. An eligible holder connects a BNB Chain wallet and selects an authentic bStock. The app shows raw amount, current multiplier, previous verified multiplier, event type and timestamp. If history is missing, it says **amount not attributable**.
2. The holder chooses a target: keep all exposure, or convert a bounded amount of the verified incremental exposure into USDT. A purchase after the record-date snapshot, a transfer or a split must not be labelled a personal dividend without reconciliation.
3. Request a fresh, wallet-bound Binance Web3 API sell quote for that exact raw token amount. Show proceeds, gas, route, expiry and cost. If net proceeds fall below a user-set floor, show **wait** instead of a trade button.
4. The user confirms with their own wallet. Show the resulting BNB Chain transaction and actual USDT received. No agent holds an unrestricted trading key.

The point of this flow is a cash-flow choice with measured net proceeds. It cannot promise higher investment returns. The safe default is to keep compounding if the transaction is uneconomic or the entitlement cannot be proved.

## Agent Studio fit

[BNB Agent Studio](https://docs.bnbchain.org/developer-kit/bnbchain-studio/) currently scaffolds a persistent **seller** service with ERC-8004 identity, A2A/MCP/x402 faces and on-chain payment rails. Its managed BNB trial is testnet only and lasts 48 hours. A separate corporate-action event service could watch multiplier changes, reconcile the issuer announcement and return a dated machine-readable event to wallet agents. Other agents would need to want and pay for that artifact; raw multiplier reads are free. No buyer or necessary paid dependency has been observed, so this service is **not approved for build**. Studio must not be presented as the mainnet trading wallet, and x402 must not be confused with income paid to a bStock holder.

## Gate and falsifiers

This is the strongest current *post-hold cash-flow* hypothesis, but it remains a narrow, unvalidated task. It reaches spec only if all of these hold:

1. Recover one QQQB or other bStock multiplier event and a consenting test wallet's raw position before and after the event, without exposing the wallet or confusing a split with a dividend.
2. Get a signed, read-only Binance Web3 API sell RFQ for the computed increment, and record actual minimum, net USDT, gas, quote lifetime and any geographic restriction. A live amount may be too small to quote.
3. Ask an eligible holder to perform the same job in Binance and an existing agent flow. Record time, output, errors and whether a cash-flow target matters to them. Don't infer demand from likes or a README.
4. Reject this direction if the trade is systematically below the route minimum or fees, if the previous multiplier can't be reconstructed reliably, or if a current product already gives the same cost-aware action.

**Decision:** no product selected, no application code or Studio setup yet. The generic quote guard moves out of the active slot. This cash-flow hypothesis remains a falsification target because it has a measurable cost gate, but the QQQB amount is tiny for a modest holding and the larger SQQQB figure comes from a daily leveraged inverse ETF unsuited to the proposed long-hold persona. It needs a better asset and an observed holder before it can justify a build.
