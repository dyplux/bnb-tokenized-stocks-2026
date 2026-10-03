# Same-task substitute check: 5 USDC before a tokenized-stock purchase

**Observed:** 2026-10-03, about 19:27 UTC. **Task:** inspect a 5 USDC stock entry and the matched inverse exit before buying, from an unauthenticated browser or public code. No wallet was connected, no account was authorized and no trade was made.

## Yostocks, code at `5cf6988af1f429615ef27e3ac70e63eca22cbbf3`

The public [buyer `scan()`](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/apps/agent/yo.mjs#L94-L105) requests USDT-to-stock quotes for several representations and picks the lowest safe per-share price. Its [seller `scanSell()`](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/apps/agent/yo.mjs#L122-L143) first reads wallet balances, filters to a positive holding and rejects the request if none exists. It then asks for a stock-to-USDT quote. The [Telegram buy card](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/apps/bot/ui.mjs#L243-L261) displays the buy result and a confirm action; the [sell card](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/apps/bot/ui.mjs#L265-L276) displays the sale amount in a later flow. This reviewed code path does not give an inverse exit quote for an unowned stock before the buy decision.

This is a **file-level gap in the reviewed path**, not proof that no other route in the product offers it or that users demand it. Yostocks already has a strong quote guard, multiple issuers, buy and sell, and [documented mainnet receipts](https://github.com/yostocks-protocol/yostocks#mainnet-proof-bsc). Its bot wasn't invoked. The founder cannot use a Binance exchange account, while [Yostocks' README](https://github.com/yostocks-protocol/yostocks#try-it) says trade access is linked through Binance Agentic Wallet; we haven't checked whether a different wallet route exists.

## PancakeSwap Stocks, live unauthenticated browser

A headless Chrome visit to [PancakeSwap Stocks](https://pancakeswap.finance/stocks) returned HTTP 200. Its NVIDIA table row showed **11 issuers** and a Trade button. Clicking it navigated to a stock detail page that defaulted to a Robinhood-chain URL in that session. The page showed a reference price, quote price, From/To trade panel, issuer selector, slippage tolerance and Connect Wallet. Clicking the issuer selector displayed Ondo, xStocks, bStocks and other representations with `Select` actions, plus a restricted-jurisdiction confirmation. We stopped before confirming or connecting. No 5 USDC entry quote, inverse exit quote or complete cost summary was observed.

This visit proves a rich discovery and trade surface, and a jurisdiction gate in this browser flow. It **doesn't** prove PancakeSwap lacks a pre-entry exit estimate after the gate, or that the founder is eligible for the selected asset. We won't click a legal-status confirmation on the founder's behalf merely to finish a comparison.

## Current outcome

| Check | Yostocks | PancakeSwap |
|---|---|---|
| Stock and issuer discovery | Yes in public code and README | Yes in live browser |
| Entry quote for target amount | Yes in code; bot not invoked | Not reached at 5 USDC |
| Inverse exit before any holding | Absent from reviewed `scan()` and blocked by positive-balance guard in `scanSell()` | Unverified behind jurisdiction and wallet flow |
| Total cost and future execution | Unverified for this task | Unverified for this task |

**Decision impact:** the exact pre-entry exit ticket has a code-level difference from Yostocks, but originality and user need remain unproved. Continue only as a bounded prototype if issuer and route access pass. Do not describe the PancakeSwap gap as confirmed. The [CEO brief](2026-10-03-market-close-ceo-brief.md) and [source method](SOURCE-METHOD.md) govern the next gate.
