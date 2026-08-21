import { describe, expect, it } from "vitest";
import { reviewerTokens } from "../../server/trpc";

const enabled = process.env.RUN_LIVE_DB_INGESTION === "1";
const reattestation = { artifactKey: "governance.automation.v0.1", title: "Bounded automation governance package", category: "governance", status: "verified", sourceUrl: "/manus-storage/research_dashboard_feed_89e89334.json", contentDigest: null, summary: "The automation registry validator accepted seven bounded jobs, all defined but not scheduled, and the skill quarantine register keeps all reviewed external skills unimported.", limitation: "No schedule, connector enablement, external skill import, or automated claim promotion occurred." };

async function callRpc(path: string, token: string, input: unknown) {
  const response = await fetch(`http://localhost:3000/api/trpc/${path}?batch=1`, { method: "POST", headers: { authorization: `Bearer ${token}`, "content-type": "application/json" }, body: JSON.stringify({ 0: { json: input } }) });
  const raw = await response.text();
  expect(response.status, raw).toBe(200);
  const payload = JSON.parse(raw) as [{ result?: { data?: { json?: Record<string, unknown> } } }];
  return payload[0]?.result?.data?.json ?? {};
}

async function listPendingRequest() {
  const response = await fetch("http://localhost:3000/api/trpc/publication.list?batch=1");
  expect(response.status).toBe(200);
  const payload = await response.json() as [{ result?: { data?: { json?: { requestKey: string; artifactKey: string; status: string }[] } } }];
  return payload[0]?.result?.data?.json?.find((request) => request.artifactKey === reattestation.artifactKey && request.status === "pending_review");
}

describe("live multi-owner publication workflow", () => {
  it.runIf(enabled)("stages, independently approves, and publishes a real governed reattestation through the running typed API", async () => {
    const ownerToken = process.env.SOVEREIGN_INGESTION_TOKEN;
    const reviewers = Object.entries(reviewerTokens()).slice(0, 2);
    expect(ownerToken).toBeTruthy();
    expect(reviewers).toHaveLength(2);
    const memberships = await callRpc("reviewerMemberships.syncConfigured", ownerToken!, undefined);
    expect(Array.isArray(memberships)).toBe(true);
    const pending = await listPendingRequest();
    const staged = pending ?? await callRpc("publication.stage", ownerToken!, reattestation);
    const requestKey = staged.requestKey as string;
    expect(staged).toMatchObject({ status: "pending_review" });
    const first = await callRpc("publication.decide", reviewers[0]![1], { requestKey, decision: "approve", rationale: "I verified that the cited artifact, declared metadata digest, and stated limitation are present and consistent. This decision approves the publication workflow only; it does not assert any external theory, physical interpretation, or applied outcome.", rationaleTemplateKey: "evidence_trace_complete" });
    expect(first).toMatchObject({ status: "pending_review", approvedCount: 1, requiredApprovals: 2 });
    const second = await callRpc("publication.decide", reviewers[1]![1], { requestKey, decision: "approve", rationale: "I verified that the cited artifact, declared metadata digest, and stated limitation are present and consistent. This decision approves the publication workflow only; it does not assert any external theory, physical interpretation, or applied outcome.", rationaleTemplateKey: "evidence_trace_complete" });
    expect(second).toMatchObject({ status: "approved", approvedCount: 2, requiredApprovals: 2 });
    const published = await callRpc("publication.publish", ownerToken!, { requestKey });
    expect(published).toMatchObject({ requestKey, status: "published", action: "update" });
    expect(published.revision as number).toBeGreaterThan(1);
  });
});
