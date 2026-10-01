# Venus scenario slice builder report

**Date:** 2026-10-01

Implemented `app/server.py`, `app/index.html` and updated `README.md` for a local, read-only NVDAB versus USDT scenario. The server binds to `127.0.0.1`, fetches the public Venus market API once per calculation, selects NVDAB and USDT by verified underlying contract on chain 56, requires a unique USDT market in the NVDAB market's pool, and validates listing, collateral, prices and USDT borrowability. Collateral capacity, health factor and liquidation stress convert USD oracle values to USDT units using the USDT oracle price. Inputs are bounded to avoid extreme Decimal magnitudes. The UI says Venus API values are indexed, can lag the chain and are not transaction-safety data; pool cash does not guarantee a borrow. The sale remains explicitly unquoted.

**Limits and risks:** the [Venus API documentation](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/services/api.md) warns indexed data can lag and is not authoritative for live prices, market pause state or liquidation safety. This slice has no wallet state, Binance Web3 quote, account-wide Venus data, E-Mode, execution costs or personal safety conclusion. The simplified health factor excludes other positions and protocol protections. No tests or build commands were run, as requested.
