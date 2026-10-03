# Same-cash quote versus swap minimum

**Observed:** 2026-10-03 about 01:53 UTC. **Task:** an illustrative 1 NVDAB holding and 100 USDT target. This was a read-only technical probe tied to a fresh temporary nonholder address. No wallet key, approval, signature, simulation, broadcast or fill was involved.

## Bounded method

The existing local signing helper made exactly four signed GETs with the ignored project credential: one exact NVDA/bStock RWA identity search, one 1 NVDAB probe quote, one calculated target-sized quote, and one `/api/v1/dex/aggregator/swap` build for the candidate and its quote ID. The quote ID and address stayed in memory. Before the build, the script required one LiquidMesh `SWAP` route on chain 56 with the pinned NVDAB and USDT contracts, 18-decimal metadata and exact raw input. The build's sender and quoted input/output were checked against that route. No raw response, calldata, signed URL, header, quote ID or address was retained.

All four calls returned HTTP 200 and Binance business code 0. Their measured latencies were 813.703 ms for identity search, 305.664 ms for the probe, 300.214 ms for the candidate quote and 333.093 ms for the build.

| Same request | Observed value |
|---|---:|
| Candidate sale | 0.426034167623447674 NVDAB |
| Quoted output | 100.000443760010104468 USDT, above the 100 USDT target before costs |
| Built minimum at 0.5% slippage | 99.500441541210053945 USDT, below the target |
| Built transaction gas limit and gas price | 450,000 gas; 57,752,130 wei per gas |
| Full-limit gas multiplication | 0.0000259884585 BNB if all gas were used at that price |
| Quoted `tradeFee` | 0.02249402 USD, estimated network fee |

The [Binance Trading API reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api) defines `toTokenAmount` as an estimated buy-token amount and `tx.minReceiveAmount` as a minimum at the selected slippage. This one observed candidate clears the typed cash target as an estimate, while the built transaction's minimum doesn't. Neither figure establishes a fill or net proceeds. The temporary address had no verified holdings, signer, approval, BNB gas balance or eligibility. Approval cost and final gas used remain unknown.

## Decision impact

The app's present target check compares the quote estimate with 100 USDT **before costs** and doesn't call `/swap`. That statement is arithmetically true for this response, but it isn't an execution-safe target verdict. The UI must say clearly that the transaction minimum may be below the target. The 4 October holder, cost and personal-risk gate remains open. A future actionable cash-target algorithm would need an explicit user slippage choice, a fresh built minimum, allowance and cost treatment, and another product decision; this probe doesn't authorize such a feature.
