# One-NVDAB cash-task market snapshot

**Observed:** 2026-10-03 about 01:13 UTC. **Source:** [public Venus markets API](https://api.venus.io/markets?chainId=56&limit=100), requested with `accept-version: next`, then the repository's `build_scenario` arithmetic. The separate fixed-block cap reading at BNB block `125394235`, 01:12:12 UTC, is recorded in the [cap screen](2026-10-02-bstock-collateral-cap-screen.md). No wallet, Binance API or transaction was used in this measurement.

| Input or market field | Observed value |
|---|---:|
| Illustrative NVDAB units | 1 |
| Cash target | 100 USDT |
| Indexed NVDAB oracle price | 234.43016754920923174 USD |
| Indexed USDT oracle price | 0.9997900440907408 USD |
| NVDAB collateral factor | 0.60 |
| NVDAB liquidation threshold | 0.70 |
| Indexed nominal capacity of 1 NVDAB | 140.687638730636759726996277143328481 USDT |
| Minimum NVDAB at the collateral factor for 100 USDT | 0.710794501224531247 |
| Isolated health-factor illustration after a 100 USDT borrow | 1.64135578519076219681495656667216561 |
| USDT variable borrow APY snapshot | 5.06581110% |
| Flat-rate simple-interest illustration, 30 days | 0.416368035616438356164383561643835616 USDT |
| Flat-rate simple-interest illustration, 90 days | 1.24910410684931506849315068493150685 USDT |
| Indexed supply-cap headroom | 11.416397058476516341 NVDAB |

The 100 USDT target fits this **isolated market illustration** at this indexed snapshot. It does not include an account's existing collateral or debt, E-Mode, accrued interest, transaction costs, approvals, protocol execution checks or future oracle changes. The nominal capacity isn't a personal borrow limit, and the illustrated health factor isn't a personal risk assessment. The cap reader observed the same headroom separately at a nearby block; neither read guarantees availability at transaction time.

This measurement shows why the same-cash task is technically plausible. It doesn't show that a holder has the asset, can use the route, wants a loan, or gains a better decision than using Binance Agentic Wallet and Venus separately. [D-017](../decisions/decision-log.md) remains provisional until the 4 October checkpoint and the consenting holder task.
