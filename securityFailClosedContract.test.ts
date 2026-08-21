import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ activate: vi.fn(), approve: vi.fn(), assertKey: vi.fn(), receipt: vi.fn(), timeline: vi.fn().mockResolvedValue([{ signatureId: "sig-1", receiptId: "receipt-1" }]) }));
vi.mock("../../server/db", async (importOriginal) => ({ ...(await importOriginal<typeof import("../../server/db")>()), activateReceiptKeyRotation: mocks.activate, approveReceiptKeyRotation: mocks.approve, assertCurrentReceiptSigningKeyUsable: mocks.assertKey, getArchiveExportReceipt: mocks.receipt, listReceiptBundleTimeline: mocks.timeline }));
import { appRouter } from "../../server/routers";

const user = { id: 1, openId: "account-security", name: "Security account", email: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };

describe("security fail-closed archive contracts", () => {
  it("does not activate a rotation when the configured signer differs from the approved candidate", async () => {
    mocks.activate.mockRejectedValueOnce(new Error("ROTATION_KEY_DOES_NOT_MATCH_CONFIGURED_SIGNER"));
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await expect(owner.keyLifecycle.activate({ requestId: "rotation-mismatch" })).rejects.toThrow("ROTATION_KEY_DOES_NOT_MATCH_CONFIGURED_SIGNER");
  });

  it("refuses bundle issuance when the active signing key is expired", async () => {
    mocks.receipt.mockResolvedValueOnce({ receiptId: "receipt-expired", accountOpenId: "account-security", format: "json", recordCount: 1, filtersSnapshot: "{}", resultDigest: "a".repeat(64), resultManifest: JSON.stringify([{ artifactKey: "record", revision: 1, metadataDigest: "b".repeat(64) }]), createdAt: new Date() });
    mocks.assertKey.mockRejectedValueOnce(new Error("RECEIPT_SIGNING_KEY_EXPIRED"));
    const caller = appRouter.createCaller({ user, ingestionAuthorized: false, reviewerId: null });
    await expect(caller.exports.bundle({ receiptId: "receipt-expired" })).rejects.toThrow("RECEIPT_SIGNING_KEY_EXPIRED");
  });

  it("loads signed snapshot events only through the authenticated account scope", async () => {
    const caller = appRouter.createCaller({ user, ingestionAuthorized: false, reviewerId: null });
    await expect(caller.exports.timeline()).resolves.toEqual([{ signatureId: "sig-1", receiptId: "receipt-1" }]);
    expect(mocks.timeline).toHaveBeenCalledWith("account-security");
  });
});
