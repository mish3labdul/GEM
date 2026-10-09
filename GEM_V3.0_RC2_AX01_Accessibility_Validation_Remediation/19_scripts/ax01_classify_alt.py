"""AX01 task 6 (read-only): classify every non-text object without alt text / decorative flag; also pictures and quality notes.
Rules (documented, deterministic):
  R1 hairline rule      : non-text sp/cxnSp, min(cx,cy) <= 3 pt                               -> DECORATIVE (Cat A) unless the slide holds an unclassified visual (R4) -> then COMPLEX VISUAL (Cat B)
  R2 background panel   : non-text sp whose box contains the centre of >=1 text shape         -> BACKGROUND / ORNAMENT (Cat A, text carries the information)
  R3 large field        : non-text sp covering >= 60% of the slide area                       -> BACKGROUND / ORNAMENT (Cat A)
  R4 other shape        : any other non-text sp (swatch without inner text, ring, spark ...)  -> COMPLEX VISUAL / UNKNOWN (Cat B, content owner)
  P  picture w/o alt    : INFORMATIVE, alt text required                                      -> Cat B (content owner), never auto-generated
Usage: ax01_classify_alt.py <repo_root> <package_dir>"""
import sys, os, csv, json, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]; PT = 12700
reg, plan = [], collections.defaultdict(list)
for key, (label, path, lineage) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}"); pres = etree.fromstring(z.read('ppt/presentation.xml')).find('.//p:sldSz', ns); SW, SH = int(pres.get('cx')), int(pres.get('cy'))
    for n, part in enumerate(slide_order(z), 1):
        objs = list(walk(etree.fromstring(z.read(part)).find('.//p:spTree', ns)))
        texts = [o for o in objs if o['kind'] == 'sp' and o['has_text'] and o['cx'] is not None]
        cand = [o for o in objs if o['kind'] in ('sp', 'cxnSp') and not o['has_text'] and not o['descr'].strip() and not o['decorative'] and o['placeholder'] is None and o['cx'] is not None]
        cls = {}
        for o in cand:
            cx, cy = o['cx'], o['cy']
            if o['kind'] == 'cxnSp' or min(cx, cy) <= 3 * PT: cls[o['id']] = 'R1'
            elif cx * cy >= 0.6 * SW * SH: cls[o['id']] = 'R3'
            elif any(o['x'] <= t['x'] + t['cx'] / 2 <= o['x'] + cx and o['y'] <= t['y'] + t['cy'] / 2 <= o['y'] + cy for t in texts): cls[o['id']] = 'R2'
            else: cls[o['id']] = 'R4'
        complex_slide = any(v == 'R4' for v in cls.values())
        for o in objs:
            if o['kind'] == 'pic':
                state = 'decorative-flagged' if o['decorative'] else ('alt' if o['descr'].strip() else 'NO ALT')
                if state == 'NO ALT':
                    reg.append([label, n, o['id'], gl(o['name'], o['id']), 'pic', 'picture', 'INFORMATIVE', 'B', 'Alt text required; content owner to supply (product imagery / Arabic label artwork must not be described by guess)', 'no', 'none'])
                continue
            if o['id'] not in cls: continue
            r = cls[o['id']]
            if r == 'R1' and complex_slide: c, cat, act = 'COMPLEX VISUAL', 'B', 'Line on a slide that also holds an unclassified visual; may be a leader/diagram line; content owner to decide (not marked decorative)'
            elif r == 'R1': c, cat, act = 'DECORATIVE', 'A', 'Mark decorative (hairline divider/rule; no information carried)'
            elif r in ('R2',): c, cat, act = 'BACKGROUND / ORNAMENT or REDUNDANT WITH ADJACENT TEXT (inner text carries the information)', 'A', 'Mark decorative (panel/card backing; the text inside carries the information)'
            elif r == 'R3': c, cat, act = 'BACKGROUND / ORNAMENT', 'A', 'Mark decorative (large background field)'
            else: c, cat, act = 'COMPLEX VISUAL / UNKNOWN', 'B', 'Shape may be informative (swatch, device form, diagram element); requires content-owner classification; not marked decorative'
            reg.append([label, n, o['id'], gl(o['name'], o['id']), o['kind'], {'R1': 'hairline rule', 'R2': 'panel behind text', 'R3': 'large field', 'R4': 'other shape'}[r], c, cat, act, 'yes' if cat == 'A' else 'no', 'decorative' if cat == 'A' else 'none'])
            if cat == 'A': plan[label].append([part, o['id'], o['name']])
H = ["Document", "Slide", "Shape id", "Shape name", "Kind", "Geometry class", "Classification", "Safe-remediation category", "Recommended action", "Applied in AX01 candidate?", "Result flag"]
csv.writer(open(f"{pkg}/07_AX01_Alt_Text_Register.csv", 'w', newline='', encoding='utf8')).writerows([H] + reg)
json.dump(plan, open(f"{pkg}/local_only/raw/decorative_plan.json", 'w'))
c = collections.Counter((r[0], r[6], r[7]) for r in reg)
for k, v in sorted(c.items()): print(k, v)
