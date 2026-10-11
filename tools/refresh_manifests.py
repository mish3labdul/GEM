#!/usr/bin/env python3
"""Refresh intentionally generated manifests; self-exclude only the checksum file."""
from pathlib import Path
import csv, hashlib, collections
ROOT = Path(__file__).resolve().parents[1]

def files():
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if p.is_file() and '.git' not in rel.parts and p.name != '.DS_Store':
            if '__pycache__' in rel.parts and rel.parts[0] != 'archive':
                continue
            yield p

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    groups = collections.defaultdict(list)
    excluded = {'governance/SHA256SUMS.txt', 'governance/duplicate-report.csv'}
    for p in files():
        rel = p.relative_to(ROOT).as_posix()
        if rel not in excluded:
            groups[digest(p)].append(rel)
    with (ROOT/'governance/duplicate-report.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator="\n");w.writerow(['sha256','copies','path','disposition'])
        for h, paths in sorted(groups.items()):
            if len(paths)>1:
                for path in paths:w.writerow([h,len(paths),path,'RETAINED: provenance/history/current-use copy'])
    lines = [f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in files() if p.relative_to(ROOT).as_posix() != 'governance/SHA256SUMS.txt']
    (ROOT/'governance/SHA256SUMS.txt').write_text(''.join(lines))
    print(f'{len(lines)} files checksummed; {sum(len(v)>1 for v in groups.values())} duplicate groups retained')

if __name__ == '__main__':
    main()
