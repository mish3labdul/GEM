from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader
from fontTools.ttLib import TTFont
import json,hashlib,subprocess
R=Path(__file__).resolve().parent.parent;ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W='{'+ns['w']+'}'
results=[]
for p in (R/'01_templates').glob('GEM*.docx'):
 with ZipFile(p) as z:
  assert len(z.namelist())==len(set(z.namelist()));assert z.testzip() is None
  roots=[E.fromstring(z.read(n)) for n in z.namelist() if n=='word/document.xml' or n.startswith('word/header') and n.endswith('.xml') or n.startswith('word/footer') and n.endswith('.xml')]
  bold=[n for root in roots for n in root.xpath('//w:b|//w:bCs',namespaces=ns) if n.get(W+'val','1') not in ['0','false','off']];assert not bold
  missing=[]
  for root in roots:
   for run in root.xpath('//w:r[w:t]',namespaces=ns):
    font=run.xpath('./w:rPr/w:rFonts/@w:ascii',namespaces=ns)
    if not font:continue
    fam=font[0];folder={'Jost':'jost','Inter':'inter','Noto Sans Arabic':'notosansarabic'}[fam];f=TTFont(R/'00_source/fonts'/folder/(fam.replace(' ','')+'-Regular.ttf'));assert f['OS/2'].usWeightClass==400;c=f.getBestCmap()
    for ch in ''.join(run.xpath('./w:t/text()',namespaces=ns)):
     if not ch.isspace() and ord(ch) not in c:missing.append((fam,ch))
  assert not missing
  styles=E.fromstring(z.read('word/styles.xml'))
  for name in ['Normal','BodyText','Heading1','Heading2']:
   st=styles.xpath(f'//w:style[@w:styleId="{name}"]',namespaces=ns)[0]
   assert st.xpath('./w:rPr/w:rFonts/@w:cs',namespaces=ns)==['Noto Sans Arabic']
   assert not any(n.get(W+'val','1') not in ['0','false','off'] for n in st.xpath('./w:rPr/w:b|./w:rPr/w:bCs',namespaces=ns))
  st=styles.xpath('//w:style[@w:styleId="BodyText"]',namespaces=ns)[0];assert st.xpath('./w:pPr/w:spacing/@w:line',namespaces=ns)==['336'];assert st.xpath('./w:pPr/w:ind/@w:right',namespaces=ns)==['1701']
  embed=[n for n in z.namelist() if n.endswith('.odttf')];assert len(embed)==3
  for root in roots[1:]:
   for para in root.xpath('//w:p',namespaces=ns):assert para.xpath('./w:pPr/w:bidi/@w:val',namespaces=ns)==['0']
  tags=[]
  for root in roots:
   for run in root.xpath('//w:r[w:t="HOSPITALITY, IN PERFECT PROPORTION"]',namespaces=ns):assert run.xpath('./w:rPr/w:spacing/@w:val',namespaces=ns)==['38'];assert run.xpath('./w:rPr/w:sz/@w:val',namespaces=ns)==['21'];tags.append(True)
  results.append({'file':p.name,'visible_weight':400,'embedded_regular_fonts':3,'unsupported_glyphs':missing,'body_style_latin_leading_pt':16.8,'body_style_end_indent_mm':30,'explicit_arabic_default':True,'header_footer_ltr_groups':True,'tagline_rule_checked':bool(tags)})
# Current repo source hashes unchanged; approved reused vectors exact.
for x in json.loads((R/'00_source/source_manifest.json').read_text())['sources']:assert hashlib.sha256((R.parent/x['repository_path']).read_bytes()).hexdigest()==x['sha256']
# Current English sample body extraction; count ordinary lines, excluding subject/metadata.
line_checks=[]
for p in (R/'02_pdf').glob('GEM*.pdf'):
 r=PdfReader(p);assert all(abs(float(x.mediabox.width)-595.28)<1 for x in r.pages)
 fonts={str(f.get_object().get('/BaseFont')) for pg in r.pages for f in pg['/Resources'].get('/Font',{}).values()};assert not any('Bold' in f for f in fonts)
 assert '/StructTreeRoot' in r.trailer['/Root'];assert r.trailer['/Root'].get('/Lang')
 if 'English_First' in p.name:
  txt=subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True);body=txt.split('Dear [RECIPIENT NAME],')[1].split('Yours sincerely,')[0];lengths=[len(x.strip()) for x in body.splitlines() if x.strip()];assert max(lengths)<=75;line_checks=lengths
# Same artwork in separately labelled digital/print candidates.
a=PdfReader(R/'02_pdf/GEM_Letterhead_Digital.pdf');b=PdfReader(R/'02_pdf/GEM_Letterhead_Print.pdf');assert len(a.pages)==len(b.pages)==8
assert all(x.get_contents().get_data()==y.get_contents().get_data() for x,y in zip(a.pages,b.pages))
res=json.loads((R/'04_qa/render_results.json').read_text());assert len(res)==len({x['file'] for x in res})
for x in res:assert x['rendered'];assert len(list((R/x['directory']).glob('page-*.png')))==x['pages']
(R/'04_qa/review_checks.json').write_text(json.dumps({'templates':results,'english_sample_body_line_lengths':line_checks,'authoritative_source_hashes_unchanged':True,'digital_print_artwork_identical':True,'rendered_documents':len(res)},indent=2))
print('All verified corrections checked; sample body line lengths:',line_checks)
