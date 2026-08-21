# Durable Signed-Bundle Retention Boundary

**Implemented:** 2026-08-19  
**Schema migration:** `0009_curvy_susan_delgado.sql`  
**Purpose:** Preserve every **newly issued** signed receipt-bundle envelope without retaining signing private material.

## Why This Exists

A public key can verify an old receipt only when the complete signed envelope is still available: the canonical payload, signature, signing descriptor, and receipt manifest are all needed. Earlier signature-event rows retained a receipt ID, public-key fingerprint, and payload digest, but not the complete bundle envelope. Those metadata values cannot recreate a lost signature after a private key has been retired.

> The system therefore stores a new signed envelope at the time it is issued. Future key rotation needs only that stored JSON and the retained public-key record; it does **not** need to retain an old private key.

## Data and Storage Boundary

| Layer | Retained value | Does not retain |
|---|---|---|
| Managed object storage | Exact JSON signed-bundle envelope under `signed-receipts/{receiptId}/{keyFingerprint}/{bundleDigest}.json` | Private key material, bearer tokens, or a general write namespace. |
| Signature-event ledger | Storage key, storage URL, SHA-256 digest of the serialized envelope, existing payload digest, receipt ID, public-key fingerprint, and timestamp | The private key or any database copy of raw bundle bytes. |
| Existing public-key register | Active/retired public JWK and lifecycle status | Retired private keys. |

The storage namespace is strict. A bundle key must contain an allowed receipt ID plus 64-character lowercase-hex public-key fingerprint and envelope digest. Any other key is rejected before a storage-provider request is made.

## Issuance Flow

1. The authorized receipt owner requests a signed bundle.
2. The server constructs and signs the bundle with the active managed key.
3. The exact serialized JSON is SHA-256 hashed and written once to the restricted signed-receipts namespace.
4. Only after storage succeeds does the server append immutable signature-event metadata with the storage pointer and digest.
5. The bundle is returned to the owner as before.

This ordering is intentionally fail-closed. If storage fails, the signature-event metadata is not written and no falsely “retained” bundle is claimed.

## Verification Readiness

A future independent continuity replay needs the persisted envelope, its ledger pointer/digest, and the historical public-key record. Verification can then recompute the serialized-bundle digest and use the JWK embedded in the bundle and/or retained in the public-key register to verify the Ed25519 signature. The retired key’s private half must remain unavailable.

This implementation cannot reconstruct any bundle that was issued before the change. Consequently, the historical pre-rotation evidence gate remains open until a new controlled rotation has a retained pre-rotation envelope or an earlier complete envelope is recovered from a legitimate archive.

## Validation

| Check | Result |
|---|---|
| Additive database migration | Applied; `bundleStorageKey`, `bundleStorageUrl`, and `bundleDigest` are present and nullable for pre-existing rows. |
| Namespace validation | Passing unit coverage accepts only declared receipt/key/digest paths and rejects malformed paths. |
| Signing retention contract | Passing unit coverage verifies that bundle storage occurs before signature-event persistence and that the pointer/digest are recorded. |
| Dashboard regression and build | **83 tests passed; 2 opt-in tests skipped; production build passed.** |

## Explicit Limitations

This is an evidence-retention mechanism. It does not promote an adapter, validate an external claim, or confer authority on the exploratory runtime. Existing historical rows are intentionally left nullable rather than backfilled with invented bundle data.
