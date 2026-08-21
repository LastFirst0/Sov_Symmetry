import { createHash, createPublicKey, verify } from "node:crypto";
import { readFileSync } from "node:fs";

const paths = process.argv.slice(2);
if (paths.length !== 2) throw new Error("EXPECTED_PRE_AND_POST_BUNDLE_PATHS");

const results = paths.map((path) => {
  const bytes = readFileSync(path);
  const bundle = JSON.parse(bytes.toString("utf8"));
  const jwk = bundle?.signing?.publicKeyJwk;
  if (jwk?.kty !== "OKP" || jwk?.crv !== "Ed25519" || typeof jwk.x !== "string") throw new Error(`INVALID_PUBLIC_KEY_JWK:${path}`);
  const fingerprint = createHash("sha256").update(JSON.stringify({ kty: jwk.kty, crv: jwk.crv, x: jwk.x })).digest("hex");
  if (fingerprint !== bundle?.signing?.keyFingerprint) throw new Error(`KEY_FINGERPRINT_MISMATCH:${path}`);
  if (typeof bundle?.canonicalPayload !== "string" || JSON.stringify(bundle.payload) !== bundle.canonicalPayload) throw new Error(`CANONICAL_PAYLOAD_MISMATCH:${path}`);
  if (bundle?.signature?.encoding !== "base64url" || typeof bundle.signature.value !== "string") throw new Error(`INVALID_SIGNATURE_ENCODING:${path}`);
  const valid = verify(null, Buffer.from(bundle.canonicalPayload, "utf8"), createPublicKey({ key: jwk, format: "jwk" }), Buffer.from(bundle.signature.value, "base64url"));
  if (!valid) throw new Error(`SIGNATURE_INVALID:${path}`);
  return {
    path,
    receiptId: bundle.payload.receipt.receiptId,
    keyFingerprint: fingerprint,
    bundleDigest: createHash("sha256").update(bytes).digest("hex"),
    payloadDigest: createHash("sha256").update(bundle.canonicalPayload).digest("hex"),
    signatureValid: valid,
  };
});

if (results[0].keyFingerprint === results[1].keyFingerprint) throw new Error("ROTATION_KEY_FINGERPRINT_DID_NOT_CHANGE");
console.log(JSON.stringify({ preRotation: results[0], postRotation: results[1], independentPublicMaterialVerification: "pass" }, null, 2));
