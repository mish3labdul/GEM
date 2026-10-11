"""AR01 final: native PowerPoint per-character probe + local-only screenshot of slide 39 for one or more deck copies (read-only; closes unsaved; verifies hash).
Output CSV (numbers only): tag, shape, index, class (A/L/D/S/P), left x pt, width pt.  Usage: ar01_native_slide39_probe.py <package_dir> <out_csv> <tag=pptx> [<tag=pptx> ...]   (docling venv python: Quartz)"""
import sys, os, re, csv, time, shutil, subprocess, hashlib, zipfile
import Quartz
sys.path.insert(0, os.path.dirname(__file__))
from ar01_common import *
pkg, outp, *jobs = sys.argv[1:]; here = os.path.dirname(os.path.abspath(__file__))
T = os.path.expanduser("~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_AR01_NATIVE_TEST"); os.makedirs(T, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def osa(script, *a, timeout=120): return subprocess.run(["osascript", "-e", script, *a], capture_output=True, text=True, timeout=timeout)
def wid(part):
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        if 'PowerPoint' in (w.get('kCGWindowOwnerName') or '') and part in (w.get('kCGWindowName') or '') and w['kCGWindowBounds']['Width'] > 1000: return str(w['kCGWindowNumber'])
cls = lambda c: 'A' if AR.search(c) else 'L' if LAT.search(c) else 'D' if c.isdigit() else 'S' if c == ' ' else 'P'
rows = []; log = []
for job in jobs:
    tag, deck = job.split('=', 1); dst = f"{T}/AR01_{tag}.pptx"; shutil.copyfile(deck, dst); h0 = sha(dst); name = f"AR01_{tag}.pptx"
    text = next(r['text'] for r in pptx_paragraphs(zipfile.ZipFile(deck)) if r['num'] == 39 and r['shape_name'] == 'Text 8')
    osa('on run argv\n with timeout of 90 seconds\n  tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))\n end timeout\nend run', dst, timeout=110); time.sleep(3)
    osa('tell application "Microsoft PowerPoint" to go to slide (view of active window) number 39'); time.sleep(2)
    w = wid(name[:-5]); shot = f"{pkg}/local_only/screenshots/{tag}_slide039.png"
    if w: subprocess.run(["python3", "-I", f"{here}/ar01_capture.py", w, shot, "560", "330", "2970", "1680"], capture_output=True)
    r = subprocess.run(["osascript", f"{here}/ar01_native_char_bounds.applescript", name, "39", "Text 8"], capture_output=True, text=True, timeout=200)
    H = next(l.split('\t') for l in r.stdout.split('\n') if l.startswith('H\t')); C = [l.split('\t') for l in r.stdout.split('\n') if l.startswith('C\t')]; assert len(C) == len(text)
    for i, (c, ch) in enumerate(zip(C, text), 1): rows.append([tag, 'Text 8', i, cls(ch), c[2], c[4]])
    log.append((tag, H[5], H[6], H[7], H[8], H[9], len(C)))
    osa(f'with timeout of 30 seconds\n tell application "Microsoft PowerPoint" to close presentation "{name}" saving no\nend timeout'); time.sleep(1)
    print(tag, 'hash unchanged:', sha(dst) == h0, 'shot:', bool(w)); os.remove(dst)
csv.writer(open(outp, 'w', newline='')).writerows([["Tag", "Shape", "Char index (logical)", "Class (A Arabic, L Latin, D digit, S space, P punct)", "Left x pt", "Width pt"]] + rows)
for l in log: print(l)
