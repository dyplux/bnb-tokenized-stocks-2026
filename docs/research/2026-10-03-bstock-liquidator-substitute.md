# bStock liquidation is not an unoccupied fallback

**Checked:** 2026-10-03 UTC. **Scope:** official Venus governance and risk reports. This is a substitute check, not a liquidation strategy, live deployment audit or user-demand observation.

## Primary-source observations

- [P] The [24 July Venus governance proposal](https://community.venus.io/t/bnb-chain-ethereum-ebtc-delisting-lisusd-resumption-bstock-liquidator-flash-loans/5872) describes a **dedicated bStock backstop liquidator** for undercollateralized positions and proposes whitelisting it for Core-pool flash loans. The proposed path repays a position, receives collateral and sells it inside one transaction. The document states that Core flash loans are limited to approved accounts. This proposal alone does not prove the whitelist was executed, how often the liquidator ran or whether it can always obtain a weekend quote.
- [P] The [Venus August risk report](https://community.venus.io/t/venus-monthly-report-august-2026/5941) reports an APRO pivot feed for bStock markets under VIP-654, adding an oracle cross-check. It does not report a measured bStock liquidation opportunity for an outside builder. The same report gives approximately **$0.3 million** of RWA supply in its appendix, but [the prior source audit](2026-10-03-public-holder-task-scan.md) found a conflict with the July report's SKHYB figure. Do not use the appendix as a clean bStock market-size estimate.
- [P] The [June Venus risk report](https://community.venus.io/t/venus-monthly-report-june-2026/5857) named maker RFQ liquidity at weekends as a structural watch-item for potential bStock liquidations. Its wording about weekend token trading predates the current 24/7 bStock Spot documentation and the [3 October live MSTRB quote](2026-10-03-mstrb-weekend-rfq-result.md). It cannot establish that all bStock routes close at weekends today.

## Consequence

- [I] A generic weekend liquidator or liquidation-warning agent is not an evidence-backed replacement for D-017: Venus has an announced backstop route and oracle protection, access is restricted, and no current outside opportunity, eligible user task or net execution outcome has been measured.
- [?] Deployed whitelist state, actual backstop transactions, liquidation frequency and weekend quote depth remain unchecked. Those would matter only if a specific user or protocol task made liquidation the selected product. They are not a reason to build one before the 4 October cash-choice checkpoint.
