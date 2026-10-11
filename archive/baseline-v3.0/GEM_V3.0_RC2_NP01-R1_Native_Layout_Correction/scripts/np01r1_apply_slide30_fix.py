"""NP01-R1: Part B slide 30 geometry-only correction as a CONTROLLED CANDIDATE COPY.
Zip-level exact attribute replacement (no python-pptx save, no re-serialization): every zip member other than ppt/slides/slide30.xml is copied
with its original bytes, order, compression and ZipInfo. Only two numeric attributes change inside slide30.xml:
  1. shape "Text 3" (token-excerpt box) <a:ext cy>   2112963 -> 2565400   (166.4 pt -> 202.0 pt)
  2. shape "Text 5" (paragraph below)    <a:off y>   +452437 EMU (+35.6 pt), keeping the existing 16 pt gap
Usage: np01r1_apply_slide30_fix.py <repo_root> <out_dir> <log_json>"""
import sys, os, re, json, zipfile, hashlib
root, outd, logp = sys.argv[1:4]
sha = lambda b: hashlib.sha256(b).hexdigest()
SRC = f"{root}/GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Digital Design System V3.0 — Part B — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx"
DST = f"{outd}/GEM Digital Design System V3.0 — Part B — RC2 — NP01-R1 CANDIDATE (UNAPPROVED).pptx"
EXPECT_SRC = "22802377eb73448ce3c9c7a0e9d2d3818195d19172f7c07470a415f03d975777"
PART = "ppt/slides/slide30.xml"; OLD_CY, NEW_CY = 2112963, 2565400; DELTA = NEW_CY - OLD_CY
assert sha(open(SRC, 'rb').read()) == EXPECT_SRC, "base candidate hash mismatch - stop"
zin = zipfile.ZipFile(SRC); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}
x = data[PART].decode('utf8')
def block(x, name):
    ms = [m for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S) if re.search(r'<p:cNvPr id="\d+" name="%s"/>' % re.escape(name), m.group(0))]
    assert len(ms) == 1, (name, len(ms)); return ms[0]
m3 = block(x, "Text 3"); b3 = m3.group(0)
old3 = f'<a:ext cx="4826000" cy="{OLD_CY}"/>'; assert b3.count(old3) == 1
new3 = b3.replace(old3, f'<a:ext cx="4826000" cy="{NEW_CY}"/>')
x2 = x[:m3.start()] + new3 + x[m3.end():]
m5 = block(x2, "Text 5"); b5 = m5.group(0)
off = re.findall(r'<a:off x="(\d+)" y="(\d+)"/>', b5); assert len(off) == 1
ox, oy = map(int, off[0]); old5 = f'<a:off x="{ox}" y="{oy}"/>'; assert b5.count(old5) == 1
new5 = b5.replace(old5, f'<a:off x="{ox}" y="{oy + DELTA}"/>')
x3 = x2[:m5.start()] + new5 + x2[m5.end():]
new = dict(data); new[PART] = x3.encode('utf8')
os.makedirs(outd, exist_ok=True)
with zipfile.ZipFile(DST, 'w') as zo:
    for i in zin.infolist():
        zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr
        zi.create_system = i.create_system; zi.comment = i.comment; zi.extra = i.extra
        zo.writestr(zi, new[i.filename])
z2 = zipfile.ZipFile(DST)
changed = [n for n in data if z2.read(n) != data[n]]
log = dict(source=SRC, source_sha256=EXPECT_SRC, output=DST, output_sha256=sha(open(DST, 'rb').read()), member_order_identical=[i.filename for i in zin.infolist()] == [i.filename for i in z2.infolist()],
           parts_changed=changed, slide30_sha256_before=sha(data[PART]), slide30_sha256_after=sha(new[PART]),
           edits=[dict(shape="Text 3", attribute="a:ext@cy", before=OLD_CY, after=NEW_CY, before_pt=OLD_CY / 12700, after_pt=NEW_CY / 12700),
                  dict(shape="Text 5", attribute="a:off@y", before=oy, after=oy + DELTA, before_pt=oy / 12700, after_pt=(oy + DELTA) / 12700)],
           delta_emu=DELTA, delta_pt=DELTA / 12700)
json.dump(log, open(logp, 'w'), indent=1, ensure_ascii=False); print(json.dumps(log, indent=1, ensure_ascii=False))
