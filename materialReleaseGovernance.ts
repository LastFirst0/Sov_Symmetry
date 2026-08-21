const REPOSITORY = "LastFirst0/sovereign-engine-dashboard";
const REPOSITORY_PATH = `/repos/${REPOSITORY}`;
const UNIFIED_REPLAY_WORKFLOW = "full_platform_end_to_end_replay.yml";
const MATERIAL_GATE_WORKFLOW = "material_release_gate.yml";
const APPROVAL_WORKFLOW = "approve_material_release_tag.yml";

type GitHubWorkflowRun = {
  id: number;
  name: string;
  head_sha: string;
  conclusion: string | null;
  html_url: string;
  created_at: string;
  updated_at: string;
};

type GitHubWorkflowRuns = { workflow_runs?: GitHubWorkflowRun[] };
type GitReference = { ref: string; object: { sha: string; type: "commit" | "tag" } };
type GitTag = { object: { sha: string; type: "commit" } };
type GitHubContent = { name: string; path: string; content?: string; encoding?: string; html_url?: string };
type GitHubRelease = { id: number; tag_name: string; target_commitish: string; html_url: string; published_at: string | null; created_at: string };
type ApprovalRecord = { tag: string; targetSha: string; approvedBy: string; approvedAt: string; sourceUrl: string };

export type ReleaseEvidenceResult = "verified" | "fail" | "unverifiable";
export type PublicReleaseEvidence = {
  evidenceId: string;
  kind: "unified_replay" | "material_gate" | "tag_approval" | "published_release";
  title: string;
  result: ReleaseEvidenceResult;
  sourceCommit: string | null;
  occurredAt: string;
  sourceUrl: string;
  testScope: string;
  limitation: string;
};

export type MaterialTagPreview = {
  tag: string;
  targetSha: string | null;
  unifiedReplay: { runId: number; result: ReleaseEvidenceResult; url: string; completedAt: string } | null;
  materialGate: { runId: number; result: ReleaseEvidenceResult; url: string; completedAt: string } | null;
  approval: { approvedBy: string; approvedAt: string; sourceUrl: string } | null;
  publishedRelease: { url: string; publishedAt: string | null } | null;
  eligibleForApproval: boolean;
};

export function isMaterialReleaseTag(tag: string) {
  return /^material-release-[A-Za-z0-9._-]+$/.test(tag);
}

export function classifyWorkflowConclusion(conclusion: string | null): ReleaseEvidenceResult {
  if (conclusion === "success") return "verified";
  if (conclusion === null) return "unverifiable";
  return "fail";
}

function githubToken() {
  const token = process.env.SOVEREIGN_GITHUB_RELEASE_TOKEN;
  if (!token) throw new Error("GITHUB_RELEASE_INTEGRATION_UNAVAILABLE");
  return token;
}

