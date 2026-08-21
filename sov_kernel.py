#!/usr/bin/env python3
"""Command-line access to the small offline Sovereign Engine kernel."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sov_evidence_geometry_core import (FileObjectStore, advanced_evidence_export, attach_local_audit, check_identity_matrix, check_matrix_inverse, check_symmetric_matrix, check_partial_order, check_undirected_connected_graph, check_rank3_last_indices_symmetric, empirical_evidence_status, parse_empirical_claim_packet, parse_empirical_analysis_receipt, receipt_bundle, replay_receipt_bundle, verify_release_artifact)

def load_json(value: str):
    path=Path(value)
    return json.loads(path.read_text()) if path.exists() else json.loads(value)
def dump(value): print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
def main():
    parser=argparse.ArgumentParser(description="Run a clear, bounded offline kernel check and receive a replayable receipt.")
    sub=parser.add_subparsers(dest="command", required=True)
    check=sub.add_parser("check"); check.add_argument("name", choices=["symmetric","identity","inverse","partial-order","graph-connected","tensor-last-symmetric"]); check.add_argument("--input", required=True, help="JSON text or JSON file; inverse accepts {left,right}."); check.add_argument("--audit-store", help="optional local store directory for audit attachment")
    replay=sub.add_parser("replay"); replay.add_argument("--bundle", required=True, help="receipt bundle JSON file")
    samples=sub.add_parser("sample-gallery", help="generate fixture-backed public examples and receipt bundles"); samples.add_argument("--output", help="optional output directory")
    empirical=sub.add_parser("validate-empirical-packet", help="validate an empirical evidence packet without running scientific inference"); empirical.add_argument("--packet", required=True)
    analysis=sub.add_parser("validate-analysis-receipt", help="validate a versioned external-method receipt against an empirical packet"); analysis.add_argument("--packet", required=True); analysis.add_argument("--receipt", required=True)
    empirical_template=sub.add_parser("empirical-template", help="write a local editable empirical packet template"); empirical_template.add_argument("--output", required=True)
    release=sub.add_parser("verify-release", help="verify a locally available release manifest and optional DSSE attestation without network access"); release.add_argument("--bundle", required=True); release.add_argument("--policy"); release.add_argument("--attestation"); release.add_argument("--report"); release.add_argument("--expect-status", choices=["verified", "fail", "unverifiable"])
    args=parser.parse_args()
    if args.command=="sample-gallery":
        command=[sys.executable, str(Path(__file__).with_name("generate_sample_gallery.py"))]
        if args.output: command.extend(["--output", args.output])
        subprocess.run(command, check=True); return
    if args.command=="validate-empirical-packet":
        packet=load_json(args.packet); dump({"packet": parse_empirical_claim_packet(packet), "status": empirical_evidence_status(packet)}); return
    if args.command=="validate-analysis-receipt":
        packet=load_json(args.packet); receipt=load_json(args.receipt); dump({"analysis_receipt": parse_empirical_analysis_receipt(receipt, packet), "status": empirical_evidence_status(packet, receipt)}); return
    if args.command=="empirical-template":
        subprocess.run([sys.executable, str(Path(__file__).with_name("write_empirical_packet_template.py")), "--output", args.output], check=True); return
    if args.command=="verify-release":
        report=verify_release_artifact(args.bundle, policy_path=args.policy, attestation_path=args.attestation)
        if args.report: Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
        dump(report)
        if args.expect_status and report["status"] != args.expect_status: raise SystemExit(2)
        return
    if args.command=="replay":
        candidate=load_json(args.bundle); dump(replay_receipt_bundle(candidate.get("bundle", candidate))); return
    payload=load_json(args.input)
    receipt = check_symmetric_matrix(payload) if args.name=="symmetric" else check_identity_matrix(payload) if args.name=="identity" else check_partial_order(payload) if args.name=="partial-order" else check_undirected_connected_graph(payload) if args.name=="graph-connected" else check_rank3_last_indices_symmetric(payload) if args.name=="tensor-last-symmetric" else check_matrix_inverse(payload["left"], payload["right"])
    bundle=receipt_bundle(receipt)
    if args.audit_store:
        attachment=attach_local_audit(bundle, FileObjectStore(args.audit_store)); bundle=receipt_bundle(receipt, assurance=attachment)
    dump({"receipt":receipt,"bundle":bundle,"advanced_export":advanced_evidence_export(bundle)})
if __name__=="__main__": main()
