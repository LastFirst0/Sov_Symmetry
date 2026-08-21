import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ record: vi.fn().mockResolvedValue({ receiptId: "export_test", recordCount: 1, format: "csv" }), listAll: vi.fn().mockResolvedValue([{ receiptId: "export_test", accountOpenId: "account-exporter", format: "csv", recordCount: 1, resultDigest: "sha256:test", createdAt: new Date() }]) }));
vi.mock("../../server/db", () => ({
  recordArchiveExport: mocks.record, getArchiveExportReceipt: vi.fn(), listAllArchiveExportReceipts: mocks.listAll, listArchiveExportReceipts: vi.fn().mockResolvedValue([]), listPublicationRequests: vi.fn(), listPublicationReviews: vi.fn(), listResearchArtifactAudits: vi.fn(), listResearchArtifacts: vi.fn().mockResolvedValue([]), listReviewerMemberships: vi.fn(), listSavedArchiveViews: vi.fn(), publishApprovedArtifact: vi.fn(), removeArchiveView: vi.fn(), reviewerOperationsStatus: vi.fn(), saveArchiveView: vi.fn(), stageArtifactPublication: vi.fn(), decidePublicationRequest: vi.fn(), syncReviewerMemberships: vi.fn(), updateReviewerMembership: vi.fn(),
}));
import { appRouter } from "../../server/routers";

const user = { id: 1, openId: "account-exporter", name: "Exporter", email: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };

describe("export receipt contract", () => {
  it("records the exact requested filter snapshot under the authenticated account", async () => {
    const caller = appRouter.createCaller({ user, ingestionAuthorized: false, reviewerId: null });
    await caller.exports.record({ format: "csv", filters: { term: "M0", category: "experiment", status: "fail", sort: "updated_desc" } });
    expect(mocks.record).toHaveBeenCalledWith("account-exporter", "csv", { term: "M0", category: "experiment", status: "fail", sort: "updated_desc" });
  });

  it("exposes all receipt identities only through the owner-gated audit procedure", async () => {
    const caller = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await expect(caller.exports.all()).resolves.toEqual(expect.arrayContaining([expect.objectContaining({ accountOpenId: "account-exporter", resultDigest: "sha256:test" })]));
    expect(mocks.listAll).toHaveBeenCalledOnce();
  });
});
