# Wallet and execution policy

Last verified: 2026-10-05. Scope: Dyplux agent and signing boundaries. Canonical owner/source: [current execution path](../product/mainnet-execution-path.md), [policy](../../app/rwa_policy.py), [agent interface](../../scripts/safety_agent_tool.py). Supersedes: none. Status: CURRENT.

| Role | Permitted material | Boundary |
|---|---|---|
| Research agent | No wallet key | Read public data and sanitized responses only. |
| Simulation agent | Public address | Build unsigned transaction and evaluate nested simulation result. |
| Testnet executor | Scoped throwaway key, with separate task approval | Never reuse a funded production key. |
| Production executor | Capability-bound signer/service | Bind exact chain, contract, amount, calldata, quote, simulation and policy version. |
| Irreversible mainnet spend | Separate human approval until explicitly changed | No broadcast on a model's recommendation alone. |

The planner or LLM never owns private signing material. A proposed transaction must match the reviewed transaction byte-for-byte on security-relevant fields. Route availability doesn't prove individual eligibility. A successful API envelope doesn't override a failed nested simulation. Missing required evidence fails closed.

No secrets, auth headers or private account identifiers belong in Git, logs, screenshots, handoffs or receipts. The current product never signs or broadcasts. Its generated read-only quote address is not a live funded user wallet. [Observed mainnet blockers](../submission/real-allow-audit.md) remain explicit.
