# TOKENIZED STOCKS: OCT 11

**As of:** 2026-10-04 11:15 UTC. Deadline 2026-10-11 12:00 UTC, about 7 days and 45 minutes away. This is the primary workstream.

| Item | State | Evidence / next gate |
|---|---|---|
| Collector | **RUNNING** | Detached PID in `data/market_hours/collector.pid`, 5-minute cadence. Health command: `python3 scripts/rwa_research.py health`. At 11:15 UTC: 356 unique live rows, 40 contracts in the latest cycle, zero consecutive failures. Raw response bodies are stored by SHA-256 with an append-only manifest; normalized rows, checkpoints, heartbeat, error and gap logs are separate. The detached process survives terminal closure; automatic restart after a machine reboot is not established because a LaunchAgent couldn't access the external SSD. |
| DevEx | **RUNNING for new research calls** | Sanitized append-only call log in `docs/devex/raw/`; raw response bodies are stored without request headers under `data/market_hours/raw/`. The `offhours` enum has full request and raw response fixtures. Existing application calls still need migration to the wrapper. |
| RWA catalog | **INITIAL LIVE SNAPSHOT** | 618 BNB Chain rows: 488 signed `/rwa/tokens` entries and 130 xStock public listings. They form 492 provisional ticker-plus-asset-type groups and 102 cross-provider candidates. JSON and Parquet in `data/normalized/`. Ticker grouping doesn't establish economic equivalence; xStock ratio and route are unverified. |
| EXP-RWA-001 | Measured | Of 130 public xStock listings probed through signed `/rwa/price`, 77 returned null price/time and 36 of the remaining 53 had token prices older than seven days. All 130 price rows had null `platformId`. A 100-address GET returned HTTP 414; 35-address batches worked. Further issuer and attestation checks remain open. |
| EXP-RWA-002 | Measured, arithmetic only | 34 bStock/Ondo stock pairs in the signed catalog and 40 latest tape price/ratio pairs. `share_ratio_audit.csv`, `share_ratio_pairs.csv`, `results.json`. No verified rights or executable spread. |
| EXP-RWA-003 | Collecting | Live price and market status time series. The first five tickers produced 9 contracts; broadening to all 35 bStock equities plus five Ondo names yields 40 contracts in one price batch. Regular-session comparison waits for market open. |
| EXP-RWA-004 | Collecting and first analysis | Sunday live rows also copied into `data/weekend_2026-10-03_05/`; Saturday gap is not backfilled. By 11:10 UTC, nine original contracts had at least ten samples each and a median observed token-price range of about 0.060%. This is token movement, not a prediction or executable edge. |
| EXP-RWA-008 | Initial read-only cross-issuer quotes | NVDA had bStock and Ondo routes; MSTR had only bStock in six bounded calls. Indicative gross price difference isn't arbitrage or a selected routing product. |
| EXP-RWA-009 | Corrected read-only quote ladder | Eight signed quotes, 10/100/1,000/10,000 USDC for MSTRB and NVDAB, each using API-confirmed 18-decimal USDC units. Initial 6-decimal-sized calls are quarantined as invalid input units. No fills, final costs or eligibility. |
| EXP-RWA-010 | Three-part audit, reference clock unknown | `reference_freshness.csv`, `results.json`, `underlying_probe.json` distinguish token price age, weekend market-state review and missing independent reference timestamp. Zero independent reference-age observations. `tokenPriceUpdatedAt` is never used as the reference clock. An initial collector clock-order error was corrected by recomputing token age from `observed_at`; the append-only early rows remain untouched. Sunday `openState=true` and `offhours` need API clarification. |
| EXP-RWA-011 | Synthetic fixtures | Token split, stock split, rebase, unknown multiplier and halt fixtures in `experiments/EXP-RWA-011/`. Five policy tests pass; no live corporate-action event reconstructed yet. |
| Policy engine | **SKELETON** | Deterministic fail-closed `app/rwa_policy.py`; no execution authority or app integration. |
| Mainnet execution | None | No wallet signing, broadcast or funded trade. |
| Leading hypothesis | Conditional RWA policy / mandate engine | Promote only if live evidence supports a user task distinct from incumbents. Off-hours prediction is unproven. |

**Critical blockers:** independent underlying reference timestamp/source, verified issuer and action metadata, issuer eligibility, independent user task and final product selection. The existing visual prototype `app/budget-preview.html` is preserved uncommitted and hasn't been integrated. No final-product video is being made.

# SET AND EARN: NOV 5

**Deadline:** 2026-11-05 12:00 UTC. Secondary workstream in a separate private workspace.

| Requirement | Observed state |
|---|---|
| ERC-8004 | No registered agent ID observed in this workspace |
| Endpoint | None |
| Marketplace listing | None |
| Action days | 0 / 3 observed |
| Onchain actions | 0 / 5 observed |
| External completed hires | 0 / 3 observed |
| Our qualifying hires | 0 / 3 observed |
| Marketplaces used | 0 / 2 observed |

**Critical blockers:** genuine execution task, live agent, marketplace event, independent testers, continuous runtime. A Set and Earn acquisition plan and a clearly marked prelaunch page were prepared locally, without deployment or outreach. They remain secondary until the RWA data collection is stable. No fake wallets, hires or action days.
