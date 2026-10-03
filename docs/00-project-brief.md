# Project brief

**Date:** 2026-10-01
**Name:** to be decided
**Stage:** provisional product spec and read-only implementation
**Owner:** Dyplux

## Mission

Build one useful, working tokenized-stocks product for [BNB Hack: Tokenized Stocks Edition](https://www.bnbchain.org/en/hackathons/tokenized-stocks). It should solve a specific user task, use the required Binance Web3 API in that task and give a judge a repeatable way to see the result.

## Current constraints

- One of bStocks, Ondo or xStocks must be central. Only spot activity on BNB Smart Chain mainnet qualifies under the [track rules](https://www.bnbchain.org/en/hackathons/tokenized-stocks), checked 2026-10-01.
- A working project, public repository, deployed link or reproducible instructions, and a report about real developer experience are required at submission. The [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) calls a video of up to four minutes optional, but the [live submission form](submission/2026-10-01-live-form-audit.md) currently requires a demo video URL.
- This repository stays private during research. Bell's repository, evidence, credentials and deployment remain separate.
- No production site or DNS change is authorized for this phase.

## What success looks like

A reviewer can identify the target user and task in one sentence, run the documented workflow, see a result grounded in actual API data and understand missing or stale data. The team can show what worked and failed in the API onboarding and explain why the product differs from existing stock terminals and wallet flows.

## Open product questions

1. Which user has a repeated decision or execution problem that existing products leave unresolved?
2. Do issuer, market-status and quote differences change that person's decision for a concrete ticker and amount?
3. Does the Binance Web3 API expose enough data and a reproducible quote for the smallest useful flow?
4. What is the simplest test that would reject the leading hypothesis?

The [status](status.md) and [decision log](decisions/decision-log.md) hold the current answer. [D-017](decisions/decision-log.md) approves one provisional sell-or-borrow slice. Signed Web3 search and quote reads succeeded for temporary nonholder addresses, but an eligible holder task, defensible final sale costs and personal borrowing risk are still missing. The technical responses don't establish an actionable product or demand.
