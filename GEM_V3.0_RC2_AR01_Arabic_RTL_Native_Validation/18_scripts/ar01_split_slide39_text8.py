"""AR01 final owner decision: split the single mixed run of Part A slide 39 'Text 8' into script-appropriate runs (controlled candidate copy; zip-level, anchored, no PowerPoint rewrite).
  Arabic run: the Arabic words and the space that precedes the identifier (variant 'A') -> lang="ar-SA"   |   Latin run: the technical identifier -> lang="en-US"
  Variant 'B' (scratch only) puts that space at the start of the Latin run instead. Both are character-for-character the same text; the variant is chosen natively.
Same rPr (font trio, size, colour, dirty) on both runs; only lang differs. No LRM/RLM/embedding controls, no added/removed spaces, no direction attribute, no geometry change.
Usage: ar01_split_slide39_text8.py <src_pptx> <dst_pptx> <variant A|B> <before_after_json|-> """
import sys, re, json, zipfile, hashlib, collections
from lxml import etree
src, dst, variant, outj = sys.argv[1:5]
sha = lambda b: hashlib.sha256(b).hexdigest(); shs = lambda s: sha(s.encode('utf8'))
PART, SHAPE, SID = 'ppt/slides/slide39.xml', 'Text 8', '10'
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
def describe(path):
    z = zipfile.ZipFile(path); root = etree.fromstring(z.read(PART))
    sp = [s for s in root.iterfind('.//p:sp', ns) if s.find('p:nvSpPr/p:cNvPr', ns).get('name') == SHAPE and s.find('p:nvSpPr/p:cNvPr', ns).get('id') == SID]; assert len(sp) == 1
    sp = sp[0]; ps = sp.findall('p:txBody/a:p', ns); assert len(ps) == 1; p = ps[0]; runs = p.findall('a:r', ns)
    text = ''.join(''.join(r.xpath('a:t/text()', namespaces=ns)) for r in runs)
    cps = ' '.join('U+%04X' % ord(c) for c in text); rp = lambda r, k: r.find('a:rPr', ns).get(k)
    tf = lambda r, t: r.find('a:rPr/a:%s' % t, ns).get('typeface'); ppr = p.find('a:pPr', ns); xf = sp.find('p:spPr/a:xfrm', ns); bp = sp.find('p:txBody/a:bodyPr', ns)
    return dict(paragraph_text_sha256=shs(text), characters=len(text), codepoint_sequence_sha256=shs(cps), whitespace_count=sum(c.isspace() for c in text), punctuation_count=sum((not c.isalnum()) and (not c.isspace()) for c in text),
                direction_control_characters=sum(ord(c) in (0x200e, 0x200f, 0x061c) or 0x202a <= ord(c) <= 0x202e or 0x2066 <= ord(c) <= 0x2069 for c in text),
                run_count=len(runs), run_lengths=[len(''.join(r.xpath('a:t/text()', namespaces=ns))) for r in runs], run_languages=[rp(r, 'lang') for r in runs], run_rtl_child_elements=sum(1 for r in runs if r.find('a:rPr/a:rtl', ns) is not None),
                paragraph_rtl=ppr.get('rtl'), paragraph_algn=ppr.get('algn'), paragraph_indent_marL=[ppr.get('indent'), ppr.get('marL')], line_spacing=ppr.find('a:lnSpc/a:spcPts', ns).get('val'), bodyPr=dict(bp.attrib),
                font_family=sorted({f"{tf(r,'latin')}/{tf(r,'ea')}/{tf(r,'cs')}" for r in runs}), font_size=sorted({rp(r, 'sz') for r in runs}), bold=sorted({str(rp(r, 'b')) for r in runs}), tracking_spc=sorted({str(rp(r, 'spc')) for r in runs}),
                run_rPr_other_attrs=sorted({json.dumps({k: v for k, v in r.find('a:rPr', ns).attrib.items() if k != 'lang'}, sort_keys=True) for r in runs}),
                text_box_geometry=dict(off=dict(xf.find('a:off', ns).attrib), ext=dict(xf.find('a:ext', ns).attrib)), endParaRPr=dict(p.find('a:endParaRPr', ns).attrib), slide_xml_sha256=sha(z.read(PART)))
