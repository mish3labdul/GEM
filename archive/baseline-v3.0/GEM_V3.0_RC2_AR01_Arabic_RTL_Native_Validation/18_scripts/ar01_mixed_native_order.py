"""AR01 task 5: native per-character positions for the mixed / numeral / bracketed paragraphs of the FINAL Part A candidate. Output: classes + direction counts only (no text).
Usage: ar01_mixed_native_order.py <package_dir> <partA_pptx> <out_csv>   (docling venv python)"""
import sys, os, re, csv, time, shutil, subprocess, hashlib, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from ar01_common import *
pkg, deck, outp = sys.argv[1:4]; here = os.path.dirname(os.path.abspath(__file__))
T = os.path.expanduser("~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_AR01_NATIVE_TEST"); os.makedirs(T, exist_ok=True)
dst = f"{T}/AR01_MIXED.pptx"; shutil.copyfile(deck, dst); h0 = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
subprocess.run(["osascript", "-e", 'on run argv\n with timeout of 90 seconds\n tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))\n end timeout\nend run', dst], capture_output=True, timeout=110); time.sleep(3)
z = zipfile.ZipFile(deck); paras = {(r['num'], r['shape_name']): r['text'] for r in pptx_paragraphs(z) if not r.get('is_picture') and r['kind'] == 'slides' and AR.search(r['text'])}
def cls(c): return 'A' if AR.search(c) else 'L' if LAT.search(c) else 'D' if c.isdigit() else 'S' if c == ' ' else 'P'
rows = []
for (slide, shape) in [(39, 'Text 8'), (39, 'Text 4'), (65, 'Text 9'), (68, 'Text 10')]:
    r = subprocess.run(["osascript", f"{here}/ar01_native_char_bounds.applescript", "AR01_MIXED.pptx", str(slide), shape], capture_output=True, text=True, timeout=200)
    C = [l.split('\t') for l in r.stdout.split('\n') if l.startswith('C\t')]; xs = [float(c[2]) for c in C]; t = paras[(slide, shape)]
    assert len(xs) == len(t), (slide, shape, len(xs), len(t))
    seq = ''.join(cls(c) for c in t)
    def run_dir(k):
        idx = [i for i, c in enumerate(seq) if c in k]
        if len(idx) < 2: return 'n/a'
        # walk contiguous index runs of class k
        dirs = []
        run = [idx[0]]
        for i in idx[1:]:
            if i == run[-1] + 1: run.append(i)
            else: dirs.append(run); run = [i]
        dirs.append(run); res = []
        for rr in dirs:
            if len(rr) < 2: continue
            d = [xs[b] - xs[a] for a, b in zip(rr, rr[1:])]; res.append('LTR' if sum(v > 0 for v in d) > sum(v < 0 for v in d) else 'RTL')
        return '/'.join(res) or 'n/a'
    lat_first = seq.find('L'); lat_x = [xs[i] for i, c in enumerate(seq) if c in 'LD' ]; ar_x = [xs[i] for i, c in enumerate(seq) if c == 'A']
    rows.append([slide, shape, re.sub(r'(.)\1+', lambda m: m.group(1) + str(len(m.group(0))), seq), 'Arabic runs: ' + run_dir('A'), 'Latin letter runs: ' + run_dir('L'), 'digit runs: ' + run_dir('D'),
                 ('Latin/digit block lies left of the Arabic block' if lat_x and ar_x and max(lat_x) < min(ar_x) else 'n/a (no Latin/digits)' if not lat_x else 'Latin/digit block NOT left of Arabic block'), len(xs)])
subprocess.run(["osascript", "-e", 'with timeout of 30 seconds\n tell application "Microsoft PowerPoint" to close presentation "AR01_MIXED.pptx" saving no\nend timeout']); time.sleep(1)
same = hashlib.sha256(open(dst, 'rb').read()).hexdigest() == h0; os.remove(dst)
csv.writer(open(outp, 'w', newline='')).writerows([["Slide", "Shape", "Logical class sequence (A=Arabic L=Latin D=digit S=space P=punct)", "Arabic", "Latin", "Digits", "Block arrangement", "Characters measured"]] + rows)
print(same, rows)
