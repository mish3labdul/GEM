#!/usr/bin/env python3
"""Read-only verification of migration identity, paths, packaging and release preservation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse, csv, hashlib, json, re, stat, subprocess, unicodedata, zipfile
ROOT = Path(__file__).resolve().parents[1]
FROZEN_PREVIEW_PATH = 'website/previews/GEM_Website_Preview_v0.5.1_2026-10-11.zip'
FROZEN_PREVIEW_SHA256 = 'eb073e84933149128f66c34a3479b6a9ba7c91bbfc92e07934852a626cf95fcf'

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()


def validate_inventory_sources(root, inventory, check, hashed):
    permitted={'excluded-cache-original-retained','out-of-active-scope-original-retained'}
    for r in inventory:
        if not r['destination']:
            check(r['disposition'] in permitted,'Unexplained empty destination: '+r['source_path']);continue
        p=root/r['destination']
        check(p.is_file(),'Missing migration destination: '+r['destination'])
        if p.is_file():check(hashed(p)==r['sha256'],'Changed source bytes: '+r['destination'])

def validate_previews(root, public_files, original, check,
                      frozen_path=FROZEN_PREVIEW_PATH,
                      frozen_sha256=FROZEN_PREVIEW_SHA256):
    """Bind historical packages to their own immutable contents and current package to site."""
    def safe_path(name, prefix=None):
        if not isinstance(name, str) or not name or '\\' in name:
            return False
        path = Path(name)
        return (not path.is_absolute() and '..' not in path.parts and
                path.as_posix() == name and
                (prefix is None or name.startswith(prefix)))
    def members_valid(members):
        return (isinstance(members, dict) and bool(members) and
                all(safe_path(n) and isinstance(h, str) and
                    re.fullmatch(r'[0-9a-f]{64}', h) for n, h in members.items()))
    packages = {p.relative_to(root).as_posix(): p for p in (root/'website/previews').glob('*.zip')}
    check(bool(packages), 'Missing preview ZIP')
    frozen_package = packages.get(frozen_path)
    check(frozen_package is not None and digest(frozen_package) == frozen_sha256,
          'Frozen preview container identity mismatch: '+frozen_path)
    register_path = root/'website/previews/preview-register.json'
    if not register_path.exists():
        # Compatibility for the unchanged frozen import, never for a derivative.
        check(public_files == original, 'Website differs from frozen ZIP')
        entries = [{'path': n, 'role': 'historical-frozen-import', 'files': original,
                    'sha256': digest(p)} for n, p in packages.items()]
        current = None
    else:
        try:
            register = json.loads(register_path.read_text())
        except (json.JSONDecodeError, UnicodeError):
            check(False, 'Invalid preview register JSON')
            register = {}
        if not isinstance(register, dict):
            check(False, 'Invalid preview register')
            register = {}
        check(register.get('schema_version') == 1, 'Unsupported preview register schema')
        raw_entries = register.get('previews', [])
        if not isinstance(raw_entries, list):
            check(False, 'Invalid preview register previews')
            raw_entries = []
        entries = []
        for index, entry in enumerate(raw_entries):
            if isinstance(entry, dict):
                entries.append(entry)
            else:
                check(False, 'Invalid preview entry: '+str(index))
        names = [e.get('path') for e in entries]
        names_are_strings = all(isinstance(name, str) for name in names)
        check(names_are_strings and len(names) == len(set(names)), 'Duplicate registered preview paths')
        check(names_are_strings and set(names) == set(packages), 'Preview register membership mismatch')
        frozen_entries = [e for e in entries if e.get('role') == 'historical-frozen-import']
        check(bool(frozen_entries), 'Missing frozen-import preview')
        check(len(frozen_entries) == 1 and frozen_entries[0].get('path') == frozen_path,
              'Frozen preview path/role identity mismatch')
        record_name = register.get('active_site_record')
        record_path_valid = safe_path(record_name, 'website/records/')
        check(record_path_valid, 'Invalid active site record path')
        current = None
        if record_path_valid:
            current_path = root/record_name
            check(current_path.is_file(), 'Missing active site record')
            if current_path.is_file():
                try:
                    current = json.loads(current_path.read_text())
                except (json.JSONDecodeError, UnicodeError):
                    check(False, 'Invalid active site record JSON')
                    current = None
                else:
                    if not isinstance(current, dict):
                        check(False, 'Invalid active site record')
                        current = None
                if current is not None:
                    check(current.get('schema_version') == 1, 'Unsupported active site schema')
                    check(members_valid(current.get('files')), 'Invalid active site member paths/hashes')
                    check(current.get('files') == public_files, 'Active site record differs from public tree')
        current_entries = [e for e in entries if e.get('role') == 'current']
        check(len(current_entries) == 1, 'Expected exactly one current preview')
        if current is not None:
            check(len(current_entries) == 1 and current.get('current_preview') == current_entries[0].get('path'), 'Current preview pointer mismatch')
    if not register_path.exists():
        frozen_entries = [e for e in entries if e.get('role') == 'historical-frozen-import']
        check(len(frozen_entries) == 1 and frozen_entries[0].get('path') == frozen_path,
              'Frozen preview path/role identity mismatch')
    for entry in entries:
        name = entry.get('path')
        check(safe_path(name, 'website/previews/') and name in packages, 'Invalid registered preview path: '+str(name))
        if not safe_path(name, 'website/previews/') or name not in packages:
            continue
        p = packages[name]
        role = entry.get('role')
        check(isinstance(role, str) and role in {'current','historical-frozen-import','historical-candidate'}, 'Invalid preview role: '+name)
        check(entry.get('sha256') == digest(p), 'Preview digest mismatch: '+name)
        members = entry.get('files')
        check(members_valid(members), 'Invalid preview member paths/hashes: '+name)
        try:
            with zipfile.ZipFile(p) as z:
                infos = z.infolist()
                names = [info.filename for info in infos]
                check(len(names) == len(set(names)), 'Duplicate ZIP entries: '+name)
                check(all(safe_path(n) for n in names), 'Unsafe ZIP member: '+name)
                regular = all(not info.is_dir() and
                              not bool(info.external_attr & 0x10) and
                              stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG)
                              for info in infos)
                check(regular, 'Non-regular ZIP member: '+name)
                zipped = {n: hashlib.sha256(z.read(n)).hexdigest() for n in names}
                check(zipped == members, 'Preview registered contents mismatch: '+name)
                if role == 'current':
                    check(zipped == public_files, 'Current preview differs from public tree: '+name)
                elif role == 'historical-frozen-import':
                    check(zipped == original, 'Frozen preview differs from original ZIP inventory: '+name)
                check(z.testzip() is None, 'ZIP CRC failure: '+name)
        except (zipfile.BadZipFile, OSError):
            check(False, 'Invalid preview ZIP: '+name)

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
    validate_inventory_sources(ROOT, inventory, check, hashed)
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
    for p in site.rglob('*.html'):
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
    validate_previews(ROOT, public_files, original, check)
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
        for b in freeze['branches']:
            live=branches.get(b['name'])
            if b['name']=='main' and live and live!=b['sha']:
                # An authorized merge advances main; it must preserve the frozen
                # history and contain the checkout whose manifest was validated.
                head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD']).decode().strip()
                for ancestor in (b['sha'],head):
                    comparison=api(f'repos/mish3labdul/GEM/compare/{ancestor}...{live}')
                    check(comparison['merge_base_commit']['sha']==ancestor, 'Main does not preserve validated history: '+ancestor)
            else:
                check(live==b['sha'],'Existing source branch moved: '+b['name'])
    report={'status':'FAIL' if failures else 'PASS','counts':counts,'remote_checked':not args.skip_remote,'checksums_checked':not args.skip_checksums,'failures':failures,'scope':'Collection identity and migration; Chromium QA is reported separately. No new approval or deferred gate closure.'}
    print(json.dumps(report,indent=2))
    return bool(failures)

if __name__=='__main__':
    raise SystemExit(main())
