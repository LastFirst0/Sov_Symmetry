import { createHash, generateKeyPairSync, sign, webcrypto } from "node:crypto";
import { beforeAll, describe, expect, it } from "vitest";
import { compareReceiptBundles, verifyReceiptBundle } from "./lib/receiptBundles";

beforeAll(() => { Object.defineProperty(globalThis, "crypto", { value: webcrypto, configurable: true }); });

describe("independent signed receipt verification", () => {
  it("accepts a valid Ed25519 bundle only when its canonical payload and manifest digest agree", async () => {
    const { privateKey, publicKey } = generateKeyPairSync("ed25519");
    const resultManifest = [{ artifactKey: "experiment.example.v1", revision: 1, metadataDigest: "abc" }];
    const payload = { schema: "sov.archive_receipt_bundle.payload" as const, schemaVersion: "0.1.0" as const, receipt: { receiptId: "receipt-1", resultDigest: createHash("sha256").update(JSON.stringify(resultManifest)).digest("hex") }, resultManifest };
    const canonicalPayload = JSON.stringify(payload);
    const bundle = { schema: "sov.archive_receipt_bundle" as const, schemaVersion: "0.1.0" as const, signing: { algorithm: "Ed25519" as const, keyFingerprint: "test", publicKeyJwk: publicKey.export({ format: "jwk" }) as JsonWebKey }, canonicalPayload, payload, signature: { encoding: "base64url" as const, value: sign(null, Buffer.from(canonicalPayload), privateKey).toString("base64url") } };
    await expect(verifyReceiptBundle(bundle)).resolves.toMatchObject({ valid: true });
    await expect(verifyReceiptBundle({ ...bundle, payload: { ...payload, resultManifest: [] } })).resolves.toMatchObject({ valid: false });
  });

  it("reports only declared manifest differences between two snapshots", () => {
    const left = { schema: "sov.archive_receipt_bundle", schemaVersion: "0.1.0", signing: {}, canonicalPayload: "", signature: {}, payload: { receipt: { receiptId: "left" }, resultManifest: [{ artifactKey: "same", revision: 1, metadataDigest: "a" }, { artifactKey: "changed", revision: 1, metadataDigest: "b" }, { artifactKey: "removed", revision: 1, metadataDigest: "c" }] } } as unknown as Parameters<typeof compareReceiptBundles>[0];
    const right = { ...left, payload: { receipt: { receiptId: "right" }, resultManifest: [{ artifactKey: "same", revision: 1, metadataDigest: "a" }, { artifactKey: "changed", revision: 2, metadataDigest: "d" }, { artifactKey: "added", revision: 1, metadataDigest: "e" }] } } as Parameters<typeof compareReceiptBundles>[1];
    expect(compareReceiptBundles(left, right)).toMatchObject({ added: ["added"], removed: ["removed"], changed: ["changed"], identical: false });
  });
});
