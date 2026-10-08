import json,re,subprocess,zipfile,sys,os
from pathlib import Path
D=Path(sys.argv[1]);jobs=json.loads((D/'word_jobs.json').read_text());out={}
def ptext(pdf,i):return subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),'-layout',str(pdf),'-'],text=True)
for jid,r in sorted(jobs.items()):
    if r['rc']!=0:out[jid]={'result':'FAIL','error':r['err'][-160:]};continue
    pdf=D/f'{jid}.pdf';docx=D/f'{jid}.docx'
    n=int(re.search(r'Pages:\s+(\d+)',subprocess.check_output(['pdfinfo',str(pdf)],text=True)).group(1))
    pages=[];okfield=True
    for i in range(1,n+1):
        t=ptext(pdf,i);clean=re.sub(r'[‎‏‪-‮]','',t)
        m=re.search(r'Page\s+(\d+)\s+of\s+(\d+)',clean)
        status='WORKING APPLICATION / PENDING VALIDATION' in clean
        cont=bool(re.search(r'GEM™\s+(\[REFERENCE NUMBER\]|GEM/QA)',clean))
        pages.append({'page':i,'page_field':m.group(0) if m else None,'status':status,'continuation_header':cont})
        okfield&=bool(m) and int(m.group(1))==i and int(m.group(2))==n and status
    fonts=sorted({re.sub(r'^[A-Z]{6}\+','',l.split()[0]) for l in subprocess.check_output(['pdffonts',str(pdf)],text=True).splitlines()[2:]})
    z=zipfile.ZipFile(docx);names=z.namelist()
    st=z.read('word/styles.xml').decode();doc=z.read('word/document.xml').decode()
    hf=''.join(z.read(x).decode() for x in names if re.match(r'word/(header|footer)\d+\.xml',x))
    fields=len(re.findall(r'PAGE',hf))>=1 and 'NUMPAGES' in hf
    emb=[x for x in names if x.endswith('.odttf')];zero=[x for x in emb if z.getinfo(x).file_size==0]
    ft=z.read('word/fontTable.xml').decode()
    embfams=sorted({m.group(1) for m in re.finditer(r'<w:font w:name="([^"]+)">((?:(?!</w:font>).)*?<w:embed)',ft,flags=re.S)})
    styles_ok=all(s in st for s in ['w:styleId="Normal"','w:styleId="BodyText"','w:styleId="Heading1"'])
    cont_ok=all(p['continuation_header'] for p in pages[1:]) and (n==1 or not pages[0]['continuation_header'] or 'Continuation' in jid)
    out[jid]={'pages':n,'page_fields_and_status_every_page':okfield,'continuation_header_pages_2plus':cont_ok,'pdf_fonts':fonts,
              'saved_docx_bytes':docx.stat().st_size,'embedded_font_families':embfams,'zero_byte_font_parts':len(zero),'named_styles_retained':styles_ok,'live_fields_in_saved_docx':fields}
json.dump(out,open(D/'word_analysis.json','w'),indent=1,ensure_ascii=False)
for k,v in out.items():
    if 'error' in v:print('%-34s FAIL %s'%(k,v['error'][-80:]));continue
    print('%-34s p=%d fields=%s cont=%s KB=%d emb=%s zero=%d styles=%s fonts=%s'%(k,v['pages'],v['page_fields_and_status_every_page'],v['continuation_header_pages_2plus'],v['saved_docx_bytes']//1024,v['embedded_font_families'],v['zero_byte_font_parts'],v['named_styles_retained'],','.join(f.split('-')[0] for f in v['pdf_fonts'])))
