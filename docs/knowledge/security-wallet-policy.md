# Wallet and execution policy

Original core evidence verified: 2026-10-05. Current integration checkpoint: 2026-10-08; see the dated separate-execution proof below. Scope: Dyplux agent and signing boundaries. Canonical owner/source: [current execution path](../product/mainnet-execution-path.md), [policy](../../app/rwa_policy.py), [agent interface](../../scripts/safety_agent_tool.py). Supersedes: none. Status: CURRENT.

| Role | Permitted material | Boundary |
|---|---|---|
| Research agent | No wallet key | Read public data and sanitized responses only. |
| Simulation agent | Public address | Build unsigned transaction and evaluate nested simulation result. |
| Testnet executor | Scoped throwaway key, with separate task approval | Never reuse a funded production key. |
| Production executor | Capability-bound signer/service | Bind exact chain, contract, amount, calldata, quote, simulation and policy version. |
| Irreversible mainnet spend | Separate human approval until explicitly changed | No broadcast on a model's recommendation alone. |

The planner or LLM never owns private signing material. A proposed transaction must match the reviewed transaction byte-for-byte on security-relevant fields. Route availability doesn't prove individual eligibility. A successful API envelope doesn't override a failed nested simulation. Missing required evidence fails closed.

No secrets, auth headers or private account identifiers belong in Git, logs, screenshots, handoffs or receipts. The stock-assessment kernel never signs or broadcasts a purchase. Its generated read-only quote address doesn't prove a funded caller's access. [Observed mainnet blockers](../submission/real-allow-audit.md) remain explicit.

## 8 October separate execution proof

The [Studio evidence subset](../submission/agent-studio-evidence.md) contains a testnet identity registration and a separate expressly authorized mainnet EIP-3009 credit payment. Those signer roles are separate from the stock-assessment kernel and the planner/model. A one-shot control bound the payment to the reviewed chain, U token, recipient, value, nonce and validity, with one signature/dispatch and no economic retry.

The HTTP result became ambiguous after dispatch. The operator reconciled only that original nonce and exact transfer against its successful receipt. No second signature or paid dispatch followed. After the runtime failure, budget/renewal were disabled, payment-capable containers stopped and VPS wallet/API-key material removed.

Provider account credit of USD 1 is attributed to the original transaction; API key credit and usage remain zero. Any allocation or restarted inference runtime needs separate review and authority. No additional funding, payment, wallet reuse or stock purchase follows from the existing balance. Original same-process continuity remains unproven. Raw signatures, payment envelopes and private account identifiers stay outside the public subset.
