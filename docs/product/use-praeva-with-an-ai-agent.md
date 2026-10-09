# Use Praeva with an AI agent

Praeva's local adapter is a small stdin/stdout tool. It accepts one JSON object and returns one JSON result. The adapter doesn't claim native MCP support, and it doesn't sign or broadcast transactions.

## Start the local review screen

From the public project root, run:

```sh
python3 app/safety_server.py
```

Open `http://127.0.0.1:8001`. This local browser UI has a dated fixture and a fresh review path; it differs from the published static console. It doesn't provide a desktop executable. A fresh **Review action** uses your own Binance API credentials and a fresh read. Never share those credentials in chat.

## Copy-paste prompt for a local agent

Give this prompt to an agent that can run local commands:

```text
Run the local Praeva safety tool with one JSON object on stdin.
Use provider "bstock", notional_usdt "10", max_notional_usdt "10", and max_price_impact_percent "0.5".
Run only this command from the project root:
printf '%s\n' '{"provider":"bstock","notional_usdt":"10","max_notional_usdt":"10","max_price_impact_percent":"0.5"}' | python3 scripts/safety_agent_tool.py
Read the JSON result. Report decision, reason_codes, receipt.receipt_sha256, and any error.
Do not sign, broadcast, retry, or paste API secrets. A returned decision doesn't approve a purchase.
```

If the tool returns an error or exits nonzero, report that failure; don't invent a decision or reuse an earlier receipt. The local adapter uses stdin/stdout. A fresh signed read requires the user's own `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` in the ignored `.env` or process environment. It supports `provider="bstock"` for NVDAB and `provider="ondo"` for NVDAon, with amounts from 10 to 1,000 USDT. Never put them in the prompt or send them to chat.

## Verify a saved receipt offline

The saved fixture can be checked without credentials:

```sh
python3 scripts/verify_receipt.py docs/judge/observed-unsafe.json
```

The result separates canonical integrity from replay. The dated fixture is useful for review. It isn't a fresh market read and it doesn't prove authenticity by itself.

## Safety boundary

`NEED_HUMAN` means evidence or authorization is unresolved. `DENY` means the policy found a rule failure. A synthetic `ALLOW` is a code-path fixture. The local tool doesn't hold a wallet key, and it doesn't make a stock purchase.
