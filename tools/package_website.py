#!/usr/bin/env python3
"""Package only the proposed static document root; never overwrite a deliverable."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import zipfile, hashlib, re
ROOT = Path(__file__).resolve().parents[1]

def main():
    readme = (ROOT / 'website/README.md').read_text()
    version = re.search(r'working preview v(\d+\.\d+\.\d+)', readme).group(1)
    date = datetime.now(ZoneInfo('Asia/Riyadh')).strftime('%Y-%m-%d')
    dest = ROOT / 'website/previews' / f'GEM_Website_Preview_v{version}_{date}.zip'
    site = ROOT / 'website/site'
    files = sorted(p for p in site.rglob('*') if p.is_file() and p.name != '.DS_Store' and '__pycache__' not in p.parts and '__MACOSX' not in p.parts and p.suffix != '.pyc')
    assert files and (site / 'index.html').is_file()
    assert not any(p.is_symlink() for p in site.rglob('*')), 'Symlink inside public root'
    assert all(p.stat().st_size < 100_000_000 for p in files)
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with dest.open('xb') as output:
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                for p in files:
                    info = zipfile.ZipInfo(p.relative_to(site).as_posix(), date_time=(2026, 10, 11, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    z.writestr(info, p.read_bytes(), compresslevel=9)
    except FileExistsError:
        raise SystemExit(f'Refusing to overwrite {dest}')
    with zipfile.ZipFile(dest) as z:
        assert z.namelist() == [p.relative_to(site).as_posix() for p in files]
        assert all(z.read(p.relative_to(site).as_posix()) == p.read_bytes() for p in files)
        assert z.testzip() is None
    print(f'{dest}\n{len(files)} files; SHA-256 {hashlib.sha256(dest.read_bytes()).hexdigest()}')

if __name__ == '__main__':
    main()
