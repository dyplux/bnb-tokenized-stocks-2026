-- Research only. Paste into Dune and run manually; this query has not run.
-- Fixed window: 2026-10-02 00:00 to 2026-10-03 04:00 UTC.
-- A green transaction can still return a nonzero Venus protocol error code.
-- Inspect output, revert reason and relevant receipt logs before assigning a cause.
-- The 200-row limit is a review bound, not a complete count of attempts.

SELECT
    block_time,
    block_number,
    tx_hash,
    trace_address,
    success AS call_success,
    tx_success,
    input AS call_input,
    output AS call_output,
    error,
    revert_reason
FROM bnb.traces
WHERE block_date >= DATE '2026-10-02'
  AND block_date < DATE '2026-10-04'
  AND block_time >= TIMESTAMP '2026-10-02 00:00:00'
  AND block_time < TIMESTAMP '2026-10-03 04:00:00'
  AND "to" = 0xeb8ca841cbe1bc4832a10b15c7dab1081edad371
  AND type = 'call'
  AND varbinary_starts_with(
      input,
      varbinary_substring(keccak(to_utf8('mint(uint256)')), 1, 4)
  )
ORDER BY block_time DESC, tx_hash
LIMIT 200;
