import { createPublicKey, verify } from "node:crypto";
import { writeFileSync } from "node:fs";
import { getArchiveExportReceipt, recordArchiveExport, recordReceiptBundleSignature, recordReceiptSigningKey } from "../server/db";
import { receiptSigningDescriptor, signReceiptBundlePayload } from "../server/receiptBundles";

const accountOpenId = process.env.OWNER_OPEN_ID;
if (!accountOpenId) throw new Error("OWNER_OPEN_ID_REQUIRED");
const receipt = await recordArchiveExport(accountOpenId, "json", { term: "", category: "all", status: "all", sort: "updated_desc" });
const persisted = await getArchiveExportReceipt(accountOpenId, receipt.receiptId);
if (!persisted?.resultManifest) throw new Error("ROTATION_EXERCISE_MANIFEST_REQUIRED");
const resultManifest = JSON.parse(persisted.resultManifest);
const bundle = signReceiptBundlePayload({ schema: "sov.archive_receipt_bundle.payload", schemaVersion: "0.1.0", receipt: { receiptId: persisted.receiptId, accountOpenId: persisted.accountOpenId, format: persisted.format, recordCount: persisted.recordCount, filtersSnapshot: persisted.filtersSnapshot, resultDigest: persisted.resultDigest, createdAt: persisted.createdAt.toISOString() }, resultManifest });
const publicKey = createPublicKey({ key: bundle.signing.publicKeyJwk, format: "jwk" });
const valid = verify(null, Buffer.from(bundle.canonicalPayload, "utf8"), publicKey, Buffer.from(bundle.signature.value, "base64url"));
if (!valid) throw new Error("ROTATION_EXERCISE_SIGNATURE_INVALID");
await recordReceiptSigningKey(receiptSigningDescriptor());
await recordReceiptBundleSignature({ receiptId: persisted.receiptId, keyFingerprint: bundle.signing.keyFingerprint, canonicalPayload: bundle.canonicalPayload });
if (process.env.ROTATION_EXERCISE_OUTPUT) writeFileSync(process.env.ROTATION_EXERCISE_OUTPUT, JSON.stringify(bundle), { encoding: "utf8", mode: 0o600 });
console.log(JSON.stringify({ receiptId: persisted.receiptId, keyFingerprint: bundle.signing.keyFingerprint, verified: valid, recordCount: persisted.recordCount }));
