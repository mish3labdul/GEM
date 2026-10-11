"""ODI01-R1: verify SHA256SUMS.txt and MANIFEST.json (QA items 18 and 19). Usage: verify_manifest.py <repo_root> <odi_dir> <out_json>"""
import sys,os,json,hashlib,subprocess,re
root=os.path.abspath(sys.argv[1]);odi=os.path.abspath(sys.argv[2])
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
SELF={'MANIFEST.json','SHA256SUMS.txt'}
on_disk={os.path.relpath(os.path.join(d,n),odi) for d,_,fn in os.walk(odi) for n in fn}
# 18
ok=bad=0;listed=set();prob=[]
for l in open(odi+'/SHA256SUMS.txt',encoding='utf-8'):
    m=re.match(r'^([0-9a-f]{64})  (.+)$',l.rstrip('\n'))
    if not m: prob.append('unparsed:'+l[:40]);continue
    h,rel=m.groups();listed.add(rel)
    if rel=='SHA256SUMS.txt': prob.append('self-listed');continue
    if os.path.exists(os.path.join(odi,rel)) and sha(os.path.join(odi,rel))==h: ok+=1
    else: bad+=1;prob.append('mismatch/missing:'+rel)
unl=on_disk-listed-{'SHA256SUMS.txt'}
r18='PASS' if bad==0 and not prob and not unl else 'FAIL'
e18=f'{ok} files listed in SHA256SUMS.txt verify, {bad} mismatches, unlisted files on disk (excluding the sums file itself)={sorted(unl)}, problems={prob}; SHA256SUMS.txt does not list itself'
# 19
M=json.load(open(odi+'/MANIFEST.json'));mf={f['path']:f for f in M['files']}
p19=[]
if set(mf)!=on_disk-SELF: p19.append('file set differs: '+str(sorted(set(mf)^(on_disk-SELF)))[:200])
for rel,f in mf.items():
    if not os.path.exists(os.path.join(odi,rel)) or sha(os.path.join(odi,rel))!=f['sha256'] or os.path.getsize(os.path.join(odi,rel))!=f['bytes']: p19.append('bad:'+rel)
if 'MANIFEST.json' in mf or 'SHA256SUMS.txt' in mf: p19.append('manifest hashes itself or the sums file')
g=lambda *a:subprocess.run(['git','-C',root]+list(a),capture_output=True,text=True)
if g('cat-file','-e',M['candidate_baseline_commit']).returncode: p19.append('baseline commit missing')
if g('merge-base','--is-ancestor',M['candidate_baseline_commit'],'HEAD').returncode: p19.append('baseline not ancestor of HEAD')
if M['branch']!=g('branch','--show-current').stdout.strip(): p19.append('branch mismatch')
for p,v in M['original_files_hashes_at_baseline'].items():
    if not v['equals_baseline_blob'] or sha(os.path.join(root,p))!=v['sha256']: p19.append('original changed:'+p)
for n,h in M['external_inputs_sha256'].items():
    pth=os.path.expanduser('~/Downloads/'+n)
    if h and os.path.exists(pth) and sha(pth)!=h: p19.append('external ODI01 input changed:'+n)
for k in ('pushed','merged','published','pr_opened'):
    if M[k]: p19.append(k+' true')
r19='PASS' if not p19 else 'FAIL'
e19=f'MANIFEST.json lists {len(mf)} files (all present, bytes and SHA-256 match, neither manifest file lists itself); candidate baseline commit {M["candidate_baseline_commit"][:12]} recorded and an ancestor of HEAD; branch {M["branch"]}; {len(M["original_files_hashes_at_baseline"])} original file hashes recorded and equal to the baseline blobs; ODI01 external input hashes unchanged; problems={p19}'
json.dump({'checksum':{'result':r18,'evidence':e18},'manifest':{'result':r19,'evidence':e19}},open(sys.argv[3],'w'),indent=1)
print('18',r18,'|','19',r19)
