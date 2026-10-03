# LiquidMesh NVDAB approval builder accepts the observed vendor

**Observed:** 2026-10-03 14:33:46.660 UTC. One signed Binance Web3 Trading API `GET /api/v1/dex/aggregator/approve-transaction`, following the [fixed protocol](2026-10-03-nvdab-approval-protocol.md). No wallet address, signature, approval or broadcast was used.

The request specified BNB Chain `56`, NVDAB `0x02fca66c1d1afb4e2a7884261eb00f63598a7436`, `approveAmount=426034167623447674` raw units and `vendor=LiquidMesh`. The amount came from an earlier 100 USDT candidate; no fresh quote was requested here.

| Response field | Observation |
|---|---|
| HTTP / business code | 200 / 0 |
| Latency | 668.385 ms |
| Returned approval entries | 1 |
| Spender | `0xB44446b0c8E56988c34f7Ff73Ae904982b5FdDA5` |
| `gasLimit` | 70,000 gas units |
| `gasPrice` | 58,045,851 wei per gas |
| Full-limit product | 4,063,209,570,000 wei, or 0.00000406320957 BNB |
| Encoded approval | `approve(address,uint256)` selector, spender and raw amount matched the response and request |

The [sanitized receipt](receipts/2026-10-03-nvdab-approval.json) preserves the selected response fields and validation flags, without calldata or authentication material. The [official Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) describes the returned gas limit as a ceiling and gas price as wei. This observation establishes that the endpoint accepts LiquidMesh and constructs the expected approval for this amount. It doesn't show an existing allowance, the wallet's BNB balance, whether approval is required for a particular holder, gas actually used, route validity after approval or final USDT proceeds. The approval estimate and earlier swap estimate were observed at different times; adding their gas products would not give a contemporaneous all-in quote.

**Decision:** update the technical cost map, but keep the NVDAB sell-or-borrow cash choice provisional under [D-033](../decisions/decision-log.md). A real holder task must read current allowance for this spender and fresh route data before displaying an actionable cash result. No transaction occurred.
