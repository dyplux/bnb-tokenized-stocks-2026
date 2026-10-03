# First post-Friday-close NVDAB quote protocol

**Prepared:** 2026-10-02 23:31 UTC, before the requested measurement. **State:** the one bounded read-only probe completed at 2026-10-03 00:02 UTC. See the separate [result](2026-10-03-after-friday-close-quote.md); this protocol preserves the question and method defined before the call.

## Question

Does Binance Web3 return a technical NVDAB to USDT route after Nasdaq's Friday 20:00 New York post-market close? [Nasdaq's current-hours page](https://www.nasdaq.com/23-5-trading), checked 2026-10-02, says its existing market runs from 04:00 to 20:00 Eastern and that the proposed 23-hour session is expected in December 2026, subject to approvals. This check concerns the exchange's published hours, not every broker or alternative trading venue.

## Fixed method and limits

- Use the existing [single-quote probe](../../scripts/probe_binance_quote.py) once, after 00:02 UTC on 3 October, with chain 56, pinned NVDAB and USDT contracts, exactly 1 NVDAB in raw units, and a newly generated temporary nonholder address. The probe loads the ignored project credentials, sends a signed read-only GET, blocks redirects and emits a sanitized result without the wallet, headers, signature or `quoteId`.
- Capture local UTC response time, HTTP/business status, latency, route count, vendor, execution mode, raw estimated output, `tradeFee` and `estimateGasFee` if present. A missing route or error remains an observation, not a zero price.
- No approval, unsigned build, simulation, signature, broadcast or trade. No holder or jurisdiction eligibility is inferred from the temporary address.

## Interpretation gate

A successful quote would show only that one vendor returned an estimate during this clock interval. It wouldn't prove an executable sale, fill, net proceeds, tradable spread, superior access against every broker or a reason to choose a loan. A failure might be pair, vendor, API or regional state; its business code must be recorded before assigning cause. Compare with the [Friday 17:15 New York quote](2026-10-02-after-regular-close-quote.md) only as two dated observations, not as a controlled price experiment.
