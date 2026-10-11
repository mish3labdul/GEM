#!/usr/bin/env python3
"""Compare the derived token package with the values documented in Part B RC2 (deck tables) and with the CSS file.
Usage: audit_tokens.py <repo_root> [out.json]   (read-only)"""
import json, re, sys, os
from pptx import Presentation
root = os.path.abspath(sys.argv[1])
deck = Presentation(f'{root}/PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pptx')
tok = json.load(open(f'{root}/PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.json'))
css = open(f'{root}/PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.css', encoding='utf8').read()
def flat(o, p=''):
    if isinstance(o, dict):
        if '$value' in o: yield p, o; return
        for k, v in o.items():
            if k.startswith('$'): continue
            yield from flat(v, p + '.' + k if p else k)
T = dict(flat(tok))
def tables(slide_no):
    out = []
    for sh in deck.slides[slide_no - 1].shapes:
        if getattr(sh, 'has_table', False) and sh.has_table:
            out.append([[c.text.strip() for c in r.cells] for r in sh.table.rows])
    return out
R = {'checks': [], 'status_findings': [], 'css': {}}
def chk(name, doc, tokv, ok): R['checks'].append({'check': name, 'documented': doc, 'token': tokv, 'result': 'PASS' if ok else 'FAIL'})
# slide 10 latin type table
for row in tables(10)[0][1:]:
    name, sl, wt, trk, _ = row; size, lh = [x.strip() for x in sl.split('/')]
    ts = T.get(f'type.size.{name}', {}).get('$value'); tl = T.get(f'type.lineHeight.{name}', {}).get('$value'); tt = T.get(f'type.tracking.{name}', {}).get('$value')
    chk(f'B10 {name} size', size, ts, ts == f'{size}px'); chk(f'B10 {name} lineHeight', lh, tl, tl == f'{lh}px')
    norm = lambda v: str(v).replace('em', '') if v not in (None,) else None
    chk(f'B10 {name} tracking', trk, tt, tt is not None and float(norm(tt)) == float(trk.replace('em', '')))
    w = T.get(f'type.weight.{name}', {}).get('$value'); chk(f'B10 {name} weight', wt, w, str(w) == wt) if w is not None else R['checks'].append({'check': f'B10 {name} weight', 'documented': wt, 'token': 'no per-style weight token', 'result': 'INFO'})
# slide 12 arabic
for row in tables(12)[0][1:]:
    name, sl, wt = row; size, lh = [x.strip() for x in sl.split('/')]
    ts = T.get(f'type.size.{name}', {}).get('$value'); tl = T.get(f'type.lineHeight.{name}', {}).get('$value')
    chk(f'B12 {name} size', size, ts, ts == f'{size}px'); chk(f'B12 {name} lineHeight', lh, tl, tl == f'{lh}px')
# slide 14 breakpoints
for row in tables(14)[0][1:]:
    band, width = row[0].lower(), row[1]; lo = re.match(r'(\d+)', width).group(1)
    tv = T.get(f'layout.breakpoint.{band}', {}).get('$value'); chk(f'B14 breakpoint {band}', lo + 'px', tv, tv == lo + 'px')
# slide 17 motion
for row in tables(17)[0][1:]:
    nm, val = row[0].replace('*', '').strip(), row[1]
    key = {'duration-instant': 'motion.duration.instant', 'duration-hover': 'motion.duration.hover', 'duration-confirmation': 'motion.duration.confirmation', 'duration-modal': 'motion.duration.modal', 'duration-reveal': 'motion.duration.reveal', 'reveal-ring': 'motion.duration.revealRing', 'reveal-spark': 'motion.duration.revealSpark', 'reveal-quarter': 'motion.duration.revealQuarter', 'easing-out': 'motion.easing.out'}.get(nm)
    tv = T.get(key, {}).get('$value') if key else None
    d = val.split(' ')[0] if nm.startswith(('reveal', 'duration')) else val
    chk(f'B17 {nm}', val, tv, tv is not None and str(tv).replace(' ', '') == d.replace(' ', ''))
# slide 8 spacing
sp = [int(x) for x in re.findall(r'^\d+$', '\n'.join(sh.text_frame.text for sh in deck.slides[7].shapes if sh.has_text_frame), re.M)]
tsp = sorted(int(v['$value'].replace('px', '')) for k, v in T.items() if k.startswith('space.'))
chk('B8 spacing scale', sp, tsp, sorted(sp) == tsp)
# status findings: Arabic tokens that are APPROVED while Part B marks Arabic PENDING VALIDATION; line-height approved while size conditional
for k, v in T.items():
    st = v.get('status') or v.get('$extensions', {}).get('status')
    if k.startswith('type.lineHeight.arabic') and st == 'APPROVED': R['status_findings'].append((k, st, 'Arabic hierarchy is PENDING VALIDATION on Part B slide 12 (M01, VAL-07)'))
    if k.startswith('type.lineHeight.') and not 'arabic' in k:
        sz = T.get(k.replace('lineHeight', 'size'), {}); ss = sz.get('status') or sz.get('$extensions', {}).get('status')
        if st == 'APPROVED' and ss == 'CONDITIONAL': R['status_findings'].append((k, st, f'paired size token is {ss}'))
# css vs json: every json token represented?
names = set(re.findall(r'--gem-([A-Za-z0-9_-]+)\s*:', css)); R['css']['custom_properties'] = len(names)
R['css']['reduced_motion_block'] = bool(re.search(r'prefers-reduced-motion\s*:\s*reduce', css))
R['css']['raw_hex_outside_foundation'] = sorted(set(re.findall(r'#[0-9a-fA-F]{6}', css)))
R['token_count'] = len(T)
R['summary'] = {k: sum(1 for c in R['checks'] if c['result'] == k) for k in ('PASS', 'FAIL', 'INFO')}
out = sys.argv[2] if len(sys.argv) > 2 else None
if out: json.dump(R, open(out, 'w'), indent=1, ensure_ascii=False)
print(R['summary'], 'tokens', R['token_count'], R['css'])
for c in R['checks']:
    if c['result'] != 'PASS': print(c)
print(len(R['status_findings']), 'status findings'); [print(' ', s) for s in R['status_findings'][:30]]
