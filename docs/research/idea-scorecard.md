# Research scorecard, 2026-10-01

**Historical first pass:** These points were assigned before the [later entrant review](2026-10-01-product-brainstorm.md). H1 no longer leads current research and no product has been selected.

The numbers order research tasks. They aren't measurements of demand or probability of winning. The [three full hypotheses](hypotheses.md) record user, trigger, evidence, alternatives, API role, minimum demo, risks, possible edge and falsifier. The [Sol critical review](../agent-reports/product-review/2026-10-01-critical-synthesis.md) challenged the two independent read-only reports before this recommendation.

## Event hard gates

| Hypothesis | BSC mainnet and spot | Central required asset | Binance Web3 API path | Working result established |
|---|---|---|---|---|
| H1. Pre-trade representation and quote receipt | Planned | bStocks and Ondo | RWA Data plus RFQ quote | No live quote yet |
| H2. Temporal quote availability monitor | Planned | bStocks or Ondo | RWA Data plus RFQ quote | No time series yet |
| H3. Pre-sign eligibility and error recovery | Planned | Could become incidental | Status plus RFQ quote | No real errors yet |

All remain provisional. No hypothesis passes the working-integration gate yet. xStocks is outside the first test because the documented RWA Data `platformId` values are only `ondo` and `bstock`; that enum doesn't prove xStocks absence from all Binance APIs.

## Weighted comparison

| Criterion | Weight | H1 | H2 | H3 |
|---|---:|---:|---:|---:|
| Severity and frequency | 20 | 2/5 | 2/5 | 2/5 |
| Evidence strength | 20 | 2/5 | 1/5 | 1/5 |
| Event and API fit | 15 | 5/5 | 5/5 | 4/5 |
| Demonstrable outcome | 15 | 4/5 | 3/5 | 3/5 |
| Differentiation | 10 | 2/5 | 2/5 | 1/5 |
| Feasibility and risk | 10 | 3/5 | 3/5 | 3/5 |
| Plausible accumulating advantage | 10 | 2/5 | 2/5 | 1/5 |
| **Weighted total** | **100** | **57** | **50** | **43** |

H1 ranks first because an issuer/contract mismatch is a concrete decision to inspect and can be shown in one receipt. Its evidence score stays low because neither pain nor a missing incumbent step has been observed. H2 needs a valid independent reference and repeated unavailable quotes. H3 is useful as error handling but Agentic Wallet already documents status and confirmation.

## Decision

Investigate H1 first with NVDA in bStocks and Ondo. Treat H3 as a safety requirement, not a second product. No application build or final name is approved. The main dissent remains open: PancakeSwap and Agentic Wallet may already give the user everything needed. A same-task comparison and a reproducible Binance quote can reject H1. [Problem brief](problem-brief.md) defines the test and stopping rule.
