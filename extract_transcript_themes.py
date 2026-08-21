from pathlib import Path
import re

src = Path('/home/ubuntu/projects/sov-e4e91854/geometric_unity.txt')
out = Path('/home/ubuntu/projects/sov-e4e91854/transcript_theme_windows.md')
lines = src.read_text(errors='replace').splitlines()
themes = {
    'GU core geometry': ['four manifold','14 manifold','bundle','metric','proto-manifold','observerse','torsion','connection','fiber'],
    'Physics and fields': ['quantum','classical','lrange','lagrang','gauge','gravity','fermion','boson','spin','chir','particle','standard model','generation'],
    'Mathematical structures': ['E8','E₈','octon','quaternion','Clifford','spinor','Hopf','Hecke','Riemann','zeta','modular','cohomology','Chern','Weyl','Cartan','Yang-Mills','Pati-Salam'],
    'Sovereign Engine links': ['engine','lattice','manifold','ledger','consensus','Monad','Logos','Merkaba','torus','swarm','node','proof','verification','AI','reason','language','DNA','material'],
    'Identity and social context': ['blacklist','gatekeep','academic','institution','peer review','outsider','conspiracy','DISC','purpose','goal','meaning','future','project'],
}
with out.open('w') as f:
    f.write('# Indexed transcript theme windows\n\n')
    for theme, terms in themes.items():
        hits=[]
        for i,line in enumerate(lines):
            if any(t.lower() in line.lower() for t in terms):
                hits.append(i)
        # merge nearby hits into windows
        windows=[]
        for i in hits:
            if not windows or i-windows[-1][-1] > 4:
                windows.append([i])
            else:
                windows[-1].append(i)
        f.write(f'## {theme}\n\n')
        for w in windows[:80]:
            start=max(0,w[0]-2); end=min(len(lines),w[-1]+3)
            f.write(f'### Lines {start+1}-{end}\n\n')
            for j in range(start,end):
                f.write(f'{j+1}: {lines[j]}\n')
            f.write('\n')
print(out)
