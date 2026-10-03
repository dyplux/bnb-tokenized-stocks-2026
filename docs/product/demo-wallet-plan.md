# Small mainnet demonstration plan

**Status, 2026-10-03:** plan only. A dedicated, zero-balance wallet exists in the Git-ignored project `.env`. No funds were sent, no transaction was signed and no stock was bought. The founder has no existing bStock holding. This wallet is separate from the Set and Earn campaign.

## Purpose and boundary

The possible trial is one small BNB Smart Chain spot round trip: USDC to NVDAB, then the resulting NVDAB back to USDC. It would test whether the documented buy and exit routes can actually settle for a controlled wallet. It would **not** validate the current product's 100 USDT sell-versus-borrow decision, a profitable strategy, or the usability of a holder's Venus position.

The [5 USDC read-only quote check](../research/2026-10-03-usdc-nvdab-roundtrip-quote.md) returned routes in both directions on 3 October. Those separate estimates expire. The inverse estimate exceeded 5 USDC before any real approvals, gas, slippage, market move or transfer charge. It is not a profit observation or a guarantee of capital recovery.

## Gates before funding

1. Founder backs up `BNB_STOCKS_DEMO_PRIVATE_KEY` from the local `.env` to a private password manager and checks that the backup can recover the public address. Never send the key or recovery material in chat, Git, screenshots or a form.
2. Apply [D-045](../decisions/decision-log.md): the 100 USDT cash-choice claim was retired after the founder chose a solo demonstration. Decide whether a technical buy and sell serves a newly selected product before moving funds.
3. Confirm that the founder is eligible to hold and trade this representation, that the contract addresses and decimals remain correct, and that the chosen USDC is the BNB Chain token quoted by the API. A route response alone does not establish eligibility.
4. Fetch new entry and inverse quotes for a 5 USDC input from the funded wallet address. Record timestamps, route vendor, minimum received, fee units and quote validity. Confirm approval requirements and simulate the exact proposed transactions. Stop if a required step cannot be explained or simulated.
5. Prepare an action summary for founder review: network, public wallet address, input token and amount, exact spender and approval amount, transaction destination, expected minimum output, gas ceiling, stop conditions and exit plan. Signing and broadcast require separate, specific authorization.

## Proposed funding ceiling

For a technical trial, propose **5 USDC plus at most €2 worth of BNB** for network fees. Keep the total asset value placed in this wallet below **€10 at the moment of funding**. The whole wallet balance can be lost. Purchase, withdrawal and return-transfer fees outside the wallet count as additional costs and must be checked before funding; do not present €10 as a guaranteed all-in loss ceiling. If the transfer minimum or external fees make this size impractical, stop instead of enlarging the trial automatically.

Use only BNB Smart Chain for these transfers. The founder should send a tiny BNB test transfer first and confirm the receiving address and chain before sending the remaining planned amount. The assistant must not infer consent to spend from the mere presence of funds.

## Execution and recovery

If specifically authorized after the gates above, use exact-amount approvals rather than unlimited allowances, execute one small purchase, record actual receipt and token balance, refresh the exit quote, then execute one sale back to USDC only if the route and minimum output remain acceptable under the founder-approved stop conditions. Revoke residual allowances when feasible. Return any remaining USDC and BNB to an address supplied by the founder through a private channel, after checking the network and transfer fee. A failed or unavailable exit may leave NVDAB in the wallet; do not claim automatic conversion back to USDC.

Record timestamps, public transaction hashes, executed amounts and paid gas in the Developer Experience log. Do not record private keys, signed raw transactions, personal wallet history or unredacted API headers.
