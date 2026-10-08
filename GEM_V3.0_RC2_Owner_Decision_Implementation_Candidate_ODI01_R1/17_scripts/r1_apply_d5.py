"""ODI01-R1 D5 implementation: targeted OOXML edits to the ODI01 candidate decks (every other zip member is copied byte-for-byte).
 1. every explicit bold flag on a GEM brand-font text run (Jost / Inter / Noto Sans Arabic) b="1" -> b="0"  (400 only; no faux bold)
 2. exact-match wording edits so no slide implies that weight 500 is usable now
 3. three cloned clarification text boxes (CURRENT IMPLEMENTATION = 400 / 500 PENDING ACCEPTED FONT FILE) placed before the footer in reading order
Usage: r1_apply_d5.py <odi01_candidate_dir> <out_dir> <log_json>"""
import sys,os,re,json,glob,zipfile,hashlib
src,out,logp=sys.argv[1:4]
BRAND=('Jost','Inter','Noto Sans Arabic')
sha=lambda b:hashlib.sha256(b).hexdigest()
PEND='500 PENDING ACCEPTED FONT FILE'
# (deck key, part, old, new, count expected, reason)
TEXT=[
 ('A','ppt/slides/slide35.xml','<a:t>EMPHASIS · INTER 500</a:t>','<a:t>EMPHASIS · INTER 400 · 500 PENDING</a:t>',1,'D5: specimen label named an unavailable weight as current'),
 ('B','ppt/slides/slide10.xml','<a:t>500 PENDING</a:t>','<a:t>400 · 500 PENDING</a:t>',1,'D5: table cell now states the current implemented weight'),
 ('B','ppt/slides/slide12.xml','<a:t>500</a:t>','<a:t>400</a:t>',2,'D5: Arabic hierarchy rows arabicH3 and arabicLabel show current implementation = 400'),
 ('B','ppt/slides/slide22.xml','<a:t>Navigates; underlined, 500, ink</a:t>','<a:t>Navigates; underlined, 400, ink</a:t>',1,'D5: link style at 400; underline remains the functional cue'),
]
# (deck key, part, anchor shape name (clone source and insert-after), new name, off x, off y, ext cx, ext cy, text, reason)
CLONE=[
 ('B','ppt/slides/slide10.xml','Text 5','Text 7',8102600,3159473,3374898,678000,'CURRENT IMPLEMENTATION: 400 for every row. 500: PENDING ACCEPTED FONT FILE.','D5: stops the Weight column being read as permission to use 500'),
 ('B','ppt/slides/slide12.xml','Text 3','Text 5',812800,5650000,10883392,452041,'Wt column = current implementation weight: 400 only. arabicH3 and arabicLabel carry 500 as FUTURE DESIGN INTENT; 500 PENDING ACCEPTED FONT FILE.','D5: separates future design intent from current implementation for Arabic rows'),
 ('C','ppt/slides/slide15.xml','Text 5','Text 8',812800,4250000,10883392,467320,'CURRENT IMPLEMENTED WEIGHT = 400 (Jost, Inter). 500 is PENDING ACCEPTED FONT FILE and is not available to any current build. Noto Sans Arabic weights remain [PENDING].','D5: makes "400 · 500 PENDING" unambiguous'),
]
RUN=re.compile(r'<a:r>(?:(?!</a:r>).)*</a:r>',re.S)
def unbold(x,part,log):
    n=0;other=0
    def f(m):
        nonlocal n,other
        r=m.group(0);mm=re.match(r'<a:r><a:rPr\b[^>]*>',r)
        if not mm or not re.search(r'\bb="1"',mm.group(0)): return r
        lat=re.search(r'<a:latin typeface="([^"]+)"',r)
        if not lat: raise SystemExit(f'{part}: bold run without explicit latin typeface — stop and review: {r[:200]}')
        if lat.group(1) not in BRAND: other+=1;return r
        n+=1;return r.replace(mm.group(0),mm.group(0).replace(' b="1"',' b="0"',1),1)
    x2=RUN.sub(f,x);log.append({'part':part,'brand_runs_unbolded':n,'non_brand_bold_left':other});return x2
