# Active Program Review Tasks

- [x] Re-read the current roadmap, target architecture, validation policy, and repository evidence matrix.
- [x] Identify policy gaps, duplicated scope, sequencing flaws, ownership gaps, and missing negative-case controls.
- [x] Deliver a prioritized change/add/remove/defer amendment set with rationale, effort class, and decision impact.
- [x] Define exact research-quarantine entry, verification, test-oracle, falsification, escalation, and exit criteria.
- [x] Draft Core Contract v0.1 with canonical objects, strict schema definitions, byte canonicalization, statuses, errors, and conformance fixtures.
- [x] Validate all new machine-readable schemas and package the specifications for implementation.
- [x] Inspect Core Contract schemas, fixture pack, existing repository boundaries, and package conventions for the Python reference implementation.
- [x] Implement the Python SDK for JCS-compatible canonicalization, schema validation, derived IDs, and typed results.
- [x] Implement the reference interpreter, operation registry, and invariant checks with deterministic fixture execution.
- [x] Execute conformance, negative-case, and replay/tamper tests; document remaining cross-language obligations.
- [x] Draft detailed subsystem specifications for audit trail, quorum verification, persistence, adapters, operations, release evidence, and integrations.
- [x] Consolidate specifications into a staged build plan with gates, dependencies, and owner roles.
- [x] Package the evidence-first Sovereign Engine research-and-build workflow as a reusable, validated skill.
- [x] Implement a Rust Core Contract fixture-parity crate and compare canonical bytes, derived IDs, and invariant outcomes with the Python reference.
- [x] Implement durable local evidence persistence with atomic storage, manifests, restore/replay, collision, and tamper tests.
- [x] Implement executable cryptographic audit primitives for events, Merkle checkpoints, inclusion proofs, consistency proofs, and tamper detection.
- [x] Verify the complete wave through focused Rust/Python parity and persistence/audit test suites.
- [x] Create and present an architecture deck summarizing the reference SDK, trust boundaries, verification evidence, and staged subsystems.

- [x] Re-read quorum, audit, Core Contract, parity, and persistence artifacts for the next gated wave.
- [x] Specify bounded multi-node quorum verification, cryptographic consensus evidence, trust policy, and failure semantics.
- [x] Build deterministic fuzz harnesses for Rust parity and Python durable storage.
- [x] Run fuzz campaigns and classify collisions, malformed inputs, replay/tamper findings, and resource limits.
- [x] Publish remediation decisions, promotion gates, and the next coordinated execution backlog.
- [ ] Expand Rust parity to full published fixture/error mapping and rational scalar cases.
- [ ] Implement the pure local quorum aggregator and offline DSSE/key-policy fixtures.

Parallel input list for later analysis: quorum/audit/Core Contract specifications; Rust parity crate and vectors; Python durable store and audit primitives; existing validation/falsification policy; current repository CI/toolchain evidence.

- [x] Inspect current Q0 quorum, audit, Core Contract, and fuzz artifacts.
- [x] Implement the pure local quorum aggregator and offline DSSE/key-policy fixtures.
- [x] Execute adversarial fuzz tests for equivocation, duplicate identity, policy, and order independence.
- [x] Prepare and present a Q0 protocol and fuzz-campaign slide deck.
- [ ] Expand Rust parity to the Q0 schemas, reason codes, rational scalar cases, and full published invariant set.
- [ ] Persist quorum decisions, rejected responses, and equivocation evidence through the durable store.
- [ ] Add offline public-key DSSE and key-policy fixtures and integrate audit checkpoints.

- [x] Package the evidence-first quorum audit and release-candidate workflow as a reusable skill.
- [x] Define and execute the next adversarial security audit campaign for Work Package Q1.
- [x] Prepare a reproducible Q1 release-candidate evidence bundle with manifests and checksums.
- [x] Write the comprehensive Sovereign Engine architecture and fuzz-testing technical whitepaper.
- [x] Extend the documentation site/dashboard with architecture, protocol, audit, and release-candidate documentation.
- [x] Validate the reusable skill, audit evidence, release bundle, whitepaper, and documentation site.

