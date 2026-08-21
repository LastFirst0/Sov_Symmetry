import { ENV } from "./_core/env";

export type StoredObject = { key: string; url: string };

/** Server-only managed object storage wrapper. It never exposes Forge credentials to React. */
async function putManagedObject(key: string, bytes: Uint8Array, contentType: string, fetchImpl: typeof fetch = fetch): Promise<StoredObject> {
  if (!ENV.forgeApiUrl || !ENV.forgeApiKey) throw new Error("STORAGE_NOT_CONFIGURED");
  const presignUrl = new URL("v1/storage/presign/put", `${ENV.forgeApiUrl.replace(/\/+$/, "")}/`);
  presignUrl.searchParams.set("path", key);
  const presign = await fetchImpl(presignUrl, { headers: { Authorization: `Bearer ${ENV.forgeApiKey}` } });
  if (!presign.ok) throw new Error("STORAGE_PRESIGN_FAILED");
  const descriptor = await presign.json() as { url?: unknown };
  if (typeof descriptor.url !== "string" || !descriptor.url) throw new Error("STORAGE_PRESIGN_INVALID");
  const stored = await fetchImpl(descriptor.url, { method: "PUT", headers: { "Content-Type": contentType }, body: Buffer.from(bytes) });
  if (!stored.ok) throw new Error("STORAGE_PUT_FAILED");
  return { key, url: `/manus-storage/${key}` };
}

/** Stores declared corpus source bytes under the restricted governed-corpus namespace only. */
export async function storagePut(key: string, bytes: Uint8Array, contentType: string, fetchImpl: typeof fetch = fetch): Promise<StoredObject> {
  if (!/^governed-corpus\/[a-z0-9._/-]+\.json$/.test(key)) throw new Error("STORAGE_KEY_INVALID");
  return putManagedObject(key, bytes, contentType, fetchImpl);
}

/** Persists a complete signed receipt-bundle envelope so future verification does not require a retired private key. */
export async function storagePutSignedReceiptBundle(key: string, bytes: Uint8Array, fetchImpl: typeof fetch = fetch): Promise<StoredObject> {
  if (!/^signed-receipts\/[a-z0-9._-]{3,96}\/[a-f0-9]{64}\/[a-f0-9]{64}\.json$/.test(key)) throw new Error("SIGNED_BUNDLE_STORAGE_KEY_INVALID");
  return putManagedObject(key, bytes, "application/json", fetchImpl);
}
