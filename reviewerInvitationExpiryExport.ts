export const REVIEWER_INVITATION_EXPIRY_WINDOWS = [24, 48, 72] as const;
export const REVIEWER_INVITATION_EXPIRY_WINDOW_HOURS = 72;
export type ReviewerInvitationExpiryWindowHours = typeof REVIEWER_INVITATION_EXPIRY_WINDOWS[number];

export function isReviewerInvitationExpiryWindowHours(value: number): value is ReviewerInvitationExpiryWindowHours {
  return REVIEWER_INVITATION_EXPIRY_WINDOWS.includes(value as ReviewerInvitationExpiryWindowHours);
}

export type ReviewerInvitationExpiryExportSource = {
  invitationId: string;
  displayName: string;
  role: string;
  requestedScope: string;
  status: string;
  expiresAt: Date | string;
};

export type ReviewerInvitationExpiryExportRow = {
  invitationId: string;
  displayName: string;
  role: string;
  requestedScope: string;
  expiresAtUtc: string;
  hoursRemaining: number;
};

function csvCell(value: string | number) {
  const text = String(value);
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

/**
 * Produces an intentionally minimal owner export. It excludes invitation notes,
 * reviewer-token material, acceptance/revocation timestamps, and reviewer IDs.
 */
export function buildNearExpiryInvitationExport(records: ReviewerInvitationExpiryExportSource[], windowHours: ReviewerInvitationExpiryWindowHours = REVIEWER_INVITATION_EXPIRY_WINDOW_HOURS, now = new Date()) {
  if (!isReviewerInvitationExpiryWindowHours(windowHours)) throw new Error("REVIEWER_INVITATION_EXPIRY_WINDOW_INVALID");
  const nowMs = now.getTime();
  const windowMs = windowHours * 60 * 60 * 1000;
  const rows: ReviewerInvitationExpiryExportRow[] = records
    .map((entry) => ({ entry, expiresAt: new Date(entry.expiresAt) }))
    .filter(({ entry, expiresAt }) => entry.status === "pending" && Number.isFinite(expiresAt.getTime()) && expiresAt.getTime() > nowMs && expiresAt.getTime() <= nowMs + windowMs)
    .sort((left, right) => left.expiresAt.getTime() - right.expiresAt.getTime())
    .map(({ entry, expiresAt }) => ({
      invitationId: entry.invitationId,
      displayName: entry.displayName,
      role: entry.role,
      requestedScope: entry.requestedScope,
      expiresAtUtc: expiresAt.toISOString(),
      hoursRemaining: Math.ceil((expiresAt.getTime() - nowMs) / (60 * 60 * 1000)),
    }));
  const header = ["invitation_id", "display_name", "role", "requested_scope", "expires_at_utc", "hours_remaining"];
  const csv = [header, ...rows.map((row) => [row.invitationId, row.displayName, row.role, row.requestedScope, row.expiresAtUtc, row.hoursRemaining])]
    .map((line) => line.map(csvCell).join(","))
    .join("\n");
  const manifest = rows.map(({ invitationId, expiresAtUtc }) => ({ invitationId, expiresAtUtc }));
  return { rows, csv: `${csv}\n`, manifest, windowHours };
}
