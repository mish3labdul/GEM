from pathlib import Path
import subprocess,json,hashlib,re
from PIL import Image,ImageDraw
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
repo=root.parents[1]
manifest=json.loads((root/'dist/manifest.json').read_text())
out=root/'qa/screenshots/documents';out.mkdir(parents=True,exist_ok=True)
report=[]
for d in manifest['documents']:
    p=root/'dist'/d['pdf']
    r=PdfReader(p)
    assert len(r.pages)==d['pages']
    assert hashlib.sha256((repo/d['original']).read_bytes()).hexdigest()==d['originalSha256']
    font_lines=subprocess.check_output(['pdffonts',str(p)],text=True).splitlines()[2:]
    assert all('yes' in line for line in font_lines)
    texts=[]
    for i in range(1,d['pages']+1):
        text=subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),str(p),'-'],text=True)
        assert '\ufffd' not in text
        assert len(text.strip())>4, f'{d["id"]} {i}: empty'
        texts.append(text)
    for i in d['arabicSlides']:
        assert any('\u0600'<=c<='\u06ff' for c in texts[i-1])
        assert not re.search(r'\u066e[(&]',texts[i-1]),f'{d["id"]} {i}: corrupt extraction'
    prefix=out/d['id']
    subprocess.run(['pdftoppm','-scale-to','640','-jpeg','-jpegopt','quality=85',str(p),str(prefix)],check=True,capture_output=True)
    pages=sorted(out.glob(d['id']+'-*.jpg'),key=lambda f:int(f.stem.rsplit('-',1)[1]))
    assert len(pages)==d['pages']
    for start in range(0,len(pages),12):
        sheet=Image.new('RGB',(1920,1544),'#eee');draw=ImageDraw.Draw(sheet)
        for offset,filename in enumerate(pages[start:start+12]):
            x=(offset%3)*640;y=(offset//3)*386
            draw.text((x+8,y+4),f'{d["id"]} / {start+offset+1}',fill='black')
            with Image.open(filename) as im:sheet.paste(im,(x,y+26))
        sheet.save(out/f'sheet-{d["id"]}-{start+1:03d}.jpg',quality=92)
    report.append({'id':d['id'],'pages':len(r.pages),'bytes':p.stat().st_size,'pdfSha256':d['pdfSha256'],'allPagesRendered':True,'replacementCharacters':0,'fonts':sorted(set(line.split()[0].split('+')[-1] for line in font_lines)),'arabicSlides':d['arabicSlides'],'sourceHashMatches':True})
(root/'qa/document-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
