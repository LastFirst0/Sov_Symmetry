import { createPublicKey, verify } from "node:crypto";
import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  receipt: vi.fn().mockResolvedValue({ receiptId: "export_bundle_test", accountOpenId: "account-bundle", format: "json", recordCount: 1, filtersSnapshot: "{\"term\":\"M0\"}", resultDigest: "b".repeat(64), resultManifest: JSON.stringify([{ artifactKey: "m0.dna_geometry.v0", revision: 1, metadataDigest: "c".repeat(64) }]), createdAt: new Date("2026-08-19T00:00:00.000Z") }),
  assertCurrentReceiptSigningKeyUsable: vi.fn().mockResolvedValue(undefined),
  recordReceiptSigningKey: vi.fn().mockResolvedValue(undefined),
  recordReceiptBundleSignature: vi.fn().mockResolvedValue(undefined),
  storagePutSignedReceiptBundle: vi.fn().mockResolvedValue({ key: `signed-receipts/export_bundle_test/${"a".repeat(64)}/${"b".repeat(64)}.json`, url: "/manus-storage/signed-receipts/export_bundle_test/test.json" }),
}));
vi.mock("../../server/db", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../../server/db")>()),
  getArchiveExportReceipt: mocks.receipt,
  assertCurrentReceiptSigningKeyUsable: mocks.assertCurrentReceiptSigningKeyUsable,
  recordReceiptSigningKey: mocks.recordReceiptSigningKey,
  recordReceiptBundleSignature: mocks.recordReceiptBundleSignature,
}));
vi.mock("../../server/storage", () => ({ storagePutSignedReceiptBundle: mocks.storagePutSignedReceiptBundle }));
import { appRouter } from "../../server/routers";

const user = { id: 1, openId: "account-bundle", name: "Bundle exporter", email: null, loginMethod: "manus", role: "user" as const, createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() };

describe("signed receipt bundle contract", () => {
  it("allows only the receipt owner to receive a signed bundle over its immutable result manifest", async () => {
    const bundle = await appRouter.createCaller({ user, ingestionAuthorized: false, reviewerId: null }).exports.bundle({ receiptId: "export_bundle_test" });
    expect(mocks.receipt).toHaveBeenCalledWith("account-bundle", "export_bundle_test");
    expect(bundle.payload.resultManifest).toEqual([{ artifactKey: "m0.dna_geometry.v0", revision: 1, metadataDigest: "c".repeat(64) }]);
    expect(verify(null, Buffer.from(bundle.canonicalPayload), createPublicKey({ key: bundle.signing.publicKeyJwk, format: "jwk" }), Buffer.from(bundle.signature.value, "base64url"))).toBe(true);
    expect(mocks.assertCurrentReceiptSigningKeyUsable).toHaveBeenCalledWith(bundle.signing);
    expect(mocks.recordReceiptSigningKey).toHaveBeenCalledWith(bundle.signing);
    expect(mocks.storagePutSignedReceiptBundle).toHaveBeenCalledWith(expect.stringContaining(`signed-receipts/export_bundle_test/${bundle.signing.keyFingerprint}/`), expect.any(Buffer));
    expect(mocks.recordReceiptBundleSignature).toHaveBeenCalledWith(expect.objectContaining({ receiptId: "export_bundle_test", keyFingerprint: bundle.signing.keyFingerprint, bundleStorageKey: expect.stringContaining("signed-receipts/export_bundle_test/"), bundleDigest: expect.stringMatching(/^[a-f0-9]{64}$/) }));
  });
});
