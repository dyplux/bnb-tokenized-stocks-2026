# Exact public demo-wallet dry run, no transaction

**Observed:** 2026-10-04 15:10 UTC. **Experiment:** `EXP-RWA-009/EXACT-WALLET-DRY-RUN`. The command `python3 scripts/prepare_exact_wallet_simulation.py --provider bstock` extracted `BNB_STOCKS_DEMO_ADDRESS` from the ignored local `.env`; it doesn't parse, use or print the private-key field. It requested one 10 USDT to NVDAB BSC quote for that address, built its unexpired `SWAP` route as an unsigned transaction, and sent the same unsigned calldata to Binance's off-chain simulation endpoint. The local full summary is ignored at `data/market_hours/exact_wallet_simulation.json` and retains no wallet address, quote ID or calldata.

| Step | API/business result | Observed outcome |
|---|---|---|
| Quote | Code `0`, one route | `LiquidMesh`, `executionMode=SWAP`; raw response SHA-256 `6bb9f2ab3424d819670e276dbe8d24d19243441788a2863e941ce5e9e5029199` |
| Unsigned build | Code `0` | Transaction `from` matched the exact public demo address; `to` and hexadecimal calldata were present. Raw response SHA-256 `8b2b2cbe62ea27d6191785e4c45f0394b88410bb680979606da094ee4823bc9b` |
| Off-chain simulation | API code `0` | Predicted transaction status `FAILED`: `BEP20: transfer amount exceeds balance`. Raw response SHA-256 `496889fdbbb3790d48fb262ada6d7dbc20885fc2880f2bf08773d6a5e5ff8705` |

The simulated failure is consistent with an unfunded demo address. This shows the three technical calls can refer to one public address; it does **not** prove eligibility, router/spender safety, successful funded execution, a fill or a reusable quote. The script has no signer or broadcast function. The product policy remains `NEED_HUMAN` or `DENY`, and no capital has moved.
