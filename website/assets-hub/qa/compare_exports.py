"""Compare all A/B fallback pages with native PowerPoint exports; inspect sheets manually."""
from pathlib import Path
import json
import fitz
from PIL import Image, ImageDraw, ImageChops, ImageStat

root = Path(__file__).resolve().parents[1]
out = root / 'qa/screenshots/export-comparison'
out.mkdir(parents=True, exist_ok=True)
report = []
for letter, name in [('a','BrandGuidelines'),('b','DigitalDesignSystem')]:
    native = fitz.open(root / f'reading-copies/part-{letter}.pdf')
    fallback = fitz.open(root / f'lo-fonts-trial/GEM_BRAND_{name}_Part{letter.upper()}_v3.0_20261009.pdf')
    assert len(native) == len(fallback)
    cards = []
    for i, (n, f) in enumerate(zip(native, fallback)):
        images=[]
        for page in [n,f]:
            pix = page.get_pixmap(matrix=fitz.Matrix(0.5,0.5), alpha=False)
            images.append(Image.frombytes('RGB',[pix.width,pix.height],pix.samples))
        diff=ImageStat.Stat(ImageChops.difference(*images)).mean
        card=Image.new('RGB',(960,292),'#ffffff')
        draw=ImageDraw.Draw(card)
        draw.text((8,4),f'Part {letter.upper()} / {i+1} — native PowerPoint | LibreOffice',fill='black')
        card.paste(images[0],(0,22));card.paste(images[1],(480,22));cards.append(card)
        fonts=sorted({f[3].split('+')[-1] for f in f.get_fonts()})
        text=f.get_text()
        report.append({'part':letter,'page':i+1,'pixelDifferenceMean':round(sum(diff)/3,2),'fonts':fonts,'replacementCharacters':text.count('\ufffd'),'textCharacters':len(text)})
    for start in range(0,len(cards),8):
        sheet=Image.new('RGB',(1920,1168),'#ddd')
        for k,card in enumerate(cards[start:start+8]):sheet.paste(card,((k%2)*960,(k//2)*292))
        sheet.save(out / f'{letter}-{start+1:02d}.jpg',quality=90)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'pagesCompared':len(report),'worstDifferences':sorted(report,key=lambda x:x['pixelDifferenceMean'],reverse=True)[:10]},indent=2))
