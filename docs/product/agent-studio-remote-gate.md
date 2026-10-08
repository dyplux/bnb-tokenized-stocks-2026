# EXP-STUDIO-002: minimum credible remote gate

**Historical record, 6 October 2026.** The original content below retains its dated local/plan scope. For current integration evidence, use the [7/8 October Studio proof](../submission/agent-studio-evidence.md) and [current claims](../submission/claims-2026-10-08.md). Those establish a dated managed replay and testnet identity; one autonomous x402 settlement and provider account credit are separate facts. Paid inference/full loop and stock-token execution remain unclaimed.


**Prepared:** 2026-10-06. **State:** plan only. No account, wallet, credential, runtime, identity, payment or on-chain action is authorized by this document.

## Target proof

One persistent remote BNB Agent Studio runtime receives a real remote task, invokes the packaged Praeva deterministic policy, and returns a verifiable receipt. Its live endpoint is tied to an ERC-8004 identity. The same fixed input must retain decision, ordered reason codes, evidence timestamps, policy version and receipt hash parity with the standalone policy. This is separate from any mainnet tokenized-stock trade.

The current scaffold's A2A task face only exposes `negotiate` and `notify_funded`. The local parity harness mocked a funded ERC-8183 job. A remote `notify_funded` call would require a real on-chain job, even at a zero-dollar seller price. The shortest candidate for this minimum gate is a bounded, **read-only `evaluate` A2A skill** backed by the same `runWork` adapter. That skill must be implemented and checked locally before any external step. If Studio's runtime cannot serve it safely, the alternative is a real testnet ERC-8183 job, which needs separate on-chain authorization. Neither path has remote proof today.

## Shortest safe route

1. Build the [EXP-STUDIO-001 container](agent-studio-local-feasibility.md) locally with a working Docker daemon. Confirm the image includes Python and the pinned policy hash; exercise the emitted task path without a wallet or public ingress. If image parity fails, stop.
2. Implement a bounded read-only A2A `evaluate` skill in the isolated Studio branch and verify the same receipt through that transport locally. Do not use an LLM to change a policy decision. If a read-only skill proves impossible, record the real ERC-8183 testnet job as a separate authorization gate.
3. Freeze runtime configuration: testnet only, no LLM execution authority, no auto-topup, bounded task schema, approved outbound hosts, authenticated ingress, durable deliverable storage, bounded logs and rate limits. Review the Studio signing and secret injection path against the [security guide](https://docs.bnbchain.org/developer-kit/bnbchain-studio/security/).
4. **Authorization boundary:** before connecting a cloud account, creating or importing a Studio wallet, provisioning secrets, deploying, registering ERC-8004, activating commerce, making a payment or transacting, present the founder with the action, reason, cost, security risk, reversibility and expected proof. Stop until that specific action is authorized.
5. If authorized later, deploy a testnet runtime, record the immutable image and policy version, register its ERC-8004 endpoint, invoke one allowlisted task remotely and verify the returned receipt hash against the standalone tool. Record task ID, runtime URL, identity ID and dated proof without publishing private account or key material.
6. Revoke or shut down any test resources as agreed. Only after the remote proof exists may submission copy mention a Studio integration. Do not add x402/B402 or a broader autonomous execution loop to this minimum gate.

| External action requiring approval | Why | Cost to quote before approval | Security risk | Reversibility | Expected proof |
|---|---|---|---|---|---|
| Connect a cloud account and deploy the AgentCore image | Persistent remote Studio runtime | Provider build, compute, storage and network charges depend on account and region; obtain a capped estimate first | Cloud permissions and public ingress | Runtime can be deleted; logs and bills may persist | Dated remote health and image digest |
| Create or import a dedicated testnet Studio wallet and store runtime secrets | Studio scaffold currently initializes a wallet even with commerce disabled | No mainnet capital planned; possible setup or provider charges need checking | Credential exposure and signer scope | Secrets can be revoked; on-chain address history persists | Scoped wallet and secret-handling audit without exposing key material |
| Register an ERC-8004 identity | Tie a live endpoint to an on-chain identity | Testnet gas or sponsor availability must be checked | Public ownership and endpoint linkage | Metadata may be updated; registration history persists | Registry ID, chain, owner and resolvable endpoint |
| Invoke a real remote task | Prove the policy runs through Studio and returns a receipt | Read-only `evaluate` could avoid a job payment; fallback ERC-8183 testnet job has transaction cost even at zero seller price | Task abuse, replay and accidental signer action | Read-only invocation is repeatable; on-chain job history persists | Task ID, dated response, canonical receipt hash and standalone parity |
| Enable ERC-8183 or x402/B402, if later justified | Needed only if the chosen task path requires commerce | Separate fee and funding estimate | Payment authorization and replay | Can disable future use; past payments remain | Real lifecycle evidence, never a mock |

## Current estimate and stop rule

The local spike estimated **8 to 16 additional engineering hours** after access and authorization for the minimum remote proof. The estimate is uncertain because image build, cloud setup, storage and identity have not been exercised. Stop if safe remote policy parity cannot be shown within the remaining submission window or if this work threatens the main Tokenized Stocks entry. Local parity alone doesn't qualify for a public Agent Studio claim.
