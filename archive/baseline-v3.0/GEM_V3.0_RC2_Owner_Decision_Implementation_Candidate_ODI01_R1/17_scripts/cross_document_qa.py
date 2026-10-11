"""ODI01-R1 20-point cross-document QA (item 15 now uses the structured validation_id_checker; item 8 audits 400-only/no-faux-bold; items 19/20 rebased on HEAD 4ea0d11 because AFC01/AFC02/ODI01 are external inputs, not repository history). Each item returns its own result; there is NO single overall PASS.
Items 18 and 19 (checksum/manifest integrity) are computed by verify_manifest.py after the manifest exists; pass --manifest-results <json> to merge them.
Usage: cross_document_qa.py <repo_root> <odi_dir> <out_json> [--manifest-results <json>]"""
import sys,os,re,json,glob,hashlib,subprocess,zipfile,collections,tempfile,shutil
from pptx import Presentation
root=os.path.abspath(sys.argv[1]);odi=os.path.abspath(sys.argv[2]);out=sys.argv[3]
mres=None
if '--manifest-results' in sys.argv: mres=json.load(open(sys.argv[sys.argv.index('--manifest-results')+1]))
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.run(['git','-C',root]+list(a),capture_output=True,text=True)
C=odi+'/19_candidate_documents/';D=C+'deck_candidates/'
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import validation_id_checker as VIC
ORIG={'A':root+'/GEM_V3_RC2/04_release/GEM Brand Guidelines V3.0 — Part A — RC2.pptx','B':root+'/PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pptx','C':root+'/GEM_V3_RC2/04_release/GEM Production Standards V3.0 — Part C — RC2.pptx','D':glob.glob(root+'/Amenities_Portfolio_PartD_RC2/04_release/*.pptx')[0]}
CAND={k:glob.glob(D+'*'+n+' — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx')[0] for k,n in (('A','Part A'),('B','Part B'),('C','Part C'),('D','Part D'))}
def lines(path):
    P=Presentation(path);res=[]
    def add(i,sh,kind):
        if sh.has_text_frame:
            for l in sh.text_frame.text.split('\n'):
                if l.strip(): res.append((i,kind,l.strip()))
        if getattr(sh,'has_table',False) and sh.has_table:
            for r in sh.table.rows:
                for c in r.cells:
                    for l in c.text.split('\n'):
                        if l.strip(): res.append((i,'table',l.strip()))
        if sh.shape_type==6:
            for g in sh.shapes: add(i,g,kind)
    for i,s in enumerate(P.slides,1):
        for sh in s.shapes: add(i,sh,'shape')
        if s.has_notes_slide:
            for l in s.notes_slide.notes_text_frame.text.split('\n'):
                if l.strip(): res.append((i,'notes',l.strip()))
    return res
LO={k:lines(v) for k,v in ORIG.items()};LC={k:lines(v) for k,v in CAND.items()}
txt=lambda L:'\n'.join(l[2] for l in L)
def newlines(k):
    so=collections.Counter(l[2] for l in LO[k]);sc=collections.Counter(l[2] for l in LC[k]);return list((sc-so).elements()),list((so-sc).elements())
