"""ODI01-R1 before/after render comparison for every slide changed in the OOXML.
Rasterises both PDFs (pdftoppm), writes side-by-side PNGs, and compares word boxes (pdftotext -bbox-layout) per page:
 word count, line count, max word-origin shift, words outside page, new overlaps. LibreOffice output = REVIEW EVIDENCE ONLY (not native PowerPoint).
Usage: r1_render_compare.py <before_dir> <after_dir> <verify.json> <odi01_candidate_dir> <out_dir>   (before/after dirs hold PartA/B/C.pdf)"""
import sys,os,re,json,glob,subprocess,zipfile,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from r1_ooxml import *
from PIL import Image,ImageChops
bd,ad,vj,odi,out=sys.argv[1:6];V=json.load(open(vj));os.makedirs(out,exist_ok=True);rows=[]
def words(pdf,page):
    x=subprocess.run(['pdftotext','-f',str(page),'-l',str(page),'-bbox-layout',pdf,'-'],capture_output=True,text=True).stdout
    W=[(html.unescape(m.group(5)),float(m.group(1)),float(m.group(2)),float(m.group(3)),float(m.group(4))) for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',x)]
    L=len(re.findall('<line ',x));pw=re.search(r'<page width="([\d.]+)" height="([\d.]+)"',x);return W,L,(float(pw.group(1)),float(pw.group(2)))
for key,tag in (('A','Part A'),('B','Part B'),('C','Part C')):
    a=[p for p in glob.glob(odi+'/*.pptx') if f'{tag} — RC2' in p][0];z=zipfile.ZipFile(a);order={p:n for n,p in slide_order(z)}
    slides=sorted(order[p] for p in V[key]['kinds_changed']['slides']);reasons={}
    for p,pp in V[key]['per_part'].items():
        r=[]
        if pp['bold_cleared']: r.append(f"{pp['bold_cleared']} bold flag(s) cleared")
        if pp['text_edits']: r.append(f"{pp['text_edits']} wording edit(s)")
        if pp['clones']: r.append('clarification text box added')
        reasons[order[p]]='; '.join(r)
    for s in slides:
        for lab,d in (('before',bd),('after',ad)): subprocess.run(['pdftoppm','-r','80','-png','-f',str(s),'-l',str(s),f'{d}/Part{key}.pdf',f'{out}/{key}{s:02d}_{lab}'],check=True)
        imgs={lab:Image.open(glob.glob(f'{out}/{key}{s:02d}_{lab}-*.png')[0]).convert('RGB') for lab in ('before','after')}
        w,h=imgs['before'].size;sbs=Image.new('RGB',(w*2+10,h),(255,0,255));sbs.paste(imgs['before'],(0,0));sbs.paste(imgs['after'],(w+10,0));sbs.save(f'{out}/{key}{s:02d}_before_after.png')
        diff=ImageChops.difference(imgs['before'],imgs['after']);bb=diff.getbbox();changed=sum(1 for px in diff.convert('L').getdata() if px>40)
        wb,lb,pg=words(f'{bd}/Part{key}.pdf',s);wa,la,_=words(f'{ad}/Part{key}.pdf',s)
        sb=[x[0] for x in wb];sa=[x[0] for x in wa]
        # words that exist in both: compare box origin by occurrence order
        shifts=[];i=j=0
        import difflib
        sm=difflib.SequenceMatcher(None,sb,sa,autojunk=False)
        for tag_,i1,i2,j1,j2 in sm.get_opcodes():
            if tag_=='equal':
                for k in range(i2-i1): shifts.append(max(abs(wb[i1+k][1]-wa[j1+k][1]),abs(wb[i1+k][2]-wa[j1+k][2])))
        maxs=max(shifts) if shifts else 0;newrows=sum(1 for t,i1,i2,j1,j2 in sm.get_opcodes() if t!='equal')
        outside=[x[0] for x in wa if x[1]<0 or x[3]>pg[0]+0.5 or x[2]<0 or x[4]>pg[1]+0.5]
        # overlap: any two after-words whose boxes overlap by >30% of the smaller area (different lines)
        ov=0
        for p in range(len(wa)):
            for q in range(p+1,min(len(wa),p+60)):
                x1=max(wa[p][1],wa[q][1]);x2=min(wa[p][3],wa[q][3]);y1=max(wa[p][2],wa[q][2]);y2=min(wa[p][4],wa[q][4])
                if x2>x1 and y2>y1:
                    ar=(x2-x1)*(y2-y1);sm_=min((wa[p][3]-wa[p][1])*(wa[p][4]-wa[p][2]),(wa[q][3]-wa[q][1])*(wa[q][4]-wa[q][2]))
                    if sm_>0 and ar/sm_>0.3: ov+=1
        wbov=0
        for p in range(len(wb)):
            for q in range(p+1,min(len(wb),p+60)):
                x1=max(wb[p][1],wb[q][1]);x2=min(wb[p][3],wb[q][3]);y1=max(wb[p][2],wb[q][2]);y2=min(wb[p][4],wb[q][4])
                if x2>x1 and y2>y1:
                    ar=(x2-x1)*(y2-y1);sm_=min((wb[p][3]-wb[p][1])*(wb[p][4]-wb[p][2]),(wb[q][3]-wb[q][1])*(wb[q][4]-wb[q][2]))
                    if sm_>0 and ar/sm_>0.3: wbov+=1
        rows.append(dict(doc=tag,slide=s,reason=reasons.get([k for k in order if order[k]==s][0] and s,''),words_before=len(wb),words_after=len(wa),lines_before=lb,lines_after=la,max_origin_shift_pt=round(maxs,2),text_diff_ops=newrows,words_outside_page=outside,overlaps_before=wbov,overlaps_after=ov,changed_pixels=changed,diff_bbox=bb,sbs=f'{key}{s:02d}_before_after.png'))
json.dump(rows,open(out+'/render_compare.json','w'),indent=1,default=str)
for r in rows: print(r['doc'],r['slide'],'w',r['words_before'],'->',r['words_after'],'lines',r['lines_before'],'->',r['lines_after'],'shift',r['max_origin_shift_pt'],'ops',r['text_diff_ops'],'out',len(r['words_outside_page']),'ov',r['overlaps_before'],'->',r['overlaps_after'])
