# Same-cash incumbent check

**Date:** 2026-10-03 UTC. **Role:** Plus Luna, read-only; coordinator checked the cited primary sources. **Task:** compare public alternatives with an eligible NVDAB holder's need for 100 USDT, using a partial sale or a Venus loan.

## Evidence

| Alternative | Public evidence checked 2026-10-03 | Same-task coverage |
|---|---|---|
| Steward Swipe | [Pinned source route](https://github.com/zkasuran/steward-bnb/blob/a1ae5cf4153e370d16ef9dd1cd85cb116f0412ba/apps/web/app/api/use/swipe/route.ts) and [README](https://github.com/zkasuran/steward-bnb/blob/a1ae5cf4153e370d16ef9dd1cd85cb116f0412ba/README.md) | The route accepts bStock units, optional account and target health factor. It returns existing USDT borrow, liquidity and a Venus borrow plan. The reviewed route doesn't size a Binance sale to a USDT target. Runtime with a connected holder wasn't observed. |
| Portir | [Pinned buy route](https://github.com/yeheskieltame/portir/blob/761f0df0e04d9fa46f0007cf69c9558ecd434161/apps/web/app/api/buy/route.ts) and [README](https://github.com/yeheskieltame/portir) | The inspected route is buy-side. The README reports live quote/build checks and a blocked cloud buy endpoint. Neither source shows the same cash-target sale versus borrow task. No runtime execution was observed. |
| Venus | [Supply and borrow guide](https://docs-v4.venus.io/guides/supply-borrow) and [interface guide](https://docs-v4.venus.io/guides/interface) | A user can enter a supply or borrow amount and inspect borrowing limits. The documented interface doesn't join a token sale quote to a loan for the same cash target. The public app exposed a JavaScript shell without a connected wallet; the task wasn't exercised there. |
| Binance Agentic Wallet | [Official market-order reference](https://github.com/binance/binance-skills-hub/blob/main/skills/binance-web3/binance-agentic-wallet/references/market-order.md) and [wallet overview](https://developers.binance.com/en/docs/products/agentic-wallet/welcome) | The quote command takes `fromTokenQty` and returns expected swap output without executing. The reviewed reference doesn't document an inverse cash-target sizing flow or a Venus comparison. A user could still do the arithmetic across tools. |

## Finding and counterargument

The reviewed public surfaces don't show one guided comparison of a target-sized partial NVDAB sale with a Venus borrowing route for the same 100 USDT need. That's a **source-level gap**, not proof that nobody offers the task or that a user values the join. Steward is the strongest counterexample: it already covers bStock-specific borrowing and optional account context. Binance Agentic Wallet covers the sale quote. A capable user can combine those paths manually.

Our prototype shows an indicative same-target sale estimate beside an isolated Venus market scenario, but it doesn't yet show net sale proceeds or personal post-action borrowing risk. No consenting holder has used it, so its ability to change an actual choice remains unknown. The existing [Steward check](../../research/2026-10-02-steward-swipe-route-check.md) already stated this distinction; this pass broadened the same-task check across four alternatives.

## Recommendation

Keep D-017 provisional only until the 4 October checkpoint. Ask an eligible, consenting holder to attempt the 100 USDT choice in an existing venue, Venus or Steward, and this prototype. If that observation doesn't show a defensible decision gain, or if final costs and personal risk can't be represented safely in time, retire or narrow the cash-choice claim. Don't add a new feature solely because a competitor's documentation omits it.

**Limits:** no wallet connection, user session, live competitor transaction, clone, paid API call or local code change. The Plus CLI didn't expose a reliable account email or remaining quota. Public documentation and inspected routes can lag deployed products.
