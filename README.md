# Dyplux RWA Safety: provisional tokenized-stock action review

**Current product core is provisional.** The new local safety screen reviews one proposed NVDA token purchase on BNB Smart Chain before signing. It identifies the exact bStock or Ondo contract, reads signed Binance RWA data and an amount-specific quote, checks the on-chain bStock multiplier, and returns a deterministic `ALLOW`, `DENY` or `NEED_HUMAN` receipt. A live anonymous check normally returns `NEED_HUMAN` because holder eligibility, an independent underlying-stock reference clock and a funded simulation remain unverified. The [safety evidence](docs/research/2026-10-04-safety-evidence.md), [one-page spec](docs/product/safety-one-page-spec.md) and [mainnet path](docs/product/mainnet-execution-path.md) distinguish working reads from unbuilt execution.

The problem is concrete: a stock-token quote can look actionable while the underlying reference clock is unknown, the market state is undocumented, the displayed spread disappears at the executable route, or the buyer's eligibility has not been checked. Six [dated observations](docs/research/2026-10-04-safety-evidence.md) support the current safety workflow. The Monday open-price experiment remains a separate test and isn't a product claim.

## Run locally

Python 3.9 or newer is enough; the safety screen has no installed package dependency. Put your own `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` in the process environment or a Git-ignored `.env`. The [template](.env.example) lists these names. No wallet key is used.

```sh
python3 app/safety_server.py
```

Open `http://127.0.0.1:8001`. Choose NVDAB or NVDAon, enter 10 to 1,000 USDT and your maximum spend and price-impact bounds. Click **Review action**. The screen shows source capture times, market state, token and independent-reference clocks separately, multiplier, route mode, holder-access gap, simulation gap, reason codes and downloadable JSON receipt. For Ondo, it also reads Binance's public Wallet Skill stock-info feed. That price has no observed stock-feed as-of timestamp, so reference age stays `UNKNOWN`. The server binds only to localhost, accepts four checks per minute and sends no transaction. The [bStock](docs/product/safety-screen-live.png) and [Ondo](docs/product/safety-screen-ondo-live.png) Sunday browser captures are dated observations, not standing service guarantees. The synthetic suite covers this service and the policy, including `offhours` and the untimed stock-feed regression.

Policy version 0.6.0 checks the returned route's chain, source token, destination contract, raw input amount and positive output against the requested action. A synthetic route mismatch denies; one new live NVDAB check matched these four fields but still returned `NEED_HUMAN`. Route identity matching doesn't prove user eligibility, wallet binding, or a fill.

Without API credentials, choose **View dated example from 4 October**. It replays one fixed, read-only NVDAB decision captured at 15:57 UTC; form entries don't change the replay. Its receipt hash can be checked offline. It doesn't demonstrate a live API connection or a current market decision.

The [current judge-run guide](docs/submission/safety-judge-run.md) walks through one live action and a mandate-denial case in a clean local session.

An optional read-only [exact-wallet dry run](docs/devex/repros/2026-10-04-demo-wallet-dry-run.md) uses the **public** `BNB_STOCKS_DEMO_ADDRESS` from the ignored `.env`: `python3 scripts/prepare_exact_wallet_simulation.py --provider bstock`. It requests a 10 USDT quote, unsigned build and off-chain simulation for one address. It can't sign or broadcast. The 4 October trial predicted `FAILED` because the demo address had insufficient USDT; it isn't an eligible funded transaction.

## Evidence a reviewer can reproduce

- The [safety evidence](docs/research/2026-10-04-safety-evidence.md) links each observed failure to a source, a product guard and its remaining uncertainty. The [single-action spec](docs/product/safety-one-page-spec.md) names the current user task and acceptance criteria.
- The [bStock](docs/product/safety-screen-live.png) and [Ondo](docs/product/safety-screen-ondo-live.png) captures show the current browser surface on 4 October. They are dated read-only observations. [Exact-wallet quote, build and failed simulation](docs/devex/repros/2026-10-04-demo-wallet-dry-run.md) are a separate technical trial without a signature or fill.
- `python3 -m unittest discover -s tests -q` runs synthetic policy, safety-service, collector, market-hour and data-integrity checks without credentials or live API calls. The [GitHub Python workflow](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions) runs the same suite.
- The [DevEx evidence summary](docs/devex/2026-10-04-evidence-summary.md) separates API documentation discrepancies from our own integration errors. Reproduction fixtures and raw-response hashes support its observations.

## Live research, separate from the app

On 4 October the project started a read-only five-minute market-hours collector. It samples 40 BNB Chain stock contracts with one signed catalog request and one batched price request per cycle. The initial 11:10 UTC research and 11:40 UTC aligned-window update, catalog grouping, ratio arithmetic and quote checks are described in the [dated research note](docs/research/2026-10-04-live-rwa-catalog-and-quotes.md). The [current status](STATUS.md) distinguishes measured results from unresolved product choices. An existing visual budget prototype remains local and unintegrated.

