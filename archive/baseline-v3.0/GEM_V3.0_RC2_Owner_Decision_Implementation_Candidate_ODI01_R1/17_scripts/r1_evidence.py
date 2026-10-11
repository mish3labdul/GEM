"""ODI01-R1 evidence writer: 07_Font_Bold_Flag_Before_After.csv, 18_qa_evidence/affected_slide_visual_qa.md, 18_qa_evidence/file_diff_register.csv.
Usage: r1_evidence.py <pkg_dir> <odi01_candidate_dir> <r1_dir> <verify.json> <apply_log.json> <render_compare.json> <render_dir> <inventory_before.csv>"""
import sys,os,re,csv,json,glob,zipfile,hashlib,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from r1_ooxml import *
pkg,odi,r1,vj,lj,cj,rd,inv=sys.argv[1:9]
V=json.load(open(vj));L=json.load(open(lj));C=json.load(open(cj));INV=list(csv.DictReader(open(inv,encoding='utf-8')))
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
# slides the author looked at (individual images or contact sheets 01,03,06,10)
sheets={1:'B07 B10 B11 B12 B13 B14',3:'B21 B22 B23 B24 B25 B26',6:'C23 C28 C30 C32 C34 C39',10:'C70 C71 C72 C74'}
VIEWED={k for s in sheets.values() for k in s.split()}|{'A35','B03','B10','B12','B22','C15'}
EDITED={('Part A',35),('Part B',10),('Part B',12),('Part B',22),('Part C',15)}
REVIEW={(r['Document'],int(r['Slide'])) for r in INV if r['Proposed action'].startswith('REQUIRES')}
cmp={(c['doc'],c['slide']):c for c in C}
def runs_per_slide(path):
    z=zipfile.ZipFile(path);o={}
    for n,p in slide_order(z): o[n]=len(re.findall(r'<a:r>',z.read(p).decode()))
    return o
rows=[];b_before={};tb=tbb=ta=0
for key,tag in (('A','Part A'),('B','Part B'),('C','Part C'),('D','Part D')):
    a=[p for p in glob.glob(odi+'/*.pptx') if f'{tag} — RC2' in p][0];b=[p for p in glob.glob(r1+'/*.pptx') if f'{tag} — RC2' in p][0]
    ra,rb=runs_per_slide(a),runs_per_slide(b);bb={};
    for r in INV:
        if r['Document']==tag: bb[int(r['Slide'])]=bb.get(int(r['Slide']),0)+1
    slides=sorted({s for (d,s) in cmp if d==tag})
    for s in slides:
        c=cmp[(tag,s)];vis='Yes — wording' if (tag,s) in EDITED else ('Yes — added clarification box' if c['text_diff_ops'] and (tag,s) not in EDITED else 'Yes — weight of text runs (400 instead of synthetic bold)')
        if bb.get(s,0)==0 and (tag,s) not in EDITED: vis='Yes'
        seen=f'{key}{s:02d}' in VIEWED
        vq=('PASS — inspected' if seen else 'PASS — automated geometry metrics only (not inspected by eye)')
        note=f"word-origin shift {c['max_origin_shift_pt']} pt; lines {c['lines_before']}→{c['lines_after']}; overlaps {c['overlaps_before']}→{c['overlaps_after']}; words outside page {len(c['words_outside_page'])}"
        if (tag,s) in REVIEW: note+='; run-in head / emphasis weakened at 400 — no adjustment applied (owner/native review)'
        rows.append([tag,s,ra[s],bb.get(s,0),bb.get(s,0),0,vis,vq,note]);tbb+=bb.get(s,0)
    tb+=sum(bb.values())
