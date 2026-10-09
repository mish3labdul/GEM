"""AX01 task 13: mark classified (Category A) shapes as decorative (zip-level, anchored; no other change).
  <p:cNvPr id=ID name=NAME/>  ->  <p:cNvPr id=ID name=NAME><a:extLst><a:ext uri="{C183D7F6-B498-43B3-948B-1728B52AA6E4}"><adec:decorative xmlns:adec="http://schemas.microsoft.com/office/drawing/2017/decorative" val="1"/></a:ext></a:extLst></p:cNvPr>
(the same form PowerPoint/python-generated pictures in these decks already use). Each target: exactly one source occurrence, no existing extLst, no existing descr.
Usage: ax01_apply_decorative.py <src_pptx> <dst_pptx> <plan_json> <log_json> [<only_slides comma list>]   plan: [[slide_part, shape_id, shape_name], ...]"""
import sys, re, json, zipfile, hashlib, html
src, dst, plan_p, logp = sys.argv[1:5]; only = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None
plan = json.load(open(plan_p)); sha = lambda b: hashlib.sha256(b).hexdigest()
if only: plan = [p for p in plan if re.search(r'slide(\d+)\.xml', p[0]).group(1) in only]
zin = zipfile.ZipFile(src); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}; new = dict(data); n = 0
DEC = '<a:extLst><a:ext uri="{C183D7F6-B498-43B3-948B-1728B52AA6E4}"><adec:decorative xmlns:adec="http://schemas.microsoft.com/office/drawing/2017/decorative" val="1"/></a:ext></a:extLst>'
for part, sid, name in plan:
    x = new[part].decode('utf8'); pat = re.compile(r'<p:cNvPr id="%s" name="([^"]*)"(/>|>.*?</p:cNvPr>)' % re.escape(sid), re.S); ms = list(pat.finditer(x)); assert len(ms) == 1, (part, sid, name, len(ms))
    m = ms[0]; assert html.unescape(m.group(1)) == name, (part, sid, 'name mismatch'); assert 'adec:decorative' not in m.group(0) and 'descr=' not in m.group(0)
    EXT = DEC[len('<a:extLst>'):-len('</a:extLst>')]
    if m.group(2) == '/>': rep = f'<p:cNvPr id="{sid}" name="{m.group(1)}">{DEC}</p:cNvPr>'
    else:
        assert m.group(2).count('</a:extLst></p:cNvPr>') == 1, (part, sid, 'unexpected cNvPr children')       # PowerPoint-saved shapes: append our ext to the existing extLst
        rep = m.group(0).replace('</a:extLst></p:cNvPr>', EXT + '</a:extLst></p:cNvPr>')
    x = x[:m.start()] + rep + x[m.end():]; new[part] = x.encode('utf8'); n += 1
with zipfile.ZipFile(dst, 'w') as zo:
    for i in zin.infolist():
        zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system; zo.writestr(zi, new[i.filename])
z2 = zipfile.ZipFile(dst); changed = sorted(k for k in data if z2.read(k) != data[k])
json.dump(dict(src_sha256=sha(open(src, 'rb').read()), dst_sha256=sha(open(dst, 'rb').read()), members_changed=changed, shapes_marked=n), open(logp, 'w'), indent=1); print(n, 'shapes;', len(changed), 'members;', sha(open(dst, 'rb').read())[:16])
