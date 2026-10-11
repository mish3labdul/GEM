"""Builds the GEM brand assets that are fully specified by the guidelines: palette sheet, tagline and
descriptive line set in type (outlined), status labels. No logo, symbol, ring/arc/quarter/spark geometry
is drawn (proportions are PENDING PRODUCTION MASTER)."""
import glob, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = pathlib.Path(__file__).resolve().parents[1]; OUT = ROOT / "01_svg"
FD = glob.glob("/tmp/claude-0/*/*/scratchpad/fonts")[0]
INK, BEIGE, BLACK, WHITE = "#12171D", "#BCACA7", "#020202", "#FFFFFF"
DATE = "20261006"; VER = "v0.1"
_cache = {}
def font(name, wght, extra=None):
    k = (name, wght)
    if k not in _cache:
        f = TTFont(f"{FD}/{name}")
        axes = {"wght": wght}
        if "opsz" in [a.axisTag for a in f["fvar"].axes]: axes["opsz"] = 14
        _cache[k] = instancer.instantiateVariableFont(f, axes)
    return _cache[k]

def text_path(txt, name, wght, size, tracking_em=0.0):
    """Return (svg path d, advance width) for txt, outlined, baseline y=0, left x=0. Latin only, no kerning."""
    f = font(name, wght); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm; s = size / upm
    x = 0; ds = []
    for ch in txt:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs)
        tp = TransformPen(pen, (s, 0, 0, -s, x, 0)); gs[g].draw(tp)
        if pen.getCommands(): ds.append(pen.getCommands())
        x += gs[g].width * s + tracking_em * size
    return " ".join(ds), x - tracking_em * size

def svg(w, h, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">\n'
            f'<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n{body}\n</svg>\n')

def name(asset, variant): return f"GEM_BRAND_{asset}_{variant}_{VER}_{DATE}.svg"

# 1. tagline, outlined, in Jost 400, tracking 0.18em, capitals (type token: tagline)
TAG = "HOSPITALITY, IN PERFECT PROPORTION"
for variant, fg, bg in (("BEIGE-ON-INK", BEIGE, INK), ("INK-ON-WHITE", INK, WHITE), ("WHITE-ON-INK", WHITE, INK), ("BLACK-ON-WHITE", BLACK, WHITE)):
    d, w = text_path(TAG, "Jost[wght].ttf", 400, 28, 0.18); pad = 32
    W, H = round(w + pad * 2), 28 + pad * 2
    body = f'<rect width="{W}" height="{H}" fill="{bg}"/>\n<path transform="translate({pad} {pad + 22})" d="{d}" fill="{fg}"/>'
    (OUT / name("TAGLINE", variant)).write_text(svg(W, H, body, "GEM tagline", "HOSPITALITY, IN PERFECT PROPORTION, set in Jost with 0.18em tracking, outlined. Fixed text; not to be reworded or translated without brand approval."))

# 2. descriptive line: GEM(TM) - Amenities & Packaging, set in type (Part A / DS: no stream logo exists)
LINE = "AMENITIES & PACKAGING"
for variant, fg, bg in (("BEIGE-ON-INK", BEIGE, INK), ("INK-ON-WHITE", INK, WHITE)):
    d, w = text_path(LINE, "Jost[wght].ttf", 500, 24, 0.16); pad = 32
    W, H = round(w + pad * 2), 24 + pad * 2
    body = f'<rect width="{W}" height="{H}" fill="{bg}"/>\n<path transform="translate({pad} {pad + 19})" d="{d}" fill="{fg}"/>'
    (OUT / name("STREAM-LINE", variant)).write_text(svg(W, H, body, "Amenities and Packaging descriptive line", "Descriptive line set in type. Not a stream logo or sub-brand. Always used beside the unchanged GEM lockup."))

# 3. palette sheet
SW = [("INK", INK, "Principal dark field, default text", WHITE), ("BEIGE", BEIGE, "Signature soft-luxury tone", INK), ("BLACK", BLACK, "Monochrome, hover and pressed", WHITE), ("WHITE", WHITE, "Canvas", INK)]
body = [f'<rect width="1280" height="520" fill="{WHITE}"/>']
for i, (n, hx, role, tx) in enumerate(SW):
    x = 64 + i * 296
    stroke = f' stroke="{INK}" stroke-width="1"' if hx == WHITE else ""
    body.append(f'<rect x="{x}" y="64" width="272" height="260" fill="{hx}"{stroke}/>')
    for j, (t, wg, sz, tr, yy, col) in enumerate([(n, 500, 22, 0.08, 104, tx), (hx, 400, 16, 0.04, 132, tx)]):
        d, _ = text_path(t, "Jost[wght].ttf" if j == 0 else "Inter[opsz,wght].ttf", wg, sz, tr)
        body.append(f'<path transform="translate({x + 20} {yy})" d="{d}" fill="{col}"/>')
    d, _ = text_path(role, "Inter[opsz,wght].ttf", 400, 14, 0)
    body.append(f'<path transform="translate({x} 352)" d="{d}" fill="{INK}"/>')
pairs = [("Beige on Ink 8.2:1", INK, BEIGE), ("Ink on White 18.0:1", WHITE, INK), ("White on Ink 18.0:1", INK, WHITE), ("Ink on Beige 8.2:1", BEIGE, INK)]
for i, (t, bg, fg) in enumerate(pairs):
    x = 64 + i * 296; stroke = f' stroke="{INK}" stroke-width="1"' if bg == WHITE else ""
    body.append(f'<rect x="{x}" y="400" width="272" height="72" fill="{bg}"{stroke}/>')
    d, _ = text_path(t, "Inter[opsz,wght].ttf", 500, 15, 0)
    body.append(f'<path transform="translate({x + 20} 442)" d="{d}" fill="{fg}"/>')
(OUT / name("PALETTE-SHEET", "LIGHT")).write_text(svg(1280, 520, "\n".join(body), "GEM colour palette", "Four brand colours: Ink #12171D, Beige #BCACA7, Black #020202, White #FFFFFF, with the four approved text pairings and contrast ratios from the guidelines. Beige on white is prohibited (2.2:1)."))

# 4. status labels (four classes, DS README): APPROVED filled ink; CONDITIONAL 2px outline; PENDING VALIDATION dashed; REFERENCE dotted
for label, style in (("APPROVED", "fill"), ("CONDITIONAL", "solid"), ("PENDING VALIDATION", "dash"), ("REFERENCE", "dot")):
    d, w = text_path(label, "Inter[opsz,wght].ttf", 500, 12, 0.08); px, py = 16, 10
    W, H = round(w + px * 2), 36
    fg = WHITE if style == "fill" else INK
    attr = {"fill": f'fill="{INK}"', "solid": f'fill="none" stroke="{INK}" stroke-width="2"',
            "dash": f'fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 4"', "dot": f'fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="1 4" stroke-linecap="round"'}[style]
    body = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" {attr}/>\n<path transform="translate({px} 23)" d="{d}" fill="{fg}"/>'
    (OUT / name("STATUS-LABEL", label.replace(" ", "-"))).write_text(svg(W, H, body, f"Status label: {label}", f"Status class {label} per the GEM design system."))
print(sorted(p.name for p in OUT.iterdir()))