before = describe(src)
zin = zipfile.ZipFile(src); data = {i.filename: zin.read(i.filename) for i in zin.infolist()}; x = data[PART].decode('utf8')
ms = [m for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S) if re.search(r'<p:cNvPr id="%s" name="%s"/>' % (SID, SHAPE), m.group(0))]; assert len(ms) == 1; b = ms[0].group(0)
rm = list(re.finditer(r'<a:r>(<a:rPr lang="ar-SA"[^>]*>.*?</a:rPr>)<a:t>([^<]*)</a:t></a:r>', b, re.S)); assert len(rm) == 1 and b.count('<a:r>') == 1 and b.count('<a:p>') == 1, 'expected exactly one paragraph and one source run'
rpr, text = rm[0].group(1), rm[0].group(2)
assert re.fullmatch(r'[\u0600-\u06FF]{3} [\u0600-\u06FF]{5} GEM-0000', text), 'unexpected source text structure'
assert rpr.count('lang="ar-SA"') == 1
cut = len(text) - len('GEM-0000') - (1 if variant == 'B' else 0)
t1, t2 = text[:cut], text[cut:]; assert t1 + t2 == text
r1 = f'<a:r>{rpr}<a:t>{t1}</a:t></a:r>'; r2 = f'<a:r>{rpr.replace(chr(108)+"ang=" + chr(34) + "ar-SA" + chr(34), "lang=" + chr(34) + "en-US" + chr(34), 1)}<a:t>{t2}</a:t></a:r>'
nb = b[:rm[0].start()] + r1 + r2 + b[rm[0].end():]; x2 = x[:ms[0].start()] + nb + x[ms[0].end():]; new = dict(data); new[PART] = x2.encode('utf8')
with zipfile.ZipFile(dst, 'w') as zo:
    for i in zin.infolist():
        zi = zipfile.ZipInfo(i.filename, i.date_time); zi.compress_type = i.compress_type; zi.external_attr = i.external_attr; zi.create_system = i.create_system; zo.writestr(zi, new[i.filename])
after = describe(dst); z2 = zipfile.ZipFile(dst); changed = sorted(n for n in data if z2.read(n) != data[n]); assert changed == [PART] and [i.filename for i in zin.infolist()] == [i.filename for i in z2.infolist()]
same = lambda k: before[k] == after[k]
proof = {k: same(k) for k in ('paragraph_text_sha256', 'characters', 'codepoint_sequence_sha256', 'whitespace_count', 'punctuation_count', 'direction_control_characters', 'paragraph_rtl', 'paragraph_algn', 'paragraph_indent_marL', 'line_spacing', 'bodyPr', 'font_family', 'font_size', 'bold', 'tracking_spc', 'run_rPr_other_attrs', 'text_box_geometry', 'endParaRPr')}
assert all(proof.values()), proof
# elements actually changed: everything else in the slide part is byte-identical outside this shape
outside_same = (x[:ms[0].start()] + x[ms[0].end():]) == (x2[:ms[0].start()] + x2[len(x2) - (len(x) - ms[0].end()):])
# reverse transform: merging the two runs back reproduces the source bytes exactly
inv = x2.replace(r1 + r2, f'<a:r>{rpr}<a:t>{text}</a:t></a:r>'); res = dict(variant=variant, src_sha256=sha(open(src, 'rb').read()), dst_sha256=sha(open(dst, 'rb').read()), members_changed=changed, member_order_identical=True,
        before=before, after=after, preserved_exactly=proof, changed_elements=["a:p/a:r: one run replaced by two consecutive runs (run boundary)", "second run a:rPr@lang: ar-SA -> en-US (identifier run); first run keeps lang=ar-SA", "no a:rPr/a:rtl child elements added; no pPr change; no control characters; no spaces added or removed"],
        rest_of_slide_member_byte_identical=outside_same, inverse_transform_reproduces_source_member=(inv.encode('utf8') == data[PART]), run_split=dict(run1_chars=len(t1), run2_chars=len(t2), run1_ends_with_space=t1.endswith(' '), run2_starts_with_space=t2.startswith(' ')))
assert res['rest_of_slide_member_byte_identical'] and res['inverse_transform_reproduces_source_member']
if outj != '-': json.dump(res, open(outj, 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('variant', 'dst_sha256', 'members_changed', 'rest_of_slide_member_byte_identical', 'inverse_transform_reproduces_source_member', 'run_split')}, indent=1)); print('preserved:', all(proof.values()), '| runs', before['run_count'], '->', after['run_count'], after['run_languages'])
