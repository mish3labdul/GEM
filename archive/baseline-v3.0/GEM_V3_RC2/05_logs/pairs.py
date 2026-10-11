import sys, os
from PIL import Image, ImageDraw
before, after, out, tag = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
pairs = [tuple(x.split(':')) for x in sys.argv[5].split(',')]   # before_no:after_no
os.makedirs(out, exist_ok=True)
def img(d, n):
    for f in os.listdir(d):
        if f.endswith(f"-{int(n):02d}.png") or f.endswith(f"-{int(n):03d}.png"): return Image.open(os.path.join(d, f)).convert("RGB")
    return None
per = 4; W = 600
for i in range(0, len(pairs), per):
    chunk = pairs[i:i+per]
    rows = len(chunk)
    sheet = Image.new("RGB", (2*W + 24, rows*(int(W*0.5625)+30)+8), "#888"); d = ImageDraw.Draw(sheet)
    for r, (b, a) in enumerate(chunk):
        y = 8 + r*(int(W*0.5625)+30)
        for c, (dirn, n, lab) in enumerate([(before, b, "BEFORE"), (after, a, "AFTER")]):
            im = img(dirn, n)
            x = 8 + c*(W+8)
            d.text((x, y), f"{tag} {lab} slide {n}", fill="white")
            if im: sheet.paste(im.resize((W, int(W*0.5625))), (x, y+14))
    sheet.save(os.path.join(out, f"pairs_{i//per+1:02d}.png"))
print("sheets:", (len(pairs)+per-1)//per)
