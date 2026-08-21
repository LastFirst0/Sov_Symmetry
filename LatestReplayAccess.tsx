import { ExternalLink, FileCheck2, ShieldCheck } from "lucide-react";

const latestReplay = {
  label: "Full Platform End-to-End Replay",
  runId: "32232417722",
  runUrl: "https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32232417722",
  evidenceUrl: "https://github.com/LastFirst0/sovereign-engine-dashboard/blob/main/docs/full_platform_end_to_end_replay_2026-08-19.md",
  scope: "Dashboard contracts/build, checksum-pinned kernel matrix, focused corpus/adapter tests, and retired/active public-material bundle verification completed in one fresh hosted runner.",
};

export function LatestReplayAccess() {
  return (
    <section className="archive-visuals" aria-label="Latest retained replay access">
      <div className="filter-title">
        <FileCheck2 size={16} />
        <div>
          <p className="eyebrow">LATEST RETAINED REPLAY</p>
          <h2>{latestReplay.label}</h2>
        </div>
        <span>run {latestReplay.runId}</span>
      </div>
      <div className="signal-stat">
        <span>Scope</span>
        <strong>Single-runner evidence</strong>
        <small>{latestReplay.scope}</small>
      </div>
      <div className="record-actions">
        <a href={latestReplay.runUrl} target="_blank" rel="noreferrer"><ExternalLink size={13} /> Open hosted run</a>
        <a href={latestReplay.evidenceUrl} target="_blank" rel="noreferrer"><ShieldCheck size={13} /> Read retained evidence record</a>
      </div>
      <small>These links expose recorded software and integrity evidence; they do not establish a theory, publish an artifact, or admit an adapter.</small>
    </section>
  );
}

export { latestReplay };
