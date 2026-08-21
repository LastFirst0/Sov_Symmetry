/**
 * Mission Control Ledger: a graphite-and-oxide research operations dashboard.
 * Visual rules: asymmetric command rail, operational grids, serif strategy headings,
 * monospaced telemetry, and restrained Signal Oxide accents (#D64635).
 */
import { useEffect, useMemo, useState } from "react";
import { documentationCards } from "@/lib/documentation";
import { emptyEvidenceSummary, loadQ1Evidence, type Q1EvidenceSummary } from "@/lib/evidence";
import { Link } from "wouter";
import {
  Activity,
  ArrowUpRight,
  BookOpen,
  Boxes,
  Check,
  ChevronRight,
  CircleDot,
  Command,
  FlaskConical,
  FolderKanban,
  FileText,
  GitBranch,
  Layers3,
  Network,
  Radar,
  Search,
  ShieldCheck,
  Sparkles,
  TriangleAlert,
} from "lucide-react";

type Status = "active" | "verified" | "planned" | "unresolved";

type Workstream = {
  id: string;
  label: string;
  short: string;
  owner: string;
  status: Status;
  progress: number;
  output: string;
  next: string;
  evidence: string;
};

const workstreams: Workstream[] = [
  { id: "WS-A", label: "Meaning & ontology", short: "Ontology", owner: "Research architect", status: "active", progress: 64, output: "Versioned meaning-layer specification", next: "Produce the machine-readable priority glossary and equation registry.", evidence: "Transcript inventory, tensor deep dive, source-span mapping" },
  { id: "WS-B", label: "Tensor & geometry kernel", short: "Kernel", owner: "Mathematical software lead", status: "active", progress: 38, output: "Tested tensor / geometry library", next: "Extend flat fixture to curved, torsion, and failure cases.", evidence: "11 flat-fixture invariant checks; API and kernel blueprint" },
  { id: "WS-C", label: "Verification & evidence", short: "Evidence", owner: "Reliability lead", status: "active", progress: 31, output: "Evidence ledger and status engine", next: "Register replay, hash, and invariant predicates.", evidence: "Evidence schema, status contract, simulation record" },
  { id: "WS-D", label: "Runtime & intelligence", short: "Runtime", owner: "Systems lead", status: "planned", progress: 14, output: "Geometry-aware reasoning runtime", next: "Define the runtime request envelope and trace model.", evidence: "Architecture intent and adapter boundary" },
  { id: "WS-E", label: "Embodiment & UX", short: "Embodiment", owner: "Product / visualization lead", status: "planned", progress: 22, output: "Demonstration suite and user journeys", next: "Select three outsider-readable demonstration journeys.", evidence: "Explorer archive inventory and deck" },
  { id: "WS-F", label: "API & developer platform", short: "API", owner: "API / platform lead", status: "verified", progress: 46, output: "Client-generation-ready platform", next: "Generate Python, TypeScript, and Rust client baselines.", evidence: "Validated OpenAPI 3.0 contract" },
  { id: "WS-G", label: "Program automation", short: "Automation", owner: "Automation lead", status: "planned", progress: 18, output: "Repeatable orchestration workflows", next: "Establish task templates and structured work-result schema.", evidence: "Manus API operating strategy" },
  { id: "WS-H", label: "Scientific validation", short: "Validation", owner: "Independent review lead", status: "unresolved", progress: 9, output: "Claim and limitation register", next: "Formalize falsification obligations for GU-specific claims.", evidence: "External source findings and hypothesis boundaries" },
];

const milestones = [
  { id: "M0", name: "Coherent program", state: "complete", caption: "Charter / baseline / control center" },
  { id: "M1", name: "Meaning kernel", state: "active", caption: "Glossary / claim graph / equation registry" },
  { id: "M2", name: "Verified geometry", state: "next", caption: "Typed kernel / fixtures / replay" },
  { id: "M3", name: "Evidence runtime", state: "future", caption: "Ledger / claim evaluator / adapters" },
  { id: "M4", name: "Demonstration system", state: "future", caption: "Tensor lab / geometry explorer" },
  { id: "M5", name: "Developer platform", state: "future", caption: "SDKs / CLI / MCP / webhooks" },
  { id: "M6", name: "Automated program", state: "future", caption: "Structured task and review loops" },
  { id: "M7", name: "Scientific review", state: "future", caption: "Benchmarks / falsification register" },
];

