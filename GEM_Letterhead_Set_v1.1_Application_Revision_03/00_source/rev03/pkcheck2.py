"""Native macOS PDFKit (Preview engine) copy/search acceptance against DOCX logical source text.
PASS-full: whole logical line present in PDFKit text. PASS-search: mixed-direction line whose every
directional segment is found by PDFKit findString (visual segmentation only). FAIL otherwise."""
import re,subprocess,sys,json
from lh03 import paras,norm
AR=re.compile(r'[؀-ۿ]')
def segments(line):
    line=re.sub(r'[‎‏]','',line)
    segs=re.findall(r'[؀-ۿ][؀-ۿ\s،«»]*[؀-ۿ»،]|[؀-ۿ]|[^؀-ۿ\s][^؀-ۿ]*[^؀-ۿ\s:]|[^؀-ۿ\s]',line)
    return [s.strip(' :·') for s in segs if len(s.strip(' :·'))>1]
def check(docx,pdf):
    out=subprocess.check_output(['./pk',pdf],text=True);t=norm(out)
    full=[];needsearch=[];res=[]
    for s in paras(docx):
        for line in s.split('\n'):
            if not line.strip():continue
            if norm(line) in t:res.append(('PASS-full',line));continue
            needsearch.append(line)
    if needsearch:
        qs=sorted({g for l in needsearch for g in segments(l)})
        so=subprocess.check_output(['./pk',pdf]+qs,text=True)
        hits={m.group(1):int(m.group(2)) for m in re.finditer(r'SEARCH\[(.*?)\] hits=(\d+)',so)}
        for l in needsearch:
            gs=segments(l);ok=all(hits.get(g,0)>0 for g in gs) and bool(gs)
            res.append(('PASS-search' if ok else 'FAIL',l,{g:hits.get(g,0) for g in gs}))
    return res
if __name__=='__main__':
    print(json.dumps(check(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=1))
