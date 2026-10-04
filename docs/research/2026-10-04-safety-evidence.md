# H-RWA-SAFETY evidence report

**Checked:** 2026-10-04 UTC  
**Scope:** BNB Smart Chain mainnet tokenized-stock data and read-only Binance Web3 API observations.  
**Status:** `H-RWA-SAFETY: PRODUCT_CORE_PROVISIONAL`. No funded transaction, signature, broadcast, fill, or user session was observed.

## Question and product boundary

The candidate user is a self-custody holder or buyer who needs to know whether a specific tokenized-stock action has enough current evidence to proceed. The trigger is a selected asset, amount, route, and market context. The current workaround is a wallet or stock-terminal quote plus separate issuer and market checks. The needed result is a bounded next action, or an explicit reason to stop and ask for human review.

The event requires one of bStocks, Ondo, or xStocks to be central, spot activity on BNB Smart Chain mainnet, a working Binance Web3 API integration, and a reproducible judge path. These requirements are from the [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) and the local [event-rules record](../01-event-rules.md). The safety evidence below does not establish eligibility for a funded demo.

## Measured facts

### 1. No independent underlying reference clock

On 4 October, the signed `/rwa/price` sample contained 40 rows, each with `tokenPrice`, `referencePrice`, and `tokenPriceUpdatedAt`, but no independent underlying-equity as-of timestamp. The Binance [RWA Data documentation](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) defines `referencePrice` as derived from token price and `tokenPriceUpdatedAt` as token-price time. Two `/underlying-market` responses and two `/underlying-profile` responses also exposed no independent reference timestamp. EXP-RWA-010 recorded 1,716 LIVE rows from 10:22 to 14:05 UTC, with zero independent reference-age observations and 1,716 unknown reference ages. See [EXP-RWA-010](../../experiments/EXP-RWA-010/results.json), the [field-level repro](../devex/repros/2026-10-04-independent-reference-clock.md), and the [source gate](2026-10-04-reference-clock-source-gate.md).

The measured token clock is not an underlying-stock clock. In the same-ticker, same-minute subset, 184 bStock rows and 184 Ondo rows covered COIN, MSTR, NVDA, and TSLA. Eight bStock token timestamps and zero Ondo token timestamps were over 60 seconds old; the longest bStock token age was 295.123 seconds. This measures token-update freshness only.

**Inference:** a fast token update cannot support a claim that the issuer's stock reference is fresh, independently priced, or suitable for an off-hours signal.

**Unknown:** the inspected Binance fields do not show whether another permitted Binance or issuer source carries a timed traditional-equity reference. APRO's observed `updatedAt` is a timed NVDAB/USD token oracle value, not the issuer's underlying NVDA clock. No Alpaca or Nasdaq authenticated benchmark call was made.

### 2. Off-hours behavior is not documented well enough to interpret as one market

The complete 4 October signed `/rwa/tokens` response had 488 BNB Chain entries. Thirty-one Ondo rows reported `marketStatus=offhours`, a value not listed in the current RWA enum. In the 1,716-row EXP-RWA-010 sample, 230 rows were `offhours` and 1,486 were `unknown`. Two Sunday NVDA `/underlying-market` calls returned `openState=true`; Ondo returned `offhours`, while bStock returned null market status. The same state repeated at 14:00 UTC. See the [market-status repro](../devex/repros/2026-10-04-market-status-enum.md), [Sunday state repro](../devex/repros/2026-10-04-underlying-market-weekend-state.md), and [EXP-RWA-010](../../experiments/EXP-RWA-010/results.json).

**Inference:** `openState` may describe token or issuer venue availability rather than regular US equity trading. Nasdaq's published hours are useful context, not proof of the API field's venue semantics.

**Unknown:** the exact meaning of `offhours`, `openState`, `nextOpenTime`, and `nextCloseTime`, including venue and timezone. This is an observed documentation boundary, not a declared documentation defect.

### 3. Displayed spread is not a route

