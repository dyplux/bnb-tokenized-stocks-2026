# Sunday NVDA sell routes did not reproduce a blocked exit

**Observed:** 2026-10-04 12:27:23 to 12:27:24 UTC. **Method:** two signed, read-only Binance Web3 Trading API quote GETs through the instrumented client, from an ephemeral nonholder address. No wallet signature, balance check, transaction build, simulation or fill. Full raw responses are retained by hash in the ignored local raw store; the tracked [row table](../../experiments/EXP-RWA-009/sell_side_quote.csv) contains no credentials or wallet address.

The same arithmetic target of 0.1 NVDA share was converted to token units using each provider's `tokenToShareRatio` and 18 token decimals. The ratios in the 11:00 catalog were unchanged in the collector's 12:25 catalog, two minutes before the probe. That confirms arithmetic input sizing for this snapshot, not legal equivalence of the tokens. Both quotes returned route code `0`, one LiquidMesh `SWAP` route, and echoed the intended raw input and 18 output decimals.

| Representation | Token amount sent (raw units / 10^18) | Indicative USDT returned | Reported trade fee | Reported price impact |
|---|---:|---:|---:|---:|
| NVDAB | 0.099922238140845070 | 23.454265883684369640 | 0.06757283 | 0% |
| NVDAon | 0.099828768824468686 | 23.441175893428839881 | 0.05478318 | 0.0001001211% |

The gross output difference was 0.013089990255529759 USDT, about 0.05584% of the Ondo quote. It isn't an arbitrage or a net proceeds calculation. The `estimateGasFee=450000` unit remains ambiguous in the [DevEx repro](../devex/repros/2026-10-04-quote-gas-units.md), and neither quote tested the address's assets, issuer permissions or actual sell acceptance. Routes expire. A previously reported Ondo after-hours sell refusal in [Yostocks' DX log](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/DX_LOG.md) is a competitor observation under different inputs and time, not contradicted as a universal statement by these two estimates.

**Falsification effect:** this selected NVDA size and weekend moment didn't produce the blocked-exit state needed to justify a dedicated recovery product. Don't manufacture one from a different user's report. Retest only if an actual holder, route, asset or hour supplies a concrete failed task and a permitted next action that existing wallet or DEX surfaces don't explain.
