# What can be proved without a holder session

**Checked:** 2026-10-03 UTC. Read-only evidence audit using the isolated Plus Sol profile, followed by a direct check of the [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks). No wallet, new API call or transaction was used for this audit.

## Measured technical evidence

- [O] A [fixed-block probe](2026-10-03-nvdab-holder-debt-overlap.md) found that **9 of 15** top-ranked vNVDAB accounts had entered NVDAB collateral and positive stored USDT debt at block **125416980**. Eight were EOAs and one was a contract. This biased sample proves account-level coexistence, not nine people or nine customers.
- [O] A [signed quote and unsigned build](2026-10-03-target-minimum-check.md) estimated **100.000443760010104468 USDT** from **0.426034167623447674 NVDAB**. At 0.5% slippage, the built minimum was **99.500441541210053945 USDT**, below the 100 USDT target. No holder, balance, approval, fill or net proceeds were observed.
- [P] The [event rules](https://www.bnbchain.org/en/hackathons/tokenized-stocks) require a working project with Binance Web3 API integration and bStocks, Ondo or xStocks central. They direct teams to dry-run with the Transaction API and demonstrate with small live mainnet amounts. They do not require a user interview.

## Claim boundary

A judge can inspect a dated, read-only comparison of an estimated sale quote and a public Venus collateral/loan scenario. It must be labelled illustrative and cannot decide which path is safe or desirable for a particular holder. The quote minimum, fees, account-wide borrow risk and country eligibility remain separate unknowns. A read-only demonstration alone also falls short of the event's mainnet demo direction.

The consenting-holder requirement in [D-033](../decisions/decision-log.md) is an **internal product-validation gate**, not an eligibility rule. The [live Steward check](2026-10-03-steward-live-swipe-same-task.md) and Binance's [bStocks DeFi Center](2026-10-03-binance-bstocks-defi-substitute.md) mean the borrow side already has substitutes. The untested difference is whether seeing a same-cash sale beside it helps a real holder decide.

**Next observation that changes the product decision:** one consenting, eligible holder brings their own actual cash need and account to a read-only walkthrough. Record what they would do in the existing venue first, then whether this comparison changes their understanding of sale minimum, costs and loan risk. Do not record their address or identity in Git. If no such session occurs, retain only the narrow technical-demo claim and apply D-033 at its internal checkpoint.
