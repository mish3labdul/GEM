#!/usr/bin/env python3
"""Read-only verification of migration identity, paths, packaging and release preservation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse, csv, hashlib, json, re, subprocess, unicodedata, zipfile
ROOT = Path(__file__).resolve().parents[1]

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()

class HTML(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ('href','src','poster'):
            if a.get(key):self.refs.append(a[key])
        if a.get('srcset'):
            self.refs.extend(part.strip().split()[0] for part in a['srcset'].split(','))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-remote',action='store_true');ap.add_argument('--skip-checksums',action='store_true');ap.add_argument('--check-index',action='store_true');args=ap.parse_args()
    failures=[];counts={};cache={}
    def check(ok,message):
        if not ok:failures.append(message)
    def hashed(p):
        if p not in cache:cache[p]=digest(p)
        return cache[p]
    inventory=list(csv.DictReader((ROOT/'governance/file-inventory.csv').open()))
    counts['source_records']=len(inventory)
    permitted={'excluded-cache-original-retained','out-of-active-scope-original-retained'}
    for r in inventory:
        if not r['destination']:
            check(r['disposition'] in permitted,'Unexplained empty destination: '+r['source_path']);continue
        p=ROOT/r['destination']
        check(p.is_file(),'Missing migration destination: '+r['destination'])
        if p.is_file():check(hashed(p)==r['sha256'],'Changed source bytes: '+r['destination'])
    migrated=list(csv.DictReader((ROOT/'governance/path-migration.csv').open()))
    check(migrated==[{k:r[k] for k in migrated[0]} for r in inventory],'Migration register differs from inventory')
    freeze=json.loads((ROOT/'governance/source-freeze.json').read_text())
    for b in freeze['branches']:
        expected=subprocess.check_output(['git','-C',str(ROOT),'ls-tree','-rz',b['sha']]).split(b'\0')
        paths={x.split(b'\t',1)[1].decode() for x in expected if x}
        found={r['source_path'] for r in inventory if r['source_scope']=='git' and r['source_ref']==b['sha']}
        check(paths==found,'Incomplete frozen branch inventory: '+b['name'])
    files=[];seen={}
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if '.git' in rel.parts or p.name=='.DS_Store':continue
        if '__pycache__' in rel.parts and rel.parts[0]!='archive':continue
        if p.is_file():files.append(p)
        key=unicodedata.normalize('NFC',rel.as_posix()).casefold()
        check(key not in seen or seen[key]==rel.as_posix(),'Case/Unicode collision: '+rel.as_posix())
        seen[key]=rel.as_posix()
        check(not p.is_symlink(),'Unexpected symlink: '+rel.as_posix())
    counts['deliverable_files']=len(files)
    check(all(p.stat().st_size<100_000_000 for p in files),'File exceeds GitHub 100 MB limit')
    # Current brand catalogue is complete and all entries are source exact.
    catalogue=list(csv.DictReader((ROOT/'brand/asset-catalogue.csv').open()))
    check(len({r['path'] for r in catalogue})==len(catalogue),'Duplicate catalogue paths')
    actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'brand').rglob('*') if p.is_file() and p.name != '.DS_Store' and p.relative_to(ROOT/'brand').as_posix() not in ('README.md','asset-catalogue.csv')}
    check(actual=={r['path'] for r in catalogue},'Incomplete brand catalogue')
    for r in catalogue:
        check(r['stream']=='BRAND' and r['artwork_version']=='PENDING' and r['artwork_issue_date']=='PENDING','Invented brand metadata: '+r['path'])
        check(hashed(ROOT/r['path'])==r['sha256'],'Brand catalogue hash: '+r['path'])
    counts['catalogued_assets']=len(catalogue)
    # Every release attachment has an unchanged current copy matching its published digest.
    promoted=list((ROOT/'documents/released/v3.0').rglob('*'))
    for a in freeze['release']['assets']:
        matches=[p for p in promoted if p.is_file() and p.name==a['name']]
        check(len(matches)==1,'Missing/ambiguous released copy: '+a['name'])
        if len(matches)==1:check('sha256:'+hashed(matches[0])==a['digest'] and matches[0].stat().st_size==a['size'],'Release digest mismatch: '+a['name'])
    counts['release_attachments']=len(freeze['release']['assets'])
    site=ROOT/'website/site';html={}
    for p in site.glob('*.html'):
        h=HTML();h.feed(p.read_text());html[p]=h
    def resolve(p,url,anchor=True):
        u=urlsplit(url)
        if u.scheme or u.netloc:return
        if not u.path:q=p
        elif u.path.startswith('/'):q=site/unquote(u.path.lstrip('/'))
        else:q=p.parent/unquote(u.path)
        q=q.resolve()
        if q.is_dir():q=q/'index.html'
        check(q.is_relative_to(site),'Reference escapes site: '+url)
        check(q.is_file(),'Broken active reference: '+p.name+' -> '+url)
        if anchor and u.fragment and q in html:check(unquote(u.fragment) in html[q].ids,'Broken anchor: '+p.name+' -> '+url)
    for p,h in html.items():
        for url in h.refs:resolve(p,url)
    for p in site.rglob('*.css'):
        for url in re.findall(r'url\(\s*[\'\"]?([^\)\'\"]+)',p.read_text()):resolve(p,url.strip(),False)
    counts['public_pages']=len(html)
    active_docs=[ROOT/'README.md',*(ROOT/x/'README.md' for x in ['brand','documents','website','governance','archive','tools']),ROOT/'website/qa/README.md']
    for p in active_docs:
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
            u=urlsplit(target)
            if not u.scheme and not u.netloc:check((p.parent/unquote(u.path)).exists(),'Broken navigation link: '+str(p.relative_to(ROOT))+' -> '+target)
    public_files={p.relative_to(site).as_posix():hashed(p) for p in site.rglob('*') if p.is_file()}
    original={r['source_path']:r['sha256'] for r in inventory if r['source_scope']=='zip'}
    check(public_files==original,'Website differs from frozen ZIP')
    packages=list((ROOT/'website/previews').glob('*.zip'))
    check(bool(packages),'Missing preview ZIP')
    for p in packages:
        with zipfile.ZipFile(p) as z:
            check(len(z.namelist())==len(set(z.namelist())),'Duplicate ZIP entries')
            zipped={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
            check(zipped==public_files,'Preview contains missing/extra/changed files: '+p.name)
            check(z.testzip() is None,'ZIP CRC failure: '+p.name)
    if not args.skip_checksums:
        sums={}
        for line in (ROOT/'governance/SHA256SUMS.txt').read_text().splitlines():
            h,name=line.split('  ',1);sums[name]=h
            p=ROOT/name;check(p.is_file(),'Checksum missing file: '+name)
            if p.is_file():check(hashed(p)==h,'Collection checksum mismatch: '+name)
        expected={p.relative_to(ROOT).as_posix() for p in files if p.relative_to(ROOT).as_posix()!='governance/SHA256SUMS.txt'}
        check(expected==set(sums),'Collection checksum membership mismatch')
        counts['checksummed_files']=len(sums)
        if args.check_index:
            indexed=set(subprocess.check_output(['git','-C',str(ROOT),'ls-files','-z']).decode().split('\0'))-{''}
            check(indexed == set(sums)|{'governance/SHA256SUMS.txt'}, 'Git index differs from final checksum membership')
            check(subprocess.run(['git','-C',str(ROOT),'diff','--quiet']).returncode == 0, 'Unstaged tracked changes remain')
    if not args.skip_remote:
        def api(p):return json.loads(subprocess.check_output(['gh','api',p]))
        check(api('repos/mish3labdul/GEM/git/ref/tags/v3.0')==freeze['v3_ref'],'Published V3.0 tag changed')
        current=api('repos/mish3labdul/GEM/releases/tags/v3.0')
        check(current['body']==freeze['release']['body'],'Published release notes changed')
        fields=('id','name','size','digest','browser_download_url')
        stable=lambda assets:sorted([tuple(a[k] for k in fields) for a in assets])
        check(stable(current['assets'])==stable(freeze['release']['assets']),'Published release attachments changed')
        branches={b['name']:b['commit']['sha'] for b in api('repos/mish3labdul/GEM/branches?per_page=100')}
        for b in freeze['branches']:check(branches.get(b['name'])==b['sha'],'Existing source branch moved: '+b['name'])
    report={'status':'FAIL' if failures else 'PASS','counts':counts,'remote_checked':not args.skip_remote,'checksums_checked':not args.skip_checksums,'failures':failures,'scope':'Collection identity and migration; Chromium QA is reported separately. No new approval or deferred gate closure.'}
    print(json.dumps(report,indent=2))
    return bool(failures)

if __name__=='__main__':
    raise SystemExit(main())