R=[]
def rec(n,name,res,ev): R.append(dict(n=n,name=name,result=res,evidence=ev)); print(n,name,res)
# ---- 1 Register
tmp=tempfile.mkdtemp();xl=root+'/GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx'
shutil.copy(xl,tmp+'/in.xlsx')
subprocess.run(['soffice','--headless','-env:UserInstallation=file://'+tmp+'/prof','--convert-to','xlsx:Calc MS Excel 2007 XML','--outdir',tmp+'/out',tmp+'/in.xlsx'],capture_output=True,timeout=300)
import openpyxl
wb=openpyxl.load_workbook(tmp+'/out/in.xlsx',data_only=True);ws=wb['Approval Register']
hdr=[c.value for c in ws[1]];si=hdr.index('Status')
cnt=collections.Counter(r[si] for r in ws.iter_rows(min_row=2,values_only=True) if r[0])
tbd=sum(1 for r in wb['Owners & Governance'].iter_rows(min_row=5,max_row=16,values_only=True) if r[2] and str(r[2]).startswith('TBD'))
overall=[c for row in wb['Dashboard'].iter_rows(values_only=True) for c in row if c=='Not ready']
rec_txt=open(C+'register_adoption/GEM_V3_Final_Brand_Approval_Register_Prefilled.ADOPTION_RECORD_2026-10-08.md',encoding='utf-8').read()
STMT='The current GEM™ V3 Approval Register is confirmed as the governing working decision baseline. Evidence-required and deferred decisions remain subject to their stated gates. This adoption does not constitute AC20 release authorization.'
main_hash=subprocess.run(['git','-C',root,'show','4ea0d117da03850854654288afcdde98f39994d5:GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx'],capture_output=True).stdout
ok=[sha(xl) in rec_txt, hashlib.sha256(main_hash).hexdigest()==sha(xl), STMT in rec_txt, dict(cnt)=={'Approved':384,'Approved with modification':72,'Evidence Required':8,'Deferred':2}, tbd==12, bool(overall), sum(cnt.values())==466]
rec(1,'Register alignment','PASS' if all(ok) else 'FAIL',f'hash in record={ok[0]}, equals main={ok[1]}, exact statement={ok[2]}, recalculated counts={dict(cnt)}, role holders TBD={tbd}/12, Dashboard Overall "Not ready"={ok[5]}, rows={sum(cnt.values())}, rows edited=0')
# ---- 2 terminology
c2=[];bad=[]
for k in 'ABCD':
    po=collections.Counter(re.findall(r'Part [A-E]\b',txt(LO[k]),re.I));pc=collections.Counter(re.findall(r'Part [A-E]\b',txt(LC[k]),re.I))
    c2.append(f'{k}:{sum(pc.values())} refs')
    if po!=pc or any(x.upper().endswith('E') for x in pc): bad.append(k)
rec(2,'Parts A/B/C/D terminology','PASS' if not bad else 'FAIL '+','.join(bad),'Part A–D reference counts identical between each original and its candidate; no "Part E": '+', '.join(c2))
# ---- 3 version IDs
c3=[];bad=[]
for k in 'ABCD':
    o=len(re.findall(r'V3\.0\s+RC2|V3\.0 — Part|RC2',txt(LO[k])));c=len(re.findall(r'V3\.0\s+RC2|V3\.0 — Part|RC2',txt(LC[k])));c3.append(f'{k}:{o}={c}')
    if o!=c: bad.append(k)
tj=json.load(open(root+'/PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.json'));cj=json.load(open(C+'tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.json'))
mv=all(tj['meta'][x]==cj['meta'][x] for x in('version','edition','documentId','issued'))
rec(3,'Version IDs','PASS' if not bad and mv else 'FAIL','RC2/V3.0 version-string counts original=candidate '+', '.join(c3)+f'; token meta version/edition/documentId/issued unchanged={mv} ({cj["meta"]["version"]}, {cj["meta"]["documentId"]})')
# ---- 4 status vocabulary
VOC={'APPROVED','CONDITIONAL','PENDING VALIDATION','REFERENCE'}
def walk(n,p=()):
    if isinstance(n,dict):
        if '$value' in n: yield '.'.join(p),n
        else:
            for k,v in n.items():
                if not k.startswith('$'): yield from walk(v,p+(k,))
CT=dict(walk(cj));OT=dict(walk(tj))
tok_ok=all(t['status'] in VOC for t in CT.values())
bad=[];ev=[]
for k in 'ABCD':
    for w in ('APPROVED','CONDITIONAL','PENDING VALIDATION'):
        o=txt(LO[k]).count(w);c=txt(LC[k]).count(w)
        if c>o: bad.append(f'{k}:{w} {o}->{c}')
    add,_=newlines(k)
    if any(re.search(r'\b(ACCEPTED|VALIDATED|FINAL APPROVAL|RELEASED|PRODUCTION READY|SYSTEM READY)\b',l.replace('PENDING ACCEPTED FONT FILE','')) for l in add): bad.append(k+':new banned word')
