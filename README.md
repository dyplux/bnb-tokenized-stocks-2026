# Dyplux Execution Safety Layer for Tokenized Equities

**Before an autonomous agent signs a tokenized-stock purchase, Dyplux checks the evidence needed to authorize it and fails closed when critical state is unknown.** The deterministic result is `ALLOW`, `DENY` or `NEED_HUMAN`, with reason codes and a SHA-256 receipt.

**[Live judge page](https://dyplux.github.io/bnb-tokenized-stocks-2026/) · [60-second evidence video](https://dyplux.github.io/bnb-tokenized-stocks-2026/media/execution-safety-judge-demo.mp4) · [Judge guide, 60 seconds to 15 minutes](JUDGE.md)**

A stock token can still have a quote when the underlying exchange is closed. In the observed NVDAB case, an amount-specific route existed, but independent underlying-reference time, individual holder eligibility and a funded passing simulation weren't verified. Dyplux returned `NEED_HUMAN`. A second observed request exceeded its 20 USDT mandate and returned `DENY`. [View both receipts](docs/submission/safety-judge-run.md). The green `ALLOW` is a synthetic policy fixture.

The current product reviews one proposed NVDAB or NVDAon purchase on BNB Chain. It uses signed Binance Web3 RWA Data and Trading API reads, a fixed-block BNB Chain multiplier check for NVDAB, and a deterministic [policy](app/rwa_policy.py). [Six observed safety findings](docs/research/2026-10-04-safety-evidence.md) explain why these checks exist. The [architecture and Built with BNB Chain proof table](JUDGE.md#3-minutes) connect each integration to code and observed evidence.

## See the product

- [Public judge page](https://dyplux.github.io/bnb-tokenized-stocks-2026/): observed, dated `NEED_HUMAN` and mandate-bound `DENY` cases; a clearly marked synthetic `ALLOW` policy fixture; source times, reason codes, receipt downloads and system status. It makes no live signed API request.
- [60-second two-case product video](https://dyplux.github.io/bnb-tokenized-stocks-2026/media/execution-safety-judge-demo.mp4): an 18:28 UTC live local read-only capture and a separate 19:56 UTC dated replay. The first returned `NEED_HUMAN`; the second returned `DENY` when a 100 USDT request exceeded a 20 USDT mandate. No trade was signed.
- [Judge instructions](docs/submission/safety-judge-run.md): run a fresh signed check with your own Binance Web3 API credentials, then try a mandate denial. The public page also works without credentials.

## Run a fresh check locally

Python 3.9 or newer is sufficient. Clone the repository and start the read-only screen from its root:

```sh
git clone https://github.com/dyplux/bnb-tokenized-stocks-2026.git
cd bnb-tokenized-stocks-2026
cp .env.example .env
python3 app/safety_server.py
```

The dated example works without credentials. For a fresh signed check, create your own key and secret in the [Binance Web3 Developer Portal](https://web3.binance.com/en/dev-portal), then fill the two values in the ignored `.env` before selecting **Review action**. The [authentication guide](https://web3.binance.com/en/dev-docs/authentication) documents the signing scheme already implemented by this client. Don't commit or paste the secret. No wallet key is needed.

Open `http://127.0.0.1:8001`. Choose NVDAB or NVDAon, enter 10 to 1,000 USDT, set maximum spend and price impact, and select **Review action**. The localhost service limits requests to four per minute. It doesn't connect a wallet, sign or broadcast. The read-only quote uses a temporary generated address, so route availability doesn't establish a particular holder's access or exact-wallet execution. The screen shows the contract, evidence times, policy decision and a downloadable receipt. [Full clean-start steps](docs/submission/safety-judge-run.md).

The same read-only decision is available to a local agent through `scripts/safety_agent_tool.py`. It accepts one JSON object on stdin with `provider`, `notional_usdt`, `max_notional_usdt` and `max_price_impact_percent`, then returns one JSON result. This is an agent-callable tool, **not** a deployed Binance Agentic Wallet or Agent Studio runtime. [Integration boundary](docs/product/agentic-wallet-integration-gate.md).

```sh
printf '%s\n' '{"provider":"bstock","notional_usdt":"10","max_notional_usdt":"10","max_price_impact_percent":"0.5"}' | python3 scripts/safety_agent_tool.py
```

With your own API credentials configured as above, the result contains `decision`, `reason_codes` and `receipt.receipt_sha256`. Exit code 0 means the tool returned a policy decision; it doesn't mean the proposed purchase was allowed. A source failure exits nonzero and returns an error instead of a decision receipt.

## What the evidence supports

| Current evidence | Limit |
|---|---|
| Signed Binance Web3 catalog, price and amount-specific route reads for NVDAB and NVDAon | A quote doesn't prove a user may hold or trade the asset. |
| Fixed-block bStock multiplier read | Current equality doesn't prove a past corporate action or future change. |
| Exact-wallet 10 USDT quote, unsigned build and off-chain simulation for NVDAB | The demo wallet has no funds; simulation predicted `FAILED`. No transaction was signed. |
| Five-minute, 40-contract market-hours collection | `tokenPriceUpdatedAt` dates the token price, not the underlying stock reference. Independent reference age remains `UNKNOWN`. |
| [Frozen Sunday-to-Monday benchmark](experiments/EXP-RWA-004/monday-findings.md) | Two of three independent tickers matched Sunday direction; TSLA missed. `SAFETY_ONLY` supports an off-hours guard, not a predictive trading claim. |

The [demo-asset comparison](docs/submission/demo-asset-selection.md) selects NVDAB for technical preflight because its quote, unsigned build, simulation and multiplier were observed. It **doesn't** clear issuer or user access. A real purchase requires verified eligibility, a funded passing simulation, route-target provenance and explicit approval for one exact transaction. [Execution gates](docs/product/mainnet-execution-path.md) and [submission blockers](docs/submission/blocker-board.md) record what remains.

The [real `ALLOW` audit](docs/submission/real-allow-audit.md) checks the available candidates. None can honestly receive `ALLOW` or `ALLOW_PENDING_SIGNATURE` with today's access and simulation evidence. The synthetic fixture remains labelled as a code-path demonstration. The working read-only safety task can be reviewed without a mainnet trade; the event's small-live-amount direction remains an unmet technical demonstration if no eligible action is approved.

## Reproduce the research

The collector is separate from the product screen. With valid local credentials, `python3 scripts/rwa_research.py health` reports its last success, failure count, observation count and next expected run. [Collector operations](docs/devex/collector-operations.md) explain restart, deduplication and gaps. The local `LIVE` tape and raw responses stay outside Git; [dated normalized results](docs/research/2026-10-04-live-rwa-catalog-and-quotes.md), [DevEx evidence](docs/devex/2026-10-04-evidence-summary.md) and [fixtures](docs/devex/fixtures/) are public. `python3 -m unittest discover -s tests -q` runs the synthetic suite without API credentials.

The [current status](STATUS.md) separates the Tokenized Stocks submission from Set and Earn. The [decision log](docs/decisions/decision-log.md) records earlier product directions and why they were retired. The public page is a dated packet, not a hosted live API service or an executed stock-token trade.
