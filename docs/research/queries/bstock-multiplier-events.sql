-- Research only. Paste into Dune and run manually; no Dune API execution.
-- Checked 2026-10-01 against the BEP-677 event signature and DuneSQL docs.
-- Window covers two Binance September 2026 corporate-action announcements.
-- A scheduled update is not necessarily effective at block_time.
-- Empty results in this window do not prove that the contracts never changed.

SELECT
    CASE contract_address
        WHEN 0x205812cdbed920aff76c6580abd681a46d11efc7 THEN 'QQQB'
        WHEN 0x7425889fe94f9d693e8daefe88bcced6acfef4c0 THEN 'METAB'
        WHEN 0x76682c454467b3a1150ad8b6a92fc5ee2c21d7ed THEN 'AVGOB'
        WHEN 0x2e065f65f1699964f4092de1d39a8efe6c8d6f32 THEN 'STXB'
        WHEN 0x25e572b466d152604d9e6c3e53b432b978825342 THEN 'SQQQB'
        WHEN 0xe28cd11c99af2df76bb8ada4cd0ef3904378280f THEN 'SOXSB'
        WHEN 0x0bb3fa77e0809f42948e435f04883c25415e8263 THEN 'MUUB'
        WHEN 0x462b5f13b7c7748279358962925c5de83bb9e598 THEN 'TQQQB'
    END AS ticker,
    contract_address,
    block_time AS announced_at_utc,
    block_number,
    tx_hash,
    varbinary_to_uint256(varbinary_substring(data, 1, 32)) AS old_multiplier_raw,
    varbinary_to_uint256(varbinary_substring(data, 33, 32)) AS new_multiplier_raw,
    varbinary_to_uint256(varbinary_substring(data, 65, 32)) AS effective_at_unix,
    data AS event_data
FROM bnb.logs
WHERE block_date >= DATE '2026-09-15'
  AND block_date < DATE '2026-10-02'
  AND contract_address IN (
      0x205812cdbed920aff76c6580abd681a46d11efc7,
      0x7425889fe94f9d693e8daefe88bcced6acfef4c0,
      0x76682c454467b3a1150ad8b6a92fc5ee2c21d7ed,
      0x2e065f65f1699964f4092de1d39a8efe6c8d6f32,
      0x25e572b466d152604d9e6c3e53b432b978825342,
      0xe28cd11c99af2df76bb8ada4cd0ef3904378280f,
      0x0bb3fa77e0809f42948e435f04883c25415e8263,
      0x462b5f13b7c7748279358962925c5de83bb9e598
  )
  AND topic0 = 0x2205df4534432b2f60654a3fdb48737ffdaf3e9edb1a498bd985bc026b15b055
ORDER BY block_time, tx_hash;
