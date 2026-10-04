# Live RWA collector operations

The collector runs every 300 seconds while the Mac is awake. Each cycle makes one signed BNB Chain RWA catalog call and one batched price call for 40 stock contracts. The [price endpoint](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data) allows up to 100 addresses per request. The 40-contract universe contains 35 bStock equities and five Ondo equities (AAPL, NVDA, TSLA, COIN, MSTR). xStocks remain catalog-only because the signed RWA pricing route hasn't been established for them.

```sh
python3 scripts/rwa_research.py start --interval 300
python3 scripts/rwa_research.py health
```

`start` detaches the loop from its terminal. An exclusive lock prevents a second loop. `health` prints `last_success_at`, `last_attempt_at`, `consecutive_failures`, `observation_count`, `contracts_sampled` and `next_expected_run`; it exits nonzero if the process is missing or more than 60 seconds overdue. The process PID is in `data/market_hours/collector.pid`; its stdout and stderr are in `data/market_hours/collector.log`.

Raw API response bodies are stored as gzip files named by SHA-256 in `data/market_hours/raw/`. `raw/manifest.jsonl` is append-only and records every captured response. No request headers or signatures are retained. Sanitized call-level DevEx records go to `docs/devex/raw/YYYY-MM-DD.jsonl`. Normalized `LIVE` observations go to `data/market_hours/YYYY-MM-DD.jsonl` and, within the event window, `data/weekend_2026-10-03_05/`. The checkpoint and heartbeat use atomic replacement. Sample IDs combine time slot and contract, so restarting within a slot doesn't duplicate normalized observations. `gaps.jsonl` and `errors.jsonl` record missed slots and failures. Rate-limit responses (HTTP 429 or business code 42900) receive at least 15 minutes of backoff; other consecutive failures use exponential backoff up to one hour. The API's `Retry-After` seconds can lengthen the delay.

No `BACKFILLED` observations have been created. Any future backfill must identify its source, acquisition time and original event time separately. The Saturday 3 October gap remains visible.

**Operational limit:** a macOS LaunchAgent trial failed to access this external SSD because of background-process permissions. The detached collector survives terminal closure, but automatic startup after reboot hasn't been demonstrated. After a reboot or SSD remount, run the health command and then `start` if health reports a dead process. The next successful cycle records the resulting gap. A Mac sleep period also interrupts collection.
