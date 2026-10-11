"""AR01 tasks 1-6 (read-only): candidate baseline + Arabic content inventory + language/bidi/typography audits.
Committed outputs contain NO Arabic strings: paragraph identifiers, property values, lengths and SHA-256 only.
Text-bearing raw output goes to local_only/ (excluded from version control pending D7).
Usage: ar01_inventory.py <repo_root> <package_dir>   (run with the docling venv python: needs lxml)"""
import sys, os, re, csv, json, zipfile, subprocess, collections
sys.path.insert(0, os.path.dirname(__file__))
from ar01_common import *

root, pkg = sys.argv[1:3]
D3 = "GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/"
OD = "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/"
LH = "GEM_Letterhead_Set_v1.1_Application_Revision_03"
DECKS = [
 ("Part A", D3 + "GEM Brand Guidelines V3.0 — Part A — RC2 — D3 CANDIDATE (UNAPPROVED).pptx", "D3 package (supersedes ODI01-R1 Part A)", "UNAPPROVED controlled candidate"),
 ("Part B", "GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/candidate_documents/GEM Digital Design System V3.0 — Part B — RC2 — NP01-R1 CANDIDATE (UNAPPROVED).pptx", "NP01-R1 package (supersedes ODI01-R1 Part B; slide 30 layout fix only)", "UNAPPROVED controlled candidate"),
 ("Part C", D3 + "GEM Production Standards V3.0 — Part C — RC2 — D3 CANDIDATE (UNAPPROVED).pptx", "D3 package (supersedes ODI01-R1 Part C)", "UNAPPROVED controlled candidate"),
 ("Part D", OD + "GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx", "ODI01-R1 package (not reissued under D3 or NP01-R1)", "UNAPPROVED controlled candidate (concept / not production)"),
]
LETTERS = ["Arabic_First_Page", "Arabic_Continuation", "Bilingual_First_Page", "Bilingual_Continuation", "Executive", "Minimal", "English_First_Page", "English_Continuation"]
sha_file = lambda p: __import__('hashlib').sha256(open(p, 'rb').read()).hexdigest()

