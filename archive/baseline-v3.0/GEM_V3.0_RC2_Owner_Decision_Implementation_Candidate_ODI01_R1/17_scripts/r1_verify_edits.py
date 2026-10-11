"""ODI01-R1 edit verifier. Compares each changed XML part of an R1 deck with the ODI01 candidate element-by-element and proves the ONLY differences are:
  (a) <a:rPr b="1"> -> b="0" on runs whose latin typeface is a GEM brand family;
  (b) the exact text edits recorded in the apply log;
  (c) the cloned clarification shapes recorded in the apply log (removed from the comparison).
Also proves every R1 part is well-formed and that no b="1" remains in any slide part.
Usage: r1_verify_edits.py <odi01_candidate_dir> <r1_dir> <apply_log.json> <out_json>"""
import sys,os,re,json,glob,zipfile
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from r1_ooxml import *
odi,r1,logp,outp=sys.argv[1:5];LOG=json.load(open(logp));res={};ok=True
def walk(root): return [e for e in root.iter() if isinstance(e.tag,str)]
for key,tag in (('A','Part A'),('B','Part B'),('C','Part C'),('D','Part D')):
    a=[p for p in glob.glob(odi+'/*.pptx') if f'{tag} — RC2' in p][0];b=[p for p in glob.glob(r1+'/*.pptx') if f'{tag} — RC2' in p][0]
    za,zb=zipfile.ZipFile(a),zipfile.ZipFile(b);r={'members_equal':za.namelist()==zb.namelist(),'changed_parts':[],'problems':[],'per_part':{}}
    texts={(t['part'],t['old'],t['new']) for t in LOG[key]['text']};clones={(c['part'],c['new_shape']) for c in LOG[key]['clone']}
    for n in za.namelist():
        if za.read(n)==zb.read(n): continue
        r['changed_parts'].append(n)
        try: ra=etree.fromstring(za.read(n));rb=etree.fromstring(zb.read(n))
        except Exception as e: r['problems'].append(f'{n}: not well-formed: {e}');continue
        # drop cloned shapes from rb
        removed=0
        for sp in list(rb.iter('{%s}sp'%NS['p'])):
            nm=sp.find('p:nvSpPr/p:cNvPr',NS)
            if (n,nm.get('name')) in clones and nm.get('name') not in [x.get('name') for x in ra.iter('{%s}cNvPr'%NS['p'])]:
                sp.getparent().remove(sp);removed+=1
        ea,eb=walk(ra),walk(rb);pp={'bold_cleared':0,'text_edits':0,'clones':removed}
        if len(ea)!=len(eb): r['problems'].append(f'{n}: element count differs {len(ea)} vs {len(eb)}');continue
        for x,y in zip(ea,eb):
            if x.tag!=y.tag: r['problems'].append(f'{n}: tag mismatch {x.tag}/{y.tag}');break
            ax,ay=dict(x.attrib),dict(y.attrib)
            if ax!=ay:
                if x.tag=='{%s}rPr'%NS['a'] and ax.get('b')=='1' and ay.get('b')=='0' and {k:v for k,v in ax.items() if k!='b'}=={k:v for k,v in ay.items() if k!='b'}:
                    lat=x.find('a:latin',NS)
                    if lat is not None and lat.get('typeface') in BRAND: pp['bold_cleared']+=1
                    else: r['problems'].append(f'{n}: b cleared on non-brand/unknown typeface')
                else: r['problems'].append(f'{n}: unexpected attribute change on {x.tag}: {ax} -> {ay}')
            if (x.text or '')!=(y.text or ''):
                if x.tag=='{%s}t'%NS['a'] and (n,'<a:t>%s</a:t>'%x.text,'<a:t>%s</a:t>'%y.text) in texts: pp['text_edits']+=1
                else: r['problems'].append(f'{n}: unexpected text change {x.text!r} -> {y.text!r}')
        r['per_part'][n]=pp
    left=sum(len(re.findall(r'\bb="1"',zb.read(n).decode())) for n in zb.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n))
    r['remaining_b1_runs_all_slide_parts']=left
    r['totals']={k:sum(v[k] for v in r['per_part'].values()) for k in ('bold_cleared','text_edits','clones')}
    exp_t=sum(t['count'] for t in LOG[key]['text']);exp_c=len(LOG[key]['clone'])
    if r['totals']['text_edits']!=exp_t: r['problems'].append(f'text edits {r["totals"]["text_edits"]} != expected {exp_t}')
    if r['totals']['clones']!=exp_c: r['problems'].append(f'clones {r["totals"]["clones"]} != expected {exp_c}')
    r['kinds_changed']={'slides':[n for n in r['changed_parts'] if '/slides/' in n],'notes':[n for n in r['changed_parts'] if 'notesSlides' in n],'other':[n for n in r['changed_parts'] if '/slides/' not in n and 'notesSlides' not in n]}
    ok&=r['members_equal'] and not r['problems'] and left==0
    res[key]=r;print(key,'changed parts',len(r['changed_parts']),r['totals'],'problems',r['problems'][:3],'remaining b=1',left)
json.dump(res,open(outp,'w'),indent=1,ensure_ascii=False);print('OVERALL','PASS' if ok else 'FAIL');sys.exit(0 if ok else 1)
