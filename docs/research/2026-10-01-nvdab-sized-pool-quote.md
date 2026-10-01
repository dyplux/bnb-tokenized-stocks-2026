# NVDAB pool size check, 1 October 2026

## Question

Would an ordinary eligible BNB Chain wallet get a materially different NVDAB execution result simply because it trades 25 rather than 2,000 USDT? This is a falsification check for a proposed amount-specific cost monitor. It is **not** a Binance Web3 API quote, transaction, or user study.

## Sources and method

- At 17:32:59 UTC, the [GeckoTerminal public pool index](https://api.geckoterminal.com/api/v2/networks/bsc/tokens/0x02fca66c1d1afb4e2a7884261eb00f63598a7436/pools) returned a PancakeSwap V3 NVDAB/USDT pool at `0x8fb4243b553ac29ba088acf00b9b7da24bd6690c`. Its index reported about $4.92 million in reserve and $8.39 million in 24-hour volume. These are indexer figures, not an executable quote.
- The [PancakeSwap V3 BSC deployment file](https://github.com/pancakeswap/pancake-v3-contracts/blob/main/deployments/bscMainnet.json) identifies QuoterV2 as `0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997`.
- Read-only `eth_call` requests to `https://bsc-dataseed.binance.org/` confirmed both token decimals are 18, `token0` is NVDAB `0x02fca66c1d1afb4e2a7884261eb00f63598a7436`, `token1` is BSC USDT `0x55d398326f99059ff775485246999027b3197955`, and `fee()` is `2500`, or 0.25% per swap.
- At 17:37:18 to 17:37:43 UTC, called QuoterV2 `quoteExactInputSingle((address,address,uint256,uint24,uint160))` through `eth_call`, using selector `0xc6a5026a`, fee `2500`, and price limit `0`. All buy and sell calls used **block 125141674**, hex `0x77582aa`. Four buys used exact USDT inputs. Each sell used the quoted NVDAB output of its matching buy as exact input. This is two independent quotes against one fixed pool state, not a sequential simulation of executed swaps.

| USDT input | Quoted NVDAB output | Quoted USDT from reverse input | Difference | Difference / input |
|---:|---:|---:|---:|---:|
| 25 | 0.10800189812764209 | 24.875145997759300 | 0.124854002240700 | 0.499416% |
| 100 | 0.43200732509995304 | 99.500460964351620 | 0.499539035648380 | 0.499539% |
| 500 | 2.16002949457797740 | 497.499024135833100 | 2.500975864166900 | 0.500195% |
| 2,000 | 8.64001101616239200 | 1,989.946887795832300 | 10.053112204167700 | 0.502656% |

The difference between the 25 and 2,000 USDT percentages is about **0.00324 percentage points**, or **0.324 basis points**. Two 0.25% pool fees account for almost all of the approximately 0.5% theoretical round-trip difference. The Quoter also returned estimated gas units, but these aren't a verified wallet transaction or a cost in USDT and are excluded from the table.

## What this changes

For this one liquid pool at this one block, sizing from 25 to 2,000 USDT barely changes the percentage quote. A consumer alert that merely says a larger order pays more price impact would add little to this task. The study cannot rule out poor execution in smaller pools, other assets or RFQ routes. It also cannot show a saving against Binance Spot, since a centralized book is not directly executable from the same self-custody wallet.

**Missing:** authenticated Binance Web3 quote for the same asset, side, amount and time; route fees and gas in consistent units; wallet restrictions and approvals; competitor walkthrough; consenting eligible participant; actual fill. No profit, arbitrage or superior route is claimed. Until a participant's task reveals a difference that an incumbent misses, the amount-specific monitor remains unapproved.
