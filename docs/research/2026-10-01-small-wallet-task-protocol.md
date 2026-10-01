# Small-wallet task protocol

**Prepared:** 2026-10-01
**Purpose:** decide whether an eligible person with stablecoins on BNB Chain has a stock task that an existing product leaves materially worse, and whether Binance Web3 API data can change the action. This is a protocol, not an observed result.

## One session, one decision

1. Ask the participant to choose a stock exposure they would consider with their own BNB Chain funds. Record why, the amount they would risk, their jurisdiction and eligibility only as a yes/no confirmation, and whether this action matters outside regular US cash-market hours. Don't prompt them to trade or collect identity documents.
2. Ask them to use their usual venue up to its final review screen. Record the time in UTC, token contract and issuer, side, input amount, visible quote, output amount, fee, expiry, availability or failure, and what they would do next. A hypothetical order is enough; don't ask for a signature or trade.
3. Repeat the same task and amount in one relevant incumbent flow when the participant can legally access it. If they can't access Binance Spot or Ondo direct, record that as a constraint, not a product advantage. An alternative BNB Chain wallet or DEX can be the comparator.
4. With their permission and a complete local Web3 API credential, obtain one read-only Binance RFQ bound to the permitted public wallet. The [probe](quote-probe.md) records a redacted result. Never save a wallet key, user identity or full API payload. Don't use a CEX book price as an executable on-chain alternative.
5. Ask one neutral follow-up: "What would you do with this result, and what information would change that decision?" Record the answer verbatim only if the participant agrees. Separate the participant's words from our interpretation.

## Decision record

| Field | Record |
|---|---|
| UTC start and end | pending |
| Participant consent and eligibility confirmed | pending |
| Asset, issuer, contract, side, exact amount | pending |
| Existing venue and observed steps | pending |
| Existing quote or error, with timestamp | pending |
| Binance Web3 RFQ and latency | pending |
| All-in cost comparison in the same units | pending |
| Participant's intended next action | pending |
| Action our product would change | pending |
| Missing evidence and alternative explanation | pending |

## Gate

Advance one idea to a one-page spec only if the participant has a concrete task, the existing flow leaves a meaningful cost or action unresolved, the Web3 integration can resolve it with real data, and the result can be demoed before 2026-10-11 12:00 UTC. A route estimate alone, an assumed profit, an unavailable venue in a restricted jurisdiction or a longer explanation of the same quote won't pass. A single session is a task observation, not a demand estimate. If no qualifying case appears, document the failure and pick another evidenced problem within the event scope.

BNB Agent Studio remains out of this session. Revisit it only for an autonomous task with a clear user and outcome beyond an expiring quote.
