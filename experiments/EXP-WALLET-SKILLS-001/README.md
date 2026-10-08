# Wallet Skills read-only evidence proof

This dated experiment uses Binance's official `binance-tokenized-securities-info` Wallet Skill with Praeva's existing deterministic kernel. It is a candidate demonstration for the Wallet Skills special prize. It doesn't demonstrate Agentic Wallet signing, a stock-token purchase or prize qualification.

## Observed chain

Official pinned skill -> API 1 exact Ondo NVDAon resolution -> API 5 dynamic data -> API 4 market state -> policy v0.6.0 -> NEED_HUMAN -> canonical receipt.

The skill requires no wallet/API key for these public reads. Captured data is historical after its observation time. The model has no verdict or signing authority, and the kernel and earlier receipts are unchanged.

## Verify without credentials or network

From the repository root:

```bash
python3 experiments/EXP-WALLET-SKILLS-001/verify_proof.py
python3 -m unittest discover -s experiments/EXP-WALLET-SKILLS-001 -p 'test_skill_proof.py' -v
```

The first command verifies every bundled hash and recreates the receipt at its recorded clock. The second runs offline focused regressions; synthetic mutations aren't live evidence. The evidence manifest must be compared with a trusted repository snapshot for an external integrity anchor.

This experiment never calls a signer, approves a token, submits an order or pays an API. It doesn't remove the unresolved main-track stock-execution gate. The earlier x402 proof and its incomplete full self-funding loop remain separate.

[Official skill](https://github.com/binance/binance-skills-hub/blob/9960c675387bd27f8866645b83693c1fa87242f6/skills/binance-web3/binance-tokenized-securities-info/SKILL.md) | [Invocation trace](AGENT-INVOCATION-TRACE.md) | [Receipt](receipt.json) | [Result](proof-result.json).