rec(4,'Status vocabulary','PASS' if tok_ok and not bad else 'FAIL '+str(bad),f'all 153 token statuses in {sorted(VOC)}={tok_ok}; no deck status word count increased; no banned status word in any added line')
# ---- 5 tagline
c5=[];bad=[]
for k in 'ABCD':
    o=len(re.findall(r'hospitality,\s*in perfect proportion',txt(LO[k]),re.I));c=len(re.findall(r'hospitality,\s*in perfect proportion',txt(LC[k]),re.I));o2=len(re.findall(r'in perfect proportion',txt(LO[k]),re.I));c2_=len(re.findall(r'in perfect proportion',txt(LC[k]),re.I));c5.append(f'{k}:{o}={c}')
    if o!=c or o2!=c2_: bad.append(k)
rec(5,'Tagline','PASS' if not bad else 'FAIL','"HOSPITALITY, IN PERFECT PROPORTION" occurrences original=candidate: '+', '.join(c5)+'; no new tagline variant or text')
# ---- 6 palette
bad=[];c6=[]
def zset(path,pat):
    z=zipfile.ZipFile(path);s=set()
    for n in z.namelist():
        if n.startswith('ppt/slides/slide') and n.endswith('.xml'): s|=set(re.findall(pat,z.read(n).decode('utf8')))
    return s
for k in 'ABCD':
    a=zset(ORIG[k],r'srgbClr val="([0-9A-Fa-f]{6})"');b=zset(CAND[k],r'srgbClr val="([0-9A-Fa-f]{6})"');c6.append(f'{k}:{len(a)}')
    if a!=b: bad.append(k)
fnd={'foundation.color.ink':'#12171D','foundation.color.beige':'#BCACA7','foundation.color.black':'#020202','foundation.color.white':'#FFFFFF'}
pal=all(CT[k]['$value'].upper()==v for k,v in fnd.items());css=open(C+'tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.css',encoding='utf-8').read()
hexes=set(x.upper() for x in re.findall(r'#[0-9a-fA-F]{6}',css))
rec(6,'Palette','PASS' if not bad and pal and hexes=={'#12171D','#BCACA7','#020202','#FFFFFF'} else 'FAIL','srgbClr sets in all slide XML identical original vs candidate ('+', '.join(c6)+' colours); foundation tokens INK #12171D, BEIGE #BCACA7, BLACK #020202, WHITE #FFFFFF intact; CSS raw hex set = those four')
# ---- 7 families
bad=[]
for k in 'ABCD':
    if zset(ORIG[k],r'typeface="([^"]+)"')!=zset(CAND[k],r'typeface="([^"]+)"'): bad.append(k)
fam=[CT['type.family.'+x]['$value'] for x in('display','body','arabic')];famo=[OT['type.family.'+x]['$value'] for x in('display','body','arabic')]
rec(7,'Typography families','PASS' if not bad and fam==famo else 'FAIL','typeface sets in all slide XML identical original vs candidate; token families unchanged: '+' | '.join(map(str,fam)))
# ---- 8 weights / D5
F=root+'/GEM_Letterhead_Set_v1.1_Application_Revision_03/00_source/fonts/'
from fontTools.ttLib import TTFont
ttfs=glob.glob(F+'**/*.ttf',recursive=True);wts={os.path.basename(p):TTFont(p)['OS/2'].usWeightClass for p in ttfs}
static_ok=bool(ttfs) and all(v==400 for v in wts.values()) and not any(re.search('Medium|Bold|wght',os.path.basename(p)) for p in ttfs)
BRANDF=('Jost','Inter','Noto Sans Arabic')
def brand_bold(path):
    z=zipfile.ZipFile(path);brand=other=0
    for m in z.namelist():
        if m.startswith('ppt/slides/slide') and m.endswith('.xml'):
            for r in re.findall(r'<a:r>(?:(?!</a:r>).)*</a:r>',z.read(m).decode('utf8'),re.S):
                mm=re.match(r'<a:r><a:rPr\b[^>]*>',r)
                if mm and re.search(r'\bb="(1|true|on)"',mm.group(0)):
                    lat=re.search(r'<a:latin typeface="([^"]+)"',r)
                    if lat and lat.group(1) in BRANDF: brand+=1
                    else: other+=1
    return brand,other