# ---- baseline
base = []; docs = []
for name, path, lineage, status in DECKS:
    z = zipfile.ZipFile(f"{root}/{path}"); paras = [r for r in pptx_paragraphs(z) if not r.get('is_picture')]
    ar = [r for r in paras if AR.search(r['text'])]
    mixed = [r for r in ar if LAT.search(r['text']) or DIG.search(r['text'])]
    n = len([x for x in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', x)])
    base.append([name, path, lineage, sha_file(f"{root}/{path}"), f"{n} slides", 'YES' if ar else 'NO', 'YES' if mixed else 'NO', status, 'WORKING CANDIDATE (not authoritative)'])
    docs.append((name, 'pptx', z, path))
for n in LETTERS:
    p = f"{LH}/01_templates/GEM_Letterhead_{n}.docx"; z = zipfile.ZipFile(f"{root}/{p}")
    paras = list(docx_paragraphs(z)); ar = [r for r in paras if AR.search(r['text'])]; mixed = [r for r in ar if LAT.search(r['text']) or DIG.search(r['text'])]
    app = z.read('docProps/app.xml').decode('utf8', 'ignore'); pg = re.search(r'<Pages>(\d+)</Pages>', app)
    pdf = f"{root}/{LH}/02_pdf/GEM_Letterhead_{n}.pdf"; pp = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout)
    same = sha_file(f"{root}/{p}") == sha_file(f"{root}/{LH}/05_release/GEM_Letterhead_{n}.docx")
    base.append([f"Letterhead {n.replace('_', ' ')}", p, f"Set v1.1 Application Revision 03 (derives from Rev 02); 01_templates == 05_release: {'yes' if same else 'NO'}", sha_file(f"{root}/{p}"),
                 f"{pg.group(1) if pg else '?'} page(s) in docx metadata; sample PDF {pp.group(1) if pp else '?'} page(s)", 'YES' if ar else 'NO', 'YES' if mixed else 'NO',
                 'WORKING APPLICATION / PENDING VALIDATION', 'WORKING CANDIDATE (not authoritative)'])
    docs.append((f"Letterhead {n.replace('_', ' ')}", 'docx', z, p))
w = csv.writer(open(f"{pkg}/02_AR01_Candidate_Baseline.csv", 'w', newline='', encoding='utf8'))
w.writerow(["Document", "Path", "Package / lineage", "SHA-256", "Slide/page count", "Arabic content present?", "Mixed Arabic/Latin content present?", "Current candidate status", "Authoritative or working candidate?"]); w.writerows(base)

# ---- inventory (committed: no text) + raw (local only: text)
inv = []; raw = []; lang_f = []; typo_f = []; bidi_f = []
C = collections.Counter()
for name, kind, z, path in docs:
    if kind == 'pptx':
        for r in pptx_paragraphs(z):
            if r.get('is_picture'):
                continue
            t = r['text']
            if not AR.search(t): continue
            cat = classify(t); runs = [x for x in r['runs'] if x['kind'] != 'br']
            ar_runs = [x for x in runs if AR.search(x['text'])]
            mixed_run = any(AR.search(x['text']) and (LAT.search(x['text']) or DIG.search(x['text'])) for x in runs)
            langs = sorted({x['lang'] or 'none' for x in ar_runs}); spcs = sorted({x['spc'] or '0' for x in ar_runs})
            fonts = sorted({f"{x['latin']}/{x['ea']}/{x['cs']}" for x in ar_runs}); sizes = sorted({x['sz'] or 'inherit' for x in ar_runs})
            bold = sorted({x['b'] or 'absent' for x in ar_runs}); rtl_flag = r['pPr'].get('rtl', 'absent')
            label = generic_label(r['shape_name'], r['shape_idx'])
            inv.append([name, r['kind'], r['num'], r['shape_idx'], label, r['shape_type'], 'yes' if r['table_rc'] is not None else 'no', 'yes' if r['in_group'] else 'no', r['para_idx'], 'yes', 'yes' if LAT.search(t) else 'no',
                        'yes' if mixed_run else 'no', rtl_flag, '|'.join(langs), r['pPr'].get('algn', 'inherit'), r['bodyPr'].get('anchor', 'inherit'), '|'.join(fonts), '|'.join(sizes), '|'.join(bold), '|'.join(spcs),
                        r['bodyPr'].get('vert', 'horz') + '/rot=' + str(r['rot'] or 0), 'yes' if r['kind'] == 'notesSlides' else 'no', cat, ','.join(bidi_dependencies(t)), len(t), sha(t)])
            raw.append(dict(doc=name, slide=r['num'], shape=label, idx=r['shape_idx'], para=r['para_idx'], text=t, cat=cat))
            C[(name, cat)] += 1
            # language metadata
            bad_lang = [x for x in ar_runs if (x['lang'] or '').lower().startswith('en') or not x['lang']]
            lang_f.append([name, r['num'], label, r['para_idx'], '|'.join(langs), 'yes' if bad_lang else 'no', 'yes' if rtl_flag == 'absent' else 'no',
                           'yes' if mixed_run else 'no', 'ar-SA expected on Arabic runs', cat])
            typo_f.append([name, r['num'], label, r['para_idx'], '|'.join(fonts), '|'.join(sizes), '|'.join(bold), '|'.join(spcs), 'yes' if any((x['spc'] or '0') != '0' for x in ar_runs) else 'no',
                           'yes' if any(x['b'] in ('1', 'true') for x in ar_runs) else 'no', 'yes' if any(x['cs'] != 'Noto Sans Arabic' for x in ar_runs) else 'no'])
            bidi_f.append([name, r['num'], label, r['para_idx'], cat, r['pPr'].get('algn', 'inherit'), rtl_flag, 'yes' if any(x['rtl_el'] for x in runs) else 'no', ','.join(bidi_dependencies(t)), len(t), sha(t)])
    else:
        for r in docx_paragraphs(z):
            t = r['text']
            if not AR.search(t): continue
            cat = classify(t); runs = [x for x in r['runs'] if x['text']]; ar_runs = [x for x in runs if AR.search(x['text'])]
            mixed_run = any(AR.search(x['text']) and (LAT.search(x['text']) or DIG.search(x['text'])) for x in runs)
            latin_runs_rtl_off = sum(1 for x in runs if LAT.search(x['text']) and not AR.search(x['text']) and not x['rtl'])
            langs = sorted({f"{x['lang_val']}/{x['lang_bidi']}" for x in ar_runs}); spcs = sorted({x['spacing'] or '0' for x in ar_runs}); bold = sorted({f"b={x['b']}/bCs={x['bCs']}" for x in ar_runs})
            fonts = sorted({f"{x['f_ascii']}/{x['f_hAnsi']}/{x['f_cs']}" for x in ar_runs}); sizes = sorted({f"{x['sz']}/{x['szCs']}" for x in ar_runs})
            inv.append([name, r['part'], '', r['para_idx'], '', 'w:p', 'yes' if r['in_table'] else 'no', 'no', r['para_idx'], 'yes', 'yes' if LAT.search(t) else 'no', 'yes' if mixed_run else 'no',
                        f"bidi={'yes' if r['bidi'] else 'no'}; rtl-runs={sum(1 for x in ar_runs if x['rtl'])}/{len(ar_runs)}; latin-runs-rtl-off={latin_runs_rtl_off}", '|'.join(langs), r['jc'] or 'inherit', 'n/a', '|'.join(fonts), '|'.join(sizes), '|'.join(bold), '|'.join(spcs),
                        'n/a', 'no', cat, ','.join(bidi_dependencies(t)) + (f"; fields={r['fields']}" if r['fields'] else ''), len(t), sha(t)])
            raw.append(dict(doc=name, part=r['part'], para=r['para_idx'], text=t, cat=cat)); C[(name, cat)] += 1
            lang_f.append([name, r['part'], '', r['para_idx'], '|'.join(langs), 'no' if all((x['lang_val'] or '').startswith('ar') for x in ar_runs) else 'yes', 'no' if r['bidi'] else 'yes', 'yes' if mixed_run else 'no', 'ar-SA expected on Arabic runs', cat])
            typo_f.append([name, r['part'], '', r['para_idx'], '|'.join(fonts), '|'.join(sizes), '|'.join(bold), '|'.join(spcs), 'yes' if any((x['spacing'] or '0') != '0' for x in ar_runs) else 'no',
                           'yes' if any(x['b'] not in (None, '0', 'false') or x['bCs'] not in (None, '0', 'false') for x in ar_runs) else 'no', 'yes' if any(x['f_cs'] != 'Noto Sans Arabic' for x in ar_runs) else 'no'])
            bidi_f.append([name, r['part'], '', r['para_idx'], cat, r['jc'] or 'inherit', 'bidi=yes' if r['bidi'] else 'bidi=no', 'rtl-runs=%d/%d' % (sum(1 for x in ar_runs if x['rtl']), len(ar_runs)), ','.join(bidi_dependencies(t)), len(t), sha(t)])

H = ["Document", "Part / kind", "Slide", "Shape index", "Shape label", "Shape type", "Table cell?", "Group item?", "Paragraph index", "Arabic present?", "Latin present?", "Mixed run?", "Paragraph rtl / bidi", "Run language(s)",
     "Alignment", "Anchor", "Font family (latin/ea/cs)", "Font size", "Bold", "Tracking (spc)", "Text rotation", "Notes Arabic?", "Technical classification", "Bidi dependencies", "Text length", "Text SHA-256"]
csv.writer(open(f"{pkg}/03_AR01_Arabic_Content_Inventory.csv", 'w', newline='', encoding='utf8')).writerows([H] + inv)
csv.writer(open(f"{pkg}/04_AR01_Language_Metadata_Findings.csv", 'w', newline='', encoding='utf8')).writerows(
    [["Document", "Slide / part", "Shape label", "Paragraph index", "Arabic run language(s)", "Latin/missing language on Arabic run?", "Paragraph direction flag absent?", "Mixed run?", "Expected", "Classification"]] + lang_f)
csv.writer(open(f"{pkg}/06_AR01_Arabic_Typography_Findings.csv", 'w', newline='', encoding='utf8')).writerows(
    [["Document", "Slide / part", "Shape label", "Paragraph index", "Font family (latin/ea/cs or ascii/hAnsi/cs)", "Size", "Bold flags", "Tracking values", "Non-zero Arabic tracking?", "Bold on Arabic?", "Complex-script font not Noto Sans Arabic?"]] + typo_f)
csv.writer(open(f"{pkg}/local_only/raw_inventory/bidi_paragraphs_structure.csv", 'w', newline='', encoding='utf8')).writerows(
    [["Document", "Slide / part", "Shape label", "Paragraph index", "Classification", "Alignment", "Direction flag", "Run rtl", "Bidi dependencies", "Length", "SHA-256"]] + bidi_f)
json.dump(raw, open(f"{pkg}/local_only/raw_inventory/arabic_text_raw.json", 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print({f"{k[0]}|{k[1]}": v for k, v in C.items()}); print("Arabic paragraphs:", len(inv))
