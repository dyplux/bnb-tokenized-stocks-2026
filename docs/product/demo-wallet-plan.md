# Demo wallet: bounded mainnet decision

**Updated:** 2026-10-04 UTC. **State:** read-only preflight only. The dedicated BNB Chain wallet has zero USDT, zero BNB and zero allowance at the [last fixed-block read](demo-wallet-state-2026-10-04.md). No stock token has been bought, no transaction has been signed, and no approval to spend capital has been given. The wallet and ignored `.env` are separate from Set and Earn.

## Action under consideration

One spot purchase of the exact NVDAB BNB Chain contract for at most 10 USDT. NVDAB is the [best observed technical target](../submission/demo-asset-selection.md) for the quote, unsigned build and simulation path. Its issuer and user-access basis is still unknown. This action is a possible proof of the [Execution Safety Layer](safety-one-page-spec.md), not a round trip, return target or investment recommendation.

## Gate before funding

1. The founder keeps a private backup of the demo wallet under their own control. The key never enters a browser, chat, repository, DevEx record or judge packet.
2. Obtain a dated official basis for access to this bStock from the founder's jurisdiction and chosen self-custody route. The [issuer access gate](../research/2026-10-04-issuer-access-gate.md) explains why a quote doesn't establish this. If the basis cannot be verified, keep the demo read-only.
3. Confirm the 10 USDT route's minimum practical amount, exact USDT contract and decimals, approval target, estimated approval gas and swap gas. The 4 October build had a 0.5% slippage tolerance and positive minimum received, but it is dated and cannot be reused.
4. Only after the access gate passes, fund the dedicated wallet within the founder's stated approximately €10 test budget plus a separately agreed gas amount. A transfer of funds alone is not permission to trade. Funding and transfer costs are not yet measured.

## Gate before requesting approval

Run a fresh [same-wallet packet](mainnet-execution-path.md) with one policy quote, unsigned build and off-chain simulation. Require `ALLOW`, a passing simulation, a still-fresh quote, matching build and simulation fingerprints, 0.5% maximum slippage, a minimum output consistent with the quote, a bounded spender and transaction destination, sufficient exact-wallet balance and allowance, and a gas ceiling. Present the exact contract, input, minimum output, spender, transaction target, policy receipt, simulation result, expiry uncertainty, costs and recovery plan to the founder. If any field is unknown or changes, stop and regenerate the packet.

**Current result:** the 17:49 UTC read-only NVDAB packet passed the local quote/build bound checks but returned `NEED_HUMAN`; its off-chain simulation predicted `FAILED` for the unfunded wallet. It is `BLOCKED`. No signer or broadcast path is enabled. The public [judge packet](https://dyplux.github.io/bnb-tokenized-stocks-2026/) is a dated safety demonstration and cannot authorize this wallet.

## After specific human approval

An approved transaction would still need a separate bounded signer with chain 56, one exact wallet, allowlisted token contracts and spender, explicit maximum input, finite validity window, gas ceiling and nonce check. Broadcast once, then record the transaction receipt and fixed-block pre/post token and BNB balances. A revert is a failed attempt, not a fill. An exit route would be a new action with new policy, quote, simulation and approval. Never assume the token can be sold back for the input amount.
