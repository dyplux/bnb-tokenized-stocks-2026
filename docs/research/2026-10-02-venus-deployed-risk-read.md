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

## A nonzero vToken balance without collateral membership

At block `125212731`, `2026-10-02 02:30:20 UTC`, a second fixed-block read used the [documented BNB Chain Venus Treasury address](https://docs-v4.venus.io/deployed-contracts/funds) `0xf322942f644a996a617bd29c16bd7d231d9f35e9` and the [Venus API market address](https://api.venus.io/markets?chainId=56&underlyingAddress=0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436&limit=10) for vNVDAB, `0xEb8Ca841cBe1BC4832A10b15c7dAB1081eDaD371`. The market lookup used the `accept-version: next` header. `vNVDAB.balanceOf(Treasury)` returned `45,000,000` base units; `vNVDAB.decimals()` returned `8`, so the token balance was `0.45 vNVDAB`. At the **same block**, `Core.getAssetsIn(Treasury)` returned an empty array, while both `getBorrowingPower(Treasury)` and `getAccountLiquidity(Treasury)` returned `(0, 0, 0)`.

This is a protocol-controlled address, not a user observation. The read demonstrates that a nonzero vToken balance needn't be enabled as collateral or create borrowing power. It doesn't establish the balance's origin, an underlying NVDAB balance, a borrow limit for an eligible person or the behavior of an account with active collateral and debt. A future account display must keep vToken holdings, entered-market membership and aggregate risk values separate.
