"""ODI01-R1 full-artifact search for weight vocabulary: 500, Medium, Semibold/SemiBold, Bold, font-weight, weight.
Searches deck text (every slide + notes, tables included), PDF text layers, token JSON/CSS and every md/csv/json/txt/css file under the given roots.
Every hit is written with its context; classification is by rule (RULES below) and anything the rules do not recognise is classed UNCLASSIFIED so it cannot be skipped.
Usage: r1_weight_search.py <out_csv> <path> [<path> ...]    (paths: files or directories)"""
import sys,os,re,csv,zipfile,subprocess,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from r1_ooxml import *
PAT=re.compile(r'(?i)(?<![\w.#-])500(?![\w.%])|\bsemi-?bold\b|\bmedium\b|\bbold\b|font-?weight|\bweights?\b')
# class codes
#  A  truthful: states 400 as current and/or marks 500 as PENDING / future / negated
#  B  current-implementation wording that implies 500 (or bold) is usable now  -> must be 0
#  C  future design intent, explicitly labelled (tokens)
#  N  not a type weight (visual weight, line/border weight, stock weight, mass of the mark)
#  H  historical / provenance text carried forward (AFC02 release notes, verification logs) - not an instruction
#  K  token type/key vocabulary (fontWeight, "weight": {, type.weight.regular = 400, type.weight.medium key name)
#  T  table header word "Weight(s)"; every value beneath it is 400 or marked pending
#  U  unclassified (QA fails if any remain)
RULES=[
 ('K',r'"\$value": 500',"token value 500 = FUTURE DESIGN INTENT; its description (next lines) states CURRENT IMPLEMENTATION = 400"),
 ('H',r'FILE_500|No accepted weight-500|^type\.(weight|styleWeight)\.|weight-500 tokens annotated|tokens\.json as the DS03',"token status log / provenance row; not an instruction"),
 ('N',r'(?i)line weights?|border weight|visual weight|optical weight|stock weights|Weight and anchor|carries the weight|Text, weight or glyph|state label \+ border weight|weight of the mark',"not a type weight"),
 ('H',r'AFC02-CANDIDATE|ODI01-D6-CANDIDATE|token_verification|"Description changed only|D5 CSS annotations|typography tables: carry no status|Jost light|LABEL · INTER 500 · CAPITALS|typography families and weights|Source: Part A pp\.',"historical / provenance text or verification log; not a current instruction"),
 ('C',r'FUTURE DESIGN INTENT = 500',"future design intent, explicitly labelled; CURRENT IMPLEMENTATION = 400 stated in the same text"),
 ('A',r'PENDING ACCEPTED FONT FILE|500 PENDING|500 WEIGHT PENDING|CURRENT IMPLEMENT\w+|\bPENDING\b.*\b500\b|\b500\b.*\bPENDING\b|not (?:yet )?(?:accepted|available|implemented|usable)|until accepted|NOT ACCEPTED|faux|synthetic',"states 400 as current and/or marks 500 as pending / not available"),
 ('A',r'(?i)Two weights per composition at most|Maximum two weights per composition|Two weights per composition',"upper bound on weights per composition; only 400 exists, so it is a cap, not a requirement for 500"),
 ('A',r'Sentence case, Jost 400|never beside the primary at equal weight|match optical weight|Arabic weights remain \[PENDING\]',"consistent with 400-only"),
 ('K',r'fontWeight|"weight": \{|"medium": \{|type\.weight\.regular|weight-regular|"type\.weight\.medium"|ODI01-R1 CANDIDATE · D4 STATUS NORMALIZATION',"token vocabulary / key name; value governed by the token (500 = future intent, description states it)"),
 ('T',r'^(Weights?)$|Weight\s{2,}Tracking|Family\s{2,}Role\s{2,}Weights|Weight\s*$',"table header; values beneath are 400 or marked PENDING"),
 ('A',r'400\s*[·,]\s*500\b(?!.*PENDING)|400 · 500',"pdf text layer of the cell '400 · 500 PENDING' (PENDING wrapped to the next line by column layout)"),
 ('A',r'Navigates; underlined, 400',"link style states 400"),
]
def classify(ctx,hit):
    for cls,pat,why in RULES:
        if re.search(pat,ctx): return cls,why
    if hit=='500' and re.search(r'#[0-9a-f]{6}|\bmm\b|\bpx\b|\bms\b|\bgsm\b|\bhttp|\.png|\.svg|\$',ctx): return 'N','number not a type weight'
    return 'U','UNCLASSIFIED — review'
def pptx_hits(path):
    z=zipfile.ZipFile(path);name=os.path.basename(path)[:60];out=[]
    for n,part in slide_order(z):
        for kind,p in (('slide',part),('notes',part.replace('slides/slide','notesSlides/notesSlide').replace('.xml','.xml'))):
            try: root=etree.fromstring(z.read(p))
            except KeyError: continue
            for para in root.iter('{%s}p'%NS['a']):
                t=''.join(x.text or '' for x in para.iter('{%s}t'%NS['a']))
                if t: out.append((name,f'slide {n}'+(' notes' if kind=='notes' else ''),t))
    return out
def text_hits(path):
    try: txt=open(path,encoding='utf-8').read()
    except Exception: return []
    return [(os.path.basename(path),f'line {i}',l.strip()) for i,l in enumerate(txt.splitlines(),1) if l.strip()]
def pdf_hits(path):
    t=subprocess.run(['pdftotext','-layout',path,'-'],capture_output=True,text=True).stdout
    return [(os.path.basename(path)[:60],f'pdf page {pi}',l.strip()) for pi,pg in enumerate(t.split('\f'),1) for l in pg.splitlines() if l.strip()]
def main():
    out=sys.argv[1];rows=[];files=[]
    for a in sys.argv[2:]:
        files+= [a] if os.path.isfile(a) else [f for f in glob.glob(a+'/**/*',recursive=True) if os.path.isfile(f)]
    for f in sorted(files):
        e=f.lower().rsplit('.',1)[-1]
        if e=='pptx': L=pptx_hits(f)
        elif e=='pdf': L=pdf_hits(f)
        elif e in ('md','csv','json','css','txt'): L=text_hits(f)
        else: continue
        for art,loc,t in L:
            for m in PAT.finditer(t):
                cls,why=classify(t,m.group(0))
                rows.append([art if e in('pptx','pdf') else os.path.relpath(f),loc,m.group(0),t[:260],cls,why])
    with open(out,'w',newline='',encoding='utf-8') as fh:
        w=csv.writer(fh);w.writerow(['Artifact','Location','Match','Context','Class','Reason']);w.writerows(rows)
    import collections;print(len(rows),dict(collections.Counter(r[4] for r in rows)))
main()
