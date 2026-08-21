# Q1 Test-Oracle Policy

The oracle is defined from the Core Contract and next-wave specification, not from the current implementation. Each case must record the input mutation, expected status or typed error, observed result, canonical decision digest, and limitation.

| Case family | Expected oracle |
|---|---|
| Three active identities, one compatible verified class | `threshold_verified`. |
| Three active identities, one compatible failed predicate class | `threshold_failed`. |
| Compatible unsupported/prerequisite responses at threshold | `threshold_unverifiable`, never affirmative verification. |
| Fewer than threshold eligible identities | `insufficient_quorum`. |
| Two trusted incompatible equivalence classes | `contested`. |
| Same identity emits two valid incompatible responses | `contested` with equivocation evidence. |
| Duplicate response from the same identity | Count once; preserve evidence; never increase independence. |
| Invalid signature, payload type, request ID, policy ID, key, or canonical bytes | Reject and preserve rejection evidence. |
| Invalid threshold, duplicate candidate key, or duplicate candidate node | Typed policy/schema error and no decision record. |
| Response order permutation | Byte-identical decision body and content ID. |
| Audit metadata mutation without core-result mutation | Equivalence remains unchanged if metadata is outside the core key. |
| Output ID, scalar policy, tolerance policy, convention, or evaluator-release mutation | Incompatible class or rejection according to the binding profile; never silently merge. |

## Falsification rules

A test is unexplained when the observed output is not in the oracle set, when a case changes outcome under permutation, when a rejected response disappears from evidence, when two keys attached to one identity increase the count, or when any exception produces an affirmative result.

## Campaign controls

Use fixed seeds, bounded case counts, a clean source revision, explicit Python/Rust toolchain versions, and machine-readable reports. Do not report a finite campaign as a proof of collision resistance or Byzantine consensus. A successful campaign establishes only that the tested implementation matched the named oracle over the named corpus.
