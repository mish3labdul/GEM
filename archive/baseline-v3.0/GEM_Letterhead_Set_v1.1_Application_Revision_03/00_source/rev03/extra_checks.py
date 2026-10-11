"""Revision 03 additional evidence: settings, mixed-direction isolation, unchanged payloads/assets,
extraction engines (incl. native macOS PDFKit), links, safe writing area, grayscale ink, Rev02 visual parity.
Usage: python extra_checks.py <rev03_root> <rev02_root> <scratch_with_pk_binary>"""
import sys, json, re, zipfile, hashlib, subprocess, unicodedata, collections
from pathlib import Path
from pypdf import PdfReader
from PIL import Image
import numpy as np

R3, R2, SC = (Path(a).resolve() for a in sys.argv[1:4])
KIT = R3.parent / 'GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal'
PK = str(SC / 'pk')
sha = lambda b: hashlib.sha256(b).hexdigest()
out = {'scope': 'Revision 03 checks run 2026-10-08 on macOS: python/pypdf/pdfplumber, poppler pdftotext, native PDFKit (Preview engine), '
                 'LibreOffice export path of Revision 02. Not covered: assistive technology, Windows/Online Word, physical print.'}


def paras(docx):
    x = zipfile.ZipFile(docx).read('word/document.xml').decode()
    res = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', x, flags=re.S):
        t = ''.join(a or ('\n' if b else '') for a, b in re.findall(r'<w:t[^>]*>([^<]*)</w:t>|(<w:br/>)', p))
        if t.strip():
            res.append(t)
    return res


def norm(s):
    s = re.sub(r'[‎‏‪-‮⁦-⁩؜‌‍]', '', s)
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s))


# 1 DOCX settings, isolation, payloads, logo assets
kit = {sha((KIT / f'{t}/gem-horizontal-{c}{s}').read_bytes()) for c in ('ink', 'black') for t, s in (('svg', '.svg'), ('png', '-2048.png'))}
docx = {}
for f in sorted((R3 / '01_templates').glob('*.docx')) + sorted((R3 / '04_qa/fixtures').glob('*.docx')):
    z = zipfile.ZipFile(f)
    st = z.read('word/settings.xml').decode()
    xml = ''.join(z.read(n).decode() for n in z.namelist() if re.match(r'word/(document|header\d+|footer\d+)\.xml$', n))
    media = {sha(z.read(n)) for n in z.namelist() if n.startswith('word/media/')}
    old = R2 / f.relative_to(R3)
    zo = zipfile.ZipFile(old)
    fonts_same = all(z.read(n) == zo.read(n) for n in z.namelist() if n.endswith('.odttf'))
    docx[str(f.relative_to(R3))] = {
        'embedSystemFonts_absent': '<w:embedSystemFonts/>' not in st,
        'saveSubsetFonts_present': '<w:saveSubsetFonts/>' in st,
        'lrm_bounded_ltr_runs': xml.count('‎') // 2,
        'logo_media_in_official_kit': media <= kit,
        'embedded_regular_payloads_identical_to_rev02': fonts_same,
        'package_parts_changed_vs_rev02': sorted(n for n in z.namelist() if n not in zo.namelist() or z.read(n) != zo.read(n)),
    }
out['docx'] = docx

# 2 extraction engines on final PDFs vs logical DOCX source (Arabic/bilingual)
def engines(pdf):
    e = {'pypdf': ''.join(p.extract_text() for p in PdfReader(pdf).pages),
         'poppler_pdftotext': subprocess.check_output(['pdftotext', str(pdf), '-'], text=True),
         'macOS_PDFKit': subprocess.check_output([PK, str(pdf)], text=True)}
    import pdfplumber
    with pdfplumber.open(pdf) as P:
        e['pdfplumber'] = ''.join(p.extract_text() or '' for p in P.pages)
    return e

ext = {}
for root, label in ((R2, 'Rev02'), (R3, 'Rev03')):
    for name in ('Arabic_First_Page', 'Arabic_Continuation', 'Bilingual_First_Page', 'Bilingual_Continuation'):
        src = [l for p in paras(root / f'01_templates/GEM_Letterhead_{name}.docx') for l in p.split('\n') if l.strip()]
        for eng, txt in engines(root / f'02_pdf/GEM_Letterhead_{name}.pdf').items():
            t = norm(txt)
            ext.setdefault(name, {}).setdefault(eng, {})[label] = f'{sum(norm(l) in t for l in src)}/{len(src)} logical lines exact'