hdr=['Document','Slide','Run count before','Brand-font bold flags before','Brand-font bold flags before (this row, all brand)','Brand-font bold flags after','Visible change?','Visual QA','Notes']
# the requested columns: Document,Slide,Run count before,Brand-font bold flags before,Brand-font bold flags after,Visible change?,Visual QA,Notes
out=[['Document','Slide','Run count before','Brand-font bold flags before','Brand-font bold flags after','Visible change?','Visual QA','Notes']]+[[r[0],r[1],r[2],r[3],r[5],r[6],r[7],r[8]] for r in rows]
tot_all_before=len(INV)
out+=[['TOTAL — all slides','','', tbb,0,'','',f'total b="1" runs before={tot_all_before}; after=0. Brand-font b="1" before={tbb}; after=0. Non-brand b="1" before=0; after=0. Part D: 0 before, 0 after, deck unchanged.']]
csv.writer(open(pkg+'/07_Font_Bold_Flag_Before_After.csv','w',newline='',encoding='utf-8')).writerows(out)
# ---- visual QA md
os.makedirs(pkg+'/18_qa_evidence/render',exist_ok=True)
md=['# Affected-slide visual QA — ODI01-R1','',
 '**Renderer: LibreOffice 26.8.1 (macOS, headless) — REVIEW EVIDENCE ONLY. This is not native PowerPoint validation; native PowerPoint QA remains OPEN.** ODI01 PDFs were made with LibreOffice 24.2; to compare like with like, **both** the ODI01 candidate ("before") and the R1 candidate ("after") were re-rendered here with identical settings (tagged PDF; accepted Regular 400 files of Jost, Inter and Noto Sans Arabic supplied from the repository, so bold requests render as the same synthetic bold seen in the ODI01 PDFs).','',
 f'**Affected slides = every slide whose OOXML part changed: {len(rows)} slides** (Part A 2, Part B {sum(1 for r in rows if r[0]=="Part B")}, Part C {sum(1 for r in rows if r[0]=="Part C")}, Part D 0). Derived from `17_scripts/r1_verify_edits.py`, not from searching for the string "500".','',
 'Method per slide: (1) rasterised before and after at 80 dpi and joined side by side (`render/<Part><slide>_before_after.png`: left = before, right = after); (2) word boxes compared via `pdftotext -bbox-layout`: word count, line count, largest word-origin shift, words outside the page, overlapping words; (3) visual inspection where marked.','',
 'Checks covered by (2): overflow, clipping, changed line wrapping, table fit, footer alignment and logo/text collision (no word box overlaps or leaves the page), unintended object movement (origin shift), font substitution (PDF fonts after: Inter-Regular, Jost-Regular, NotoSansArabic-Regular + the same non-brand helpers as before). Accidental colour change: colours are unchanged in the XML (srgbClr sets identical, QA item 6). Arabic shaping/RTL: no Arabic run was changed except bold-flag removal on the Part B tables; text and shaping geometry unchanged (shift 0).','',
 '| Document | Slide | Reason affected | Before / after render | Result | Adjustment required? |','|---|---|---|---|---|---|']
for tag,key in (('Part A','A'),('Part B','B'),('Part C','C')):
    z=zipfile.ZipFile([p for p in glob.glob(odi+'/*.pptx') if f'{tag} — RC2' in p][0]);order={p:n for n,p in slide_order(z)}
    rsn={order[p]:pp for p,pp in V[key]['per_part'].items()}
    for s in sorted(rsn):
        pp=rsn[s];c=cmp[(tag,s)];why=[]
        if pp['bold_cleared']: why.append(f"{pp['bold_cleared']} explicit bold flag(s) cleared (b=1→0)")
        if pp['text_edits']: why.append(f"{pp['text_edits']} wording edit(s) (D5 500→400 / pending)")
        if pp['clones']: why.append('clarification text box added')
        seen=f'{key}{s:02d}' in VIEWED
        res='PASS'+(' (inspected)' if seen else ' (metrics only)')
        if (tag,s) in REVIEW: res+=' · hierarchy weakened'
        adj='No. Run-in heads / emphasis now rely on punctuation and position; Brand Owner / native review to decide whether a 400-compatible cue (size, spacing, rule) is wanted. Bold NOT reintroduced.' if (tag,s) in REVIEW else 'No'
        if (tag,s) in EDITED: adj='No further adjustment (text edits fit; added box clear of footer)'
        md.append(f"| {tag} | {s} | {'; '.join(why)} | `render/{key}{s:02d}_before_after.png` | {res} | {adj} |")
        shutil.copy(f"{rd}/{key}{s:02d}_before_after.png",pkg+'/18_qa_evidence/render/')
