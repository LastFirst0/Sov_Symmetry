import { describe, expect, it } from "vitest";
import { createPublicKey, verify } from "node:crypto";
import { appRouter } from "../../server/routers";
import { signReceiptBundlePayload } from "../../server/receiptBundles";

describe("receipt signing key configuration", () => {
  it("exposes only a valid Ed25519 public verification descriptor through the lightweight typed endpoint", async () => {
    const caller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    const descriptor = await caller.exports.signingKey();
    expect(descriptor).toMatchObject({ algorithm: "Ed25519", publicKeyJwk: { kty: "OKP", crv: "Ed25519" } });
    expect(descriptor.publicKeyJwk.x).toMatch(/^[A-Za-z0-9_-]+$/);
    expect(descriptor.keyFingerprint).toMatch(/^[a-f0-9]{64}$/);
  });

  it("signs a receipt manifest that verifies against the exported public key without exposing private material", () => {
    const bundle = signReceiptBundlePayload({ schema: "sov.archive_receipt_bundle.payload", schemaVersion: "0.1.0", receipt: { receiptId: "receipt-key-contract", accountOpenId: "account-contract", format: "json", recordCount: 1, filtersSnapshot: "{}", resultDigest: "a".repeat(64), createdAt: "2026-08-19T00:00:00.000Z" }, resultManifest: [{ artifactKey: "release.contract.v1", revision: 1, metadataDigest: "b".repeat(64) }] });
    expect(verify(null, Buffer.from(bundle.canonicalPayload), createPublicKey({ key: bundle.signing.publicKeyJwk, format: "jwk" }), Buffer.from(bundle.signature.value, "base64url"))).toBe(true);
  });
});