def clone(x,anchor,newname,ox,oy,cx,cy,text):
    sps=[m for m in re.finditer(r'<p:sp>.*?</p:sp>',x,re.S) if re.search(r'<p:cNvPr id="\d+" name="%s"/>'%re.escape(anchor),m.group(0))]
    assert len(sps)==1,(anchor,len(sps))
    s=sps[0].group(0);assert s.count('<a:r>')==1
    nid=max(map(int,re.findall(r'<p:cNvPr id="(\d+)"',x)))+1
    t=re.sub(r'<p:cNvPr id="\d+" name="[^"]*"/>',f'<p:cNvPr id="{nid}" name="{newname}"/>',s,count=1)
    t=re.sub(r'<a:off x="\d+" y="\d+"/><a:ext cx="\d+" cy="\d+"/>',f'<a:off x="{ox}" y="{oy}"/><a:ext cx="{cx}" cy="{cy}"/>',t,count=1)
    t=re.sub(r'<a:t>[^<]*</a:t>',lambda m:'<a:t>'+text.replace('&','&amp;').replace('<','&lt;')+'</a:t>',t,count=1)
    return x[:sps[0].end()]+t+x[sps[0].end():]
def build(key,srcf,dst):
    zin=zipfile.ZipFile(srcf);data={i.filename:zin.read(i.filename) for i in zin.infolist()};new=dict(data);log={'source_sha256':sha(open(srcf,'rb').read()),'unbold':[],'text':[],'clone':[]}
    for p in sorted(n for n in data if re.match(r'ppt/slides/slide\d+\.xml$',n)):
        x=data[p].decode('utf-8')
        if re.search(r'\bb="1"',x): new[p]=unbold(x,p,log['unbold']).encode('utf-8')
    for k,p,old,newt,cnt,why in TEXT:
        if k!=key: continue
        x=new[p].decode('utf-8');assert x.count(old)==cnt,(key,p,old,x.count(old));new[p]=x.replace(old,newt).encode('utf-8');log['text'].append({'part':p,'old':old,'new':newt,'count':cnt,'reason':why})
    for k,p,anc,nn,ox,oy,cx,cy,t,why in CLONE:
        if k!=key: continue
        new[p]=clone(new[p].decode('utf-8'),anc,nn,ox,oy,cx,cy,t).encode('utf-8');log['clone'].append({'part':p,'after_shape':anc,'new_shape':nn,'text':t,'reason':why})
    with zipfile.ZipFile(dst,'w') as zo:
        for i in zin.infolist():
            zi=zipfile.ZipInfo(i.filename,i.date_time);zi.compress_type=i.compress_type;zi.external_attr=i.external_attr
            zo.writestr(zi,new[i.filename])
    z2=zipfile.ZipFile(dst);log['parts_changed']=[n for n in data if z2.read(n)!=data[n]];log['out_sha256']=sha(open(dst,'rb').read());return log
os.makedirs(out,exist_ok=True);LOG={}
for key,tag in (('A','Part A'),('B','Part B'),('C','Part C'),('D','Part D')):
    s=[p for p in glob.glob(src+'/*.pptx') if f'{tag} — RC2 — ODI01 CANDIDATE' in p][0]
    d=os.path.join(out,os.path.basename(s).replace('ODI01 CANDIDATE','ODI01-R1 CANDIDATE'))
    LOG[key]=build(key,s,d);LOG[key]['out']=os.path.basename(d);print(key,LOG[key]['parts_changed'],sum(u['brand_runs_unbolded'] for u in LOG[key]['unbold']),'runs unbolded')
json.dump(LOG,open(logp,'w'),indent=1,ensure_ascii=False)
