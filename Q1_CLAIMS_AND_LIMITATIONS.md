# Q1 Claims and Limitations

| Claim | Evidence class | Evidence | Confidence | Limitation |
|---|---|---|---|---|
| The offline aggregator applies threshold logic over unique identities. | Tested contract | `sov_evidence_geometry_core/quorum.py`; Q1 audit report; Q0 fuzz report. | High for the tested fixture profile. | Does not prove live registry correctness or operator independence. |
| Response order does not affect the canonical decision body. | Tested contract | Q1 order-permutation case and Q0 1,000-case order campaign. | High for the named implementation and corpus. | Not a universal statement about future adapters. |
| Valid signer equivocation produces a contested result. | Tested contract | Q1 valid-equivocation case and Q0 2,000-case equivocation campaign. | High for the fixture profile. | Does not address live key compromise or network evidence delivery. |
| The HMAC DSSE fixture binds exact payload bytes. | Tested contract | Quorum module and signature/binding mutation cases. | High for the fixture profile. | HMAC is explicitly not a production public-key profile. |
| The underlying geometric predicate is true. | Not claimed | No release evidence. | None. | Q1 verifies evidence relationships, not physical or semantic truth. |
| The system is production Byzantine consensus. | Not claimed | Explicitly excluded by the wave specification. | None. | Network, liveness, fault model, and operational gates are incomplete. |

## Release language

Use **candidate** only for the bounded offline harness. Use **candidate-with-blockers** when any required QG is not evidenced. Never use “secure,” “trustless,” “Byzantine,” “collision-proof,” or “hallucination-free” as an unqualified release claim.