- [x] Re-baseline the trusted-kernel program against current Core Contract, parity, audit, quorum, and formal-anchor evidence.
- [x] Define an evidence-weighted kernel completion model and release boundary.
- [x] Write a coordinated multi-wave kernel execution roadmap with exit gates, dependencies, risks, and non-goals.
- [x] Select and initiate the first parallelizable implementation batch only after the release gates and fixture contracts are explicit.

- [x] Verify and version the K1 shared fixture manifest with tamper rejection.
- [x] Add fail-closed Rust shared-fixture ingestion and publish a coverage map.
- [x] Define the offline Ed25519 fixture/key-policy profile and negative-case matrix.
- [x] Define durable quorum decision, rejection, and equivocation record contracts.
- [x] Produce an integrated K1 release-gate report from reproducible checks.

- [x] Execute all 17 shared Core Contract semantic cases through the Rust K1 adapter with fail-closed coverage reporting.
- [x] Persist durable quorum decisions, rejected responses, and equivocation evidence through the FileObjectStore.
- [x] Bind durable quorum records to Merkle checkpoints and validate restart and tamper behavior.
- [x] Package and validate a reusable K1 kernel-closure skill.
- [x] Generate and present a K1 chained-execution status and remaining-blockers slide deck.

- [x] Classify current kernel rules as essential safeguards, provisional implementation choices, or unclear terminology.
- [x] Define a simplified public kernel model with practical input, check, receipt, and next-action flows.
- [x] Consolidate the remaining essential release scope and remove unnecessary internal ceremony from the public kernel surface.
- [x] Produce a plain-language kernel guide, worked examples, and evidence-backed release checklist.

- [x] Run and document a step-by-step matrix-symmetry receipt walkthrough.
- [x] Classify assurance-layer components by advanced-user exposure priority and purpose.
- [x] Write a stakeholder presentation script for the simplified plain-language kernel model.

- [x] Draft a non-technical FAQ for holds, fail, and unverifiable outcomes.
- [x] Specify advanced assurance exposure for receipt provenance, signatures, quorum decisions, and Merkle evidence.
- [x] Generate and present a complete stakeholder deck matching the simplified-kernel presentation script.

- [x] Define a replayable receipt provenance and advanced evidence bundle contract.
- [x] Implement local provenance and optional advanced evidence export for simple kernel receipts.
- [x] Validate receipt replay, tamper rejection, and advanced bundle boundary behavior.

- [x] Define the receipt-to-local-audit attachment and offline Ed25519 fixture contracts.
- [x] Implement durable audit attachments for replayable receipt exports.
- [x] Implement and test offline Ed25519 DSSE fixture verification with typed key-policy outcomes.
- [x] Validate integrated receipt replay, audit proof, signature, and tamper behavior.

- [x] Freeze the final offline kernel release boundary and acceptance gates.
- [x] Harden the public receipt interface and provide a reproducible kernel CLI.
- [x] Build a reproducible offline release evidence bundle and integrated verification runner.
- [x] Execute the final isolated release matrix across Python, audit, signature, persistence, and Rust parity.
- [x] Publish the offline kernel release guide and explicit operational follow-on boundary.

- [x] Extract the multi-framework evidence model and claim boundaries from science_project.md.
- [x] Audit and correct theory-specific or Geometric Unity-preferring kernel documentation.
- [x] Define the theory-agnostic universal kernel ontology and framework-adapter contract.
- [x] Re-baseline the roadmap and public kernel documentation around evaluable claims rather than preferred theories.

- [x] Run and preserve a comparative same-claim test across multiple framework labels.
- [x] Audit remaining kernel modules and release assets for theory-specific assumptions or nomenclature.
- [x] Generalize any remaining theory-specific kernel paths and define the next universal adapter portfolio gate.
- [x] Write a stakeholder script for the theory-agnostic universal kernel re-baseline.

