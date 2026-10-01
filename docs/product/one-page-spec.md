# Sell or borrow, one-page product spec

**Decision:** provisional read-only slice approved in [D-017](../decisions/decision-log.md), 2026-10-01. **Name:** working label only. **Chain:** BNB Chain mainnet. **First asset:** genuine NVDAB; the other three Venus bStock markets may follow after the first slice works.

## User and task

An eligible self-custody NVDAB holder needs a chosen amount of USDT today. They want to see what selling enough NVDAB would return now, and whether supplying their NVDAB to Venus and borrowing that USDT would leave a tolerable debt and liquidation threshold. The user makes the choice; the app doesn't sign a sale, supply or loan.

The trigger is a cash need, not a predicted price move. A public Venus API snapshot on 2026-10-01 showed vNVDAB with about $341,944 of indexed supply and 26 market supplier records, not 26 proven borrowers or product prospects. The [Venus interface](https://docs-v4.venus.io/guides/interface) already offers borrowing, and [Steward](https://github.com/zkasuran/steward-bnb/blob/a1ae5cf4153e370d16ef9dd1cd85cb116f0412ba/apps/web/app/api/use/swipe/route.ts) calculates a maximum bStock-backed borrow. This product must make the **same cash need** legible against a real sale, with risk and costs, or it has no reason to exist.

## End-to-end slice

1. User enters an EVM wallet address, cash target in USDT and NVDAB as the first supported asset. The app reads the token balance and Venus account state from BNB Chain. It never infers eligibility from the address.
2. Server resolves NVDAB through the signed Binance Web3 RWA Data API, checks chain ID and contract, then requests a fresh Trading API sell quote for an indicated raw token amount near the cash target. The UI shows quoted USDT, token units, route mode, fee fields as documented or unknown, quote time and expiry. If no route exists, it says so and doesn't invent a sale.
3. Server reads Venus market listing, effective collateral and liquidation factors, oracle price, vUSDT liquidity and variable borrow rate at a stated block/time. For a wallet with other collateral, debt or E-Mode, the first slice suppresses any simplified liquidation threshold until an account-wide calculation is implemented. A no-position scenario is labelled as a scenario, never as the user's balance.
4. The result shows two paths against the cash target: **sell**, with quoted proceeds and remaining token balance; **borrow**, with feasible or infeasible target, retained exposure, current-rate interest illustration for 30 and 90 days, and a clearly labelled price-drop stress or a reason that it can't be computed safely. It points to the existing execution venues for a new quote and user approval. Quotes can expire; reopening the page refreshes them.

## Data and failure boundaries

Binance Web3 API supplies token identity and an amount-specific spot sell quote. BNB Chain and Venus supply holdings and loan state. The Binance [`referencePrice` source is unresolved](../research/2026-10-01-reference-price-source-audit.md); it is not a cash-equity benchmark in this product. Variable APY is a snapshot; 30/90-day interest is an illustration if the rate stays fixed. The interface must show the time and source of each number and separate a documented fee from an unknown network or execution cost.

Wrong network, unrecognized contract, insufficient balance, no route, unsupported RFQ mode, stale market data, halted borrowing, insufficient pool cash, existing multi-asset debt and API failure each get a specific state. Unknown is a valid result. No automatic refinancing, Agent Studio, payment token, trade execution, profit estimate or jurisdiction bypass belongs in this slice.

## Acceptance criteria

1. A reviewer can enter one permitted wallet and a USDT target and see a live BNB Chain balance, Venus block and source timestamp, with sample mode visibly separate.
2. The server makes at least one successful signed Binance Web3 API request for this task and shows the observed route or exact no-route state without exposing credentials or a wallet-bound quote ID.
3. Both paths use the same cash target and explicit token units; a sale shortfall remains visible rather than being rounded into success.
4. A wallet with other debt, other collateral or E-Mode cannot receive a simplified personal liquidation-price claim.
5. A quote or Venus read failure leaves the other path visible with its own freshness and a safe retry action.
6. The README reproduces the read-only path, and the DX report records real setup, latency, errors and missing fields. A clean judge session can finish the task without a founder explanation.

**Main measure:** among observed eligible tasks, whether the user can name the feasible cash path and its principal cost/risk after the result, compared with the same task in existing wallet, trading and Venus screens. One session won't establish demand. **Demo sentence:** “For a holder who needs 100 USDT, show what a fresh NVDAB sale would return and what a Venus loan would put at risk.”

**Stop rule:** retire this candidate if no permitted signed quote can be obtained, if account-wide Venus state makes the comparison unsafe within the deadline, or if existing products give the same decision with equal clarity in the same task. This spec authorizes implementation only; it doesn't establish a working product or financial advantage.
