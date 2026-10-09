# Final proof packet, 9 October 2026

This is the dated root proof index for the 9 October documentation checkpoint. It supplements, and doesn't rewrite, the frozen 5 October records or the 8 October claim map.

## Mainnet SPYon action

The [sanitized live packet](../judge/live/spyon-purchase-2026-10-09.json) records one operator-authorized 10 USDT SPYon purchase on BNB Smart Chain mainnet. Its direct route is marked `VERIFIED`. The private wrapper returned `ALLOW`; the real-state RPC simulation passed without override and the Binance Transaction API returned success.

The packet records two signatures, two dispatches, zero economic retries, and aggregate gas of 13,499,550,000,000 wei, equal to 0.00001349955 BNB. Its approval transaction is [`0x29d8cd792b6b511efd350635e3a2cc875d7c2478c2152d6d340aabc449b89965`](https://bscscan.com/tx/0x29d8cd792b6b511efd350635e3a2cc875d7c2478c2152d6d340aabc449b89965) and its swap transaction is [`0xd7c7587446ee0da063fb47c3deff6094abe76cefb5b1d63dd7e58a17dee7c34b`](https://bscscan.com/tx/0xd7c7587446ee0da063fb47c3deff6094abe76cefb5b1d63dd7e58a17dee7c34b).

The wallet received **0.012666722432517425 SPYon**. Both core0.6.0 and the private wrapper returned ALLOW before signing. The final allowance is zero.

This is one bounded operator-authorized purchase. It doesn't establish general autonomous trading, universal signer enforcement, or a production-feed guarantee.

## Studio explanation recovery

The [recovered explanation packet](../judge/studio/recovered-explanation-2026-10-09.json) records one operator-assisted, key-funded paid explanation request in a new process. It returned HTTP 200, one model attempt, a paid usage delta, and the recovered explanation. The first and second requests in the same new process preserved receipt `63c918049dc88ab90faef38f9b749be3993884989ec38bb253f5c2b887ae54db`. One model call consumed97 input and37 completion tokens, billed **USD0.000021**. The second request blocked another inference; cleanup passed.

The packet doesn't prove continuity of the original OOM-killed process, a fully autonomous loop, or an autonomous paid explanation. Its authority is `NONE`; it did not alter the stock decision or receipt.

## Preserved historical boundaries

The console still contains the same three labelled static cases: NVDAB `NEED_HUMAN`, historical SPYon `DENY`, and synthetic `ALLOW`. The original Nasdaq-based SPYon `DENY` remains historical. The 120-second video predates the live purchase and doesn't show it. The 63-second video remains the 6 October historical film.

The [9 October claims](claims-2026-10-09.md) provide the PROVEN, PARTIAL, SYNTHETIC, HISTORICAL and NOT CLAIMED matrix. The public baseline `8ac6edd` and tag `v1` are preserved.
