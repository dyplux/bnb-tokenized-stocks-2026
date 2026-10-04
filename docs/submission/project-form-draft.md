# Project submission draft

**Prepared:** 2026-10-04. **Status:** internal draft for the frozen safety core. No build form has been submitted from this file. Recheck every claim against the final build before submission; Monday only decides whether an optional off-hours finding is added.

| Form field | Prepared answer or owner |
|---|---|
| Team or project name | Proposed: **Dyplux Execution Safety Layer for Tokenized Equities**. The founder confirms the final name against registration and the DX report. |
| Contact email | Founder enters directly in the form. |
| Prize wallet or Binance UID | Founder enters directly in the form. Never commit either. |
| Telegram | Optional; founder decides. |
| Tracks | Main Tokenized Stocks track. Claim the Agentic Wallet or Agent Studio special only after a working qualifying integration exists. |
| Public repository URL | `https://github.com/dyplux/bnb-tokenized-stocks-2026`, public and accessible without sign-in on 4 October. |
| Demo video URL | Pending. The older Exit Check clip shows a retired flow and mustn't be submitted for this product. |
| Deployed link or judge instructions | [Public dated judge packet](https://dyplux.github.io/bnb-tokenized-stocks-2026/) and [local live judge-run guide](safety-judge-run.md). Chrome desktop and mobile checks passed on 4 October. The public page doesn't call the signed API; it labels the safe policy branch synthetic. |
| DX report | Submit the factual [current draft](dx-form-current.md) after the Monday market-state observations and founder-only fields are checked. |

## What did you build?

> Dyplux's Execution Safety Layer reviews one proposed tokenized NVDA purchase on BNB Chain before a wallet signs it. A user selects NVDAB or NVDAon, enters a USDT amount and sets spend and price-impact limits. The local screen reads Binance Web3 RWA identity, token price, market state and an amount-specific route. For NVDAB it checks the share multiplier against a recent BNB Chain block. A deterministic policy returns ALLOW, DENY or NEED_HUMAN with reason codes, source times and a downloadable receipt. A separate read-only 10 USDT public-wallet path binds one exact-wallet quote to the policy, unsigned transaction build and off-chain simulation. On 4 October it returned NEED_HUMAN and the unfunded simulation predicted failure. A public judge page shows this dated decision beside a clearly labelled synthetic ALLOW fixture. No token was bought or sold.

The [4 October evidence report](../research/2026-10-04-safety-evidence.md) gives six observed reasons for a pre-signing check. The signed price API has a token update time but no observed independent underlying-stock as-of time. Sunday Ondo responses reported the undocumented state `offhours`; a same-ticker displayed gap had no corresponding route for the cheaper representation during a bounded probe. A quote alone didn't establish issuer access. The [same-quote pre-execution packet](../product/pre-execution-packet-linked-2026-10-04.json) records the current stop reasons. These observations motivate the safety workflow; they don't prove profitable trading or user demand.

**Current limits:** the live signed-API interface is local and read-only; the public page is a dated packet. Issuer rights and the intended user's access haven't been verified; no independent stock-reference clock, funded passing simulation, signature, broadcast or fill exists. Monday's preregistered open-price test remains a separate experiment and isn't a product claim. Final copy must change if the build or evidence changes.
