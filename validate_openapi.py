from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit(f'PyYAML unavailable: {exc}')

path = Path('/home/ubuntu/projects/sov-e4e91854/sovereign_engine_api.openapi.yaml')
data = yaml.safe_load(path.read_text())
errors = []
if data.get('openapi') != '3.0.3':
    errors.append('openapi version is not 3.0.3')
for key in ('info', 'servers', 'paths', 'components'):
    if key not in data:
        errors.append(f'missing top-level key: {key}')
paths = data.get('paths', {})
operation_ids = []
for route, item in paths.items():
    if not route.startswith('/v1') and route != '/manifolds':
        pass
    for method, operation in item.items():
        if method.lower() not in {'get','post','put','patch','delete','options','head','trace'}:
            continue
        op_id = operation.get('operationId')
        if not op_id:
            errors.append(f'{method.upper()} {route} missing operationId')
        operation_ids.append(op_id)
        if 'responses' not in operation:
            errors.append(f'{method.upper()} {route} missing responses')
if len(operation_ids) != len(set(operation_ids)):
    errors.append('duplicate operationId')
refs = []
def walk(value, where='root'):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == '$ref' and isinstance(child, str):
                refs.append((where, child))
            walk(child, f'{where}.{key}')
    elif isinstance(value, list):
        for i, child in enumerate(value):
            walk(child, f'{where}[{i}]')
for where, ref in refs:
    if ref.startswith('#/components/schemas/'):
        name = ref.rsplit('/', 1)[-1]
        if name not in data['components'].get('schemas', {}):
            errors.append(f'unresolved schema ref at {where}: {ref}')
    elif ref.startswith('#/components/responses/'):
        name = ref.rsplit('/', 1)[-1]
        if name not in data['components'].get('responses', {}):
            errors.append(f'unresolved response ref at {where}: {ref}')
print(f'openapi={data.get("openapi")} paths={len(paths)} operations={len(operation_ids)} schemas={len(data.get("components", {}).get("schemas", {}))}')
if errors:
    for error in errors:
        print('ERROR:', error)
    raise SystemExit(1)
print('VALID: required fields, operation IDs, and local component references passed')
