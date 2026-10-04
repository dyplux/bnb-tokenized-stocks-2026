# Project submission draft

**Prepared:** 2026-10-04. **Status:** internal draft for the provisional safety product. No form has been submitted from this file. Recheck every claim against the final build and Monday data before submission.

| Form field | Prepared answer or owner |
|---|---|
| Team or project name | Undecided. “Dyplux RWA Safety” labels the current local build, not an approved final name. The founder confirms the name against registration and the DX report. |
| Contact email | Founder enters directly in the form. |
| Prize wallet or Binance UID | Founder enters directly in the form. Never commit either. |
| Telegram | Optional; founder decides. |
| Tracks | Main Tokenized Stocks track. Claim the Agentic Wallet or Agent Studio special only after a working qualifying integration exists. |
| Public repository URL | `https://github.com/dyplux/bnb-tokenized-stocks-2026`, after founder authorization to make the reviewed repo public. |
| Demo video URL | Pending. The older Exit Check clip shows a retired flow and mustn't be submitted for this product. |
| Deployed link or judge instructions | Current [safety judge-run guide](safety-judge-run.md) is local. A stable judge-access path is still needed; the event page's deployed-link wording needs organiser clarification. |
| DX report | Submit the factual [current draft](dx-form-current.md) after the Monday market-state observations and founder-only fields are checked. |

## What did you build?

> Dyplux RWA Safety reviews one proposed tokenized NVDA purchase on BNB Chain before a wallet signs it. A user selects NVDAB or NVDAon, enters a USDT amount and sets spend and price-impact limits. The local screen reads Binance Web3 RWA identity, token price, market state and an amount-specific route. For NVDAB it checks the displayed share multiplier against one recent BNB Chain block. A deterministic policy returns ALLOW, DENY or NEED_HUMAN with reason codes, source times and a downloadable receipt. A separate read-only 10 USDT public-wallet trial requests an exact-wallet quote, unsigned transaction build and off-chain simulation, then produces a blocked pre-execution packet. In the 4 October sample the policy returned NEED_HUMAN and the unfunded simulation predicted failure. No token was bought or sold.

The [4 October evidence report](../research/2026-10-04-safety-evidence.md) gives six observed reasons for a pre-signing check. The signed price API has a token update time but no observed independent underlying-stock as-of time. Sunday Ondo responses reported the undocumented state `offhours`; a same-ticker displayed gap had no corresponding route for the cheaper representation during a bounded probe. A quote alone didn't establish issuer access. The [pre-execution packet](../product/pre-execution-packet-2026-10-04.json) records the current stop reasons. These observations motivate the safety workflow; they don't prove profitable trading or user demand.

**Current limits:** the interface is local and read-only. Issuer rights and the intended user's access haven't been verified; no independent stock-reference clock, funded passing simulation, signature, broadcast or fill exists. Monday's preregistered open-price test remains a separate experiment and isn't a product claim. Final copy must change if the build or evidence changes.