async function githubJson<T>(path: string, init: RequestInit = {}, allowNotFound = false): Promise<T | null> {
  const response = await fetch(`https://api.github.com${path}`, {
    ...init,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${githubToken()}`,
      "X-GitHub-Api-Version": "2022-11-28",
      ...init.headers,
    },
  });
  if (response.status === 404 && allowNotFound) return null;
  if (!response.ok) throw new Error(`GITHUB_RELEASE_API_${response.status}`);
  if (response.status === 204) return null;
  return response.json() as Promise<T>;
}

async function matchingWorkflowRuns(workflow: string, sourceCommit?: string) {
  const query = new URLSearchParams({ per_page: "25" });
  if (sourceCommit) query.set("head_sha", sourceCommit);
  const result = await githubJson<GitHubWorkflowRuns>(`${REPOSITORY_PATH}/actions/workflows/${workflow}/runs?${query.toString()}`);
  return result?.workflow_runs ?? [];
}

async function resolveTagCommit(tag: string) {
  const reference = await githubJson<GitReference>(`${REPOSITORY_PATH}/git/ref/tags/${encodeURIComponent(tag)}`, {}, true);
  if (!reference) return null;
  if (reference.object.type === "commit") return reference.object.sha;
  const annotatedTag = await githubJson<GitTag>(`${REPOSITORY_PATH}/git/tags/${reference.object.sha}`, {}, true);
  return annotatedTag?.object.type === "commit" ? annotatedTag.object.sha : null;
}

function workflowSummary(run: GitHubWorkflowRun | undefined) {
  if (!run) return null;
  return { runId: run.id, result: classifyWorkflowConclusion(run.conclusion), url: run.html_url, completedAt: run.updated_at };
}

async function approvalForTag(tag: string): Promise<ApprovalRecord | null> {
  const path = `release-approvals/${tag}.json`;
  const content = await githubJson<GitHubContent>(`${REPOSITORY_PATH}/contents/${path}?ref=main`, {}, true);
  if (!content?.content || content.encoding !== "base64") return null;
  try {
    const parsed = JSON.parse(Buffer.from(content.content.replace(/\n/g, ""), "base64").toString("utf8")) as { schema?: string; status?: string; tag?: string; targetSha?: string; approvedBy?: string; approvedAt?: string };
    const targetSha = parsed.targetSha;
    const approvedBy = parsed.approvedBy;
    const approvedAt = parsed.approvedAt;
    if (parsed.schema !== "sov.material_release_approval.v0.1" || parsed.status !== "approved" || parsed.tag !== tag || typeof targetSha !== "string" || typeof approvedBy !== "string" || typeof approvedAt !== "string") return null;
    return { tag, targetSha, approvedBy, approvedAt, sourceUrl: content.html_url ?? `https://github.com/${REPOSITORY}/blob/main/${path}` };
  } catch {
    return null;
  }
}

export async function previewMaterialReleaseTag(tag: string): Promise<MaterialTagPreview> {
  if (!isMaterialReleaseTag(tag)) throw new Error("MATERIAL_RELEASE_TAG_REQUIRED");
  const targetSha = await resolveTagCommit(tag);
  if (!targetSha) return { tag, targetSha: null, unifiedReplay: null, materialGate: null, approval: null, publishedRelease: null, eligibleForApproval: false };

  const [unifiedRuns, gateRuns, approval, release] = await Promise.all([
    matchingWorkflowRuns(UNIFIED_REPLAY_WORKFLOW, targetSha),
    matchingWorkflowRuns(MATERIAL_GATE_WORKFLOW, targetSha),
    approvalForTag(tag),
    githubJson<GitHubRelease>(`${REPOSITORY_PATH}/releases/tags/${encodeURIComponent(tag)}`, {}, true),
  ]);
  const unifiedReplay = workflowSummary(unifiedRuns.find((run) => run.head_sha === targetSha && run.name === "Full Platform End-to-End Replay" && run.conclusion === "success"));
  const materialGate = workflowSummary(gateRuns.find((run) => run.head_sha === targetSha && run.name === "Material Release Gate" && run.conclusion === "success"));
  const matchingApproval = approval?.targetSha === targetSha ? approval : null;
  const publishedRelease = release ? { url: release.html_url, publishedAt: release.published_at } : null;
  return { tag, targetSha, unifiedReplay, materialGate, approval: matchingApproval, publishedRelease, eligibleForApproval: Boolean(unifiedReplay && materialGate && !matchingApproval && !publishedRelease) };
}

export async function listOwnerMaterialReleaseTags() {
  const references = await githubJson<GitReference[]>(`${REPOSITORY_PATH}/git/matching-refs/tags/material-release-`) ?? [];
  const tags = references.map((reference) => reference.ref.replace("refs/tags/", "")).filter(isMaterialReleaseTag).sort().reverse().slice(0, 20);
  return Promise.all(tags.map((tag) => previewMaterialReleaseTag(tag)));
}

export async function dispatchMaterialReleaseApproval(tag: string) {
  const preview = await previewMaterialReleaseTag(tag);
  if (!preview.eligibleForApproval) throw new Error("MATERIAL_RELEASE_TAG_NOT_ELIGIBLE_FOR_APPROVAL");
  await githubJson<never>(`${REPOSITORY_PATH}/actions/workflows/${APPROVAL_WORKFLOW}/dispatches`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ref: "main", inputs: { tag } }),
  });
  return { tag, workflowUrl: `https://github.com/${REPOSITORY}/actions/workflows/${APPROVAL_WORKFLOW}`, status: "approval_dispatch_recorded" as const };
}

