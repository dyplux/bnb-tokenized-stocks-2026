# Venus Core current facet boundary

**Observed:** 2026-10-03 01:08 UTC, BNB Smart Chain block `125393938`. **Method:** public read-only JSON-RPC at `https://bsc-dataseed.bnbchain.org`, with no wallet signature or paid API. The Plus Sol research pass couldn't resolve its RPC host, so the coordinator repeated only bounded public reads from the main environment. No repo code or app behavior changed.

## What the deployed contract returned

The [Venus Core Diamond interface](https://docs-v4.venus.io/technical-reference/reference-core-pool/comptroller/diamond/diamond) exposes `facetAddress(bytes4)`. At the pinned block, Core Unitroller `0xfD36E2c2a6789Db23113685031d7F16329158384` returned `0x8930b02c69edd37464b50991680d306bb9b8fdbd` as the first ABI word for both `getBorrowingPower(address)` selector `0x528a174c` and `getAccountLiquidity(address)` selector `0x5ec88c79`. The second word differed (`4` and `3`); it wasn't an address. The deployed facet had **14,049 runtime bytes** at that block. Its runtime SHA-256 was `66d156eea77f5b048b7d60383ae62982726ac83e5db224724861137e9df07bc4`.

These observations refresh the earlier [fixed-block selector routing](2026-10-02-venus-deployed-risk-read.md). A code hash is an identifier for the observed bytes, not a match to the [reviewed Venus PolicyFacet v10.3.0 source](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Comptroller/Diamond/facets/PolicyFacet.sol). Verified compiler input, settings and a normalized bytecode comparison weren't available, so source parity remains unknown.

## Attempted populated-account probe

A [public transaction receipt](https://bscscan.com/tx/0xbeba4bee7d8178527895e7507fcce98b5bb6c65a4f820bb5c81ecac4c25c4705) at block `96267085` contained two logs with the Venus `Borrow` event topic. Their borrower fields were used locally for two read-only current-block ABI calls without recording the addresses. Both accounts returned `(errorCode, liquidity, shortfall) = (0, 0, 0)` for both risk methods at block `125393793`. An old borrow event doesn't prove an open position today.

Two `eth_getLogs` attempts for those two emitting markets, over 500 and 25 recent blocks, each returned RPC error `-32005 limit exceeded`. No recent populated account or independent arithmetic reproduction was obtained. The direct BscScan page was inaccessible with HTTP 403 in the research environment. No account address, raw request or response was saved in this repo.

## Decision impact

The active facet routing and nonempty code are observed. Deployed-source parity and populated-account arithmetic parity are **not proven**. [D-030](../decisions/decision-log.md) still blocks a personal post-supply or post-borrow risk forecast. The 4 October [D-017](../decisions/decision-log.md) product checkpoint remains necessary, and a public account probe wouldn't replace a consenting holder task.
