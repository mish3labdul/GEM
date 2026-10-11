"""AR01 PowerPoint metadata correction table / register (identifiers, hashes, lengths and attribute values only; no Arabic text).
  pre : ar01_build_metadata_register.py pre  <pkg> <D3_partA> <NP01R1_partB> <current_partA> <out_csv>      -> Task-1 table BEFORE editing (current = current Part A candidate, Part B = NP01-R1)
  post: ar01_build_metadata_register.py post <pkg> <D3_partA> <NP01R1_partB> <AR01_partA> <AR01_partB> <out_csv> -> final per-paragraph before/after register (baseline lineage vs AR01 candidates)"""
import sys, os, re, csv, zipfile, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from ar01_common import *
from lxml import etree
mode = sys.argv[1]
def paras(path):
    z = zipfile.ZipFile(path); out = {}
    for r in pptx_paragraphs(z):
        if r.get('is_picture') or r['kind'] != 'slides' or not AR.search(r['text']): continue
        p = r['paragraph']; ppr = p.find('a:pPr', ns); epr = p.find('a:endParaRPr', ns)
        runs = r['runs']; xf = p.xpath('ancestor::p:sp[1]/p:spPr/a:xfrm', namespaces=ns)
        geo = (xf[0].find('a:off', ns).attrib, xf[0].find('a:ext', ns).attrib) if xf else None
        lns = ppr.xpath('a:lnSpc/a:spcPts/@val', namespaces=ns) if ppr is not None else []
        out[(r['num'], r['shape_name'], r['shape_id'])] = dict(
            part=r['part'], rtl=(ppr.get('rtl') if ppr is not None else None), algn=(ppr.get('algn') if ppr is not None else None), lnSpc=(lns[0] if lns else None),
            run_lang='|'.join(sorted({x['lang'] or '(none)' for x in runs})), runs=len(runs),
            lang_ar='|'.join(sorted({x['lang'] or '(none)' for x in runs if AR.search(x['text'])})) or '(none)', lang_lat='|'.join(sorted({x['lang'] or '(none)' for x in runs if LAT.search(x['text']) and not AR.search(x['text'])})) or '(no separate Latin run)', latin_present=bool(LAT.search(r['text'])), cls=classify(r['text']),
            fam='|'.join(sorted({f"{x['latin']}/{x['ea']}/{x['cs']}" for x in runs})), sz='|'.join(sorted({str(x['sz']) for x in runs})), spc='|'.join(sorted({str(x['spc']) for x in runs})),
            b='|'.join(sorted({str(x['b']) for x in runs})), endpara_lang=(epr.get('lang') if epr is not None else None),
            text_sha=sha(r['text']), chars=len(r['text']), geo=(f"off={dict(geo[0])} ext={dict(geo[1])}" if geo else 'n/a'), slide_sha=hashlib.sha256(z.read(r['part'])).hexdigest())
    return out
def deck_label(n): return 'Part A' if n == 'A' else 'Part B'
if mode == 'pre':
    pkg, d3, b1, cur, outp = sys.argv[2:7]
    A, B, C = paras(d3), paras(cur), paras(b1)
    rows = []
    for d, src in (('Part A', B), ('Part B', C)):
        for k in sorted(src, key=lambda k: (k[0], k[1])):
            v = src[k]; mixed = v['latin_present']
            done = v['rtl'] == '1' and v['run_lang'] == 'ar-SA'
            rows.append([d, k[0], f"{k[1]} (id {k[2]})", 'MIXED Arabic+Latin' if mixed else ('Arabic + numerals/neutrals' if v['cls'] != 'ARABIC ONLY' else 'Arabic-only'),
                         v['rtl'] or '(absent = LTR)', '1', v['run_lang'], 'ar-SA', 'YES (single run, not fragmented)' if mixed else 'NO', 'LTR via bidi algorithm; no separate Latin run exists, so no run-level Latin language is applied' if mixed else 'n/a',
                         'NO', 'NO - already corrected (AR01 stage 1)' if done else 'YES'])
    w = csv.writer(open(outp, 'w', newline='')); w.writerow(['Document', 'Slide', 'Shape', 'Script content', 'Current paragraph direction (rtl)', 'Target paragraph direction (rtl)', 'Current Arabic-run language', 'Target Arabic-run language', 'Latin run present?', 'Latin-run target direction/language', 'Text changes required?', 'Needs correction now?']); w.writerows(rows)
    print(len(rows), 'paragraphs;', sum(1 for r in rows if r[-1] == 'YES'), 'need correction;', sum(1 for r in rows if r[-1] != 'YES'), 'already done')
    for r in rows: print(' | '.join(map(str, r)))
