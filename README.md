# BNB tokenized stocks project

Working repository for a new Dyplux entry to [BNB Hack: Tokenized Stocks Edition](https://www.bnbchain.org/en/hackathons/tokenized-stocks). The provisional product test compares an NVDAB sale with a Venus USDT borrowing scenario for the same cash target.

## Run the read-only Venus scenario

Requires Python 3.9 or newer and no installed packages. From the repository root, run:

```sh
python3 app/server.py
```

Open `http://127.0.0.1:8000`. Enter NVDAB units and a USDT target, then select **Fetch scenario**. Each request retrieves an indexed snapshot from the public Venus API. The JSON endpoint is `GET /api/scenario?units=1&cash=100`.

An optional public wallet address reads the NVDAB ERC-20 balance through the [official BNB Chain mainnet RPC](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/). The server checks chain ID 56, reads contract code and `decimals()` metadata, then calls `balanceOf` at one recorded block. It reports that balance and whether it covers the entered sale units. RPC failure leaves the balance unknown. The address is sent in a POST body, not a URL. The public RPC receives the address in the balance request; this app does not write it to application logs or storage. A public address does not prove ownership or jurisdiction eligibility. This read does not inspect Venus positions.

The Venus panel remains a market-level illustration only, with no wallet debt or collateral, Binance Web3 integration, sell quote, order, transaction, or execution. The sale card says **Unquoted** and reports no proceeds. Borrow capacity, hypothetical health factor, liquidation-price stress, pool cash and flat-rate interest figures use isolated assumptions and do not establish personal safety or guarantee borrowing. [Venus says its indexed API can lag chain state](https://github.com/VenusProtocol/venus-protocol-documentation/blob/main/services/api.md); inspect the displayed source and retrieval time.

## Research record

Research starts with one user task, current alternatives and the event's required Binance Web3 API integration. [Project brief](docs/00-project-brief.md), [verified event rules](docs/01-event-rules.md), [API map](docs/api-map.md), [current status](docs/status.md) and [decision log](docs/decisions/decision-log.md) record evidence and stopping conditions. The current application slice is provisional and does not validate demand or product advantage.

Bell is a separate CoinMarketCap hackathon project. This repository shares no code, credentials, data or deployment with Bell.
