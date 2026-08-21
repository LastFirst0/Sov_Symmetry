# Q0 Quorum Verification and Adversarial Fuzzing Deck Outline

## Deck thesis

Q0 is an offline verification protocol: it answers whether a declared threshold of distinct policy-approved verifier identities reproduced the same Core Contract result. It preserves conflicts and limitations rather than converting agreement into physical truth.

## Slide plan

1. **Title — Q0: Agreement Without Overclaiming**  
   Introduce the implementation wave and the central boundary: quorum evidence is not a truth oracle.

2. **Why the quorum layer exists**  
   Show the problem between one deterministic evaluator and a release decision: independent responses must be bound to the exact request, contract, policies, and output IDs.

3. **Protocol boundary**  
   Diagram the Core Contract, response envelopes, local aggregator, audit evidence, and explicitly excluded network/consensus surfaces.

4. **The Q0 object model**  
   Present request, verifier identity, response, policy, decision, and equivocation evidence as typed immutable records.

5. **Deterministic decision function**  
   Explain compatibility grouping, `(key_id, response_id)` ordering, threshold evaluation, and the six decision statuses.

6. **Offline DSSE/key-policy fixture profile**  
   Explain exact payload binding, payload type, active key selection, duplicate identity counting, and why fixture HMAC is not production signing.

7. **Adversarial behaviors**  
   Show duplicate identities, same-key equivocation, output divergence, stale/revoked keys, request mismatch, and insufficient quorum.

8. **Fuzz campaign design**  
   Summarize deterministic seed, generator classes, oracle hierarchy, and fail-closed rules.

9. **Campaign results**  
   Show 5,750 adversarial cases: 1,650 duplicate-identity cases, 2,000 equivocation cases, 1,000 order permutations, 1,000 binding/signature mutations, and 100 invalid-policy cases; 0 unexplained failures.

10. **What the campaign proved—and did not prove**  
    State the implementation evidence and the limits: no production consensus, key custody, network liveness, Byzantine resilience, or physical-theory validation.

11. **Promotion gates QG1–QG5**  
    Show semantic agreement, cryptographic binding, audit integration, adversarial confidence, and operational/security decision gates.

12. **Next wave**  
    Sequence full fixture/error mapping, rational parity, local durable quorum decisions, offline signature policy profiles, audit checkpoint integration, and only then operational review.

## Evidence anchors

- `NEXT_GATED_QUORUM_CONSENSUS_WAVE_v0.2.md`
- `sov_evidence_geometry_core/quorum.py`
- `tests/core_contract/test_quorum.py`
- `tools/run_quorum_adversarial_fuzz.py`
- `q0_adversarial_fuzz_report.json`
- `FUZZ_CAMPAIGN_REPORT.md`

## Visual direction

Use the established Sovereign Engine Mission Control Ledger style: graphite field, ivory evidence panels, oxide-red decision marks, monospaced protocol telemetry, and a restrained geometry/orbit motif. Use no decorative imagery that implies a live distributed network; all diagrams should communicate bounded local verification and preserved uncertainty.
