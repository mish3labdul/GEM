"""AX01 tasks 4-5 (read-only): title remediation register + reading-order register. Heading text never enters committed files (shape ids, sizes, lengths and hashes only).
Title plan (Category A) is limited to slides whose visible heading is unambiguous: Part D (24: the 43.5 pt heading at y~0.121, else the single display statement), Part A slide 1 and Part C slide 1 (cover headings).
Everything else is classified (B/C/D/E) with a recommended option and is NOT applied. Usage: ax01_titles_reading.py <repo_root> <package_dir>"""
import sys, os, csv, json, zipfile, hashlib, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]; T, R = [], []; plan = collections.defaultdict(list)
COVER = set()   # cover headings (Part A slide 1, Part C slide 1) were piloted natively: title mapping moved the heading up ~0.8 pt (7 XML variants, all identical shift) -> NOT applied, see COVER_HELD
COVER_HELD = {('Part A', 1), ('Part C', 1)}
for key, (label, path, lineage) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}"); pres = etree.fromstring(z.read('ppt/presentation.xml')).find('.//p:sldSz', ns); SW, SH = int(pres.get('cx')), int(pres.get('cy'))
    for n, part in enumerate(slide_order(z), 1):
        objs = list(walk(etree.fromstring(z.read(part)).find('.//p:spTree', ns))); texts = [o for o in objs if o['kind'] == 'sp' and o['has_text'] and not o['hidden'] and o['cx'] is not None]
        title = [o for o in objs if o['placeholder'] in ('title', 'ctrTitle')]
        arabic = any(o['arabic'] for o in objs)
        szof = lambda o: max([int(x) for x in o['el'].xpath('.//a:rPr/@sz', namespaces=ns)] or [0]) / 100
        # ---------------- titles
        if not title:
            heading = None; klass = None; act = ''
            top = sorted([o for o in texts if szof(o)], key=lambda o: (-szof(o), o['y']))
            if label == 'Part D':
                h = [o for o in texts if abs(szof(o) - 43.5) < 0.01 and abs(o['y'] / SH - 0.121) < 0.01]
                heading = h[0] if h else (top[0] if top else None)
                klass, act = 'A. Visible heading exists but is not structurally recognized', 'Map the existing heading shape to a title placeholder (no visible text added)'
            elif (label, n) in COVER_HELD:
                heading = top[0]; klass, act = 'A. Visible heading exists but is not structurally recognized', 'CONTENT / GOVERNANCE DECISION REQUIRED: the tested title mapping shifts the heading about 0.8 pt; not applied, no compensating geometry or hidden title (visible layout authoritative)'
            else:
                eyebrow = [o for o in texts if szof(o) <= 12 and o['y'] / SH < 0.12]
                heading = top[0] if top else None
                if arabic: klass, act = 'E. Title structure requires governance/content decision', 'Bilingual/Arabic slide: structural title (language, order) is a content/governance decision (S07 governs wayfinding and does not resolve it); not changed'
                elif n == 80 and label == 'Part A': klass, act = 'C. Intentional closing/visual slide; hidden title may be appropriate', 'Content owner to approve a concise title (e.g. derived from the closing tagline); not added'
                elif label == 'Part C' and n in (10, 14): klass, act = 'D. Section/colour specimen slide needing a concise accessibility title', 'Content owner to approve a title derived from the slide label; not added'
                else: klass, act = 'E. Title structure requires governance/content decision', 'Slide has a small label (eyebrow) and several parallel statements; whether the label or a new concise title should become the title is a content decision; not changed'
            applied = label == 'Part D' or (label, n) in COVER
            if applied and heading: plan[label].append([part, heading['id'], heading['name']])
            txt = ''.join(heading['el'].xpath('.//a:t/text()', namespaces=ns)).strip() if heading else ''
            T.append([label, n, os.path.basename(part), 'shape id %s (%s), %.1f pt, y=%.3f, %d chars, sha12 %s' % (heading['id'], gl(heading['name'], heading['id']), szof(heading), heading['y'] / SH, len(txt), hashlib.sha256(txt.encode()).hexdigest()[:12]) if heading else 'none found', 'none (no title placeholder)', klass, act, 'no', 'APPLIED (title placeholder mapped)' if applied and heading else 'NOT APPLIED (' + ('visible shift measured natively; owner decision' if (label, n) in COVER_HELD else 'content owner / governance') + ')'])
        # ---------------- reading order
        idx = {o['id']: i for i, o in enumerate(objs)}
        rtl = arabic
        vis = sorted(texts, key=lambda o: (round(o['y'] / (0.05 * SH)), -o['x'] if rtl else o['x']))
        zs = [o['id'] for o in texts]; vs = [o['id'] for o in vis]; pos = {i: k for k, i in enumerate(vs)}
        inv = sum(1 for a in range(len(zs)) for b in range(a + 1, len(zs)) if pos[zs[a]] > pos[zs[b]])
        tfirst = '' if not title else ('title first among text shapes' if texts and texts[0]['id'] == title[0]['id'] else 'title NOT first among text shapes')
        if arabic: klass, cat = 'MANUAL TEST REQUIRED (Arabic/bilingual: logical order to be confirmed with a screen reader; AR01 logical-order model preserved)', 'D'
        elif inv == 0 and tfirst != 'title NOT first among text shapes': klass, cat = 'PASS (static: z-order matches top-to-bottom, left-to-right)', 'none'
        else: klass, cat = 'MANUAL / ASSISTIVE-TECH REVIEW REQUIRED (heuristic flag: z-order differs from top-to-bottom, left-to-right text order; PowerPoint object order affects stacking, so no reordering was applied)', 'B'
        R.append([label, n, os.path.basename(part), len(texts), 'yes' if title else 'no', tfirst, inv, 'Arabic' if arabic else '', klass, cat, 'no'])
H1 = ["Document", "Slide", "Part", "Heading candidate (identifiers only)", "Current structural title", "Classification", "Recommended action", "Content invention required?", "Result"]
csv.writer(open(f"{pkg}/05_AX01_Title_Remediation_Register.csv", 'w', newline='', encoding='utf8')).writerows([H1] + [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], 'NO' if r[5][0] == 'A' else 'YES — a title would have to be chosen by the content owner', r[8]] for r in T])
H2 = ["Document", "Slide", "Part", "Text shapes", "Title placeholder", "Title position", "z-order vs visual-order inversions (text shapes)", "Arabic content", "Classification", "Safe-remediation category", "Applied in AX01 candidate?"]
csv.writer(open(f"{pkg}/06_AX01_Reading_Order_Register.csv", 'w', newline='', encoding='utf8')).writerows([H2] + R)
json.dump(plan, open(f"{pkg}/local_only/raw/title_plan.json", 'w'))
print('title rows', len(T), collections.Counter((r[0], r[8][:7]) for r in T)); print(collections.Counter((r[0], r[8][:12]) for r in R))
