#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=. python3 -m py_compile \
  sov_evidence_geometry_core/adapter_registry.py \
  sov_evidence_geometry_core/legacy_runtime_adapter.py \
  sov_evidence_geometry_core/empirical_analysis.py \
  sov_evidence_geometry_core/release_assurance.py \
  tools/build_docs_manifest.py \
  tools/generate_sample_gallery.py \
  tools/generate_fixture_manifest.py \
  tools/validate_adapter_package.py \
  tools/validate_governance_register.py \
  tools/validate_docs_and_governance.py \
  tools/build_release_dashboard_feed.py
PYTHONPATH=. python3 tools/build_docs_manifest.py
PYTHONPATH=. python3 tools/validate_docs_and_governance.py
PYTHONPATH=. python3 tools/generate_sample_gallery.py
PYTHONPATH=. python3 tools/generate_fixture_manifest.py --fixture templates/external_adapter/fixtures.json --output /tmp/sov_fixture_manifest.json
grep -q '2e0aabe6ec03f7102e307ca65473defaa6d0e9668b6ba702c197062bb1a92cc8' /tmp/sov_fixture_manifest.json
PYTHONPATH=. python3 tools/validate_adapter_package.py templates/external_adapter --execute-reference > /tmp/sov_adapter_admission_report.json
grep -q '"decision": "candidate"' /tmp/sov_adapter_admission_report.json
PYTHONPATH=. pytest -q --confcutdir=tests/core_contract \
  tests/core_contract/test_simple_kernel.py \
  tests/core_contract/test_universal_kernel.py \
  tests/core_contract/test_legacy_runtime_adapter.py \
  tests/core_contract/test_universal_integration_pack.py \
  tests/core_contract/test_empirical_packet.py \
  tests/core_contract/test_receipt_provenance.py \
  tests/core_contract/test_assurance_attachments.py \
  tests/core_contract/test_release_assurance.py \
  tests/core_contract/test_k1_fixture_manifest.py \
  tests/core_contract/test_durable_quorum_k1.py \
  tests/core_contract/test_quorum.py \
  tests/core_contract/test_persistence_and_audit.py \
  tests/core_contract/test_documentation_manifest.py \
  tests/core_contract/test_sample_gallery.py \
  tests/core_contract/test_adapter_ecosystem.py \
  tests/core_contract/test_empirical_analysis_receipt.py \
  tests/core_contract/test_empirical_template_cli.py \
  tests/core_contract/test_ecosystem_dashboard_feed.py \
  tests/core_contract/test_governance_ecosystem.py \
  tests/core_contract/test_fixture_manifest_generator.py \
  tests/core_contract/test_docs_tamper_gate.py
PYTHONPATH=. python tools/run_universal_six_adapter_integration.py > /tmp/sov_universal_six_adapter_report.json
cargo test --manifest-path crates/sov-contract-parity/Cargo.toml --quiet
PYTHONPATH=. python tools/sov_kernel.py check symmetric --input '[[1,2],[2,4]]' --audit-store /tmp/sov_release_cli_audit > /tmp/sov_release_cli_output.json
PYTHONPATH=. python tools/sov_kernel.py replay --bundle /tmp/sov_release_cli_output.json | grep -q '"status": "verified"'
PYTHONPATH=. python tools/sov_kernel.py validate-empirical-packet --packet tests/core_contract/data/empirical_packet_example.json > /tmp/sov_empirical_packet_status.json
PYTHONPATH=. python tools/sov_kernel.py validate-analysis-receipt --packet tests/core_contract/data/empirical_packet_example.json --receipt tests/core_contract/data/empirical_analysis_receipt_example.json > /tmp/sov_empirical_analysis_status.json
grep -q 'E_EMPIRICAL_INTERPRETATION_EXTERNAL' /tmp/sov_empirical_analysis_status.json
PYTHONPATH=. python tools/build_release_dashboard_feed.py
env -i PATH="$PATH" PYTHONPATH=. python3 tools/sov_kernel.py --help > /tmp/sov_clean_cli_help.txt
sha256sum artifacts/documentation_manifest.json artifacts/sample_gallery/v0.1/index.json artifacts/ecosystem_dashboard_feed.json > artifacts/ECOSYSTEM_ARTIFACTS.sha256
printf 'OFFLINE_KERNEL_ECOSYSTEM_RELEASE_MATRIX=PASS\n'
