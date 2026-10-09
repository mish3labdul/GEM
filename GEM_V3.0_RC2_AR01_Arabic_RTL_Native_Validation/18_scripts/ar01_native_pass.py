"""AR01 task 8/9/16: native PowerPoint pass over every Arabic slide of a deck copy (read-only; closes without saving; never touches candidates).
For each Arabic paragraph shape: LOCAL-ONLY screenshot per slide (taken before any property read) + native probe of REQUESTED direction, alignment, font, size, bold,
and per-character horizontal positions. Output CSV contains numbers and generic labels only (no Arabic text).
Usage: ar01_native_pass.py <package_dir> <deck_pptx> <tag> <deck_label_in_inventory>   (docling venv python: Quartz)"""
import sys, os, re, csv, json, time, shutil, subprocess, hashlib
import Quartz
pkg, deck, tag, label = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
T = os.path.expanduser("~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_AR01_NATIVE_TEST"); os.makedirs(T, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
inv = [r for r in csv.reader(open(f"{pkg}/03_AR01_Arabic_Content_Inventory.csv", encoding='utf8'))][1:]
targets = sorted({(int(r[2]), r[4]) for r in inv if r[0] == label and r[2]})        # (slide, shape label)
dst = f"{T}/AR01_{tag}.pptx"; shutil.copyfile(deck, dst); h0 = sha(dst)
def osa(script, *a, timeout=120): return subprocess.run(["osascript", "-e", script, *a], capture_output=True, text=True, timeout=timeout)
def wid(part):
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        if 'PowerPoint' in (w.get('kCGWindowOwnerName') or '') and part in (w.get('kCGWindowName') or '') and w['kCGWindowBounds']['Width'] > 1000: return str(w['kCGWindowNumber'])
osa('on run argv\n with timeout of 90 seconds\n  tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))\n end timeout\nend run', dst, timeout=110); time.sleep(3)
name = f"AR01_{tag}.pptx"; rows = []; shots = []
for slide in sorted({s for s, _ in targets}):
    osa(f'tell application "Microsoft PowerPoint" to go to slide (view of active window) number {slide}'); time.sleep(2)
    w = wid(f"AR01_{tag}")
    if w:
        out = f"{pkg}/local_only/screenshots/{tag}_slide{slide:03d}.png"
        subprocess.run(["python3", "-I", f"{here}/ar01_capture.py", w, out, "560", "330", "2970", "1680"], capture_output=True); shots.append(os.path.basename(out))
for slide, shape in targets:
    r = subprocess.run(["osascript", f"{here}/ar01_native_char_bounds.applescript", name, str(slide), shape], capture_output=True, text=True, timeout=200)
    L = r.stdout.split('\n'); H = next((l.split('\t') for l in L if l.startswith('H\t')), None); C = [l.split('\t') for l in L if l.startswith('C\t')]
    if not H: rows.append([tag, slide, shape, 'PROBE FAILED', r.stderr[:80]]); continue
    xs = [(float(c[2]), float(c[4])) for c in C]; left = min(x for x, _ in xs); right = max(x + w_ for x, w_ in xs); bl, bw = float(H[1]), float(H[3])
    # progression: consecutive characters should step leftwards inside an RTL word (count steps that go rightwards among adjacent chars whose gap is small)
    ups = sum(1 for a, b in zip(xs, xs[1:]) if b[0] > a[0] and (b[0] - a[0]) < 40)
    rows.append([tag, slide, shape, H[5], H[6], H[7], H[8], H[9], len(C), f"{left:.1f}", f"{right:.1f}", f"{bl:.1f}", f"{bl + bw:.1f}", 'inside' if left >= bl - 0.5 and right <= bl + bw + 0.5 else 'OUTSIDE BOX', ups])
saved = osa(f'tell application "Microsoft PowerPoint" to return saved of presentation "{name}"').stdout.strip()
osa(f'with timeout of 30 seconds\n tell application "Microsoft PowerPoint" to close presentation "{name}" saving no\nend timeout'); time.sleep(1)
unchanged = sha(dst) == h0; os.remove(dst)
w = csv.writer(open(f"{pkg}/17_qa/native_pass_{tag}.csv", 'w', newline='', encoding='utf8'))
w.writerow(["Deck copy", "Slide", "Shape label", "Requested alignment", "Requested text direction", "Requested font", "Requested size pt", "Requested bold", "Characters", "Text left x pt", "Text right x pt", "Box left x pt", "Box right x pt", "Inside box?", "Rightward steps between adjacent chars (RTL progression check)"]); w.writerows(rows)
print(json.dumps(dict(tag=tag, staged_sha256=h0, unchanged_after=unchanged, saved_flag_after_probe=saved, screenshots=shots, shapes_probed=len(rows)), indent=1))
