# NVDAB collateral and USDT debt overlap

**Observed:** 2026-10-03 04:02:50 UTC, BNB Chain block `125416980`. Read-only. No wallet connected, transaction built, order submitted or participant contacted.

## Method

The [Binance Web3 holder-ranking reference](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/general-data), checked 2026-10-03, documents a signed `GET /api/v1/dex/market/token/holder` with `binanceChainId` and `tokenContractAddress`. One signed request for the pinned Venus vNVDAB contract returned **48 ranked addresses**. The endpoint returns at most 100 and has no pagination. Ranking is by token holdings, so the first 15 aren't a random user sample.

The [reproducible probe](../../scripts/probe_nvdab_holder_debt.py) checked chain 56, vNVDAB and vUSDT code, each market's underlying and Core Comptroller, then pinned one block. For each of the first 15 addresses it read vNVDAB `balanceOf`, Core `getAssetsIn`, and vUSDT `getAccountSnapshot` at that block. The [Venus Core reference](https://docs-v4.venus.io/technical-reference/reference-core-pool/vtoken), checked 2026-10-03, defines the snapshot's account token balance and borrow balance. The deployed vUSDT returned six 32-byte words; the probe uses the four declared values and rejects a nonzero protocol error. It also read account code for addresses with both collateral membership and USDT debt. No address, raw response, key or signature is printed or committed.

## Result

| Fixed-block observation | Count |
|---|---:|
| Top-ranked addresses checked without RPC error | 15 |
| Positive vNVDAB balance | 15 |
| vNVDAB entered as Venus Core collateral | 15 |
| Positive stored vUSDT debt | 9 |
| Both entered vNVDAB and positive vUSDT debt | 9 |
| EOAs among those nine addresses | 8 |
| Contract accounts among those nine addresses | 1 |
| Both debt and vNVDAB as the sole entered market | 0 |

The first bounded one-off read at block `125416096`, 03:56:12 UTC, also found 9 of the top 15 with entered vNVDAB and positive vUSDT debt. The later run above is the reproducible result. Account rankings or balances can change between runs.

## Interpretation and limits

This establishes account-level overlap between NVDAB collateral membership and USDT debt in a biased top-holder sample. All nine debt accounts had at least one other entered Core market, so this result **doesn't isolate how much borrowing power came from NVDAB**. A positive stored debt is a snapshot; it doesn't accrue the market in this read. Eight EOA addresses aren't eight verified people, eligible bStock traders or prospective product users.

No holder requested a cash amount, compared selling with borrowing, supplied sale costs or consented to a task observation. The result narrows the claim that this workflow is merely hypothetical, but it doesn't pass [D-033](../decisions/decision-log.md). It doesn't justify showing a personal safe-loan amount or publishing the current app.

**Sources:** [Binance holder-ranking API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/general-data), [Venus Core vToken reference](https://docs-v4.venus.io/technical-reference/reference-core-pool/vtoken), [BNB public RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/). All checked 2026-10-03. The signed response and account identifiers were handled in memory only.