else:
    pkg, d3, b1, a_new, b_new, outp = sys.argv[2:8]
    base = {'Part A': paras(d3), 'Part B': paras(b1)}; new = {'Part A': paras(a_new), 'Part B': paras(b_new)}
    cols = ['Document', 'Slide', 'Shape', 'Shape ID', 'Corrected in', 'Script content', 'pPr rtl before', 'pPr rtl after', 'Arabic-run lang before', 'Arabic-run lang after', 'Latin run present', 'Latin-run lang before', 'Latin-run lang after', 'endParaRPr lang before', 'endParaRPr lang after',
            'Text SHA-256 before', 'Text SHA-256 after', 'Chars before', 'Chars after', 'Text identical', 'Font family before', 'Font family after', 'Size (sz) before', 'Size (sz) after', 'Tracking (spc) before', 'Tracking (spc) after',
            'Bold before', 'Bold after', 'Alignment (algn) before', 'Alignment (algn) after', 'Line spacing before', 'Line spacing after', 'Run count before', 'Run count after', 'Geometry identical', 'Slide XML SHA-256 before', 'Slide XML SHA-256 after', 'All non-intended attributes identical']
    rows = []; ok_all = True
    for d in ('Part A', 'Part B'):
        assert set(base[d]) == set(new[d]), (d, 'paragraph set differs')
        for k in sorted(new[d], key=lambda k: (k[0], k[1])):
            a, b = base[d][k], new[d][k]
            split = a['latin_present'] and b['runs'] == a['runs'] + 1   # slide 39 Text 8: the single mixed run is split into an Arabic run and a Latin run
            keep = all(a[f] == b[f] for f in ('text_sha', 'chars', 'fam', 'sz', 'spc', 'b', 'algn', 'lnSpc', 'geo', 'endpara_lang', 'cls')) and (a['runs'] == b['runs'] or split)
            ok_all &= keep and b['rtl'] == '1' and b['lang_ar'] == 'ar-SA' and (b['lang_lat'] == 'en-US' if split else True)
            rows.append([d, k[0], k[1], k[2], ('AR01 stage 1 (slide-39 mixed-run pass); Text 8 run split in the final owner decision' if k[1] == 'Text 8' else 'AR01 stage 1 (slide-39 mixed-run pass)') if (d == 'Part A' and k[0] == 39) else 'AR01 owner-decision-1 pass', ('MIXED Arabic+Latin (single run before; Arabic run + Latin run after)' if a['latin_present'] else 'Arabic-only' if a['cls'] == 'ARABIC ONLY' else 'Arabic + numerals/neutrals'),
                         a['rtl'] or '(absent)', b['rtl'], a['lang_ar'], b['lang_ar'], 'YES' if a['latin_present'] else 'NO', a['lang_lat'], b['lang_lat'], a['endpara_lang'], b['endpara_lang'], a['text_sha'], b['text_sha'], a['chars'], b['chars'], a['text_sha'] == b['text_sha'],
                         a['fam'], b['fam'], a['sz'], b['sz'], a['spc'], b['spc'], a['b'], b['b'], a['algn'], b['algn'], a['lnSpc'], b['lnSpc'], a['runs'], b['runs'], a['geo'] == b['geo'], a['slide_sha'], b['slide_sha'], keep])
    w = csv.writer(open(outp, 'w', newline='')); w.writerow(cols); w.writerows(rows)
    print(len(rows), 'rows; every paragraph rtl=1 + ar-SA with all other tracked attributes identical:', ok_all)
    assert ok_all
