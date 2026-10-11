"""AX01 task 15-17 static verification of AX01 candidates against their sources: (1) accessibility predicates before/after, (2) every paragraph's text hash, run languages, paragraph direction, font/size/tracking/bold unchanged,
(3) only expected members differ, (4) non-slide members byte-identical (incl. NP01-R1 slide 30), (5) no new fonts/colours. Usage: ax01_static_verify.py <repo_root> <package_dir>"""
import sys, os, re, csv, json, zipfile, hashlib, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]; out = f"{pkg}/21_candidate_corrections"; rows = []; res = {}
def preds(z):
    t = d = n = tb = 0; ph = 0
    for part in slide_order(z):
        objs = list(walk(etree.fromstring(z.read(part)).find('.//p:spTree', ns)))
        t += 0 if any(o['placeholder'] in ('title', 'ctrTitle') for o in objs) else 1
        n += sum(1 for o in objs if o['kind'] in ('sp', 'cxnSp') and not o['has_text'] and not o['descr'].strip() and not o['decorative'] and o['placeholder'] is None)
        d += sum(1 for o in objs if o['decorative']); tb += sum(1 for o in objs if o['kind'] == 'table' and o['el'].find('.//a:tblPr', ns).get('firstRow') != '1')
    return t, n, d, tb
def para_sig(z):
    sig = {}
    for part in slide_order(z):
        root_el = etree.fromstring(z.read(part)); k = 0
        for p in root_el.iterfind('.//a:p', ns):
            ppr = p.find('a:pPr', ns); runs = p.findall('a:r', ns)
            sig[(part, k)] = (hashlib.sha256(''.join(''.join(r.xpath('a:t/text()', namespaces=ns)) for r in runs).encode()).hexdigest(), tuple((r.find('a:rPr', ns).get('lang'), r.find('a:rPr', ns).get('sz'), r.find('a:rPr', ns).get('spc'), r.find('a:rPr', ns).get('b'), tuple(sorted((c.get('typeface') for c in r.find('a:rPr', ns) if etree.QName(c).localname in ('latin', 'ea', 'cs'))))) for r in runs if r.find('a:rPr', ns) is not None), dict(ppr.attrib) if ppr is not None else {}); k += 1
    return sig
for key, (label, path, lineage) in DECKS.items():
    src = zipfile.ZipFile(f"{root}/{path}"); cand = [f for f in os.listdir(out) if f.endswith('.pptx') and f"Part {label[-1]}" in f]; dst = zipfile.ZipFile(f"{out}/{cand[0]}")
    ps, pd = preds(src), preds(dst); sg, dg = para_sig(src), para_sig(dst)
    same_text_props = sg == dg; diff = [k for k in sg if sg[k] != dg.get(k)]
    changed = sorted(n for n in src.namelist() if src.read(n) != dst.read(n)); nonslide = [n for n in changed if not re.match(r'ppt/slides/slide\d+\.xml$', n)]
    fonts = lambda z: set(re.findall(r'typeface="([^"]+)"', ''.join(z.read(n).decode('utf8', 'ignore') for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n))))
    cols = lambda z: set(re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', ''.join(z.read(n).decode('utf8', 'ignore') for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n))))
    s30 = (src.read('ppt/slides/slide30.xml') == dst.read('ppt/slides/slide30.xml')) if label == 'Part B' else None
    rows.append([label, cand[0], 'slides without title placeholder %d -> %d' % (ps[0], pd[0]), 'non-text shapes without alt/decorative %d -> %d' % (ps[1], pd[1]), 'decorative-flagged objects %d -> %d' % (ps[2], pd[2]), 'tables without header flag %d -> %d' % (ps[3], pd[3]),
                 'paragraph texts/runs/langs/sizes/tracking/bold/fonts/direction identical: %s (%d paragraphs)' % (same_text_props, len(sg)), 'members changed: %d (non-slide members changed: %d)' % (len(changed), len(nonslide)), 'fonts added: %s' % (sorted(fonts(dst) - fonts(src)) or 'none'), 'colours added: %s' % (sorted(cols(dst) - cols(src)) or 'none'),
                 'NP01-R1 slide30.xml byte-identical: %s' % s30 if s30 is not None else ''])
    res[label] = dict(paragraph_diff=len(diff), nonslide_changed=nonslide)
    assert same_text_props and not nonslide and not (fonts(dst) - fonts(src)) and not (cols(dst) - cols(src)), (label, diff[:3], nonslide)
csv.writer(open(f"{pkg}/20_qa/ax01_static_verification.csv", 'w', newline='', encoding='utf8')).writerows([["Document", "Candidate", "Titles", "Alt/decorative", "Decorative flags", "Table headers", "Content preservation", "Members", "New fonts", "New colours", "NP01-R1 slide 30"]] + rows)
for r in rows: print(' | '.join(r[:10]))
