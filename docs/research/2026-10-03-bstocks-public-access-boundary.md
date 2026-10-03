# bStocks public-access boundary for the current prototype

**Checked:** 2026-10-03 UTC. **Source:** [Binance bStocks deposit, withdrawal and conversion FAQ](https://www.binance.com/en/support/faq/detail/f0d41139fadc4790bf9a4c0c7bce2e88), published 11 June and updated 29 July 2026. This note concerns the current NVDAB read-only screen, not a legal opinion on any person's eligibility.

## Published facts [P]

The FAQ says bStocks are available on a secondary-market basis only to eligible users in permitted jurisdictions. It says transfers can be subject to smart-contract controls, screening and eligibility rules. Its third-party integration section tells integrators to enforce geographic restrictions and says a public REST country-eligibility endpoint exists. The FAQ doesn't provide that endpoint's path or schema in the inspected page.

The [hackathon event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) requires a public repository and a deployed link **or judge-run instructions**. The [live form audit](../submission/2026-10-01-live-form-audit.md) found the same choice in the submission field. It also found a video URL required by the form.

## Inference and decision [I/D]

A Binance Web3 quote for a public address doesn't establish that a person may buy or hold NVDAB. The local prototype should keep that limit visible. A public quote service without a verified country-eligibility control would go beyond what this team can currently support from the published integration guidance. Prepare a reproducible local judge path and a real screen recording first. Keep the server bound to localhost. Reopen public deployment only after the endpoint and restrictions are resolved or the central asset changes under a documented product decision.

## Unknown [?]

- The exact country-eligibility endpoint, request contract and response semantics.
- The founder's route-specific bStock eligibility. It cannot be inferred from an API quote, self-custody wallet or inability to use a Binance exchange account.
- Whether a read-only public quote interface falls within every part of the FAQ's integration requirement. The conservative local path avoids presuming an exception.
