# Project submission draft

**Prepared:** 2026-10-03. **Status:** internal draft. The final wording must describe the verified final build. No form has been submitted from this file.

| Form field | Prepared answer or owner |
|---|---|
| Team or project name | Exit Check by Dyplux, working name. Founder confirms the final name matches registration and DX report. |
| Contact email | Founder enters directly in the form. |
| Prize wallet or Binance UID | Founder enters directly in the form. Never commit either. |
| Telegram | Optional; founder decides. |
| Tracks | Main track only. No Agentic Wallet or Agent Studio claim. |
| Public repository URL | `https://github.com/dyplux/bnb-tokenized-stocks-2026`, only after the founder authorizes public visibility and the final history/media review passes. |
| Demo video URL | Pending an actual capture of the final behavior. The live form requires it; keep the video at or below four minutes. |
| Deployed link or judge instructions | [Judge-run instructions](judge-run.md). The official event page accepts instructions in place of a deployed link. |
| DX report | Submit the factual DX form first, then tick its completion in the project form. |

## What did you build?

> Exit Check lets a self-custodial BNB Chain user inspect both directions of a possible small tokenized-stock trade before signing. For a USDC amount and public address, it verifies the pinned NVDAB bStock identity through Binance Web3 RWA Data, checks the token contracts on BNB Chain, requests an entry quote through the Binance Web3 Trading API, then requests an immediate inverse quote for the estimated NVDAB output. The screen separates a quoted pair from a missing entry route, missing exit route or incomplete verification. It shows source times, the provider route and any reported network-fee estimates, with a 20-second display window. It neither connects a wallet nor executes a trade. Issuer eligibility, approval cost, gas payment, slippage minimum, fill and future exit price remain unverified.

The two signed 5 USDC quote directions were [observed on 3 October](../research/2026-10-03-usdc-nvdab-roundtrip-quote.md) for a temporary nonholder address before this interface existed. Do not say that this paragraph was reproduced through the final UI until that has happened. Do not claim profit, volume, adoption or an executable round trip.
