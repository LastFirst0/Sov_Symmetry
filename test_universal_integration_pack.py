import json
from pathlib import Path
from sov_evidence_geometry_core import evaluate_structural_claim

def test_shared_six_adapter_pack_matches_expected_outcomes():
    pack=json.loads((Path(__file__).parent/'data/universal_six_adapter_fixture_pack.json').read_text())
    assert len({case['check'] for case in pack['cases']}) == 6
    for case in pack['cases']:
        packet={'schema':'sov.structural_claim_packet','schema_version':'0.1.0','framework_id':pack['framework_id'],'claim_id':'test:'+case['id'],'claim_class':'structural','check':case['check'],'input':case['input']}
        if 'inverse' in case: packet['inverse']=case['inverse']
        assert evaluate_structural_claim(packet)['status'] == case['expected'], case['id']
