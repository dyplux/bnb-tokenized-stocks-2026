# Fixed-block check of bStock UI multipliers

**Question:** does the signed Binance Web3 catalog's `tokenToShareRatio` agree with the on-chain display multiplier for currently monitored bStocks? **Measured:** 4 October 2026. The collector's local signed catalog snapshot was refreshed at 13:40:03 UTC; its timestamp, source response hash and the 35 compared ratios are frozen in the [audit result](../../experiments/EXP-RWA-011/onchain_multiplier_audit.json). The audit pinned all contract reads to block `0x77dd188`, timestamp 13:42:15 UTC, through the [BNB Chain public endpoint](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/). The exact read requests and replies are retained in the [raw fixture](../../data/external_reference/2026-10-04-bstock-multiplier-rpc-raw.json). Reproduce with `python3 scripts/audit_onchain_multiplier.py`.

The [BNB BEP-677 draft](https://github.com/bnb-chain/BEPs/blob/master/BEPs/BEP-677.md) defines `uiMultiplier()` as a display scale in 18-decimal fixed-point units. It also defines `newUIMultiplier()` and `effectiveAt()` for a scheduled update. We queried those three view functions on all 35 bStock equity contracts in the monitored universe. Thirty-two had a nonunit catalog ratio and the sample contained 14 distinct ratio values.

| Observation | Count |
|---|---:|
| Readable current, next and effective-time values | 35 / 35 |
| Current on-chain UI multiplier exactly equals catalog ratio | 35 / 35 |
| `newUIMultiplier` equals current multiplier | 35 / 35 |
| `effectiveAt=0`, no pending change observed | 35 / 35 |

This supports using the on-chain UI multiplier as a current independent cross-check for **display scaling** and token/share normalization. The catalog and block were about two minutes apart, so this isn't an atomic same-block proof. The values don't establish issuer backing, legal rights, source price, historical corporate-action correctness or whether a future split/rebase will be reflected without delay. No live pre/post corporate action occurred in this audit. A later nonzero `effectiveAt` would require checking the schedule and new multiplier before treating a raw-token price move as an economic spread.

The bStock interface replies are consistent with the queried BEP-677 functions. We haven't checked every interface and event required by that draft, so this isn't a full standards-compliance audit. The [synthetic split and rebase cases](../../experiments/EXP-RWA-011/) remain simulations, separately labelled from this fixed-block observation.
