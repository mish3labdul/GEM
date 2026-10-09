"""NP01 coverage pass: step a fresh, unmodified PowerPoint window through listed slides, capture the window with screencapture, crop to the slide canvas and tile 2x2 contact sheets. View-only (no property reads, no saves). Usage: np01_coverage_sheets.py <windowId> <label> <outdir> <slide>..."""
import sys, subprocess, time, os
from PIL import Image, ImageDraw
wid, label, out, slides = sys.argv[1], sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4:]]
os.makedirs(out, exist_ok=True)
CROP = (560, 330, 2970, 1680)   # slide canvas inside the 3024x1794 window capture (thumbnail pane, no notes pane)
tiles = []
for s in slides:
    subprocess.run(["osascript", "-e", f'tell application "Microsoft PowerPoint" to go to slide (view of active window) number {s}'], check=True, capture_output=True, timeout=60)
    time.sleep(1.6)
    p = f"{out}/{label}_s{s:03d}.png"
    subprocess.run(["screencapture", "-x", "-o", "-l", wid, p], check=True, timeout=30)
    im = Image.open(p).convert("RGB").crop(CROP).resize((780, 437))
    ImageDraw.Draw(im).rectangle((0, 0, 120, 22), fill=(255, 215, 0)); ImageDraw.Draw(im).text((4, 4), f"{label} slide {s}", fill=(0, 0, 0))
    tiles.append(im); os.remove(p)
for i in range(0, len(tiles), 4):
    grp = tiles[i:i + 4]; sheet = Image.new("RGB", (780 * 2 + 6, 437 * 2 + 6), (60, 60, 60))
    for j, t in enumerate(grp): sheet.paste(t, ((j % 2) * 786, (j // 2) * 443))
    sheet.save(f"{out}/{label}_sheet{i // 4 + 1:02d}.png")
print("sheets:", (len(tiles) + 3) // 4)
