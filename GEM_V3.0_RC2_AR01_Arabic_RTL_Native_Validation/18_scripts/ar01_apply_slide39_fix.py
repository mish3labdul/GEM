"""AR01 task 15: Part A slide 39 technical correction as a CONTROLLED CANDIDATE COPY (zip-level, no python-pptx save, no re-serialization).
For the two Arabic paragraphs on slide 39 (shapes 'Text 4' and 'Text 8'):
  1. <a:pPr algn="r" indent="0" marL="0">           -> same + rtl="1"         (paragraph base direction RTL; alignment value unchanged: algn is physical)
  2. the Arabic run's <a:rPr lang="en-US" ...>        -> lang="ar-SA"            (run language; endParaRPr left unchanged)
No text, no run split, no direction marks, no font/size/spacing/colour/geometry change. Every other zip member is raw-copied (order, compression, ZipInfo).
Usage: ar01_apply_slide39_fix.py <repo_root> <out_dir> <log_json>"""
import sys, os, re, json, zipfile, hashlib
root, outd, logp = sys.argv[1:4]
sha = lambda b: hashlib.sha256(b).hexdigest()
SRC = f"{root}/GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/GEM Brand Guidelines V3.0 — Part A — RC2 — D3 CANDIDATE (UNAPPROVED).pptx"
DST = f"{outd}/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx"
EXPECT = "eca6b80ba6f301cf503b091821736f56c685e10d721c03a5579f9b238e1dc752"
PART = 'ppt/slides/slide39.xml'; SHAPES = ('Text 4', 'Text 8')
assert sha(open(SRC, 'rb').read()) == EXPECT, "base candidate hash mismatch - stop"
zin = zipfile.ZipFile(SRC); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}
x = data[PART].decode('utf8'); edits = []
for shape in SHAPES:
    ms = [m for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S) if re.search(r'<p:cNvPr id="\d+" name="%s"/>' % re.escape(shape), m.group(0))]
    assert len(ms) == 1, (shape, len(ms)); b = ms[0].group(0)
    old_p = '<a:pPr algn="r" indent="0" marL="0">'; assert b.count(old_p) == 1, (shape, 'pPr')
    old_r = '<a:rPr lang="en-US"'; assert b.count(old_r) == 1, (shape, 'rPr')
    nb = b.replace(old_p, '<a:pPr algn="r" indent="0" marL="0" rtl="1">').replace(old_r, '<a:rPr lang="ar-SA"')
    x = x[:ms[0].start()] + nb + x[ms[0].end():]
    edits += [dict(shape=shape, element='a:pPr', attribute='rtl', before='(absent)', after='1'), dict(shape=shape, element='a:rPr (Arabic run)', attribute='lang', before='en-US', after='ar-SA')]
new = dict(data); new[PART] = x.encode('utf8'); os.makedirs(outd, exist_ok=True)
with zipfile.ZipFile(DST, 'w') as zo:
    for i in zin.infolist():
        zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system
        zo.writestr(zi, new[i.filename])
z2 = zipfile.ZipFile(DST); changed = [n for n in data if z2.read(n) != data[n]]
log = dict(source_sha256=EXPECT, output=os.path.basename(DST), output_sha256=sha(open(DST, 'rb').read()), members_changed=changed, member_order_identical=[i.filename for i in zin.infolist()] == [i.filename for i in z2.infolist()],
           slide39_sha256_before=sha(data[PART]), slide39_sha256_after=sha(new[PART]), attribute_edits=edits)
json.dump(log, open(logp, 'w'), indent=1, ensure_ascii=False); print(json.dumps(log, indent=1, ensure_ascii=False))