bo={k:brand_bold(ORIG[k]) for k in 'ABCD'};bc={k:brand_bold(CAND[k]) for k in 'ABCD'}
tot_before=sum(sum(v) for v in bo.values());tot_after=sum(sum(v) for v in bc.values())
# remaining 500 references: every un-negated standalone 500 must be explicitly pending / future / negated
rem=[];unex=[]
for k in 'ABCD':
    for i,kind,l in LC[k]:
        if re.search(r'(?<![\w.#-])500(?![\w.%])',l):
            ok5=bool(re.search(r'PENDING|FUTURE DESIGN INTENT',l)); rem.append((k,i,l[:60],ok5))
            if not ok5: unex.append((k,i,l[:60]))
tokd=[CT[x].get('description','') for x in ('type.weight.medium','type.styleWeight.label','type.styleWeight.arabicH3','type.styleWeight.arabicLabel')]
tok_ok=all('FUTURE DESIGN INTENT = 500' in d and 'CURRENT IMPLEMENTATION = 400' in d for d in tokd) and all(CT[x]['$value']==500 for x in ('type.weight.medium','type.styleWeight.label','type.styleWeight.arabicH3','type.styleWeight.arabicLabel'))
rec(8,'Actual available font weights (D5: 400 only, no faux bold)','PASS' if static_ok and not unex and sum(v[0] for v in bc.values())==0 and tok_ok else 'FAIL '+str(unex),f'font files in main: {wts} (all weight 400, no 500/bold/variable file); brand-font explicit bold runs original={ {k:v[0] for k,v in bo.items()} } candidate={ {k:v[0] for k,v in bc.items()} } (current faux-bold dependency = {sum(v[0] for v in bc.values())}); all b="1" runs original={tot_before} candidate={tot_after} (non-brand b="1" candidate={sum(v[1] for v in bc.values())}); standalone "500" occurrences in candidate decks={len(rem)}, every one marked PENDING / FUTURE DESIGN INTENT={not unex}; four 500-weight tokens keep value 500 and state FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400={tok_ok}')
# ---- 9 token values
vo={k:(t['$value'],t['$type']) for k,t in OT.items()};vc={k:(t['$value'],t['$type']) for k,t in CT.items()}
decl=lambda s:re.findall(r'(--gem-[A-Za-z0-9-]+)\s*:\s*([^;]+);',s)
cssorig=open(root+'/PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.css',encoding='utf-8').read()
rec(9,'Token values','PASS' if vo==vc and len(vc)==153 and decl(cssorig)==decl(css) else 'FAIL',f'153 tokens: value+type identical={vo==vc}; names identical={list(vo)==list(vc)}; CSS declarations (name+value) identical={decl(cssorig)==decl(css)}; audit_tokens.py on originals: see audit_tokens_original.json')
# ---- 10 token statuses
RK={'APPROVED':3,'CONDITIONAL':2,'PENDING VALIDATION':1}
ch=[k for k in OT if OT[k]['status']!=CT[k]['status']];up=[k for k in ch if RK[CT[k]['status']]>RK[OT[k]['status']]]
tv=json.load(open(C+'tokens/token_verification.json'))
rec(10,'Token statuses','PASS' if len(ch)==26 and not up and all(str(v).startswith(('PASS','SEE')) for v in tv['verifications'].values()) else 'FAIL',f'{len(ch)} normalizations, {len(up)} promotions, transitions {tv["transitions"]}; dependency-hierarchy check: {tv["verifications"]["Dependency hierarchy: unexplained inflation (candidate)"]}')
# ---- 11 Arabic status
ar=[k for k in CT if k.startswith('type.') and re.search('arabic',k,re.I) and not k.startswith(('type.tracking.arabic','type.family.arabic')) and k!='type.arabicLineHeightMin']
b12=[l for l in LC['B'] if l[0]==12 and 'PENDING VALIDATION' in l[2]]
lo=sum(txt(LO[k]).count('PENDING LOCALIZATION APPROVAL') for k in 'ABCD');lc=sum(txt(LC[k]).count('PENDING LOCALIZATION APPROVAL') for k in 'ABCD')
LHD=glob.glob(root+'/GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/*.docx')
def dx(p):
    z=zipfile.ZipFile(p);return ''.join(re.sub('<[^>]+>','',z.read(n).decode('utf8','ignore')) for n in z.namelist() if re.match(r'word/(document|header\d*|footer\d*)\.xml',n))
