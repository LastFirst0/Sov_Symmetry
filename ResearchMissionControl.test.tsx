import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import ResearchMissionControl, { AdapterReviewStateBoard, ResearchFeedUnavailable } from "./ResearchMissionControl";

const readyResearch = { state: "ready" as const, message: "Loaded", feed: { schema: "sov.research_dashboard_feed" as const, schema_version: "0.1.0" as const, scope: "generated evidence", work_packages: [{ work_package_id: "m0.dna_geometry", title: "M0 public DNA", lane: "molecular_geometry", status: "complete", claim_class: "experimental_result", question: "Does it improve?", source_manifests: ["m0"], outputs: [], non_claims: ["No health claim"], risk_level: "medium", decision_gate: "protocol_review", owner_role: "research_protocol_steward" }], falsification_entries: [{ id: "H-DNA-01", title: "DNA geometry", status: "tested_fail", statement: "s", contrary_result: "No advantage", evidence: "a", next_obligation: "Replicate" }], adapter_review: [{ adapter_id: "candidate.adapter", status: "candidate", review_state: "candidate" }], adapter_review_state_board: [{ state: "candidate", record_count: 1, adapter_ids: ["candidate.adapter"], evidence_note: "Record present" }, { state: "reviewed_admitted", record_count: 1, adapter_ids: ["admitted.adapter"], evidence_note: "Record present" }, { state: "blocked", record_count: 0, adapter_ids: [], evidence_note: "No record" }, { state: "unavailable", record_count: 0, adapter_ids: [], evidence_note: "No record" }], release_verification: { status: "unverifiable" }, m0_experiment: { status: "verified", verdict: "fail", verdict_reason: "No advantage", aggregate: { test: { hyperbolic_poincare_prototype: { auroc: 0.75, average_precision: 0.8 }, matched_euclidean_prototype: { auroc: 0.75, average_precision: 0.8 }, shuffled_label_control: { auroc: 0.5, average_precision: 0.5 } } }, constants: { seeds: [17, 43, 97], kmer_size: 5, projection_dimensions: 16, bootstrap_rounds: 200 }, limitations: ["No health claim", "No biological conclusion"], dataset_manifest_sha256: "abc" }, artifacts: [{ role: "m0_evaluation_bundle", state: "available", path: "artifact", sha256: "abcd" }], operational_boundary: "No automatic promotion" } };

describe("ResearchMissionControl", () => {
  it("renders the loading-safe research control entry points", () => {
    const html = renderToStaticMarkup(<ResearchMissionControl />);
    expect(html).toContain("Reality trace for every research claim");
    expect(html).toContain("Loading generated research artifacts");
    expect(html).toContain("RESEARCH MISSION CONTROL");
  });
  it("renders generated ready-state M0, adapter review, and evidence boundaries", () => {
    const html = renderToStaticMarkup(<ResearchMissionControl initialResearch={readyResearch} />);
    expect(html).toContain("did not clear its advantage gate");
    expect(html).toContain("M0 public DNA");
    expect(html).toContain("reviewed / admitted");
    expect(html).toContain("No automatic promotion");
  });
  it("renders the four generated adapter-review states without inventing member records", () => {
    const html = renderToStaticMarkup(<AdapterReviewStateBoard states={readyResearch.feed.adapter_review_state_board} />);
    expect(html).toContain("candidate");
    expect(html).toContain("reviewed / admitted");
    expect(html).toContain("blocked");
    expect(html).toContain("unavailable");
    expect(html).toContain("No record");
  });
  it("renders a fail-closed unavailable state with a retry control", () => {
    const html = renderToStaticMarkup(<ResearchFeedUnavailable research={{ state: "unavailable", feed: null, message: "Schema rejected" }} onRetry={() => undefined} />);
    expect(html).toContain("Research control feed unavailable");
    expect(html).toContain("Retry artifact feed");
  });
});
