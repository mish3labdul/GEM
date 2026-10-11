"""AX01 task 4 (read-only): for every slide without a recognized title find the visible heading candidate (largest text, upper area). Raw table with text is LOCAL-ONLY (local_only/raw/title_candidates.csv).
Usage: ax01_title_candidates.py <repo_root> <package_dir>"""
import sys, os, csv, zipfile, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]; rows = []
for key, (label, path, lineage) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}"); order = slide_order(z)
    sw = None
    pres = etree.fromstring(z.read('ppt/presentation.xml')); sz_el = pres.find('.//p:sldSz', ns); H = int(sz_el.get('cy')); W = int(sz_el.get('cx'))
    for n, part in enumerate(order, 1):
        tree = etree.fromstring(z.read(part)).find('.//p:spTree', ns); objs = list(walk(tree))
        if any(o['placeholder'] in ('title', 'ctrTitle') for o in objs): continue
        cands = []
        for o in objs:
            if o['kind'] != 'sp' or not o['has_text'] or o['hidden']: continue
            szs = [int(x) for x in o['el'].xpath('.//a:rPr/@sz', namespaces=ns)]
            if not szs: continue
            cands.append((max(szs), o))
        top = sorted(cands, key=lambda c: (-c[0], c[1]['y'] or 0))[:3]
        for rank, (sz, o) in enumerate(top):
            txt = text_of(o['el'].find('./p:txBody', ns)).strip()
            rows.append([label, n, rank + 1, o['id'], o['name'], sz / 100, round((o['y'] or 0) / H, 3), round((o['x'] or 0) / W, 3), len(txt), hashlib.sha256(txt.encode()).hexdigest()[:12], 'Arabic' if o['arabic'] else '', txt[:90].replace('\n', ' | ')])
os.makedirs(f"{pkg}/local_only/raw", exist_ok=True)
csv.writer(open(f"{pkg}/local_only/raw/title_candidates.csv", 'w', newline='', encoding='utf8')).writerows([["Document", "Slide", "Rank", "Shape id", "Shape name", "Max font pt", "y fraction", "x fraction", "Text length", "Text sha12", "Arabic", "Text (local only)"]] + rows)
print(len(rows))
