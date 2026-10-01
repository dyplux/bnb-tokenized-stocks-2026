# Venus bStock collateral oracle check, 1 October 2026

## Product question

Could a persistent agent help someone borrowing against a bStock on BNB Chain by showing a difference between the price used for borrow power and the price used for liquidation? This is a research test, not an approved product or proof that a borrower has encountered a problem.

## Documentary basis

The [Venus DeviationBoundedOracle guide](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/technical-reference/reference-technical-articles/deviation-bounded-oracle.md), read on 1 October, says Protection Mode can bound the collateral price on the borrow-power path while the liquidation path continues to use the ResilientOracle spot price. The [Venus oracle configuration page](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/risk/resilient-price-oracle.md) lists NVDAB, SKHYB and SPCXB with a 16.67% deviation trigger, but warns that the table is a snapshot. The [official deployment list](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/deployed-contracts/oracles.md) identifies the BNB mainnet ResilientOracle and DeviationBoundedOracle. The [Venus market API documentation](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/services/api.md) documents unauthenticated indexed market data.

## Read-only observation

At 17:54 UTC, `GET https://api.venus.io/markets?chainId=56&limit=100` returned the following indexed Core markets. `supplierCount` counts market-level suppliers and cannot be summed into unique people. `totalSupplyUnderlyingCents` is the API's indexed USD estimate, not audited collateral or debt attribution.

| Market | Indexed supply USD | Market suppliers | Collateral factor | Liquidation threshold | Borrowing this bStock |
|---|---:|---:|---:|---:|---|
| vNVDAB | 341,943.84 | 26 | 60% | 70% | disabled |
| vSKHYB | 62,699.96 | 16 | 50% | 65% | disabled |
| vSPCXB | 210,390.37 | 40 | 50% | 65% | disabled |
| vTSLAB | 42,982.29 | 19 | 60% | 70% | disabled |

These four markets total about $658,016.46 in indexed supply and 101 **market supplier records**, with overlap possible. The API says each can be collateral; it does not say how many suppliers also borrowed another asset. Borrowing the bStock itself is disabled, which does not prevent borrowing a supported stablecoin against it.

At 18:01:01 UTC, read-only `eth_call` requests to `https://bsc-dataseed.binance.org/` fixed BNB block **125144831**. The Core Comptroller `0xfD36E2c2a6789Db23113685031d7F16329158384` returned ResilientOracle `0x6592b5DE802159F3E74B2486b091D11a8256ab8A` from `oracle()` and DeviationBoundedOracle `0xc79Cb7efEBd121DC4B39eA141C214606595D665A` from `deviationBoundedOracle()`. This resolves the apparent ambiguity that `oracle()` alone created.

For each underlying, `assetProtectionConfig(address)` on the DeviationBoundedOracle returned `isBoundedPricingEnabled=true`, `currentlyUsingProtectedPrice=false`, `lastProtectionTriggeredAt=0`, `triggerThreshold=0.1667`, `resetThreshold=0.05`, and a 3,600-second cooldown. `getBoundedPricesView(vToken)` returned the same two numbers as the ResilientOracle `getUnderlyingPrice(vToken)` at that block:

| Market | Spot USD | Bounded collateral USD | Bounded debt USD | Active |
|---|---:|---:|---:|---|
| vNVDAB | 230.8251696741065 | 230.8251696741065 | 230.8251696741065 | no |
| vSKHYB | 190.1944157487037 | 190.1944157487037 | 190.1944157487037 | no |
| vSPCXB | 150.7770581250122 | 150.7770581250122 | 150.7770581250122 | no |
| vTSLAB | 357.6302333382500 | 357.6302333382500 | 357.6302333382500 | no |

Token prices above divide the returned 18-decimal mantissas by `1e18`. The live configuration is more authoritative than the documentation snapshot. A zero `lastProtectionTriggeredAt` in the current contract state does not establish that no borrower has ever faced an oracle issue on Venus or another lending protocol.

## Decision impact and limits

At the observed block, there was **no divergence** for the four bStock markets and no identified affected borrower. A generic collateral alert would duplicate existing portfolio health interfaces without a demonstrated trigger. A buyer for an autonomous paid Agent Studio service is also missing. Keep this as a possible future recovery state if protection activates and a consenting borrower's task shows an incumbent gap. Do not build a liquidation agent or imply that an upcoming liquidation can be prevented from these observations.

This check used Venus data and BNB public RPC, not Binance Web3 API. It does not satisfy the hackathon integration gate. No account was contacted, no trade or borrow was made, and no address-level position was stored.
