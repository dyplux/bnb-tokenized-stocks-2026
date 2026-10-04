# Shared safety core for a later rebalancing agent

**Scope, 2026-10-04:** interface contract only. This is not a deployed agent or a qualifying Set and Earn action. Tokenized Stocks remains the active build. The Set and Earn workspace is separate; it keeps its own identity, wallet, marketplace, credentials and evidence.

The reusable part is the deterministic [policy result](../../app/rwa_policy.py): `intent`, `mandate`, dated `evidence`, `decision`, `reason_codes`, `policy_version` and `receipt_sha256`. The [local safety service](../../app/safety_service.py) currently supplies this for one NVDA buy review. A [JSON-in/JSON-out adapter](../../scripts/safety_agent_tool.py) exposes the exact same read-only review to a local agent runtime. It accepts only four action and mandate fields, never a wallet secret. It has no execution permission and normally returns `NEED_HUMAN` for an anonymous user.

Example input on stdin, with the local signed API credentials available only to the process: `{"provider":"bstock","notional_usdt":"100","max_notional_usdt":"100","max_price_impact_percent":"0.5"}`. Exit code 0 means a policy receipt was produced, **not** that the action was allowed. A source or input error has a nonzero exit code and no decision receipt.

A genuine rebalancing wrapper would need to add, in order:

1. A user-owned portfolio, target weights and a bounded rebalance trigger. Price drift alone is not permission to trade.
2. One exact proposed action per leg, with fresh chain, contract, holder-access and liquidity evidence passed through this policy. `DENY` and `NEED_HUMAN` halt that leg.
3. A funded same-wallet quote, build and simulation, then the explicit per-action human or delegated mandate approval required by the final safety design.
4. A bounded signer with pre/post balance proof and on-chain transactions consistent with the declared rebalancing task.
5. Separate ERC-8004 ownership, public endpoint uptime, marketplace listing, independent hires and distinct action-day evidence for Set and Earn.

The wrapper must not translate the screen's temporary-wallet quote into a spend instruction, silently waive the unknown stock-reference clock, or treat an agent's text as execution authority. No Set and Earn qualification counter advances from a local policy receipt. This boundary can be implemented after the October 11 product path is stable without coupling the two repositories.
