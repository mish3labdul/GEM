"""AR01 shared read-only helpers: paragraph iterators for PPTX and DOCX plus script/bidi classification.
Nothing here writes to any document. Run with a Python that has lxml (the docling venv)."""
import re, hashlib, zipfile
from lxml import etree

AR = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
LAT = re.compile(r'[A-Za-z]')
DIG = re.compile(r'[0-9]')
ARDIG = re.compile(r'[\u0660-\u0669\u06F0-\u06F9]')
MARKS = re.compile(r'[\u200e\u200f\u061c\u202a-\u202e\u2066-\u2069]')
TECHID = re.compile(r'[A-Za-z]{2,}[-_][A-Za-z0-9]+|\b[A-Z]{2,}\d+\b|\[[A-Z ]{3,}\]|\.[a-z]{2,4}\b')
sha = lambda s: hashlib.sha256(s.encode('utf8')).hexdigest()
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns = {'a': A, 'p': P, 'w': W}
q = lambda n, t: '{%s}%s' % (n, t)

def toggle_on(el):
    """OOXML on/off element: present and w:val not in (0, false, off)."""
    if el is None: return False
    v = el.get(q(W, 'val'))
    return v is None or v.lower() not in ('0', 'false', 'off')

def generic_label(name, idx):
    """Shape label safe for committed evidence: generic PowerPoint names pass through, anything else becomes 'shape #idx'."""
    return name if re.match(r'^(Text|Shape|Table|Picture|Group|Title|TextBox|Rectangle|Line|Flow box)\s?\d+', name or '', re.I) else f'shape #{idx}'

# ---------------------------------------------------------------- PPTX
def _runs_a(p):
    out = []
    for r in p:
        t = etree.QName(r).localname
        if t not in ('r', 'fld', 'br'):
            continue
        if t == 'br':
            out.append(dict(text='\n', lang=None, altLang=None, b=None, i=None, spc=None, sz=None, latin=None, ea=None, cs=None, rtl_el=False, kind='br'))
            continue
        rp = r.find('a:rPr', ns)
        att = lambda k: rp.get(k) if rp is not None else None
        tf = lambda tag: (rp.find('a:%s' % tag, ns).get('typeface') if rp is not None and rp.find('a:%s' % tag, ns) is not None else None)
        txt = ''.join(r.xpath('a:t/text()', namespaces=ns))
        out.append(dict(text=txt, lang=att('lang'), altLang=att('altLang'), b=att('b'), i=att('i'), spc=att('spc'), sz=att('sz'),
                        latin=tf('latin'), ea=tf('ea'), cs=tf('cs'), rtl_el=(rp is not None and rp.find('a:rtl', ns) is not None), kind=t))
    return out

def pptx_paragraphs(z):
    """Yield one dict per paragraph (any script) with full structural context."""
    parts = sorted([n for n in z.namelist() if re.match(r'ppt/(slides|notesSlides|slideLayouts|slideMasters|notesMasters|handoutMasters)/[^/]+\.xml$', n)],
                   key=lambda n: (n.split('/')[1], int(re.findall(r'(\d+)\.xml', n)[0]) if re.findall(r'(\d+)\.xml', n) else 0))
    for part in parts:
        root = etree.fromstring(z.read(part))
        kind = part.split('/')[1]
        num = int(re.findall(r'(\d+)\.xml', part)[0]) if re.findall(r'(\d+)\.xml', part) else None
        counter = [0]
        def walk(parent, in_group):
            for el in parent:
                tag = etree.QName(el).localname
                if tag == 'grpSp':
                    counter[0] += 1; walk(el, True)
                elif tag in ('sp', 'cxnSp', 'pic', 'graphicFrame'):
                    counter[0] += 1; idx = counter[0]
                    nv = el.find('.//p:cNvPr', ns); name = nv.get('name') if nv is not None else ''; sid = nv.get('id') if nv is not None else ''
                    xf = el.find('.//a:xfrm', ns); flip = (xf.get('flipH') if xf is not None else None); rot = (xf.get('rot') if xf is not None else None)
                    if tag == 'pic':
                        yield dict(part=part, kind=kind, num=num, shape_idx=idx, shape_id=sid, shape_name=name, shape_type='pic', in_group=in_group, table_rc=None,
                                   is_picture=True, flipH=flip, rot=rot, paragraph=None)
                    for tc_i, tc in enumerate(el.iterfind('.//a:tbl//a:tc', ns)):
                        for pi, p in enumerate(tc.iterfind('a:txBody/a:p', ns)):
                            yield _para(part, kind, num, idx, sid, name, 'table-cell', in_group, tc_i, p, tc.find('a:txBody/a:bodyPr', ns), rot, flip, pi)
                    if el.find('.//a:tbl', ns) is None:
                        bp = el.find('p:txBody/a:bodyPr', ns)
                        for pi, p in enumerate(el.iterfind('p:txBody/a:p', ns)):
                            yield _para(part, kind, num, idx, sid, name, tag, in_group, None, p, bp, rot, flip, pi)
        yield from walk(root.find('.//p:spTree', ns) if root.find('.//p:spTree', ns) is not None else root, False)

