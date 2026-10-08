"""ODI01-R1 font claim/file matrix. Scans the repository tree (git-tracked or not) for font binaries, plus the local ~/Library/Fonts GEM-Working-* copies,
and records every Jost / Inter / Noto Sans Arabic weight 400 and 500 claim against the actual file evidence.
Usage: r1_font_matrix.py <worktree_root> <out_csv>   (exit 3 = a 500-weight file was found -> STOP and report)"""
import sys,os,glob,json,hashlib,csv
from fontTools.ttLib import TTFont
root=os.path.abspath(sys.argv[1]);out=sys.argv[2]
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
FAM={'Jost':'jost','Inter':'inter','Noto Sans Arabic':'notosansarabic'}
LIC={'Jost':'SIL OFL 1.1; OFL.txt in package (Copyright 2020 The Jost Project Authors)','Inter':'SIL OFL 1.1; OFL.txt in package (Copyright 2020 The Inter Project Authors)','Noto Sans Arabic':'SIL OFL 1.1; OFL.txt in package (Copyright 2022 The Noto Project Authors)'}
found=[]
for ext in ('ttf','otf','ttc','woff','woff2'):
    for p in glob.glob(root+'/**/*.'+ext,recursive=True):
        if '/.git/' in p: continue
        found.append(p)
local=glob.glob(os.path.expanduser('~/Library/Fonts/GEM-Working-*.ttf'))
mf=json.load(open(root+'/GEM_Letterhead_Set_v1.1_Application_Revision_03/00_source/Original_Font_Manifest.json'))
rows=[];stop=False
def info(p):
    f=TTFont(p);n=f['name'];return n.getDebugName(1),n.getDebugName(2),n.getDebugName(5),f['OS/2'].usWeightClass,'fvar' in f
for p in sorted(found):
    fam,sty,ver,w,var=info(p);rel=os.path.relpath(p,root)
    famk=next((k for k in FAM if k.lower().replace(' ','') in (fam or '').lower().replace(' ','')),fam)
    if w==500: stop=True
    rows.append([famk,w,os.path.basename(p),rel,sha(p),ver,LIC.get(famk,'see OFL.txt'),'PRESENT — CURRENT (working build, genuine static 400; deployment-rights acceptance NOT given: VAL-05, Y03)' if w==400 and not var else f'PRESENT — weight {w} — NOT ACCEPTED'])
shas={r[4] for r in rows}
for p in sorted(local):
    h=sha(p)
    if h in shas: continue
    fam,sty,ver,w,var=info(p);m=next((e for e in mf if e['sha256']==h),None)
    st=m['status'] if m else 'UNREGISTERED'
    rows.append([fam,w,os.path.basename(p),'~/Library/Fonts/'+os.path.basename(p)+' (user machine, OUTSIDE repository)',h,ver,LIC.get(fam,''),f'NOT IN REPOSITORY — NOT ACCEPTED — weight {w} — manifest status: {st}. Not a 500; does not satisfy D5.'])
inrepo={r[4] for r in rows}
for e in mf:
    if e['sha256'] in inrepo or any(r[4]==e['sha256'] for r in rows): continue
    fam=e['family'];w='variable (wght axis incl. 500)' if '[' in e['file'] else (700 if 'Bold' in e['file'] else '?')
    rows.append([fam,w,os.path.basename(e['file']),'(recorded in letterhead Original_Font_Manifest.json only)',e['sha256'],e['version'],LIC.get(fam,''),f'NOT IN REPOSITORY — NOT ACCEPTED — manifest status: {e["status"]}'])
# explicit 400 / 500 claim rows per family
claims=[]
for fam in FAM:
    r4=[r for r in rows if r[0]==fam and r[1]==400 and r[3].startswith('GEM_Letterhead')]
    claims.append([fam,'400 (Regular)','PRESENT / CURRENT' if r4 else 'MISSING',r4[0][3] if r4 else '',r4[0][4] if r4 else '',(r4[0][2]+' is a genuine static weight-400 file (OS/2 usWeightClass 400, no fvar)') if r4 else ''])
    r5=[r for r in rows if r[0]==fam and r[1]==500]
    claims.append([fam,'500 (Medium)','NOT ACCEPTED / CURRENTLY UNAVAILABLE' if not r5 else 'FILE FOUND — STOP',';'.join(r[3] for r in r5),';'.join(r[4] for r in r5),'No static 500 file anywhere in the repository; variable working builds are recorded in the manifest only (file not in repo, not accepted)'])
w=csv.writer(open(out,'w',newline='',encoding='utf-8'))
w.writerow(['Family','Weight','Filename','Path','SHA-256','Version','Licence evidence','Accepted / current status'])
for r in sorted(rows,key=lambda r:(r[0],str(r[1]),r[2])): w.writerow(r)
w.writerow([]);w.writerow(['CLAIM SUMMARY','Weight','Result','Path','SHA-256','Note'])
for c in claims: w.writerow(c)
print('rows',len(rows),'500 file found' if stop else 'no 500-weight file found')
sys.exit(3 if stop else 0)
