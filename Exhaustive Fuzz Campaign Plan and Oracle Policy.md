# Exhaustive Fuzz Campaign Plan and Oracle Policy

## Objective

Exercise the actual current seams of the Rust parity crate and Python `FileObjectStore` across malformed values, boundary sizes, Unicode, duplicate keys, ID/path parsing, content-address collisions, replay drift, truncated files, manifest corruption, and operation-order permutations. The campaign is deterministic and reproducible from recorded seeds. It is not a cryptographic proof that SHA-256 has no collision; it is a search for implementation-induced collisions, identity aliasing, non-determinism, and fail-open behavior.

## Campaign lanes

| Lane | Target | Generator families | Primary oracle |
|---|---|---|---|
| R1 | Rust canonicalizer | recursive JSON values, key permutations, Unicode, integer boundaries, floats, deep arrays/objects | Python canonicalizer for accepted values; contract status for rejected values |
| R2 | Rust ID derivation | canonical-body permutations and mutation pairs | Same accepted bytes → same ID; changed bytes → changed ID in campaign corpus |
| R3 | Rust invariant interpreter | metric matrices, sparse tensors, malformed records, operation/input permutations | Shared vector semantics plus explicit status/reason-code policy |
| P1 | Python durable store | valid records, malformed IDs, object bytes, manifest lines, truncation, duplicate entries | clean reopen/replay root; tamper must fail closed |
| P2 | Python path and collision seam | IDs with boundary characters, same path/different bytes, idempotent re-put | content ID/path bijection and typed collision failure |
| P3 | Python replay seam | reorder, duplicate, missing, corrupt, appended, and edited manifest/object entries | manifest verification and recorded root expectations |

## Seed and volume policy

The suite uses fixed seeds `0x534f565f5231`, `0x534f565f5232`, and `0x534f565f5031`, plus the published fixtures and hand-authored boundary vectors. Each seed runs 10,000 generated cases per lane in the fast campaign, followed by a 100,000-case extended campaign when the fast campaign is clean. Every failure records seed, case index, minimized input, expected oracle, observed result, elapsed time, and resource class.

A “collision” means either: two distinct accepted canonical bodies produce the same derived ID within the corpus; two distinct stored byte payloads are accepted under one ID; or two distinct manifest histories produce an identical root while verification accepts both. A SHA-256 collision is not inferred from an absence of corpus collisions.

## Oracle hierarchy

1. **Exact canonical oracle:** accepted JSON values must match the Python reference canonical bytes and Rust output byte-for-byte. Rejected values must map to an allowed canonicalization error class.
2. **Contract oracle:** schemas and Core Contract rules determine whether a request is invalid, evaluable, failed, or unverifiable.
3. **Independent metamorphic oracle:** key-order permutations preserve bytes/ID; array permutations do not unless an operation explicitly declares order invariance; re-put of identical content is idempotent; altered stored bytes fail replay.
4. **Cross-language oracle:** the Rust result must match the Python/reference fixture for canonical bytes, ID, status, and reason code on the shared domain.
5. **No-oracle result:** if the generated case exercises unsupported scalar kinds, unknown operations, or an unmodeled mathematical condition, it must be classified `unverifiable` or a typed request error—not treated as a failure of the mathematics.

## Required property set

### Rust canonicalization and IDs

For every accepted value, canonicalization is deterministic across repeated calls; object key insertion order does not change bytes; string Unicode is preserved according to the contract; accepted integers remain within the safe boundary; no raw float/NaN/Infinity is accepted; and the ID equals SHA-256 of the returned bytes. For mutation pairs, a changed semantic body must either change the ID or be rejected. No accepted pair may produce two canonical byte strings for the same semantic body.

For every rejected value, the harness records a typed error and ensures no ID is returned. The harness separately counts parser rejection, contract rejection, and resource-limit rejection.

### Rust interpreter

For generated square integer diagonal matrices with nonzero diagonal entries, inverse checks are compared against an exact matrix oracle. For sparse symmetry, all generated entries are checked against a reference dictionary that treats missing components as zero. Input-order permutations preserve results. Unknown operation IDs are always `unverifiable` with `E_OPERATION_UNKNOWN`. Malformed references never produce `verified`.

### Python durable store

For every valid record graph, `put → get → reopen → verify_manifest` preserves the record bytes, object ID, and manifest root. Identical re-put is idempotent and does not append a duplicate manifest entry. Any edited object bytes, invalid JSON, altered record hash, duplicate object entry, unsupported manifest action, missing object, or truncated manifest must cause a typed audit failure or canonical parse failure; it must not return a valid root.

For path parsing, malformed IDs never escape the object root, and an ID with a valid digest cannot make the store read a different path. A same-ID/different-byte situation must fail with `E_ID_MISMATCH`.

## Resource and safety limits

The fast campaign caps generated depth at 8, object/array width at 16, string length at 256, tensor dimension at 8, and file payload at 64 KiB. The extended campaign raises each limit only after the fast campaign passes. Each case has a 2-second process limit and a 128 MiB RSS observation target. A timeout or memory exhaustion is a `resource finding`, not a semantic failure, and blocks promotion until triaged.

## Failure classification

| Finding | Severity | Promotion behavior |
|---|---|---|
| Distinct accepted bodies share an ID | Critical | Stop; preserve reproducer; do not continue promotion |
| Same ID accepts distinct stored bytes | Critical | Stop; fix store boundary |
| Different key order changes accepted canonical bytes | High | Stop parity gate |
| Rust/Python accepted-domain mismatch | High | Stop parity gate; classify contract or implementation drift |
| Tampered object/manifest verifies | Critical | Stop audit/replay gate |
| Malformed input crashes or escapes root | High | Stop robustness gate |
| Unknown/unsupported feature returns `verified` | Critical | Stop fail-closed gate |
| Deterministic resource limit exceeded | Medium/High | Quarantine case; revise limit or classify `unverifiable` |
| Non-semantic error-text difference only | Low | Record, but do not block if code/status contract matches |

## Exit criteria

The fast campaign passes only when there are zero critical/high findings, zero unexplained cross-language mismatches, zero accepted-domain ID collisions, zero fail-open outcomes, and all expected tamper/replay cases fail closed. The extended campaign may be marked complete only when its seed list, counts, duration, resource observations, minimized corpus, and known limitations are recorded. This result authorizes only the next local gate; it does not authorize public quorum or consensus deployment.

## References

[1] [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/info/rfc8785/)  
[2] [NIST FIPS 180-4: Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)  
[3] [JSON Schema Draft 2020-12](https://json-schema.org/specification)
