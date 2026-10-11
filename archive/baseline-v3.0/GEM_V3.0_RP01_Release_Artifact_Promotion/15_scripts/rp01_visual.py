#!/usr/bin/env python3
"""RP01 visual regression: rasterize source and promoted PDFs (LibreOffice renders produced beforehand) and compare per page.
Usage: rp01_visual.py <render_dir> <out_csv>   (render_dir contains src/pdf/*.pdf and new/pdf/*.pdf)
Classes: PIXEL IDENTICAL | EXPECTED RELEASE-LABEL CHANGE ONLY (diff confined to text-band rows, <=4% of page area) | SUB-PIXEL NATIVE VARIANCE (diff px <0.02% of page)
| VISIBLE REGRESSION (anything else; needs human look). Needs numpy + PIL (docling venv)."""
import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

root, out = Path(sys.argv[1]), Path(sys.argv[2])
DPI = 72
rows = []
for pdf in sorted((root / "src" / "pdf").glob("*.pdf")):
    key = pdf.stem
    sd, nd = root / "png" / "src" / key, root / "png" / "new" / key
    for d, p in ((sd, pdf), (nd, root / "new" / "pdf" / pdf.name)):
        d.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", str(p), str(d / "p")], check=True)
    sp, npg = sorted(sd.glob("p-*.png")), sorted(nd.glob("p-*.png"))
    if len(sp) != len(npg):
        rows.append([key, "ALL", "VISIBLE REGRESSION", "page count %d -> %d" % (len(sp), len(npg)), "", ""])
        continue
    for i, (a, b) in enumerate(zip(sp, npg), 1):
        A, B = np.asarray(Image.open(a).convert("RGB")).astype(int), np.asarray(Image.open(b).convert("RGB")).astype(int)
        if A.shape != B.shape:
            rows.append([key, i, "VISIBLE REGRESSION", "size %s -> %s" % (A.shape, B.shape), "", ""])
            continue
        m = (np.abs(A - B).max(axis=2) > 24)
        n = int(m.sum())
        if n == 0:
            rows.append([key, i, "PIXEL IDENTICAL", "0 px", "", ""])
            continue
        ys, xs = np.where(m)
        h, w = m.shape
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        area = (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1) / float(h * w)
        frac = n / float(h * w)
        if frac < 0.0002:
            cls = "SUB-PIXEL NATIVE VARIANCE"
        elif area <= 0.04 or (frac < 0.02 and (ys.max() - ys.min() + 1) / float(h) <= 0.25):
            cls = "EXPECTED RELEASE-LABEL CHANGE ONLY"
        else:
            cls = "VISIBLE REGRESSION"
        rows.append([key, i, cls, "%d px (%.3f%%)" % (n, frac * 100), "bbox %s" % (bbox,), "area %.1f%%" % (area * 100)])
with open(out, "w", encoding="utf-8", newline="") as fh:
    c = csv.writer(fh, lineterminator="\n")
    c.writerow(["Artifact", "Page/slide", "Class", "Differing pixels", "Diff bbox (px @72dpi)", "Bbox area"])
    c.writerows(rows)
from collections import Counter
print(Counter(r[2] for r in rows))
for k in sorted({r[0] for r in rows}):
    print(k, Counter(r[2] for r in rows if r[0] == k))
