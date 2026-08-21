# Owner-Authorized Genesis Source Intake Exercise

**Exercise date:** 2026-08-19

This record documents a real owner-authorized dashboard upload. It is a provenance and operational test record only. The accepted bytes were not automatically promoted to a research artifact, publication request, verification verdict, or interpretive conclusion.

| Field | Recorded value |
|---|---|
| Intake ID | `corpus_mszotx0m_4fccb28d` |
| Declared source role | `genesis_oshb` |
| Original filename | `Genesis_OSHB.json` |
| Managed storage key | `governed-corpus/genesis_oshb/ddadbb315bb13fcca64ebfabaeb3006fc5294cda50676db1d570c7f6cd8de7ef-80c37687-ce4f-4522-8848-e4ce6fcb4a74.json` |
| Stored source pointer | `/manus-storage/governed-corpus/genesis_oshb/ddadbb315bb13fcca64ebfabaeb3006fc5294cda50676db1d570c7f6cd8de7ef-80c37687-ce4f-4522-8848-e4ce6fcb4a74.json` |
| Byte length | `19,220,561` |
| SHA-256 | `ddadbb315bb13fcca64ebfabaeb3006fc5294cda50676db1d570c7f6cd8de7ef` |
| Validation status | `accepted` |
| Validator | `living-word-source.v1` |
| Validated word count | `20,630` |
| Recorded actor | `owner-token` |

## Verification Observations

The stored source pointer returned a server-managed HTTP `307` redirect to a signed object URL, confirming that the recorded object key resolves through the managed storage proxy. The database row contains the same SHA-256 digest in its top-level field and structural validation report.

The no-promotion boundary was checked with a single-row database query against the recorded pointer and digest. It returned `publishedArtifactCount = 0` and `publicationRequestCount = 0`. The upload therefore created only a durable source-intake record.

> **Boundary:** Structural source acceptance and retention do not validate the content, establish a research claim, publish an archive record, or issue a universal-kernel receipt.
