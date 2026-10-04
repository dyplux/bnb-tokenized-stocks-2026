const form = document.querySelector('#check-form');
const submit = document.querySelector('#submit');
const error = document.querySelector('#form-error');
let latest = null;

const labels = {
  ISSUER_UNVERIFIED: 'Issuer rights haven’t been independently verified for this review.',
  USER_ELIGIBILITY_UNKNOWN: 'A quote doesn’t establish whether this user may hold or trade the token.',
  INDEPENDENT_REFERENCE_TIME_UNKNOWN: 'The underlying stock reference has no independent as-of timestamp.',
  UNDERLYING_MARKET_NOT_REGULAR: 'The reported market state is outside a confirmed regular session.',
  MARKET_STATE_UNKNOWN: 'The market state is missing or isn’t a known regular-session value.',
  ONCHAIN_MULTIPLIER_UNVERIFIED: 'The bStock multiplier couldn’t be verified at a recent BSC block.',
  ONCHAIN_MULTIPLIER_MISMATCH: 'The on-chain multiplier differs from the catalog ratio.',
  ONCHAIN_MULTIPLIER_PENDING_CHANGE: 'A different next on-chain multiplier has been scheduled or exposed.',
  ONCHAIN_NEXT_MULTIPLIER_UNVERIFIED: 'The next on-chain multiplier couldn’t be checked.',
  ONCHAIN_MULTIPLIER_SCHEDULE_UNKNOWN: 'A multiplier change needs a dated issuer review.',
  MANDATE_LIMIT_EXCEEDED: 'This amount exceeds the maximum spend you entered.',
  PRICE_IMPACT_LIMIT_EXCEEDED: 'The quoted price impact exceeds your limit.',
  NO_EXECUTABLE_QUOTE: 'The API returned no route for this exact amount and representation.',
  QUOTE_UNVERIFIED: 'A route couldn’t be verified in this check.',
  PRICE_IMPACT_UNKNOWN: 'The quote didn’t establish price impact.',
  SIMULATION_UNVERIFIED: 'A funded user-wallet transaction hasn’t been simulated.',
  TOKEN_PRICE_STALE: 'The token price is older than the 60-second mandate.',
  TOKEN_PRICE_AGE_UNKNOWN: 'The token-price timestamp couldn’t be measured.',
  TOKEN_PRICE_AGE_PROVENANCE_UNKNOWN: 'The token-price clock lacks a verified calculation.',
  SHARE_RATIO_UNKNOWN: 'The token-to-share ratio is missing.',
  UNVERIFIED_RATIO_CHANGE: 'The economic share ratio changed without a verified corporate action.',
};

function item(list, code) {
  const li = document.createElement('li');
  const strong = document.createElement('strong');
  strong.textContent = code.replaceAll('_', ' ');
  const description = document.createElement('span');
  description.textContent = labels[code] || 'This check needs a closer review of the recorded evidence.';
  li.append(strong, description);
  list.append(li);
}

function fact(list, name, value, status = '') {
  const row = document.createElement('div');
  row.className = 'fact' + (status ? ' ' + status : '');
  const term = document.createElement('dt');
  term.textContent = name;
  const detail = document.createElement('dd');
  detail.textContent = value === null || value === undefined || value === '' ? 'Unknown' : String(value);
  row.append(term, detail);
  list.append(row);
}

