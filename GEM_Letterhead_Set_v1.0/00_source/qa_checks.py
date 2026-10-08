from pathlib import Path
from pypdf import PdfReader
from lxml import etree as E
from fontTools.ttLib import TTFont
import zipfile,json,subprocess,hashlib
R=Path(__file__).resolve().parent.parent;results=[]
for p in (R/'01_templates').glob('GEM*.docx'):
 with zipfile.ZipFile(p) as z:
  xm=E.fromstring(z.read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  bad=[];families=set()
  for r in xm.xpath('//w:r[w:t]',namespaces=ns):
   text=''.join(r.xpath('./w:t/text()',namespaces=ns));font=r.xpath('./w:rPr/w:rFonts/@w:ascii',namespaces=ns)
   if not font:continue
   font=font[0];families.add(font);folder={'Jost':'jost','Inter':'inter','Noto Sans Arabic':'notosansarabic'}[font]
   f=TTFont(R/'00_source/fonts'/folder/(font.replace(' ','')+'-Regular.ttf'));c=f.getBestCmap()
   for ch in text:
    if not ch.isspace() and ord(ch) not in c:bad.append((ch,font))
  svg=[n for n in z.namelist() if n.endswith('.svg')]
  for n in svg:
   variant='black' if 'black' in n else 'ink';master=R.parent/f'GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/svg/gem-horizontal-{variant}.svg'
   if not master.exists():master=R/'00_source/reused_assets'/master.name
   assert z.read(n)==master.read_bytes()
  colors=set(xm.xpath('//@w:color|//w:color/@w:val',namespaces=ns));assert colors<={'12171D','BCACA7','020202','FFFFFF','auto'}
  results.append({'docx':p.name,'font_families':sorted(families),'missing_glyphs':bad,'svg_matches_repo':True,'embedded_fonts':len([n for n in z.namelist() if n.endswith('.odttf')])})
for p in list((R/'02_pdf').glob('*.pdf')):
 r=PdfReader(p);fontnames=set();images=0
 for pg in r.pages:
  res=pg['/Resources']
  for font in res.get('/Font',{}).values():fontnames.add(str(font.get_object().get('/BaseFont')))
  for x in res.get('/XObject',{}).values():images+=x.get_object().get('/Subtype')=='/Image'
 assert all(any(x in f for x in ['Inter','Jost','NotoSansArabic']) for f in fontnames),fontnames
 assert all(abs(float(pg.mediabox.width)-595.28)<1 and abs(float(pg.mediabox.height)-841.89)<1 for pg in r.pages)
 results.append({'pdf':p.name,'pages':len(r.pages),'tagged_structure_present':'/StructTreeRoot' in r.trailer['/Root'],'language':str(r.trailer['/Root'].get('/Lang')),'image_xobjects':images,'fonts':sorted(fontnames),'selectable_text':all(len(pg.extract_text())>100 for pg in r.pages)})
(R/'04_qa/structural_checks.json').write_text(json.dumps(results,indent=2,ensure_ascii=False));print('Checked',len(results),'files; missing glyphs:',sum(len(x.get('missing_glyphs',[])) for x in results))