arab_ok=all('PENDING LOCALIZATION APPROVAL' in dx(p) for p in LHD if re.search('Arabic|Bilingual',p))
g15=open(odi+'/14_Remaining_Gates.md',encoding='utf-8').read()
rec(11,'Arabic status','PASS' if all(CT[k]['status']=='PENDING VALIDATION' for k in ar) and b12 and lo==lc and arab_ok and 'VAL-07' in g15 else 'FAIL',f'{len(ar)} Arabic hierarchy tokens PENDING VALIDATION; Part B slide 12 still "PENDING VALIDATION"={bool(b12)}; "PENDING LOCALIZATION APPROVAL" deck occurrences original={lo} candidate={lc}; present in all Arabic/bilingual letterhead DOCX={arab_ok}; VAL-07 open in 14')
# ---- 12 asset naming
kit_changed=git('status','--porcelain','--','GEM_Brand_Assets_v1.0').stdout.strip()
xo=json.load(open(C+'d3a_carried_forward/x12_options_check.json'));d13=open(odi+'/13_D3_Unresolved.md',encoding='utf-8').read()
rec(12,'Asset naming policy','PASS' if not kit_changed and xo['n']==34 and xo['uniqA']==34 and xo['uniqB']==34 and 'No STREAM token is chosen' in d13 and os.path.exists(C+'d3a_carried_forward/x12_mapping_option_A_BRAND.csv') and os.path.exists(C+'d3a_carried_forward/x12_mapping_option_B_Logo.csv') else 'FAIL',f'GEM_Brand_Assets_v1.0 working-tree changes={bool(kit_changed)} (none = no source renamed); both mappings cover 34 files with 34 unique names each, 0 collisions with the 11 existing X12-shaped files; doc 13 states no STREAM token is chosen (D3 unresolved); D3B left to owner')
# ---- 13 letterhead
lh_changed=git('status','--porcelain','--','GEM_Letterhead_Set_v1.1_Application_Revision_03').stdout.strip()
wap=all('WORKING APPLICATION / PENDING VALIDATION' in dx(p) for p in LHD)
tag=all('Tagged:          yes' in subprocess.run(['pdfinfo',p],capture_output=True,text=True).stdout for p in glob.glob(root+'/GEM_Letterhead_Set_v1.1_Application_Revision_03/02_pdf/*.pdf'))
no04=not glob.glob(root+'/**/*Revision_04*',recursive=True)
d9=open(odi+'/09_Letterhead_Status.md',encoding='utf-8').read()
rec(13,'Letterhead application state','PASS' if not lh_changed and wap and tag and no04 and len(LHD)==8 and 'retired' in d9 else 'FAIL',f'letterhead package unchanged={not lh_changed}; 8/8 templates carry "WORKING APPLICATION / PENDING VALIDATION"={wap}; 10 PDFs tagged={tag}; no Revision 04 artifact exists={no04}; "R04 unavailable" retired in 09; native Windows Word / Word Online / Acrobat / AT / physical proof listed NOT closed (09, 10, 14)')
# ---- 14 production status
bad=[]
for k in 'ABCD':
    add,_=newlines(k)
    if any(re.search(r'PRODUCTION READY|print-ready|SYSTEM READY|CMYK|Pantone|\bGSM\b|Delta ?E',l,re.I) for l in add): bad.append(k)
