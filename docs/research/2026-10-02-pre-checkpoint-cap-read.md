# NVDAB Core cap before the product checkpoint

**Captured:** 2026-10-02 23:01:56 UTC. **BNB block:** [125376873](https://bscscan.com/block/125376873), timestamp 23:01:56 UTC. This is a public market and contract read, not a Binance Web3 API call or a holder transaction.

Using the repository's `app/server.py`, I fetched the [Venus public markets API](https://api.venus.io/markets?chainId=56&limit=100) with the `next` response version, calculated the isolated scenario for 1 NVDAB and a 100 USDT target, then attached the same-block Core cap read from the [BNB Chain public RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/). The contract reader checks chain 56, contract code and the vNVDAB underlying before calculating headroom from `supplyCaps`, `totalSupply` and `exchangeRateStored`.

| Field | Observed result |
|---|---:|
| Contract cap status | verified |
| Contract headroom | 11.416397058476516341 NVDAB |
| Typed 1 NVDAB within headroom | yes |
| Isolated collateral-only minimum for 100 USDT | 0.711990811891640418 NVDAB |
| Minimum within headroom | yes |
| Indexed USDT pool cash check | target feasible |

The first local invocation passed strings to `build_scenario`, which expects `Decimal`, and stopped with a Python `TypeError` before any scenario result. Repeating the read with `Decimal('1')` and `Decimal('100')` produced the values above. No signed Binance call followed. This was a caller mistake, not a Venus or BNB RPC failure.

**Interpretation:** the 1 NVDAB controlled example still passes this supply-cap precondition at this block. Headroom was about 11.416397078470495107 NVDAB in an earlier read; the small difference has not been attributed to a specific transaction. Neither cap room nor the isolated minimum proves that a real holder can deposit, borrow safely or execute a sale. The [4 October product checkpoint](../decisions/decision-log.md) still needs a same-task holder observation and an account-safe economic comparison.
