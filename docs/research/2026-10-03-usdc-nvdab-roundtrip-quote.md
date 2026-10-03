# USDC to NVDAB and back, read-only quote check

**Observed:** 2026-10-03 17:36:57 to 17:36:58 UTC. **Purpose:** check whether a small demonstration could return to USDC after buying NVDAB. These were two signed Binance Web3 Trading API quote GETs using a fresh temporary address without a controlled key or balance. No approval, swap build, simulation, signature, broadcast or fill occurred. The address and quote IDs were not retained.

| Direction | Raw input | Estimated raw output | Latency | Route |
|---|---:|---:|---:|---|
| BNB Chain USDC to NVDAB | 20,000,000,000,000,000,000 USDC units | 85,213,121,232,658,697 NVDAB units | 736.071 ms | One LiquidMesh `SWAP` |
| That quoted NVDAB amount to USDC | 85,213,121,232,658,697 NVDAB units | 19,998,847,497,193,789,736 USDC units | 381.281 ms | One LiquidMesh `SWAP` |

Both responses returned HTTP 200, business code 0, `isBest=true`, 18 decimals for both tokens and `estimateGasFee=450000`. They matched USDC contract `0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d` and NVDAB contract `0x02fca66c1d1afb4e2a7884261eb00f63598a7436` on chain 56. The first response reported `tradeFee=0.02259212` USD, the second `0.02251469` USD; the [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) calls this an estimated network fee. The same reference describes output as an estimate, not settled proceeds.

The two displayed estimates imply 19.998847497193789736 USDC back from 20 USDC, an arithmetic difference of 0.001152502806210264 USDC before any separately paid gas, approvals, slippage, token-price movement or transfer cost. This is **not** a measured round-trip loss. The second quote used the first quote's estimated output as its input, with no intervening buy. Quote validity and a real wallet's eligibility were not tested. A future funded experiment needs a new current entry quote, a current exit quote, allowance and transaction simulation checks, a loss ceiling and a recovery plan. The observed route does not guarantee an exit to USDC at the same price.

**Method:** existing sanitized [quote probe](../../scripts/probe_binance_quote.py), called once in each direction. No raw API response, signed headers, wallet address or secret was saved.
