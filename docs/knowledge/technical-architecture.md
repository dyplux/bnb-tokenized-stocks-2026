# Technical architecture and trust boundaries

Original core evidence verified: 2026-10-05. Current integration checkpoint: 2026-10-08; see the dated runtime/payment section below. Scope: shipped read-only core and bounded execution design. Canonical owner/source: [safety service](../../app/safety_service.py), [policy](../../app/rwa_policy.py), [pre-execution packet](../product/pre-execution-packet-linked-2026-10-04.json). Supersedes: none. Status: CURRENT.

1. [Safety service](../../app/safety_service.py) accepts a bounded action and collects signed Binance Web3 RWA/Trading reads. It checks route identity against chain, source/destination contracts and raw amount, and obtains a fixed-block BNB Chain multiplier read where applicable. Public addresses used for read-only quotes don't prove the caller's access.
2. [Deterministic policy](../../app/rwa_policy.py) evaluates market state, timestamp availability, ratio, route, price impact and mandate. Unknown or contradictory required evidence yields `NEED_HUMAN` or `DENY`, never an optimistic default. An LLM may submit the intent; it doesn't authorize it.
3. The policy serializes a decision receipt with sorted JSON keys and compact separators, hashes it with SHA-256, and includes the hash. This establishes integrity of the receipt bytes under the stated canonicalization, not truth of upstream claims.
4. The [agent tool](../../scripts/safety_agent_tool.py) is a local stdin/stdout adapter. [EXP-STUDIO-001](../product/agent-studio-local-feasibility.md) passed parity with a separate local Studio scaffold. Those original artifacts retain their local-only scope. A separate [7 October managed fixed-replay runtime](../submission/agent-studio-evidence.md) now has remote parity proof; no marketplace listing or stock signer is claimed.
5. The [optional pre-execution script](../../scripts/prepare_pre_execution_packet.py) obtains an exact-wallet quote, unsigned build and off-chain simulation. The observed simulation API returned a response but predicted failure for an unfunded wallet. No stock signature, broadcast or fill occurred in that 4 October packet.

The stock-assessment kernel has no private signing key. A future signer must be separate and bind chain, contract, amount, calldata, quote, simulation and policy version to the exact approved action. It must reject expiry, route change and mandate breach, and require a separate human gate for irreversible mainnet spend. See [security policy](security-wallet-policy.md).

## 8 October runtime and payment separation

The public console replays stored receipts. The stable A2A card references a dated managed fixed replay and a separately labelled VPS fallback. The managed trial has an explicit expiry; it isn't a fresh market-data endpoint. ERC-8004 Agent ID 2574 is on chain 97.

A separately reviewed one-shot mainnet credit-payment runtime initiated one quote, one EIP-3009 signature and one paid dispatch; exactly 1 U settled with no economic retry. Its deterministic stock receipt remained unchanged. Provider account credit was subsequently attributed to that transaction. API key credit/usage remain zero; allocation and paid inference haven't occurred. See the [compact dated proof](../submission/agent-studio-evidence.md).

The optional explanation has authority NONE. No model changes the stock decision, reasons, policy version, amount or signing permission. Payment capability belonged to a separate explicitly authorized executor; its spending switches and VPS secrets were removed after the run. No stock-token transaction was executed.
