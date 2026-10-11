"""AR01 task 7/15 helper: build SCRATCH variants of Part A slide 39 to test paragraph-direction / alignment / language semantics natively.
Zip-level exact attribute edits only (no python-pptx save); every other member is raw-copied. Output stays in local_only/scratch (never committed).
Usage: ar01_make_variants.py <repo_root> <out_dir>"""
import sys, os, re, zipfile, hashlib, json
root, out = sys.argv[1:3]
SRC = f"{root}/GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/GEM Brand Guidelines V3.0 — Part A — RC2 — D3 CANDIDATE (UNAPPROVED).pptx"
BASE_SHA = "eca6b80ba6f301cf503b091821736f56c685e10d721c03a5579f9b238e1dc752"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert sha(open(SRC, 'rb').read()) == BASE_SHA, "base candidate hash mismatch"
PART = 'ppt/slides/slide39.xml'; SHAPES = ('Text 4', 'Text 8')
zin = zipfile.ZipFile(SRC); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}
# variant -> (add rtl?, new algn or None, set lang ar-SA?)
VARIANTS = {'V0_baseline': (False, None, False), 'V1_rtl_only': (True, None, False), 'V2_rtl_algn_l': (True, 'l', False), 'V3_rtl_plus_lang': (True, None, True), 'V4_lang_only': (False, None, True)}
os.makedirs(out, exist_ok=True); log = {}
for vn, (rtl, algn, lang) in VARIANTS.items():
    x = data[PART].decode('utf8'); n_edits = 0
    for shape in SHAPES:
        ms = [m for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S) if re.search(r'<p:cNvPr id="\d+" name="%s"/>' % re.escape(shape), m.group(0))]
        assert len(ms) == 1, (shape, len(ms)); b = ms[0].group(0); nb = b
        old_ppr = '<a:pPr algn="r" indent="0" marL="0">'; assert nb.count(old_ppr) == 1, (shape, 'pPr')
        new_ppr = '<a:pPr algn="%s" indent="0" marL="0"%s>' % (algn or 'r', ' rtl="1"' if rtl else '')
        nb = nb.replace(old_ppr, new_ppr); n_edits += int(old_ppr != new_ppr)
        if lang:
            assert nb.count('<a:rPr lang="en-US"') == 1, (shape, 'lang'); nb = nb.replace('<a:rPr lang="en-US"', '<a:rPr lang="ar-SA"'); n_edits += 1  # the Arabic run's rPr only; endParaRPr is left unchanged
        x = x[:ms[0].start()] + nb + x[ms[0].end():]
    new = dict(data); new[PART] = x.encode('utf8'); dst = f"{out}/AR01_A39_{vn}.pptx"
    with zipfile.ZipFile(dst, 'w') as zo:
        for i in zin.infolist():
            zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system
            zo.writestr(zi, new[i.filename])
    z2 = zipfile.ZipFile(dst); changed = [n for n in data if z2.read(n) != data[n]]
    log[vn] = dict(file=os.path.basename(dst), sha256=sha(open(dst, 'rb').read()), members_changed=changed, attribute_edits=n_edits)
json.dump(log, open(f"{out}/variants_log.json", 'w'), indent=1); print(json.dumps(log, indent=1))
