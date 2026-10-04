# Judge demo narrative, maximum four minutes

**Prepared:** 2026-10-04 UTC. **Length:** 358 spoken words, about 3 minutes at 120 words per minute, leaving up to one minute for screen transitions. This is a script and screen order, not a rendered video or a mainnet execution claim. The [60-second film](safety-judge-video-qa.md) combines an 18:28 UTC live local read-only capture with a separate 19:56 UTC dated replay.

## 0:00 to 0:30, one action

**Screen:** the public [judge page](https://dyplux.github.io/bnb-tokenized-stocks-2026/), with the proposed NVDAB purchase visible.

**Narration:** "A tokenized stock can show a route while the exchange behind the underlying share is closed. The route answers one question: can this swap be quoted right now? It doesn't tell an agent whether the stock reference is fresh, whether this buyer may hold the token, or whether the proposed action fits the buyer's limit. Dyplux checks those conditions before a signature."

## 0:30 to 1:25, the observed uncertainty

**Screen:** select the observed `NEED_HUMAN` case. Show the contract, market state, token clock, independent reference clock, route and reason codes. Download the receipt.

**Narration:** "This is a dated NVDAB review from 4 October. Signed Binance Web3 RWA and Trading calls identified the token and returned a route. A fixed-block BNB Chain read matched its current multiplier. The response also left the underlying-stock reference time unverified. The market-status field didn't establish a regular session, and neither the route nor this read-only check verified holder eligibility or a funded simulation. The policy returned NEED_HUMAN. Each reason and source hash is in the receipt."

## 1:25 to 2:05, the observed hard stop

**Screen:** select the 19:56 UTC observed `DENY` case. Highlight 100 USDT requested, 20 USDT mandate, `MANDATE_LIMIT_EXCEEDED`, and the quoted route.

**Narration:** "Here's a second live read-only request. The user proposed 100 USDT and set a 20 USDT spending limit. Binance Web3 returned a route. Dyplux still denied the action because the limit was exceeded. This isn't a model deciding whether a trade feels safe. A deterministic rule stopped it, and the receipt preserves the evidence and the exact rule."

## 2:05 to 2:45, what the code does

**Screen:** README quick start, one local screen capture, policy file and sanitized DevEx evidence links.

**Narration:** "A reviewer can run the same screen locally with their own Binance Web3 API credentials. The public page holds no API key. The local service accepts one asset and one mandate, fetches signed market and route data, checks the on-chain multiplier for bStocks, then returns ALLOW, DENY or NEED_HUMAN. The collector independently samples 40 BNB Chain contracts every five minutes. At the 19:35 UTC 4 October cut, our DevEx log contained 611 calls, including 516 signed Binance Web3 calls. The logs keep errors and documentation gaps alongside successful responses."

## 2:45 to 3:20, limits and next action

**Screen:** the synthetic `ALLOW` fixture label, blocker board and status. End on the two observed decisions.

**Narration:** "The green ALLOW example is a labelled test fixture. It shows the policy branch, not a completed purchase. The demo wallet's unfunded simulation predicted failure, and no transaction was signed or broadcast. A real purchase needs verified access, a funded passing simulation, route-target review and approval for that exact transaction. Monday's preregistered market-open comparison may add an off-hours finding. The current product gives an agent a dated reason to stop before signing."

## Evidence and edit boundary

- The two observed decisions are [dated receipt files](../judge/observed-unsafe.json) and [mandate denial](../judge/observed-mandate-deny.json). The green branch is [synthetic](../judge/synthetic-safe.json).
- The 611-call cutoff is [fixed at 19:35 UTC](../devex/2026-10-04-metrics.json); do not present it as a current total when recording later.
- If Monday adds an off-hours finding, replace only the final two sentences of the last narration block. Do not rewrite the product problem or change the frozen [Monday protocol](../../experiments/EXP-RWA-004/monday-open-protocol.md).
- If no capital action is approved, keep the no-trade sentence. Never show a synthetic receipt or off-chain simulation as a fill.
