#!/usr/bin/env python3
"""AFC01 copy (duplicate-basename fix). Verify every SHA-256 list found in a repo checkout. Usage: verify_checksums.py <repo_root>
For each list, entries are resolved relative to the list's directory, then its parents (up to repo root).
Prints per-list: OK / MISMATCH / MISSING counts, and details for non-OK."""
import hashlib, os, re, sys
root = os.path.abspath(sys.argv[1])
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()
lists = []
for d, dn, fn in os.walk(root):
    dn[:] = [x for x in dn if x != '.git']
    for n in fn:
        if re.search(r'sha256', n, re.I):
            lists.append(os.path.join(d, n))
tot = {'OK': 0, 'MISMATCH': 0, 'MISSING': 0, 'UNPARSED': 0}
for L in sorted(lists):
    ok = mm = ms = up = 0; detail = []
    base = os.path.dirname(L)
    for line in open(L, encoding='utf8', errors='replace'):
        line = line.rstrip('\n')
        m = re.match(r'^([0-9a-fA-F]{64})\s+\*?(.+)$', line)
        if not m:
            if line.strip(): up += 1
            continue
        h, rel = m.group(1).lower(), m.group(2).strip()
        cand = None; b = base
        while True:
            p = os.path.normpath(os.path.join(b, rel))
            if os.path.isfile(p): cand = p; break
            if os.path.abspath(b) == root: break
            b = os.path.dirname(b)
            if not b.startswith(root): break
        if cand is None:
            # try basename search under root
            hits = [os.path.join(d, os.path.basename(rel)) for d, _, fs in os.walk(root) if '.git' not in d and os.path.basename(rel) in fs]
            if len(hits) == 1: cand = hits[0]
            elif len(hits) > 1:  # AFC01: ambiguous basename -> accept if any candidate matches
                m2 = [x for x in hits if sha(x) == h]
                if m2: cand = m2[0]
        if cand is None: ms += 1; detail.append(('MISSING', rel)); continue
        if sha(cand) == h: ok += 1
        else: mm += 1; detail.append(('MISMATCH', rel, os.path.relpath(cand, root)))
    print(f"{os.path.relpath(L, root)}: OK={ok} MISMATCH={mm} MISSING={ms} UNPARSED_LINES={up}")
    for x in detail[:12]: print('    ', *x)
    tot['OK'] += ok; tot['MISMATCH'] += mm; tot['MISSING'] += ms; tot['UNPARSED'] += up
print('TOTAL', tot)