def _para(part, kind, num, idx, sid, name, stype, in_group, tc_i, p, bp, rot, flip, pi):
    ppr = p.find('a:pPr', ns); runs = _runs_a(p)
    return dict(part=part, kind=kind, num=num, shape_idx=idx, shape_id=sid, shape_name=name, shape_type=stype, in_group=in_group, table_rc=tc_i,
                is_picture=False, flipH=flip, rot=rot, para_idx=pi,
                pPr=dict(ppr.attrib) if ppr is not None else {}, bodyPr=dict(bp.attrib) if bp is not None else {}, runs=runs,
                text=''.join(r['text'] for r in runs), paragraph=p)

# ---------------------------------------------------------------- DOCX
def docx_paragraphs(z):
    parts = [n for n in z.namelist() if re.match(r'word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$', n)]
    for part in sorted(parts):
        root = etree.fromstring(z.read(part)); body = root
        sect_i = 0; pi = 0
        for p in root.iterfind('.//w:p', ns):
            in_table = bool(p.xpath('ancestor::w:tbl', namespaces=ns))
            ppr = p.find('w:pPr', ns)
            g = lambda path, att='val': (ppr.find(path, ns).get(q(W, att)) if ppr is not None and ppr.find(path, ns) is not None else None)
            runs = []
            for r in p.iterfind('.//w:r', ns):
                rp = r.find('w:rPr', ns)
                f = lambda path, att='val': (rp.find(path, ns).get(q(W, att)) if rp is not None and rp.find(path, ns) is not None else None)
                has = lambda path: rp is not None and rp.find(path, ns) is not None
                on = lambda path: rp is not None and toggle_on(rp.find(path, ns))
                txt = ''
                for ch in r:
                    t = etree.QName(ch).localname
                    if t == 't': txt += ch.text or ''
                    elif t == 'tab': txt += '\t'
                    elif t == 'br': txt += '\n'
                lang = rp.find('w:lang', ns) if rp is not None else None
                runs.append(dict(text=txt, rtl=on('w:rtl'), rtl_present=has('w:rtl'), lang_val=(lang.get(q(W, 'val')) if lang is not None else None), lang_bidi=(lang.get(q(W, 'bidi')) if lang is not None else None),
                                 lang_ea=(lang.get(q(W, 'eastAsia')) if lang is not None else None),
                                 f_ascii=f('w:rFonts', 'ascii'), f_hAnsi=f('w:rFonts', 'hAnsi'), f_cs=f('w:rFonts', 'cs'), sz=f('w:sz'), szCs=f('w:szCs'),
                                 spacing=f('w:spacing'), b=(f('w:b') if has('w:b') else None), bCs=(f('w:bCs') if has('w:bCs') else None), i=(f('w:i') if has('w:i') else None)))
            instr = ' '.join(p.xpath('.//w:instrText/text()', namespaces=ns)) + ' ' + ' '.join(p.xpath('.//w:fldSimple/@w:instr', namespaces=ns))
            yield dict(part=part, para_idx=pi, in_table=in_table, bidi=(ppr is not None and toggle_on(ppr.find('w:bidi', ns))), jc=g('w:jc'), runs=runs,
                       text=''.join(r['text'] for r in runs), fields=instr.strip(), sect_end=(ppr is not None and ppr.find('w:sectPr', ns) is not None))
            pi += 1

# ---------------------------------------------------------------- classification
def classify(text):
    """Technical script mix only; says nothing about meaning."""
    a, lt, dg = bool(AR.search(text)), bool(LAT.search(text)), bool(DIG.search(text) or ARDIG.search(text))
    if not a: return None
    if lt and TECHID.search(text): return 'ARABIC + TECHNICAL ID'
    if lt: return 'MIXED ARABIC + LATIN'
    if dg: return 'ARABIC + NUMERIC'
    return 'ARABIC ONLY'

def bidi_dependencies(text):
    d = []
    if DIG.search(text) or ARDIG.search(text): d.append('number')
    if LAT.search(text): d.append('latin-text')
    if re.search(r'[A-Za-z]{2,}[-_][A-Za-z0-9]+|\b[A-Z]{2,}\d+\b', text): d.append('technical-id')
    if re.search(r'[()\[\]{}«»]', text): d.append('brackets-or-parentheses')
    if ':' in text or '：' in text: d.append('colon')
    if '/' in text or '\\' in text: d.append('slash')
    if re.search(r'[-–—]', text): d.append('dash')
    if '%' in text or '\u066a' in text: d.append('percent')
    if re.search(r'\.[a-z]{2,4}\b', text): d.append('filename-like')
    if re.search(r'https?://|www\.', text): d.append('url')
    if re.search(r'\b\d{1,4}[/-]\d{1,2}[/-]\d{1,4}\b|\b20\d\d\b', text): d.append('date-like')
    if MARKS.search(text): d.append('explicit-direction-marks')
    return d
