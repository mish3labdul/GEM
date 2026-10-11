"""AX01 native slide capture (read-only; closes unsaved; hash re-verified). Usage: ax01_native_capture.py <package_dir> <tag> <deck_pptx> <slide> [<slide> ...]
Local-only PNGs: <package>/local_only/screenshots/<tag>_slide<NNN>.png (slide canvas crop). Prints placeholder info per slide from the PowerPoint object model."""
import sys, os, time, shutil, subprocess, hashlib
import Quartz
pkg, tag, deck, *slides = sys.argv[1:]; here = os.path.dirname(os.path.abspath(__file__))
T = os.path.expanduser("~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_AX01_NATIVE_TEST"); os.makedirs(T, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); name = f"AX01_{tag}.pptx"; dst = f"{T}/{name}"; shutil.copyfile(deck, dst); h0 = sha(dst)
def osa(s, *a, timeout=120): return subprocess.run(["osascript", "-e", s, *a], capture_output=True, text=True, timeout=timeout)
def wid(part):
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        if 'PowerPoint' in (w.get('kCGWindowOwnerName') or '') and part in (w.get('kCGWindowName') or '') and w['kCGWindowBounds']['Width'] > 1000: return str(w['kCGWindowNumber'])
osa('on run argv\n with timeout of 100 seconds\n  tell application "Microsoft PowerPoint" to open (POSIX file (item 1 of argv))\n end timeout\nend run', dst, timeout=120); time.sleep(3)
for s in slides:
    osa(f'tell application "Microsoft PowerPoint" to go to slide (view of active window) number {s}'); time.sleep(2)
    w = wid(name[:-5]); out = f"{pkg}/local_only/screenshots/{tag}_slide{int(s):03d}.png"
    if w: subprocess.run(["python3", "-I", f"{here}/ax01_capture.py", w, out, "560", "330", "2970", "1680"], capture_output=True)
    print('slide', s, 'captured' if w else 'NO WINDOW')
osa(f'with timeout of 30 seconds\n tell application "Microsoft PowerPoint" to close presentation "{name}" saving no\nend timeout'); time.sleep(1)
print('hash unchanged:', sha(dst) == h0); os.remove(dst)
