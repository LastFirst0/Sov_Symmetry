import { describe, expect, it, vi } from "vitest";
import { storagePut, storagePutSignedReceiptBundle } from "../../server/storage";

describe("managed storage wrapper", () => {
  it("fails closed when the managed presign call fails", async () => { const fetcher = vi.fn().mockResolvedValue({ ok: false }); await expect(storagePut("governed-corpus/genesis_oshb/test.json", Buffer.from("{}"), "application/json", fetcher)).rejects.toThrow("STORAGE_PRESIGN_FAILED"); });
  it("fails closed when the provider rejects the presigned PUT", async () => { const fetcher = vi.fn().mockResolvedValueOnce({ ok: true, json: async () => ({ url: "https://object.example/put" }) }).mockResolvedValueOnce({ ok: false }); await expect(storagePut("governed-corpus/genesis_oshb/test.json", Buffer.from("{}"), "application/json", fetcher)).rejects.toThrow("STORAGE_PUT_FAILED"); });
  it("rejects an invalid storage key before contacting the provider", async () => { const fetcher = vi.fn(); await expect(storagePut("outside/key.json", Buffer.from("{}"), "application/json", fetcher)).rejects.toThrow("STORAGE_KEY_INVALID"); expect(fetcher).not.toHaveBeenCalled(); });
  it("accepts only a receipt ID, key fingerprint, and envelope digest in the signed-bundle namespace", async () => { const fetcher = vi.fn().mockResolvedValueOnce({ ok: true, json: async () => ({ url: "https://object.example/put" }) }).mockResolvedValueOnce({ ok: true }); const key = `signed-receipts/export_bundle_test/${"a".repeat(64)}/${"b".repeat(64)}.json`; await expect(storagePutSignedReceiptBundle(key, Buffer.from("{}"), fetcher)).resolves.toMatchObject({ key }); await expect(storagePutSignedReceiptBundle("signed-receipts/not-a-valid-key.json", Buffer.from("{}"), fetcher)).rejects.toThrow("SIGNED_BUNDLE_STORAGE_KEY_INVALID"); });
});