const artifactRows = [
  ["Meaning layer dossier", "WS-A", "baseline", "Promote concepts into registry"],
  ["Tensor calculus deep dive", "WS-A", "baseline", "Convert equations into fixture records"],
  ["Tensor blueprint + API", "WS-B / WS-F", "active", "Align module boundaries"],
  ["OpenAPI 3.0 specification", "WS-F", "verified", "Generate SDK baselines"],
  ["Tensor-state simulation", "WS-B / WS-C", "verified", "Add non-flat + failure fixtures"],
];

const statusStyle: Record<Status, string> = {
  active: "bg-[#d64635] text-white",
  verified: "bg-[#acc2a8] text-[#102018]",
  planned: "bg-[#c1c8cf] text-[#17222d]",
  unresolved: "bg-[#e3bb72] text-[#3a2400]",
};

function StatusStamp({ status }: { status: Status }) {
  return <span className={`status-stamp ${statusStyle[status]}`}><span className="status-dot" />{status}</span>;
}

function SectionHeader({ label, title, action, actionHref }: { label: string; title: string; action?: string; actionHref?: string }) {
  return (
    <div className="section-head">
      <div>
        <p className="eyebrow">{label}</p>
        <h2>{title}</h2>
      </div>
      {action && actionHref && <Link className="text-action" href={actionHref}>{action}<ArrowUpRight size={14} /></Link>}
    </div>
  );
}

