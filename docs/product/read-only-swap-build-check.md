# Read-only bStock SWAP build check

**Decision context:** D-020 leaves the LiquidMesh `SWAP` route review-required. The [Binance Trading API introduction](https://web3.binance.com/en/dev-docs/products/trading-api/introduction) specifies `GET /quote` then `GET /swap` for a bStock LiquidMesh route. The [swap endpoint reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes the second GET as transaction-data construction. No wallet signature or broadcast is required for the read.

## One technical question

For one fresh NVDAB-to-USDT quote bound to a temporary address with no signer, will the documented `/swap` GET return a `SWAP` transaction payload with route and gas fields? If it rejects the request, what sanitized business code or state is observed?

## Boundaries

1. Use the existing ignored server-side Binance key pair. Make one signed quote for exactly 1 NVDAB and, only if it returns one LiquidMesh `SWAP` route and `quoteId`, make one signed `/swap` GET within the documented roughly 30-second lifetime. Use the same address, chain, token contracts and raw amount, with `slippagePercent=0.5` and no approval-transaction request. No retries.
2. Keep the temporary address, quote ID, signed URL, headers, calldata, signature material and full response in memory only. Log only UTC, latency, HTTP and business code, response mode, whether `tx` and its named gas/receive fields exist, and any error label. Never print the temporary address or quote ID.
3. Do not request approval calldata, sign a wallet transaction, submit an RFQ order, simulate, or broadcast. A constructed `tx` for a nonholder is not executable evidence or a settled sale.
4. Do not change the public app or net-proceeds claim from this check alone. Record documentation contradictions and any actual response separately. A consenting eligible holder and cost interpretation remain release gates.

**Acceptance:** one dated, sanitized observation answers whether this one technical route reached transaction construction and identifies what remains unknown. A rejected call is a valid result.

**Result:** the 2026-10-02 [sanitized live build](../research/2026-10-02-first-live-swap-build.md) returned HTTP 200/business code 0 at both steps and an unsigned `tx` payload. This passes the technical build check only; the holder and execution gates remain open.
