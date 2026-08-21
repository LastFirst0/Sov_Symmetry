export type ArtifactCategory = "research_register" | "falsification" | "experiment" | "release" | "governance";
export type ArtifactStatus = "verified" | "fail" | "unverifiable" | "unavailable";
export type PersistedArtifact = { id: number; artifactKey: string; title: string; category: ArtifactCategory; status: ArtifactStatus; sourceUrl: string; contentDigest: string | null; summary: string; limitation: string; publicationState: "staged" | "published"; revision: number; metadataDigest: string | null; updatedBy: string; updatedAt: Date };
export type PersistedAudit = { id: number; artifactKey: string; revision: number; action: "create" | "update" | "backfill"; actorType: "owner_token" | "system_backfill"; actorLabel: string; priorMetadataDigest: string | null; metadataDigest: string; recordSnapshot: string; createdAt: Date };
export type ArchiveLoad = { state: "loading" | "ready" | "unavailable"; records: PersistedArtifact[]; message?: string };

export function archiveLoadFromQuery(input: { isLoading: boolean; error: unknown; data?: PersistedArtifact[] }): ArchiveLoad {
  if (input.isLoading) return { state: "loading", records: [] };
  if (input.error || !Array.isArray(input.data)) return { state: "unavailable", records: [], message: "Persisted research archive is unavailable." };
  return { state: "ready", records: input.data };
}
