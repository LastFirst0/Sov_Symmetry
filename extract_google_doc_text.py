import json
from pathlib import Path

source = Path('/home/ubuntu/projects/sov-e4e91854/google_architecture_formal_verification_report.json')
target = Path('/home/ubuntu/projects/sov-e4e91854/google_architecture_formal_verification_report.txt')

document = json.loads(source.read_text(encoding='utf-8'))
chunks = []

def walk(node):
    if isinstance(node, dict):
        text_run = node.get('textRun')
        if isinstance(text_run, dict) and isinstance(text_run.get('content'), str):
            chunks.append(text_run['content'])
        for value in node.values():
            walk(value)
    elif isinstance(node, list):
        for item in node:
            walk(item)

walk(document)
target.write_text(''.join(chunks), encoding='utf-8')
print(target)
