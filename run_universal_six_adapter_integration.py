from __future__ import annotations
import hashlib,json
from pathlib import Path
from sov_evidence_geometry_core import evaluate_structural_claim
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'tests/core_contract/data/universal_six_adapter_fixture_pack.json'
def main():
    pack=json.loads(PACK.read_text()); rows=[]
    for case in pack['cases']:
        packet={'schema':'sov.structural_claim_packet','schema_version':'0.1.0','framework_id':pack['framework_id'],'claim_id':'integration:'+case['id'],'claim_class':'structural','check':case['check'],'input':case['input']}
        if 'inverse' in case: packet['inverse']=case['inverse']
        result=evaluate_structural_claim(packet)
        actual=result['status']; ok=actual==case['expected']
        rows.append({'id':case['id'],'adapter':case['check'],'class':case['class'],'expected':case['expected'],'actual':actual,'pass':ok,'receipt_id':result.get('receipt',{}).get('receipt_id')})
    report={'schema':'sov.universal_adapter_integration_report','schema_version':'0.1.0','fixture_pack_sha256':hashlib.sha256(PACK.read_bytes()).hexdigest(),'adapter_count':len({r['adapter'] for r in rows}),'case_count':len(rows),'passed':sum(r['pass'] for r in rows),'failed':sum(not r['pass'] for r in rows),'rows':rows}
    print(json.dumps(report,indent=2,sort_keys=True))
    if report['failed']: raise SystemExit(1)
if __name__=='__main__': main()
