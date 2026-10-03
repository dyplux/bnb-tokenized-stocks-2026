# Venus Core current facet boundary

**Observed:** 2026-10-03 01:08 UTC, BNB Smart Chain block `125393938`. **Method:** public read-only JSON-RPC at `https://bsc-dataseed.bnbchain.org`, with no wallet signature or paid API. The Plus Sol research pass couldn't resolve its RPC host, so the coordinator repeated only bounded public reads from the main environment. No repo code or app behavior changed.

## What the deployed contract returned

The [Venus Core Diamond interface](https://docs-v4.venus.io/technical-reference/reference-core-pool/comptroller/diamond/diamond) exposes `facetAddress(bytes4)`. At the pinned block, Core Unitroller `0xfD36E2c2a6789Db23113685031d7F16329158384` returned `0x8930b02c69edd37464b50991680d306bb9b8fdbd` as the first ABI word for both `getBorrowingPower(address)` selector `0x528a174c` and `getAccountLiquidity(address)` selector `0x5ec88c79`. The second word differed (`4` and `3`); it wasn't an address. The deployed facet had **14,049 runtime bytes** at that block. Its runtime SHA-256 was `66d156eea77f5b048b7d60383ae62982726ac83e5db224724861137e9df07bc4`.

These observations refresh the earlier [fixed-block selector routing](2026-10-02-venus-deployed-risk-read.md). A code hash is an identifier for the observed bytes, not a match to the [reviewed Venus PolicyFacet v10.3.0 source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol). Verified compiler input, settings and a normalized bytecode comparison weren't available, so source parity remains unknown.

## Official source trail, checked 2026-10-03

The [Venus PolicyFacet reference](https://github.com/VenusProtocol/venus-protocol-documentation/blob/ebe979cdff722c107fc5f51cfc2f9bb9862fc701/technical-reference/reference-core-pool/comptroller/diamond/facets/policy-facet.md) names this same facet address at block `118363255` and directs readers to the [v10.3.0 source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol). The [VIP-640 BNB Chain data](https://github.com/VenusProtocol/vips/blob/9384f04bb4cff9865e583ad677a7fdb6c2bbec08/vips/vip-640/utils/data.bscmainnet.ts) records replacement of the previous PolicyFacet with `0x8930B02c69EDd37464B50991680D306Bb9B8FDBD` and includes selectors `0x528a174c` and `0x5ec88c79`. The [Venus deployment list](https://github.com/VenusProtocol/venus-protocol/blob/46afc66b1dbd61a707d0a3492b3ec21bf90fc17a/deployments/bscmainnet_addresses.json) names it `PolicyFacet`.

In the linked v10.3.0 source, `getBorrowingPower(address)` calls the internal liquidity calculation with `USE_COLLATERAL_FACTOR`, and `getAccountLiquidity(address)` calls it with `USE_LIQUIDATION_THRESHOLD`. The official trail identifies the intended source and selector routing, and the public RPC read above confirms current routing at a later block. It does not reproduce compilation or prove runtime bytecode equality. No populated-account arithmetic has been reproduced, so it doesn't approve a post-action personal forecast.

## Attempted populated-account probe

A [public transaction receipt](https://bscscan.com/tx/0xbeba4bee7d8178527895e7507fcce98b5bb6c65a4f820bb5c81ecac4c25c4705) at block `96267085` contained two logs with the Venus `Borrow` event topic. Their borrower fields were used locally for two read-only current-block ABI calls without recording the addresses. Both accounts returned `(errorCode, liquidity, shortfall) = (0, 0, 0)` for both risk methods at block `125393793`. An old borrow event doesn't prove an open position today.

Two `eth_getLogs` attempts for those two emitting markets, over 500 and 25 recent blocks, each returned RPC error `-32005 limit exceeded`. No recent populated account or independent arithmetic reproduction was obtained. The direct BscScan page was inaccessible with HTTP 403 in the research environment. No account address, raw request or response was saved in this repo.

## Decision impact

The active facet routing and nonempty code are observed. Deployed-source parity and populated-account arithmetic parity are **not proven**. [D-030](../decisions/decision-log.md) still blocks a personal post-supply or post-borrow risk forecast. The 4 October [D-017](../decisions/decision-log.md) product checkpoint remains necessary, and a public account probe wouldn't replace a consenting holder task.
