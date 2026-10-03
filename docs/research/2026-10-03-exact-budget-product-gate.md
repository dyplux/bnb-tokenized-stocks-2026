# Exact-budget stock purchase: product gate

**Checked:** 2026-10-03 UTC. **State:** provisional product hypothesis, no purchase or deployment.

## The task in one minute

A person has **5 USDC in a self-custodial BNB Chain wallet** and wants a small Apple exposure while the US stock market is closed. They need to know which tokenized representation has a route for that exact wallet asset and amount, why other routes fail, what is still missing from the cost, and what action they could take next. They don't need a promise of profit.

The first screen would ask for a stock and an amount already held in the wallet. Its result would show one of four concrete states for each representation: quote returned, no vendor liquidity, payment pair unsupported, or below minimum. A quote would remain an estimate; an issuer-access notice would remain unresolved until the applicable route and user location are checked. The product must not recommend a token or ask for a signature when access, gas or cost is unknown.

```text
Apple exposure                        Wallet input: 5 USDC

AAPLx     No vendor route at this size and time
AAPLon    This USDC pair is unsupported
AAPLB     Quote returned; issuer access and final cost unverified

If you prefer AAPLon: 5 USDT was below its observed minimum;
10 USDT returned a quote. That doesn't price the USDC to USDT conversion.

Next action: inspect the permitted issuer route and total cost before funding.
```

Those rows describe the **3 October API observation**, not a live or personalized recommendation. They cannot be cached as a current quote.

## Evidence, substitutes and limits

Eight signed, read-only Binance Web3 GETs between 22:38 and 22:46 UTC are logged in the [AAPL route check](2026-10-03-aapl-three-representation-route-check.md). For 5 USDC, AAPLx returned business code `40374`, AAPLon `40368` and AAPLB one SWAP estimate. AAPLon returned `40375` for 5 USDT and one quote for 10 USDT. No trade, wallet balance, complete fee or participant eligibility was checked. The [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes the quote output and gas figures as estimates.

The [Yostocks README](https://github.com/yostocks-protocol/yostocks) documents `/buy NVDA 5` with USDT, scans representations and guards bad quotes. Its [reviewed buy code](https://github.com/yostocks-protocol/yostocks/blob/5cf6988af1f429615ef27e3ac70e63eca22cbbf3/apps/agent/yo.mjs#L94-L105) already solves much of issuer choice. The [PARALLAX README](https://github.com/rishu4436/parallax) describes a USDT-funded desk that quotes every wrapper, simulates swaps and offers an Agent Studio surface. Both are serious substitutes. Their public descriptions don't establish an exact 5 USDC explanation of the three failure states above. That absence is a narrow documentation observation, not a claim that their live products cannot solve the task. [PancakeSwap Stocks](https://pancakeswap.finance/stocks) has stock, issuer and trading screens; our unauthenticated browser review stopped at a jurisdiction confirmation, so its exact-size behavior is unverified.

The [issuer access map](2026-10-03-issuer-access-by-route.md) leaves the founder's personal bStock, Ondo and xStock route eligibility unknown. A route response cannot answer that question. [xStocks' legal overview](https://docs.xstocks.fi/docs/product-legal-overview) describes EU/EEA distribution through licensed third parties, not a blanket authorization for this app. This limits a consumer buy flow, especially one that would rank an AAPLB quote as the answer.

## CEO decision and kill conditions

The old **Exit Check** only adds an inverse quote before purchase. It ran locally three times, but it didn't establish a complete cost or an action changed. PARALLAX and Yostocks already cover much of the surrounding trade task. Retire Exit Check as the submission product; keep its read-only implementation as a research tool.

Advance the exact-budget task to **one-page product specification**, with an explicit access and execution gate before any buy button. It may be a stronger task because the same 5 USDC request produced three distinct, actionable API states. The evidence is still thin: it is one provider, one stock and one amount, with no independent user session.

Stop or redesign this hypothesis if any of the following is true:

1. An incumbent already explains the same exact-budget failure and next action at equal clarity in a usable flow.
2. No selected issuer route can be shown lawfully and technically to an eligible judge or founder.
3. Conversion, approval or gas costs make the small purchase non-executable or opaque, with no useful decision left to present.
4. The interface can only say “a quote exists” without a defensible next action.

The next bounded work is a spec and static screen review, then an access and cost check for one route. No new video, transaction, public site, funding or form submission follows from this document.
