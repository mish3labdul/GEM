"""AR01 local-only capture: screencapture of a PowerPoint/Word window by CGWindowID, optionally cropped. View only. Usage: ar01_capture.py <windowId> <out_png> [x0 y0 x1 y1]"""
import sys, subprocess, os
from PIL import Image
wid, out = sys.argv[1:3]; tmp = out + ".full.png"
subprocess.run(["screencapture", "-x", "-o", "-l", wid, tmp], check=True, timeout=30)
im = Image.open(tmp).convert("RGB")
if len(sys.argv) >= 7: im = im.crop(tuple(int(v) for v in sys.argv[3:7]))
im.save(out); os.remove(tmp); print(out, im.size)
