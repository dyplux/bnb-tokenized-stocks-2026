# Exact-budget stock purchase assistant

**Draft:** 2026-10-03 UTC. **Gate:** D-051 approves specification only. Product, issuer route and funded demonstration remain unselected.

## User and task

A person has a small stablecoin balance in a self-custodial BNB Chain wallet, without a Binance exchange account. Outside ordinary US market hours, they choose a company and ask: **“With the asset and amount I already hold, what stock-token route can I use right now, and what do I need to do next?”** The first observed example is 5 USDC toward Apple exposure. It is an example API task, not a confirmed user interview or a funded wallet.

## Screen and action

1. The person chooses a stock, spending token and exact amount. An optional public wallet address can check token and BNB gas balances without claiming wallet ownership.
2. The app resolves current BNB Chain token identities from Binance RWA data plus a separately verified issuer list where the signed search omits a representation. It never treats a ticker match as token identity.
3. For each supported representation, one bounded Binance Web3 Trading API quote attempt returns either a fresh route estimate or a specific failure: no vendor liquidity, unsupported input pair, below minimum, or technical error.
4. The result explains the next action. Examples: “Try another payment token”, “Increase size only if you intended to spend more”, “No route from this provider now”, or “Review this quoted route's issuer access and full cost”. It never labels the highest output the best investment.
5. Before an executable route is offered, show issuer/venue access, wallet balance, approval need, estimated gas, amount due and simulation. Any unknown that prevents a safe action blocks the action. The app refreshes an expired quote before a new decision.

The read-only first slice ends at step 4. The full product requires step 5 and a separate authorized wallet execution path. A read-only slice may support a candid technical submission, but it doesn't prove a working consumer purchase.

## Proof and limits

The [3 October AAPL check](../research/2026-10-03-aapl-three-representation-route-check.md) observed, for 5 USDC, a failed AAPLx vendor route, unsupported AAPLon USDC pair and one AAPLB quote. Ondo then rejected 5 USDT as below minimum and quoted 10 USDT. Those results are dated snapshots; none establishes a fill, present route, personal eligibility or profit. The [issuer access map](../research/2026-10-03-issuer-access-by-route.md) explains why a quote can't stand in for access approval. Yostocks and PARALLAX already scan issuers for USDT-funded purchases, so the proposed distinction is the person's **actual input asset, exact amount, failure reason and next action**. A same-task PancakeSwap comparison remains incomplete.

## Acceptance criteria for the next read-only slice

1. A fresh 5 USDC AAPL request shows the exact provider response per supported token, with contract, chain, amount, receipt time and quote age. It must not replay the 3 October rows as live data.
2. A valid quote, business failure, network failure and stale response have different visible states. No failure becomes a zero price or an automatic alternative token.
3. The app identifies whether an input-token balance and BNB gas balance are known. Missing balance data produces “unknown”, not “enough”.
4. The result names one realistic next action per state, while issuer access and full cost remain explicit unresolved gates.
5. All user-facing numbers, token identities and costs come from current source fields with units and provenance. Signed credentials stay server-side; the interface never exposes them.
6. In a clean local walkthrough, a person can explain the result and why they would stop, change payment token or inspect a route, without an oral explanation from the builder. This checks comprehension only, not independent demand.

**Primary product measure:** proportion of attempted exact-budget tasks that end with a correct, understandable next action. Measure it in a dated task log rather than guessing a conversion rate. Secondary technical measures are quote success/failure classification and response time. No return or trade-performance target is claimed.

## Excluded from this slice

No purchase, approval, agent strategy, portfolio return, future resale estimate, automatic stablecoin conversion, issuer eligibility verdict or public buy button. Add one only after its user task, source and execution gate have been reviewed. The local Exit Check remains research code and its film stays internal.
