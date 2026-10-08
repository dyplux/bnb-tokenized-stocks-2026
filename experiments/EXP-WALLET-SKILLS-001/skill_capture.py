"""Bounded public GET transport. No wallet, API credential or transaction path."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

BASE = 'https://www.binance.com'
CONTRACT = '0xa9ee28c80f960b889dfbd1902055218cba016f75'
PATHS = {
    'api1': '/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai',
    'api5': '/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai',
    'api4': '/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/asset/market/status/ai',
}
PARAMS = {'api1': {'type': '1'}, 'api5': {'chainId': '56', 'contractAddress': CONTRACT}, 'api4': {'chainId': '56', 'contractAddress': CONTRACT}}
MAX_BODY = 2 * 1024 * 1024

def clock():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def save(path, value, binary=False):
    path = Path(path)
    with path.open('wb') as f:
        f.write(value if binary else (json.dumps(value, sort_keys=True, indent=2) + '\n').encode())
        f.flush()
        os.fsync(f.fileno())

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result

def decode(raw):
    obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs)
    if not isinstance(obj, dict) or obj.get('code') != '000000' or obj.get('success') is not True or 'data' not in obj:
        raise ValueError('PROVIDER_ENVELOPE_INVALID')
    return obj['data']

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, new_url):
        return None

class Capture:
    def __init__(self, folder, baseline_calls=3):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.marker = self.folder / 'request-count.json'
        if self.marker.exists():
            raise ValueError('CAPTURE_ALREADY_STARTED_NO_LIVE_RETRY')
        self.count = baseline_calls
        self.opener = urllib.request.build_opener(NoRedirect())

    def get(self, name):
        if name not in PATHS or self.count >= 6:
            raise ValueError('REQUEST_NOT_ALLOWLISTED_OR_LIMIT_EXCEEDED')
        self.count += 1
        save(self.marker, {'total_calls_including_prior_agent': self.count})
        url = BASE + PATHS[name] + '?' + urllib.parse.urlencode(PARAMS[name])
        request = urllib.request.Request(url, method='GET', headers={'User-Agent': 'binance-web3/1.1 (Skill)', 'Accept-Encoding': 'identity'})
        started = clock()
        try:
            try:
                response = self.opener.open(request, timeout=15)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                raw = response.read(MAX_BODY + 1)
                status, final_url = response.code, response.geturl()
                content_type = response.headers.get('Content-Type')
            meta = {'method': 'GET', 'request_url': url, 'final_url': final_url, 'status': status, 'started_at': started, 'received_at': clock(), 'redirect_followed': False, 'complete_body': len(raw) <= MAX_BODY, 'body_bytes': len(raw), 'body_sha256': hashlib.sha256(raw).hexdigest(), 'content_type': content_type}
            save(self.folder / (name + '.body.bin'), raw, True)
            save(self.folder / (name + '.transport.json'), meta)
            if status != 200 or final_url != url or not meta['complete_body'] or not isinstance(content_type, str) or 'application/json' not in content_type:
                raise ValueError('HTTP_CONTEXT_REJECTED')
            return decode(raw), meta
        except Exception as error:
            save(self.folder / (name + '.failure.json'), {'at': clock(), 'error_type': type(error).__name__, 'calls': self.count})
            raise
