"""D3B: build BOTH X12 mappings on the same asset set; change only the STREAM token. NO source file is renamed; NO asset-ID or checksum rule is invented.
Assumptions (each labelled A1..A4 in the CSV; none is a naming rule): A1 ASSET value = the kit's shape word in the Title-case style of the Part A example (Horizontal, Stacked, Symbol, SymbolNoSpark);
A2 VARIANT value = colour word (Ink, Beige, Black, White) as in the Part A example, plus the kit's own qualifiers (clearspace 2u, pixel size) appended, because the pattern has one VARIANT field and Part C allows Latin letters and digits only;
A3 vX.Y and YYYYMMDD stay as the pattern's literal placeholders (version and manifest issue date are undecided); A4 extension = the source extension.
Usage: d3_x12_mapping.py <repo_root> <out_dir>"""
import sys,os,re,csv,json,hashlib,collections,glob
root,out=sys.argv[1:3]
K='GEM_Brand_Assets_v1.0/04_official_kit/logo'
sha=lambda p:hashlib.sha256(open(os.path.join(root,p),'rb').read()).hexdigest()
RX=re.compile(r'^gem-(horizontal|stacked|symbol-nospark|symbol)-(ink|beige|black|white)(-clearspace-2u)?(?:-(\d+))?\.(svg|pdf|eps|png)$')
SHAPE={'horizontal':'Horizontal','stacked':'Stacked','symbol':'Symbol','symbol-nospark':'SymbolNoSpark'}
files=sorted(os.path.relpath(os.path.join(d,n),root) for d,_,fn in os.walk(os.path.join(root,K)) for n in fn)
rows=[];skipped=[]
for p in files:
    n=os.path.basename(p);m=RX.match(n)
    if not m: skipped.append(p);continue
    shp,col,cs,px,ext=m.groups()
    asset=SHAPE[shp];var=col.capitalize()+('Clearspace2u' if cs else '')+(px or '')
    rows.append(dict(path=p,name=n,sha=sha(p),fmt=ext.upper(),shape=asset,colour=col.capitalize(),asset=asset,variant=var,ext=ext,
        qual=('2u clearspace' if cs else '')+((' ' if cs and px else '')+(px+' px' if px else ''))))
assert len(rows)==128 and skipped==[K+'/metrics.json'],(len(rows),skipped)
def build(stream,noun):
    res=[]
    for r in rows:
        a=('Logo'+r['asset']) if noun else r['asset']
        res.append(f"GEM_{stream}_{a}_{r['variant']}_vX.Y_YYYYMMDD.{r['ext']}")
    return res
OPT={'BRAND':('BRAND',build('BRAND',False),build('BRAND',True)),'Logo':('Logo',build('Logo',False),build('Logo',True))}
# existing X12-shaped working files (01_svg) for collision testing
existing=[os.path.basename(p) for p in glob.glob(os.path.join(root,'GEM_Brand_Assets_v1.0/01_svg/*.svg'))]
ex_triples={tuple(re.match(r'^GEM_([^_]+)_([^_]+)_(.+)_v0\.1_\d{8}\.svg$',e).groups()) for e in existing}
H=['Source path (unchanged)','Source filename (unchanged)','SHA-256 of source','Format','Shape','Colour','Qualifier (kit token)','STREAM','ASSET','VARIANT','Controlled name — exact X12 pattern','Controlled name if ASSET carried the noun "Logo" (readability test only)','Assumptions applied']
stats={}
for key,(stream,names,names_noun) in OPT.items():
    fn=os.path.join(out,{'BRAND':'05_D3B_X12_BRAND_Mapping.csv','Logo':'06_D3B_X12_Logo_Mapping.csv'}[key])
    with open(fn,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(H)
        for r,nm,nn in zip(rows,names,names_noun): w.writerow([r['path'],r['name'],r['sha'],r['fmt'],r['shape'],r['colour'],r['qual'],stream,r['asset'],r['variant'],nm,nn,'A1 A2 A3 A4'])
        w.writerow([K+'/metrics.json','metrics.json',sha(K+'/metrics.json'),'JSON','','','','','','','NOT MAPPED — data file used by the kit, not a brand asset; manifest-only','','—'])
    low=[n.lower() for n in names]
    triples={(stream,r['asset'],r['variant']) for r in rows}
    stats[key]=dict(stream=stream,files=len(names),unique=len(set(names)),unique_case_insensitive=len(set(low)),max_len=max(map(len,names)),min_len=min(map(len,names)),
        stream_in_asset=sum(1 for r in rows if stream.lower() in r['asset'].lower()),stream_in_asset_if_noun=sum(1 for r in rows if stream.lower() in ('Logo'+r['asset']).lower()),
        collisions_with_existing_working_names=len(triples&ex_triples),charset_ok=all(re.fullmatch(r'GEM_[A-Za-z0-9]+_[A-Za-z0-9]+_[A-Za-z0-9]+_vX\.Y_YYYYMMDD\.(svg|pdf|eps|png)',n) for n in names),
        sample=names[:1]+[n for n,r in zip(names,rows) if r['asset']=='SymbolNoSpark' and r['variant']=='Ink' and r['ext']=='svg'])
stats['existing_working_files']=existing;stats['kit_logo_files_mapped']=len(rows)
stats['by_shape']=dict(collections.Counter(r['asset'] for r in rows));stats['by_format']=dict(collections.Counter(r['fmt'] for r in rows))
json.dump(stats,open(os.path.join(out,'11_QA_Evidence','d3b_mapping_stats.json'),'w'),indent=1)
print(json.dumps({k:v for k,v in stats.items() if k in('BRAND','Logo','by_shape','by_format')},indent=1)[:1800])
