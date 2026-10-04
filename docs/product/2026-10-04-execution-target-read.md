# NVDAB execution target, fixed-block read

**Observed:** 2026-10-04 UTC. **Scope:** public BSC RPC reads of the target in one unsigned 10 USDT to NVDAB LiquidMesh `SWAP` build. No wallet signature, approval, transaction or security audit was performed. The [public RPC fixture](../devex/fixtures/2026-10-04-nvdab-route-target-fixed-block.json) contains the exact JSON-RPC requests and responses, without wallet or API credentials. Its SHA-256 is `416f01ac7798ef41e78e89b726e90e48d937896a81a00bbf30e717c6c1047d43`.

| Fixed-block observation | Value |
|---|---|
| Chain and block | BSC 56, `0x77e86df` |
| Built `tx.to` and quote `approveTarget` | `0xB44446b0c8E56988c34f7Ff73Ae904982b5FdDA5` |
| Built calldata selector | `0xad43f73d` |
| Target runtime | 180 bytes, SHA-256 `678b647bfc7b65b4036969469d160aa275ee2b9bef20c30e124ae1c2519648f1` |
| Selector mapping key returned by `web3_sha3` | `0x7ddc1c45a5ae31800e181de98e8cb97525e9b89f99e5829d49f25a8ca4bac1d7` |
| Mapping storage value, low 20 bytes | `0xa9fa1b56f4d7bd25375c2d40b4c8e36a9509e603` |
| Mapped address runtime | 8,622 bytes, SHA-256 `924e9da536e78a9ce92f633058a62907ee5834738947432d186e02b212a0d574` |
| Standard ERC-1967 implementation, beacon and admin slots | All zero at this block |

The 180-byte target runtime is **consistent with** a selector-to-implementation dispatcher: it hashes a masked selector and a constant storage slot, reads an address, then delegates the call. The fixture proves the storage value and code present at one block. It doesn't prove who controls that mapping, whether the mapped code can change, whether the source or ABI matches a trusted release, or whether this user may hold the security. Zero [ERC-1967 slots](https://eips.ethereum.org/EIPS/eip-1967) don't rule out another dispatch or upgrade mechanism.

A 4 October read of [Sourcify's documented v2 contract lookup](https://docs.sourcify.dev/docs/api/) returned HTTP 404 with `match:null` for both addresses on chain 56. This means **no Sourcify match was returned by that lookup**, not that the contracts are globally unverified or unsafe. The indexed BscScan address page couldn't be opened from this environment, so source, ABI and deployment ownership remain unverified here.

[LiquidMesh's own documentation](https://docs.liquidmesh.io/docs/quote-api) describes quote and swap-data construction as separate stages. Its [security overview](https://docs.liquidmesh.io/docs/overview) describes token and address risk screening; it doesn't establish country-specific bStock investor eligibility. We haven't verified that the Binance gateway passes the actual wallet through every LiquidMesh screening step. A successful Binance quote is therefore neither an issuer-access decision nor a contract allowlist decision.

**Execution gate:** before approving one concrete trade, bind a fresh quote and unsigned build to the intended wallet, amount and token contracts; identify the target, spender and mapped implementation at a fresh fixed block; verify trusted contract provenance and any mutable dispatch mechanism; then require an eligible holder, sufficient balance and gas, passing simulation, `ALLOW` policy and specific human approval. A changed selector, target or mapped implementation invalidates this review. The present route remains read-only.

**RPC limit observed during reproduction:** a re-read of the earlier block `0x77e8576` from the same public endpoint returned `missing trie node` for code and storage. A new fixed-block read succeeded at `0x77e86df`. This shows the public endpoint cannot be assumed to supply arbitrary historical state; preserve fixed-block responses when collected and recheck fresh state before any action.
