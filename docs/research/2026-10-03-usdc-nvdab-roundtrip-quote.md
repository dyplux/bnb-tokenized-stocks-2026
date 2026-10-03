# USDC to NVDAB and back, read-only quote check

**Observed:** 2026-10-03 17:36:57 to 17:36:58 UTC. **Purpose:** check whether a small demonstration could return to USDC after buying NVDAB. These were two signed Binance Web3 Trading API quote GETs using a fresh temporary address without a controlled key or balance. No approval, swap build, simulation, signature, broadcast or fill occurred. The address and quote IDs were not retained.

| Direction | Raw input | Estimated raw output | Latency | Route |
|---|---:|---:|---:|---|
| BNB Chain USDC to NVDAB | 20,000,000,000,000,000,000 USDC units | 85,213,121,232,658,697 NVDAB units | 736.071 ms | One LiquidMesh `SWAP` |
| That quoted NVDAB amount to USDC | 85,213,121,232,658,697 NVDAB units | 19,998,847,497,193,789,736 USDC units | 381.281 ms | One LiquidMesh `SWAP` |

Both responses returned HTTP 200, business code 0, `isBest=true`, 18 decimals for both tokens and `estimateGasFee=450000`. They matched USDC contract `0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d` and NVDAB contract `0x02fca66c1d1afb4e2a7884261eb00f63598a7436` on chain 56. The first response reported `tradeFee=0.02259212` USD, the second `0.02251469` USD; the [Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) calls this an estimated network fee. The same reference describes output as an estimate, not settled proceeds.

The two displayed estimates imply 19.998847497193789736 USDC back from 20 USDC, an arithmetic difference of 0.001152502806210264 USDC before any separately paid gas, approvals, slippage, token-price movement or transfer cost. This is **not** a measured round-trip loss. The second quote used the first quote's estimated output as its input, with no intervening buy. Quote validity and a real wallet's eligibility were not tested. A future funded experiment needs a new current entry quote, a current exit quote, allowance and transaction simulation checks, a loss ceiling and a recovery plan. The observed route does not guarantee an exit to USDC at the same price.

**Method:** existing sanitized [quote probe](../../scripts/probe_binance_quote.py), called once in each direction. No raw API response, signed headers, wallet address or secret was saved.

## Smaller technical check at the founder's loss ceiling

At 17:47:02 to 17:47:03 UTC on the same day, two further signed quote GETs used a new temporary nonholder address and the same pinned contracts. A 5 USDC input returned one LiquidMesh SWAP estimate of `0.021307880278873944 NVDAB` in 759.582 ms. An immediate inverse request for that estimated NVDAB amount returned one LiquidMesh SWAP estimate of `5.002414582877189283 USDC` in 327.693 ms. Both returned HTTP 200 and business code 0. Their `tradeFee` fields were `0.0214146` and `0.01863272` USD estimates; both returned `estimateGasFee=450000`.

The inverse estimate being above 5 USDC does not establish a profit or an executable arbitrage. These are separate, expiring quotes from a zero-balance address; no buy or sale locked either price, and approval, gas, slippage and any eligibility condition remain unmeasured. The check only establishes that the API exposed both directions for this smaller amount at that moment. A 5 USDC live technical trial would put the full principal at risk until exit and still would not validate the product's 100 USDT cash-choice task.
