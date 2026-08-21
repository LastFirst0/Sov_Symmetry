import { describe, expect, it } from "vitest";
import { compareInvitationExportReceipts, invitationExportReceiptDetail } from "../../server/reviewerInvitationReceiptComparison";

const receipt = (receiptId: string, reminderWindowHours: number, resultDigest: string, entries: Array<{ invitationId: string; expiresAtUtc: string }>) => ({ receiptId, reminderWindowHours, recordCount: entries.length, resultDigest, resultManifest: JSON.stringify(entries) });

describe("reviewer invitation export receipt inspection and comparison", () => {
  it("returns only recorded safe manifest fields and compares entry deltas without inferring cause or status", () => {
    const left = receipt("invitation_export_left", 24, "a".repeat(64), [{ invitationId: "invite_alpha", expiresAtUtc: "2026-08-20T10:00:00.000Z" }, { invitationId: "invite_beta", expiresAtUtc: "2026-08-20T11:00:00.000Z" }]);
    const right = receipt("invitation_export_right", 72, "b".repeat(64), [{ invitationId: "invite_beta", expiresAtUtc: "2026-08-20T12:00:00.000Z" }, { invitationId: "invite_gamma", expiresAtUtc: "2026-08-20T13:00:00.000Z" }]);
    expect(invitationExportReceiptDetail(left)).toEqual({ receiptId: "invitation_export_left", reminderWindowHours: 24, recordCount: 2, resultDigest: "a".repeat(64), manifest: [{ invitationId: "invite_alpha", expiresAtUtc: "2026-08-20T10:00:00.000Z" }, { invitationId: "invite_beta", expiresAtUtc: "2026-08-20T11:00:00.000Z" }] });
    const comparison = compareInvitationExportReceipts(left, right);
    expect(comparison.digestMatches).toBe(false);
    expect(comparison.onlyInLeft).toEqual([{ invitationId: "invite_alpha", expiresAtUtc: "2026-08-20T10:00:00.000Z" }]);
    expect(comparison.onlyInRight).toEqual([{ invitationId: "invite_gamma", expiresAtUtc: "2026-08-20T13:00:00.000Z" }]);
    expect(comparison.shared).toEqual([{ invitationId: "invite_beta", leftExpiresAtUtc: "2026-08-20T11:00:00.000Z", rightExpiresAtUtc: "2026-08-20T12:00:00.000Z", expiryChanged: true }]);
  });

  it("fails closed on malformed or duplicate manifest entries", () => {
    expect(() => invitationExportReceiptDetail({ ...receipt("invitation_export_bad", 24, "a".repeat(64), []), resultManifest: "not-json" })).toThrow("REVIEWER_INVITATION_EXPORT_MANIFEST_INVALID");
    expect(() => invitationExportReceiptDetail(receipt("invitation_export_duplicate", 24, "a".repeat(64), [{ invitationId: "invite_alpha", expiresAtUtc: "2026-08-20T10:00:00.000Z" }, { invitationId: "invite_alpha", expiresAtUtc: "2026-08-20T11:00:00.000Z" }]))).toThrow("REVIEWER_INVITATION_EXPORT_MANIFEST_DUPLICATE_ENTRY");
  });
});
