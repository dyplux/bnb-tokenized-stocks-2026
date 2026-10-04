# Judge run: one stock-token action

**State:** local read-only build, checked 2026-10-04. Use Python 3.9+ and your own Binance Web3 API key and secret in a Git-ignored `.env` or process environment. No wallet, Binance account or private key is needed for the screen. The API can change between this note and judging.

1. Run `python3 app/safety_server.py` and open `http://127.0.0.1:8001`.
2. Select **NVDAB**, set the action to **10 USDT** and the mandate to **10 USDT maximum**. Leave price impact at **0.5%**. Select **Review action**.
3. Read the exact NVDA contract and market state. Compare **token price last updated** with **underlying reference age**. The latter should remain `UNKNOWN` unless an independent timestamp has actually been supplied. Read the fixed-block multiplier, quote mode, access and simulation states.
4. Open the receipt JSON. It contains `policy_version`, reason codes, source capture times and response hashes. A route quote is evidence of a route response, not holder eligibility. The screen must not offer a sign or buy control.
5. Repeat with **NVDAon**. The public stock-info feed can show a distinct stock price, but currently no independent as-of time; its reference age must remain `UNKNOWN`.

**Bounded failure case:** set **100 USDT** as the action and **20 USDT** as the mandate maximum. The policy must return `DENY` with `MANDATE_LIMIT_EXCEEDED` even if an API route appears. If a source fails, the check must expose the missing evidence and not return a success-looking blank result.

**What the reviewer can establish:** one real read-only BNB Chain data flow, a deterministic policy boundary, captured source provenance and safe unknown states. This run doesn't establish issuer access for any person, a funded simulation, trade execution, savings, return or Monday opening-price accuracy. The [frozen Monday protocol](../../experiments/EXP-RWA-004/monday-open-protocol.md) evaluates the separate off-hours hypothesis after the market opens.
