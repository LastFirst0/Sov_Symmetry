# Fuzz Campaign Report: Rust Parity and Python Durable Store

**Campaign status:** Fast deterministic campaign passed after remediation.  
**Campaign seeds:** `0x534f565f5231`, `0x534f565f5232`, `0x534f565f5031`.  
**Scope:** Rust canonicalization/ID streaming parity; Python durable object storage, replay, manifest corruption, ID/path parsing, and tamper behavior.

## Final results

| Lane | Cases | Accepted/handled | Findings | Result |
|---|---:|---:|---:|---|
| Rust ↔ Python canonicalization and IDs | 10,000 | Python accepted 8,734; rejected 1,266 | 0 cross-language mismatches; 0 accepted-domain ID collisions | Passed |
| Python durable valid-record/idempotence | 1,000 records plus repeat puts | 1,000 idempotent cases | 0 clean replay failures | Passed |
| Python object-byte tamper mutations | 250 | 250 rejected | 0 tamper acceptances after fix | Passed |
| Python manifest-corruption mutations | 250 | 250 rejected | 0 corruption acceptances | Passed |
| Malformed ID/path cases | 6 boundary inputs | All rejected or contained | 0 path escapes after fix | Passed |
| Focused regression suite | 18 tests | 18 passed | Includes both fuzz-found regressions | Passed |

The Rust stream completed in approximately 0.56 seconds. The Python durable-store campaign completed in approximately 2.78 seconds. These timings are local observations, not performance guarantees.

## Findings and remediation

The first campaign exposed two real implementation defects.

**Finding F-001 — path traversal through non-hex digest text, critical.** The store accepted a 64-character digest containing `../`; path construction then escaped the object root. The fix requires the digest portion to match exactly `[0-9a-f]{64}` before path construction. A regression test now asserts `E_SCHEMA_INVALID` for the reproducer.

**Finding F-002 — noncanonical stored bytes accepted as valid, high.** Appending whitespace to a stored canonical JSON object changed the file bytes but not the parsed semantic object. Because manifest verification re-canonicalized the parsed object, the tampered file was previously accepted. The fix reads raw bytes, parses them, and requires `canonicalize(parsed) == raw_bytes` before returning the object. A regression test now asserts `E_AUDIT_TAMPER` for the reproducer.

These findings demonstrate why the campaign is valuable: the SHA-256 implementation was not the problem; the storage boundary and path validator were.

## Oracle interpretation

The campaign used the following hierarchy: exact Rust/Python canonical bytes for the accepted common domain; contract error classes for rejected values; metamorphic key-order and idempotence properties; exact status/reason-code expectations for supported invariant cases; and fail-closed behavior for unsupported or malformed cases. A zero-collision corpus is evidence about this implementation and corpus only. It is not a mathematical proof of SHA-256 collision resistance.

## Promotion decision

The Rust/Python parity and local durable-store gates may advance to the next local wave. The evidence does **not** authorize production quorum, public transparency, distributed consensus, key custody, or a claim that majority agreement establishes physical truth.

## Next steps

1. Expand Rust parity beyond the current integer-only and two-predicate surface to schema/semantic error mapping, rational scalar cases, all published conformance fixtures, and the remaining registered invariant checks.
2. Add a pure local quorum aggregator implementing the v0.2 equivalence key and decision statuses, with no network or storage side effects.
3. Add offline DSSE/key-policy fixtures and verify exact payload binding, duplicate-key counting, expiration/revocation, and equivocation evidence.
4. Add durable quorum/audit decision records and replay proofs only after the local aggregator is deterministic.
5. Defer network discovery, leader election, replicated logs, and production cryptographic custody until the QG5 operational/security gate is accepted.

## References

[1] [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/info/rfc8785/)  
[2] [NIST FIPS 180-4: Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)  
[3] [DSSE Protocol](https://github.com/secure-systems-lab/dsse/blob/master/protocol.md)  
[4] [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/info/rfc9162)
