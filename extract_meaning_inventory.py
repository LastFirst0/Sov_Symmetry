from __future__ import annotations
import json, re
from pathlib import Path

TRANSCRIPT = Path('/home/ubuntu/projects/sov-e4e91854/geometric_unity.txt')
ANALYSIS = Path('/home/ubuntu/projects/sov-e4e91854/geometric_unity_analysis.txt')
REPO = Path('/home/ubuntu/sovereign_engine')
OUT = Path('/home/ubuntu/projects/sov-e4e91854/meaning_inventory.json')

files = {'transcript': TRANSCRIPT.read_text(errors='replace'), 'analysis': ANALYSIS.read_text(errors='replace')}
for p in sorted(REPO.glob('**/*')):
    if p.is_file() and '.git' not in p.parts and p.suffix.lower() in {'.md','.txt','.py','.rs','.lean','.toml','.yaml','.yml','.json'}:
        try:
            files[str(p.relative_to(REPO))] = p.read_text(errors='replace')
        except Exception:
            pass

all_text = '\n'.join(files.values())
patterns = {
    'equation_like': r'(?im)^.{0,240}(?:=|→|↔|⟷|∝|∈|⊂|\+|−|×|/|\^|\\frac|\\sum|\\int|\\partial|dim|Spin|SU\d|SO\d|E8|E₈|\bq\b|\bR\b|\bF\b|\bG\b|\bH\b|\bT\b).{0,240}$',
    'dimension_and_constant': r'(?i)\b(?:\d+(?:\.\d+)?|\d+\s*[×x]\s*\d+|\d+\s*(?:d|dim|dimensions|manifold|roots|generations|nodes|offices|levels|degrees|hours|months|years))\b',
    'capitalized_terms': r'\b(?:[A-Z][A-Za-z0-9₀-₉-]*(?:\s+[A-Z][A-Za-z0-9₀-₉-]*){0,4})\b',
    'symbolic_terms': r'(?<![A-Za-z])(?:[A-Za-z][A-Za-z0-9_]*(?:_[A-Za-z0-9]+)?|[A-Z][A-Z0-9]{1,8})(?![A-Za-z])',
}
result = {
    'source_stats': {k: {'chars': len(v), 'lines': v.count('\n')+1, 'words': len(v.split())} for k,v in files.items()},
    'matches': {}
}
for name, pattern in patterns.items():
    vals = set()
    for text in files.values():
        vals.update(m.group(0).strip() for m in re.finditer(pattern, text) if m.group(0).strip())
    result['matches'][name] = sorted(vals, key=lambda x: (x.lower(), x))

# Context windows for high-value anchors in the supplied sources.
anchors = ['four manifold','14 manifold','bundle','metric','torsion','Spin(7)','Pati-Salam','three generations','gamma','quantum','classical','E8','144,000','Merkaba','Monad',' Logos','ledger','consensus','observerse','proto-manifold','double copy','Hecke','Riemann','Sedenion','Leech','Hopf','cymatic']
contexts = []
for source in ('transcript','analysis'):
    text = files[source]
    lines = text.splitlines()
    for i,line in enumerate(lines):
        if any(a.lower() in line.lower() for a in anchors):
            contexts.append({'source': source, 'line': i+1, 'text': line.strip()})
result['anchor_contexts'] = contexts
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps({'sources': len(files), 'stats': result['source_stats'], 'output': str(OUT)}, ensure_ascii=False, indent=2))
