# BNB Agent Studio feasibility for the safety core

**Checked:** 2026-10-04. **State:** official path mapped; no package installed, agent deployed, identity registered, paid job, or special-prize claim.

## Task that could warrant an agent

A buyer submits one proposed tokenized-equity action and receives a dated, machine-readable `ALLOW`, `DENY` or `NEED_HUMAN` receipt before signing. The buyer may use that result in a separate trading workflow. The existing [read-only policy tool](../../scripts/safety_agent_tool.py) performs the decision work; an agent runtime would provide discovery, invocation and delivery. A seller wrapper should not invent an execution path or treat the model's text as authority.

The [official Studio architecture](https://docs.bnbchain.org/developer-kit/bnbchain-studio/architecture/) says its generated TypeScript seller core implements `runWork`, while fixed entrypoint code handles signing. A2A, MCP and x402 are optional faces around the same runtime. The [quickstart](https://docs.bnbchain.org/developer-kit/bnbchain-studio/quickstart/) lists Node 22+, Corepack/pnpm 10 and Bun 1.3+ for deployment. The managed BNB target is a **48-hour testnet trial** and requires a throwaway wallet because signing material leaves the operator's control. That target cannot serve as proof of a BNB Chain mainnet tokenized-stock execution.

## Minimum honest integration

1. Wrap the existing JSON input and policy result in Studio's `runWork` hook. Pin the policy version and preserve the full receipt and source timestamps in the deliverable. A Python subprocess bridge is a candidate, but this exact bridge has not been built or run inside Studio.
2. Use one local read-only face first. Verify that a real request yields the same policy decision and receipt hash as the standalone tool. `DENY` and `NEED_HUMAN` must not trigger a signer.
3. Only if a buyer task and runtime stability are demonstrated, add a testnet identity and a paid rail using a new throwaway wallet. Inspect generated signing, storage and budget boundaries before any deployment.
4. Keep the mainnet demo wallet, private keys and exact-wallet trade path outside the managed testnet runtime. Any later mainnet execution needs its own policy, simulation and human approval gate.

## Decision for this submission

The official Studio trial is technically plausible, but it doesn't remove the current blockers: verified issuer access, an independent reference clock, a funded passing simulation and human approval. A testnet seller that returns the policy receipt could show a genuine agent invocation; it would still be a separate demonstration from a mainnet stock trade. We won't claim the Agent Studio special from a local CLI tool or a scaffold. Reassess after the main judge path and the eligibility gate are stable.

The [official Wallet Skills overview](https://developers.binance.com/en/docs/products/wallet-skills/overview) lists a read-only tokenized-securities skill and a separate Agentic Wallet skill with write capability. Our Ondo review calls the **public endpoint documented by that read-only skill**; the skill package itself hasn't been installed or invoked. Its observed response supplied no independent stock-reference timestamp. The [Agentic Wallet installation path](https://developers.binance.com/en/docs/products/agentic-wallet/quickstart/install-agentic-wallet) requires a Binance account and MPC wallet, which the founder says they cannot use. No Agentic Wallet runtime has been activated.

## Documentation uncertainty

The current [Studio architecture](https://docs.bnbchain.org/developer-kit/bnbchain-studio/architecture/) describes TypeScript files under `app/agent/src/`. The [security page](https://docs.bnbchain.org/developer-kit/bnbchain-studio/security/) still names `app/agent/signing.py` and a keyless Service path. We cannot assume both describe the same current scaffold. Before implementing a Studio adapter, inspect the exact emitted version locally and record any mismatch with a fixture. This is an integration uncertainty, not yet a reproducible defect claim.

**4 October local readiness probe:** Node v25.8.0 is present; Corepack resolved pnpm 12.9.1; Bun isn't installed and `bag` isn't on `PATH`. The official [quickstart](https://docs.bnbchain.org/developer-kit/bnbchain-studio/quickstart/) asks for Node 22+, pnpm 10 and Bun 1.3+ for deployment. The npm registry reports `@bnbagent/studio-cli` 0.0.14 under Apache-2.0. We queried metadata only; no Studio package, skill or scaffold was installed or executed. Local pnpm does not match the documented major version, so a clean isolated scaffold is the next compatibility check, not a deploy claim.

**Narrow adapter acceptance:** feed one fixed request to the standalone [read-only policy tool](../../scripts/safety_agent_tool.py) and to Studio's emitted `runWork`. Require identical decision, reason codes, receipt hash, source times and fail-closed error behavior. Keep signing outside the tool. This is the smallest meaningful Studio integration; it remains unimplemented until the actual emitted scaffold is inspected.
