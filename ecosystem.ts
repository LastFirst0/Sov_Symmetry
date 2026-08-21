export const ECOSYSTEM_FEED_URL = "/manus-storage/ecosystem_dashboard_feed_updated_7de2da58.json";

export type KernelStatus = "verified" | "fail" | "unverifiable";
export type JourneySample = { declared_input: unknown; receipt: { receipt_id: string; status: KernelStatus; what_i_checked?: string; why?: string; plain_status?: string; scope?: string } };
export type KernelJourney = { id: string; title: string; adapter_id: string; non_claim: string; baseline: JourneySample; mutation: JourneySample; unverifiable: JourneySample };
export type EcosystemFeed = {
  schema: "sov.ecosystem_dashboard_feed";
  schema_version: "0.1.0";
  release_scope: string;
  documentation: { canonical_entries: number; archival_entries: number; tiers: string[] };
  adapters: Array<{ adapter_id: string; version: string; predicate_id: string; status: "admitted" | "candidate"; claimed_domain: string; non_claims: string[] }>;
  journeys: KernelJourney[];
  claim_classes: Array<{ id: string; label: string; meaning: string; limitation: string }>;
  operational_boundaries: string[];
};
export type EcosystemLoad = { state: "loading" | "ready" | "unavailable"; feed: EcosystemFeed | null; message?: string };
export const emptyEcosystemLoad: EcosystemLoad = { state: "loading", feed: null };

function isStatus(value: unknown): value is KernelStatus { return value === "verified" || value === "fail" || value === "unverifiable"; }
function isSample(value: unknown): value is JourneySample { if (!value || typeof value !== "object") return false; const receipt = (value as { receipt?: unknown }).receipt; return !!receipt && typeof receipt === "object" && typeof (receipt as { receipt_id?: unknown }).receipt_id === "string" && isStatus((receipt as { status?: unknown }).status); }
function isFeed(value: unknown): value is EcosystemFeed { if (!value || typeof value !== "object") return false; const item = value as Partial<EcosystemFeed>; return item.schema === "sov.ecosystem_dashboard_feed" && item.schema_version === "0.1.0" && typeof item.release_scope === "string" && !!item.documentation && Array.isArray(item.journeys) && item.journeys.length === 6 && item.journeys.every((journey) => typeof journey.id === "string" && typeof journey.title === "string" && isSample(journey.baseline) && isSample(journey.mutation) && isSample(journey.unverifiable)) && Array.isArray(item.adapters) && Array.isArray(item.claim_classes) && Array.isArray(item.operational_boundaries); }

export async function loadEcosystemFeed(): Promise<EcosystemLoad> {
  try { const response = await fetch(ECOSYSTEM_FEED_URL); if (!response.ok) throw new Error("Ecosystem release feed could not be fetched"); const candidate: unknown = await response.json(); if (!isFeed(candidate)) throw new Error("Ecosystem release feed has an unsupported schema"); return { state: "ready", feed: candidate }; }
  catch (error) { return { state: "unavailable", feed: null, message: error instanceof Error ? error.message : "Ecosystem release feed unavailable" }; }
}
