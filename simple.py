"""Small public verification interface for clear, bounded mathematical checks.

This module does not replace the Core Contract. It gives people a direct way to
ask one concrete question and receive a readable receipt with the same three
terminal statuses used by the deterministic kernel.
"""
from __future__ import annotations
import hashlib
import math
from collections.abc import Sequence
from typing import Any
from .canonical import canonicalize

_PUBLIC_WORDS = {"verified": "holds in this check", "fail": "does not hold in this check", "unverifiable": "cannot be checked from this input"}
def _hashable(value: Any) -> Any:
    if isinstance(value, float): return {"kind": "float_text", "value": format(value, ".17g")}
    if isinstance(value, list): return [_hashable(item) for item in value]
    if isinstance(value, dict): return {key: _hashable(item) for key, item in value.items()}
    return value
def _receipt_id(body: dict[str, Any]) -> str: return "sov:sha256:" + hashlib.sha256(canonicalize(_hashable(body))).hexdigest()
def check_symmetric_matrix(matrix: Sequence[Sequence[int | float]]) -> dict[str, Any]:
    """Check whether a finite square numeric matrix equals its transpose."""
    normalized = [list(row) for row in matrix]
    if not normalized or any(len(row) != len(normalized) for row in normalized) or any(not isinstance(value, (int, float)) or isinstance(value, bool) or (isinstance(value, float) and not math.isfinite(value)) for row in normalized for value in row):
        status, why, details = "unverifiable", "I need a finite square matrix of ordinary numbers.", {"reason_code": "E_INPUT_NOT_SQUARE_NUMERIC"}
    else:
        mismatches = [{"at": [row, column], "value": normalized[row][column], "transpose_value": normalized[column][row]} for row in range(len(normalized)) for column in range(row + 1, len(normalized)) if normalized[row][column] != normalized[column][row]]
        status = "verified" if not mismatches else "fail"
        why = "Every off-diagonal pair matches its transpose partner." if not mismatches else "At least one off-diagonal pair differs from its transpose partner."
        details = {"predicate": "matrix.symmetric.v1", "mismatches": mismatches}
    body = {"schema": "sov.simple_receipt", "schema_version": "0.1.0", "check": "matrix.symmetric.v1", "input": normalized, "status": status, "details": details}
    return {"receipt_id": _receipt_id(body), "status": status, "plain_status": _PUBLIC_WORDS[status], "what_i_checked": "Whether the matrix equals its transpose (Aᵀ = A).", "why": why, "details": details, "next_action": "Use the result as evidence for this matrix symmetry check only; inspect the mismatches if it fails.", "scope": "Exact finite-matrix equality only; this receipt does not prove a physical theory or a broader tensor claim.", "provenance": {"check": "matrix.symmetric.v1", "input": normalized, "receipt_schema": "sov.simple_receipt.v0.1"}}
def check_identity_matrix(matrix: Sequence[Sequence[int | float]]) -> dict[str, Any]:
    """Check whether a finite square numeric matrix is the identity matrix."""
    normalized = [list(row) for row in matrix]
    if not normalized or any(len(row) != len(normalized) for row in normalized) or any(not isinstance(value, (int, float)) or isinstance(value, bool) or (isinstance(value, float) and not math.isfinite(value)) for row in normalized for value in row):
        status, why, details = "unverifiable", "I need a finite square matrix of ordinary numbers.", {"reason_code": "E_INPUT_NOT_SQUARE_NUMERIC"}
    else:
        mismatches=[{"at":[r,c],"value":normalized[r][c],"expected":1 if r==c else 0} for r in range(len(normalized)) for c in range(len(normalized)) if normalized[r][c] != (1 if r==c else 0)]
        status="verified" if not mismatches else "fail"; why="Every diagonal entry is 1 and every off-diagonal entry is 0." if not mismatches else "One or more entries differ from the identity matrix."
        details={"predicate":"matrix.identity.v1","mismatches":mismatches}
    body={"schema":"sov.simple_receipt","schema_version":"0.1.0","check":"matrix.identity.v1","input":normalized,"status":status,"details":details}
    return {"receipt_id":_receipt_id(body),"status":status,"plain_status":_PUBLIC_WORDS[status],"what_i_checked":"Whether this matrix is the identity matrix (I).","why":why,"details":details,"next_action":"Inspect the reported entry mismatches or use this as the expected product in an inverse check.","scope":"Exact finite-matrix equality only; no numerical tolerance or physical interpretation is implied.","provenance":{"check":"matrix.identity.v1","input":normalized,"receipt_schema":"sov.simple_receipt.v0.1"}}
