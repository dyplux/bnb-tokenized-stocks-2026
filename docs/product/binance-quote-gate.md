# Binance Web3 sell quote gate

**Prepared:** 2026-10-01. **Runtime status:** the local app contains signed read-only RWA search and quote request paths, but neither has run with credentials. The exact identity check in step 2 is implemented as a gate before the quote. This is a bounded integration plan for the [cash-choice spec](one-page-spec.md), not evidence that a sell route exists.

## Task and inputs

An eligible NVDAB holder enters a public BNB Chain address, NVDAB units available to sell and a USDT cash target. The current local app can read the ERC-20 balance at one block and display an indexed Venus borrowing scenario. A valid sell comparison needs a fresh, wallet-bound Binance Web3 quote for the **same units**, with any difference from the cash target visible. The address doesn't establish control or jurisdiction eligibility.

## Read-only integration sequence

1. Load the complete `BINANCE_WEB3_API_KEY` and `BINANCE_WEB3_SECRET_KEY` from the ignored private `.env` on the server. Keep both out of browser code, HTTP responses, logs and commits. The [authentication guide](https://web3.binance.com/en/dev-docs/authentication) requires `X-OC-APIKEY`, an ISO timestamp and `X-OC-SIGN` over a path that includes `/build` and the exact query string.
2. Make one signed exact-ticker [RWA search](../research/rwa-probe.md). Accept NVDAB only if the response identifies chain 56, the pinned contract `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436`, and the bStock platform. Record latency, API business code and a redacted identity result. A malformed response blocks the quote.
3. Convert the entered token units to an integer raw amount using `decimals()` read from the NVDAB contract at a recorded block. The [Trading API quote](https://web3.binance.com/en/dev-docs/llms-full.txt) takes `binanceChainId=56`, the pinned NVDAB and USDT contracts, `amount` in smallest units and `userWalletAddress` for RFQ routes. Make one signed `GET /api/v1/dex/aggregator/quote`. No `/swap`, approval, order or broadcast belongs in this gate.
4. Treat HTTP 200 with a non-zero Binance business `code` as an error. Distinguish missing credentials, authentication, region, market hours, unsupported pair, no liquidity, rate limit and malformed route. Record codes and latency without raw signed URLs, headers, quote IDs or wallet addresses. An empty route list means **no observed route**, not a zero-price sale.
5. A bStock can return both `SWAP` and `RFQ` routes, according to the [official execution guide](https://web3.binance.com/en/dev-docs/llms-full.txt). Preserve each route's mode and vendor; never infer mode from the ticker. The documentation says a route `quoteId` lasts about 30 seconds. Do not expose it in a dated receipt or promise an executable quote after expiry.
6. Confirm with an actual response whether `fromTokenAmount`, `toTokenAmount`, gas and fee fields are in base units or display units, and what costs are included. Only after that confirmation may the UI convert a route to USDT proceeds and compare it with the user's target. If units or net cost remain uncertain, show **route observed, proceeds unverified**.

## Release gate

One permitted holder-sized signed response, with raw evidence in an ignored local path, must establish token identity, route mode, amount units, quote freshness and error handling. The [DX field log](../dx/field-log.md) must receive the actual UTC time, latency, code, selected fields and limitation. A quote is an estimate; it does not establish a fill, net settled proceeds, profit or user eligibility. The current secret supplied in chat was truncated and no complete key pair is present in this private repo, so this gate cannot be completed yet.
