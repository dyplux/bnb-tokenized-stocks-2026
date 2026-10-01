# Binance first-party capability check

**Checked:** 2026-10-01
**Purpose:** find out whether a new stock assistant, status screen or quote guard would duplicate Binance's own tools. This is a documentation review, not a product walkthrough or trade.

## Documented capabilities

| Source | What it documents | Limit of this check |
|---|---|---|
| [Binance Tokenized Securities Info skill](https://github.com/binance/binance-skills-hub/blob/main/skills/binance-web3/binance-tokenized-securities-info/SKILL.md) | An Ondo-focused workflow for token discovery, issuer metadata and attestations, market and asset status, corporate-action reason codes, token and stock data, order limits and candles. Its six public BAPI surfaces need no API key. | The skill describes endpoints and example responses. We didn't run a full user task or verify live coverage for bStocks and xStocks through this skill. |
| [Binance Agentic Wallet skill](https://github.com/binance/binance-skills-hub/blob/main/skills/binance-web3/binance-agentic-wallet/SKILL.md) | Wallet balance, gas, quote, buy and sell flows. Its ticker-resolution instructions point to RWA list types 1, 2 and 3 for Ondo, xStocks-style and bStocks. | Published instructions don't prove a route for a given token, wallet, jurisdiction, size or time. No signed request or order was made here. |
| [Binance Stock Trading guide](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading) | Stock-token lookup, quote confirmation, purchase and sale, order status and examples of persistent earnings or news-based rules. | Examples are vendor documentation. We haven't reproduced a live order, a user's setup time or net execution cost. |

## Consequence for product selection

**Inference:** a screen that lists a ticker, issuer, market session, halt reason, candles or a generic quote has little distinct value on current evidence. A news-to-buy agent also overlaps the documented Agentic Wallet path. The Ondo information skill has narrower stated coverage than the Agentic Wallet's ticker-resolution instructions, so it doesn't establish that every issuer has the same status data.

The remaining question is task-level: for a permitted small wallet with stablecoins on BNB Chain, does an existing flow leave a meaningful action unavailable, costly or unclear, and can a fresh Binance Web3 API result change that action? Use the [small-wallet task protocol](2026-10-01-small-wallet-task-protocol.md). Record an actual participant's task and an amount-specific RFQ before claiming a saving, edge or better decision. Without that observation, another wrapper around these fields would be a weak submission.

## Unknowns

- Live availability, minimum, fees and expiry for one issuer, contract, side, amount and wallet.
- Whether a participant can and wants to use Binance Spot or Agentic Wallet in their jurisdiction.
- Whether a first-party flow already explains the exact blocked or expensive action that a participant encounters.
- Whether a paid Agent Studio task has a distinct buyer. A separate prize doesn't answer this.
