"""AR01 structural QA (adapted from NP01-R1; slide 39) (read-only): member-level and attribute-level proof that only the two intended numeric attributes changed.
Usage: np01r1_structural_qa.py <before_pptx> <after_pptx> <out_json>"""
import sys, re, json, zipfile, hashlib
b, a, outp = sys.argv[1:4]
sha = lambda x: hashlib.sha256(x).hexdigest()
zb, za = zipfile.ZipFile(b), zipfile.ZipFile(a)
nb = [i.filename for i in zb.infolist()]; na = [i.filename for i in za.infolist()]
changed = [n for n in nb if zb.read(n) != za.read(n)]
meta_same = all((i.date_time, i.compress_type, i.external_attr) == (j.date_time, j.compress_type, j.external_attr) for i, j in zip(zb.infolist(), za.infolist()))
P = "ppt/slides/slide39.xml"; xb, xa = zb.read(P).decode('utf8'), za.read(P).decode('utf8')
tok = lambda x: re.findall(r'<[^>]+>|[^<]+', x)
tb, ta = tok(xb), tok(xa); diffs = []
assert len(tb) == len(ta), "token count differs - structure changed"
for i, (p, q) in enumerate(zip(tb, ta)):
    if p != q: diffs.append(dict(token_index=i, before=p, after=q))
texts_b, texts_a = re.findall(r'<a:t>([^<]*)</a:t>', xb), re.findall(r'<a:t>([^<]*)</a:t>', xa)
cnt = lambda pat: (len(re.findall(pat, xb)), len(re.findall(pat, xa)))
res = dict(before_sha256=sha(open(b, 'rb').read()), after_sha256=sha(open(a, 'rb').read()),
  member_count_before=len(nb), member_count_after=len(na), member_order_identical=nb == na, zipinfo_identical=meta_same,
  members_changed=changed, slides=len([n for n in na if re.match(r'ppt/slides/slide\d+\.xml$', n)]),
  notes_masters_layouts_themes_docprops_byte_identical=all(zb.read(n) == za.read(n) for n in nb if not n.startswith('ppt/slides/slide39.xml')),
  slide39_token_count=len(tb), slide39_attribute_level_differences=diffs,
  all_a_t_text_identical=texts_b == texts_a, a_t_count=len(texts_a),
  rPr_identical=re.findall(r'<a:rPr[^>]*>', xb) == re.findall(r'<a:rPr[^>]*>', xa), bodyPr_identical=re.findall(r'<a:bodyPr[^>]*>', xb) == re.findall(r'<a:bodyPr[^>]*>', xa),
  colours_identical=re.findall(r'srgbClr val="[^"]+"', xb) == re.findall(r'srgbClr val="[^"]+"', xa), typefaces_identical=re.findall(r'typeface="[^"]+"', xb) == re.findall(r'typeface="[^"]+"', xa),
  line_spacing_identical=re.findall(r'<a:spcPts val="\d+"/>', xb) == re.findall(r'<a:spcPts val="\d+"/>', xa), font_sizes_identical=re.findall(r'sz="\d+"', xb) == re.findall(r'sz="\d+"', xa),
  bold_flags_after=sorted(set(re.findall(r'\bb="([^"]+)"', xa))), bold_true_count_after=len(re.findall(r'\bb="(?:1|true|on)"', xa)))
json.dump(res, open(outp, 'w'), indent=1, ensure_ascii=False); print(json.dumps(res, indent=1, ensure_ascii=False))
