# Deployed Venus Core risk-read check

**Observed:** 2026-10-02 02:24:04 UTC, BNB Smart Chain block `125211896` (`0x77694f8`). **Method:** public read-only JSON-RPC calls to `https://bsc-dataseed.bnbchain.org`. No wallet signature, deposit, borrow or Binance Web3 request was made.

The [Venus Core Diamond interface](https://docs-v4.venus.io/technical-reference/reference-core-pool/comptroller/diamond/diamond) exposes `facetAddress(bytes4)`. The [PolicyFacet documentation](https://docs-v4.venus.io/technical-reference/reference-core-pool/comptroller/diamond/facets/policy-facet) names `getBorrowingPower(address)` and `getAccountLiquidity(address)`. Function selectors were computed with Keccak-256 in a temporary local tool. Two cross-checks matched known selectors: `getAssetsIn(address)` yielded `0xabfceffc`, already used by the app, and `facetAddress(bytes4)` yielded `0xcdffacc6`.

| Read at the fixed block | Selector | Result |
|---|---|---|
| `eth_chainId` | n/a | `0x38` (56) |
| `eth_getCode` on Core Unitroller `0xfD36E2c2a6789Db23113685031d7F16329158384` | n/a | Nonempty runtime code |
| `facetAddress(getAssetsIn(address))` | `0xabfceffc` | `0x21f8e1471b153f49be1d645a008e4a57434eed23`, with runtime code |
| `facetAddress(getBorrowingPower(address))` | `0x528a174c` | `0x8930b02c69edd37464b50991680d306bb9b8fdbd`, with runtime code |
| `facetAddress(getAccountLiquidity(address))` | `0x5ec88c79` | Same deployed risk facet, with runtime code |
| `getBorrowingPower(0x000...000)` | `0x528a174c` | Three ABI words: `(0, 0, 0)` |
| `getAccountLiquidity(0x000...000)` | `0x5ec88c79` | Three ABI words: `(0, 0, 0)` |

The zero address was a deliberately empty ABI probe. It isn't a user case and doesn't demonstrate that borrowing or liquidation values are correct for an account with collateral and debt. The fixed-block facet routing and tuple shape support a later current-position read, but the facet bytecode wasn't matched to the reviewed v10.3.0 source in this pass. They don't authorize a personal post-action forecast. A nonempty, consented holder case and the signed Binance sale quote remain the product gates. See the earlier [source-level feasibility note](2026-10-02-account-wide-risk-feasibility.md).
