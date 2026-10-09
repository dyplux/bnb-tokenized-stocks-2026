"use client";

import { useRef, useState } from "react";
import managed from "@/public/console-evidence/managed-replay.json";
import spyon from "@/public/console-evidence/spyon-deny.json";
import synthetic from "@/public/evidence/synthetic-safe.json";
import { canonicalize } from "@/lib/receipt";
import styles from "./console.module.css";

type EvidenceRow = { label: string; value: string; state: "pass" | "hold" | "deny" | "fixture" };
type Case = {
  id: string;
  tab: string;
  origin: string;
  verdict: "NEED_HUMAN" | "DENY" | "ALLOW";
  asset: string;
  action: string;
  amount: string;
  chain: string;
  context: string;
  timestamp: string;
  policy: string;
  reasonCodes: string[];
  receiptHash: string;
  receipt: Record<string, unknown>;
  file: string;
  evidence: EvidenceRow[];
  explanation: string;
  sourceLinks: { label: string; href: string }[];
};

const managedReceipt = managed.receipt;
const spyonReceipt = spyon.receipt;
const syntheticReceipt = synthetic.receipt;
const cases: Case[] = [
  {
    id: "managed",
    tab: "Observed NEED_HUMAN",
    origin: "DATED MANAGED AGENT STUDIO REPLAY · 7 OCT 2026",
    verdict: "NEED_HUMAN",
    asset: "NVDAB",
    action: "Assess quoted route",
    amount: "100 USDT",
    chain: "BNB Chain",
    context: `Three remote A2A calls between ${managed.runtime_events[0].received_at} and ${managed.runtime_events[2].completed_at} returned this receipt. The fixed input evidence is dated 4 Oct. Managed trial expires ${managed.managed_expires_at}. This page uses the preserved response and redacted runtime events, with no live call.`,
    timestamp: managedReceipt.timestamp,
    policy: managedReceipt.policy_version,
    reasonCodes: managedReceipt.reason_codes,
    receiptHash: managedReceipt.receipt_sha256,
    receipt: managedReceipt,
    file: "/console-evidence/managed-replay.json",
    explanation: "A route was quoted, but the evidence required to authorize signing wasn't complete.",
    evidence: [
      { label: "Asset integrity", value: "Issuer unverified", state: "hold" },
      { label: "Market state", value: "Unknown", state: "hold" },
      { label: "Independent reference", value: "Timestamp unknown", state: "hold" },
      { label: "Multiplier", value: "Fixed-block value recorded", state: "pass" },
      { label: "Eligibility", value: "Unknown", state: "hold" },
      { label: "Route", value: "Quote identity matched", state: "pass" },
      { label: "Simulation", value: "Unverified", state: "hold" },
    ],
    sourceLinks: [
      { label: "Managed agent card (trial)", href: managed.managed_card_url },
      { label: "Deterministic policy source", href: "https://github.com/dyplux/bnb-tokenized-stocks-2026/blob/0b2d59e78cdd8ee9b58c9c569b57ce07399ddbd5/app/rwa_policy.py" },
    ],
  },
  {
    id: "spyon",
    tab: "Observed DENY",
    origin: "DATED MAINNET READ-ONLY CAPTURE · 7 OCT 2026",
    verdict: "DENY",
    asset: "SPYon",
    action: "BUY proposal",
    amount: "10 USDT",
    chain: "BNB Chain",
    context: `At BNB Chain block ${spyon.block}, the independent Nasdaq SPY reference was ${spyon.independent_reference.age_seconds_at_decision.toFixed(3)} seconds old. Policy maximum: 60 seconds. This dated decision used a private read-only direct-route adapter around the unchanged core. Person scope was self-attested, not legal or issuer clearance. No swap was signed.`,
    timestamp: spyonReceipt.timestamp,
    policy: spyonReceipt.policy_version,
    reasonCodes: spyonReceipt.reason_codes,
    receiptHash: spyonReceipt.receipt_sha256,
    receipt: spyonReceipt,
    file: "/console-evidence/spyon-deny.json",
    explanation: "The independent stock reference exceeded the unchanged 60-second guard. The direct swap simulation also lacked approval.",
    evidence: [
      { label: "Asset integrity", value: "Product documents and onchain checks reviewed", state: "pass" },
      { label: "Market state", value: "Core at capture", state: "pass" },
      { label: "Independent reference", value: `${spyon.independent_reference.age_seconds_at_decision.toFixed(3)} s old · limit 60 s`, state: "deny" },
      { label: "Multiplier", value: "No standalone verdict in this packet", state: "hold" },
      { label: "Eligibility", value: "Documentary secondary path supported; no issuer approval", state: "hold" },
      { label: "Route", value: "Direct PancakeSwap provenance verified", state: "pass" },
      { label: "Simulation", value: "Failed: missing allowance", state: "hold" },
    ],
    sourceLinks: [
      { label: "Independent Nasdaq SPY source", href: spyon.independent_reference.source_url },
      { label: "PancakeSwap deployment manifest", href: spyon.route.official_manifest.url },
    ],
  },
  {
    id: "synthetic",
    tab: "Synthetic ALLOW",
    origin: "SYNTHETIC POLICY FIXTURE · NO REAL TRADE",
    verdict: "ALLOW",
    asset: "TEST",
    action: "Policy test",
    amount: "10 USDT (synthetic)",
    chain: "BNB Chain fixture",
    context: "Every input is synthetic. This fixture demonstrates the policy's ALLOW branch. It proves no holder eligibility, funded simulation, authorized signature or trade.",
    timestamp: syntheticReceipt.timestamp,
    policy: syntheticReceipt.policy_version,
    reasonCodes: syntheticReceipt.reason_codes,
    receiptHash: syntheticReceipt.receipt_sha256,
    receipt: syntheticReceipt,
    file: "/evidence/synthetic-safe.json",
    explanation: "The policy returns ALLOW for this fully synthetic input only.",
    evidence: [
      { label: "Asset integrity", value: "Synthetic fixture", state: "fixture" },
      { label: "Market state", value: "Synthetic regular", state: "fixture" },
      { label: "Independent reference", value: "Synthetic 10-second age", state: "fixture" },
      { label: "Multiplier", value: "Synthetic ratio 1", state: "fixture" },
      { label: "Eligibility", value: "Synthetic ELIGIBLE", state: "fixture" },
      { label: "Route", value: "Synthetic quote", state: "fixture" },
      { label: "Simulation", value: "Synthetic pass", state: "fixture" },
    ],
    sourceLinks: [
      { label: "Original public fixture", href: "https://github.com/dyplux/bnb-tokenized-stocks-2026/blob/e6ac2d4616a9d066d2d00d588a508e8762c75f4c/docs/judge/synthetic-safe.json" },
    ],
  },
];

