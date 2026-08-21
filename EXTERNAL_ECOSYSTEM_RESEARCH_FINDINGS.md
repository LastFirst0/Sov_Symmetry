# External Ecosystem Research Findings

**Access date:** 2026-08-16  
**Use:** These findings inform build/buy/adapt decisions. They do not establish Sovereign Engine claims or authorize a dependency without license, security, and integration review.

## Symbolic tensor and geometry foundations

| Source | Observed capability | Architectural implication |
|---|---|---|
| [SymPy tensor documentation](https://docs.sympy.org/latest/modules/tensor/tensor.html) | Defines tensor index types with optional metrics, covariant/contravariant index representation, symmetry metadata, metric contraction/raising/lowering, and Butler–Portugal canonicalization for supported tensor symmetries. | **Adapt as an exploratory/reference backend**, not as the trusted canonical object model. Its index/symmetry patterns are valuable for fixture/differential tests. |
| [EinsteinPy user guide](https://einsteinpy-einsteinpy.readthedocs.io/en/latest/user_guide.html) | Provides metric-oriented geometry utilities including Christoffel and Riemann symbolic calculations, coordinate conversions, and GR-oriented numerical trajectories. | **Adopt for exploratory/numerical reference fixtures only.** Keep Sovereign’s evidence schema and operation registry independent. |
| [Lean 4 theorem-proving guide](https://leanprover.github.io/theorem_proving_in_lean4/) | Lean 4 is a programming language/proof assistant based on dependent type theory with formal structures, proofs, tactics, and computation. | **Use selectively as a formal-reference layer** for high-value stable statements, not as an all-at-once replacement for Rust/Python implementation. |

## API and release-evidence foundations

| Source | Observed capability | Architectural implication |
|---|---|---|
| [OpenAPI Generator usage](https://openapi-generator.tech/docs/usage/) | Supports specification validation, generator discovery/configuration, dry-run generation, and language-specific client/server generation from OpenAPI. | **Adopt after contract stabilization** for Python/TypeScript/Rust clients. Pin tool version and commit generated outputs or regenerate in CI deterministically. |
| [Sigstore overview](https://docs.sigstore.dev/about/overview/) | Supports signing/verifying artifacts, identity binding, short-lived certificates, and transparency-log verification for releases, binaries, containers, SBOMs, and more. | **Defer enforcement until a release pipeline exists.** Start audit-only after green core and clean artifact generation; do not deploy private trust infrastructure prematurely. |
| [in-toto](https://in-toto.io/) | Defines an open framework/metadata approach for making supply-chain steps, actors, and order transparent. | **Adapt conceptual model** for release evidence, but do not force production adoption before artifact boundaries and CI are stable. |

## First-hand video evidence

### Lean maintainer talk: “The Lean proof assistant: introduction and challenges”

URL: [YouTube](https://www.youtube.com/watch?v=BY78oZYMGCk). A structured video analysis captured Leonardo de Moura’s discussion of Lean as a proof assistant and programming language grounded in dependent type theory. The analysis reported statements that Lean has a small trusted kernel, that formalization has substantial overhead, and that large formal mathematical objects impose engineering and build-time costs. The bounded architectural consequence is to formalize selected high-value invariants and specification anchors only when their failure cost justifies the maintenance burden.

### Sigstore practitioner talk: “Securing the Supply Chain with Sigstore Artifacts Signatures at Scale”

URL: [YouTube](https://www.youtube.com/watch?v=Tp-t_7ccW0Y). The analyzed practitioner discussion described short-lived signing keys, identity-bound certificates, transparency/audit logs, gradual rollout, registry load, and admission-time verification. The bounded architectural consequence is that artifact signing can strengthen release evidence after reproducible artifact generation exists; it should be audit-only first and must not substitute for kernel-level mathematical replay.

## GitHub candidate snapshot

The program captured a live candidate snapshot in `github_ecosystem_candidates.tsv`. Notable candidates include [SymPy](https://github.com/sympy/sympy), [EinsteinPy](https://github.com/einsteinpy/einsteinpy), [Lean 4](https://github.com/leanprover/lean4), [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator), [in-toto](https://github.com/in-toto), and [Sigstore](https://github.com/sigstore). Candidate popularity, license field, and recency are discovery signals only; they require individual review before adoption.

## Preliminary build/buy/adapt conclusions

1. **Build:** Canonical claim/evidence model, typed geometry semantics, operation/predicate registry, replay, and GU hypothesis policy. These are Sovereign Engine’s unique trust boundary.
2. **Adapt:** SymPy and EinsteinPy for reference/differential fixtures; Lean for selected formal anchors; in-toto-style provenance concepts for release evidence.
3. **Adopt later:** OpenAPI Generator after API stabilization; Sigstore after clean artifacts/release workflows exist.
4. **Avoid for now:** Private certificate infrastructure, cluster admission controllers, broad agent/provenance platforms, and any external library that would become the authoritative meaning model.

## Limitation

The scientific-skill finder’s real-time fetch encountered GitHub API parsing failures and fell back to cache without matches. This is recorded as a tool-path limitation, not evidence that no suitable external skills exist. The next review should use manual GitHub evaluation and test candidate workflows before creating custom skills.
