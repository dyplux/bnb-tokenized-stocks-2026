#!/usr/bin/env python3
"""Offline verification of captured Wallet Skills evidence and fixed-clock policy replay."""
import hashlib
import json
from pathlib import Path
from skill_capture import decode
from skill_policy import canonical_hash, evaluate, normalize

ROOT = Path(__file__).resolve().parent
KERNEL = ROOT.parents[1] / 'app/rwa_policy.py'

def main():
    inputs = json.loads((ROOT / 'policy-input.json').read_text())
    receipt = json.loads((ROOT / 'receipt.json').read_text())
    manifest = json.loads((ROOT / 'evidence-manifest.json').read_text())
    for row in manifest['files']:
        if hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('EVIDENCE_BYTES_CHANGED')
    bodies, transports = {}, {}
    for key in ['api1', 'api5', 'api4']:
        raw = (ROOT / 'capture' / (key + '.body.bin')).read_bytes()
        meta = json.loads((ROOT / 'capture' / (key + '.transport.json')).read_text())
        if meta['status'] != 200 or meta['redirect_followed'] or meta['request_url'] != meta['final_url'] or hashlib.sha256(raw).hexdigest() != meta['body_sha256']:
            raise ValueError('CAPTURE_CONTEXT_OR_HASH_FAILED')
        bodies[key], transports[key] = decode(raw), meta
    evidence = normalize(bodies['api1'], bodies['api5'], bodies['api4'], transports, inputs['evaluation_clock'])
    if evidence != inputs['evidence'] or canonical_hash(receipt) != manifest['receipt_sha256']:
        raise ValueError('INPUT_OR_RECEIPT_CHANGED')
    if evaluate(KERNEL, evidence, inputs['evaluation_clock']) != receipt:
        raise ValueError('FIXED_CLOCK_REPLAY_FAILED')
    print(json.dumps({'integrity':'PASS', 'fixed_clock_replay':'PASS', 'decision':receipt['decision'], 'policy_version':receipt['policy_version'], 'receipt_sha256':receipt['receipt_sha256'], 'network_calls':0}))

if __name__ == '__main__': main()