EXP-RWA-002 captured 34 bStock/Ondo ticker pairs at 11:00 UTC. The largest raw gap was CBRS at 6.2036%. At 12:51 UTC, the gap was 5.25%; the cheaper Ondo token's price timestamp was 35.85 hours old. The CBRSB buy and sell requests each returned one LiquidMesh `SWAP` route, while the cheaper CBRSon buy and sell requests returned business code `40367` and zero routes. See [EXP-RWA-002](../../experiments/EXP-RWA-002/results.json) and [CBRS displayed gap versus routes](2026-10-04-cbrs-displayed-gap-vs-routes.md).

As counterevidence to a permanent no-route claim, the 4 October 13:25 to 13:26 UTC 100 USDT coverage probe returned routes for 38 of 40 monitored contracts: 34 of 35 bStocks and 4 of 5 selected Ondo assets. AAOI bStock later returned routes at 10, 100, and 1,000 USDT, while MSTR Ondo returned `40374` at all three sizes. The requests were sequential and unfunded. See [weekend route coverage](2026-10-04-weekend-route-coverage.md).

**Inference:** a catalog price difference is not an executable spread. Route availability, amount, quote lifetime, issuer rights, eligibility, fees, and settlement must be checked separately.

**Unknown:** whether both representations can be acquired or exited by the same eligible user at the same time and net cost.

### 4. A quote is not proof of eligibility

EXP-RWA-009 made eight corrected signed quote calls on 4 October from 10:36:14 to 10:36:17 UTC for MSTRB and NVDAB at 10, 100, 1,000, and 10,000 USDC. All eight returned one LiquidMesh route, `executionMode=SWAP`, verified 18-decimal input units, and reported price impact from 0.0004685048% to 0.0030489031%. The source records zero fills and `holder_eligibility_verified=false`.

The 40-contract Sunday coverage sample likewise used one temporary, unfunded address. An unsigned build and off-chain simulation returned an API success but predicted `FAILED` because the wallet lacked tokens. No approval, signature, gas payment, broadcast, or fill followed. See [EXP-RWA-009](../../experiments/EXP-RWA-009/results.json), [quote depth](../../experiments/EXP-RWA-009/quote_depth.csv), and the [unsigned-build repro](../devex/repros/2026-10-04-unsigned-build-simulation.md).

**Inference:** a returned quote proves only that the API produced a short-lived estimate for the request context. It does not prove geographic eligibility, holder status, allowance, balance, execution, final cost, or settlement.

**Unknown:** the founder's eligibility and whether the same route accepts a funded, eligible holder wallet.

### 5. bStock on-chain multiplier cross-check

On 4 October, the signed catalog was captured at 13:40:03 UTC and compared with BNB Chain reads pinned to block `0x77dd188`, timestamped 13:42:15 UTC. The audit covered all 35 monitored bStock equity contracts. Current on-chain `uiMultiplier()` matched the catalog `tokenToShareRatio` for 35 of 35; `newUIMultiplier` equalled current for 35 of 35; all 35 had `effectiveAt=0`; and there were zero read errors. See [EXP-RWA-011 audit](../../experiments/EXP-RWA-011/onchain_multiplier_audit.json), [multiplier note](2026-10-04-bstock-multiplier-onchain.md), the [raw RPC fixture](../../data/external_reference/2026-10-04-bstock-multiplier-rpc-raw.json), the [BNB JSON-RPC documentation](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/), and [BEP-677](https://github.com/bnb-chain/BEPs/blob/master/BEPs/BEP-677.md).

**Inference:** this supports a current display-scaling and token/share normalization guard. It does not prove backing, legal rights, issuer action dates, historical corporate-action handling, or future multiplier correctness. The catalog and block reads were close but not atomic.

**Unknown:** whether a future split, rebase, scheduled multiplier, or issuer action will be reflected in time for a specific trade. EXP-RWA-011's 796-row live ratio watch found zero transitions from 10:22 to 12:10 UTC, and its CRWD/NFLX profile reads exposed no dated corporate-action field. The confirmed issuer events and their limits are recorded in [the real-event audit](../../experiments/EXP-RWA-011/real_event_audit.md).

### 6. Documentation says RFQ, observed route says SWAP

At 10:53:50 UTC, a signed read-only NVDAB quote for 10 USDC returned one LiquidMesh route with `executionMode=SWAP`. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) says equity/RWA tokens always return `RFQ` in the quote response, while the broader [Trading API introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) describes bStock SWAP. The corrected eight-call ladder and the 40-contract coverage probe also returned only `SWAP` routes in their observed samples. See the [route repro](../devex/repros/2026-10-04-rwa-swap-route.md) and [DX evidence summary](../devex/2026-10-04-evidence-summary.md).

