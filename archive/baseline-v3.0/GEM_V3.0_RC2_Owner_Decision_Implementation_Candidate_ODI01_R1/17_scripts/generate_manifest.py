"""ODI01-R1: write MANIFEST.json and SHA256SUMS.txt. Neither hashes itself. MANIFEST.json lists every package file except itself and SHA256SUMS.txt; SHA256SUMS.txt lists every file except itself (it includes MANIFEST.json).
Rebased for R1: baseline = HEAD 4ea0d11 (the repository's real lineage); AFC01/AFC02/ODI01 are external inputs recorded by hash, not repository history.
Usage: generate_manifest.py <repo_root> <pkg_dir>"""
import sys,os,json,hashlib,subprocess,glob
root=os.path.abspath(sys.argv[1]);pkg=os.path.abspath(sys.argv[2])
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
git=lambda *a:subprocess.run(['git','-C',root]+list(a),capture_output=True,text=True).stdout.strip()
SELF={'MANIFEST.json','SHA256SUMS.txt'}
files=sorted(os.path.relpath(os.path.join(d,n),pkg) for d,dn,fn in os.walk(pkg) for n in fn if os.path.relpath(os.path.join(d,n),pkg) not in SELF and n!='.DS_Store')
ORIG=['GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx']+[os.path.relpath(p,root) for p in sorted(glob.glob(root+'/GEM_V3_RC2/04_release/*.pptx')+glob.glob(root+'/GEM_V3_RC2/04_release/*.pdf')+glob.glob(root+'/PartB_RC2/05_release/*Part B*')+glob.glob(root+'/Amenities_Portfolio_PartD_RC2/04_release/*'))]+['PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.json','PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.css','README.md','GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md','qa/GEM_V3_RC2_Asset_Sync_Change_Log.md','qa/GEM_V3_RC2_Final_Release_Notes.md','qa/GEM_V3_RC2_Release_Notes.md','Amenities_Portfolio_PartD_RC2/README.md']
BASE=git('rev-parse','4ea0d11')
dl=os.path.expanduser('~/Downloads/')
EXT={n:(sha(dl+n) if os.path.exists(dl+n) else None) for n in ('ODI01_1_documents_evidence_scripts.zip','ODI01_2_candidate_decks_A_B_C.zip','ODI01_3_D3A_carried_forward_decks.zip')}
M={'package':os.path.basename(pkg),'pass':'ODI01-R1 — narrow technical reconciliation of ODI01 (validation-ID checker; D5 400-only / no faux bold)',
 'status':'GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE',
 'synchronized_means':'SYNCHRONIZED = governing-content, terminology, identifier and status alignment. It does NOT mean fully validated in every native application and production process.',
 'ac20':'OPEN','created':'2026-10-09','branch':git('branch','--show-current'),'candidate_baseline_commit':BASE,'origin_main':git('rev-parse','origin/main'),
 'pushed':False,'merged':False,'published':False,'pr_opened':False,
 'self_hash_policy':'MANIFEST.json and SHA256SUMS.txt do not hash themselves; SHA256SUMS.txt also covers MANIFEST.json.',
 'external_inputs_note':'AFC01 (5dbd017), AFC02 (f346133) and ODI01 (6fbd951) are not objects in this repository; ODI01 inputs are recorded here by SHA-256 of the delivered zips (Downloads). ODI01 was not overwritten.',
 'external_inputs_sha256':EXT,
 'original_files_hashes_at_baseline':{p:{'sha256':sha(os.path.join(root,p)),'equals_baseline_blob':hashlib.sha256(subprocess.run(['git','-C',root,'show',BASE+':'+p],capture_output=True).stdout).hexdigest()==sha(os.path.join(root,p))} for p in ORIG},
 'files':[{'path':f,'bytes':os.path.getsize(os.path.join(pkg,f)),'sha256':sha(os.path.join(pkg,f))} for f in files]}
json.dump(M,open(pkg+'/MANIFEST.json','w'),indent=1,ensure_ascii=False)
allf=sorted(files+['MANIFEST.json'])
open(pkg+'/SHA256SUMS.txt','w',encoding='utf-8').write(''.join(f"{sha(os.path.join(pkg,f))}  {f}\n" for f in allf))
print(len(files),'files in manifest;',len(allf),'in SHA256SUMS; originals recorded',len(ORIG),'all equal baseline',all(v['equals_baseline_blob'] for v in M['original_files_hashes_at_baseline'].values()))
