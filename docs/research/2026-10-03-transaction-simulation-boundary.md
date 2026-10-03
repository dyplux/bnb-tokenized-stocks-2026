# Transaction API simulation boundary for the NVDAB sale

**Checked:** 2026-10-03. **Method:** official Binance Web3 Transaction API reference, compared with the project's [unsigned SWAP build](2026-10-02-first-live-swap-build.md). No signed Transaction API request, wallet signature or transaction was made.

The [official simulation endpoint](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/transaction-api) is signed `POST /api/v1/dex/pre-transaction/simulate`. For an EVM chain it takes `binanceChainId` and one `evmTx` object with `from`, `to`, `value` in wei and ABI `data`. The documented response has a predicted `status`, optional `failReason`, token `balanceChanges` and ERC-20 `allowanceChanges`. This is a forecast, not a settlement receipt.

The technical NVDAB quote returned `executionMode=SWAP` and a later `/swap` request built an unsigned EVM transaction for a temporary nonholder. That account's holdings and allowance were not verified. The simulation reference documents no state override for token balance or allowance. A failed simulation from this address would show its current inability to execute, not whether an eligible holder could sell. A successful API response alone would not prove fill, minimum received, net proceeds or permission to trade.

| Check before a meaningful simulation | Current evidence |
|---|---|
| Same fresh quote and built transaction, chain 56, pinned NVDAB and USDT | A single technical SWAP build exists; it expired and must not be reused |
| `from` is the consenting holder's funded wallet | No consenting eligible holder session is recorded |
| NVDAB balance, allowance, BNB gas balance and any approval step | Not verified for a holder |
| Predicted status and balance deltas | No Transaction API simulation called |
| Executed amount, gas and received USDT | No live transaction or receipt |

**Gate:** do not describe the current quote and build as a dry-run of an executable sale. After [D-033's product checkpoint](../decisions/decision-log.md), a bounded holder-specific simulation could narrow execution and cost uncertainty. A live mainnet demonstration needs a separate amount, fee limit and founder authorization. The [official track](https://www.bnbchain.org/en/hackathons/tokenized-stocks) directs teams to dry-run with the Transaction API and demo with small live amounts.