function render(data) {
  latest = data;
  document.querySelector('#empty-state').hidden = true;
  document.querySelector('#result-state').hidden = false;
  const decision = document.querySelector('#decision');
  decision.textContent = data.decision.replace('_', ' ');
  decision.className = data.decision.toLowerCase();
  document.querySelector('#decision-context').textContent = data.decision === 'DENY'
    ? 'At least one check blocks this action under the entered mandate.'
    : data.decision === 'NEED_HUMAN'
      ? 'Some required facts can’t be established for this user and action yet.'
      : 'The supplied evidence passed this policy. Signing still needs a separate approval.';
  const reasons = document.querySelector('#reasons');
  reasons.replaceChildren();
  (data.reason_codes.length ? data.reason_codes : ['NO_POLICY_FLAGS']).forEach(code => item(reasons, code));
  const view = data.view;
  const facts = document.querySelector('#facts');
  facts.replaceChildren();
  fact(facts, 'Security', `${view.canonical_security} / ${view.representation} · ${view.provider}`);
  fact(facts, 'BSC contract', view.contract);
  fact(facts, 'Market state', view.market_status || 'UNKNOWN', view.market_status === 'regular' ? 'ok' : 'caution');
  fact(facts, 'Token price', view.token_price_usd === null ? 'UNKNOWN' : `$${view.token_price_usd}`);
  fact(facts, 'Token price clock', view.token_price_updated_at ? `${view.token_price_updated_at} · ${view.token_price_age_ms} ms old` : 'UNKNOWN');
  fact(facts, 'Reported reference', view.reported_reference_price_usd === null ? 'UNKNOWN' : `$${view.reported_reference_price_usd} · source time unknown`, 'caution');
  if (view.provider === 'ondo') fact(facts, 'Binance stock feed', view.stock_feed_price_usd === null ? 'UNKNOWN' : `$${view.stock_feed_price_usd} · as-of unknown`, 'caution');
  fact(facts, 'Stock reference clock', 'UNKNOWN · no independent timestamp', 'caution');
  fact(facts, 'Share ratio / multiplier', `${view.token_to_share_ratio} / ${view.multiplier_integrity}`,
       view.multiplier_integrity === 'MATCHED_FIXED_BLOCK' ? 'ok' : 'caution');
  fact(facts, 'Holder eligibility', view.eligibility, 'caution');
  fact(facts, 'Size-specific route', `${view.route}${view.execution_mode ? ` · ${view.execution_mode}` : ''}${view.quote_vendor ? ` · ${view.quote_vendor}` : ''}`,
       view.route === 'QUOTED' ? 'ok' : 'caution');
  fact(facts, 'Quoted price impact', view.price_impact_percent === null ? 'UNKNOWN' : `${view.price_impact_percent}%`);
  fact(facts, 'Quote captured at', data.sources.quote?.observed_at || 'UNKNOWN');
  if (data.sources.rpc) fact(facts, 'Multiplier BSC block', `${data.sources.rpc.block} · ${data.sources.rpc.block_timestamp}`);
  fact(facts, 'Simulation', view.simulation, 'caution');
  fact(facts, 'Your mandate', `${data.receipt.intent.notional_usd} USDT requested · ${data.mandate.max_notional_usd} USDT cap · ${data.mandate.max_price_impact_percent}% impact cap`);
  fact(facts, 'Observed at', data.receipt.timestamp);
  if (data.errors.length) fact(facts, 'Source errors', data.errors.map(e => e.source).join(', '), 'caution');
  const next = data.reason_codes.includes('MANDATE_LIMIT_EXCEEDED')
    ? 'Lower the requested amount or explicitly revise your maximum permitted spend, then run a new check.'
    : data.reason_codes.includes('NO_EXECUTABLE_QUOTE')
      ? 'Try a new live quote later. This check can’t claim a trade route at this amount.'
      : 'Verify issuer access and the underlying reference time for the intended user. A funded simulation and human approval would still be required before any transaction.';
  document.querySelector('#next-step').textContent = next;
  document.querySelector('#receipt-hash').textContent = `Receipt SHA-256 ${data.receipt.receipt_sha256.slice(0, 16)}…`;
  document.querySelector('#observed').textContent = data.origin;
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  error.hidden = true;
  if (!form.reportValidity()) return;
  submit.disabled = true;
  submit.textContent = 'Checking live sources…';
  const values = new FormData(form);
  const request = Object.fromEntries(values.entries());
  try {
    const response = await fetch('/api/safety-check', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(request),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'The live check failed.');
    render(payload);
  } catch (failure) {
    error.textContent = failure.message;
    error.hidden = false;
  } finally {
    submit.disabled = false;
    submit.innerHTML = 'Review action <span aria-hidden="true">↗</span>';
  }
});

document.querySelector('#download').addEventListener('click', () => {
  if (!latest) return;
  const blob = new Blob([JSON.stringify(latest, null, 2)], {type: 'application/json'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `dyplux-nvda-decision-${latest.receipt.timestamp.slice(0, 10)}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
});
