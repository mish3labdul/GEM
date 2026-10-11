"""AX01 task 7 (read-only): classify every table. Header-row evidence: first row cells all non-empty AND first row differs from the body rows in at least one of fill colour, text colour, font size, capitalisation (all-caps), or is shorter on average (labels vs content).
Output holds identifiers/counts only. Usage: ax01_classify_tables.py <repo_root> <package_dir>"""
import sys, os, csv, json, zipfile, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]; rows_out = []; plan = collections.defaultdict(list)
def cell_feats(tc):
    t = text_of(tc).strip(); fills = tc.xpath('./a:tcPr/a:solidFill/a:srgbClr/@val', namespaces=ns); cols = tc.xpath('.//a:rPr/a:solidFill/a:srgbClr/@val', namespaces=ns); szs = tc.xpath('.//a:rPr/@sz', namespaces=ns); bs = tc.xpath('.//a:rPr/@b', namespaces=ns)
    return dict(text=t, n=len(t), caps=bool(t) and t.upper() == t and any(c.isalpha() for c in t), fill=fills[0] if fills else '', col=cols[0] if cols else '', sz=szs[0] if szs else '', b=bs[0] if bs else '')
for key, (label, path, lineage) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}")
    for n, part in enumerate(slide_order(z), 1):
        for o in walk(etree.fromstring(z.read(part)).find('.//p:spTree', ns)):
            if o['kind'] != 'table': continue
            tbl = o['el'].find('.//a:tbl', ns); pr = tbl.find('a:tblPr', ns); trs = tbl.findall('a:tr', ns); grid = [[cell_feats(c) for c in r.findall('a:tc', ns)] for r in trs]
            first, body = grid[0], [c for r in grid[1:] for c in r]
            merged = sum(1 for r in trs for c in r.findall('a:tc', ns) if c.get('gridSpan') or c.get('rowSpan') or c.get('hMerge') or c.get('vMerge'))
            flag = pr.get('firstRow') == '1'; style = pr.find('a:tableStyleId', ns) is not None
            if len(trs) < 2 or len(first) < 2:
                kind, ev = 'SINGLE-ROW / SINGLE-COLUMN LAYOUT TABLE', 'fewer than 2 rows or columns'
            else:
                nonempty = all(c['n'] > 0 for c in first)
                diff = []
                if body and len({c['fill'] for c in first}) == 1 and first[0]['fill'] != body[0]['fill'] and first[0]['fill']: diff.append('fill')
                if body and first[0]['col'] != body[0]['col']: diff.append('text colour')
                if body and first[0]['sz'] != body[0]['sz']: diff.append('size')
                if all(c['caps'] for c in first) and not all(c['caps'] for c in body[:len(first)]): diff.append('caps')
                short = body and sum(c['n'] for c in first) / len(first) < 0.6 * (sum(c['n'] for c in body) / max(1, len(body)))
                if nonempty and diff: kind, ev = 'COLUMN-HEADER ROW (distinct first row)', 'first row differs: ' + '+'.join(diff)
                elif nonempty and short and len(first) >= 3: kind, ev = 'COLUMN-HEADER ROW LIKELY (labels)', 'first row shorter labels over content columns'
                else: kind, ev = 'KEY/VALUE OR LIST TABLE (no distinct header row)', 'first row not distinguishable from body'
            cat = 'A' if kind.startswith('COLUMN-HEADER ROW') and not flag else ('already set' if flag else 'B')
            rows_out.append([label, n, o['id'], o['name'], len(trs), len(first), merged, sum(1 for r in grid for c in r if not c['text']), 'yes' if flag else 'no', 'yes' if style else 'no (explicit cell formatting only)', kind, ev, cat,
                             'Set firstRow=1 (no table style is applied, so no restyling expected)' if cat == 'A' else ('Header flag already set' if cat == 'already set' else 'Not a column-header table by evidence, or a layout table; content owner to decide (no header flag set)')])
            if cat == 'A': plan[label].append([part, o['id'], o['name']])
H = ["Document", "Slide", "Shape id", "Shape name", "Rows", "Columns", "Merged cells", "Empty cells", "firstRow flag set", "Table style applied", "Classification", "Evidence", "Safe-remediation category", "Recommended action"]
csv.writer(open(f"{pkg}/08_AX01_Table_Accessibility_Register.csv", 'w', newline='', encoding='utf8')).writerows([H] + rows_out); json.dump(plan, open(f"{pkg}/local_only/raw/table_plan.json", 'w'))
c = collections.Counter((r[0], r[10], r[12]) for r in rows_out)
for k, v in sorted(c.items()): print(k, v)
