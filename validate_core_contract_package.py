import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

root = Path('/home/ubuntu/projects/sov-e4e91854')
core_schema = json.loads((root / 'schemas/sov.core.v0_1.schema.json').read_text(encoding='utf-8'))
quarantine_schema = json.loads((root / 'schemas/sov.research_quarantine.v0_1.schema.json').read_text(encoding='utf-8'))
fixture_schema = json.loads((root / 'schemas/sov.core_conformance.v0_1.schema.json').read_text(encoding='utf-8'))
fixture_pack = json.loads((root / 'fixtures/sov_core_v0_1_fixture_pack.json').read_text(encoding='utf-8'))
quarantine_example = json.loads((root / 'fixtures/research_quarantine_packet_example.json').read_text(encoding='utf-8'))

for name, schema in [('core', core_schema), ('quarantine', quarantine_schema), ('conformance', fixture_schema)]:
    Draft202012Validator.check_schema(schema)
    print(f'valid meta-schema: {name}')

fixture_validator = Draft202012Validator(fixture_schema, format_checker=FormatChecker())
core_validator = Draft202012Validator(core_schema, format_checker=FormatChecker())
quarantine_validator = Draft202012Validator(quarantine_schema, format_checker=FormatChecker())

assert fixture_pack['schema'] == 'sov.core.conformance-pack'
assert fixture_pack['schema_version'] == '0.1.0'
assert len(fixture_pack['fixtures']) == 17

for fixture in fixture_pack['fixtures']:
    errors = sorted(fixture_validator.iter_errors(fixture), key=lambda error: list(error.path))
    if errors:
        raise AssertionError(f"fixture schema failure {fixture['fixture_id']}: {errors[0].message}")
    record = fixture['input'].get('core_record')
    if record is not None and fixture['category'] == 'valid_object':
        errors = sorted(core_validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            raise AssertionError(f"core record failure {fixture['fixture_id']}: {errors[0].message}")

errors = sorted(quarantine_validator.iter_errors(quarantine_example), key=lambda error: list(error.path))
if errors:
    raise AssertionError(f'quarantine example failure: {errors[0].message}')

counts = {}
for fixture in fixture_pack['fixtures']:
    counts[fixture['category']] = counts.get(fixture['category'], 0) + 1

assert counts == {
    'valid_object': 8,
    'invalid_request': 4,
    'unverifiable_result': 2,
    'failed_predicate': 1,
    'tamper': 1,
    'determinism': 1,
}

print('conformance fixtures: 17')
print('category counts:', json.dumps(counts, sort_keys=True))
print('quarantine example: valid')
