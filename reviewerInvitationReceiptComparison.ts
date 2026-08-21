export type InvitationExportManifestEntry = { invitationId: string; expiresAtUtc: string };
export type InvitationExportReceiptComparable = {
  receiptId: string;
  reminderWindowHours: number;
  recordCount: number;
  resultDigest: string;
  resultManifest: string;
};

function parseManifest(receipt: InvitationExportReceiptComparable): InvitationExportManifestEntry[] {
  let parsed: unknown;
  try { parsed = JSON.parse(receipt.resultManifest); } catch { throw new Error("REVIEWER_INVITATION_EXPORT_MANIFEST_INVALID"); }
  if (!Array.isArray(parsed) || !parsed.every((item) => typeof item === "object" && item !== null && typeof (item as Record<string, unknown>).invitationId === "string" && typeof (item as Record<string, unknown>).expiresAtUtc === "string" && !Number.isNaN(Date.parse((item as Record<string, string>).expiresAtUtc)))) throw new Error("REVIEWER_INVITATION_EXPORT_MANIFEST_INVALID");
  const manifest = parsed as InvitationExportManifestEntry[];
  if (new Set(manifest.map((item) => item.invitationId)).size !== manifest.length) throw new Error("REVIEWER_INVITATION_EXPORT_MANIFEST_DUPLICATE_ENTRY");
  return manifest;
}

function sortedManifest(manifest: InvitationExportManifestEntry[]) {
  return [...manifest].sort((left, right) => left.invitationId.localeCompare(right.invitationId));
}

export function invitationExportReceiptDetail(receipt: InvitationExportReceiptComparable) {
  return { receiptId: receipt.receiptId, reminderWindowHours: receipt.reminderWindowHours, recordCount: receipt.recordCount, resultDigest: receipt.resultDigest, manifest: parseManifest(receipt) };
}

/** Compares retained declaration snapshots only; it does not infer invitation status, reviewer identity, or a change cause. */
export function compareInvitationExportReceipts(left: InvitationExportReceiptComparable, right: InvitationExportReceiptComparable) {
  const leftManifest = sortedManifest(parseManifest(left)); const rightManifest = sortedManifest(parseManifest(right));
  const leftById = new Map(leftManifest.map((entry) => [entry.invitationId, entry]));
  const rightById = new Map(rightManifest.map((entry) => [entry.invitationId, entry]));
  const onlyInLeft = leftManifest.filter((entry) => !rightById.has(entry.invitationId));
  const onlyInRight = rightManifest.filter((entry) => !leftById.has(entry.invitationId));
  const shared = leftManifest.filter((entry) => rightById.has(entry.invitationId)).map((entry) => ({ invitationId: entry.invitationId, leftExpiresAtUtc: entry.expiresAtUtc, rightExpiresAtUtc: rightById.get(entry.invitationId)!.expiresAtUtc, expiryChanged: entry.expiresAtUtc !== rightById.get(entry.invitationId)!.expiresAtUtc }));
  return {
    left: { receiptId: left.receiptId, reminderWindowHours: left.reminderWindowHours, recordCount: left.recordCount, resultDigest: left.resultDigest },
    right: { receiptId: right.receiptId, reminderWindowHours: right.reminderWindowHours, recordCount: right.recordCount, resultDigest: right.resultDigest },
    digestMatches: left.resultDigest === right.resultDigest,
    onlyInLeft, onlyInRight, shared,
  };
}
