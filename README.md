# Dyplux RWA Safety: provisional tokenized-stock action review

**Current product core is provisional.** The new local safety screen reviews one proposed NVDA token purchase on BNB Smart Chain before signing. It identifies the exact bStock or Ondo contract, reads signed Binance RWA data and an amount-specific quote, checks the on-chain bStock multiplier, and returns a deterministic `ALLOW`, `DENY` or `NEED_HUMAN` receipt. A live anonymous check normally returns `NEED_HUMAN` because holder eligibility, an independent underlying-stock reference clock and a funded simulation remain unverified. The [safety evidence](docs/research/2026-10-04-safety-evidence.md), [one-page spec](docs/product/safety-one-page-spec.md) and [mainnet path](docs/product/mainnet-execution-path.md) distinguish working reads from unbuilt execution.

The former Exit Check is a separate archived research interface. It asks Binance Web3 for a NVDAB entry quote and an inverse quote on the estimated NVDAB amount. It makes no trade. [D-051](docs/decisions/decision-log.md) retired it as the proposed submission product. The [exact-budget spec](docs/product/exact-budget-stock-spec.md) is also inactive.

On Saturday 3 October 2026 at 22:05 UTC, the local app returned both directions for 5 USDC. The entry estimate was **0.021265631210341636 NVDAB**; the immediate inverse estimate was **5.001168101976778857 USDC** at BNB metadata block **125561266**. Those are separate, expiring quotes. The inverse amount above 5 USDC isn't profit: approval, gas, slippage, eligibility and execution weren't verified. See the [sanitized record](docs/submission/video-record.json) and [observation](docs/research/2026-10-03-exit-check-live-browser.md).

## Run locally

Python 3.9 or newer is enough; the safety screen has no installed package dependency. Put your own `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` in the process environment or a Git-ignored `.env`. The [template](.env.example) lists these names. No wallet key is used.

```sh
python3 app/safety_server.py
```

Open `http://127.0.0.1:8001`. Choose NVDAB or NVDAon, enter 10 to 1,000 USDT and your maximum spend and price-impact bounds. Click **Review action**. The screen shows the source capture times, market state, token and independent-reference clocks separately, multiplier, route mode, holder-access gap, simulation gap, reason codes and downloadable JSON receipt. It binds only to localhost, accepts four checks per minute and sends no transaction. The [live Sunday browser capture](docs/product/safety-screen-live.png) is a dated observation, not a standing service guarantee. [Twenty-five focused tests](tests/test_safety_service.py) cover this service and the policy, including the `offhours` fail-closed regression.

The older Exit Check remains available separately:

```sh
python3 app/server.py
```

Open `http://127.0.0.1:8000`. Add your own `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` to the process environment or a Git-ignored `.env` file. The [empty template](.env.example) lists those fields. Keep the default **5 USDC**, enter a **public** BNB Chain `0x` address and select **Check both routes**. The address is sent to Binance Web3 for address-specific quotes. The app doesn't request a private key, wallet connection, signature or Binance exchange account.

The server verifies the exact NVDAB bStock identity through Binance Web3 RWA Data, checks NVDAB and USDC token metadata at one BNB Chain block, requests a USDC-to-NVDAB quote and then requests an NVDAB-to-USDC quote for the first estimated output. It returns only selected amounts, routes, fee estimates and timestamps. Quote IDs and the input address don't appear in the app response. A visible result expires 20 seconds after the request starts. Six accepted quote checks per minute and one active check are the local process limits.

The screen distinguishes **Both routes quoted**, **Entry route unavailable**, **Exit route unavailable** and **Check incomplete**. A missing or mismatched identity, contract or amount blocks the next quote. A route now says nothing about a later price or settled proceeds. [Judge-run instructions](docs/submission/judge-run.md) describe the one-minute path and failure states.

## Evidence a reviewer can reproduce

- The [current-build observation](docs/research/2026-10-03-exit-check-live-browser.md) records three local read-only runs on 3 October. The [video record](docs/submission/video-record.json) corresponds to one continuous browser capture, with no wallet address or credentials retained.
- The [34-second video QA](docs/submission/video-qa.md) records an internal technical capture. Video and submission work stopped at [D-049](docs/decisions/decision-log.md), before the product was selected.
- `python3 -m unittest discover -s tests -q` is the synthetic suite for RWA policy, collector health, session boundaries, tape integrity, reference-formula arithmetic, ratio transitions and external-close arithmetic. The [GitHub Python workflow](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions) runs it without credentials or live API calls. Three policy cases also cover missing, ineligible and stale user access.
- The [DX field log](docs/dx/field-log.md) separates signed API observations, local integration errors and missing measurements. The [Exit Check spec](docs/product/pre-entry-exit-spec.md) defines the built prototype; the [exact-budget spec](docs/product/exact-budget-stock-spec.md) and [D-051](docs/decisions/decision-log.md) record the newer, unbuilt hypothesis. The [5 USDC Apple route check](docs/research/2026-10-03-aapl-three-representation-route-check.md) records three different provider states and an Ondo USDT minimum follow-up.

## Live research, separate from the app

On 4 October the project started a read-only five-minute market-hours collector. It samples 40 BNB Chain stock contracts with one signed catalog request and one batched price request per cycle. The initial 11:10 UTC research and 11:40 UTC aligned-window update, catalog grouping, ratio arithmetic and quote checks are described in the [dated research note](docs/research/2026-10-04-live-rwa-catalog-and-quotes.md). The [current status](STATUS.md) distinguishes measured results from unresolved product choices. An existing visual budget prototype remains local and unintegrated.

The [Sunday DevEx summary](docs/devex/2026-10-04-evidence-summary.md) traces 91 logged calls and links exact fixtures for the undocumented `offhours` state, a route-documentation conflict and the 100-address GET failure. It also separates our own amount-unit and clock errors from API behavior.

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

This repository is private while the founder reviews the product and [publication and submission steps](docs/submission/final-review-packet.md). The official hackathon accepts judge-run instructions in place of a deployed link. The project form and Developer Experience Report haven't been submitted. Bell is a separate CoinMarketCap hackathon project; this repository has separate code, credentials and evidence.

Earlier NVDAB sale-versus-Venus-borrow work was retired as the active product. Its original README and method remain in the [research archive](docs/archive/README-before-exit-check.md); the panel still runs at `/venus-scenario` for inspection.