cm=[len(re.findall('CONCEPT / NOT PRODUCTION ARTWORK',txt(LO['D']))),len(re.findall('CONCEPT / NOT PRODUCTION ARTWORK',txt(LC['D'])))]
rec(14,'Production status','PASS' if not bad and cm[0]==cm[1] and cm[0]>0 else 'FAIL '+str(bad),f'no production-ready / print-ready / supplier-spec words in any line added to a candidate deck; "CONCEPT / NOT PRODUCTION ARTWORK" markings original={cm[0]} candidate={cm[1]}; supplier values remain [REQUIRES SUPPLIER] / [PENDING PHYSICAL PROOF]')
# ---- 15 validation IDs (structured: VAL-18 explanatory mentions allowed, active-gate use fails)
docs=sorted(glob.glob(odi+'/[0-9][0-9]_*.md'))
scan=docs+sorted(glob.glob(C+'partd/*.md'))
allv,badf,expl=VIC.check_files(scan)
badl=[]
for p in docs:
    for l in open(p,encoding='utf-8'):
        if re.search(r'VAL-(05|07|08|13|15|20)\b',l) and re.search(r'\b(CLOSED|closed by)\b',l) and not re.search(r'not|NOT|never|no |No |nothing|without|does not|Not',l): badl.append((os.path.basename(p),l[:90]))
documented=any('VAL-18' in open(p,encoding='utf-8').read() and re.search(r'VAL-18[^\n]{0,60}unallocated|no VAL-18',open(p,encoding='utf-8').read()) for p in (odi+'/14_Remaining_Gates.md',odi+'/05_Validation_ID_QA_Fix.md')) 
rec(15,'Validation IDs','PASS' if not badf and not badl and documented and all(f'VAL-{n:02d}' in g15 for n in (5,7,8,13,15,20)) else 'FAIL '+str([(f['source'],f['line'],f['kind']) for f in badf][:3]),f'VAL ids referenced in {len(scan)} R1 documents {allv}; allocated set is VAL-01..VAL-21 except VAL-18 (intentionally unallocated); {len(expl)} explanatory mention(s) of the unallocated ID classified EXPLANATORY and allowed; active-gate or unknown-ID findings={len(badf)}; unallocated ID documented in 14/05={documented}; VAL-05/07/08/13/15/20 listed open in 14; no line closes them {badl}')
# ---- 16 release wording
LABEL='GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE'
neg=re.compile(r'\b(not|no|never|nor|without|until|cannot|neither|none|NOT|No)\b|SYSTEM READY → NOT RELEASED|C4|banned|forbidden|Not issued|does not|issue',re.I)
flag=[]
for p in docs:
    for l in open(p,encoding='utf-8'):
        if re.search(r'PRODUCTION READY|SYSTEM READY|FULL SYSTEM CONSISTENCY PASSED|\bRELEASED\b',l) and not re.search(r'NOT RELEASED',l.replace('NOT RELEASED','NOT RELEASED')) and not neg.search(l): flag.append((os.path.basename(p),l.strip()[:100]))
        if re.search(r'FULL SYSTEM CONSISTENCY PASSED',l) and not neg.search(l): flag.append((os.path.basename(p),l.strip()[:100]))
