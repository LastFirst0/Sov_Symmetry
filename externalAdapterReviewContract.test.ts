import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  externalAdapterCandidateStatus: vi.fn().mockResolvedValue({
    candidateId: "external.candidate.nondecreasing-sequence",
    candidateVersion: "0.1.0",
    sourceCommit: "d4b73ae5e6bc7f8d6f0b6f6c6c054a900fead5a0",
    packageUrl: "https://example.test/package",
    admissionReportUrl: "https://example.test/report",
    firstRunUrl: "https://example.test/first-run",
    status: "quarantine",
    reason: "Both required reviewer scopes must be assigned to distinct active reviewers.",
    independentlyReviewed: false,
    admissionDecision: "quarantine",
    activationAllowed: false,
    assignments: [{ scope: "semantics", assignment: null, reviewer: null, isAssigned: false, isActiveReviewer: false }],
  }),
  listExternalAdapterReviewAssignments: vi.fn().mockResolvedValue([]),
  listExternalAdapterReviewEvents: vi.fn().mockResolvedValue([]),
  assignExternalAdapterReviewer: vi.fn().mockResolvedValue({ assignmentId: "adapter_review_alpha", scope: "semantics", reviewerId: "reviewer-alpha", status: "pending" }),
  decideExternalAdapterReview: vi.fn().mockResolvedValue({ assignmentId: "adapter_review_alpha", scope: "semantics", reviewerId: "reviewer-alpha", status: "approved" }),
}));

vi.mock("../../server/db", async (importOriginal) => ({ ...(await importOriginal<typeof import("../../server/db")>()), ...mocks }));
import { appRouter } from "../../server/routers";

describe("external adapter review contract", () => {
  it("exposes a public quarantine state without assignment identifiers or reviewer details", async () => {
    const caller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    const status = await caller.externalAdapterReview.status();
    expect(status).toMatchObject({ status: "quarantine", activationAllowed: false, admissionDecision: "quarantine" });
    expect(status.assignments[0]).toEqual({ scope: "semantics", state: "unassigned", isAssigned: false, reviewerAvailable: false });
    expect(JSON.stringify(status)).not.toContain("assignmentId");
    expect(mocks.externalAdapterCandidateStatus).toHaveBeenCalledOnce();
  });

  it("requires owner authority for scope assignments and binds the actor label", async () => {
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await owner.externalAdapterReview.assign({ scope: "semantics", reviewerId: "reviewer-alpha" });
    expect(mocks.assignExternalAdapterReviewer).toHaveBeenCalledWith({ scope: "semantics", reviewerId: "reviewer-alpha", assignedBy: "owner-token" });
    const publicCaller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(publicCaller.externalAdapterReview.assign({ scope: "implementation", reviewerId: "reviewer-beta" })).rejects.toThrow("Owner authorization");
  });

  it("requires a reviewer identity and records only that reviewer as the decision actor", async () => {
    const reviewer = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: "reviewer-alpha" });
    await reviewer.externalAdapterReview.decide({ assignmentId: "adapter_review_alpha", decision: "approved", rationale: "The finite input and output conditions are fully restatable from the package evidence.", independenceAttestation: "I am not the candidate author or controlling organization and reviewed only the assigned semantics scope.", evidenceUrl: "https://example.test/semantics-review" });
    expect(mocks.decideExternalAdapterReview).toHaveBeenCalledWith(expect.objectContaining({ assignmentId: "adapter_review_alpha", reviewerId: "reviewer-alpha", decision: "approved" }));
    const publicCaller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(publicCaller.externalAdapterReview.decide({ assignmentId: "adapter_review_alpha", decision: "approved", rationale: "The finite input and output conditions are fully restatable from the package evidence.", independenceAttestation: "I am not the candidate author or controlling organization and reviewed only the assigned semantics scope.", evidenceUrl: "https://example.test/semantics-review" })).rejects.toThrow("independent reviewer token");
  });
});