function workflowEvidence(run: GitHubWorkflowRun, kind: "unified_replay" | "material_gate"): PublicReleaseEvidence {
  const unified = kind === "unified_replay";
  return {
    evidenceId: `${kind}:${run.id}`,
    kind,
    title: unified ? "Full Platform End-to-End Replay" : "Material Release Gate",
    result: classifyWorkflowConclusion(run.conclusion),
    sourceCommit: run.head_sha,
    occurredAt: run.updated_at,
    sourceUrl: run.html_url,
    testScope: unified ? "Dashboard contracts and production build; checksum-pinned bounded kernel matrix; focused corpus/adapter checks; retained public-material continuity verification." : "Exact-commit material-release gate requiring a successful unified replay and retained evidence artifact.",
    limitation: unified ? "A successful replay verifies the declared bounded fixtures and contracts for the recorded source commit; it does not establish semantic truth outside that scope." : "A successful gate records eligibility for the formal tag process; it does not itself approve or publish release notes.",
  };
}

export async function listPublicReleaseEvidence(): Promise<PublicReleaseEvidence[]> {
  const [unifiedRuns, gateRuns, approvalDirectory, releases] = await Promise.all([
    matchingWorkflowRuns(UNIFIED_REPLAY_WORKFLOW),
    matchingWorkflowRuns(MATERIAL_GATE_WORKFLOW),
    githubJson<GitHubContent[]>(`${REPOSITORY_PATH}/contents/release-approvals?ref=main`, {}, true),
    githubJson<GitHubRelease[]>(`${REPOSITORY_PATH}/releases?per_page=25`),
  ]);
  const workflowEvidenceItems = [
    ...unifiedRuns.filter((run) => run.name === "Full Platform End-to-End Replay").map((run) => workflowEvidence(run, "unified_replay")),
    ...gateRuns.filter((run) => run.name === "Material Release Gate").map((run) => workflowEvidence(run, "material_gate")),
  ];
  const approvalItems: Array<PublicReleaseEvidence | null> = await Promise.all((approvalDirectory ?? []).filter((entry) => entry.name.endsWith(".json")).map(async (entry) => {
    const tag = entry.name.slice(0, -5);
    const approval = await approvalForTag(tag);
    if (!approval) return null;
    return {
      evidenceId: `tag_approval:${tag}`,
      kind: "tag_approval" as const,
      title: `Approved material tag: ${tag}`,
      result: "verified" as const,
      sourceCommit: approval.targetSha,
      occurredAt: approval.approvedAt,
      sourceUrl: approval.sourceUrl,
      testScope: `Explicit GitHub approval record, written only after a matching successful Material Release Gate. Approved by ${approval.approvedBy}.`,
      limitation: "Approval is limited to the recorded tag and exact target commit; it does not publish release notes by itself.",
    } satisfies PublicReleaseEvidence;
  }));
  const releaseItems = (releases ?? []).map((release) => ({
    evidenceId: `published_release:${release.id}`,
    kind: "published_release" as const,
    title: `Published release: ${release.tag_name}`,
    result: "verified" as const,
    sourceCommit: release.target_commitish || null,
    occurredAt: release.published_at ?? release.created_at,
    sourceUrl: release.html_url,
    testScope: "GitHub release note publication recorded after the approved-tag workflow completed.",
    limitation: "Publication records the release-note event; readers should inspect the linked approval and replay evidence for its specific validation scope.",
  } satisfies PublicReleaseEvidence));
  return [...workflowEvidenceItems, ...approvalItems.filter((item): item is PublicReleaseEvidence => item !== null), ...releaseItems].sort((left, right) => +new Date(right.occurredAt) - +new Date(left.occurredAt)).slice(0, 50);
}
