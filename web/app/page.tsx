import observedUnsafe from "@/public/evidence/observed-unsafe.json";
import observedDeny from "@/public/evidence/observed-mandate-deny.json";
import syntheticSafe from "@/public/evidence/synthetic-safe.json";
import type { ReceiptData } from "@/lib/receipt";
import EvidenceSelector from "./evidence-selector";

const pinnedRoot =
  "https://github.com/dyplux/bnb-tokenized-stocks-2026/tree/e6ac2d4616a9d066d2d00d588a508e8762c75f4c";
const pinnedFile =
  "https://github.com/dyplux/bnb-tokenized-stocks-2026/blob/e6ac2d4616a9d066d2d00d588a508e8762c75f4c/";
const unsafe = observedUnsafe as ReceiptData;
const evidence = unsafe.receipt.evidence;
const tokenPriceUpdatedAt =
  unsafe.view?.token_price_updated_at ?? evidence.token_price_updated_at;
const date = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "short",
  year: "numeric",
  timeZone: "UTC",
}).format(new Date(unsafe.receipt.timestamp ?? ""));
const Arrow = () => (
  <span className="button-arrow" aria-hidden="true">
    ↗
  </span>
);

function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-title">
      <div className="hero-copy">
        <p className="eyebrow">
          <span className="hero-brand">
            <img src="/praeva-mark.svg" width="200" height="200" alt="" />
            <span>Praeva</span>
          </span>{" "}
          / dated read-only review
        </p>
        <h1 id="hero-title">
          A route exists
          <br />
          Signing takes
          <br />
          <em>evidence</em>
        </h1>
        <p className="hero-lede">
          Deterministic RWA evidence-sufficiency and authorization review
          immediately before a separate privileged signer. Inspect one proposed
          action, its evidence, mandate and decision receipt.
        </p>
        <div className="hero-actions">
          <a className="button button-primary" href="/console/">
            Open assessment console <Arrow />
          </a>
          <a className="button button-secondary" href="#evidence">
            Explore evidence <Arrow />
          </a>
          <a className="button button-secondary" href="#demo">
            Watch demo <Arrow />
          </a>
          <a
            className="button button-secondary"
            href={pinnedRoot}
            target="_blank"
            rel="noreferrer"
          >
            Read the source <Arrow />
          </a>
        </div>
      </div>
      <aside className="receipt" aria-labelledby="receipt-title">
        <div className="receipt-top">
          <div className="receipt-kicker">
            <span className="receipt-label">Observed / read-only receipt</span>
            <span className="receipt-meta">{date} · UTC</span>
          </div>
          <div className="receipt-decision">
            <h2 id="receipt-title">NEED_HUMAN</h2>
            <span className="decision-badge">DATED</span>
          </div>
        </div>
        <div className="receipt-body">
          <p>A route can exist while authority to sign remains unproven.</p>
          <dl className="receipt-grid">
            <div>
              <dt>Proposed action</dt>
              <dd>
                {unsafe.receipt.intent.notional_usd} USDT →{" "}
                {unsafe.view?.representation}
              </dd>
            </div>
            <div>
              <dt>Route exists</dt>
              <dd>{unsafe.view?.route} → NEED_HUMAN</dd>
            </div>
            <div>
              <dt>Evidence missing</dt>
              <dd>Reference time: {evidence.reference_age_status}; holder eligibility and funded passing simulation</dd>
            </div>
            <div>
              <dt>Evidence checked</dt>
              <dd>Catalog, quote, mandate, multiplier; policy {unsafe.receipt.policy_version}</dd>
            </div>
          </dl>
        </div>
        <div className="receipt-foot">
          <span>Context {date} UTC</span>
          <a href="#evidence">Verify receipt bytes</a>
        </div>
      </aside>
    </section>
  );
}

function Demo() {
  return (
    <section id="demo" className="section demo" aria-labelledby="demo-title">
      <div className="section-intro">
        <p className="section-label">Demo / 120 seconds</p>
        <h2 id="demo-title">See the pre-signing review</h2>
        <p>Recorded product walkthrough, 8 October 2026. The packet remains read-only.</p>
      </div>
      <div className="demo-video-wrap">
        <video
          className="demo-video"
          controls
          preload="metadata"
          playsInline
          width="1920"
          height="1080"
        >
          <source src="/media/praeva-bnb-hack-final-v2.mp4" type="video/mp4" />
          Your browser does not support HTML video.
        </video>
      </div>
      <a
        className="demo-download"
        href="/media/praeva-bnb-hack-final-v2.mp4"
        download="praeva-bnb-hack-final-v2.mp4"
      >
        Download the 120-second video <Arrow />
      </a>
      <a className="demo-download" href="/media/praeva-bnb-hack-final.mp4">Historical 63-second film <Arrow /></a>
      <p className="hero-lede">Added after this recording: <a href="https://github.com/dyplux/bnb-tokenized-stocks-2026/blob/850c053354a47e9f4ba10edcfd73a5796addd311/docs/submission/wallet-skills-evidence-2026-10-09.md">official Wallet Skills read-only proof, 9 October</a>. No Agentic Wallet execution is claimed.</p>
    </section>
  );
}

