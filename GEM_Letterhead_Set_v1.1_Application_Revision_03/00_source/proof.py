from pathlib import Path
import subprocess,concurrent.futures,json,hashlib
from PIL import Image,ImageDraw,ImageChops
from pypdf import PdfReader
R=Path('work/GEM/GEM_Letterhead_Set_v1.1');TMP=Path('work/letterhead_revision_02');OUT=TMP/'pdfproof';OUT.mkdir(exist_ok=True)
BIN='/Users/mediacenter1/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
jobs=[(R/'02_pdf/GEM_Letterhead_Digital.pdf',OUT/'digital')]
for f in (R/'01_templates').glob('*.docx'):jobs.append((TMP/'render'/f.stem/(f.stem+'.pdf'),OUT/f.stem))
def go(item):
 f,out=item;subprocess.run([BIN,'-scale-to','1700','-png',str(f),str(out)],check=True,capture_output=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:list(p.map(go,jobs))
order=['English_First_Page','English_Continuation','Arabic_First_Page','Arabic_Continuation','Bilingual_First_Page','Bilingual_Continuation','Executive','Minimal']
checks=[]
for i,name in enumerate(order):
 a=Image.open(OUT/f'digital-{i+1}.png');b=Image.open(OUT/f'GEM_Letterhead_{name}-1.png');assert ImageChops.difference(a,b).getbbox() is None,name
 a.convert('L').convert('RGB').save(OUT/f'gray-{i+1}.png');checks.append({'template':name,'pdf_mapping_and_tag_repairs_pixel_identical':True})
a=PdfReader(R/'02_pdf/GEM_Letterhead_Digital.pdf');b=PdfReader(R/'02_pdf/GEM_Letterhead_Print.pdf')
assert all(x.get_contents().get_data()==y.get_contents().get_data() for x,y in zip(a.pages,b.pages))
(R/'04_qa/evidence/Visual_Preservation.json').write_text(json.dumps({'print_and_digital_content_streams_identical':True,'pages':checks},indent=2))
groups={'digital':list(OUT.glob('digital-*.png')),'gray':list(OUT.glob('gray-*.png')),'automatic':list((TMP/'render').glob('QA_*_automatic_flow/page-*.png'))}
for label,files in groups.items():
 files=sorted(files)
 for i in range(0,len(files),4):
  s=Image.new('RGB',(1400,2040),'#e8e8e8');dr=ImageDraw.Draw(s)
  for j,f in enumerate(files[i:i+4]):
   im=Image.open(f).convert('RGB');im.thumbnail((675,965));x=j%2*700+12;y=j//2*1020+32;s.paste(im,(x,y));dr.text((x,y-24),f.parent.name+'/'+f.stem,fill='black')
  s.save(OUT/f'{label}-sheet-{i//4+1}.png')
print('PASS: all eight repaired PDFs pixel-identical to DOCX exports; Print artwork identical; grayscale and automatic-flow proofs ready')
