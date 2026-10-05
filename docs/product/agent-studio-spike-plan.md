# BNB Agent Studio: bounded spike, not a deployment claim

Last verified: 2026-10-05. Scope: optional $2,000 special after core submission gates. Canonical owner/source: [official Studio architecture](https://docs.bnbchain.org/developer-kit/bnbchain-studio/architecture/), [quickstart](https://docs.bnbchain.org/developer-kit/bnbchain-studio/quickstart/), [local package inspection](agent-studio-feasibility.md). Supersedes: none. Status: NEEDS_REVALIDATION before implementation.

**Timebox:** 6 to 10 engineering hours only after the public judge path and final DevEx are stable. No Studio special-prize claim before real remote proof.

| Gate | Required proof | Likely architecture and cost |
|---|---|---|
| Minimum credible | Genuine Studio runtime, persistent remote deployment, ERC-8004 identity, remote invocation, invocation reaches real Dyplux policy, verifiable runtime/task evidence. | Inspect emitted `@bnbagent/studio-cli` 0.0.14 scaffold; package policy in deploy image or host an authenticated read-only policy service. Local Python path on a Mac isn't deployable. |
| Strong | Same fixed intent returns identical decision, reason codes, times and receipt hash as standalone tool; unsafe/over-limit task is blocked by policy. | Pin policy version and fixtures; remote integration logs must be sanitized. |
| Prize-competitive | Consider ERC-8183 task lifecycle, product-relevant x402/B402 payment and scoped wallet controls only if real task and remote runtime justify them. | Additional identity/payment/signer audit; avoid adding rails just to display logos. |

The official managed target offers a short testnet trial and handles signing material. Use a new throwaway testnet wallet only, never the demo or campaign key. Review generated signing and storage paths, package versions and network egress. A real policy service needs authentication, rate limits and secret isolation. A deployed agent must not authorize mainnet spend by itself.

**Hard blockers:** Bun/deployment environment not yet validated; pnpm major version mismatch in local setup; no proven remote policy service or packaged Python runtime; no ERC-8004 identity; no task/payment evidence. [Earlier feasibility audit](agent-studio-feasibility.md) records the exact package inspection. **Kill criterion:** if a remote invocation cannot execute the same deterministic policy with a verifiable receipt within the timebox, stop and keep the current submission without an Agent Studio claim.
