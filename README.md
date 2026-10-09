# Praeva

**by Dyplux**

Deterministic RWA evidence and authorization review before a separate signer.

**Praeva by Dyplux** is the final product brand. Earlier dated artifacts, including the [frozen claims](docs/submission/frozen-claims-2026-10-05.md), may refer to **Dyplux Execution Safety Layer**. Their original historical state is preserved.

**Praeva is a deterministic RWA evidence-sufficiency and authorization review immediately before a separate privileged signer.** The deterministic result is `ALLOW`, `DENY` or `NEED_HUMAN`, with reason codes and a SHA-256 receipt.

**[Try the assessment console](https://praeva.dyplux.com/console/) · [Website](https://praeva.dyplux.com/) · [Stable agent card](https://agent.praeva.dyplux.com/.well-known/agent-card.json) · [Judge guide](JUDGE.md) · [Current 120-second film](https://praeva.dyplux.com/media/praeva-bnb-hack-final-v2.mp4) · [GitHub Pages fallback](https://dyplux.github.io/bnb-tokenized-stocks-2026/)**

A stock token can still have a quote when the underlying exchange is closed. The dated NVDAB replay returned `NEED_HUMAN`, and the historical mandate-bound SPYon request returned `DENY`. A separate 9 October [live SPYon proof](docs/submission/final-proof-2026-10-09.md) records one operator-authorized 10 USDT purchase that reached `ALLOW`, passed real-state RPC and Binance checks, and settled on BNB Smart Chain. The console's green `ALLOW` remains a synthetic policy fixture.

The current product reviews one proposed NVDAB or NVDAon purchase on BNB Chain. It uses signed Binance Web3 RWA Data and Trading API reads, a fixed-block BNB Chain multiplier check for NVDAB, and a deterministic [policy](app/rwa_policy.py). [Six observed safety findings](docs/research/2026-10-04-safety-evidence.md) explain why these checks exist. The [architecture and Built with BNB Chain proof table](JUDGE.md#3-minutes) connect each integration to code and observed evidence.

## See the product

- [Assessment console](https://praeva.dyplux.com/console/): three labelled static cases, a dated managed-runtime NVDAB `NEED_HUMAN` replay, a historical SPYon `DENY`, and a synthetic `ALLOW` policy test. The separate live SPYon purchase is indexed in the [9 October proof packet](docs/submission/final-proof-2026-10-09.md).

- [Primary website](https://praeva.dyplux.com): current destination for the observed, dated `NEED_HUMAN` and mandate-bound `DENY` cases, a clearly marked synthetic `ALLOW` policy fixture, source times, reason codes, receipt downloads. The fallback also exposes its system status. It makes no live signed API request. The [GitHub Pages judge page](https://dyplux.github.io/bnb-tokenized-stocks-2026/) remains available as fallback.
- [Current 120-second founder-selected video](https://praeva.dyplux.com/media/praeva-bnb-hack-final-v2.mp4): the current deployed variant, captured before the 9 October SPYon proof. It does not show that purchase. The [historical 63-second film](https://praeva.dyplux.com/media/praeva-bnb-hack-final.mp4) remains preserved, as does the [original 60-second two-case film](https://dyplux.github.io/bnb-tokenized-stocks-2026/media/execution-safety-judge-demo.mp4).
- [Judge instructions](docs/submission/safety-judge-run.md): run a fresh signed check with your own Binance Web3 API credentials, then try a mandate denial. The public page also works without credentials.

## Agent Studio proof, 7 to 9 October 2026

ERC-8004 Agent ID **2574** is registered on **BNB Chain testnet, chain 97**, with a [stable agent card](https://agent.praeva.dyplux.com/.well-known/agent-card.json). Three remote managed-runtime requests returned the canonical fixed NVDAB replay; an invalid task failed closed. Policy v0.6.0 receipt: `63c918049dc88ab90faef38f9b749be3993884989ec38bb253f5c2b887ae54db`.

A separate one-shot mainnet proof autonomously initiated one x402 top-up. Exactly **1 U** settled in [transaction `0xb0344256c2807a7ce5d888738048bf74d326bd816b007f6df0a06004506b415b`](https://bscscan.com/tx/0xb0344256c2807a7ce5d888738048bf74d326bd816b007f6df0a06004506b415b). One quote, one EIP-3009 payment signature and one paid dispatch occurred, with no economic retry. Authenticated provider evidence later attributed **USD 1 account credit** to the same transaction.

The HTTP payment wait timed out; the original runtime later exited through OOM, so same-process continuity isn't proven. A [9 October recovered explanation](docs/submission/final-proof-2026-10-09.md) succeeded in a new operator-assisted, key-funded process with one paid model attempt. It does not prove continuity of the original process or a complete autonomous loop. [Compact dated Studio proof](docs/submission/agent-studio-evidence.md) and [current claim buckets](docs/submission/claims-2026-10-09.md).

The managed trial expires **9 October 2026, 18:48:44 UTC**. Its [last managed request](docs/judge/studio/last-managed-2026-10-09.json) was captured before the [verified early switch to VPS fallback](docs/judge/studio/fallback-switch-2026-10-09.json) at 09:39 UTC. The stable Agent Card and `/a2a` endpoint now work without login. The endpoint serves the fixed dated replay; it doesn't fetch fresh market evidence or claim managed infrastructure. The console remains accessible without credentials.

## Download and open the console

The repository now includes the published frontend source in [web/](web/README.md) and its prebuilt static console. Python 3.9+ is sufficient; Node and API credentials aren't needed to inspect the recorded cases.

```sh
python3 scripts/run_console.py
```

This opens `http://127.0.0.1:8937/console/` in your browser. macOS users can try `Start-Praeva.command`; Windows users can try `Start-Praeva.bat` with Python installed. The launchers aren't signed installers. Both videos remain online rather than being duplicated in the checkout. The five evidence JSON files and receipt bytes are unchanged.

## Connect an AI agent

[Configure the local MCP server](docs/product/use-praeva-with-an-ai-agent.md) for three read-only tools: replay a dated case, verify receipt JSON offline, or explicitly request a fresh NVDAB/NVDAon assessment with your own Binance Web3 credentials. Python starts the stdio server; it has no signer, transaction or payment tool.

```sh
python3 scripts/praeva_mcp.py
```

Your MCP client launches that process and sends protocol requests; it isn't a chat terminal. Terminal-based agents can still use the JSON-in/JSON-out command below.

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

The same read-only decision is available to a local agent through `scripts/safety_agent_tool.py`. It accepts one JSON object on stdin with `provider`, `notional_usdt`, `max_notional_usdt` and `max_price_impact_percent`, then returns one JSON result. This adapter runs locally over stdin/stdout. The separate Agent Studio runtime serves the fixed dated replay described above. Binance Agentic Wallet remains unclaimed. A later [official read-only Wallet Skills proof](docs/submission/wallet-skills-evidence-2026-10-09.md) is dated 9 October; it preserves unresolved evidence and the same kernel. [Integration boundary](docs/product/agentic-wallet-integration-gate.md).

For a local agent prompt, stdin/stdout example and offline receipt check, see [Use Praeva with an AI agent](docs/product/use-praeva-with-an-ai-agent.md). The guide covers the MCP server and the original local stdin/stdout tool.

```sh
printf '%s\n' '{"provider":"bstock","notional_usdt":"10","max_notional_usdt":"10","max_price_impact_percent":"0.5"}' | python3 scripts/safety_agent_tool.py
```

With your own API credentials configured as above, the result contains `decision`, `reason_codes` and `receipt.receipt_sha256`. Exit code 0 means the tool returned a policy decision; it doesn't mean the proposed purchase was allowed. A source failure exits nonzero and returns an error instead of a decision receipt.

## What the evidence supports

| Current evidence | Limit |
|---|---|
| Signed Binance Web3 catalog, price and amount-specific route reads for NVDAB and NVDAon | A quote doesn't prove a user may hold or trade the asset. |
| Fixed-block bStock multiplier read | Current equality doesn't prove a past corporate action or future change. |
| Exact-wallet 10 USDT quote, unsigned build and off-chain simulation for NVDAB | The 4 October packet was unfunded at capture and its simulation predicted `FAILED`. No stock transaction was signed. |
| 7 October SPYon direct-route capture, shown in the console | The historical packet had zero router allowance, a stale independent SPY reference and a failed simulation. The separate 9 October live proof is documented in the root proof packet. |
| 9 October SPYon direct-route purchase | One operator-authorized 10 USDT purchase reached private-wrapper `ALLOW`; real-state RPC and Binance checks passed, with two signatures, two dispatches and no economic retry. It is not a general autonomous-trading or production-feed claim. |
| Five-minute, 40-contract market-hours collection | `tokenPriceUpdatedAt` dates the token price, not the underlying stock reference. Independent reference age remains `UNKNOWN`. |
| [Frozen Sunday-to-Monday benchmark](experiments/EXP-RWA-004/monday-findings.md) | Two of three independent tickers matched Sunday direction; TSLA missed. `SAFETY_ONLY` supports an off-hours guard, not a predictive trading claim. |

The [demo-asset comparison](docs/submission/demo-asset-selection.md) selects NVDAB for technical preflight because its quote, unsigned build, simulation and multiplier were observed. It **doesn't** clear issuer or user access. A real purchase requires verified eligibility, a funded passing simulation, route-target provenance and explicit approval for one exact transaction. [Execution gates](docs/product/mainnet-execution-path.md) and [submission blockers](docs/submission/blocker-board.md) record what remains.

The [real `ALLOW` audit](docs/submission/real-allow-audit.md) preserves the earlier candidate analysis and adds the bounded 9 October SPYon result. The live proof is one operator-authorized action, not a universal `ALLOW` claim. The synthetic fixture remains labelled as a code-path demonstration.

Praeva sits between a proposed action and a separate signer. Its [competitive positioning](docs/product/competitive-positioning.md) distinguishes that RWA evidence task from a router, wallet, trading agent or generic policy engine. It doesn't claim to have invented agent safety.

## Reproduce the research

The collector is separate from the product screen. With valid local credentials, `python3 scripts/rwa_research.py health` reports its last success, failure count, observation count and next expected run. [Collector operations](docs/devex/collector-operations.md) explain restart, deduplication and gaps. The local `LIVE` tape and raw responses stay outside Git; [dated normalized results](docs/research/2026-10-04-live-rwa-catalog-and-quotes.md), [DevEx evidence](docs/devex/2026-10-04-evidence-summary.md) and [fixtures](docs/devex/fixtures/) are public. `python3 -m unittest discover -s tests -q` runs the synthetic suite without API credentials.

The [current status](STATUS.md) separates the Tokenized Stocks submission from Set and Earn. The [decision log](docs/decisions/decision-log.md) records earlier product directions and why they were retired. The console presents captured cases, while the stable agent endpoint executes a fixed dated replay. Fresh signed market reviews use local credentials. One dated SPYon purchase is documented separately and does not turn the console presets into live execution.

## Evidence sufficiency and authority

A route can exist while authority to sign remains unproven. `NEED_HUMAN` is a first-class result: required evidence or authorization prerequisites are unresolved, so a human must resolve them before a separate signer may act. It doesn't authorize a trade. `DENY` records a policy violation; the console `ALLOW` fixture is synthetic; the separate9October purchase has an observed core/direct ALLOW.

Covenant / StockGuard overlap exists. Praeva's strongest distinction in this build is evidence sufficiency, provenance, freshness and authorization prerequisites before a separate signer. The receipt doesn't cryptographically enforce that signer's behavior or certify universal tokenized-stock safety.

Follow the [dated proof matrix](docs/submission/proof-matrix-2026-10-08.md) and the [9 October final proof](docs/submission/final-proof-2026-10-09.md). The later live purchase and recovered explanation are dated separately from the static console cases and the 8 October Studio package.

## Verify captured receipts offline

```sh
python3 scripts/verify_receipt.py docs/judge/observed-unsafe.json
python3 scripts/verify_receipt.py docs/judge/observed-unsafe.json --expected-sha256 63c918049dc88ab90faef38f9b749be3993884989ec38bb253f5c2b887ae54db
```

No API key or network request is needed. The verifier prints canonical integrity and saved-input replay separately. Integrity isn't authenticity; a trusted external expected hash pins bytes. Replay uses the same unchanged policy kernel, so it isn't an independent policy implementation. Missing saved context returns `REPLAY_UNAVAILABLE`. [States and exit codes](JUDGE.md#verify-a-receipt).
