# Venus Core parity probe, four additional voter entries

**Observed:** 2026-10-03 03:05 UTC. Read-only BNB Chain mainnet and [Venus governance voter API](https://api.venus.io/governance/voters?limit=5&page=0). No account address was printed or retained, and no wallet was connected.

The [probe](../../scripts/probe_venus_core_parity.py) now accepts `--voter-index 0` through `4`, with `3` as the unchanged default. It still caps each run at 35 RPC calls and five entered markets. Each invocation pins its own BNB block, so these are separate technical samples rather than one same-block cohort.

| Voter index | BNB block | Entered Core markets | Result |
|---:|---:|---:|---|
| 0 | 125409315, 03:05:19 UTC | 0 | Both current-risk tuples matched empty states; 10 RPC calls |
| 1 | 125409399, 03:05:57 UTC | 0 | Both current-risk tuples matched empty states; 10 RPC calls |
| 2 | 125409404, 03:05:59 UTC | 0 | Both current-risk tuples matched empty states; 10 RPC calls |
| 4 | later read, block not retained | 9 | Probe refused this entry because it exceeds the five-market bound; no parity conclusion |

The earlier [index 3 case](2026-10-03-venus-core-bounded-arithmetic-parity.md) remains the only nonempty parity sample. The three new exact matches are trivial empty-account checks. They do not add evidence for E-Mode, VAI repayment, a post-action forecast or an NVDAB holder. Index 4 confirms that this governor-voter discovery source can find a more complex account, but the current bounded script cannot analyze it. No extra call budget was approved merely to force that example through.

**Next proof:** an eligible consenting holder's task and address, handled outside committed records, if the founder can arrange one. Do not describe governance voters as product users or keep sampling them to imply demand. [D-030 and D-033](../decisions/decision-log.md) remain unchanged.
