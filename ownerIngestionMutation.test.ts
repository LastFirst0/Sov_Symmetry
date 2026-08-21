import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ stageArtifactPublication: vi.fn().mockResolvedValue({ requestKey: "owner.audit.v1:r1:unique", proposedRevision: 1, status: "pending_review", metadataDigest: "digest" }) }));
vi.mock("../../server/db", () => ({
  stageArtifactPublication: mocks.stageArtifactPublication,
  decidePublicationRequest: vi.fn(),
  publishApprovedArtifact: vi.fn(),
  listPublicationRequests: vi.fn(),
  listPublicationReviews: vi.fn(),
  listResearchArtifactAudits: vi.fn(),
  listResearchArtifacts: vi.fn(),
  getArchiveExportReceipt: vi.fn(),
  reviewerOperationsStatus: vi.fn(),
}));

import { appRouter } from "../../server/routers";
import { createContext } from "../../server/trpc";

const input = { artifactKey: "owner.audit.v1", title: "Owner audit ingestion", category: "governance" as const, status: "unverifiable" as const, sourceUrl: "/manus-storage/audit.json", contentDigest: null, summary: "A validated owner-only staged-publication contract test.", limitation: "This unit test does not write a database record." };

describe("owner publication staging mutation", () => {
  it("accepts the configured owner token and stages, rather than directly publishes, a validated record", async () => {
    const context = await createContext({ req: { headers: { authorization: `Bearer ${process.env.SOVEREIGN_INGESTION_TOKEN}` } } as never, res: {} as never });
    const result = await appRouter.createCaller(context).publication.stage(input);
    expect(result).toMatchObject({ requestKey: "owner.audit.v1:r1:unique", status: "pending_review" });
    expect(mocks.stageArtifactPublication).toHaveBeenCalledWith(input);
  });
});
