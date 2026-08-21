import { describe, expect, it } from "vitest";
import { buildNearExpiryInvitationExport } from "../../server/reviewerInvitationExpiryExport";

describe("near-expiry reviewer invitation CSV export", () => {
  const now = new Date("2026-08-19T12:00:00.000Z");

  it("exports only pending invitations inside the 72-hour window, ordered by upcoming expiry", () => {
    const result = buildNearExpiryInvitationExport([
      { invitationId: "invite-later", displayName: "Later Reviewer", role: "reviewer", requestedScope: "general", status: "pending", expiresAt: "2026-08-21T12:00:00.000Z" },
      { invitationId: "invite-first", displayName: "First, Reviewer", role: "lead_reviewer", requestedScope: "semantics", status: "pending", expiresAt: "2026-08-19T13:00:00.000Z" },
      { invitationId: "invite-outside", displayName: "Outside Reviewer", role: "reviewer", requestedScope: "implementation", status: "pending", expiresAt: "2026-08-22T13:00:00.000Z" },
      { invitationId: "invite-accepted", displayName: "Accepted Reviewer", role: "reviewer", requestedScope: "general", status: "accepted", expiresAt: "2026-08-19T14:00:00.000Z" },
      { invitationId: "invite-expired", displayName: "Expired Reviewer", role: "reviewer", requestedScope: "general", status: "pending", expiresAt: "2026-08-19T11:59:59.000Z" },
    ], 72, now);

    expect(result.rows.map((row) => row.invitationId)).toEqual(["invite-first", "invite-later"]);
    expect(result.rows[0]?.hoursRemaining).toBe(1);
    expect(result.csv).toContain('"First, Reviewer"');
    expect(result.csv).not.toContain("invite-accepted");
    expect(result.manifest).toEqual([{ invitationId: "invite-first", expiresAtUtc: "2026-08-19T13:00:00.000Z" }, { invitationId: "invite-later", expiresAtUtc: "2026-08-21T12:00:00.000Z" }]);
  });

  it("uses the selected 24-, 48-, or 72-hour boundary rather than silently defaulting every export to 72 hours", () => {
    const source = [{ invitationId: "invite-48", displayName: "Window Reviewer", role: "reviewer", requestedScope: "general", status: "pending", expiresAt: "2026-08-21T11:00:00.000Z" }];
    expect(buildNearExpiryInvitationExport(source, 24, now).rows).toHaveLength(0);
    expect(buildNearExpiryInvitationExport(source, 48, now).rows).toHaveLength(1);
    expect(buildNearExpiryInvitationExport(source, 72, now).windowHours).toBe(72);
  });
});