const checks: Array<[string, string]> = [
  ["Market state", "Recognized market state"],
  ["Independent reference integrity", "Independent stock clock"],
  ["Multiplier", "Economic token/share scaling"],
  ["Eligibility", "Issuer/user access evidence"],
  ["Route identity", "Chain/contract/amount identity"],
  ["Price impact / slippage", "Within mandate"],
  ["Mandate", "User spend bound"],
  ["Simulation", "Required preflight evidence"],
];
function Clocks() {
  return (
    <section className="section clocks">
      <div className="section-intro">
        <p className="section-label">01 / clocks and problem</p>
        <h2>A route can exist while its reference clock is missing</h2>
        <p>
          Token venues may trade continuously while underlying price discovery is
          intermittent. The packet records a quote observed at capture.
          Reference age remains UNKNOWN because its timestamp is unavailable.
        </p>
      </div>
      <div className="clock-grid">
        <article>
          <strong>TOKEN price timestamp</strong>
          <span>{String(tokenPriceUpdatedAt)}</span>
          <small>Quote time: {String(evidence.quote_observed_at)}</small>
        </article>
        <article>
          <strong>STOCK reference</strong>
          <span>UNKNOWN</span>
          <small>Receipt evidence has no independent reference timestamp</small>
        </article>
      </div>
      <p className="safety-note">
        SAFETY_ONLY · research finding, not a policy decision or trading edge.{" "}
        <a
          href={`${pinnedFile}experiments/EXP-RWA-004/monday-findings.md`}
          target="_blank"
          rel="noreferrer"
        >
          Monday findings
        </a>
      </p>
    </section>
  );
}
function Checks() {
  return (
    <section className="section checks">
      <div className="section-intro">
        <p className="section-label">03 / eight guards</p>
        <h2>Eight checks before a decision</h2>
      </div>
      <div className="check-grid">
        {checks.map(([name, purpose], i) => (
          <div className="check" key={name}>
            <span>{String(i + 1).padStart(2, "0")}</span>
            <strong>{name}</strong>
            <small>{purpose}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
function Architecture() {
  return (
    <section id="architecture" className="section architecture">
      <div className="section-intro">
        <p className="section-label">04 / architecture</p>
        <h2>Intent becomes evidence, then a bounded verdict</h2>
      </div>
      <div className="flow" role="group" aria-label="Decision flow">
        <span>Intent</span>
        <b aria-hidden="true">→</b>
        <span>Evidence</span>
        <b aria-hidden="true">→</b>
        <span>Deterministic policy</span>
        <b aria-hidden="true">→</b>
        <span className="verdicts">ALLOW / DENY / NEED_HUMAN</span>
        <b aria-hidden="true">→</b>
        <span>Receipt</span>
      </div>
      <div className="signer-boundary">
        <strong>Signer boundary · outside current build</strong>
        <span>
          An agent may propose an action. The deterministic policy returns a
          decision receipt. Signing stays outside this read-only build. NEED_HUMAN
          means required evidence or authorization remains unresolved. Covenant /
          StockGuard overlap exists; this build reviews evidence sufficiency,
          provenance, freshness and authorization prerequisites.
        </span>
      </div>
      <div className="section-intro">
        <h3>Verified execution and runtime proofs, 9 October 2026</h3>
        <p>
          A separate bounded mainnet demo spent 10 USDT and received
          0.012666722432517425 SPYon. The core returned ALLOW after real
          RPC and Binance Transaction API simulations passed. One limited
          approval, one swap and no economic retry. <a href="https://github.com/dyplux/bnb-tokenized-stocks-2026/blob/main/docs/submission/final-proof-2026-10-09.md">Inspect the dated proof</a>.
        </p>
        <p>
          Agent Studio evidence includes testnet Agent ID 2574, dated managed
          replay and a 1 U mainnet x402 settlement. A later operator-assisted
          recovery produced a paid explanation with authority NONE and served
          another request in the same new process. The original process was
          OOM-killed; uninterrupted original self-funding remains unproven.
          The console cases and 120-second film predate these latest proofs.
        </p>
      </div>
    </section>
  );
}
function Integrations() {
  const rows = [
    [
      "Binance Web3 RWA Data",
      "Market / representation / price evidence",
      "docs/devex/2026-10-04-evidence-summary.md",
    ],
    [
      "Trading API",
      "Size-specific quote / route",
      "docs/devex/repros/2026-10-04-rwa-swap-route.md",
    ],
    [
      "Transaction build / simulation",
      "Unsigned preflight; observed prediction FAILED for unfunded wallet",
      "docs/product/pre-execution-packet-linked-2026-10-04.json",
    ],
    [
      "BNB Chain RPC",
      "Fixed-block multiplier",
      "experiments/EXP-RWA-011/onchain_multiplier_audit.json",
    ],
    [
      "bStocks",
      "NVDAB representation / scaling",
      "experiments/EXP-RWA-011/onchain_multiplier_audit.json",
    ],
    [
      "Ondo",
      "NVDAon representation / market evidence",
      "experiments/EXP-RWA-010/results.json",
    ],
  ];
  return (
    <section className="section integrations">
      <div className="section-intro">
        <p className="section-label">05 / integrations</p>
        <h2>Each input has one job</h2>
        <p>
          Independent stock reference is UNKNOWN here, not an integrated
          verified feed.
        </p>
      </div>
      <div className="integration-list">
        {rows.map(([name, contribution, proof]) => (
          <div className="integration-row" key={name}>
            <strong>{name}</strong>
            <span>{contribution}</span>
            <a
              aria-label={`Evidence for ${name}`}
              href={`${pinnedFile}${proof}`}
              target="_blank"
              rel="noreferrer"
            >
              Evidence <Arrow />
            </a>
          </div>
        ))}
      </div>
    </section>
  );
}

export default function HomePage() {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <header className="site-header">
        <div className="header-inner">
          <a className="wordmark" href="/" aria-label="Praeva by Dyplux home">
            <img src="/praeva-logo.svg" width="760" height="200" alt="" />
          </a>
          <nav className="header-nav" aria-label="Primary navigation">
            <a href="/console/">Console</a>
            <a href="#evidence">Evidence</a>
            <a href="#architecture">How it decides</a>
            <a href={pinnedRoot} target="_blank" rel="noreferrer">
              Source
            </a>
          </nav>
        </div>
      </header>
      <main id="main">
        <Hero />
        <Demo />
        <Clocks />
        <section id="evidence" className="section evidence-section">
          <div className="section-intro">
            <p className="section-label">02 / evidence selector</p>
            <h2>Inspect the decision packet</h2>
            <p>
              Unchanged public fixtures. Synthetic inputs are clearly labelled
              and the ALLOW fixture is TEST / 10 USDT.
            </p>
          </div>
          <EvidenceSelector
            cases={[
              observedUnsafe as ReceiptData,
              observedDeny as ReceiptData,
              syntheticSafe as ReceiptData,
            ]}
          />
        </section>
        <Checks />
        <Architecture />
        <Integrations />
        <section id="trust" className="section trust">
          <div className="section-intro">
            <p className="section-label">06 / boundaries</p>
            <h2>Know what the packet can say</h2>
          </div>
          <div className="trust-grid">
            <article>
              <strong>REAL</strong>
              <p>
                Dated public observations, policy inputs, receipt fields, and
                browser hash checks.
              </p>
            </article>
            <article>
              <strong>SYNTHETIC</strong>
              <p>ALLOW is a TEST / 10 USDT fixture. It isn't observed NVDAB.</p>
            </article>
            <article>
              <strong>NOT CLAIMED</strong>
              <p>
                Signing, upstream truth, legal access, funded success, trade, or
                alpha.
              </p>
            </article>
          </div>
        </section>
        <section className="final-cta">
          <p className="section-label">07 / continue</p>
          <h2>Start with the evidence</h2>
          <a className="button button-primary" href="#evidence">
            Review the receipts <Arrow />
          </a>
        </section>
      </main>
      <footer className="site-footer">
        <span>Praeva by Dyplux</span>
        <span>Read-only dated review · {date}</span>
        <nav aria-label="Footer">
          <a
            href="https://dyplux.github.io/bnb-tokenized-stocks-2026/"
            target="_blank"
            rel="noreferrer"
          >
            Live evidence
          </a>
          <a href="#demo">Watch demo</a>
          <a href={`${pinnedFile}JUDGE.md`} target="_blank" rel="noreferrer">
            JUDGE.md
          </a>
          <a
            href="https://github.com/dyplux/bnb-tokenized-stocks-2026"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
          <a href="https://dyplux.com" target="_blank" rel="noreferrer">
            Dyplux
          </a>
        </nav>
      </footer>
    </>
  );
}
