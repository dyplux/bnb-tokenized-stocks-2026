# NVDAB holder current-risk arithmetic parity

**Observed:** 2026-10-03 around 04:38 UTC, BNB Chain block `125421781`. Read-only. No wallet connection, transaction, order or participant contact.

## Method

The [reproducible bounded probe](../../scripts/probe_nvdab_holder_risk_parity.py) made one signed Binance Web3 [holder-ranking GET](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/general-data) for Venus vNVDAB. It considered the first 15 ranked rows. After checking BNB Chain 56 and validating Core, vNVDAB and vUSDT contract identities at one block, it selected the first public account with a positive vNVDAB balance, vNVDAB entered as Core collateral, positive stored vUSDT debt and no more than five entered Core markets. The account identifier and signed response stayed in memory and weren't printed or saved.

The script then recomputed Core's current borrowing-power and liquidation-threshold tuples using the integer order in the [Venus v10.3.0 ComptrollerLens](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Lens/ComptrollerLens.sol). It compared both complete three-word tuples with the deployed Core calls at the same block. The standalone parity helper caps itself at 35 public RPC calls; it used 21 in this run. The script exposes only counts, booleans and tuple differences.

## Result

| Fixed-block check | Observed |
|---|---:|
| Holder rows considered | 15 |
| Accounts inspected before candidate | 1 |
| Candidate with entered vNVDAB and positive vUSDT debt | 1 |
| Entered Core markets in that account | 3 |
| Active markets used in each risk calculation | 2 |
| E-Mode pool ID | 0 |
| VAI repayment nonzero | no |
| Borrowing-power tuple | exact, difference `[0, 0, 0]` |
| Liquidation-threshold tuple | exact, difference `[0, 0, 0]` |

The script returned `status=ok`, exit code 0. One signed holder-ranking request was added to the [Developer Experience log](../dx/field-log.md); its individual latency wasn't retained. No Binance business error or rate limit was observed.

## Interpretation and limits

This improves on the earlier [governance-voter parity case](2026-10-03-venus-core-bounded-arithmetic-parity.md): the selected public account held and entered NVDAB, had USDT debt, and used two nonzero markets in current-risk arithmetic. The selected account also had other entered markets, so the result doesn't isolate NVDAB's contribution to its borrowing power. Ranked holders aren't a random sample or verified eligible people.

The parity is for **current state**. It doesn't model a new NVDAB supply, an additional USDT borrow, accrued future debt, a sale, E-Mode, nonzero VAI, execution costs or a post-action safety margin. The reviewed v10.3.0 source hasn't been proven byte-identical to the deployed facet. A consenting holder's cash task has still not been observed. [D-033](../decisions/decision-log.md) and the 4 October product checkpoint stay open.

**Sources checked 2026-10-03:** [Binance Web3 holder-ranking reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/general-data), [Venus v10.3.0 ComptrollerLens](https://github.com/VenusProtocol/venus-protocol/blob/v10.3.0/contracts/Lens/ComptrollerLens.sol), [BNB Chain public RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/).