The [Sunday DevEx summary](docs/devex/2026-10-04-evidence-summary.md) links exact fixtures for the undocumented `offhours` state, a route-documentation conflict and the 100-address GET failure. It also separates our own amount-unit and clock errors from API behavior. The collector keeps adding logged calls; use its dated metrics and raw log for a count at a given time.

The [5 USDC Apple substitute matrix](docs/research/2026-10-04-exact-budget-substitute-matrix.md) compares our dated route check with pinned Yostocks source and PancakeSwap's public Stock Terminal. [D-054](docs/decisions/decision-log.md) pauses the exact-budget standalone build until it demonstrates a permitted user action that existing tools don't already support. A separate [public Binance payload repro](docs/devex/repros/2026-10-04-public-stock-reference-clock.md) shows the reference-source ambiguity without claiming an independent stock-price clock.

A [Sunday sell-side probe](docs/research/2026-10-04-sell-route-sunday.md) returned two indicative NVDA exit quotes and no blocked route for its bounded amount. The [pinned gateway substitute audit](docs/research/2026-10-04-gateway-substitute-audit.md) records why a generic policy/MCP/tape wrapper would overlap OneTicker. One block-pinned APRO NVDAB/USD round has a real update time, but it dates a token oracle, not the underlying stock reference.

With a valid local `.env`, the research commands are:

```sh
python3 scripts/rwa_research.py health
python3 scripts/audit_market_tape.py 2026-10-04
python3 scripts/rwa_research.py start --interval 300 --keep-awake
python3 scripts/normalize_catalog.py
python3 scripts/analyze_rwa.py
python3 scripts/audit_reference_formula.py 2026-10-04
python3 scripts/compare_friday_close.py --slot 5970384
python3 scripts/probe_live_policy.py --slot 5970384
python3 scripts/audit_ratio_transitions.py
```

`start` detaches the collector; don't run a second copy. `health` exits nonzero if it has stopped or fallen overdue. See the [collector operations](docs/devex/collector-operations.md) for logs, restart behavior and the external SSD reboot limitation. The `LIVE` tape and raw API response store remain local. Frozen fixtures, normalized catalog snapshots and experiment summaries are in this repository. The API provides `tokenPriceUpdatedAt`, while an independent underlying reference timestamp hasn't been observed. The analysis stores reference age as `UNKNOWN`; it doesn't substitute token-price age.

The separate [read-only policy skeleton](app/rwa_policy.py) checks token and issuer identity, caller-verified user eligibility with a dated basis, share-ratio changes, market state, age, quote availability, size, impact and simulation status. It measures independent reference age only when supplied by an independent source; a mandate can explicitly waive that requirement for a task that doesn't use a stock-market reference. A country indication or quote alone can't satisfy the user-eligibility guard. A policy `ALLOW` only means the supplied evidence passed this prototype's checks; it isn't issuer authorization, a trade or an investment recommendation.

## Limits and submission state

The app is a read-only localhost prototype. It hasn't bought or sold NVDAB, simulated a funded transaction, proved issuer access for a person or jurisdiction, measured final paid costs or validated later exit availability. Binance's [bStocks FAQ](https://www.binance.com/en/support/faq/detail/f0d41139fadc4790bf9a4c0c7bce2e88) says third-party integrators must enforce geographic restrictions; the endpoint path mentioned there wasn't confirmed in our source review. Public quote hosting is blocked pending that control.

This repository is private while the founder reviews the product and [current submission gates](docs/submission/current-readiness.md). The [official submission section](https://www.bnbchain.org/en/hackathons/tokenized-stocks) permits a deployed link **or** judge-run instructions, while its eligibility section says the repo, demo and deployed link must remain accessible through judging. The project needs a public repo and a reliable judge-access path before submission; the precise link requirement should be confirmed with the organisers. The project form and Developer Experience Report haven't been submitted. Bell is a separate CoinMarketCap hackathon project; this repository has separate code, credentials and evidence.

Earlier NVDAB sale-versus-Venus-borrow work was retired as the active product. Its original README and method remain in the [research archive](docs/archive/README-before-exit-check.md); the panel still runs at `/venus-scenario` for inspection.

The later Exit Check and exact-budget experiments are also inactive. The [Exit Check observation](docs/research/2026-10-03-exit-check-live-browser.md) records a 5 USDC two-way quote; it did not prove a round-trip fill or profit. Its [former judge instructions](docs/submission/judge-run.md), [video QA](docs/submission/video-qa.md) and [exact-budget spec](docs/product/exact-budget-stock-spec.md) remain available for the decision history. To inspect the archived local interface, run `python3 app/server.py` and open `http://127.0.0.1:8000`.
