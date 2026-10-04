# bStock eligibility endpoint: documented need, unlocated interface

**Checked:** 2026-10-04 UTC. **State:** unresolved documentation path, not a proved API defect. No country or wallet eligibility result was obtained.

## Reproduction

1. Open Binance's [bStocks deposit, withdrawal and conversion FAQ](https://www.binance.com/en/support/faq/detail/f0d41139fadc4790bf9a4c0c7bce2e88), item 9. It says third-party integrators are responsible for geographic restrictions and mentions a public REST country-eligibility endpoint. The FAQ gives no URL, HTTP method, request schema or response example for that endpoint.
2. Open the official [Binance Web3 API full documentation bundle](https://web3.binance.com/en/dev-docs/llms-full.txt), available as text on 4 October. Search its 7,678 lines for `country eligibility`, `eligibility endpoint` and `countryCode`. These exact searches returned no matching endpoint definition. This is a bounded search, not proof that no other Binance API documents it.
3. Open the separate [Web3 API service-restricted regions page](https://web3.binance.com/en/dev-docs/web3-api-prohibited-regions), last modified 1 October 2026. Its heading and first sentence say the list concerns access to the developer portal and API server through IP checks. It doesn't claim to decide whether a person may acquire a particular bStock. Portugal isn't listed there, but that fact doesn't determine bStock user or wallet eligibility.

## Consequence for this integration

Our signed quote and unsigned build work for the demo wallet, yet neither response proves the intended Portugal-based holder may acquire NVDAB. The API service-region list cannot substitute for the issuer's bStock country check. The policy must keep `eligibility_status=UNKNOWN`, and a mainnet purchase must not proceed from these facts alone.

## Documentation request

Please link the canonical country-eligibility endpoint, specify country-code input, response schema, update policy and whether a separate person, wallet, asset or venue check is required for a self-custodial BSC swap. Show how an integrator should fail closed when that endpoint is unavailable. This request is [mentor question 4](../mentor-questions.md); it has not been sent.
