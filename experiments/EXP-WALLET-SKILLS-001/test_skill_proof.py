import copy
import json
from pathlib import Path
import tempfile
import unittest
from skill_capture import Capture, CONTRACT, NoRedirect, decode
from skill_policy import canonical_hash, evaluate, normalize

ROOT = Path(__file__).resolve().parent
KERNEL = ROOT.parents[1] / 'app/rwa_policy.py'
INPUT = json.loads((ROOT / 'policy-input.json').read_text())
BODIES = {key: json.loads((ROOT / 'capture' / (key + '.body.bin')).read_bytes())['data'] for key in ['api1', 'api5', 'api4']}
META = {key: json.loads((ROOT / 'capture' / (key + '.transport.json')).read_text()) for key in ['api1', 'api5', 'api4']}
CLOCK = INPUT['evaluation_clock']

class ProofTests(unittest.TestCase):
    def data(self):
        return copy.deepcopy((BODIES['api1'], BODIES['api5'], BODIES['api4']))
    def mapped(self):
        return normalize(*self.data(), META, CLOCK)
    def test_live_data_maps_with_unknown_clocks(self):
        e = self.mapped()
        self.assertEqual(e['reference_age_status'], 'UNKNOWN')
        self.assertIsNone(e['token_price_age_ms'])
        self.assertEqual(e['source_response_sha256'], {k: v['body_sha256'] for k, v in META.items()})
        self.assertEqual(e['stock_feed_price_usd'], str(BODIES['api5']['stockInfo']['price']))
    def test_missing_evidence_fails_closed(self):
        r = evaluate(KERNEL, self.mapped(), CLOCK)
        self.assertEqual(r['decision'], 'NEED_HUMAN')
        for reason in ['INDEPENDENT_REFERENCE_TIME_UNKNOWN', 'USER_ELIGIBILITY_UNKNOWN', 'QUOTE_UNVERIFIED', 'SIMULATION_UNVERIFIED']:
            self.assertIn(reason, r['reason_codes'])
    def test_wrong_chain(self):
        a, b, c = self.data()
        for row in a:
            if row.get('contractAddress', '').lower() == CONTRACT and row.get('chainId') == '56': row['chainId'] = '1'
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_wrong_contract(self):
        a, b, c = self.data()
        for row in a:
            if row.get('contractAddress', '').lower() == CONTRACT: row['contractAddress'] = '0x' + '0' * 40
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_duplicate_identity(self):
        a, b, c = self.data()
        a.append(next(copy.deepcopy(r) for r in a if r.get('chainId') == '56' and r.get('contractAddress', '').lower() == CONTRACT))
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_symbol_mismatch(self):
        a, b, c = self.data(); b['symbol'] = 'NVDAB'
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_provider_mismatch(self):
        a, b, c = self.data(); b['type'] = 2
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_wrong_identity_shadow(self):
        a, b, c = self.data(); b['chainId'] = '1'
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_invalid_numbers(self):
        for value in ['NaN', 'Infinity', '0', '-1', 'invalid']:
            with self.subTest(value=value):
                a, b, c = self.data(); b['tokenInfo']['price'] = value
                with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_ratio_conflict(self):
        a, b, c = self.data(); b['tokenInfo']['sharesMultiplier'] = '2'
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_market_conflict(self):
        a, b, c = self.data(); c['marketStatus'] = 'regular'
        with self.assertRaises(ValueError): normalize(a, b, c, META, CLOCK)
    def test_malformed_body(self):
        with self.assertRaises(ValueError): decode(b'bad JSON')
    def test_error_envelope(self):
        with self.assertRaises(ValueError): decode(b'{"code":"40374","success":false,"data":null}')
    def test_duplicate_json(self):
        with self.assertRaises(ValueError): decode(b'{"code":"000000","code":"000000","success":true,"data":[]}')
    def test_receipt_hash_and_fixed_clock(self):
        r = evaluate(KERNEL, self.mapped(), CLOCK)
        self.assertEqual(canonical_hash(r), r['receipt_sha256'])
        self.assertEqual(r, evaluate(KERNEL, self.mapped(), CLOCK))
        changed = copy.deepcopy(r); changed['intent']['notional_usd'] = '11'
        self.assertNotEqual(canonical_hash(changed), r['receipt_sha256'])
    def test_policy_denies_tampered_chain(self):
        e = self.mapped(); e['chain_id'] = '1'
        r = evaluate(KERNEL, e, CLOCK)
        self.assertEqual(r['decision'], 'DENY'); self.assertIn('CHAIN_MISMATCH', r['reason_codes'])
    def test_no_redirect_following(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com'))
    def test_dispatch_cap_without_network(self):
        c = object.__new__(Capture); c.count = 6
        with self.assertRaises(ValueError): c.get('api1')
    def test_failed_http_persists_before_parse(self):
        class Response:
            code = 403
            headers = {'Content-Type': 'application/json'}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, limit): return b'{"code":"403","success":false}'
            def geturl(self): return 'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=1'
        class Transport:
            def open(self, *args, **kwargs): return Response()
        with tempfile.TemporaryDirectory() as folder:
            c = Capture(folder); c.opener = Transport()
            with self.assertRaises(ValueError): c.get('api1')
            self.assertTrue((Path(folder) / 'api1.body.bin').exists())
            self.assertEqual(json.loads((Path(folder) / 'api1.transport.json').read_text())['status'], 403)
            with self.assertRaises(ValueError): Capture(folder)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProofTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    Path('FOCUSED-TEST-RESULTS.json').write_text(json.dumps({'tests': result.testsRun, 'passed': result.testsRun - len(result.errors) - len(result.failures), 'failures': len(result.failures), 'errors': len(result.errors), 'live_http_calls': 0, 'scope': 'Offline mutations of captured data and mock transport; not new live evidence'}, indent=2) + '\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
