"""AX01 shared read-only helpers (PowerPoint OOXML object walk + deck registry). Run with the docling venv python (lxml)."""
import re, hashlib, zipfile
from lxml import etree
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'; P = 'http://schemas.openxmlformats.org/presentationml/2006/main'; R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ADEC = 'http://schemas.microsoft.com/office/drawing/2017/decorative'
ns = {'a': A, 'p': P, 'r': R, 'adec': ADEC}
AR = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
shaf = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
DECKS = {
 'A': ("Part A", "GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/19_candidate_corrections/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx", "AR01 candidate (D3 → AR01; slide 39 run split)"),
 'B': ("Part B", "GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/19_candidate_corrections/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx", "AR01 candidate (NP01-R1 → AR01; slide 9 metadata)"),
 'C': ("Part C", "GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/GEM Production Standards V3.0 — Part C — RC2 — D3 CANDIDATE (UNAPPROVED).pptx", "D3 candidate"),
 'D': ("Part D", "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx", "ODI01-R1 candidate (latest controlled)"),
}
LETTERHEADS = ["English_First_Page", "English_Continuation", "Arabic_First_Page", "Arabic_Continuation", "Bilingual_First_Page", "Bilingual_Continuation", "Executive", "Minimal"]
LH = "GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/GEM_Letterhead_%s.docx"

def slide_order(z):
    """slide part names in presentation order"""
    pres = etree.fromstring(z.read('ppt/presentation.xml')); rels = etree.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
    rid = {r.get('Id'): r.get('Target') for r in rels}
    out = []
    for s in pres.iterfind('.//p:sldIdLst/p:sldId', ns):
        t = rid[s.get('{%s}id' % R)]; out.append('ppt/' + t.lstrip('/').replace('ppt/', '') if not t.startswith('/') else t.lstrip('/'))
    return out

def layout_of(z, part):
    relp = part.replace('slides/', 'slides/_rels/') + '.rels'; rels = etree.fromstring(z.read(relp))
    for r in rels:
        if r.get('Type').endswith('/slideLayout'): return 'ppt/' + r.get('Target').replace('../', '')
    return None

def text_of(el): return ''.join(el.xpath('.//a:t/text()', namespaces=ns))

def walk(tree_parent, in_group=None, depth=0, counter=None):
    """yield dict per drawable object in spTree order (z-order), recursing into groups."""
    if counter is None: counter = [0]
    for el in tree_parent:
        tag = etree.QName(el).localname
        if tag not in ('sp', 'pic', 'grpSp', 'graphicFrame', 'cxnSp'): continue
        nv = el.find('.//p:cNvPr', ns)
        counter[0] += 1
        ext = nv.find('.//adec:decorative', ns) if nv is not None else None
        xf = el.find('./p:spPr/a:xfrm', ns) if tag != 'grpSp' else el.find('./p:grpSpPr/a:xfrm', ns)
        if tag == 'graphicFrame': xf = el.find('./p:xfrm', ns)
        off = xf.find('a:off', ns) if xf is not None else None; exe = xf.find('a:ext', ns) if xf is not None else None
        ph = el.find('./p:nvSpPr/p:nvPr/p:ph', ns) if tag == 'sp' else None
        gd = el.find('.//a:graphicData', ns) if tag == 'graphicFrame' else None
        kind = tag
        if tag == 'graphicFrame': kind = 'table' if gd is not None and gd.find('a:tbl', ns) is not None else 'chart' if gd is not None and 'chart' in (gd.get('uri') or '') else 'graphicFrame-other'
        txt = text_of(el.find('./p:txBody', ns)) if tag == 'sp' and el.find('./p:txBody', ns) is not None else ''
        is_txbox = tag == 'sp' and (el.find('./p:nvSpPr/p:cNvSpPr', ns) is not None and el.find('./p:nvSpPr/p:cNvSpPr', ns).get('txBox') == '1')
        d = dict(z=counter[0], id=nv.get('id'), name=nv.get('name'), kind=kind, descr=nv.get('descr') or '', title_attr=nv.get('title') or '', hidden=nv.get('hidden') == '1', decorative=ext is not None and ext.get('val') in ('1', 'true'),
                 has_text=bool(txt.strip()), text_len=len(txt.strip()), txbox=is_txbox, placeholder=(ph.get('type') or 'obj') if ph is not None else None, in_group=in_group, depth=depth,
                 x=int(off.get('x')) if off is not None else None, y=int(off.get('y')) if off is not None else None, cx=int(exe.get('cx')) if exe is not None else None, cy=int(exe.get('cy')) if exe is not None else None,
                 hlink=len(el.xpath('.//a:hlinkClick', namespaces=ns)), arabic=bool(AR.search(txt)), el=el)
        if tag == 'pic':
            d['media'] = el.find('.//a:videoFile', ns) is not None or el.find('.//a:audioFile', ns) is not None
        yield d
        if tag == 'grpSp': yield from walk(el, in_group=nv.get('id'), depth=depth + 1, counter=counter)

GENERIC_NAME = re.compile(r'^(Text|Shape|Table|Picture|Group|Title|TextBox|Rectangle|Line|Flow box|Flow arrow|Image|Connector|Straight Connector)\s?[\d-]+$')
def gl(name, sid):
    """Shape label safe for committed evidence: generic PowerPoint names pass through; names that may hold deck text (e.g. PowerPoint-saved Part D) become 'shape id N'."""
    return name if GENERIC_NAME.match(name or '') else f'shape id {sid}'
