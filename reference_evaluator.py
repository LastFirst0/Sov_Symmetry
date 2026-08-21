"""Starter-only pure evaluator. Copy and replace with a bounded deterministic predicate."""
from __future__ import annotations

import hashlib
import json
import sys


def evaluate(packet: dict) -> dict:
    values = packet.get("input")
    if not isinstance(values, list) or not 1 <= len(values) <= 8 or any(type(value) is not int for value in values):
        status, reason = "unverifiable", "E_SEQUENCE_INPUT"
    elif any(values[index] > values[index + 1] for index in range(len(values) - 1)):
        status, reason = "fail", "E_SEQUENCE_DECREASE"
    else:
        status, reason = "verified", "OK"
    receipt_id = hashlib.sha256(json.dumps({"predicate": "sequence.non_decreasing.v1", "input": values}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"status": status, "reason_code": reason, "receipt_id": f"receipt:{receipt_id}", "scope": "Finite integer sequence monotonicity only."}


if __name__ == "__main__":
    print(json.dumps(evaluate(json.loads(sys.stdin.read()))))
