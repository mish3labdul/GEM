import re,unicodedata,subprocess,zipfile,sys,json
from collections import Counter
from pypdf import PdfReader
def paras(docx):
    x=zipfile.ZipFile(docx).read('word/document.xml').decode();o=[]
    for p in re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S):
        t=re.sub(r'<w:br[^>]*/>','\n',p);t=''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>|(\n)',t) and [a or b for a,b in re.findall(r'<w:t[^>]*>([^<]*)</w:t>|(\n)',t)])
        if t.strip():o.append(t)
    return o
def norm(s):
    s=re.sub(r'[‎‏‪-‮⁦-⁩؜‌‍]','',s)
    s=unicodedata.normalize('NFKC',s);return re.sub(r'\s+','',s)
def engines(pdf):
    e={}
    e['pypdf']=''.join(p.extract_text() for p in PdfReader(pdf).pages)
    e['pdftotext']=subprocess.check_output(['pdftotext',pdf,'-'],text=True)
    return e
def score(docx,pdf):
    src=paras(docx);res={}
    ar=[s for s in src if re.search('[؀-ۿ]',s)]
    for name,txt in engines(pdf).items():
        pool=Counter(norm(txt));tot=Counter(norm(''.join(src)));
        miss=Counter();extra=Counter()
        need=Counter(norm(''.join(ar)))
        miss=need-pool;extra=pool-Counter(norm(txt) if False else '')
        full=sum(1 for a in ar if norm(a) in norm(txt))
        res[name]={'arabic_paragraphs':len(ar),'paragraphs_exact_in_stream':full,'missing_chars':dict((k,v) for k,v in miss.items())}
    return res
if __name__=='__main__':
    print(json.dumps(score(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=1))
