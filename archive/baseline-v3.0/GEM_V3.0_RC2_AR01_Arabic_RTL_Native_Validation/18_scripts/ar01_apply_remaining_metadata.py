"""AR01 owner-decision-1: apply the ten remaining PowerPoint Arabic metadata/direction corrections as CONTROLLED CANDIDATE COPIES (zip-level; no python-pptx save, no re-serialisation).
Per paragraph (exact anchored single-hit edits inside the owning <p:sp>, located by shape name AND id):
  1. <a:pPr algn="X" indent="0" marL="0">        -> same + rtl="1"    (paragraph base direction RTL; algn untouched: it is a PHYSICAL left/right value)
  2. the single Arabic run's <a:rPr lang="en-US"  -> lang="ar-SA"      (endParaRPr left unchanged)
No text, run split, direction mark, manual space, font, size, tracking, bold, weight, alignment, colour or geometry change.
Part A: continues from the stage-1 AR01 candidate (slide 39 already corrected).  Part B: NEW AR01 candidate derived from the NP01-R1 candidate (slide-30 clipping fix must survive byte-identically).
Usage: ar01_apply_remaining_metadata.py <package_dir> <scratch_stage1_pptx> <partB_np01r1_pptx> <log_json>"""
import sys, os, re, json, zipfile, hashlib
pkg, a_src, b_src, logp = sys.argv[1:5]
sha = lambda b: hashlib.sha256(b).hexdigest()
OUTD = f"{pkg}/19_candidate_corrections"
A_DST = f"{OUTD}/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx"
B_DST = f"{OUTD}/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx"
A_EXPECT = "73712e1cf1a74ee23240cc674cf6af5939ca0bb2cf810b622f091f39df22c7a7"   # stage-1 AR01 candidate (slide 39 only)
B_EXPECT = "44145a44c4529db0c0c5d9f38a6d2881e3c5fa549ba21686f1b694699a874d01"   # NP01-R1 Part B candidate
# (part, shape name, shape id, algn)  -- each expected to occur exactly once
PLAN = {
 'A': [('ppt/slides/slide37.xml', 'Text 4', '6', 'r'), ('ppt/slides/slide38.xml', 'Text 4', '6', 'r'), ('ppt/slides/slide38.xml', 'Text 7', '9', 'r'), ('ppt/slides/slide38.xml', 'Text 8', '10', 'r'),
       ('ppt/slides/slide65.xml', 'Text 9', '12', 'r'), ('ppt/slides/slide66.xml', 'Text 6', '9', 'r'), ('ppt/slides/slide66.xml', 'Text 7', '11', 'r'), ('ppt/slides/slide66.xml', 'Text 10', '14', 'r'),
       ('ppt/slides/slide68.xml', 'Text 10', '14', 'r')],
 'B': [('ppt/slides/slide9.xml', 'Text 12', '14', 'l')]}
def build(src, expect, dst, plan, label):
    assert sha(open(src, 'rb').read()) == expect, f"{label}: base candidate hash mismatch - stop"
    zin = zipfile.ZipFile(src); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}; new = dict(data); edits = []
    for part, shape, sid, algn in plan:
        x = new[part].decode('utf8')
        ms = [m for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S) if re.search(r'<p:cNvPr id="%s" name="%s"/>' % (sid, re.escape(shape)), m.group(0))]
        assert len(ms) == 1, (label, part, shape, 'shape count', len(ms)); b = ms[0].group(0)
        assert b.count('<a:p>') == 1 and len(re.findall(r'<a:r>', b)) == 1, (label, part, shape, 'expected exactly 1 paragraph / 1 run')
        old_p = f'<a:pPr algn="{algn}" indent="0" marL="0">'; assert b.count(old_p) == 1, (label, part, shape, 'pPr anchor count', b.count(old_p))
        assert 'rtl=' not in b.split('<a:r>')[0], (label, part, shape, 'rtl already present')
        old_r = '<a:rPr lang="en-US"'; assert b.count(old_r) == 1, (label, part, shape, 'rPr anchor count', b.count(old_r))
        nb = b.replace(old_p, f'<a:pPr algn="{algn}" indent="0" marL="0" rtl="1">').replace(old_r, '<a:rPr lang="ar-SA"')
        assert len(nb) - len(b) == len(' rtl="1"') + 0 + (len('ar-SA') - len('en-US'))
        x = x[:ms[0].start()] + nb + x[ms[0].end():]; new[part] = x.encode('utf8')
        edits += [dict(deck=label, part=part, shape=shape, shape_id=sid, element='a:pPr', attribute='rtl', expected_source_occurrences=1, before='(absent)', after='1'),
                  dict(deck=label, part=part, shape=shape, shape_id=sid, element='a:rPr (Arabic run)', attribute='lang', expected_source_occurrences=1, before='en-US', after='ar-SA')]
    os.makedirs(OUTD, exist_ok=True)
    with zipfile.ZipFile(dst, 'w') as zo:
        for i in zin.infolist():
            zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system
            zo.writestr(zi, new[i.filename])
    z2 = zipfile.ZipFile(dst); changed = sorted(n for n in data if z2.read(n) != data[n])
    assert changed == sorted({p for p, *_ in plan}), (label, changed)
    return dict(source_sha256=expect, output=os.path.basename(dst), output_sha256=sha(open(dst, 'rb').read()), members_changed=changed, member_order_identical=[i.filename for i in zin.infolist()] == [i.filename for i in z2.infolist()],
                member_sha256_before={n: sha(data[n]) for n in changed}, member_sha256_after={n: sha(z2.read(n)) for n in changed}, attribute_edits=edits), data, z2
logA, dA, zA = build(a_src, A_EXPECT, A_DST, PLAN['A'], 'Part A')
logB, dB, zB = build(b_src, B_EXPECT, B_DST, PLAN['B'], 'Part B')
# NP01-R1 slide-30 clipping fix must survive byte-identically in the new Part B candidate
s30 = 'ppt/slides/slide30.xml'; assert zB.read(s30) == dB[s30]
x30 = zB.read(s30).decode('utf8')
logB['np01r1_slide30_preserved'] = dict(slide30_member_byte_identical=True, slide30_sha256=sha(dB[s30]))
log = dict(partA=logA, partB=logB); json.dump(log, open(logp, 'w'), indent=1, ensure_ascii=False); print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'attribute_edits'} for k, v in log.items()}, indent=1, ensure_ascii=False)); print('edits:', len(logA['attribute_edits']) + len(logB['attribute_edits']))
