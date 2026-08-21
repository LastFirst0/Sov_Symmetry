# Sovereign Engine Build / Buy / Adapt / Avoid Matrix

## Decision rubric

Candidates are assessed against semantic authority, determinism, license clarity, maintenance signal, language fit, testability, attack surface, interoperability, and reversibility. A candidate may assist an adapter or test oracle, but only the internal typed model and evidence core own Sovereign Engine semantics.

| Capability | Candidate / reference | Decision | Why | Integration boundary | Gate before adoption |
|---|---|---|---|---|---|
| Canonical claim/evidence records | Internal | **Build** | This is the project’s differentiating trust boundary; no external project has the transcript/GU claim model. | Pure core schema and verifier | Canonical vectors, replay, tamper suite |
| Typed tensor/geometry AST | Internal | **Build** | Must encode project-specific convention profiles, source spans, units, claim class, and evidence links. | Core Rust types + JSON schema | Invalid-index and convention fixture suite |
| Symbolic tensor reference | [SymPy tensor](https://docs.sympy.org/latest/modules/tensor/tensor.html) | **Adapt** | Provides index/symmetry/canonicalization patterns and potential differential oracle. | Python exploratory/reference adapter only | Version pin, license review, fixtures revealing expected divergences |
| GR symbolic/numerical fixtures | [EinsteinPy](https://einsteinpy-einsteinpy.readthedocs.io/en/latest/user_guide.html) | **Adapt** | Useful for standard metrics, Christoffel/Riemann calculations, and educational/prototype fixtures. | Python fixture generator / differential test adapter | Reproducible fixture definitions; no semantic ownership |
| Formal proof anchors | [Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/) | **Adapt selectively** | Strong for stable high-value statements; video evidence highlights substantial formalization and maintenance overhead. | Separate formal-reference workspace | Named theorem, source/revision, executable bridge status |
| OpenAPI SDK generation | [OpenAPI Generator](https://openapi-generator.tech/docs/usage/) | **Adopt later** | Supports validation and generated clients after semantic contract stabilizes. | Generated TypeScript/Python/Rust SDKs | Pinned version, clean regeneration, consumer contract tests |
| Contract/property API testing | [Schemathesis](https://github.com/schemathesis/schemathesis) | **Adapt later** | Candidate for OpenAPI fuzz/property tests once a runnable server boundary exists. | CI non-authoritative API test job | API stable, test data isolation, deterministic seeds |
| Python property tests | [Hypothesis](https://github.com/HypothesisWorks/hypothesis) | **Adopt for exploration** | Good candidate for generating tensor index, canonicalization, and equivalence counterexamples. | Python reference/fixture tests | Saved seed/shrunk counterexample evidence |
| Rust property tests | Rust ecosystem candidate | **Evaluate** | Repository search did not identify a clear primary result; select after direct crate/doc review. | Rust core tests | Cargo-vet/license/security review |
| Release provenance | [in-toto](https://in-toto.io/) concepts | **Adapt later** | An open metadata model for who performed which step and in which order fits release evidence. | CI release package metadata | Clean artifact pipeline, no opaque builders |
| Artifact signing | [Sigstore](https://docs.sigstore.dev/about/overview/) | **Adopt in audit-only stage** | Enables signed, identity-linked, verifiable artifacts; does not replace mathematical evidence. | Release artifact signing/verification | OIDC/CI identity, artifact storage, audit-only rollout |
| Core persistence | Filesystem + SQLite-compatible model | **Build minimally** | Offline replay and simple inspectability precede graph/database services. | Evidence store adapter | Atomic write, migrations, corruption tests |
| Graph search/provenance service | Neo4j + embeddings | **Defer** | Current adapter entangles mutable network services with canonicalization; core does not require this. | Optional query adapter | Measured query need, threat model, data-retention policy |
| P2P/blockchain/consensus | Existing repo modules | **Defer** | No green-core use case or threat model justifies inclusion in initial trust boundary. | Later systems layer | Specific verified use case and attack model |
| LLM agent/runtime | Existing repo and Manus API | **Adapter only** | Useful for explanation/planning; cannot set verifier semantics or promote claims. | Typed operation-plan adapter | All actions traceable to registry/evidence |
| KMS/private signing service | Existing adapter placeholder | **Avoid for now** | Operational/security complexity and currently hard-coded development defaults. | Future adapter | Security owner, secrets design, threat model |
| Private Sigstore/Fulcio/Rekor | External infrastructure | **Avoid for now** | Premature without release cadence and security operations capacity. | None | Sustained public/audit-only success and requirements |

## Architectural non-goals for the first release

The green core does not train models, provide a global knowledge graph, establish a blockchain, prove GU physics, host a production cluster, or recreate full symbolic mathematics/GR/formal-proof ecosystems. It provides an auditable semantic substrate that can ask those systems precisely bounded questions.

## Reference sources

[1] [SymPy tensor documentation](https://docs.sympy.org/latest/modules/tensor/tensor.html)  
[2] [EinsteinPy user guide](https://einsteinpy-einsteinpy.readthedocs.io/en/latest/user_guide.html)  
[3] [Lean 4 guide](https://leanprover.github.io/theorem_proving_in_lean4/)  
[4] [OpenAPI Generator usage](https://openapi-generator.tech/docs/usage/)  
[5] [Sigstore overview](https://docs.sigstore.dev/about/overview/)  
[6] [in-toto](https://in-toto.io/)  
[7] `github_ecosystem_candidates.tsv`; `github_validation_candidates.tsv`; `EXTERNAL_ECOSYSTEM_RESEARCH_FINDINGS.md`