export default function Home() {
  const [activeNav, setActiveNav] = useState("Overview");
  const [filter, setFilter] = useState<"all" | Status>("all");
  const [selectedId, setSelectedId] = useState("WS-A");
  const [query, setQuery] = useState("");
  const [evidence, setEvidence] = useState<Q1EvidenceSummary>(emptyEvidenceSummary);
  const selected = workstreams.find((item) => item.id === selectedId) ?? workstreams[0];
  const filtered = useMemo(() => workstreams.filter((item) => {
    const matchesStatus = filter === "all" || item.status === filter;
    const haystack = `${item.label} ${item.owner} ${item.output}`.toLowerCase();
    return matchesStatus && haystack.includes(query.toLowerCase());
  }), [filter, query]);
  useEffect(() => { void loadQ1Evidence().then(setEvidence); }, []);

  return (
    <div className="app-shell">
      <aside className="command-rail">
        <div className="brand-lockup">
          <img className="brand-mark" src="/manus-storage/sovereign-mark_983baceb.png" alt="Sovereign Engine mark" />
          <div><span className="brand-name">SOVEREIGN</span><span className="brand-sub">ENGINE / PROGRAM</span></div>
        </div>

        <nav className="rail-nav" aria-label="Dashboard sections">
          {[{ label: "Overview", icon: Radar, href: "#overview" }, { label: "Workstreams", icon: Layers3, href: "#workstreams" }, { label: "Milestones", icon: GitBranch, href: "#milestones" }, { label: "Evidence", icon: ShieldCheck, href: "#evidence" }, { label: "Artifacts", icon: FolderKanban, href: "#artifacts" }, { label: "Docs", icon: FileText, href: "/docs" }].map(({ label, icon: Icon, href }) => (
            label === "Docs" ? <Link key={label} href={href} className={activeNav === label ? "rail-nav-item active" : "rail-nav-item"} onClick={() => setActiveNav(label)}><Icon size={17} /><span>{label}</span></Link> : <a key={label} href={href} onClick={() => setActiveNav(label)} className={activeNav === label ? "rail-nav-item active" : "rail-nav-item"}>
              <Icon size={17} /><span>{label}</span>
            </a>
          ))}
        </nav>

        <div className="rail-bottom">
          <div className="signal-block"><span className="signal-label">PROGRAM STATUS</span><strong>BASELINE LOCKED</strong><span>Commit 1678023</span></div>
          <Link href="/archive" className="operator"><Command size={15} /> Open operator console</Link>
        </div>
      </aside>

      <main className="command-canvas">
        <header className="topbar">
          <div className="breadcrumb"><span>PROGRAM CONTROL</span><ChevronRight size={13} /><strong>{activeNav.toUpperCase()}</strong></div>
          <div className="topbar-actions"><span className="live-readout"><i />SYSTEM SYNCHRONIZED</span><Link href="/archive" className="avatar-button" aria-label="Open archive operations">SE</Link></div>
        </header>

        <section className="hero-field">
          <img className="hero-image" src="/manus-storage/sovereign-hero-field_68eabae4.png" alt="Abstract geometric mission-control field" />
          <div className="hero-overlay" />
          <div className="hero-content">
            <p className="eyebrow on-dark">SOVEREIGN ENGINE / OPERATING MAP</p>
            <h1>Advance only when<br /><em>the invariant survives.</em></h1>
            <p className="hero-copy">A unified development surface for the geometry-native meaning system: workstreams, evidence posture, milestone gates, and the next coordinated execution wave.</p>
            <div className="hero-metrics">
              <div><strong>8</strong><span>WORKSTREAMS</span></div>
              <div><strong>8</strong><span>MILESTONES</span></div>
              <div><strong>{evidence.q0FuzzCases?.toLocaleString() ?? "—"}</strong><span>{evidence.state === "verified" ? "VERIFIED FUZZ CASES" : "EVIDENCE LOADING"}</span></div>
            </div>
          </div>
          <div className="hero-corner"><span>LIVE PROGRAM SIGNAL</span><Activity size={16} /></div>
        </section>

        <section className="overview-grid" id="overview">
          <article className="north-star-panel">
            <p className="eyebrow">NORTH STAR</p>
            <h2>Geometry-native, provenance-aware, <span>verifiable meaning.</span></h2>
            <p>Build meaning infrastructure that maintains a strict boundary between established mathematics, repository observations, tested software contracts, and unresolved Geometric Unity hypotheses.</p>
            <div className="layer-strip"><span>ONTOLOGY</span><b>→</b><span>KERNEL</span><b>→</b><span>EVIDENCE</span><b>→</b><span>RUNTIME</span><b>→</b><span>EMBODIMENT</span></div>
          </article>
          <article className="gate-panel">
            <div className="gate-top"><p className="eyebrow">CURRENT GATE</p><StatusStamp status="active" /></div>
            <h3>Gate 1<br />Meaning Layer</h3>
            <p>Every priority term and equation has an owner, normalized notation, source span, claim class, and proof/test or explicit unresolved state.</p>
            <div className="gate-progress"><span>{evidence.state === "verified" ? `Q1 ORACLE ${evidence.q1Passed}/${evidence.q1Cases} PASS` : evidence.state === "unavailable" ? "Q1 EVIDENCE UNAVAILABLE" : "Q1 EVIDENCE LOADING"}</span><div><i style={{ width: evidence.state === "verified" && evidence.q1Cases ? `${(evidence.q1Passed! / evidence.q1Cases) * 100}%` : "0%" }} /></div></div>
          </article>
        </section>

        <section className="roadmap-section" id="milestones">
          <SectionHeader label="PROGRAM TRAJECTORY" title="Milestone signal line" action="Open research roadmap" actionHref="/research" />
          <div className="signal-line" aria-label="Sovereign Engine milestone progression">
            {milestones.map((milestone, index) => (
              <button className={`milestone ${milestone.state}`} type="button" key={milestone.id} onClick={() => setActiveNav("Milestones")}>
                <span className="mile-node">{milestone.state === "complete" ? <Check size={13} /> : index + 1}</span>
                <span className="mile-id">{milestone.id}</span>
                <strong>{milestone.name}</strong>
                <small>{milestone.caption}</small>
              </button>
            ))}
          </div>
        </section>

        <section className="workstream-section" id="workstreams">
          <SectionHeader label="COORDINATED EXECUTION" title="Workstream field" action="View control center" actionHref="/research" />
          <div className="workstream-toolbar">
            <div className="filter-group" aria-label="Filter workstreams by status">
              {(["all", "active", "verified", "planned", "unresolved"] as const).map((option) => <button key={option} type="button" onClick={() => setFilter(option)} className={filter === option ? "filter-button selected" : "filter-button"}>{option}</button>)}
            </div>
            <label className="search-box"><Search size={15} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search stream or owner" /></label>
          </div>
          <div className="workstream-layout">
            <div className="workstream-list">
              {filtered.map((stream) => <button type="button" key={stream.id} onClick={() => setSelectedId(stream.id)} className={selectedId === stream.id ? "stream-row selected" : "stream-row"}>
                <span className="stream-id">{stream.id}</span>
                <span className="stream-main"><strong>{stream.label}</strong><small>{stream.owner}</small></span>
                <span className="stream-progress"><i style={{ width: `${stream.progress}%` }} /><small>{stream.progress}%</small></span>
                <StatusStamp status={stream.status} />
                <ChevronRight size={16} className="stream-arrow" />
              </button>)}
            </div>
            <aside className="inspection-panel">
              <div className="inspection-heading"><span className="crosshair" /><p className="eyebrow">STREAM INSPECTION</p></div>
              <div className="inspection-title"><span>{selected.id}</span><StatusStamp status={selected.status} /></div>
              <h3>{selected.label}</h3>
              <p className="owner-line">OWNER / {selected.owner.toUpperCase()}</p>
              <dl><div><dt>EXIT ARTIFACT</dt><dd>{selected.output}</dd></div><div><dt>NEXT DECISION</dt><dd>{selected.next}</dd></div><div><dt>EVIDENCE BASIS</dt><dd>{selected.evidence}</dd></div></dl>
              <Link href="/research" className="inspect-button">Open work package <ArrowUpRight size={15} /></Link>
            </aside>
          </div>
        </section>

        <section className="bottom-grid" id="artifacts">
          <article className="artifact-panel">
            <SectionHeader label="CONTROLLED ARTIFACTS" title="Current source-of-truth assets" />
            <div className="artifact-table">
              <div className="artifact-row artifact-head"><span>ARTIFACT</span><span>OWNER</span><span>STATUS</span><span>NEXT DECISION</span></div>
              {artifactRows.map(([artifact, owner, state, next]) => <div className="artifact-row" key={artifact}><span><BookOpen size={14} />{artifact}</span><span>{owner}</span><span><span className={`mini-state ${state}`}>{state}</span></span><span>{next}</span></div>)}
            </div>
          </article>
          <article className="evidence-panel" id="evidence">
            <img src="/manus-storage/sovereign-evidence-grid_7f17ba8f.png" alt="Abstract evidence ledger grid" />
            <div className="evidence-shade" />
            <div className="evidence-content"><p className="eyebrow on-dark">EVIDENCE POSTURE</p><h3>Every result names<br />its <em>boundary.</em></h3><p>Standard mathematics, transcript mappings, repository observations, software contracts, and GU hypotheses remain visibly distinct.</p><Link href="/research">Review claim matrix <ArrowUpRight size={14} /></Link></div>
          </article>
        </section>

        <section className="documentation-section" id="documentation-site">
          <SectionHeader label="DOCUMENTATION SITE" title="Evidence index" action="Open evidence index" actionHref="/docs" />
          <div className="documentation-grid">
            {documentationCards.map((card) => <article className="documentation-card" key={card.title}>
              <div className="doc-card-top"><span className="eyebrow">{card.label}</span><span className={`mini-state ${card.status}`}>{card.status}</span></div>
              <h3>{card.title}</h3>
              <p>{card.body}</p>
              <Link href="/docs" className="text-action">Read evidence <ArrowUpRight size={14} /></Link>
            </article>)}
          </div>
        </section>

        <section className="execution-wave">
          <div className="wave-copy"><p className="eyebrow">NEXT COORDINATED WAVE</p><h2>M1 → M2 foundation packet</h2><p>Deliver the machine-readable glossary, non-flat fixture suite, invariant registry, runtime request schema, and three selected demonstration journeys as one shared substrate.</p></div>
          <div className="wave-orbit"><img src="/manus-storage/sovereign-geometry-orbit_252bdcf3.png" alt="Abstract geometric transformation orbit" /></div>
          <div className="wave-actions"><Link href="/archive" className="primary-action"><Sparkles size={16} /> Assemble work package</Link><Link href="/lab" className="secondary-action"><FlaskConical size={16} /> Review fixture evidence</Link></div>
        </section>
      </main>
    </div>
  );
}
