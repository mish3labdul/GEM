"""AR01 PDF check (adapted from NP01-R1) (read-only): compare the LibreOffice renders of the ODI01-R1 candidate (before) and the NP01-R1 candidate (after), page by page,
by word text and word bounding boxes (pdftotext -bbox-layout), plus the delivered ODI01-R1 PDF for text parity.
Usage: np01r1_pdf_compare.py <before.pdf> <after.pdf> <odi01_delivered.pdf> <out_json>"""
import sys, re, json, subprocess
bp, ap, dp, outp = sys.argv[1:5]
def pages(pdf):
    x = subprocess.run(['pdftotext', '-bbox-layout', pdf, '-'], capture_output=True, text=True).stdout
    out = []
    for pg in re.split(r'<page ', x)[1:]:
        out.append([(float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)) for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pg)])
    return out
def text(pdf): return [re.sub(r'\s+', ' ', t).strip() for t in subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f') if t.strip()]
B, A = pages(bp), pages(ap)
info = lambda p: subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout
res = dict(pages_before=len(B), pages_after=len(A), tagged_after=bool(re.search(r'Tagged:\s+yes', info(ap))), tagged_before=bool(re.search(r'Tagged:\s+yes', info(bp))), tagged_delivered=bool(re.search(r'Tagged:\s+yes', info(dp))), producer_after=re.search(r'Producer:\s+(.*)', info(ap)).group(1).strip(), producer_delivered=re.search(r'Producer:\s+(.*)', info(dp)).group(1).strip())
res['pages_with_any_difference'] = []; res['pages_text_identical'] = []
for i, (pb, pa) in enumerate(zip(B, A), 1):
    same_text = [w[4] for w in pb] == [w[4] for w in pa]
    moved = [(w[4], round(v[1] - w[1], 1)) for w, v in zip(pb, pa) if same_text and (abs(v[1] - w[1]) > 0.05 or abs(v[0] - w[0]) > 0.05 or abs(v[2] - w[2]) > 0.05 or abs(v[3] - w[3]) > 0.05)]
    if not same_text or moved: res['pages_with_any_difference'].append(dict(page=i, text_identical=same_text, words_moved=len(moved), dy_values=sorted({m[1] for m in moved}), sample=[m[0] for m in moved][:30]))
    if same_text: res['pages_text_identical'].append(i)
tb, ta, td = text(bp), text(ap), text(dp)
res['text_before_vs_after_all_pages_identical'] = tb == ta
res['rerender_before_vs_delivered_D3_PartA_pdf_text_identical'] = tb == td
res['pages_delivered'] = len(td)
ns = lambda L: [re.sub(r'\s+', '', x) for x in L]
res['rerender_before_vs_delivered_D3_PartA_pdf_text_identical_ignoring_all_whitespace'] = ns(tb) == ns(td)
res['pages_where_whitespace_stripped_text_differs_from_delivered'] = [i + 1 for i, (x, y) in enumerate(zip(ns(tb), ns(td))) if x != y]
msk = lambda L: [sorted(re.sub(r'\s+', '', x)) for x in L]
res['rerender_before_vs_delivered_page_character_multisets_identical'] = msk(tb) == msk(td)
res['pages_where_character_multiset_differs_from_delivered'] = [i + 1 for i, (x, y) in enumerate(zip(msk(tb), msk(td))) if x != y]
res['note_reference'] = 'In AR01 the third argument (delivered PDF) is the D3 Part A candidate PDF; the key names say D3_PartA for that reason.'
res['note_whitespace'] = 'pdftotext splits letter-spaced capitals differently between two LibreOffice runs (e.g. OVERVIEW vs OV ERV I EW); the like-for-like comparison is before-rerender vs after-rerender with identical settings.'
json.dump(res, open(outp, 'w'), indent=1, ensure_ascii=False); print(json.dumps(res, indent=1, ensure_ascii=False))
