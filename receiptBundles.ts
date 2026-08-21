import { createHash, createPrivateKey, createPublicKey, sign as signDetached } from "node:crypto";

export type ReceiptBundlePayload = {
  schema: "sov.archive_receipt_bundle.payload";
  schemaVersion: "0.1.0";
  receipt: {
    receiptId: string;
    accountOpenId: string;
    format: "csv" | "json";
    recordCount: number;
    filtersSnapshot: string;
    resultDigest: string;
    createdAt: string;
  };
  resultManifest: { artifactKey: string; revision: number; metadataDigest: string | null }[];
};

function configuredPrivateKey() {
  const material = process.env.SOVEREIGN_RECEIPT_SIGNING_PRIVATE_KEY;
  if (!material) throw new Error("RECEIPT_SIGNING_KEY_UNAVAILABLE");
  const normalized = material.trim().replace(/^['"]|['"]$/g, "").replace(/\\n/g, "\n");
  const attempts: (() => ReturnType<typeof createPrivateKey>)[] = [
    () => createPrivateKey(normalized),
    () => createPrivateKey({ key: JSON.parse(normalized), format: "jwk" }),
  ];
  if (/^[A-Za-z0-9+/_=-]+$/.test(normalized)) {
    const decoded = Buffer.from(normalized, "base64");
    attempts.push(() => createPrivateKey(decoded.toString("utf8")));
    attempts.push(() => createPrivateKey({ key: decoded, format: "der", type: "pkcs8" }));
    if (decoded.length === 32) {
      const pkcs8Prefix = Buffer.from("302e020100300506032b657004220420", "hex");
      attempts.push(() => createPrivateKey({ key: Buffer.concat([pkcs8Prefix, decoded]), format: "der", type: "pkcs8" }));
    }
  }
  let privateKey: ReturnType<typeof createPrivateKey> | null = null;
  for (const attempt of attempts) {
    try { privateKey = attempt(); break; } catch { /* Attempt only documented, non-secret key encodings. */ }
  }
  if (!privateKey) throw new Error("RECEIPT_SIGNING_KEY_UNPARSEABLE");
  if (privateKey.asymmetricKeyType !== "ed25519") throw new Error("RECEIPT_SIGNING_KEY_MUST_BE_ED25519");
  return privateKey;
}

export function receiptSigningDescriptor() {
  const publicKey = createPublicKey(configuredPrivateKey());
  const publicKeyJwk = publicKey.export({ format: "jwk" }) as JsonWebKey;
  if (publicKeyJwk.kty !== "OKP" || publicKeyJwk.crv !== "Ed25519" || !publicKeyJwk.x) throw new Error("RECEIPT_SIGNING_PUBLIC_KEY_INVALID");
  const keyFingerprint = createHash("sha256").update(JSON.stringify({ kty: publicKeyJwk.kty, crv: publicKeyJwk.crv, x: publicKeyJwk.x })).digest("hex");
  return { algorithm: "Ed25519" as const, keyFingerprint, publicKeyJwk };
}

export function signReceiptBundlePayload(payload: ReceiptBundlePayload) {
  const canonicalPayload = JSON.stringify(payload);
  const signature = signDetached(null, Buffer.from(canonicalPayload, "utf8"), configuredPrivateKey()).toString("base64url");
  return { schema: "sov.archive_receipt_bundle" as const, schemaVersion: "0.1.0", signing: receiptSigningDescriptor(), canonicalPayload, payload, signature: { encoding: "base64url" as const, value: signature } };
}
