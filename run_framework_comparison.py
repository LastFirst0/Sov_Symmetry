import json
from sov_evidence_geometry_core import evaluate_structural_claim
frameworks=[
    "framework:geometric-unity",
    "framework:causal-set",
    "framework:exceptional-algebra",
    "framework:amplitudes-twistor",
    "framework:noncommutative-geometry",
    "framework:holographic-qec",
    "framework:custom-research",
]
rows=[]
for framework_id in frameworks:
    packet={"schema":"sov.structural_claim_packet","schema_version":"0.1.0","framework_id":framework_id,"claim_id":"claim:shared-symmetric-relation-matrix","claim_class":"structural","check":"matrix.symmetric.v1","input":[[1,2],[2,4]]}
    result=evaluate_structural_claim(packet)
    rows.append({"framework_id":framework_id,"status":result["status"],"receipt_id":result["receipt"]["receipt_id"],"evaluation_scope":result["scope"]})
assert len({row["receipt_id"] for row in rows}) == 1
assert {row["status"] for row in rows} == {"verified"}
print(json.dumps({"scenario":"same declared structural claim, different provenance labels","framework_count":len(rows),"comparative_rows":rows,"conclusion":"All labels produced the same result and receipt ID; framework_id is provenance only."},indent=2,sort_keys=True))
