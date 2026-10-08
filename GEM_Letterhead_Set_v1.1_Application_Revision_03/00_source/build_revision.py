from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,hashlib,shutil,datetime
from docx import Document
from docx.shared import Pt,Mm,RGBColor
BASE=Path('work/GEM/GEM_Letterhead_Set_v1.0')
OUT=Path('work/GEM/GEM_Letterhead_Set_v1.1')
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
q=lambda s:'{'+NS['w']+'}'+s
def child(p,t):
 e=p.find(q(t))
 if e is None:e=E.SubElement(p,q(t))
 return e
def text(p):return ''.join(t.text or '' for t in p.iter(q('t')))
def run(t,size=9,ar=False):
 r=E.Element(q('r'));pr=E.SubElement(r,q('rPr'));family='Noto Sans Arabic' if ar else 'Inter'
 E.SubElement(pr,q('rFonts'),{q(a):family for a in ['ascii','hAnsi','cs','eastAsia']})
 for tag,val in [('sz',round(size*2)),('szCs',round(size*2)),('b',0),('bCs',0),('rtl',int(ar)),('spacing',0)]:E.SubElement(pr,q(tag),{q('val'):str(val)})
 E.SubElement(pr,q('color'),{q('val'):'12171D'});E.SubElement(pr,q('lang'),{q('val'):'ar-SA' if ar else 'en-GB',q('bidi'):'ar-SA' if ar else 'en-GB'})
 E.SubElement(r,q('t'),{'{http://www.w3.org/XML/1998/namespace}space':'preserve'}).text=t
 return r
for s in ['00_source','01_templates','02_pdf','03_specs','04_qa/fixtures','04_qa/evidence','05_release']: (OUT/s).mkdir(parents=True,exist_ok=True)
before={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.rglob('*') if p.is_file()}
(OUT/'04_qa/evidence/Original_v1.0_Hashes.json').write_text(json.dumps(before,indent=2))
snapshot=json.loads(Path('outputs/GEM_Letterhead_UIAudit_BrandKit_Review/evidence/Source_Snapshot.json').read_text())
for item in snapshot['governing_files']:
 assert hashlib.sha256((BASE.parent/item['path']).read_bytes()).hexdigest()==item['sha256']
snapshot['refresh']='Live main SHA and local governing-file hashes reverified 2026-10-07; unchanged'
(OUT/'00_source/Source_Snapshot.json').write_text(json.dumps(snapshot,indent=2))
reconciliation=[]
for src in sorted((BASE/'07_final_audit/corrected_docx').glob('*.docx')):
 data={n:ZipFile(src).read(n) for n in ZipFile(src).namelist()}; ar='Arabic' in src.name or 'Bilingual' in src.name
 for name,blob in list(data.items()):
  if not name.endswith('.xml'):continue
  root=E.fromstring(blob)
  if name.startswith('word/footer'):
   for p in root.findall('.//w:p',NS):
    content=text(p)
    if 'WORKING APPLICATION' in content:
     # two complete lines, leaving the pending localization gate on every page
     for r in list(p):
      if r.tag!=q('pPr'):p.remove(r)
     p.append(run('WORKING APPLICATION / PENDING VALIDATION'))
     if ar:
      rr=E.SubElement(p,q('r'));E.SubElement(rr,q('br'));p.append(run('PENDING LOCALIZATION APPROVAL'))
    for r in p.findall('.//w:r',NS):
     pr=child(r,'rPr')
     for tag in ['sz','szCs']:child(pr,tag).set(q('val'),'18')
     for tag in ['b','bCs','rtl','spacing']:child(pr,tag).set(q('val'),'0')
     rf=child(pr,'rFonts')
     for a in ['ascii','hAnsi','cs','eastAsia']:rf.set(q(a),'Inter')
    sp=child(child(p,'pPr'),'spacing');sp.set(q('line'),'252');sp.set(q('lineRule'),'exact');sp.set(q('after'),'30')
  if name.startswith('word/header'):
   for el in root.xpath('//*[local-name()="docPr"]'):
    el.set('descr','GEM trademark horizontal logo. Supplied official vector kit; production-master acceptance pending.')
  if name=='word/document.xml':
   body=root.find('w:body',NS)
   # Preserve useful working edits from release, with unbroken editable LTR tokens.
   if 'Continuation' not in src.name:
    ps=[p for p in body.findall('w:p',NS) if '[DATE]' in text(p) and '[REFERENCE NUMBER]' in text(p)]
    if ps:
     p=ps[0];other=deepcopy(p)
     for r in list(p):
      if r.tag!=q('pPr'):p.remove(r)
     for r in list(other):
      if r.tag!=q('pPr'):other.remove(r)
     p.append(run('التاريخ: ' if ar else 'Date: ',10 if ar else 9,ar));p.append(run('[DATE]'))
     other.append(run('المرجع: ' if ar else 'Reference: ',10 if ar else 9,ar));other.append(run('[REFERENCE NUMBER]'))
     p.addnext(other);child(child(p,'pPr'),'keepNext')
    if 'Bilingual' in src.name:
     for p in body.findall('w:p',NS):
      if text(p).startswith('[RECIPIENT NAME] · [ORGANIZATION]'):
       for r in list(p):
        if r.tag!=q('pPr'):p.remove(r)
       for i,t in enumerate(['[RECIPIENT NAME]','[ORGANIZATION]','[ADDRESS]']):
        if i:rr=E.SubElement(p,q('r'));E.SubElement(rr,q('br'))
        p.append(run(t))
      if '[SIGNATORY NAME] · [TITLE]'==text(p):
       for t in p.findall('.//w:t',NS):t.text='[SIGNATORY NAME — ENGLISH / TRANSLITERATION, IF REQUIRED] · [TITLE]'
   for p in body.findall('w:p',NS):
    if text(p).startswith('SAMPLE CONTENT'):
     for r in p.findall('w:r',NS):
      for tag in ['sz','szCs']:child(child(r,'rPr'),tag).set(q('val'),'18')
  if name=='word/settings.xml':child(root,'updateFields').set(q('val'),'true')
  if name=='docProps/core.xml':
   n={'dc':'http://purl.org/dc/elements/1.1/','cp':'http://schemas.openxmlformats.org/package/2006/metadata/core-properties','dcterms':'http://purl.org/dc/terms/'}
   for tag,val in [('dc:title','GEM Branded Letterhead Set v1.1 Application Revision 02 '+src.stem.replace('GEM_Letterhead_','').replace('_',' ')),('dc:subject','WORKING APPLICATION / PENDING VALIDATION; RC2 application; 2026-10-07'),('dc:creator',''),('cp:lastModifiedBy','')]:
    e=root.find(tag,n)
    if e is not None:e.text=val
   for tag in ['dcterms:created','dcterms:modified']:
    e=root.find(tag,n)
    if e is not None:e.text='2026-10-07T12:00:00Z'
  data[name]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 # Source has three valid Regular-only font payloads. Preserve all media and fonts bytes.
 assert all(len(v)>32 for n,v in data.items() if n.startswith('word/fonts/'))
 with ZipFile(OUT/'01_templates'/src.name,'w',ZIP_DEFLATED) as z:
  for n,v in data.items():z.writestr(n,v)
 reconciliation.append({'file':src.name,'baseline':str(src.relative_to(BASE)),'preserved_release_edits':['Separate metadata lines','Executive optional second signatory retained from corrected candidate','Bilingual separate recipient organization and transliteration guidance where applicable'],'discarded':'Unintended export icons, invalid font embedding, split RTL brackets and typographic drift; original files preserved'})
