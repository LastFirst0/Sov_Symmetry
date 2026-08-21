import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  listReviewerInvitations: vi.fn().mockResolvedValue([]),
  createReviewerInvitation: vi.fn().mockResolvedValue({ invitationId: "reviewer_invite_alpha", status: "pending" }),
  revokeReviewerInvitation: vi.fn().mockResolvedValue({ invitationId: "reviewer_invite_alpha", status: "revoked" }),
  acceptReviewerInvitation: vi.fn().mockResolvedValue({ invitationId: "reviewer_invite_alpha", status: "accepted" }),
}));

vi.mock("../../server/db", async (importOriginal) => ({ ...(await importOriginal<typeof import("../../server/db")>()), ...mocks }));
import { appRouter } from "../../server/routers";

describe("reviewer invitation contract", () => {
  const invitationInput = { proposedReviewerId: "reviewer-alpha", displayName: "Reviewer Alpha", role: "reviewer" as const, requestedScope: "semantics" as const, invitationNote: "Please review the declared finite predicate semantics independently and retain your evidence link.", expiresInDays: 14 };

  it("requires owner authority to list and create onboarding records without creating a reviewer token", async () => {
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await owner.reviewerInvitations.list();
    await owner.reviewerInvitations.create(invitationInput);
    expect(mocks.createReviewerInvitation).toHaveBeenCalledWith({ ...invitationInput, createdBy: "owner-token" });
    const unauthenticated = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(unauthenticated.reviewerInvitations.list()).rejects.toThrow("Owner authorization");
    await expect(unauthenticated.reviewerInvitations.create(invitationInput)).rejects.toThrow("Owner authorization");
  });

  it("binds acceptance to the reviewer-token identity and gates revocation to the owner", async () => {
    const reviewer = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: "reviewer-alpha" });
    await reviewer.reviewerInvitations.accept({ invitationId: "reviewer_invite_alpha" });
    expect(mocks.acceptReviewerInvitation).toHaveBeenCalledWith("reviewer_invite_alpha", "reviewer-alpha");
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await owner.reviewerInvitations.revoke({ invitationId: "reviewer_invite_alpha" });
    expect(mocks.revokeReviewerInvitation).toHaveBeenCalledWith("reviewer_invite_alpha");
    const unauthenticated = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(unauthenticated.reviewerInvitations.accept({ invitationId: "reviewer_invite_alpha" })).rejects.toThrow("independent reviewer token");
  });
});
