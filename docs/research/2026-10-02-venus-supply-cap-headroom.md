# NVDAB indexed supply-cap headroom

**Observed:** 2026-10-02 00:43 UTC. **Source:** [Venus public BNB Chain markets API](https://api.venus.io/markets?chainId=56&limit=100), requested with `accept-version: next`. This is an indexed snapshot, not a fixed-block contract read or transaction simulation.

## Finding

The vNVDAB row reported `supplyCapsMantissa=1500000000000000000000`, `totalSupplyMantissa=147996050485`, `exchangeRateMantissa=10000000018731039135729946976`, and 18 underlying decimals. Under the [Venus Core `mintAllowed` formula](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol), supplied underlying raw units are `floor(vToken total supply × stored exchange rate / 10^18)`. These observed fields imply 1,479.960507622119813567 NVDAB supplied and **20.039492377880186433 NVDAB** of indexed headroom beneath the 1,500 NVDAB cap.

For the local 100 USDT target, a hypothetical 1 NVDAB deposit fits this indexed cap check; 25 NVDAB exceeds it even though the collateral-factor calculation alone suggests enough nominal borrowing power. The source code checks the supply cap in `mintAllowed`, alongside market listing and pause state. A zero Core supply cap rejects minting; it doesn't mean unlimited supply.

## Product consequence and limits

The local scenario now reports this headroom and compares the entered units with it. It doesn't mark a loan executable when the check passes. The API can lag, the cap can change, and this calculation doesn't inspect protocol pause state, a specific wallet's debt, effective E-Mode factors, market entry, an actual supply transaction or a borrow transaction. A current contract read or simulation would be needed before any action. If the cap check fails, the illustrated borrow path may be unavailable even when the nominal capacity looks large.

This is Venus third-party integration evidence, not a Binance Web3 API result. No authenticated Binance quote or holder task was observed during this check.