(OUT/'00_source/Reconciliation.json').write_text(json.dumps(reconciliation,indent=2))
shutil.copy2(__file__,OUT/'00_source/build_revision.py')
# Fixtures derive from the actual new templates. Explicit and automatic flow, long fields, signature and mixed IDs.
for lang in ['English','Arabic','Bilingual']:
 for count in [2,3]:
  d=Document(OUT/'01_templates'/f'GEM_Letterhead_{lang}_First_Page.docx')
  sig=next(p for p in d.paragraphs if text(p._p) in ['Yours sincerely,','وتفضلوا بقبول التحية،'])
  for i in range(count-1):
   p=sig.insert_paragraph_before('');p.add_run().add_break(__import__('docx').enum.text.WD_BREAK.PAGE)
   for j in range(3):
    p=sig.insert_paragraph_before('');p._p.append(run('Additional sample content for pagination review.' if lang=='English' else 'نص تجريبي إضافي لمراجعة الصفحات.',10.5 if lang=='English' else 11.5,lang!='English'))
    if lang!='English':child(child(p._p,'pPr'),'bidi').set(q('val'),'1')
  d.save(OUT/'04_qa/fixtures'/f'QA_{lang}_{count}_pages.docx')
 d=Document(OUT/'01_templates'/f'GEM_Letterhead_{lang}_First_Page.docx')
 for p in d.paragraphs:
  for r in p.runs:
   if '[REFERENCE NUMBER]' in r.text:r.text=r.text.replace('[REFERENCE NUMBER]','[REFERENCE-2026-TEST-0123456789-ABCDEFGHIJ]')
   if '[RECIPIENT ORGANIZATION]' in r.text:r.text=r.text.replace('[RECIPIENT ORGANIZATION]','[LONG RECIPIENT ORGANIZATION FOR PROCUREMENT AND ADMINISTRATIVE REVIEW]')
   if 'Request for supplier' in r.text:r.text+=' and clarification of supporting evidence for procurement review and subsequent internal assessment'
   if '«اسم الجهة»' in r.text:r.text=r.text.replace('«اسم الجهة»','«اسم الجهة الطويل لاختبار المراسلات الإدارية ومراجعة المشتريات»')
 p=d.add_paragraph('');p._p.append(run('QA ONLY: [E: user@example.invalid] [W: https://example.invalid] [T: +000 000 0000] [ID: TEST-2026-001]',9))
 d.save(OUT/'04_qa/fixtures'/f'QA_{lang}_long_fields.docx')
for lang in ['English','Arabic','Bilingual']:
 d=Document(OUT/'01_templates'/f'GEM_Letterhead_{lang}_First_Page.docx')
 sig=next(p for p in d.paragraphs if text(p._p) in ['Yours sincerely,','وتفضلوا بقبول التحية،'])
 prototype=next(p for p in d.paragraphs if text(p._p).startswith('Please share' if lang=='English' else 'يرجى'))
 for i in range(25):sig._p.addprevious(deepcopy(prototype._p))
 d.save(OUT/'04_qa/fixtures'/f'QA_{lang}_automatic_flow.docx')
print('Created eight corrected templates and twelve fixtures',OUT)
