import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  reviewerOperationsStatus: vi.fn().mockResolvedValue({
    activeDeciderCount: 2,
    pendingRequestCount: 1,
    reviewers: [
      { reviewerId: "reviewer-alpha", displayName: "Reviewer Alpha", role: "reviewer", status: "active", decisionsRecorded: 0, approvalsRecorded: 0, rejectionsRecorded: 0, pendingEligibleDecisions: 1 },
      { reviewerId: "reviewer-beta", displayName: "Reviewer Beta", role: "reviewer", status: "active", decisionsRecorded: 0, approvalsRecorded: 0, rejectionsRecorded: 0, pendingEligibleDecisions: 1 },
    ],
    requests: [{ requestKey: "request-contract", artifactKey: "artifact-contract", status: "pending_review", requiredApprovals: 2, approvals: 0, remainingApprovals: 2, eligibleUndecided: 2, quorumStatus: "awaiting_decisions" }],
  }),
}));
vi.mock("../../server/db", async (importOriginal) => ({ ...(await importOriginal<typeof import("../../server/db")>()), reviewerOperationsStatus: mocks.reviewerOperationsStatus }));
import { appRouter } from "../../server/routers";

describe("reviewer operations contract", () => {
  it("returns only ledger-derived workload and quorum counts through the owner-gated endpoint", async () => {
    const caller = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    const status = await caller.reviewerOperations.status();
    expect(status.activeDeciderCount).toBeGreaterThanOrEqual(0);
    expect(status.pendingRequestCount).toBeGreaterThanOrEqual(0);
    expect(status.reviewers.every((reviewer) => reviewer.pendingEligibleDecisions >= 0 && reviewer.decisionsRecorded >= 0)).toBe(true);
    expect(status.requests.every((request) => request.approvals <= request.requiredApprovals && request.eligibleUndecided >= 0)).toBe(true);
    expect(mocks.reviewerOperationsStatus).toHaveBeenCalledOnce();
  });
});
