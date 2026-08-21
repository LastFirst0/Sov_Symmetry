export const RESEARCH_FEED_URL = "/manus-storage/research_dashboard_feed_updated_af750af8.json";

export type WorkPackage = {
  work_package_id: string; title: string; lane: string; status: string; claim_class: string; question: string;
  source_manifests: string[]; outputs: { kind: string; schema_or_format: string }[]; non_claims: string[]; risk_level: string; decision_gate: string; owner_role: string;
};
export type FalsificationEntry = { id: string; title: string; status: string; statement: string; contrary_result: string; evidence: string; next_obligation: string };
export type ResearchFeed = {
  schema: "sov.research_dashboard_feed"; schema_version: "0.1.0"; scope: string; work_packages: WorkPackage[]; falsification_entries: FalsificationEntry[];
  adapter_review: { adapter_id: string; status: string; review_state: string }[]; adapter_review_state_board: { state: string; record_count: number; adapter_ids: string[]; evidence_note: string }[]; release_verification: { status: string; reason_code?: string; checked_file_count?: number; scope?: string };
  m0_experiment: null | { status: string; verdict: string; verdict_reason: string; aggregate: Record<string, Record<string, { auroc: number; average_precision: number }>>; constants: { seeds: number[]; kmer_size: number; projection_dimensions: number; bootstrap_rounds: number }; limitations: string[]; dataset_manifest_sha256: string };
  artifacts: { role: string; state: string; path: string; sha256?: string }[]; operational_boundary: string;
};
export type ResearchLoad = { state: "loading" | "ready" | "unavailable"; feed: ResearchFeed | null; message: string };
export const emptyResearchLoad: ResearchLoad = { state: "loading", feed: null, message: "Loading generated research feed…" };

function string(value: unknown): value is string { return typeof value === "string" && value.length > 0; }
function isFeed(value: unknown): value is ResearchFeed {
  if (!value || typeof value !== "object") return false;
  const data = value as Partial<ResearchFeed>;
  return data.schema === "sov.research_dashboard_feed" && data.schema_version === "0.1.0" && Array.isArray(data.work_packages) && Array.isArray(data.falsification_entries) && Array.isArray(data.adapter_review) && Array.isArray(data.adapter_review_state_board) && Array.isArray(data.artifacts) && string(data.scope) && !!data.release_verification && string(data.operational_boundary);
}

export async function loadResearchFeed(fetcher: typeof fetch = fetch): Promise<ResearchLoad> {
  try {
    const response = await fetcher(RESEARCH_FEED_URL);
    if (!response.ok) throw new Error(`Research feed returned ${response.status}`);
    const candidate: unknown = await response.json();
    if (!isFeed(candidate)) throw new Error("Research feed schema was not accepted");
    return { state: "ready", feed: candidate, message: "Generated research artifacts loaded." };
  } catch (error) {
    return { state: "unavailable", feed: null, message: error instanceof Error ? error.message : "Research feed unavailable" };
  }
}
