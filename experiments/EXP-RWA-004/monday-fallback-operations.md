# Monday open observation fallback

**Prepared:** 2026-10-04 UTC. **Window:** 2026-10-05 13:20 to 13:45 UTC. This protects observation continuity. It doesn't change the [frozen Sunday sample, outcome definition or scorer](monday-open-protocol.md).

## Sources and separation

| Label | Process | Data location | Scope |
|---|---|---|---|
| `PRIMARY` | Existing 40-contract, five-minute collector and 30-minute underlying watch | Ignored `data/market_hours/` and `data/weekend_2026-10-03_05/`; existing records say `origin=LIVE` | Original research tape, with its own checkpoints and gaps |
| `FALLBACK` | Separate local one-minute process | Ignored `data/monday_open_fallback/local/` | Six frozen BNB Chain representations: NVDA, TSLA and COIN from bStock and Ondo; separate raw response hashes and capture times |
| `FALLBACK` | GitHub Actions public-data process | Independent workflow-run artifacts | Six contract-addressed public Binance website prices and intraday public observations for NVDA, TSLA and COIN, without Binance credentials or a Mac dependency |

The local fallback reads the six contract identities from the frozen [Friday-close benchmark](friday_close_benchmark.csv). A preflight before Monday is labelled `PREFLIGHT`, not a Monday observation. New Monday fallback observations use `origin=FALLBACK`. The processes never append to or rewrite the `PRIMARY` tape. A token-price timestamp does not become an underlying stock-reference timestamp; the latter stays `UNKNOWN` unless an independent source supplies that specific clock.

## Operation

Start the separate local process before the window and keep the existing collector and watchdog running:

```sh
python3 scripts/monday_open_fallback.py once
python3 scripts/monday_open_fallback.py start
python3 scripts/monday_open_fallback.py status
python3 scripts/rwa_research.py health
python3 scripts/collector_watchdog.py status
```

The local fallback records one-minute signed Binance catalog and price snapshots for the six frozen contracts. The public path records the same six contract queries through the credential-free website endpoint plus Yahoo intraday chart responses for the three underlyings. Public website prices are labelled as a separate source and are never silently treated as signed Web3 API prices. During the opening window the local process records a primary-health snapshot every ten seconds: collector PID, watchdog PID, latest complete 40-contract slot, underlying-watch success time, UTC time and seconds since the last successful primary observation. State transitions and source failures go to append-only logs. The existing watchdog retains its own restart rules; the opening monitor adds faster detection without changing collector semantics.

The separate [GitHub workflow](../../.github/workflows/monday-open-public-fallback.yml) starts at 12:47 and 13:07 UTC on 5 October and waits for the same 13:20 to 13:45 window. Two additional runs at 20:09 and 20:27 UTC request the dated daily row as supporting evidence after the regular close. A manual `workflow_dispatch` runs a bounded public-data preflight. Each run uploads its raw responses, timestamps, normalized observations and error log as a separate artifact, even when capture fails. GitHub [documents that scheduled workflows can be delayed or dropped](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows); the early starts and repeated attempts reduce that risk but don't remove it. Check run pages and download artifacts after each window. Keep their run IDs with the evidence record.

**Preflight evidence, 2026-10-04 23:22 UTC:** Local signed capture returned six of six frozen contracts with two raw responses and no logged error. Local public capture returned six of six contract prices and three of three underlying charts with nine retained raw responses and no logged error. The separately hosted [GitHub run 37243437175](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions/runs/37243437175) also completed successfully; its downloaded artifact `monday-open-public-37243437175-1` contains six public contract observations, three Yahoo chart observations, nine raw-response manifest entries and no error row. GitHub reported artifact digest `sha256:3dbd9b72e0aacb998ab68ef2a8fccde853a619071b8dacee6a6c89b1a0b5cb23`, with retention through 18 October. These are `PREFLIGHT`, not Monday opening observations.

## Use in the frozen experiment

The scorer still reads the committed Sunday 12:00 token rows and independently dated Monday **daily regular-session open and close** rows. The fallback's Monday intraday minute bars and token snapshots are supporting observations. A separately retrieved dated daily row may be reviewed as an outcome source, with its exact session date, publisher, retrieval time and raw hash; it is never fed to the scorer automatically. Fallback observations aren't automatically substituted for a missing primary slot or a missing dated daily row. If primary collection fails, record the exact missing period, fallback acquisition time, source and raw hash in a separate finding before using any fallback observation for a claim. A minute bar must not be called the daily open merely because it was near 13:30 UTC. If the dated daily row is unavailable or ambiguous, the frozen scorer keeps its outcome null.

## Readiness and single points of failure

The local status command prints `MONDAY_OPEN_READY=YES` or `NO` with the current health fields. Readiness requires a successful six-contract signed preflight, a live primary collector and watchdog, and a separately running local fallback. Check the frozen sample hashes independently. Public workflow readiness also needs its preflight artifact visible in GitHub; confirm that separately because a local process cannot prove a future hosted schedule will fire.

Remaining single points of failure are: Mac mini power or reboot; external SSD mount and macOS background file-read permission; the Mac's network path; the shared Binance Web3 key, account quota and API service for both local processes; the public data publisher's availability and possible delay; GitHub Actions scheduling and artifact retention; and the accuracy and session date of the eventual daily historical outcome. The public GitHub runner removes the Mac dependency for public stock observations, but it doesn't independently capture Binance token prices or prove issuer reference freshness. A failed component must be reported, not silently replaced.
