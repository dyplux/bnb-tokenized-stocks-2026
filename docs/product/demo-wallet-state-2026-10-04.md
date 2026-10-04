# Demo wallet funding and approval read

**Observed:** 2026-10-04 17:03:30 UTC, BNB Chain block 125712975. **Action:** the [16:58 UTC unsigned NVDAB packet](pre-execution-packet-linked-2026-10-04.json), 10 USDT input. `python3 scripts/read_demo_wallet_state.py` loaded the packet and the retained response bodies by SHA-256, checked that the policy, quote and unsigned build describe the same action, then read public balances and allowance at one fixed block. The local response is ignored at `data/market_hours/demo_wallet_state.json`; it doesn't retain the wallet address in its summary. The script has no signing or broadcast method.

| Read | Result |
|---|---:|
| USDT balance | 0 |
| BNB balance | 0 |
| USDT allowance to quoted approval target | 0 |
| Quoted input | 10 USDT |
| Unsigned swap's gas-limit times gas-price ceiling | 0.00002439733905 BNB |
| Approval target has contract code at block | Yes |

The wallet therefore can't pass a funded simulation now. An approval transaction would need its own gas, and the quoted route may expire before funds arrive. The gas product is a bound from one unsigned build, not a final paid network cost. The read doesn't establish eligibility to acquire or hold NVDAB. It gives no reason to transfer capital until that access question is resolved and a fresh same-quote preflight is available for the founder's review.

**Next gate:** obtain a dated bStock access basis for the founder and route, then use a fresh quote and same-wallet build. Read the spender and allowance again, estimate any approval separately, and simulate after funding. The policy still needs an independently timed reference or an explicit mandate choice, a regular market state, issuer verification and a passing simulation before it can return `ALLOW`. A specific human approval is required even after those checks.
