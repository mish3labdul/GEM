"""AR01 static checks (read-only): logo mirroring (M08), manual-space pseudo-layout, bilingual paragraph order (Arabic leads?), Arabic outside slide bodies, rotation.
Output contains counts, identifiers and script-class sequences only (no Arabic text). Usage: ar01_static_checks.py <repo_root> <package_dir>"""
import sys, os, re, json, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from ar01_common import *
root, pkg = sys.argv[1:3]
D3 = "GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/"; OD = "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/"
DECKS = {"Part A (D3)": D3 + "GEM Brand Guidelines V3.0 — Part A — RC2 — D3 CANDIDATE (UNAPPROVED).pptx",
         "Part A (AR01)": f"{pkg}/19_candidate_corrections/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx",
         "Part B (NP01-R1)": "GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/candidate_documents/GEM Digital Design System V3.0 — Part B — RC2 — NP01-R1 CANDIDATE (UNAPPROVED).pptx",
         "Part B (AR01)": f"{pkg}/19_candidate_corrections/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx",
         "Part C (D3)": D3 + "GEM Production Standards V3.0 — Part C — RC2 — D3 CANDIDATE (UNAPPROVED).pptx", "Part D (ODI01-R1)": OD + "GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx"}
LH = "GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/GEM_Letterhead_%s.docx"
LET = ["Arabic_First_Page", "Arabic_Continuation", "Bilingual_First_Page", "Bilingual_Continuation", "Executive", "Minimal", "English_First_Page", "English_Continuation"]
res = dict(pptx={}, docx={})
for name, p in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{p}" if not p.startswith(pkg) else p) if not p.startswith(pkg) else zipfile.ZipFile(p)
    paras = list(pptx_paragraphs(z)); ar_slides = sorted({r['num'] for r in paras if not r.get('is_picture') and r['kind'] == 'slides' and AR.search(r.get('text', ''))})
    pics = [r for r in paras if r.get('is_picture') and r['kind'] == 'slides' and r['num'] in ar_slides]
    all_pics_flip = [(r['num'], r['shape_idx']) for r in paras if r.get('is_picture') and r.get('flipH') in ('1', 'true')]
    arabic_nonbody = sorted({(r['kind'], r['num']) for r in paras if not r.get('is_picture') and r['kind'] != 'slides' and AR.search(r.get('text', ''))})
    spaces = [dict(slide=r['num'], para=r['para_idx'], double_space=bool(re.search(r'  +', r['text'])), leading_trailing=bool(re.search(r'^\s|\s$', r['text'])), tabs='\t' in r['text'])
              for r in paras if not r.get('is_picture') and r['kind'] == 'slides' and AR.search(r['text'])]
    rot = [(r['num'], r['shape_idx']) for r in paras if not r.get('is_picture') and r['kind'] == 'slides' and AR.search(r['text']) and (r['bodyPr'].get('vert', 'horz') != 'horz' or r['rot'] not in (None, '0'))]
    res['pptx'][name] = dict(arabic_slides=ar_slides, pictures_on_arabic_slides=len(pics), pictures_flipped_on_arabic_slides=[(r['num'], r['shape_idx']) for r in pics if r.get('flipH') in ('1', 'true')],
                             pictures_flipped_anywhere_in_deck=all_pics_flip, arabic_in_notes_masters_layouts=arabic_nonbody, arabic_paragraphs_with_manual_space_patterns=[s for s in spaces if s['double_space'] or s['leading_trailing'] or s['tabs']], arabic_text_rotation_or_vertical=rot)
for n in LET:
    z = zipfile.ZipFile(f"{root}/{LH % n}"); paras = [r for r in docx_paragraphs(z) if r['part'] == 'word/document.xml' and r['text'].strip()]
    seq = ''.join('A' if AR.search(r['text']) else 'E' if LAT.search(r['text']) else '-' for r in paras)
    flips = sum(len(re.findall(r'flipH="(?:1|true)"', z.read(m).decode('utf8', 'ignore'))) for m in z.namelist() if re.match(r'word/(document|header\d*|footer\d*)\.xml$', m))
    imgs = sum(len(re.findall(r'<pic:pic\b|<w:drawing\b', z.read(m).decode('utf8', 'ignore'))) for m in z.namelist() if re.match(r'word/(document|header\d*|footer\d*)\.xml$', m))
    spaces = sum(1 for r in paras if AR.search(r['text']) and (re.search(r'  +', r['text']) or '\t' in r['text']))
    bad_lg = sum(1 for r in paras if AR.search(r['text']) and not r['bidi'])
    res['docx'][n] = dict(content_paragraph_script_sequence=seq, drawings_in_body_headers_footers=imgs, flipped_drawings=flips, arabic_paragraphs_with_double_space_or_tab=spaces, arabic_paragraphs_without_bidi=bad_lg)
json.dump(res, open(f"{pkg}/17_qa/ar01_static_checks.json", 'w'), indent=1, default=str)
for k, v in res['pptx'].items(): print(k, {a: b for a, b in v.items() if a != 'arabic_slides'}, 'arabic slides', v['arabic_slides'])
for k, v in res['docx'].items(): print(k, v)
