const cases = {
  observed: {url: 'judge/observed-unsafe.json', title: 'NEED_HUMAN',
    summary: 'This dated NVDAB quote returned a route. The policy stopped because market state, issuer access, an independent stock-reference clock and funded simulation weren\'t established.'},
  mandate: {url: 'judge/observed-mandate-deny.json', title: 'DENY',
    summary: 'This dated NVDAB check returned a route, but the proposed 100 USDT purchase exceeded the 20 USDT mandate. Missing evidence remained visible in the receipt.'},
  synthetic: {url: 'judge/synthetic-safe.json', title: 'ALLOW · fixture only',
    summary: 'All inputs were supplied by a synthetic test fixture. It shows the passing policy branch and proves no real access, quote, simulation or trade.'}
};
let activeRequest = 0;

function stable(value) {
  if (Array.isArray(value)) return '[' + value.map(stable).join(',') + ']';
  if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + stable(value[k])).join(',') + '}';
  return JSON.stringify(value);
}

async function hashReceipt(receipt) {
  const body = {...receipt};
  delete body.receipt_sha256;
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stable(body)));
  return [...new Uint8Array(digest)].map(n => n.toString(16).padStart(2, '0')).join('');
}

function row(list, label, value) {
  const line = document.createElement('div');
  const term = document.createElement('dt');
  const detail = document.createElement('dd');
  term.textContent = label;
  detail.textContent = value == null || value === '' ? 'UNKNOWN' : String(value);
  line.append(term, detail);
  list.append(line);
}

async function showCase(key) {
  const selected = cases[key];
  const requestId = ++activeRequest;
  for (const button of document.querySelectorAll('[data-case]')) {
    const active = button.dataset.case === key;
    button.classList.toggle('selected', active);
    button.setAttribute('aria-pressed', String(active));
  }
  document.querySelector('#decision-title').textContent = 'Loading...';
  document.querySelector('#hash-state').textContent = 'Checking receipt...';
  document.querySelector('#receipt-link').removeAttribute('href');
  try {
    const response = await fetch(selected.url, {cache: 'no-store'});
    if (!response.ok) throw new Error('Receipt unavailable');
    const data = await response.json();
    if (requestId !== activeRequest) return;
    const receipt = data.receipt;
    const evidence = receipt.evidence;
    document.querySelector('#case-origin').textContent = data.origin;
    document.querySelector('#case-time').textContent = receipt.timestamp;
    document.querySelector('#decision-title').textContent = selected.title;
    document.querySelector('#case-summary').textContent = selected.summary;
    const list = document.querySelector('#evidence');
    list.replaceChildren();
    row(list, 'Security and representation', `${receipt.intent.ticker} / ${receipt.intent.provider}`);
    row(list, 'BNB Chain contract', receipt.intent.contract);
    row(list, 'Requested amount', `${receipt.intent.notional_usd} USDT`);
    row(list, 'Market state', key === 'synthetic' ? 'regular (test input)' : evidence.market_status);
    row(list, 'Independent stock-reference age', key === 'synthetic'
      ? `${evidence.reference_age_status} (test input)` : evidence.reference_age_status);
    row(list, 'Issuer and user access', key === 'synthetic'
      ? 'ELIGIBLE IN TEST INPUT ONLY; no real access verified'
      : `${evidence.issuer_verified === true ? 'verified' : 'unknown'} / ${evidence.eligibility_status || 'UNKNOWN'}`);
    row(list, 'Multiplier or share ratio', evidence.token_to_share_ratio);
    row(list, 'On-chain multiplier check', evidence.onchain_multiplier_block == null
      ? 'Fixture only; no chain read' :
      (evidence.onchain_ui_multiplier === evidence.token_to_share_ratio
        ? `Matched at block ${evidence.onchain_multiplier_block}`
        : `Mismatch at block ${evidence.onchain_multiplier_block}`));
    row(list, 'Exact route match', evidence.quote_identity_match);
    row(list, 'Route mode and vendor', evidence.quote_available === true
      ? `${evidence.quote_execution_mode || 'UNKNOWN'} / ${evidence.quote_vendor || 'UNKNOWN'}`
      : 'NO ROUTE');
    row(list, 'Price impact', evidence.price_impact_percent == null ? null : `${evidence.price_impact_percent}%`);
    row(list, 'Slippage tolerance', 'NOT INCLUDED IN THIS POLICY RECEIPT');
    row(list, 'Funded simulation passed', key === 'synthetic'
      ? 'true (test input only; no funded transaction)' : evidence.simulation_passed);
    row(list, 'Mandate cap', `${receipt.mandate.max_notional_usd} USDT`);
    const reasons = document.querySelector('#reasons');
    reasons.replaceChildren();
    for (const code of receipt.reason_codes.length ? receipt.reason_codes : ['NO_POLICY_FLAGS_IN_FIXTURE']) {
      const li = document.createElement('li');
      li.textContent = code;
      reasons.append(li);
    }
    document.querySelector('#receipt-hash').textContent = receipt.receipt_sha256;
    document.querySelector('#receipt-link').href = selected.url;
    const valid = await hashReceipt(receipt) === receipt.receipt_sha256;
    if (requestId !== activeRequest) return;
    document.querySelector('#hash-state').textContent = valid ? 'Hash matches the downloaded decision body' : 'Hash mismatch. Do not rely on this packet.';
  } catch (error) {
    if (requestId !== activeRequest) return;
    document.querySelector('#decision-title').textContent = 'Receipt unavailable';
    document.querySelector('#case-summary').textContent = 'The published file could not be loaded. Try the repository link.';
    document.querySelector('#hash-state').textContent = 'No verification completed';
  }
}

for (const button of document.querySelectorAll('[data-case]')) {
  button.addEventListener('click', () => showCase(button.dataset.case));
}
showCase('observed');