**Measured interpretation:** the response field observed in these calls was `SWAP`, not `RFQ`. This is a documentation and route-semantics question for verification, not a declaration that the documentation is defective. A client must branch on returned `executionMode` and preserve the exact route response.

**Unknown:** which asset, provider, vendor, endpoint, or API version conditions produce `RFQ` versus `SWAP`, and which execution and cost rules apply to each.

## Supporting safety evidence and counterevidence

The same-cycle EXP-RWA-002 formula check matched `tokenPrice / tokenToShareRatio` at reported precision for all 40 rows at 11:55:02 UTC. This confirms token-derived arithmetic only. The 4 October Sunday comparison with Friday 2 October Yahoo closes showed six token-derived values above close by 0.2078% to 1.3251%, but Yahoo's daily bar has no independent intraday timestamp and no Monday result was observed. See [formula output](../../experiments/EXP-RWA-002/reference_formula_results.json) and [external-close benchmark](2026-10-04-external-close-benchmark.md).

The strict offline policy probe used 40 LIVE rows, a synthetic 100 USD intent, and a 60-second token-age limit at 12:00 UTC. It returned 3 `DENY`, 37 `NEED_HUMAN`, and 0 `ALLOW`. All 40 lacked verified issuer access, independent reference time, quote, price impact, and simulation evidence. This was a synthetic policy input, not a user decision or trade. See [policy falsification](2026-10-04-live-policy-falsification.md).

The first quote ladder used incorrect six-decimal USDC units and is quarantined. The corrected ladder used 18 decimals. This is an integration error found and corrected during research, not evidence of an API failure. The [unit repro](../devex/repros/2026-10-04-bsc-usdc-decimals.md) and [DevEx log](../devex/2026-10-04-evidence-summary.md) retain both facts.

## Product interpretation

These observations support a provisional product core: a read-only, fail-closed evidence receipt that separates token freshness, market-state semantics, on-chain display scaling, route output, eligibility, and simulation. It may explain why a requested action is `DENY` or `NEED_HUMAN` and identify the next verification step.

They do not support an automatic safety verdict, an arbitrage claim, an off-hours price-discovery claim, a guaranteed exit, or a net-return claim. They also do not support a user-demand claim. No independent user session, consented holder task, adoption measure, interview, or observed decision change exists. The founder has provisionally selected the safety primitive as the product core; the final user task and submission claim remain open. See [STATUS.md](../../STATUS.md), [docs/status.md](../status.md), and the [decision log](../decisions/decision-log.md).

## Next verification gates

1. Obtain a permitted, independently timestamped underlying-equity benchmark with source, venue, market session, data rights, and as-of semantics. Keep it separate from `tokenPriceUpdatedAt`, APRO's token-oracle time, and server response time.
2. Re-run the 40-contract tape through a regular US session and the next opening benchmark. Explain `offhours`, `openState`, and next-open/close fields for each relevant venue. Preserve Saturday and Sunday gaps as gaps.
3. Repeat the same asset, side, and amount with a consenting eligible holder or an explicitly authorized test wallet. Record eligibility basis, balance, allowance, quote, route mode, simulation, gas units, final fee, broadcast, and fill. Do not infer eligibility from a quote.
4. Verify route semantics with Binance for the exact endpoint and vendor conditions that returned `SWAP`, then reconcile quote, build, simulation, and execution documentation without assuming RFQ.
5. Continue the bStock multiplier watch and capture any scheduled `newUIMultiplier` and `effectiveAt` transition with a dated issuer action source. Keep split and rebase fixtures labelled synthetic until a live pre/post event is reconstructed.
6. Observe one real user task against the strongest incumbent path, with consent and no private identity in the repository. Select the product only if the result changes the user's next action and the evidence is reproducible. Otherwise retain this report as a safety boundary, not a product claim.
