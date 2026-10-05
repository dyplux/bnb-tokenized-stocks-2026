# Evidence model: fields that must stay separate

Last verified: 2026-10-05. Scope: tokenized-equity pre-signing decisions. Canonical owner/source: [policy](../../app/rwa_policy.py), [three-part clock audit](../../experiments/EXP-RWA-010/results.json), [safety evidence](../research/2026-10-04-safety-evidence.md). Supersedes: none. Status: CURRENT.

Freshness below means that the source time and observation time must be carried independently. The current policy may escalate when the precise upstream time is absent; this table defines the evidence boundary, not a claim that every check is implemented.

| Concept | Proves | Doesn't prove | Source | Freshness / fail-closed rule |
|---|---|---|---|---|
| Token price | A token quote or mark was returned | Economic equivalence or executable fill | Signed RWA `/price` | Record observation and token time; missing value blocks price-based approval. |
| Token-price timestamp | When that token field says it updated | Age of underlying stock reference | `tokenPriceUpdatedAt` | Record verbatim; stale or absent token clock escalates. |
| Underlying reference price | A displayed reference value | Independent upstream provenance or as-of time | RWA `referencePrice`, public `stockInfo` | Preserve source; never substitute token price as independent reference. |
| Underlying-reference timestamp | Dated upstream stock price, if independently provided | Token tradability | Inspected feeds currently don't expose one | `reference_age_status=UNKNOWN` when absent; no inferred age. |
| Market/session state | Reported product or venue status | That US regular session is open | `/underlying-market`, token fields | Unknown or `offhours` never defaults to OPEN. |
| Route existence | API found an amount-specific path | Access, liquidity after signing, fill | Signed Trading `/quote` | Bind to exact input, contracts and observation; expired route escalates. |
| Route mode | Label such as SWAP or RFQ | Documented settlement semantics | Trading quote | Record observed label; ambiguity needs review. |
| Liquidity and impact | Estimated executable size/cost | Guaranteed realization | Exact-amount quote ladder | Requote at action amount; unavailable depth blocks cost claim. |
| Eligibility/access | Verified permission for this person and asset | Route quality | Issuer and user rules, exact-wallet check | Unknown access never becomes ALLOW. |
| Simulation API success | The API answered a request | Transaction would succeed | `/simulate` envelope | Inspect nested predicted result. |
| Simulation predicted result | Whether current unsigned action is predicted to pass | Future inclusion or fill | `/simulate` result | Failure blocks signing; missing/currently stale result escalates. |
| Economic multiplier/share ratio | Scaling for one representation at a block | Historic corporate-action integrity | Fixed-block RPC and issuer metadata | Bind block and contract; missing or mismatch escalates. |
| Corporate-action state | Dated split/rebase/halt event if proven | Automatic route eligibility | Issuer sources and history | Fixtures remain synthetic; absent history stays unknown. |
| Wallet mandate | User's spend and impact limits | Permission for any other wallet | User-provided limits | Breach is DENY before signer. |
| Human authorization | Approval of one reviewed action | Approval of changed calldata or later spend | Separate user gate | Must bind exact action; absence blocks mainnet spend. |
| Signature | Cryptographic authorization by a key | Broadcast or successful execution | Separate signer | Never infer from build/simulation. |
| Broadcast | Network accepted a submitted transaction | Final success or intended balances | BSC transaction hash and receipt | Require chain confirmation and post-state check. |
| Decision receipt | What policy decided on a recorded evidence bundle | Upstream truth, legal access or trade | `app/rwa_policy.py` SHA-256 | Verify canonical hash; don't call it a settlement receipt. |

The [Monday finding](../../experiments/EXP-RWA-004/monday-findings.md) measured a directional hypothesis, not an independent reference clock or profitable execution.
