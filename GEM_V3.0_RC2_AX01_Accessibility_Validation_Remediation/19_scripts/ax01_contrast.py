"""AX01 task 11 (read-only): contrast of text/background colour pairs actually used. Background = innermost solid-filled shape below the text (bbox contains text centre), else slide background fill;
text over pictures or with no resolvable background is reported as MANUAL. Threshold: large text (>=18 pt) 3:1, else 4.5:1 (WCAG 2.2 SC 1.4.3 for text). Output: colour pairs, counts, ratios, slide lists (no text).
Usage: ax01_contrast.py <repo_root> <package_dir>"""
import sys, os, csv, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]
PAL = {'12171D': 'INK', 'BCACA7': 'BEIGE', '020202': 'BLACK', 'FFFFFF': 'WHITE'}
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]; c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]; return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
pairs = collections.defaultdict(lambda: dict(runs=0, slides=set(), large=0, small=0, docs=set())); manual = collections.Counter(); nonpal = collections.Counter()
def srgb(el, path):
    r = el.xpath(path, namespaces=ns); return r[0].upper() if r else None
for key, (label, path, lineage) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}")
    for n, part in enumerate(slide_order(z), 1):
        sr = etree.fromstring(z.read(part)); bg = srgb(sr, '//p:bg//a:srgbClr/@val') or None
        objs = list(walk(sr.find('.//p:spTree', ns)))
        for i, o in enumerate(objs):
            if o['kind'] != 'sp' or not o['has_text'] or o['hidden'] or o['cx'] is None: continue
            cxm, cym = o['x'] + o['cx'] / 2, o['y'] + o['cy'] / 2
            under = None; pic = False; unres = False
            own = srgb(o['el'], './p:spPr/a:solidFill/a:srgbClr/@val'); own_other = o['el'].xpath('./p:spPr/a:gradFill|./p:spPr/a:blipFill|./p:spPr/a:pattFill', namespaces=ns)
            for u in objs[:i]:
                if u['cx'] is None or not (u['x'] <= cxm <= u['x'] + u['cx'] and u['y'] <= cym <= u['y'] + u['cy']): continue
                if u['kind'] == 'pic': pic = True; under = None
                elif u['kind'] == 'sp':
                    f = srgb(u['el'], './p:spPr/a:solidFill/a:srgbClr/@val')
                    if f: under = f; pic = False
                    elif u['el'].xpath('./p:spPr/a:gradFill|./p:spPr/a:blipFill|./p:spPr/a:pattFill', namespaces=ns): under = None; pic = True
            bgc = own if own else ('' if (own_other or pic) else (under or bg))
            for r in o['el'].xpath('.//a:r', namespaces=ns):
                t = ''.join(r.xpath('a:t/text()', namespaces=ns)).strip()
                if not t: continue
                fc = srgb(r, './a:rPr/a:solidFill/a:srgbClr/@val'); sz = int(r.xpath('./a:rPr/@sz', namespaces=ns)[0]) / 100 if r.xpath('./a:rPr/@sz', namespaces=ns) else None
                if not fc or not bgc: manual[(label, 'text over picture / unresolved background' if not bgc else 'unresolved text colour')] += 1; continue
                for c in (fc, bgc):
                    if c not in PAL: nonpal[(label, c)] += 1
                d = pairs[(fc, bgc)]; d['runs'] += 1; d['slides'].add((label, n)); d['docs'].add(label)
                if sz and sz >= 18: d['large'] += 1
                else: d['small'] += 1
rows = []
for (fc, bgc), d in sorted(pairs.items(), key=lambda kv: -kv[1]['runs']):
    r = ratio(fc, bgc); nm = lambda c: PAL.get(c, '#' + c + ' (non-palette)')
    verdict_n = 'PASS' if r >= 4.5 else 'FAIL'; verdict_l = 'PASS' if r >= 3 else 'FAIL'
    rows.append([nm(fc), nm(bgc), f"{r:.2f}", d['runs'], d['small'], d['large'], verdict_n, verdict_l, ', '.join(sorted(d['docs'])), len(d['slides']),
                 'Governed pair fails both thresholds (4.5:1 and 3:1): GOVERNANCE / DESIGN ACCESSIBILITY REVIEW; may intentionally demonstrate a prohibited combination (Part A slide 33); no palette change inferred or made' if verdict_n == 'FAIL' and fc in PAL and bgc in PAL else ('Non-palette colour: observation only' if fc not in PAL or bgc not in PAL else '')])
for (label, why), c in manual.items(): rows.append(['(manual)', why, '', c, '', '', 'MANUAL', 'MANUAL', label, '', 'Cannot be measured statically; manual contrast check required'])
for (label, c), k in nonpal.items(): pass
H = ["Text colour", "Background colour", "Contrast ratio", "Runs", "Runs < 18 pt (needs 4.5:1)", "Runs >= 18 pt (needs 3:1)", "Normal-text verdict (4.5:1)", "Large-text verdict (3:1)", "Documents", "Slides", "Finding"]
csv.writer(open(f"{pkg}/09_AX01_Contrast_Assessment.csv", 'w', newline='', encoding='utf8')).writerows([H] + rows)
for r in rows: print(r[:10])
