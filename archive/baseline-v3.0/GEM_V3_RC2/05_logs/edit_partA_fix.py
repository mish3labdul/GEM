import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pptx import Presentation
from pptx_helpers import *
F = pathlib.Path(__file__).resolve().parents[1] / "01_working" / "A-RC2.pptx"
prs = Presentation(F); S = lambda n: prs.slides[n-1]
def geo(sh): return f"{sh.name} x={sh.left/914400:.2f} y={sh.top/914400:.2f} w={sh.width/914400:.2f} h={sh.height/914400:.2f}"

t = find(S(3), "Dielines, materials"); defit(t); set_text(t, "Dielines, materials, tolerances, supplier proofs. Issued as RC2, pending production validation."); move(t, top=5.30, height=0.72)
t = find(S(3), "Domain ownership"); defit(t)
t = find(S(4), "Shape carries"); defit(t)
t = find(S(33), "NEVER. 2.2"); defit(t); move(t, top=4.42, height=1.05)
t = find(S(34), "Display and headings: 400"); print("34", geo(t)); defit(t); move(t, top=t.top/914400 - 0.32, height=t.height/914400 + 0.32)
t = find(S(36), "Never track Arabic"); defit(t); move(t, top=6.08, height=0.5)
t = find(S(38), "Both languages share"); defit(t)
t = find(S(41), "Let a form leave"); defit(t)
t = find(S(45), "Glyphs help people"); defit(t)
t = find(S(48), "REFERENCE · CONCEPT / NOT PRODUCTION PHOTOGRAPHY · PLAIN"); defit(t)
t = find(S(50), "REFERENCE · CONCEPT"); print("50", geo(t)); defit(t); move(t, width=10.2)
t = find(S(51), "About 1.5 seconds"); print("51", geo(t)); defit(t); move(t, top=t.top/914400 - 0.22, height=0.5)
t = find(S(53), "Near-square"); defit(t)
t = find(S(60), "Same logo"); defit(t)
t = find(S(61), "The brand is seen first"); defit(t)
t = find(S(65), "One direction"); defit(t)
t = find(S(65), "PROJECT-SPECIFIC"); defit(t); move(t, top=6.25, height=0.5)
t = find(S(68), "CONCEPT / NOT PRODUCTION ARTWORK · ARABIC"); defit(t)
t = find(S(69), "One form, one line"); print("69", geo(t)); defit(t); move(t, height=0.5)
t = find(S(72), "Roles follow"); defit(t)
t = find(S(75), "Approval, checksum"); defit(t)
t = find(S(78), "Also open"); defit(t); set_text(t, "Also open: VAL-13 to VAL-17, VAL-19 to VAL-21 and the template deliverables (AB10, AB11, W01–W14). IDs follow the V3 Approval Register."); move(t, top=6.47, height=0.3)
t = find(S(79), "Change log"); defit(t); set_text(t, "Change log · RC2, 2026-10-06: synchronized with Part B and Part C RC2 and the V3 Approval Register (authority order, twelve roles, VAL IDs, S07 wayfinding default, six-level hierarchy T05, X12 naming, edition vocabulary, alt text). Full record: GEM_V3_RC2_Release_Notes."); move(t, top=6.3, height=0.5)
t = find(S(1), "V3.0 RC2"); defit(t)
prs.save(F); print("saved")