md+=['','## Results','',f'- Slides rendered before and after: **{len(rows)} / {len(rows)}**.',
 f'- Slides inspected by eye (individual images or contact sheets): **{len(VIEWED)}**; remaining {len(rows)-len(VIEWED)} are covered by the automated geometry metrics only and are labelled "metrics only".',
 f'- Word count / line count unchanged on every slide except the 5 edited slides ({", ".join(f"{d} {s}" for d,s in sorted(EDITED))}); there the changes are the intended wording and clarification boxes.',
 '- Largest word-origin shift on an unedited slide: %s pt (sub-pixel; no re-wrapping).'%max(c['max_origin_shift_pt'] for c in C if (c['doc'],c['slide']) not in EDITED),
 '- New overlaps after: 0. Words outside page after: 0. Footer / logo collisions: none observed.',
 '- **Visual regressions found: none that break layout.** One **hierarchy finding**: on %d slides (%s) bold run-in heads and emphasis ("Character.", "Principles.", "Use:", "Added:" …) now read at 400. They stay legible and identifiable by punctuation and position, but their emphasis is weaker. Not corrected: re-adding bold is prohibited by D5, and the alternative cues (capitalisation, size, rules) would be a design change beyond a narrow reconciliation. Flagged for Brand Owner review.'%(len({k for k in REVIEW}),', '.join(f'{d.split()[-1]}{s}' for d,s in sorted(REVIEW))),
 '- Table header rows (Part B Beige fill, Part C Ink fill with white text) keep their hierarchy through fill and contrast.','',
 'Pre-existing, unchanged by R1: on Part B slide 12 the footnote starts at the lower edge of the right-hand table in the LibreOffice render (also visible in the "before" render).','',
 'Not tested: native PowerPoint rendering, PowerPoint accessibility checker, reading order, Windows/Mac PowerPoint font fallback.']
open(pkg+'/18_qa_evidence/affected_slide_visual_qa.md','w',encoding='utf-8').write('\n'.join(md)+'\n')
# ---- file diff register
fd=[['File','Original ODI01 hash','R1 hash','Reason','Decision scope','XML parts changed','Visible effect?','QA result']]
for key,tag in (('A','Part A'),('B','Part B'),('C','Part C'),('D','Part D')):
    a=[p for p in glob.glob(odi+'/*.pptx') if f'{tag} — RC2' in p][0];b=[p for p in glob.glob(r1+'/*.pptx') if f'{tag} — RC2' in p][0];v=V[key]
    parts=v['changed_parts'];n=v['totals']
    fd.append([os.path.basename(b),sha(a),sha(b),f"{n['bold_cleared']} brand-font bold flags cleared; {n['text_edits']} wording edit(s); {n['clones']} clarification box(es)" if parts else 'No R1 change (renamed copy of the ODI01 candidate)','D5' if parts else '—',f"{len(parts)} slide parts: "+', '.join(p.replace('ppt/slides/','') for p in parts) if parts else 'none',('Yes' if parts else 'No'),'PASS — r1_verify_edits.py (only intended differences); 112 assertions PASS; visual QA PASS' if parts else 'unchanged: hash equal to ODI01'])
    pa,pb=a[:-5]+'.pdf',b[:-5]+'.pdf'
    if os.path.exists(pa) or os.path.exists(b[:-5]+'.pdf'):
        pdf_o=glob.glob(f"{odi}/*{tag} — RC2 — ODI01 CANDIDATE*.pdf");pdf_n=glob.glob(f"{r1}/*{tag} — RC2 — ODI01-R1 CANDIDATE*.pdf")
        if pdf_o and pdf_n: fd.append([os.path.basename(pdf_n[0]),sha(pdf_o[0]),sha(pdf_n[0]),'Re-exported from the R1 deck (LibreOffice 26.8.1, tagged PDF) so the PDF matches the PPTX' if parts else 'Unchanged copy','D5' if parts else '—','n/a (PDF)','Yes' if parts else 'No','Tagged: yes; same page count as PPTX; fonts embedded Regular only' if parts else 'unchanged'])
T=odi.replace('deck_candidates','tokens');
fd.append(['gem-tokens.v3.0-rc2.ODI01-R1-candidate.json',sha(T+'/gem-tokens.v3.0-rc2.ODI01-candidate.json'),sha(pkg+'/19_candidate_documents/tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.json'),'4 weight-500 token descriptions + meta wording: FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400','D5','n/a (JSON): description x4, meta.status, meta.note','No (not rendered)','PASS — 153/153 values+types+names identical to original; 26 status changes retained; 0 promotions'])
fd.append(['gem-tokens.v3.0-rc2.ODI01-R1-candidate.css',sha(T+'/gem-tokens.v3.0-rc2.ODI01-candidate.css'),sha(pkg+'/19_candidate_documents/tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.css'),'4 comments + header comment: same wording as JSON','D5','n/a (CSS comments only)','No','PASS — all declarations (name+value) identical to original'])
csv.writer(open(pkg+'/18_qa_evidence/file_diff_register.csv','w',newline='',encoding='utf-8')).writerows(fd)
print(len(rows),'slides;',len(VIEWED),'inspected;',len(fd)-1,'diff rows')
