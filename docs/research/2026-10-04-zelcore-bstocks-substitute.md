# ZelCore as a bStock purchase substitute

**Source check:** 2026-10-04 UTC. This is a review of ZelCore's public product documentation, not an independent live wallet test. The documents may change before judging.

## Documented workflow

ZelCore's [bStocks guide](https://docs.zelcore.io/docs/guides/bstocks-tokenized-stocks-guide/) describes a self-custodial BSC wallet, a bStock asset list, Binance Web3 and other swap providers, transaction history, and a server-side country check. Its [desktop walkthrough](https://docs.zelcore.io/docs/walkthroughs/bstocks-desktop/) shows a 10 USDT MSFTB purchase path with provider selection, a transaction summary, a separate first-time token approval, swap submission and a later completion state. The walkthrough calls the rate floating and labels the received amount estimated. The guide says a Binance account isn't required for that self-custodial swap, while access still depends on jurisdiction.

The guide states that ZelCore hides bStock acquisition and swap controls when its country check fails, and that it sources restricted-country data from Binance. The exact issuer endpoint and schema aren't given there. This is ZelCore's documented implementation, not proof that the founder in Portugal is eligible or that Dyplux can reuse ZelCore's compliance result.

## Impact on the Dyplux decision

| Claim or task | What the source changes | Current Dyplux evidence |
|---|---|---|
| “Buy a bStock without a Binance exchange account” | ZelCore already documents that path. It isn't a defensible standalone novelty claim. | Our own exact-wallet quote, unsigned build and unfunded simulation are read-only. |
| “Check country before exposing a trade” | ZelCore already documents a fail-closed regional check. We cannot claim the basic pattern as unique. | Dyplux leaves holder access `UNKNOWN` and blocks approval because the issuer endpoint and individual eligibility remain unverified. |
| “Show a quote and estimated output” | ZelCore already shows competing providers and a transaction summary. | Dyplux's different task is to bind a proposed action to a policy receipt, exact route identity, independent clock status, multiplier state and simulation. The complete funded user benefit is still unproven. |
| “Use a returned quote as execution proof” | ZelCore's own walkthrough separates estimated output, approval, submission and completion. | Dyplux also keeps those stages separate; its current simulation predicts failure for an unfunded wallet. |

## Remaining uncertainty and next check

We haven't run ZelCore with a consenting eligible wallet, measured its exact safety warnings for an `offhours` token, or confirmed that it displays an independent stock-reference timestamp or corporate-action check at the point of approval. Absence from its guide isn't proof of absence from the product. A same-action walkthrough would be needed before claiming a product advantage. The issuer's current country endpoint and venue terms remain the gate for any Dyplux mainnet demo; ZelCore's public guide doesn't settle them.
