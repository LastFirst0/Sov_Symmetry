import { describe, expect, it } from "vitest";
import { invitationExpiryIndicator, invitationExpiryMessage } from "./reviewerInvitationExpiry";

describe("reviewer invitation expiry indicators", () => {
  const now = new Date("2026-08-19T12:00:00.000Z");

  it("distinguishes pending, expiring, and expired invitations from their durable expiry timestamp", () => {
    expect(invitationExpiryIndicator("pending", "2026-08-25T12:00:00.000Z", now)).toBe("pending");
    expect(invitationExpiryIndicator("pending", "2026-08-21T11:00:00.000Z", now)).toBe("expiring");
    expect(invitationExpiryIndicator("pending", "2026-08-19T11:59:59.000Z", now)).toBe("expired");
  });

  it("preserves accepted and revoked lifecycle terminal states rather than treating them as pending reminders", () => {
    expect(invitationExpiryIndicator("accepted", "2026-08-19T11:00:00.000Z", now)).toBe("accepted");
    expect(invitationExpiryIndicator("revoked", "2026-08-25T12:00:00.000Z", now)).toBe("revoked");
    expect(invitationExpiryMessage("pending", "2026-08-21T11:00:00.000Z", now)).toContain("Expiring");
  });
});
