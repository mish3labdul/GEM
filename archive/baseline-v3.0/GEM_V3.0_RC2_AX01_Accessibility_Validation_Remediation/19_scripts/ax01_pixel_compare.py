"""AX01 task 16: compare native before/after captures (local-only PNGs). Usage: ax01_pixel_compare.py <package_dir> <out_json> <tag_pairs like A:A_before:A_after> ...
Classification: PIXEL-IDENTICAL (0 differing px outside the floating Copilot button), SUB-PIXEL NATIVE VARIANCE (edge-only, no centroid/area change), VISIBLE REGRESSION (otherwise)."""
import sys, os, re, json, glob, numpy as np
from PIL import Image, ImageChops
pkg, outp, *pairs = sys.argv[1:]; S = f"{pkg}/local_only/screenshots/"; res = []
for pr in pairs:
    doc, b, a = pr.split(':')
    for fb in sorted(glob.glob(S + f'{b}_slide*.png')):
        s = int(re.search(r'slide(\d+)', fb).group(1)); fa = S + f'{a}_slide{s:03d}.png'
        if not os.path.exists(fa): continue
        A = np.asarray(Image.open(fb).convert('L')).astype(int); B = np.asarray(Image.open(fa).convert('L')).astype(int)
        if A.shape != B.shape: res.append([doc, s, 'VISIBLE REGRESSION', 'size differs', 0, 0]); continue
        d = np.abs(A - B); d[1150:, 2050:] = 0; d[40:160, 2040:] = 0   # masks: floating Copilot button, PowerPoint transient toast (UI, not slide content)
        n = int((d > 0).sum()); big = int((d > 24).sum())
        if n == 0: cls = 'PIXEL-IDENTICAL'
        else:
            ys, xs = np.nonzero(d > 0); box = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1)); ink = lambda M: (M[box] < 128).sum(); ma = ink(A) - ink(B)
            cls = 'SUB-PIXEL NATIVE VARIANCE' if big < 25000 and abs(ma) <= max(40, 0.01 * ink(A)) and min(int(np.abs(A[box] - np.roll(B, dy, 0)[box]).sum()) for dy in (0,)) <= min(int(np.abs(A[box] - np.roll(B, dy, 0)[box]).sum()) for dy in (-1, 1)) else 'REVIEW: possible visible change'
        res.append([doc, s, cls, f'{n} differing px ({big} > 24)', n, big])
json.dump(res, open(outp, 'w'), indent=1)
import collections; print(collections.Counter((r[0], r[2]) for r in res)); [print(r) for r in res if r[2] != 'PIXEL-IDENTICAL']
