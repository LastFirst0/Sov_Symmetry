import { createPublicKey, verify } from "node:crypto";
import { readFileSync } from "node:fs";
import { getReceiptSigningKey } from "../server/db";

type Bundle = { signing: { keyFingerprint: string; publicKeyJwk: JsonWebKey }; canonicalPayload: string; signature: { value: string } };
async function inspect(path: string) {
  const bundle = JSON.parse(readFileSync(path, "utf8")) as Bundle;
  const signatureValid = verify(null, Buffer.from(bundle.canonicalPayload, "utf8"), createPublicKey({ key: bundle.signing.publicKeyJwk, format: "jwk" }), Buffer.from(bundle.signature.value, "base64url"));
  const retained = await getReceiptSigningKey(bundle.signing.keyFingerprint);
  if (!signatureValid || !retained) throw new Error(`CONTINUITY_CHECK_FAILED:${path}`);
  return { path, keyFingerprint: bundle.signing.keyFingerprint, signatureValid, retainedStatus: retained.status };
}

const pre = await inspect("/tmp/sov_rotation_pre.json");
const post = await inspect("/tmp/sov_rotation_post.json");
if (pre.retainedStatus !== "retired" || post.retainedStatus !== "active") throw new Error("CONTINUITY_KEY_STATUS_UNEXPECTED");
console.log(JSON.stringify({ pre, post, continuityVerified: true }));
