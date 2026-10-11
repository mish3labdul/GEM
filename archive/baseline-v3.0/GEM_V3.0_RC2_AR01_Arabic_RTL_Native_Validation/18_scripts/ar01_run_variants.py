"""AR01 native variant runner (scratch decks only; never touches candidates). For each variant: stage a hash-verified copy in PowerPoint's
sandbox container, open it, capture a LOCAL-ONLY window screenshot BEFORE any property read, probe per-character native positions (read-only),
close WITHOUT saving, verify the staged copy is unchanged. Needs the docling venv python (Quartz for window ids).
Usage: ar01_run_variants.py <package_dir> <variant_dir> <label>[,<label>...] <slide> <shape>[,<shape>...]"""
import sys, os, subprocess, time, shutil, hashlib, json
import Quartz
pkg, vdir, labels, slide, shapes = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4], sys.argv[5].split(',')
T = os.path.expanduser("~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_AR01_NATIVE_TEST")
os.makedirs(T, exist_ok=True); here = os.path.dirname(os.path.abspath(__file__))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def osa(script, *args, timeout=120):
    return subprocess.run(["osascript", "-e", script, *args], capture_output=True, text=True, timeout=timeout)
def window_id(title_part):
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        if 'PowerPoint' in (w.get('kCGWindowOwnerName') or '') and title_part in (w.get('kCGWindowName') or '') and w['kCGWindowBounds']['Width'] > 1000:
            return str(w['kCGWindowNumber'])
log = {}
for lab in labels:
    src = [f for f in os.listdir(vdir) if f.startswith(f"AR01_A39_{lab}") and f.endswith('.pptx')][0]; dst = f"{T}/{src}"
    shutil.copyfile(f"{vdir}/{src}", dst); h0 = sha(dst)
    osa('on run argv\n with timeout of 50 seconds\n  tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))\n end timeout\nend run', dst, timeout=70); time.sleep(3)
    osa(f'tell application "Microsoft PowerPoint" to go to slide (view of active window) number {slide}'); time.sleep(2)
    wid = window_id(src[:-5]); cap = None
    if wid:
        subprocess.run(["python3", "-I", f"{here}/ar01_capture.py", wid, f"{pkg}/local_only/screenshots/A39_{lab}_native.png", "560", "330", "2970", "1680"], capture_output=True)
        cap = f"A39_{lab}_native.png"
    for sh in shapes:
        r = subprocess.run(["osascript", f"{here}/ar01_native_char_bounds.applescript", src, slide, sh], capture_output=True, text=True, timeout=150)
        open(f"{pkg}/local_only/scratch/probes/probe_{src[:-5]}_{sh.replace(' ', '_')}.tsv", 'w').write(r.stdout + r.stderr)
    saved = osa(f'tell application "Microsoft PowerPoint" to return saved of presentation "{src}"').stdout.strip()
    osa(f'with timeout of 30 seconds\n tell application "Microsoft PowerPoint" to close presentation "{src}" saving no\nend timeout'); time.sleep(1)
    log[lab] = dict(file=src, staged_sha256=h0, unchanged_after=(sha(dst) == h0), window_found=bool(wid), screenshot=cap, saved_flag_after_probe=saved)
    os.remove(dst)
print(json.dumps(log, indent=1))
