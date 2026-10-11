"""D3 package MANIFEST.json / SHA256SUMS.txt (neither hashes itself; SHA256SUMS.txt also covers MANIFEST.json).
Usage: d7_manifest.py generate <pkg_dir> | verify <pkg_dir>"""
import sys,os,json,hashlib,subprocess
mode,pkg=sys.argv[1],os.path.abspath(sys.argv[2])
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
SELF={'MANIFEST.json','SHA256SUMS.txt'}
files=sorted(os.path.relpath(os.path.join(d,n),pkg) for d,_,fn in os.walk(pkg) for n in fn if n!='.DS_Store' and os.path.relpath(os.path.join(d,n),pkg) not in SELF)
if mode=='generate':
    g=lambda *a:subprocess.run(['git','-C',pkg]+list(a),capture_output=True,text=True).stdout.strip()
    M={'package':os.path.basename(pkg),'purpose':'D3 owner decision package: D3A implemented as candidates; D3B owner decision required','status':'D3A IMPLEMENTED IN CANDIDATE · D3B OWNER DECISION REQUIRED · D7 PENDING (NO PUSH) · AC20 OPEN',
       'release_label':'GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE','created':'2026-10-09','branch':g('branch','--show-current'),
       'based_on_head':'ab6d886','pushed':False,'merged':False,'published':False,'pr_opened':False,'repository_setting_changed':False,'authoritative_originals_modified':False,'d3a':'IMPLEMENTED IN CANDIDATE (C1–C4)','d3b':'OWNER DECISION REQUIRED',
       'self_hash_policy':'MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.',
       'files':[{'path':f,'bytes':os.path.getsize(os.path.join(pkg,f)),'sha256':sha(os.path.join(pkg,f))} for f in files]}
    json.dump(M,open(pkg+'/MANIFEST.json','w'),indent=1,ensure_ascii=False)
    open(pkg+'/SHA256SUMS.txt','w',encoding='utf-8').write(''.join(f"{sha(os.path.join(pkg,f))}  {f}\n" for f in sorted(files+['MANIFEST.json'])))
    print(len(files),'files in manifest')
else:
    import re
    prob=[];ok=0;listed=set()
    for l in open(pkg+'/SHA256SUMS.txt',encoding='utf-8'):
        m=re.match(r'^([0-9a-f]{64})  (.+)$',l.rstrip('\n'))
        if not m: prob.append('unparsed');continue
        h,rel=m.groups();listed.add(rel)
        if rel=='SHA256SUMS.txt': prob.append('self-listed')
        elif os.path.exists(os.path.join(pkg,rel)) and sha(os.path.join(pkg,rel))==h: ok+=1
        else: prob.append('mismatch/missing '+rel)
    M=json.load(open(pkg+'/MANIFEST.json'));mf={f['path']:f for f in M['files']}
    if set(mf)!=set(files): prob.append('manifest file set differs from disk')
    for r,f in mf.items():
        p=os.path.join(pkg,r)
        if not os.path.exists(p) or sha(p)!=f['sha256'] or os.path.getsize(p)!=f['bytes']: prob.append('manifest mismatch '+r)
    if listed!=set(files)|{'MANIFEST.json'}: prob.append('sums list differs from disk')
    for k in ('pushed','merged','published','pr_opened','repository_setting_changed','authoritative_originals_modified'):
        if M[k]: prob.append(k+' true')
    print(f'SHA256SUMS verified {ok}; manifest files {len(mf)}; problems={prob}');sys.exit(1 if prob else 0)
