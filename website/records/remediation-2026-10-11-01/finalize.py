from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,difflib,re,shutil
A=Path(__file__).resolve().parent;R=A.parent
excluded={'.git','node_modules','__pycache__','.venv','transient-dependencies'}
files={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and A not in p.parents and not any(x in excluded for x in p.relative_to(R).parts)}
baseline=json.loads((A/'raw-results/baseline.json').read_text())['files']
changed=sorted(k for k,v in baseline.items() if k in files and files[k]!=v)
deleted=sorted(set(baseline)-set(files));added=sorted(set(files)-set(baseline))
expected_changed={'site/index.html','site/privacy.html','site/assets/css/site.css','site/assets/js/site.js','qa/run_qa.py'}
expected_deleted={'site/.DS_Store','site/assets/.DS_Store'}
expected_added={'qa/font_validation.py','qa/run_corrections_qa.py','qa/README.md'}
unexpected={'changed':sorted(set(changed)-expected_changed),'deleted':sorted(set(deleted)-expected_deleted),'added':sorted(set(added)-expected_added)}
site={k.removeprefix('site/'):v for k,v in files.items() if k.startswith('site/')}
tested={}
for label,path in [('regression','regression/20261011T170638Z'),('corrections','corrections/20261011T171103Z')]:
    tested[label]=json.loads((A/'raw-results'/path/'environment.json').read_text())['site_files']==site
result={'utc':datetime.now(timezone.utc).isoformat(),'baseline_files':len(baseline),'final_files_outside_evidence':len(files),'changed':changed,'deleted':deleted,'added':added,'unexpected_concurrent_changes':unexpected,'site_matches_successful_test_hashes':tested}
(A/'raw-results/final-comparison.json').write_text(json.dumps(result,indent=2))
(A/'FINAL_SHA256.txt').write_text(''.join(f'{v}  {k}\n' for k,v in sorted(files.items())))
(A/'SOURCE_QA_FINAL_SHA256.txt').write_text(''.join(f'{v}  {k}\n' for k,v in sorted(files.items()) if k.startswith(('site/','qa/'))))
diff=''
for name in changed:
    before=A/'before'/name
    if before.exists():diff+=''.join(difflib.unified_diff(before.read_text().splitlines(keepends=True),(R/name).read_text().splitlines(keepends=True),fromfile='before/'+name,tofile=name))
for name in added:diff+=''.join(difflib.unified_diff([], (R/name).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile=name))
diff+='\nRemoved public Finder metadata (exact bytes preserved in before/):\n'+'\n'.join(deleted)+'\n'
(A/'CHANGES.diff').write_text(diff)
clean=not any(unexpected.values()) and all(tested.values())
text=f'''# Final integrity and change attribution

Final comparison UTC: {result['utc']}.

Baseline: {len(baseline)} pre-existing files. Final outside this evidence directory: {len(files)}.

Attributed changes: {len(changed)} modified text files, {len(deleted)} removed Finder metadata files, {len(added)} new QA/documentation files. Exact lists and hashes are in raw-results/final-comparison.json and FINAL_SHA256.txt. Before copies of every modified/removed existing file are retained; CHANGES.diff includes new text files too.

No unexpected concurrent changes detected: {not any(unexpected.values())}.
Final site hashes match successful regression and correction run environments: {all(tested.values())}.

Previous audits, creative packages, records/owner decisions, original images, logo/font assets and source references remain unchanged. This session changed only the documented confirmed-correction scope. No deployment, form connection, email-app navigation or enquiry sending occurred.

Baseline/final hashing excludes this evidence directory and .git, node_modules, __pycache__, .venv, transient-dependencies trees. Python caches may be created by QA. This is a content hash comparison, not filesystem-metadata or excluded-cache equivalence.

Result: {'PASS — attributed changes only; tested site state retained.' if clean else 'ATTENTION — inspect raw comparison before accepting.'}
'''
(A/'INTEGRITY.md').write_text(text)
required=['START_HERE.md','CHANGELOG.md','PENDING_DECISIONS.md','VERIFICATION.md','CODE_REVIEW.md','INTEGRITY.md','BASELINE_SHA256.txt','FINAL_SHA256.txt','SOURCE_QA_FINAL_SHA256.txt','CHANGES.diff']
broken=[]
for p in A.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' not in link and not (p.parent/link.split('#')[0]).exists():broken.append({'file':p.name,'link':link})
validation={'required_reports_present':all((A/x).is_file() for x in required),'broken_local_links':broken,'integrity_clean':clean}
(A/'raw-results/package-validation.json').write_text(json.dumps(validation,indent=2))
# Copy a small, clearly selected screenshot set; full original runs remain in raw-results.
capture=A/'raw-results/corrections/20261011T171103Z/screenshots'
for name in ['privacy-1440-full.png','privacy-768-full.png','privacy-375-full.png','privacy-320-full.png','room-range-error.png','long-draft-copy.png','blocked-fonts-failed-brand-acceptance.png']:
    shutil.copy2(capture/name,A/'screenshots'/name)
print(json.dumps(result,indent=2));print(json.dumps(validation,indent=2))
