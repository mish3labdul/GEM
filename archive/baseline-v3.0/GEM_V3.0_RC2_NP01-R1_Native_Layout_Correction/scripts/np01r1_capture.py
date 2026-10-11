"""NP01-R1 local-only capture: screencapture of a PowerPoint window (by CGWindowID), cropped to the slide canvas. View only. Usage: np01r1_capture.py <windowId> <out_png>"""
import sys, subprocess, os
from PIL import Image
wid, out = sys.argv[1:3]; tmp = out + ".full.png"
subprocess.run(["screencapture", "-x", "-o", "-l", wid, tmp], check=True, timeout=30)
Image.open(tmp).convert("RGB").crop((560, 330, 2970, 1680)).save(out); os.remove(tmp); print(out)
