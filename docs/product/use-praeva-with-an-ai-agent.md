# Use Praeva with an AI agent

Praeva exposes the existing Praeva safety service through a small Model Context Protocol stdio process. It has three read-only tools:

- `praeva_replay` reads one of three fixed judge fixtures. It never calls a network service.
- `praeva_verify_receipt` verifies receipt JSON supplied in the request. It accepts an optional expected SHA-256 and never accepts a filesystem path.
- `praeva_assess` validates a four-field action request and performs the existing Praeva live review for `bstock` or `ondo`, from 10 to 1,000 USDT. It requires the local Binance Web3 credentials, permits at most four live tool calls per rolling minute, and never signs or broadcasts.

The server runs locally over stdio. It has no wallet or payment capability. The synthetic `ALLOW` case is a policy fixture only. A live result remains a read-only review result.

## Run it over stdio

Use Python 3.9 or newer and the absolute path to the existing Praeva checkout. The placeholder below is intentional:

```json
{
  "mcpServers": {
    "praeva": {
      "command": "python3",
      "args": [
        "ABSOLUTE/PATH/scripts/praeva_mcp.py",
        "--praeva-root",
        "ABSOLUTE/PATH/to/bnb-tokenized-stocks-2026"
      ]
    }
  }
}
```

The MCP client must use newline-delimited JSON on stdin and stdout. The server negotiates protocol version `2025-06-18`, then expects `notifications/initialized` before `tools/list` or `tools/call`. A client that sends another protocol version receives the supported version in the initialize result and can stop.

The process writes protocol responses to stdout. Diagnostic lines use fixed codes on stderr. Message lines, including requests and responses, are limited to 64 KiB. Duplicate JSON keys and non-finite JSON numbers are rejected.

## Example prompt

> Replay the observed NEED_HUMAN Praeva case, verify its receipt hash, then explain the decision and its limits. Do not make a live call.

For a live review, make the intent explicit:

> Run one read-only Praeva assessment for a 100 USDT `bstock` request with a 100 USDT mandate and a 0.5 percent price-impact limit. Use local credentials only. Do not sign, broadcast, retry, or place an order.

## Live request shape

The only accepted fields are:

```json
{
  "provider": "bstock",
  "notional_usdt": "100",
  "max_notional_usdt": "100",
  "max_price_impact_percent": "0.5"
}
```

Validation remains owned by `app.safety_service.review`, including provider names and amount bounds. Credentials are checked before the existing review is imported for a live call. Missing credentials return `CREDENTIALS_REQUIRED`. Review failures return a generic `LIVE_REVIEW_ERROR`; secret or adapter exception text isn't returned to the client.

## Receipt verification

Pass the parsed receipt object, not a path:

```json
{
  "receipt": {
    "policy_version": "0.6.0",
    "timestamp": "..."
  },
  "expected_sha256": "optional-64-character-lowercase-or-uppercase-hex"
}
```

The wrapper reuses `scripts/verify_receipt.py`. Its result separates canonical integrity and saved-input replay. Authenticity needs a trusted expected hash. It doesn't modify receipts or add policy thresholds.

## Scope and conformance note

This is a narrow wrapper for the Praeva checkout. It covers the MCP methods and lifecycle needed by this adapter, with newline JSON transport and read-only tool annotations. It makes no universal MCP client or server conformance claim. Offline protocol tests and repository CI cover the documented paths; installed client-specific setup still depends on that client.

## Terminal agents

The existing `scripts/safety_agent_tool.py` remains available as JSON on stdin/stdout. Start with offline `praeva_replay` and `praeva_verify_receipt`; use `praeva_assess` only for an explicit fresh review with your own credentials configured in the ignored `.env`. No API secret belongs in an MCP prompt or a committed config.

The MCP observed DENY fixture is the dated NVDAB mandate denial. The console also shows a separate dated SPYon denial. These are distinct captures, rather than interchangeable current market evidence.
