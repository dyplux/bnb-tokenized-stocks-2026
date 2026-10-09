"use client";

import { useEffect, useRef, useState } from "react";
import { digestReceipt, type ReceiptData } from "@/lib/receipt";

const files = [
  "observed-unsafe.json",
  "observed-mandate-deny.json",
  "synthetic-safe.json",
];
const labels = [
  "Observed NEED_HUMAN",
  "Observed DENY",
  "SYNTHETIC POLICY FIXTURE",
];
const field = (value: unknown) =>
  value === null || value === undefined || value === ""
    ? "UNKNOWN"
    : String(value);

export default function EvidenceSelector({ cases }: { cases: ReceiptData[] }) {
  const [selected, setSelected] = useState(0);
  const [status, setStatus] = useState("Not verified");
  const [error, setError] = useState(false);
  const requestId = useRef(0);
  const item = cases[selected];
  const evidence = item.receipt.evidence;

  async function verifySelected(index: number) {
    const currentRequest = ++requestId.current;
    setStatus("Fetching and verifying receipt…");
    setError(false);
    try {
      const response = await fetch(`/evidence/${files[index]}`, {
        cache: "no-store",
      });
      if (!response.ok) throw new Error(`Fetch failed (${response.status}).`);
      const fetched = (await response.json()) as ReceiptData;
      if (
        fetched.receipt?.receipt_sha256 !== cases[index].receipt.receipt_sha256
      )
        throw new Error(
          "Trusted receipt hash doesn't match the fetched receipt.",
        );
      const actual = await digestReceipt(fetched);
      if (actual !== cases[index].receipt.receipt_sha256)
        throw new Error(
          "Canonical receipt digest doesn't match the trusted hash.",
        );
      if (currentRequest === requestId.current)
        setStatus(
          "Verified: fetched receipt hash and canonical SHA-256 match.",
        );
    } catch (cause) {
      if (currentRequest === requestId.current) {
        setError(true);
        setStatus(
          cause instanceof Error
            ? `Verification failed: ${cause.message}`
            : "Verification failed: invalid JSON or unavailable crypto.",
        );
      }
    }
  }

  useEffect(() => {
    requestId.current += 1;
    setStatus("Not verified");
    setError(false);
  }, [selected]);
  const tokenTimestamp =
    item.view?.token_price_updated_at ?? evidence.token_price_updated_at;
  const simulation =
    item.disclosure && evidence.simulation_passed === true
      ? "PASS (SYNTHETIC)"
      : field(item.view?.simulation ?? evidence.simulation_passed);
  const rows = [
    [
      "Asset / provider",
      `${field(evidence.ticker)} / ${field(evidence.provider)}`,
    ],
    [
      "Requested notional / spend cap",
      `${field(item.receipt.intent.notional_usd)} USDT / ${field(item.receipt.mandate?.max_notional_usd)} USDT`,
    ],
    ["Market status", field(evidence.market_status)],
    [
      "Independent reference clock",
      `${field(evidence.reference_age_status)} / ${field(evidence.reference_price_updated_at)}`,
    ],
    ["TOKEN price timestamp", field(tokenTimestamp)],
    ["Eligibility", field(evidence.eligibility_status)],
    ["Multiplier / ratio", field(evidence.token_to_share_ratio)],
    [
      "Quote / impact",
      `${field(evidence.quote_observed_at)} / ${field(evidence.price_impact_percent)}%`,
    ],
    ["Simulation", simulation],
    [
      "Policy / time",
      `${field(item.receipt.policy_version)} / ${field(item.receipt.timestamp)}`,
    ],
  ];
  return (
    <div className="evidence-panel">
      <div className="case-tabs" role="group" aria-label="Evidence cases">
        {labels.map((label, index) => (
          <button
            key={label}
            type="button"
            aria-pressed={selected === index}
            onClick={() => setSelected(index)}
          >
            {label}
          </button>
        ))}
      </div>
      <div
        className={`case-status ${error ? "status-error" : ""}`}
        aria-live="polite"
      >
        {status}
      </div>
      <div className="case-heading">
        <div>
          <p className="section-label">{item.origin}</p>
          <h3>{item.receipt.decision}</h3>
        </div>
        <span>{item.receipt.timestamp}</span>
      </div>
      <dl className="field-grid">
        {rows.map(([name, value]) => (
          <div key={name}>
            <dt>{name}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
      {item.disclosure && (
        <p className="synthetic-note">SYNTHETIC: {item.disclosure}</p>
      )}
      <details>
        <summary>
          Ordered reason codes ({item.receipt.reason_codes.length})
        </summary>
        <ol>
          {item.receipt.reason_codes.map((code) => (
            <li key={code}>
              <code>{code}</code>
            </li>
          ))}
        </ol>
      </details>
      <div className="receipt-sha">
        <span>Trusted receipt SHA-256</span>
        <code>{item.receipt.receipt_sha256}</code>
      </div>
      <div className="case-actions">
        <button
          className="button button-primary"
          type="button"
          onClick={() => verifySelected(selected)}
        >
          Verify receipt
        </button>
        <a
          className="button button-secondary"
          download={files[selected]}
          href={`/evidence/${files[selected]}`}
        >
          Download original JSON ↧
        </a>
        <a
          className="button button-secondary"
          href="https://dyplux.github.io/bnb-tokenized-stocks-2026/"
          target="_blank"
          rel="noreferrer"
        >
          Live evidence ↗
        </a>
      </div>
    </div>
  );
}
