"""AR01 Word native probe analysis (read-only). Usage: ar01_word_analyze.py <probe.tsv> <template.docx> [out.json]
Per paragraph (positions = horizontal position relative to text boundary): char count (Word vs source), script-class runs (A=Arabic, L=Latin, D=digit, N=neutral) and, from native per-character
horizontal positions, whether each same-class segment advances right-to-left (Arabic) or left-to-right (Latin). No text is emitted."""
import sys, os, re, json, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from ar01_common import *
tsv, docx = sys.argv[1:3]
rows = [l.rstrip('\n').split('\t') for l in open(tsv)]
P = {int(r[1]): r for r in rows if r[0] == 'P'}; X = collections.defaultdict(dict)
for r in rows:
    if r[0] == 'X': X[int(r[1])][int(r[2])] = float(r[4])  # text-boundary-relative reading (page-relative reading has sporadic outliers)
z = zipfile.ZipFile(docx); paras = [p for p in docx_paragraphs(z) if p['part'] == 'word/document.xml']
def cls(c):
    if AR.search(c): return 'A'
    if LAT.search(c): return 'L'
    if c.isdigit(): return 'D'
    return 'N'
out = []
for i in sorted(P):
    src = paras[i-1] if i-1 < len(paras) else None
    t = src['text'] if src else ''
    n_w = int(P[i][-1]); xs = X[i]
    segs = []; cur = None
    for j, c in enumerate(t, 1):
        k = cls(c)
        if k == 'N': continue
        if cur and cur[0] == k and j - cur[2] <= 3: cur[2] = j; cur[3].append(j)
        else:
            cur = [k, j, j, [j]]; segs.append(cur)
    res = []
    for k, a, b, idx in segs:
        pos = [xs[j] for j in idx if j in xs]
        if len(pos) < 2: res.append((k, len(pos), 'n/a')); continue
        dec = sum(1 for u, v in zip(pos, pos[1:]) if v < u); inc = sum(1 for u, v in zip(pos, pos[1:]) if v > u)
        res.append((k, len(pos), 'RTL' if dec > inc else 'LTR' if inc > dec else 'flat'))
    lx = [xs[j] for j, c in enumerate(t, 1) if cls(c) in 'LD' and j in xs]; ax = [xs[j] for j, c in enumerate(t, 1) if cls(c) == 'A' and j in xs]
    arr = 'n/a' if not (lx and ax) else ('Latin/digit block left of Arabic block' if max(lx) < min(ax) else 'Latin/digit block right of Arabic block' if min(lx) > max(ax) else 'interleaved')
    out.append(dict(block_arrangement=arr, para=i, native_chars=n_w, src_chars=len(t), src_chars_plus_mark=len(t)+1, align=P[i][2], lang=P[i][3], font=P[i][4], cs_font=P[i][5], size=P[i][6], bold=P[i][7], bold_bi=P[i][8], spacing=P[i][9],
                    src_bidi=src['bidi'] if src else None, src_jc=src['jc'] if src else None, fields=src['fields'] if src else None,
                    script_mix=''.join(sorted({s[0] for s in segs})), seg_direction=collections.Counter((s[0], s[2]) for s in res if s[2] != 'n/a').most_common(), min_x=min(xs.values()) if xs else None, max_x=max(xs.values()) if xs else None))
json.dump(out, open(sys.argv[3], 'w'), indent=1) if len(sys.argv) > 3 else None
for o in out: print({k: v for k, v in o.items() if k not in ('cs_font',)})
