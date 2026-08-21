import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ request: vi.fn().mockResolvedValue({ requestId: "rotation_contract", status: "pending" }), list: vi.fn().mockResolvedValue([]), approve: vi.fn(), activate: vi.fn(), cancel: vi.fn().mockResolvedValue({ requestId: "rotation_contract", status: "cancelled" }), refresh: vi.fn(), notifications: vi.fn().mockResolvedValue([]), update: vi.fn() }));
vi.mock("../../server/db", async (importOriginal) => ({ ...(await importOriginal<typeof import("../../server/db")>()), requestReceiptKeyRotation: mocks.request, listReceiptKeyRotationRequests: mocks.list, approveReceiptKeyRotation: mocks.approve, activateReceiptKeyRotation: mocks.activate, cancelReceiptKeyRotation: mocks.cancel, refreshOwnerNotifications: mocks.refresh, listOwnerNotifications: mocks.notifications, updateOwnerNotification: mocks.update }));
import { appRouter } from "../../server/routers";

describe("key lifecycle and owner notification boundaries", () => {
  it("requires the owner boundary for lifecycle proposals and forwards only public key material", async () => {
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    const expiry = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000);
    await expect(owner.keyLifecycle.request({ publicKeyJwk: { kty: "OKP", crv: "Ed25519", x: "candidate-public-x" }, expiresAt: expiry, rationale: "Replace the current key before its approved operational expiry." })).resolves.toMatchObject({ requestId: "rotation_contract" });
    expect(mocks.request).toHaveBeenCalledWith(expect.objectContaining({ algorithm: "Ed25519", requestedExpiryAt: expiry, publicKeyJwk: expect.objectContaining({ x: "candidate-public-x" }) }));
  });

  it("rejects notification-center reads without the owner boundary", async () => {
    const anonymous = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(anonymous.ownerNotifications.list()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("allows the owner to cancel an unactivated successor key request", async () => {
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await expect(owner.keyLifecycle.cancel({ requestId: "rotation_contract" })).resolves.toMatchObject({ status: "cancelled" });
    expect(mocks.cancel).toHaveBeenCalledWith("rotation_contract");
  });

  it("blocks non-owner approval and preserves a fail-closed expired request error for the owner", async () => {
    const anonymous = appRouter.createCaller({ user: null, ingestionAuthorized: false, reviewerId: null });
    await expect(anonymous.keyLifecycle.approve({ requestId: "rotation-expired" })).rejects.toMatchObject({ code: "FORBIDDEN" });
    mocks.approve.mockRejectedValueOnce(new Error("ROTATION_REQUEST_EXPIRED"));
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await expect(owner.keyLifecycle.approve({ requestId: "rotation-expired" })).rejects.toThrow("ROTATION_REQUEST_EXPIRED");
    expect(mocks.approve).toHaveBeenCalledWith("rotation-expired");
  });

  it("fails closed when an owner attempts to approve a non-pending rotation request", async () => {
    mocks.approve.mockRejectedValueOnce(new Error("ROTATION_REQUEST_NOT_APPROVABLE"));
    const owner = appRouter.createCaller({ user: null, ingestionAuthorized: true, reviewerId: null });
    await expect(owner.keyLifecycle.approve({ requestId: "rotation-already-approved" })).rejects.toThrow("ROTATION_REQUEST_NOT_APPROVABLE");
    expect(mocks.approve).toHaveBeenCalledWith("rotation-already-approved");
  });
});
