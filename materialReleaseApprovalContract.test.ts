import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  listPublicReleaseEvidence: vi.fn().mockResolvedValue([{ evidenceId: "unified_replay:1", kind: "unified_replay", result: "verified" }]),
  listOwnerMaterialReleaseTags: vi.fn().mockResolvedValue([]),
  previewMaterialReleaseTag: vi.fn().mockResolvedValue({ tag: "material-release-v0.1.0", eligibleForApproval: true }),
  dispatchMaterialReleaseApproval: vi.fn().mockResolvedValue({ tag: "material-release-v0.1.0", status: "approval_dispatch_recorded" }),
}));

vi.mock("../../server/materialReleaseGovernance", () => mocks);
import { appRouter } from "../../server/routers";

describe("material release approval API boundary", () => {
  it("keeps validation history public and gates tag administration behind owner authorization", async () => {
    const publicCaller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await publicCaller.materialReleaseEvidence.list();
    expect(mocks.listPublicReleaseEvidence).toHaveBeenCalledOnce();

    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await owner.materialReleaseApprovals.list();
    await owner.materialReleaseApprovals.preview({ tag: "material-release-v0.1.0" });
    await owner.materialReleaseApprovals.approve({ tag: "material-release-v0.1.0" });
    expect(mocks.previewMaterialReleaseTag).toHaveBeenCalledWith("material-release-v0.1.0");
    expect(mocks.dispatchMaterialReleaseApproval).toHaveBeenCalledWith("material-release-v0.1.0");
  });

  it("fails closed when an unauthorised caller attempts owner release-tag operations", async () => {
    const unauthorised = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(unauthorised.materialReleaseApprovals.list()).rejects.toThrow("Owner authorization");
    await expect(unauthorised.materialReleaseApprovals.preview({ tag: "material-release-v0.1.0" })).rejects.toThrow("Owner authorization");
    await expect(unauthorised.materialReleaseApprovals.approve({ tag: "material-release-v0.1.0" })).rejects.toThrow("Owner authorization");
  });
});
