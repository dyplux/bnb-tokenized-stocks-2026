# Corporate-action source audit, 4 October 2026

## Confirmed issuer events

- [CrowdStrike](https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-first-quarter-fiscal-year-2027-financial) announced a four-for-one stock split on 3 June 2026, effective for split-adjusted trading on 2 July 2026.
- [Netflix](https://ir.netflix.net/investor-news-and-events/financial-releases/press-release-details/2025/Netflix-Announces-Ten-For-One-Stock-Split/default.aspx) announced a ten-for-one split on 30 October 2025, with split-adjusted trading expected from 17 November 2025.
- [Ondo's product FAQ](https://ondo.finance/ondo-stocks) says stock splits are reflected in its tokens to preserve economic exposure, and minting/redemption may pause briefly around corporate actions.

## Live token snapshot

The signed Binance Web3 catalog captured on 4 October 2026 reported `CRWDon` at a token/share ratio of `4` with token price `$4,321.655808` and derived per-share reference `$1,080.413952`. It reported `NFLXon` at ratio `10`, token price `$6,706.2353` and derived per-share reference `$670.62353`. These values and the issuer split factors have the same numerical multipliers.

**Limit:** the catalog is a single 2026 snapshot. It contains no token ratio or token price from before either split and no signed issuer-specific token action notice for those dates. The matching factors don't prove that Ondo changed either ratio because of the split, nor that a trader saw a false opportunity. EXP-RWA-011's split/rebase cases remain labelled synthetic. The next evidence gate is a dated pre/post token ratio and issuer action record, or a current observed ratio change in the live tape with a matching verified source.

## Signed profile probe, 4 October 2026

Two logged, read-only calls to Binance Web3 `GET /api/v1/dex/market/rwa/underlying-profile` returned current Ondo ratios of `4` for CRWD and `10` for NFLX. The [probe summary](profile_probe.json) records the contracts, capture times, field names and SHA-256 hashes. Exact response bodies are retained as [CRWD](../../docs/devex/fixtures/2026-10-04-crwd-underlying-profile-raw.json) and [NFLX](../../docs/devex/fixtures/2026-10-04-nflx-underlying-profile-raw.json) fixtures. Both profiles exposed `tokenToShareRatio`, company information and daily/monthly attestation links. Neither response included a corporate-action event, ratio-change timestamp or independent reference-price timestamp. The two assets shared the same attestation links; this probe didn't inspect the linked reports or establish per-asset attestation.

The profile probe closes one possible source of a dated split record inside the current Web3 API. It does not establish that no issuer record exists elsewhere. Keep the synthetic guard's `UNVERIFIED_RATIO_CHANGE` state and the live split claim unproven.
