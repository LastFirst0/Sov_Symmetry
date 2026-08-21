import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ lookup: vi.fn(), list: vi.fn().mockResolvedValue([]), record: vi.fn() }));
vi.mock("../../server/db", async (importOriginal) => ({ ...(await importOriginal<typeof import("../../server/db")>()), getReceiptSigningKey: mocks.lookup, listReceiptSigningKeys: mocks.list, recordReceiptSigningKey: mocks.record }));
import { appRouter } from "../../server/routers";
import { receiptSigningDescriptor } from "../../server/receiptBundles";

describe("historical receipt signing-key lookup", () => {
  it("returns the live public descriptor by fingerprint without exposing private material", async () => {
    const descriptor = receiptSigningDescriptor();
    const caller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(caller.signingKeyHistory.lookup({ keyFingerprint: descriptor.keyFingerprint })).resolves.toMatchObject({ source: "current", keyFingerprint: descriptor.keyFingerprint, publicKeyJwk: { kty: "OKP", crv: "Ed25519" } });
    expect(mocks.lookup).not.toHaveBeenCalled();
  });

  it("resolves a retained historical public key record by fingerprint", async () => {
    const fingerprint = "f".repeat(64); const now = new Date("2026-08-19T00:00:00.000Z");
    mocks.lookup.mockResolvedValueOnce({ keyFingerprint: fingerprint, algorithm: "Ed25519", publicKeyJwk: JSON.stringify({ kty: "OKP", crv: "Ed25519", x: "historical" }), status: "retired", firstSeenAt: now, lastSeenAt: now, retiredAt: now });
    const caller = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(caller.signingKeyHistory.lookup({ keyFingerprint: fingerprint })).resolves.toMatchObject({ source: "historical", status: "retired", publicKeyJwk: { x: "historical" } });
  });
});
