# Developer experience lessons

Last verified: 2026-10-05. Scope: 4 October signed/API and RPC observations. Canonical owner/source: [611-call fixed cut](../devex/2026-10-04-evidence-summary.md) and linked repros. Supersedes: none. Status: HISTORICAL.

| Expectation | Observation and reproduction | Impact / workaround / suggested improvement |
|---|---|---|
| Market enum documents all states | Signed 488-row catalog returned 31 `offhours` Ondo rows; [repro](../devex/repros/2026-10-04-market-status-enum.md). | Unknown state must fail closed; document enum and venue semantics. |
| Up to 100 addresses per price request works | 4,597-character GET got HTTP 414; 35/35/35/25 batches worked; [repro](../devex/repros/2026-10-04-rwa-price-url-limit.md). | Client batches conservatively; document URL limit or offer POST batch. |
| All RWA routes use RFQ per endpoint reference | NVDAB and broader Sunday quotes labelled `SWAP`; Trading introduction already mentions bStock SWAP; [repro](../devex/repros/2026-10-04-rwa-swap-route.md). | Record mode, avoid a blanket docs-defect claim; reconcile reference and introduction. |
| Underlying reference has an independently dated clock | Inspected signed price, market, profile and public stock info fields supplied no independent upstream timestamp; [repro](../devex/repros/2026-10-04-independent-reference-clock.md). | Keep reference age `UNKNOWN`; add upstream source and as-of field if available. |
| A quote proves a user can act | Read-only routes were available without verified individual access; [eligibility gap](../devex/repros/2026-10-04-bstock-eligibility-documentation-gap.md). | Separate route and holder eligibility; document exact eligibility check. |
| HTTP/API success means a simulated transaction passes | Unsigned build and simulation API answered, but unfunded nested prediction failed; [repro](../devex/repros/2026-10-04-unsigned-build-simulation.md). | Inspect nested result; clarify envelope versus execution outcome in docs. |
| Our first input units and age calculation were sound | Six-decimal USDC assumption and cycle-start clock arithmetic were our bugs; [units](../devex/repros/2026-10-04-bsc-usdc-decimals.md), [clock](../devex/repros/2026-10-04-token-age-clock.md). | Corrected units and per-row observed-time arithmetic; keep raw rows, test both locally, don't blame the API. |

The fixed cut mixes collector and exploratory calls. It isn't an endpoint reliability benchmark or a human-developer interview.