def check_matrix_inverse(matrix: Sequence[Sequence[int | float]], inverse: Sequence[Sequence[int | float]]) -> dict[str, Any]:
    """Check whether two finite square numeric matrices multiply to the identity matrix."""
    left=[list(row) for row in matrix]; right=[list(row) for row in inverse]
    n=len(left)
    valid=n>0 and len(right)==n and all(len(row)==n for row in left+right) and all(isinstance(v,(int,float)) and not isinstance(v,bool) and (not isinstance(v,float) or math.isfinite(v)) for row in left+right for v in row)
    if not valid: status, why, details="unverifiable","I need two finite square numeric matrices of the same size.",{"reason_code":"E_INPUT_NOT_COMPATIBLE_SQUARE_NUMERIC"}
    else:
        product=[[sum(left[r][k]*right[k][c] for k in range(n)) for c in range(n)] for r in range(n)]
        mismatches=[{"at":[r,c],"product":product[r][c],"expected":1 if r==c else 0} for r in range(n) for c in range(n) if product[r][c] != (1 if r==c else 0)]
        status="verified" if not mismatches else "fail"; why="The declared matrix product equals the identity matrix." if not mismatches else "The declared matrix product contains entries that differ from identity."
        details={"predicate":"matrix.inverse.v1","product":product,"mismatches":mismatches}
    body={"schema":"sov.simple_receipt","schema_version":"0.1.0","check":"matrix.inverse.v1","left":left,"right":right,"status":status,"details":details}
    return {"receipt_id":_receipt_id(body),"status":status,"plain_status":_PUBLIC_WORDS[status],"what_i_checked":"Whether the first matrix multiplied by the second equals identity.","why":why,"details":details,"next_action":"Inspect the product mismatch or use a declared inverse candidate with corrected entries.","scope":"Exact finite-matrix multiplication only; this is not a general symbolic, numeric-tolerance, or physical metric proof.","provenance":{"check":"matrix.inverse.v1","left":left,"right":right,"receipt_schema":"sov.simple_receipt.v0.1"}}

def check_partial_order(relation: Sequence[Sequence[bool | int]]) -> dict[str, Any]:
    """Check whether a finite 0/1 relation matrix is reflexive, antisymmetric, and transitive."""
    normalized = [list(row) for row in relation]
    valid = bool(normalized) and all(len(row) == len(normalized) for row in normalized) and all(isinstance(value, (bool, int)) and not isinstance(value, float) and value in (0, 1, False, True) for row in normalized for value in row)
    if not valid:
        status, why, details = "unverifiable", "I need a finite square relation matrix containing only 0 or 1.", {"reason_code":"E_INPUT_NOT_SQUARE_BINARY_RELATION"}
    else:
        n = len(normalized)
        missing_reflexive = [{"at":[i,i],"expected":1,"value":normalized[i][i]} for i in range(n) if not normalized[i][i]]
        anti_pairs = [{"pair":[i,j]} for i in range(n) for j in range(i+1,n) if normalized[i][j] and normalized[j][i]]
        transitive = [{"path":[i,j,k],"missing":[i,k]} for i in range(n) for j in range(n) for k in range(n) if normalized[i][j] and normalized[j][k] and not normalized[i][k]]
        violations = {"missing_reflexivity":missing_reflexive,"antisymmetry_pairs":anti_pairs,"missing_transitivity":transitive}
        status = "verified" if not any(violations.values()) else "fail"
        why = "The relation is reflexive, antisymmetric, and transitive." if status == "verified" else "The relation violates one or more partial-order requirements."
        details = {"predicate":"relation.partial_order.v1", **violations}
    body = {"schema":"sov.simple_receipt","schema_version":"0.1.0","check":"relation.partial_order.v1","input":normalized,"status":status,"details":details}
    return {"receipt_id":_receipt_id(body),"status":status,"plain_status":_PUBLIC_WORDS[status],"what_i_checked":"Whether this finite relation is a partial order (reflexive, antisymmetric, and transitive).","why":why,"details":details,"next_action":"Inspect the reported relation violations or use the verified relation as a bounded order structure.","scope":"Finite binary relations only; this does not establish a physical causal theory or any framework-level interpretation.","provenance":{"check":"relation.partial_order.v1","input":normalized,"receipt_schema":"sov.simple_receipt.v0.1"}}

