"""AX01 task 13: set the table header-row flag on tables classified as column-header tables (zip-level, anchored).
  inside the <p:graphicFrame> whose cNvPr has id=ID name=NAME:  <a:tblPr/>  ->  <a:tblPr firstRow="1"/>   (no table style is applied in these decks, so no restyling is expected)
Usage: ax01_apply_tables.py <src_pptx> <dst_pptx> <plan_json> <log_json>   plan: [[slide_part, shape_id, shape_name], ...]"""
import sys, re, json, zipfile, hashlib
src, dst, plan_p, logp = sys.argv[1:5]; plan = json.load(open(plan_p)); sha = lambda b: hashlib.sha256(b).hexdigest()
zin = zipfile.ZipFile(src); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}; new = dict(data); n = 0
for part, sid, name in plan:
    x = new[part].decode('utf8'); ms = [m for m in re.finditer(r'<p:graphicFrame>.*?</p:graphicFrame>', x, re.S) if re.search(r'<p:cNvPr id="%s" name="[^"]*"' % re.escape(sid), m.group(0).split('</p:nvGraphicFramePr>')[0])]
    assert len(ms) == 1, (part, sid, name, len(ms)); b = ms[0].group(0); assert b.count('<a:tblPr/>') == 1, (part, sid, 'tblPr anchor')
    x = x[:ms[0].start()] + b.replace('<a:tblPr/>', '<a:tblPr firstRow="1"/>', 1) + x[ms[0].end():]; new[part] = x.encode('utf8'); n += 1
with zipfile.ZipFile(dst, 'w') as zo:
    for i in zin.infolist():
        zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system; zo.writestr(zi, new[i.filename])
z2 = zipfile.ZipFile(dst); changed = sorted(k for k in data if z2.read(k) != data[k])
json.dump(dict(src_sha256=sha(open(src, 'rb').read()), dst_sha256=sha(open(dst, 'rb').read()), members_changed=changed, tables_flagged=n), open(logp, 'w'), indent=1); print(n, 'tables;', len(changed), 'members;', sha(open(dst, 'rb').read())[:16])
