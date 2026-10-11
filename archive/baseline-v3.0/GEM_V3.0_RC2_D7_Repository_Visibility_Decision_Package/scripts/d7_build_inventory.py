"""D7: object-level inventory of what a branch-only push of claude/gem-worktree-safety-30b559 would ADD to origin (mish3labdul/GEM).
'Already on remote' = the blob SHA is in the object set reachable from origin/main, origin/claude/pensive-mayer-s1xbmb and every refs/pull/*/head held locally.
Sensitivity columns are RULE-BASED labels (LOW/MEDIUM/HIGH) for decision preparation, not legal conclusions. Read-only.
Usage: d7_build_inventory.py <repo_root> <origin_objects.txt> <out_csv> <out_json>"""
import sys,os,subprocess,csv,json,collections
root,objs,out,outj=sys.argv[1:5]
git=lambda *a:subprocess.run(['git','-C',root]+list(a),capture_output=True,text=True,check=True).stdout
ORIG=set(open(objs).read().split())
PKG='GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1'
tree=git('ls-tree','-r','-l','-z','HEAD','--',PKG).split('\0')
rows=[]
for e in tree:
    if not e: continue
    meta,path=e.split('\t',1);mode,typ,sha,size=meta.split(None,3);size=int(size)
    ext=os.path.splitext(path)[1].lower();rel=path[len(PKG)+1:];low=rel.lower()
    deck='deck_candidates/' in rel and ext in('.pptx',)
    pdfdeck='deck_candidates/' in rel and ext=='.pdf'
    tok=os.path.basename(rel).startswith('gem-tokens.') and ext in('.json','.css')
    render=rel.startswith('18_qa_evidence/render/')
    gitev=rel.startswith('18_qa_evidence/git_evidence') or 'main_ref_movement' in rel or 'push_readiness' in rel
    script=rel.startswith('17_scripts/')
    partd='part d' in low
    typ_={'.pptx':'PPTX deck (editable)','.pdf':'PDF export','.png':'PNG render','.json':'JSON','.css':'CSS','.csv':'CSV','.md':'Markdown','.py':'Python script','.txt':'Text'}.get(ext,ext or 'other')
    # editable/source
    if deck: es='Yes — editable deck source'
    elif tok: es='Yes — editable token source'
    elif script: es='Yes — script source'
    elif ext in('.md','.csv','.json','.txt'): es='Yes — editable text/data'
    else: es='No — rendered/derived'
    # IP sensitivity
    if deck: ip='HIGH'
    elif tok: ip='HIGH'
    elif pdfdeck: ip='MEDIUM'
    elif render: ip='MEDIUM'
    elif script or rel.startswith('18_qa_evidence') or ext in('.md','.csv'): ip='LOW'
    else: ip='LOW'
    # rights dependency
    if deck or pdfdeck: rd='Logos/marks (VAL-03, VAL-04); fonts named/embedded (VAL-05, VAL-19)'+('; AI-generated concept imagery (VAL-06)' if partd else '')+'; master acceptance (VAL-02)'
    elif tok: rd='Font families and weights (VAL-05, VAL-19); palette/brand marks derived from the brand system (VAL-03, VAL-04)'
    elif render: rd='Derived from decks: logos (VAL-03, VAL-04), fonts (VAL-05)'
    else: rd='None directly (describes rights gates)' if (rel[:2] in ('03','05','14') or '14_' in rel) else 'None'
    # governance sensitivity
    gtxt=rel[:2] in('01','02','03','04','05','07','12','14','15','16') and ext=='.md' or gitev or rel.startswith('18_qa_evidence/main_') 
    if gitev: gs='MEDIUM — local machine paths, identity and Git internals'
    elif gtxt: gs='HIGH — internal decisions, open gates, validation gaps, owner decisions'
    elif script or ext in('.csv','.json') and rel.startswith('18_qa_evidence'): gs='MEDIUM — QA method and results; reveals validation gaps'
    elif deck or pdfdeck or tok: gs='MEDIUM — unapproved candidate content labelled UNAPPROVED / NOT RELEASED'
    elif render: gs='LOW — images of candidate slides'
    else: gs='LOW'
    notes=''
    if deck: notes=('Unpublished visual candidate; byte-identical copy of ODI01 Part D deck (adds a candidate-named object)' if partd and 'Part D' in rel else 'Unpublished visual candidate derived from the public release deck; differs by D5 edits')
    elif pdfdeck: notes='Unpublished PDF export of an unapproved candidate'
    elif tok: notes='Candidate token package (status-reduced; 500-weight descriptions); derives from public tokens'
    elif rel.startswith('02_Preflight'): notes='Contains absolute local file-system paths and delivered-package hashes'
    elif gitev: notes='Raw Git evidence including local absolute paths, committer identity (noreply) and ref history'
    elif rel.startswith('18_qa_evidence/render'): notes='Side-by-side before/after slide render'
    elif rel.startswith('19_candidate_documents/partd') or 'd3a_carried' in rel or 'register_adoption' in rel: notes='Candidate prose / carried-forward record (D3A and register adoption)'
    rows.append(dict(Path=path,Type=typ_,Size=size,**{'Already on remote?':'Yes' if sha in ORIG else 'No','New exposure?':'No' if sha in ORIG else 'Yes','Editable/source?':es,'IP sensitivity':ip,'Rights dependency':rd,'Governance sensitivity':gs,'Notes':notes}))
H=['Path','Type','Size','Already on remote?','New exposure?','Editable/source?','IP sensitivity','Rights dependency','Governance sensitivity','Notes']
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=H);w.writeheader();w.writerows(rows)
new=[r for r in rows if r['New exposure?']=='Yes']
by=collections.Counter();bs=collections.Counter()
for r in new: by[r['Type']]+=1;bs[r['Type']]+=r['Size']
sm=dict(files=len(rows),new_files=len(new),new_bytes=sum(r['Size'] for r in new),already_on_remote=len(rows)-len(new),by_type={k:[by[k],bs[k]] for k in by},
 editable_new=sum(1 for r in new if r['Editable/source?'].startswith('Yes')),high_ip_new=[r['Path'].split('/')[-1] for r in new if r['IP sensitivity']=='HIGH'],
 git=dict(commits_new=int(git('rev-list','--count','HEAD','--not',*[l for l in open('/tmp/_origin_tips.txt').read().split()]).strip()),objects_new=len([l for l in subprocess.run(['git','-C',root,'rev-list','--objects','HEAD','--not']+open('/tmp/_origin_tips.txt').read().split(),capture_output=True,text=True).stdout.splitlines() if l])))
json.dump(sm,open(outj,'w'),indent=1);print(json.dumps(sm,indent=1)[:1400])
