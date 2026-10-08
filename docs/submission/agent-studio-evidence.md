# Praeva by Dyplux: Agent Studio evidence

**Evidence date: 7 and 8 October 2026.** This page presents a fixed dated replay, testnet identity and one bounded mainnet credit-payment proof.

## Start with the assessment

Open the [console](https://praeva.dyplux.com/console/) and select **Observed NEED_HUMAN**. The NVDAB case returns `NEED_HUMAN`, five ordered reason codes, policy `0.6.0` and receipt `63c918049dc88ab90faef38f9b749be3993884989ec38bb253f5c2b887ae54db`. Its input evidence is dated 4 October. Three remote calls to the managed endpoint on 7 October returned this same receipt.

**Observed DENY** shows a historical SPYon capture. **Synthetic ALLOW** is a policy test. Every preset keeps its origin visible. The console inspects captured assessments without requesting fresh market data.

## Follow the compact proof route

1. **Identity:** ERC-8004 Agent ID **2574**, BNB Chain testnet, chain **97**. [Registration transaction](https://testnet.bscscan.com/tx/0x725975968a68bc3af35d2958b645add79477ff66e9d643e99c7f92a62fddaf6b), [sanitized identity facts](../judge/studio/identity.json).
2. **Stable card:** [agent.praeva.dyplux.com](https://agent.praeva.dyplux.com/.well-known/agent-card.json). The card identifies the active replay backend and request authentication. Managed requests currently require OAuth; no credential is embedded here.
3. **Managed runtime:** [Dated three-request proof](../judge/studio/managed-replay.json). All three canonical requests matched the local receipt. An invalid task returned `TASK_NOT_ALLOWLISTED`; commerce was disabled. The trial expires **9 October 2026, 18:48:44 UTC**. A separate VPS fallback has its own backend label and parity evidence. Verify the actual switch and active card through judging.
4. **x402 settlement:** [Mainnet transaction](https://bscscan.com/tx/0xb0344256c2807a7ce5d888738048bf74d326bd816b007f6df0a06004506b415b), [sanitized one-shot evidence](../judge/studio/x402-settlement.json). The runtime discovered low credit, obtained one quote, created one EIP-3009 signature and sent one paid HTTP dispatch. Exactly **1 U** settled to the reviewed recipient. No economic retry occurred.
5. **Provider credit:** [Dated provider observation](../judge/studio/provider-credit.json). Authenticated account state reported **USD 1**. Its deposit ledger matches the original transaction, chain, U token, B383 sender, USD 1 and onchain Transfer log index **306**, status `credited`. Account authentication is required to refresh this observation; private identifiers and key hashes are excluded.
6. **Limits and cleanup:** [Runtime boundary](../judge/studio/runtime-boundary.json). API key credit and usage remain zero. Allocation hasn't occurred. Paid inference, paid explanation, original same-process continuity and the complete self-funding loop aren't proven. Budget and renewal are OFF; payment-capable containers were stopped and VPS wallet/API-key material was removed.

## Verify the receipt

Download [canonical-receipt.json](../judge/studio/canonical-receipt.json). Remove its `receipt_sha256` field, serialize the rest with sorted keys, compact separators and UTF-8, and SHA-256 hash the bytes. The expected hash is `63c918049dc88ab90faef38f9b749be3993884989ec38bb253f5c2b887ae54db`. [Public policy implementation](../../app/rwa_policy.py).

A matching receipt hash verifies canonical bytes. The source evidence, holder access and transaction execution have their own checks.

## Preserve the failure record

The existing five-second explanation deadline aborted the paid HTTP wait after dispatch. The SDK audit recorded failure and the one-shot journal remained ambiguous. Read-only reconciliation subsequently found the original authorization nonce and exact 1 U transfer in one successful transaction. No paid HTTP success receipt was captured.

A separate authentication-only observer later ran inside the original 512 MiB cgroup. The kernel OOM-killed the primary process before a post-settlement request. The two observed kernel receipts remained equal; explanation was `UNAVAILABLE`, authority `NONE`. Later provider reads established account credit, while key credit and usage remained zero. A future recovery needs separately dated evidence.

## Claim classification

| PROVEN | PARTIAL | SYNTHETIC | NOT CLAIMED |
|---|---|---|---|
| Testnet identity; dated managed replay; canonical parity; autonomous top-up initiation; exact 1 U settlement; provider account credit | Complete self-funding sequence stops before allocation and paid inference | ALLOW policy fixture | Stock-token purchase; real purchase ALLOW; paid inference/explanation; full loop; original same-process continuity; paid B402 seller; Agentic Wallet/Wallet Skills |

The [official event page](https://www.bnbchain.org/en/hackathons/tokenized-stocks) names identity, autonomous runtime and x402 self-funding in the Studio special-prize criteria. These artifacts expose the observed depth and its limits; the judges determine the award.

[Sanitized file manifest](../judge/studio/manifest.json) · [Current claims](claims-2026-10-08.md) · [Product judge guide](../../JUDGE.md)
