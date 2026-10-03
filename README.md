# Exit Check by Dyplux, research prototype

**Product decision still open.** This read-only prototype asks Binance Web3 for a NVDAB entry quote, then an inverse quote on the exact estimated NVDAB amount for a chosen USDC amount and public BNB Chain address. It makes no trade. The founder has not approved this as the final product or its demo.

On Saturday 3 October 2026 at 22:05 UTC, the local app returned both directions for 5 USDC. The entry estimate was **0.021265631210341636 NVDAB**; the immediate inverse estimate was **5.001168101976778857 USDC** at BNB metadata block **125561266**. Those are separate, expiring quotes. The inverse amount above 5 USDC isn't profit: approval, gas, slippage, eligibility and execution weren't verified. See the [sanitized record](docs/submission/video-record.json) and [observation](docs/research/2026-10-03-exit-check-live-browser.md).

## Run locally

Python 3.9 or newer is enough; the app has no installed package dependency.

```sh
python3 app/server.py
```

Open `http://127.0.0.1:8000`. Add your own `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` to the process environment or a Git-ignored `.env` file. The [empty template](.env.example) lists those fields. Keep the default **5 USDC**, enter a **public** BNB Chain `0x` address and select **Check both routes**. The address is sent to Binance Web3 for address-specific quotes. The app doesn't request a private key, wallet connection, signature or Binance exchange account.

The server verifies the exact NVDAB bStock identity through Binance Web3 RWA Data, checks NVDAB and USDC token metadata at one BNB Chain block, requests a USDC-to-NVDAB quote and then requests an NVDAB-to-USDC quote for the first estimated output. It returns only selected amounts, routes, fee estimates and timestamps. Quote IDs and the input address don't appear in the app response. A visible result expires 20 seconds after the request starts. Six accepted quote checks per minute and one active check are the local process limits.

The screen distinguishes **Both routes quoted**, **Entry route unavailable**, **Exit route unavailable** and **Check incomplete**. A missing or mismatched identity, contract or amount blocks the next quote. A route now says nothing about a later price or settled proceeds. [Judge-run instructions](docs/submission/judge-run.md) describe the one-minute path and failure states.

## Evidence a reviewer can reproduce

- The [current-build observation](docs/research/2026-10-03-exit-check-live-browser.md) records three local read-only runs on 3 October. The [video record](docs/submission/video-record.json) corresponds to one continuous browser capture, with no wallet address or credentials retained.
- The [34-second video QA](docs/submission/video-qa.md) describes the local MP4 and full source archive. A public video URL hasn't been published yet.
- `python3 -m unittest discover -s tests -q` ran **54 synthetic tests** locally. The [GitHub Python workflow](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions/runs/37157834389) passed on private commit `45f0e0e` without credentials or live API calls.
- The [DX field log](docs/dx/field-log.md) separates signed API observations, local integration errors and missing measurements. The [one-page spec](docs/product/pre-entry-exit-spec.md) defines this prototype's task and excluded claims; [D-049](docs/decisions/decision-log.md) reopens the product decision.

## Limits and submission state

The app is a read-only localhost prototype. It hasn't bought or sold NVDAB, simulated a funded transaction, proved issuer access for a person or jurisdiction, measured final paid costs or validated later exit availability. Binance's [bStocks FAQ](https://www.binance.com/en/support/faq/detail/f0d41139fadc4790bf9a4c0c7bce2e88) says third-party integrators must enforce geographic restrictions; the endpoint path mentioned there wasn't confirmed in our source review. Public quote hosting is blocked pending that control.

This repository is private while the founder reviews [publication and submission steps](docs/submission/final-review-packet.md). The official hackathon accepts judge-run instructions in place of a deployed link. The project form and Developer Experience Report haven't been submitted. Bell is a separate CoinMarketCap hackathon project; this repository has separate code, credentials and evidence.

Earlier NVDAB sale-versus-Venus-borrow work was retired as the active product. Its original README and method remain in the [research archive](docs/archive/README-before-exit-check.md); the panel still runs at `/venus-scenario` for inspection.
