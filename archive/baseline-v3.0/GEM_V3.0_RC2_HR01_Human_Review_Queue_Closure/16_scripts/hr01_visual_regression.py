#!/usr/bin/env python3
"""HR01 visual regression: page-by-page raster comparison of before (source candidate) and after (HR01 candidate) PDFs.

Run from the repository root:
  python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_visual_regression.py <before_dir> <after_dir> <work_dir> <out_csv>
Both dirs hold same-named PDFs (A,B,C,D = PowerPoint decks; W_<template> = Word templates), rendered with the same engine.
Classes: PIXEL IDENTICAL | SUB-PIXEL RENDER VARIANCE | EXPECTED CONTENT CHANGE ONLY (page is in the approved-change list) | VISIBLE REGRESSION.
Relative paths only; the rasters stay in <work_dir> (local-only).
"""
import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

before, after, work, outp = (Path(a) for a in sys.argv[1:5])
work.mkdir(parents=True, exist_ok=True)
# Pages whose visible content is expected to change (approved Arabic wording; Word letter text and footer label).
EXPECTED = {("A", 38), ("A", 65), ("A", 68)}
EXPECTED_WORD = {"W_Arabic_First_Page": {1}, "W_Arabic_Continuation": {1}, "W_Bilingual_First_Page": {1}, "W_Bilingual_Continuation": {1}}


def raster(pdf, tag):
    d = work / tag
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "60", "-gray", "-png", str(pdf), str(d / "p")], check=True)
    return sorted(d.glob("p-*.png"))


rows = []
for key in ["A", "B", "C", "D", "W_Arabic_First_Page", "W_Arabic_Continuation", "W_Bilingual_First_Page", "W_Bilingual_Continuation"]:
    b = raster(before / (key + ".pdf"), key + "_before")
    a = raster(after / (key + ".pdf"), key + "_after")
    assert len(a) == len(b), (key, len(a), len(b))
    for i, (pb, pa) in enumerate(zip(b, a), 1):
        A = np.asarray(Image.open(pb)).astype(int)
        B = np.asarray(Image.open(pa)).astype(int)
        if A.shape != B.shape:
            rows.append([key, i, "VISIBLE REGRESSION", "size differs", 0, 0])
            continue
        d = np.abs(A - B)
        n, big = int((d > 0).sum()), int((d > 24).sum())
        changed_ok = (key, i) in EXPECTED or i in EXPECTED_WORD.get(key, set())
        if n == 0:
            cls = "PIXEL IDENTICAL"
        elif changed_ok:
            cls = "EXPECTED CONTENT CHANGE ONLY"
        elif big <= 3:
            cls = "SUB-PIXEL RENDER VARIANCE"
        else:
            cls = "VISIBLE REGRESSION"
        rows.append([key, i, cls, "%d differing px (%d > 24)" % (n, big), n, big])
with open(outp, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["Document", "Page/slide", "Classification", "Detail", "Differing px", "Differing px > 24"])
    w.writerows(rows)
from collections import Counter
print(Counter((r[0], r[2]) for r in rows))
for r in rows:
    if r[2] not in ("PIXEL IDENTICAL",):
        print(r)