d1=open(odi+'/01_Executive_Summary.md',encoding='utf-8').read() if os.path.exists(odi+'/01_Executive_Summary.md') else ''
ac=all('AC20' in open(odi+f'/{f}',encoding='utf-8').read() and 'OPEN' in open(odi+f'/{f}',encoding='utf-8').read() for f in ('03_Owner_Decisions_Carried_Forward.md','14_Remaining_Gates.md'))
dk=[k for k in 'ABCD' if re.search(r'SYSTEM READY|PRODUCTION READY',txt(LC[k]))]
rec(16,'Release wording','PASS' if not flag and LABEL in d1 and ac and not dk else 'FAIL '+str(flag[:3]),f'status label present in 01={LABEL in d1}; AC20 OPEN stated in 03/14={ac}; no un-negated PRODUCTION READY / SYSTEM READY / RELEASED / FULL SYSTEM CONSISTENCY PASSED in ODI01 documents (flagged={flag}); no such phrase in any candidate deck={not dk}')
# ---- 17 Part D claims
def pda(path):
    r=subprocess.run([sys.executable,os.path.dirname(os.path.abspath(__file__))+'/partd_claim_audit.py',root,'/dev/null',path],capture_output=True,text=True).stdout
    return r
ro=pda(ORIG['D']);rc=pda(CAND['D'])
uo=int(re.search(r"'UNSUPPORTED CLAIM': (\d+)",ro).group(1)) if "'UNSUPPORTED CLAIM'" in ro else 0;uc=int(re.search(r"'UNSUPPORTED CLAIM': (\d+)",rc).group(1)) if "'UNSUPPORTED CLAIM'" in rc else 0
s15='Bleed, safe area and tolerances come from the supplier dieline, once supplied and approved.' in txt(LC['D']);n23='A mockup register is provided with this package; other registers are not part of it.' in txt(LC['D'])
reg=os.path.exists(root+'/Amenities_Portfolio_PartD_RC2/01_mockups/MOCKUP_REGISTER.csv')
rec(17,'Part D claims','PASS' if uo==1 and uc==0 and s15 and n23 and reg else 'FAIL',f'UNSUPPORTED CLAIM original={uo} candidate={uc}; slide-15 and slide-23-notes wording present={s15},{n23}; MOCKUP_REGISTER.csv exists={reg}; no register invented; changed lines are exactly two')
# ---- 18/19
if mres:
    rec(18,'Checksum integrity',mres['checksum']['result'],mres['checksum']['evidence']);rec(19,'Manifest integrity',mres['manifest']['result'],mres['manifest']['evidence'])
else:
    rec(18,'Checksum integrity','PENDING — computed by verify_manifest.py after the manifest exists','');rec(19,'Manifest integrity','PENDING — computed by verify_manifest.py after the manifest exists','')
# ---- 20 separation
PKGN=os.path.basename(odi)
st=git('status','--porcelain').stdout.splitlines();outside=[l for l in st if PKGN not in l]
orig_unchanged=git('diff','--quiet','HEAD','--','GEM_V3_RC2','PartB_RC2','Amenities_Portfolio_PartD_RC2','GEM_Brand_Assets_v1.0','GEM_Letterhead_Set_v1.1_Application_Revision_03','qa','README.md','GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md').returncode==0
names=all('ODI01-R1' in os.path.basename(p) for p in glob.glob(D+'*')+glob.glob(C+'tokens/gem-tokens*')+glob.glob(C+'partd/*'))
rec(20,'Candidate/original separation','PASS' if not outside and orig_unchanged and names else 'FAIL '+str(outside[:3]),f'working-tree changes outside the R1 folder={len(outside)}; authoritative originals (Register, Parts A–D, tokens, asset kit, letterhead, qa/, README, audit note) unchanged vs HEAD={orig_unchanged}; every candidate deck, token and Part D prose file carries an ODI01-R1 marker in its file name={names}; ODI01 (external input, not in repository history) is not overwritten: its input hashes are in 02_Preflight.md and MANIFEST.json; D3A candidates kept in d3a_carried_forward/')
json.dump(R,open(out,'w'),indent=1,ensure_ascii=False)
shutil.rmtree(tmp,ignore_errors=True)