const reasonLabels: Record<string, string> = {
  INDEPENDENT_REFERENCE_TIME_UNKNOWN: "Stock reference time is unknown",
  ISSUER_UNVERIFIED: "Issuer evidence isn't verified",
  MARKET_STATE_UNKNOWN: "Market state is unknown",
  SIMULATION_UNVERIFIED: "Swap simulation isn't verified",
  USER_ELIGIBILITY_UNKNOWN: "Buyer eligibility is unknown",
  INDEPENDENT_REFERENCE_STALE: "Stock reference exceeds 60 seconds",
  DIRECT_SIMULATION_UNVERIFIED: "Direct swap lacks a passing simulation",
};

async function hashReceipt(receipt: Record<string, unknown>): Promise<string> {
  const bytes = new TextEncoder().encode(JSON.stringify(canonicalize(receipt, true)));
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export default function Console() {
  const [active, setActive] = useState(0);
  const [feedback, setFeedback] = useState("");
  const verificationId = useRef(0);
  const item = cases[active];

  async function verifyReceipt() {
    const currentId = ++verificationId.current;
    setFeedback("Fetching receipt and checking canonical SHA-256.");
    try {
      const response = await fetch(item.file, { cache: "no-store" });
      if (!response.ok) throw new Error(`Evidence fetch returned ${response.status}`);
      const fetched = (await response.json()) as { receipt?: Record<string, unknown> };
      if (!fetched.receipt || fetched.receipt.receipt_sha256 !== item.receiptHash)
        throw new Error("The fetched receipt differs from the displayed hash");
      const actual = await hashReceipt(fetched.receipt);
      if (actual !== item.receiptHash) throw new Error("The canonical receipt hash differs");
      if (currentId === verificationId.current)
        setFeedback("Receipt SHA-256 verified. This confirms bytes, not upstream truth or execution.");
    } catch (error) {
      if (currentId === verificationId.current)
        setFeedback(`Verification failed: ${error instanceof Error ? error.message : "unknown error"}.`);
    }
  }

  async function copyReceipt() {
    try {
      await navigator.clipboard.writeText(JSON.stringify(item.receipt, null, 2));
      setFeedback("Receipt JSON copied.");
    } catch {
      setFeedback("Copy failed. Use Download evidence JSON.");
    }
  }

  return (
    <>
      <a className="skip-link" href="#console-main">Skip to assessment</a>
      <header className="site-header">
        <div className="header-inner">
          <a className="wordmark" href="/" aria-label="Praeva by Dyplux home">
            <img src="/praeva-logo.svg" width="760" height="200" alt="" />
          </a>
          <nav className="header-nav" aria-label="Primary navigation">
            <a href="/">Home</a>
            <a href="https://dyplux.github.io/bnb-tokenized-stocks-2026/" target="_blank" rel="noreferrer">Judge evidence</a>
          </nav>
        </div>
      </header>
      <main className={styles.main} id="console-main">
        <div className={styles.heading}>
          <div>
            <p className={styles.kicker}>PRE-SIGN ASSESSMENT CONSOLE / BNB CHAIN</p>
            <h1>Assessment console</h1>
            <p>Proposal → evidence → verdict → receipt.</p>
          </div>
          <span className={styles.readOnly}>READ-ONLY · DATED CASES</span>
        </div>
        <p className={styles.notice}>Read-only recorded assessments. Inspect evidence without a wallet or signature.</p>
        <div className={styles.presets} role="group" aria-label="Assessment presets">
          {cases.map((entry, index) => (
            <button
              className={active === index ? styles.presetActive : styles.preset}
              key={entry.id}
              type="button"
              aria-pressed={active === index}
              onClick={() => { verificationId.current += 1; setActive(index); setFeedback(""); }}
            >
              <span>{entry.tab}</span>
              <small>{entry.id === "managed" ? "Dated managed replay" : entry.id === "spyon" ? "Real mainnet capture" : "Synthetic policy test"} · {entry.asset}</small>
            </button>
          ))}
        </div>
        <p className={styles.origin}>{item.origin}</p>
        <div className={styles.caseSummary} aria-live="polite" aria-atomic="true">
          <div><span>Proposed action</span><strong>{item.amount} → {item.asset}</strong></div>
          <div><span>Verdict</span><strong className={item.verdict === "DENY" ? styles.summaryDeny : item.verdict === "ALLOW" ? styles.summaryAllow : styles.summaryHold}>{item.verdict}</strong><span>{item.id === "synthetic" ? "Synthetic test inputs" : `${item.reasonCodes.length} reason codes`}</span></div>
          <a href="#receipt-title">Receipt {item.receiptHash.slice(0, 12)} · inspect</a>
        </div>
        <div className={styles.topGrid}>
          <section className={styles.panel} aria-labelledby="proposal-title">
            <div className={styles.panelHead}><span>01</span><h2 id="proposal-title">Proposed action</h2></div>
            <dl className={styles.actionRows}>
              <div><dt>Asset</dt><dd>{item.asset}</dd></div>
              <div><dt>Action</dt><dd>{item.action}</dd></div>
              <div><dt>Amount</dt><dd>{item.amount}</dd></div>
              <div><dt>Network</dt><dd>{item.chain}</dd></div>
            </dl>
            <details className={styles.captureContext}><summary>Capture context and limits</summary><p className={styles.context}>{item.context}</p></details>
          </section>
          <section className={`${styles.panel} ${styles.decisionPanel}`} aria-labelledby="decision-title">
            <div className={styles.panelHead}><span>02</span><h2 id="decision-title">Decision</h2></div>
            <strong className={item.verdict === "DENY" ? styles.deny : item.verdict === "ALLOW" ? styles.allow : styles.needHuman}>{item.verdict}</strong>
            <p className={styles.decisionText}>{item.explanation}</p>
            <div className={styles.reasonHeading}>REASONS <span>{item.reasonCodes.length}</span></div>
            {item.reasonCodes.length ? <ol className={styles.reasons}>{item.reasonCodes.map(code => <li key={code}>{reasonLabels[code] || code}</li>)}</ol> : <p className={styles.noReasons}>No reason codes in this synthetic fixture.</p>}
            {item.reasonCodes.length > 0 && <details className={styles.captureContext}><summary>Ordered reason codes</summary><ol className={styles.reasons}>{item.reasonCodes.map(code => <li key={code}><code>{code}</code></li>)}</ol></details>}
          </section>
        </div>
        <section className={`${styles.panel} ${styles.evidencePanel}`} aria-labelledby="evidence-title">
          <div className={styles.panelHead}><span>03</span><h2 id="evidence-title">Evidence</h2></div>
          <div className={styles.evidenceGrid}>
            {item.evidence.map(row => (
              <div className={styles.evidenceRow} key={row.label}>
                <span className={styles.evidenceLabel}>{row.label}</span>
                <strong className={styles[row.state]}>{row.value}</strong>
              </div>
            ))}
          </div>
        </section>
        <section className={`${styles.panel} ${styles.receiptPanel}`} aria-labelledby="receipt-title">
          <div className={styles.panelHead}><span>04</span><h2 id="receipt-title">Verifiable receipt</h2></div>
          <dl className={styles.receiptMeta}>
            <div><dt>Policy</dt><dd>{item.policy}</dd></div>
            <div><dt>Decision time</dt><dd>{item.timestamp}</dd></div>
            <div className={styles.hash}><dt>Receipt SHA-256</dt><dd><code>{item.receiptHash}</code></dd></div>
          </dl>
          <div className={styles.actions}>
            <button type="button" onClick={verifyReceipt}>Verify receipt</button>
            <button type="button" onClick={copyReceipt}>Copy receipt</button>
            <a href={item.file} download>Download selected case JSON</a>
          </div>
          <p className={styles.feedback} role="status" aria-live="polite">{feedback || "A matching hash verifies receipt bytes. It doesn't prove upstream truth, eligibility or execution."}</p>
          <div className={styles.sources}>Source links: {item.sourceLinks.map((link) => <a key={link.href} href={link.href.includes("bnbagent-api.bnbchain.world") ? "/console-evidence/managed-replay.json" : link.href} target="_blank" rel="noreferrer">{link.href.includes("bnbagent-api.bnbchain.world") ? "Recorded managed proof" : link.label} ↗</a>)}</div>
        </section>
        <section className={`${styles.panel} ${styles.runtimePanel}`} aria-labelledby="runtime-title">
          <div className={styles.panelHead}><span>05</span><h2 id="runtime-title">Agent runtime evidence</h2></div>
          <div className={styles.runtimeGrid}>
            <div><span>BNB Agent Studio</span><strong>Managed replay · 7 Oct 2026</strong><a href="/console-evidence/managed-replay.json">Inspect remote receipt</a></div>
            <div><span>ERC-8004 identity</span><strong>Agent ID 2574 · testnet</strong><a href="https://agent.praeva.dyplux.com/.well-known/agent-card.json" target="_blank" rel="noreferrer">Stable Agent Card ↗</a></div>
            <div><span>x402 settlement</span><strong>1 U confirmed · 8 Oct 2026</strong><a href="https://bscscan.com/tx/0xb0344256c2807a7ce5d888738048bf74d326bd816b007f6df0a06004506b415b" target="_blank" rel="noreferrer">Inspect settlement ↗</a></div>
            <div><span>Wallet Skills</span><strong>Ondo read-only · 9 Oct 2026</strong><a href="https://github.com/dyplux/bnb-tokenized-stocks-2026/blob/850c053354a47e9f4ba10edcfd73a5796addd311/docs/submission/wallet-skills-evidence-2026-10-09.md" target="_blank" rel="noreferrer">Inspect skill proof ↗</a></div>
          </div>
          <p className={styles.context}>The original 8 October payment run didn't demonstrate paid explanation or uninterrupted post-settlement continuity. Wallet Skills adds read-only evidence, not Agentic Wallet execution.</p>
        </section>
        <p className={styles.boundary}>Praeva returns a decision before a separate signer acts. These cases include no authorized trade. The SPYon route and replay evidence are historical snapshots.</p>
      </main>
      <footer className="site-footer"><span>Praeva by Dyplux</span><nav aria-label="Footer"><a href="/">Product</a><a href="https://github.com/dyplux/bnb-tokenized-stocks-2026" target="_blank" rel="noreferrer">Source</a></nav></footer>
    </>
  );
}
