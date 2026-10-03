# Binance DeFi positions coverage for a public NVDAB collateral account

**Observed:** 2026-10-03 UTC. Read-only. No wallet connection, approval, transaction, order or participant contact. No account address, raw response, key or signature was saved.

## Source and method

The [Binance DeFi Positions reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/defi-data), checked 2026-10-03, documents signed `POST /api/v1/defi/data/position/list` with up to three addresses and an optional chain filter. It groups positions by protocol, pool and token role, including `supply` and `borrow`. Its server timestamp is not a BNB block number.

Two bounded probes each made one signed holder-ranking GET for vNVDAB, inspected at most the first 15 ranked addresses against one pinned BNB block, then made one signed DeFi Positions POST for the first account with Core vNVDAB entered and positive stored vUSDT debt. Ranking and account reads used the methods in the [holder overlap probe](2026-10-03-nvdab-holder-debt-overlap.md). The requests sent one public address and chain `56` to Binance. The address and position amounts were handled in memory only.

## Results

| Probe | Fixed BNB block used to select the account | Signed GET | Signed POST | Sanitized response |
|---|---:|---|---|---|
| First | 125419030 | HTTP 200, business code 0 | HTTP 200, business code 0; 433.847 ms | One address row. Protocol list included Venus and PancakeSwap. USDT appeared in a borrow token group. The first parser checked only the vNVDAB receipt token in supply and therefore couldn't answer whether the underlying NVDAB was represented. |
| Second | 125419107 | HTTP 200, business code 0 | HTTP 200, business code 0; latency not retained | The Venus protocol response contained a `Lending` pool, NVDAB in a `supply` token group and USDT in a `borrow` token group. The vNVDAB receipt token wasn't found in the supply groups. The probe didn't retain whether both tokens belonged to the same pool or position. |

One initial local script failed on an import before any API request. The corrected probes made four signed calls in total. No API business error or rate limit was observed in these four calls.

## Interpretation

This establishes live Binance DeFi Positions coverage of NVDAB supply and USDT borrow roles under Venus for a selected public account. It also shows that a parser looking only for the vToken receipt address misses the underlying supply token in this response.

The response wasn't reconciled to a particular Venus Core pool contract, block or exact amount. The two probes didn't retain addresses, so they aren't asserted to be the same account. The API response supplies no post-deposit or post-borrow forecast. It doesn't prove that NVDAB alone backs the USDT debt, that an eligible person wants a cash comparison, or that the app can show a safe personal loan. [D-033](../decisions/decision-log.md) remains open.
