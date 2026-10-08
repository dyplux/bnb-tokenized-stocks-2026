# Dated proof matrix

Checked against retained local evidence on 8 October 2026. Public rollout remains pending.

Praeva is a deterministic RWA evidence-sufficiency and authorization review immediately before a separate privileged signer.

A route can exist while authority to sign remains unproven. Covenant / StockGuard overlap exists. The demonstrated distinction is evidence sufficiency, provenance, freshness and authorization prerequisites. There's no cryptographic coupling to the signer.

## Hero assessment

| Stage | Evidence and claim | Boundary |
|---|---|---|
| PROPOSED ACTION | Observed 100 USDT NVDAB assessment in [receipt](../judge/observed-unsafe.json) | Proposed purchase, no executed trade |
| Route exists | Signed amount-specific route in [route repro](../devex/repros/2026-10-04-rwa-swap-route.md) | Route availability doesn't prove holder authority |
| Evidence checked | Catalog, quote, mandate and fixed-block multiplier in [judge packet](safety-judge-run.md) | Dated inputs, no live market claim |
| Evidence missing | Independent underlying-reference time, holder eligibility and funded passing simulation | Required prerequisites remain unresolved |
| NEED_HUMAN | Observed receipt preserves ordered reasons | First-class unresolved-evidence state; no signing permission |
| Receipt | SHA-256 of canonical receipt bytes | Integrity against a compared hash; no issuer or source authentication |
| Verify action | Download receipt and inspect [judge verification](../../JUDGE.md#verify-a-receipt) | Rehashed modifications don't prove origin without a trusted external expected hash |

The separate [observed mandate DENY](../judge/observed-mandate-deny.json) exceeds its 20 USDT mandate. [ALLOW](../judge/synthetic-safe.json) is a synthetic policy fixture. Historical receipts and kernel bytes stay unchanged.

## Separate Studio and x402 proof

| Stage | Retained source | Supported claim |
|---|---|---|
| ERC-8004 identity | [Identity](../judge/studio/identity.json) | Agent 2574, BNB Chain TESTNET, chain 97 |
| Public Agent Card | [Dated guide](agent-studio-evidence.md) | Public stable card; active backend requires separate current checks |
| Managed runtime | [Replay](../judge/studio/managed-replay.json) | Three dated managed requests, canonical receipt parity; invalid task rejected |
| x402 quote | [Settlement evidence](../judge/studio/x402-settlement.json) | One retained quote in separate mainnet payment runtime |
| EIP-3009 authorization | [Settlement evidence](../judge/studio/x402-settlement.json) | One payment authorization; no public signature material |
| ONE paid dispatch | [Settlement evidence](../judge/studio/x402-settlement.json) | One paid HTTP dispatch, no economic retry; HTTP wait timed out |
| 1 U settlement | [Settlement evidence](../judge/studio/x402-settlement.json) | One observed MAINNET transfer, separate from testnet identity |
| USD 1 provider account credit | [Provider observation](../judge/studio/provider-credit.json) | Authenticated ledger matches original transaction; key credit and usage zero |
| STOP | [Runtime boundary](../judge/studio/runtime-boundary.json) | API key allocation hasn't executed; paid inference, full recovered loop and original same-process continuation remain unproved |

Provider credit remains untouched. Later recovery needs separate authorization and dated evidence. The original runtime timed out, then exited through OOM; account reconciliation doesn't establish inference or continuation.