def check_undirected_connected_graph(adjacency: Sequence[Sequence[bool | int]]) -> dict[str, Any]:
    """Check whether a finite binary, symmetric, loop-free adjacency matrix is connected."""
    normalized = [list(row) for row in adjacency]
    valid = bool(normalized) and all(len(row) == len(normalized) for row in normalized) and all(isinstance(v, (bool, int)) and not isinstance(v, float) and v in (0, 1, False, True) for row in normalized for v in row)
    if not valid:
        status, why, details = "unverifiable", "I need a finite square 0/1 adjacency matrix.", {"reason_code":"E_INPUT_NOT_SQUARE_BINARY_GRAPH"}
    else:
        n=len(normalized); asym=[{"pair":[i,j]} for i in range(n) for j in range(i+1,n) if bool(normalized[i][j]) != bool(normalized[j][i])]; loops=[i for i in range(n) if normalized[i][i]]
        if asym or loops:
            status, why, details = "unverifiable", "I need an undirected loop-free graph: the adjacency matrix must be symmetric with zeros on the diagonal.", {"reason_code":"E_INPUT_NOT_SIMPLE_UNDIRECTED_GRAPH","asymmetric_pairs":asym,"loop_vertices":loops}
        else:
            seen={0}; frontier=[0]
            while frontier:
                current=frontier.pop()
                for neighbor, edge in enumerate(normalized[current]):
                    if edge and neighbor not in seen: seen.add(neighbor); frontier.append(neighbor)
            missing=sorted(set(range(n))-seen); status="verified" if not missing else "fail"; why="Every vertex is reachable from the first vertex." if status=="verified" else "One or more vertices are disconnected from the first vertex."; details={"predicate":"graph.undirected_connected.v1","reachable_vertices":sorted(seen),"unreachable_vertices":missing}
    body={"schema":"sov.simple_receipt","schema_version":"0.1.0","check":"graph.undirected_connected.v1","input":normalized,"status":status,"details":details}
    return {"receipt_id":_receipt_id(body),"status":status,"plain_status":_PUBLIC_WORDS[status],"what_i_checked":"Whether this finite simple undirected graph is connected.","why":why,"details":details,"next_action":"Inspect unreachable vertices or supply a symmetric loop-free adjacency matrix.","scope":"Finite simple undirected graphs only; connectivity does not establish a network, spacetime, or emergent-geometry interpretation.","provenance":{"check":"graph.undirected_connected.v1","input":normalized,"receipt_schema":"sov.simple_receipt.v0.1"}}

def check_rank3_last_indices_symmetric(tensor: Sequence[Sequence[Sequence[int | float]]]) -> dict[str, Any]:
    """Check T[i,j,k] = T[i,k,j] for a finite rank-three numeric tensor."""
    normalized = [[list(row) for row in plane] for plane in tensor]
    valid = bool(normalized) and all(bool(plane) for plane in normalized)
    if valid:
        second=len(normalized[0]); third=len(normalized[0][0]) if normalized[0] else 0
        valid = second == third and all(len(plane)==second and all(len(row)==third for row in plane) for plane in normalized) and all(isinstance(v,(int,float)) and not isinstance(v,bool) and (not isinstance(v,float) or math.isfinite(v)) for plane in normalized for row in plane for v in row)
    if not valid:
        status, why, details = "unverifiable", "I need a finite rectangular rank-three numeric tensor whose final two dimensions have equal size.", {"reason_code":"E_INPUT_NOT_RANK3_NUMERIC_SQUARE_LAST_INDICES"}
    else:
        mismatch=[{"at":[i,j,k],"mirror_at":[i,k,j],"value":normalized[i][j][k],"mirror_value":normalized[i][k][j]} for i in range(len(normalized)) for j in range(second) for k in range(j+1,third) if normalized[i][j][k] != normalized[i][k][j]]
        status="verified" if not mismatch else "fail"; why="Every declared final-index pair matches its swapped partner." if status=="verified" else "One or more declared final-index pairs differ after swapping."; details={"predicate":"tensor.rank3_last_indices_symmetric.v1","shape":[len(normalized),second,third],"mismatches":mismatch}
    body={"schema":"sov.simple_receipt","schema_version":"0.1.0","check":"tensor.rank3_last_indices_symmetric.v1","input":normalized,"status":status,"details":details}
    return {"receipt_id":_receipt_id(body),"status":status,"plain_status":_PUBLIC_WORDS[status],"what_i_checked":"Whether the final two indices of this finite rank-three tensor are symmetric.","why":why,"details":details,"next_action":"Inspect the reported component pairs or correct the declared tensor components.","scope":"Exact finite component equality only; this does not establish a physical tensor field, coordinate invariance, or theory-level result.","provenance":{"check":"tensor.rank3_last_indices_symmetric.v1","input":normalized,"receipt_schema":"sov.simple_receipt.v0.1"}}