- [x] Define and implement the next universal graph invariant adapter with fixtures and explicit non-claims.
- [x] Define and implement the next finite tensor relation adapter with fixtures and explicit non-claims.
- [x] Classify theory-specific historical research as archival context and update public entry points.
- [x] Generate and present the theory-agnostic universal kernel stakeholder slide deck.

- [x] Define and execute a shared six-adapter universal integration fixture pack with positive, negative, malformed, and mutation cases.
- [x] Publish the formal third-party theoretical framework adapter specification and admission test policy.
- [x] Write the stakeholder script for the theory-agnostic universal kernel and adapter contract.
- [x] Complete final offline universal-kernel release verification and evidence bundle closure.

- [x] Draft the versioned empirical-claim packet with dataset provenance, uncertainty, and external-method bindings.
- [x] Draft the architecture and governance gates for admitting the first external third-party adapter.
- [x] Generate and present the empirical evidence layer and external-adapter roadmap deck.

- [x] Implement and test the fail-closed empirical-claim packet parser and validator in the core package.
- [x] Publish the reusable eight-gate external-adapter evaluation scorecard and checklist.
- [x] Write the stakeholder script matching the empirical evidence and external-adapter roadmap deck.
- [x] Write non-technical documentation explaining the end-to-end claim intake, evidence, review, and outcome process.

- [x] Build the canonical documentation catalog, archive labeling, and machine-readable documentation manifest.
- [x] Generate synchronized public adapter journeys, receipt examples, and CLI reference materials.
- [x] Implement the third-party adapter starter kit, code-owned registry, and eight-gate validator.
- [x] Implement analysis receipts, empirical fixtures, CLI tools, and packet-builder contracts.
- [x] Integrate release evidence, claim registry, and learning documentation into the dashboard.
- [x] Add governance workflows, documentation validation, and final ecosystem release checks.
- [x] Validate the complete ecosystem matrix, rebuild the curated release bundle, and synchronize the dashboard evidence feed.
- [x] Inventory legacy and current kernel artifacts, compare their actual scopes and evidence, and publish a source-grounded migration/bridge report.
- [x] Inventory deferred legacy mathematical components, assess a fail-closed runtime/kernel feedback loop, and define a falsifiable geometric-language research program.
- [x] Run a bounded hierarchy-recovery experiment on a transparent sample corpus and publish its code, inputs, results, and limits.
- [x] Write the exact production-ready technical specification for the legacy-runtime/universal-kernel feedback loop.
- [x] Research reusable open-source components and relevant integration paths for the experiment and feedback loop.
- [x] Generate an evidence-grounded presentation covering deferred mathematics, feedback-loop architecture, and language-geometry experiment findings.
- [x] Inspect the `v2.0-clean-release` genetic-analysis additions, classify their actual molecular capabilities and evidence limits, and assess a bounded molecular-sequence geometry experiment.
- [x] Establish the research register, source-manifest schema, decision log, claim taxonomy, and falsification register.
- [x] Create public-data provenance contracts and M0 molecular-experiment intake validation controls.
- [x] Implement signed release-artifact verification with DSSE policy, tamper fixtures, CLI reporting, and release-gate integration.
- [x] Implement the M0 DNA experiment framework with frozen data manifests, matched baselines, leakage checks, and evidence artifacts.
- [x] Build research-register, experiment-record, adapter-review, and evidence-gap workflows into the dashboard.
- [x] Establish bounded automation runbooks, connector governance, skill evaluation, and approved custom-skill workflow.
- [x] Create a versioned automation-job registry, validator, and terminal-failure controls for deterministic evidence maintenance.
- [x] Publish connector governance and a skill-quarantine scorecard that records K-Dense candidate disposition without automatic import.
- [x] Run the full platform validation matrix, regenerate release/dashboard evidence, and publish the work-package closeout.
