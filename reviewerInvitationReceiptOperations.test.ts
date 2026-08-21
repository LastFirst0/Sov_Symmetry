import { describe, expect, it } from "vitest";
import { invitationReceiptComparisonCsv, invitationReceiptComparisonReport, recomputeInvitationReceiptManifestDigest } from "./reviewerInvitationReceiptOperations";

describe("reviewer invitation receipt browser operations", () => {
  const manifest = [{ invitationId: "invite_alpha", expiresAtUtc: "2026-08-20T10:00:00.000Z" }];
  const comparison = {
    left: { receiptId: "receipt_left", reminderWindowHours: 24, recordCount: 1, resultDigest: "a".repeat(64) },
    right: { receiptId: "receipt_right", reminderWindowHours: 72, recordCount: 2, resultDigest: "b".repeat(64) },
    digestMatches: false,
    onlyInLeft: manifest,
    onlyInRight: [{ invitationId: "invite_beta", expiresAtUtc: "2026-08-20T11:00:00.000Z" }],
    shared: [{ invitationId: "invite_gamma", leftExpiresAtUtc: "2026-08-20T12:00:00.000Z", rightExpiresAtUtc: "2026-08-20T13:00:00.000Z", expiryChanged: true }],
  };

  it("recomputes the exact SHA-256 digest of the retained manifest bytes locally", async () => {
    await expect(recomputeInvitationReceiptManifestDigest(manifest)).resolves.toBe("6eb7c281d8ce1081888be3f066cc27931bcfacb5f4651f34e61602b89102cf28");
  });

  it("serializes a read-only comparison report with a clear interpretation boundary", () => {
    const report = invitationReceiptComparisonReport(comparison);
    expect(report.boundary).toContain("does not infer current invitation status");
    expect(report.left.receiptId).toBe("receipt_left");
    const csv = invitationReceiptComparisonCsv(comparison);
    expect(csv).toContain("only_in_left,invite_alpha");
    expect(csv).toContain("shared,invite_gamma");
    expect(csv).not.toContain("reviewer token");
  });
});
