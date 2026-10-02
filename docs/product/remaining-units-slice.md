# Conditional remaining NVDAB units

**Prepared:** 2026-10-02 23:45 UTC. **Scope:** one read-only UI increment under [D-017](../decisions/decision-log.md), using the existing balance and target-sized quote responses. No new Binance or BNB RPC call.

## Job

A holder checking a partial sale for a chosen USDT need should see how many NVDAB units would remain if that candidate size sold. The result is arithmetic on an observed BNB Chain balance and a short-lived vendor estimate. It isn't settled balance, net proceeds, allowance or execution proof.

## Display rule

Show one compact conditional line under the quote summary only when both reads refer to the same public wallet, the balance block time and local receipt are within five minutes, the target-sized estimate meets the typed USDT target before costs, and the candidate raw units don't exceed the balance in exact 18-decimal arithmetic. Include the balance block number. If the candidate exceeds the observed balance, say so instead of displaying a negative remainder. With no fresh balance, invite the optional balance read. Hide the line on input changes, quote failure or expiry. Never put the result in the main Sell card.

## Acceptance

1. A recent 1 NVDAB balance and 0.43 NVDAB candidate show 0.57 NVDAB left, explicitly conditional.
2. A zero or smaller balance than the candidate gives no negative remainder.
3. A quote and balance for different wallets or changed inputs never combine.
4. Expiry, error and stale balance remove the conditional arithmetic.
5. Local tests and synthetic browser checks cover both result orderings and mobile width without live credentials.
