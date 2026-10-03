# Public source check for a populated Venus Core account

**Checked:** 2026-10-03 01:49 to 01:51 UTC. Read-only public requests only. No holder, wallet connection, key or transaction was used.

The [BNB Chain RPC documentation](https://docs.bnbchain.org/bnb-smart-chain/developers/json_rpc/json-rpc-endpoint/) says `eth_getLogs` is disabled on its listed public mainnet endpoints. A targeted check of alternative public providers produced these observations:

| Provider and bounded request | Observed result |
|---|---|
| [Blockmachine public BNB RPC](https://blockmachine.io/bnb-chain-rpc), `eth_chainId` | HTTP 403 |
| [PublicNode BNB RPC](https://bsc.publicnode.com/), Core vUSDT logs over 20 recent blocks | HTTP 403 |
| [Alchemy public BNB RPC](https://www.alchemy.com/rpc/bnb), `eth_chainId` | HTTP 200, chain `0x38` |
| Same Alchemy endpoint, Core vUSDT logs over 101 recent blocks | HTTP 429 |

The vUSDT contract came from the [public Venus markets API](https://api.venus.io/markets?chainId=56&limit=100) and was matched to the Core Comptroller before the log attempts. No logs or account addresses were obtained or retained. Provider errors don't indicate that Venus has no populated accounts; they only limit this keyless method in this environment.

The [current facet source trail](2026-10-03-venus-current-facet-boundary.md) identifies the intended Venus source, but a populated-account parity check remains unperformed. A consenting eligible holder's public address, or a separately authorized and working log/index source, is the next direct way to check account-specific behavior. This technical proof still wouldn't replace observation of the holder's actual cash task.
