# NVDAB indexed supply-cap headroom

**Observed:** 2026-10-02 00:43 UTC. **Source:** [Venus public BNB Chain markets API](https://api.venus.io/markets?chainId=56&limit=100), requested with `accept-version: next`. This is an indexed snapshot, not a fixed-block contract read or transaction simulation.

## Finding

The vNVDAB row reported `supplyCapsMantissa=1500000000000000000000`, `totalSupplyMantissa=147996050485`, `exchangeRateMantissa=10000000018731039135729946976`, and 18 underlying decimals. Under the [Venus Core `mintAllowed` formula](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol), supplied underlying raw units are `floor(vToken total supply × stored exchange rate / 10^18)`. These observed fields imply 1,479.960507622119813567 NVDAB supplied and **20.039492377880186433 NVDAB** of indexed headroom beneath the 1,500 NVDAB cap.

For the local 100 USDT target, a hypothetical 1 NVDAB deposit fits this indexed cap check; 25 NVDAB exceeds it even though the collateral-factor calculation alone suggests enough nominal borrowing power. The source code checks the supply cap in `mintAllowed`, alongside market listing and pause state. A zero Core supply cap rejects minting; it doesn't mean unlimited supply.

## Product consequence and limits

The local scenario now reports this headroom and compares the entered units with it. It doesn't mark a loan executable when the check passes. The API can lag, the cap can change, and this calculation doesn't inspect protocol pause state, a specific wallet's debt, effective E-Mode factors, market entry, an actual supply transaction or a borrow transaction. A current contract read or simulation would be needed before any action. If the cap check fails, the illustrated borrow path may be unavailable even when the nominal capacity looks large.

## Fixed-block contract check

At BNB Chain block **125200560** (`2026-10-02T00:59:01Z`), read-only `eth_call` requests through the [official mainnet RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/) returned the following values. Chain ID was 56; the Core Unitroller, vNVDAB and underlying NVDAB addresses all had code at this block. `vNVDAB.underlying()` matched NVDAB, and `NVDAB.decimals()` returned 18.

| Contract call at block 125200560 | Raw result |
|---|---:|
| Core `supplyCaps(vNVDAB)` | `1500000000000000000000` |
| vNVDAB `totalSupply()` | `147996050485` |
| vNVDAB `exchangeRateStored()` | `10000000018731039135729946976` |

Function selectors were Keccak-256 derived from their canonical ABI signatures: `supplyCaps(address)` = `0x02c3bcbb`, `totalSupply()` = `0x18160ddd`, `exchangeRateStored()` = `0x182df0f5`. The [Venus protocol math guide](https://github.com/venusprotocol/venus-protocol-documentation/blob/main/guides/protocol-math.md) confirms the integer conversion. It yields `floor(147996050485 × 10000000018731039135729946976 / 10^18) = 1479960507622119813567` raw NVDAB supplied, leaving **20039492377880186433** raw NVDAB, or **20.039492377880186433 NVDAB**, beneath the cap. The on-chain fields matched the earlier indexed fields at these two observation times; this doesn't establish that they stay equal.

The app still presents an indexed cap snapshot, because the fixed-block check was a separate research read. A later viewer must recheck current contract state before acting. This is Venus third-party integration evidence, not a Binance Web3 API result. No authenticated Binance quote, transaction simulation, deposit, loan or holder task was observed during this check.