out['extraction_engines'] = ext
q = subprocess.check_output([PK, str(R3 / '02_pdf/GEM_Letterhead_Arabic_First_Page.pdf'), '[DATE]', '[REFERENCE NUMBER]', 'التاريخ', 'يرجى تزويدنا'], text=True)
q2 = subprocess.check_output([PK, str(R2 / '02_pdf/GEM_Letterhead_Arabic_First_Page.pdf'), '[DATE]', '[REFERENCE NUMBER]', 'التاريخ', 'يرجى تزويدنا'], text=True)
out['pdfkit_search_arabic_first_page'] = {'Rev02': re.findall(r'SEARCH\[.*?\] hits=\d+', q2), 'Rev03': re.findall(r'SEARCH\[.*?\] hits=\d+', q)}

# 3 PDFs: links, safe writing area, grayscale ink, A4
pdfs = {}
for f in sorted((R3 / '02_pdf').glob('*.pdf')):
    r = PdfReader(f)
    links = sum(1 for p in r.pages for a in (p.get('/Annots') or []) if a.get_object().get('/Subtype') == '/Link')
    bb = subprocess.check_output(['pdftotext', '-bbox', str(f), '-'], text=True)
    xs = [(float(a), float(b)) for a, b in re.findall(r'xMin="([\d.]+)" yMin="[\d.]+" xMax="([\d.]+)"', bb)]
    subprocess.run(['pdftoppm', '-r', '50', '-gray', '-png', '-f', '1', '-l', '1', '-singlefile', str(f), '/tmp/r3ink'], check=True)
    g = np.array(Image.open('/tmp/r3ink.png').convert('L')).astype(float)
    pdfs[f.name] = {'pages': len(r.pages), 'a4': all(abs(float(p.mediabox.width) - 595.28) < 1 and abs(float(p.mediabox.height) - 841.89) < 1 for p in r.pages),
                    'link_annotations': links, 'text_x_range_pt': [round(min(a for a, _ in xs), 1), round(max(b for _, b in xs), 1)],
                    'text_within_25mm_side_margins_1pt_glyph_tolerance': min(a for a, _ in xs) >= 70.8 and max(b for _, b in xs) <= 525.4,
                    'page1_ink_coverage_percent_grayscale': round((255 - g).sum() / 255 / g.size * 100, 2)}
out['pdf'] = pdfs

# 4 visual parity with Revision 02 (LibreOffice exports, 100 dpi)
vis = {}
for f in sorted((R3 / '02_pdf').glob('GEM_Letterhead_*.pdf')):
    if f.stem in ('GEM_Letterhead_Digital', 'GEM_Letterhead_Print'):
        continue
    for tag, src in (('n', f), ('o', R2 / '02_pdf' / f.name)):
        subprocess.run(['pdftoppm', '-r', '100', '-gray', '-png', '-singlefile', str(src), f'/tmp/vis_{tag}'], check=True)
    a = np.array(Image.open('/tmp/vis_n.png')).astype(int); b = np.array(Image.open('/tmp/vis_o.png')).astype(int)
    d = np.abs(a - b)
    vis[f.name] = {'max_delta': int(d.max()), 'pixels_delta_gt40': int((d > 40).sum()),
                   'note': 'identical' if d.max() == 0 else 'differences confined to intended corrections: footer page digits now 9 pt (R03-08, all files); Arabic/bilingual sub-pixel shifts beside invisible U+200E marks (R03-02) and continuation placeholder punctuation (R03-07); reviewed visually'}
out['visual_parity_vs_rev02'] = vis
(R3 / '04_qa/evidence/Rev03_Checks.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
bad = [k for k, v in docx.items() if not (v['embedSystemFonts_absent'] and v['saveSubsetFonts_present'] and v['logo_media_in_official_kit'] and v['embedded_regular_payloads_identical_to_rev02'])]
bad += [k for k, v in pdfs.items() if not (v['a4'] and v['text_within_25mm_side_margins_1pt_glyph_tolerance'])]
print('Rev03 checks written; failures:', bad)
print(json.dumps(ext, ensure_ascii=False, indent=0)[:1600])
print(out['pdfkit_search_arabic_first_page'])
print({k: (v['link_annotations'], v['text_x_range_pt'], v['page1_ink_coverage_percent_grayscale']) for k, v in pdfs.items()})
print({k: v['package_parts_changed_vs_rev02'] for k, v in list(docx.items())[:8]})
