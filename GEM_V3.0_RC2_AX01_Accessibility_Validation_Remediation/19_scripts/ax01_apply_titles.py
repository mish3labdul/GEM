"""AX01 task 13: map an EXISTING visible heading shape to a title placeholder (zip-level, anchored; no run/paragraph/geometry change).
  <p:cNvPr .../><p:cNvSpPr .../><p:nvPr/>   ->   same with <p:nvPr><p:ph type="title"/></p:nvPr>  (cNvPr may carry an extLst, as in the PowerPoint-saved Part D)
Expectations per edit: shape found exactly once by id+name, nvPr empty, slide has no existing title placeholder, source part member only changed.
Usage: ax01_apply_titles.py <src_pptx> <dst_pptx> <plan_json> <log_json>   plan: [[slide_part, shape_id, shape_name], ...]"""
import sys, re, json, zipfile, hashlib, html
src, dst, plan_p, logp = sys.argv[1:5]; plan = json.load(open(plan_p)); sha = lambda b: hashlib.sha256(b).hexdigest()
zin = zipfile.ZipFile(src); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}; new = dict(data); edits = []
for part, sid, name in plan:
    x = new[part].decode('utf8')
    assert not re.search(r'<p:ph type="(title|ctrTitle)"', x), (part, 'title placeholder already present')
    pat = re.compile(r'(<p:cNvPr id="%s" name="([^"]*)"(?:/>|>.*?</p:cNvPr>)<p:cNvSpPr(?:/>| [^>]*/>|>(?:(?!</p:cNvSpPr>).)*</p:cNvSpPr>))<p:nvPr/>' % re.escape(sid), re.S); ms = pat.findall(x); assert len(ms) == 1, (part, sid, name, len(ms))
    assert html.unescape(ms[0][1]) == name, (part, sid, 'name mismatch')   # names can hold line breaks / ampersands (XML-escaped)
    x = pat.sub(lambda m: m.group(1) + '<p:nvPr><p:ph type="title"/></p:nvPr>', x, count=1); new[part] = x.encode('utf8')
    # Inheritance guard: as a title placeholder the shape inherits the master titleStyle where it sets nothing itself. Any inherited paragraph property that would differ from today's
    # effective value (presentation default / master otherStyle) must be pinned explicitly, otherwise the heading would change visibly.
    from lxml import etree
    A_ = '{http://schemas.openxmlformats.org/drawingml/2006/main}'; mx = etree.fromstring(zin.read('ppt/slideMasters/slideMaster1.xml')); ts = mx.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}titleStyle/' + A_ + 'lvl1pPr')
    pres = etree.fromstring(zin.read('ppt/presentation.xml')); dflt = pres.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}defaultTextStyle/' + A_ + 'lvl1pPr')
    ts_ln = ts.find(A_ + 'lnSpc'); ts_attrs = dict(ts.attrib); d_attrs = dict(dflt.attrib) if dflt is not None else {}
    x = new[part].decode('utf8'); sp = re.search(r'<p:sp>(?:(?!</p:sp>).)*?<p:cNvPr id="%s" .*?</p:sp>' % re.escape(sid), x, re.S); blk = sp.group(0); nblk = blk; pinned = []
    for pm in list(re.finditer(r'<a:pPr(?P<attrs>[^>]*?)(?P<close>/?)>', blk)):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', pm.group('attrs')))
        for k, v in ts_attrs.items():
            if k not in attrs and d_attrs.get(k, v) != v: raise SystemExit(f'{part} {sid}: inherited paragraph attribute {k}={v} differs from current effective {d_attrs.get(k)} and is not explicit; stop')
    if ts_ln is not None:
        def pin(m):
            if m.group('close') == '/': return m.group(0)[:-2] + '><a:lnSpc><a:spcPct val="100000"/></a:lnSpc></a:pPr>'
            return m.group(0) + '<a:lnSpc><a:spcPct val="100000"/></a:lnSpc>'
        def fix_p(pm):
            body = pm.group(0)
            if '<a:lnSpc>' in body.split('</a:pPr>')[0] if '</a:pPr>' in body else '<a:lnSpc>' in body: return body
            if '<a:pPr' not in body.split('<a:r>')[0].split('<a:br')[0]: return body.replace('<a:p>', '<a:p><a:pPr><a:lnSpc><a:spcPct val="100000"/></a:lnSpc></a:pPr>', 1)   # paragraph without pPr
            return re.sub(r'<a:pPr(?P<attrs>[^>]*?)(?P<close>/?)>', pin, body, count=1)
        nblk = re.sub(r'<a:p>.*?</a:p>', fix_p, blk, flags=re.S); pinned = ['a:pPr: explicit lnSpc 100% (previous effective value; master titleStyle would otherwise apply 90%)'] if nblk != blk else []
    if nblk != blk: x = x.replace(blk, nblk, 1); new[part] = x.encode('utf8')
    edits.append(dict(part=part, shape_id=sid, shape=name, element='p:nvPr', before='(empty)', after='<p:ph type="title"/>', expected_source_occurrences=1, pinned_to_preserve_appearance=pinned))
with zipfile.ZipFile(dst, 'w') as zo:
    for i in zin.infolist():
        zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system; zo.writestr(zi, new[i.filename])
z2 = zipfile.ZipFile(dst); changed = sorted(n for n in data if z2.read(n) != data[n]); assert changed == sorted({p for p, *_ in plan}), changed
json.dump(dict(src_sha256=sha(open(src, 'rb').read()), dst_sha256=sha(open(dst, 'rb').read()), members_changed=changed, edits=edits), open(logp, 'w'), indent=1); print(len(edits), 'edits;', changed, sha(open(dst, 'rb').read())[:16])
