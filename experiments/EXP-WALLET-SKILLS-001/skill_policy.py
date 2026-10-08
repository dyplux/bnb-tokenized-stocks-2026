"""Observable skill evidence to the existing deterministic policy, with no signer."""
import hashlib
import importlib.util
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from skill_capture import CONTRACT

KERNEL_SHA = '58037f676a8dfe7511cd256fcab34533bf1dfa0a70af33e6af86ec7354336556'
INTENT = {'chain_id': '56', 'ticker': 'NVDA', 'provider': 'ondo', 'contract': CONTRACT, 'notional_usd': '10'}
MANDATE = {'max_token_price_age_ms': 60000, 'require_independent_reference': True, 'max_reference_age_seconds': 60, 'max_notional_usd': 20, 'max_price_impact_percent': 2, 'max_eligibility_age_seconds': 60, 'require_onchain_multiplier': False}

def positive(value):
    try:
        n = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError('NUMERIC_FIELD_INVALID')
    if not n.is_finite() or n <= 0:
        raise ValueError('NUMERIC_FIELD_INVALID')
    return n

def normalize(catalog, dynamic, status, transports, observed):
    if not isinstance(catalog, list) or not isinstance(dynamic, dict) or not isinstance(status, dict):
        raise ValueError('DATA_SHAPE_INVALID')
    matches = [r for r in catalog if isinstance(r, dict) and str(r.get('chainId')) == '56' and r.get('ticker') == 'NVDA' and str(r.get('contractAddress', '')).lower() == CONTRACT and type(r.get('type')) is int and r['type'] == 1]
    if len(matches) != 1:
        raise ValueError('CATALOG_IDENTITY_NOT_UNIQUE')
    row = matches[0]
    if dynamic.get('ticker') != 'NVDA' or dynamic.get('symbol') != row.get('symbol') or row.get('symbol') != 'NVDAon' or type(dynamic.get('type')) is not int or dynamic['type'] != 1:
        raise ValueError('DYNAMIC_IDENTITY_MISMATCH')
    for key, expected in [('chainId', '56'), ('contractAddress', CONTRACT)]:
        if key in dynamic and str(dynamic[key]).lower() != expected:
            raise ValueError('DYNAMIC_IDENTITY_SHADOW_CONFLICT')
    token = dynamic.get('tokenInfo')
    if not isinstance(token, dict) or not isinstance(dynamic.get('statusInfo'), dict):
        raise ValueError('DYNAMIC_SHAPE_INVALID')
    ratio = positive(row.get('multiplier'))
    if ratio != positive(token.get('sharesMultiplier')):
        raise ValueError('RATIO_SOURCE_CONFLICT')
    price = positive(token.get('price'))
    for key in ['marketStatus', 'reasonCode', 'openState']:
        if status.get(key) != dynamic['statusInfo'].get(key):
            raise ValueError('MARKET_SOURCE_CONFLICT')
    source_hashes = {key: value['body_sha256'] for key, value in transports.items()}
    if set(source_hashes) != {'api1', 'api4', 'api5'} or any(not isinstance(v, str) or len(v) != 64 or any(c not in '0123456789abcdef' for c in v) for v in source_hashes.values()):
        raise ValueError('SOURCE_HASHES_INVALID')
    stock = dynamic.get('stockInfo')
    stock_price = stock.get('price') if isinstance(stock, dict) else None
    if stock_price is not None:
        stock_price = str(positive(stock_price))
    return {'chain_id': '56', 'ticker': 'NVDA', 'provider': 'ondo', 'contract': CONTRACT, 'issuer_verified': False, 'eligibility_status': 'UNKNOWN', 'token_to_share_ratio': str(ratio), 'market_status': status.get('marketStatus'), 'market_reason': status.get('reasonCode'), 'market_open_state': status.get('openState'), 'token_price_usd': str(price), 'token_price_age_ms': None, 'token_price_age_calculation': None, 'stock_feed_price_usd': stock_price, 'stock_feed_price_asof': None, 'reference_price_updated_at': None, 'reference_age_seconds': None, 'reference_age_status': 'UNKNOWN', 'quote_available': None, 'quote_identity_match': None, 'price_impact_percent': None, 'simulation_passed': None, 'source_observed_at': observed, 'source_response_sha256': source_hashes}

def evaluate(kernel_path, evidence, observed):
    kernel_path = Path(kernel_path)
    if hashlib.sha256(kernel_path.read_bytes()).hexdigest() != KERNEL_SHA:
        raise ValueError('FROZEN_KERNEL_HASH_MISMATCH')
    spec = importlib.util.spec_from_file_location('unchanged_praeva_policy', kernel_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(INTENT, evidence, MANDATE, now=datetime.fromisoformat(observed.replace('Z', '+00:00')))

def canonical_hash(receipt):
    clean = {k: v for k, v in receipt.items() if k != 'receipt_sha256'}
    return hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
