"""Pure local Q0 quorum verification.

This module is an offline verification adapter. It does not discover nodes,
fetch keys, access a clock, write storage, or claim Byzantine consensus.
Fixture signing uses HMAC-SHA256 only to exercise exact DSSE payload binding;
this is not a production public-key profile.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from .audit import dsse_pae
from .canonical import canonicalize, parse_strict_json
from .errors import CoreContractError

DSSE_PAYLOAD_TYPE = "application/vnd.sovereign.quorum.response.v1+json"
FIXTURE_ALGORITHM = "hmac-sha256-fixture-only"


def _typed_id(prefix: str, body: Mapping[str, Any]) -> str:
    return f"{prefix}:sha256:{hashlib.sha256(canonicalize(body)).hexdigest()}"


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _unb64(value: Any) -> bytes:
    if not isinstance(value, str):
        raise CoreContractError("E_SCHEMA_INVALID", "base64 field must be a string")
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except (ValueError, UnicodeEncodeError) as exc:
        raise CoreContractError("E_CANONICALIZATION", "invalid base64 field") from exc


def fixture_sign(payload_type: str, payload: bytes, secret: bytes) -> str:
    return _b64(hmac.new(secret, dsse_pae(payload_type, payload), hashlib.sha256).digest())


def build_fixture_response(
    *,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    key_id: str,
    secret: bytes,
    status: str,
    output_ids: Sequence[str],
    reason_codes: Sequence[str],
    verification_scope: str = "exact_symbolic",
    evaluator_release: str = "release:fixture-evaluator.v1",
    response_tag: str = "default",
) -> dict[str, Any]:
    payload = {
        "schema": "sov.quorum.response",
        "schema_version": "0.1.0",
        "response_id": f"response:{key_id}:{response_tag}",
        "request_id": request["request_id"],
        "policy_id": policy["policy_id"],
        "contract_version": request["contract_version"],
        "operation_id": request["operation_id"],
        "predicate_id": request["predicate_id"],
        "convention_profile_id": request["convention_profile_id"],
        "scalar_policy_id": request["scalar_policy_id"],
        "tolerance_policy_id": request["tolerance_policy_id"],
        "status": status,
        "output_ids": list(output_ids),
        "reason_codes": list(reason_codes),
        "verification_scope": verification_scope,
        "evaluator_release": evaluator_release,
    }
    payload_bytes = canonicalize(payload)
    envelope = {
        "payloadType": DSSE_PAYLOAD_TYPE,
        "payload": _b64(payload_bytes),
        "signatures": [{"keyid": key_id, "sig": fixture_sign(DSSE_PAYLOAD_TYPE, payload_bytes, secret)}],
    }
    return {"payload": payload, "envelope": envelope}


def _policy_index(policy: Mapping[str, Any]) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    candidates = policy.get("candidates")
    threshold = policy.get("threshold")
    if not isinstance(candidates, list) or not isinstance(threshold, int) or isinstance(threshold, bool) or not (1 <= threshold <= len(candidates)):
        raise CoreContractError("E_SCHEMA_INVALID", "invalid quorum threshold or candidate list")
    by_key: dict[str, Mapping[str, Any]] = {}
    by_node: dict[str, Mapping[str, Any]] = {}
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            raise CoreContractError("E_SCHEMA_INVALID", "candidate must be an object")
        key_id, node_id = candidate.get("key_id"), candidate.get("node_id")
        if not isinstance(key_id, str) or not isinstance(node_id, str) or key_id in by_key or node_id in by_node:
            raise CoreContractError("E_SCHEMA_INVALID", "candidate key and node identities must be unique")
        by_key[key_id] = candidate
        by_node[node_id] = candidate
    return by_key, by_node


def _decode_response(response: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any], by_key: Mapping[str, Mapping[str, Any]]) -> tuple[dict[str, Any], Mapping[str, Any], str]:
    envelope = response.get("envelope")
    if not isinstance(envelope, Mapping) or envelope.get("payloadType") != DSSE_PAYLOAD_TYPE:
        raise CoreContractError("E_PAYLOAD_TYPE", "unsupported or missing DSSE payload type")
    payload_bytes = _unb64(envelope.get("payload"))
    payload = parse_strict_json(payload_bytes.decode("utf-8"))
    if not isinstance(payload, dict) or canonicalize(payload) != payload_bytes:
        raise CoreContractError("E_CANONICALIZATION", "DSSE payload is not canonical JSON")
    signatures = envelope.get("signatures")
    if not isinstance(signatures, list) or len(signatures) != 1 or not isinstance(signatures[0], Mapping):
        raise CoreContractError("E_SCHEMA_INVALID", "Q0 requires exactly one fixture signature")
    signature = signatures[0]
    key_id = signature.get("keyid")
    candidate = by_key.get(key_id)
    if candidate is None:
        raise CoreContractError("E_KEY_UNKNOWN", "signer key is not in quorum policy")
    if candidate.get("status") != "active" or candidate.get("algorithm") != FIXTURE_ALGORITHM:
        raise CoreContractError("E_KEY_REJECTED", "signer key is inactive or unsupported")
    secret = _unb64(candidate.get("fixture_secret_b64"))
    expected = fixture_sign(DSSE_PAYLOAD_TYPE, payload_bytes, secret)
    if not hmac.compare_digest(expected, signature.get("sig", "")):
        raise CoreContractError("E_SIGNATURE_INVALID", "fixture DSSE signature does not verify")
    required = {"request_id": request.get("request_id"), "policy_id": policy.get("policy_id"), "contract_version": request.get("contract_version"), "operation_id": request.get("operation_id"), "predicate_id": request.get("predicate_id"), "convention_profile_id": request.get("convention_profile_id"), "scalar_policy_id": request.get("scalar_policy_id"), "tolerance_policy_id": request.get("tolerance_policy_id")}
    if any(payload.get(key) != value for key, value in required.items()):
        raise CoreContractError("E_REQUEST_BINDING", "response is not bound to the exact request and policy")
    if payload.get("status") not in {"verified", "fail", "unverifiable"}:
        raise CoreContractError("E_SCHEMA_INVALID", "unsupported core response status")
    return payload, candidate, hashlib.sha256(payload_bytes).hexdigest()


def _equivalence_key(payload: Mapping[str, Any]) -> tuple[Any, ...]:
    reason_codes = tuple(sorted(str(code) for code in payload.get("reason_codes", [])))
    output_ids = tuple(payload.get("output_ids", []))
    return (payload["request_id"], payload["contract_version"], payload["operation_id"], payload["predicate_id"], payload["convention_profile_id"], payload["scalar_policy_id"], payload["tolerance_policy_id"], payload["status"], output_ids, reason_codes, payload["verification_scope"])


def aggregate(policy: Mapping[str, Any], request: Mapping[str, Any], responses: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_key, _ = _policy_index(policy)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    by_identity: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for response in responses:
        try:
            payload, candidate, payload_hash = _decode_response(response, request, policy, by_key)
            item = {"payload": payload, "node_id": candidate["node_id"], "key_id": candidate["key_id"], "payload_hash": payload_hash, "equivalence_key": _equivalence_key(payload)}
            by_identity[candidate["node_id"]].append(item)
            accepted.append(item)
        except CoreContractError as error:
            rejected.append({"response_id": response.get("payload", {}).get("response_id") if isinstance(response.get("payload"), Mapping) else None, "code": error.code})
    equivocations: list[dict[str, Any]] = []
    counted: list[dict[str, Any]] = []
    for node_id, items in by_identity.items():
        unique_hashes = {item["payload_hash"] for item in items}
        if len(unique_hashes) > 1:
            equivocations.append({"node_id": node_id, "payload_hashes": sorted(unique_hashes), "response_ids": sorted(item["payload"].get("response_id", "") for item in items)})
        counted.append(sorted(items, key=lambda item: (item["key_id"], item["payload_hash"]))[0])
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for item in counted:
        groups[item["equivalence_key"]].append(item)
    threshold = policy["threshold"]
    qualifying = [items for items in groups.values() if len(items) >= threshold]
    if equivocations or len(qualifying) > 1:
        status = "contested"
    elif len(qualifying) == 1:
        result_status = qualifying[0][0]["payload"]["status"]
        status = {"verified": "threshold_verified", "fail": "threshold_failed", "unverifiable": "threshold_unverifiable"}[result_status]
    else:
        status = "insufficient_quorum"
    body = {"schema": "sov.quorum.decision", "schema_version": "0.1.0", "request_id": request["request_id"], "policy_id": policy["policy_id"], "decision_status": status, "accepted_response_ids": sorted(item["payload"].get("response_id", "") for item in counted), "rejected": sorted(rejected, key=lambda item: (item.get("response_id") or "", item["code"])), "equivalence_class_count": len(groups), "equivocation_evidence": equivocations, "threshold": threshold}
    return {"decision_id": _typed_id("quorum_decision", body), "body": body}
