# Plus Luna approval arithmetic review

**Date:** 2026-10-03 UTC. **Task:** check the gas product and claim boundary in the [NVDAB approval read](../../research/2026-10-03-nvdab-approval-result.md). The isolated `codex-plus` profile used `gpt-5.6-luna` read-only with no tools or file reads. The reviewer received only the selected, sanitized response fields.

- **Finding:** 70,000 × 58,045,851 = 4,063,209,570,000 wei = 0.00000406320957 BNB. This is a full-limit product at the supplied gas price, not gas paid.
- **Counterargument and limit:** a constructed approval doesn't show a holder needs it, can execute the subsequent swap or will pay that amount. No holder state or transaction was reviewed.
- **Recommendation and decision impact:** keep the phrase "full-limit gas product" and leave D-033 unchanged. The primary proof is the [sanitized API receipt](../../research/receipts/2026-10-03-nvdab-approval.json), not this model review.
- **Consumption:** CLI reported 7,168 tokens; no quota balance or account email was exposed. This was too costly for a simple arithmetic check, so the next narrow verification should use direct arithmetic and source data without an additional model pass.
