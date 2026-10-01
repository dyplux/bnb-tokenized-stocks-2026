# Venus scenario slice builder report

**Date:** 2026-10-01

Implemented `app/server.py`, `app/index.html` and updated `README.md` for a local, read-only NVDAB versus USDT scenario. The server binds to `127.0.0.1`, fetches the public Venus market API once per calculation, selects NVDAB and USDT by verified underlying contract on chain 56, requires a unique USDT market in the NVDAB market's pool, and validates listing, collateral, prices and USDT borrowability. Collateral capacity, health factor and liquidation stress convert USD oracle values to USDT units using the USDT oracle price. Inputs are bounded to avoid extreme Decimal magnitudes. The UI says Venus API values are indexed, can lag the chain and are not transaction-safety data; pool cash does not guarantee a borrow. The sale remains explicitly unquoted.

**Limits and risks:** the [Venus API documentation](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/services/api.md) warns indexed data can lag and is not authoritative for live prices, market pause state or liquidation safety. This slice has no account-wide Venus state, Binance Web3 quote, E-Mode, execution costs or personal safety conclusion. The simplified health factor excludes other positions and protocol protections. No tests or build commands were run, as requested.

## Optional wallet balance read

Added a separate `POST /api/balance` flow. It accepts the public address and entered NVDAB units in the request body, verifies `eth_chainId` is 56, chooses one block number, reads NVDAB contract code and `decimals()` at that block, requires 18 decimals, and calls `balanceOf` at that same block. The UI shows exact token units, block number/tag and block time, plus whether the entered units are covered. Failed RPC or metadata validation leaves the balance explicitly unknown. App access logs do not include POST bodies, response data omits the address, and the browser does not persist it. The public RPC receives the address in `balanceOf` calldata.

The public address is not proof of address control, product eligibility or jurisdiction. The Venus scenario remains isolated and has no wallet debt/collateral or personal liquidation calculation. The [official BNB Chain endpoint documentation](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/) lists the configured mainnet RPC and chain ID 56. No tests or build commands were run.
