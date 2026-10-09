"""RP01 SUCCESSOR of the ODI01 / AFC02 consistency checker (the original is unchanged). Explicit expectation changes vs the original (each is also listed in 11_RP01_Release_Consistency_Audit.md):
(1) check "Version string V3.0 RC2 present" is replaced by two checks: running-header RC2 label absent, and a V3.0 version label present;
(2) check "Document ID present" now expects GEM-(BG|DDS|PS)-V3.0 not followed by -RC2;
(3) the PDF export checks are removed because RP01 promotes no PDF (no PDF is authorized for external issue by FA01).
All other assertions are byte-for-byte the original.
"""
"""AFC02 COPY of the AFC01 corrected checker (reporting changed: assertions, not system consistency). AFC01 CORRECTED COPY (B anchor now required; output path argument). Original retained unchanged.
RC2 automated consistency check across A (pptx), B (pdf, unchanged) and C (pptx).
Writes qa/GEM_V3_RC2_Consistency_Report.md. Run from anywhere."""
import pathlib, re, subprocess, sys, zipfile
from pptx import Presentation

ROOT = pathlib.Path(sys.argv[1]).resolve()  # repo root passed explicitly
A = ROOT / "GEM_V3_RC2/01_working/A-RC2.pptx"
C = ROOT / "GEM_V3_RC2/01_working/C-RC2.pptx"
B = ROOT / "PartB_RC2/01_source/B-RC2.pptx"
BPDF = ROOT / "PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pdf"
import os  # ODI01: optional candidate-deck overrides (GEM_A_PATH, GEM_B_PATH, GEM_C_PATH, GEM_BPDF_PATH)
A = pathlib.Path(os.environ.get("GEM_A_PATH", A)); B = pathlib.Path(os.environ.get("GEM_B_PATH", B)); C = pathlib.Path(os.environ.get("GEM_C_PATH", C)); BPDF = pathlib.Path(os.environ.get("GEM_BPDF_PATH", BPDF))

def pptx_text(path):
    prs = Presentation(path); out = []
    for i, s in enumerate(prs.slides, 1):
        parts = []
        for sh in s.shapes:
            if sh.has_text_frame: parts.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                parts += [c.text for r in sh.table.rows for c in r.cells]
        if s.has_notes_slide: parts.append("[notes] " + s.notes_slide.notes_text_frame.text)
        out.append((i, "\n".join(parts)))
    return out

def pdf_text(path):
    txt = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout
    return [(i + 1, re.sub(r"[ \t]+", " ", p)) for i, p in enumerate(txt.split("\f")) if p.strip()]

def pptx_fonts(path):
    z = zipfile.ZipFile(path); fonts = set()
    for n in z.namelist():
        if n.startswith("ppt/slides/slide") and n.endswith(".xml"):
            fonts |= set(re.findall(r'typeface="([^"]+)"', z.read(n).decode("utf8")))
    return fonts

docs = {"A": pptx_text(A), "B": pptx_text(B), "C": pptx_text(C)}
rows = []  # (check, doc, result, detail)

def hits(doc, pattern, flags=re.I):
    return [n for n, t in docs[doc] if re.search(pattern, t, flags)]

def check(name, doc, pattern, expect_present, flags=re.I, note=""):
    h = hits(doc, pattern, flags)
    ok = bool(h) if expect_present else not h
    rows.append((name, doc, "PASS" if ok else "FAIL", (f"pages/slides {h[:12]}" if h else "none") + (f" · {note}" if note else "")))

for d in "ABC":
    check("Primary tagline present", d, r"HOSPITALITY, IN PERFECT PROPORTION", True, flags=0)
    check("Secondary line present (A, B) / absent (C by design)", d, r"Every arrival, precisely composed\.", d != "C")
    for hx in ["#12171D", "#BCACA7", "#020202", "#FFFFFF"]:
        check(f"Palette {hx}", d, re.escape(hx), True)
    for fam in ["Jost", "Inter", "Noto Sans Arabic"]:
        check(f"Type family named: {fam}", d, re.escape(fam), True)
    check("Prohibited: 'Jost light' / 'Jost Light' / Jost 300", d, r"Jost\s+(light|300)\b", False)
    check("Legacy fonts only as legacy/reference", d, r"(Futura PT|Montserrat|Aeonik|Satoshi|Whyte)(?![^.\n]*(legacy|reference|archive|retire|not for production|v1 only|V1))", False, note="any mention must sit in a legacy/reference sentence")
    check("Stale: 'not yet issued'", d, r"not yet issued", False)
    check("Stale: 'still to come'", d, r"still to come", False)
    check("Stale: 'Production Standards not issued'", d, r"Production Standards not issued", False)
    check("Stale: 'Release Candidate 1' as current edition", d, r"RELEASE CANDIDATE 1(?!.*undated)", False, flags=0)
    check("Running header no longer carries the RC2 label", d, r"(BRAND GUIDELINES|Digital Design System|PRODUCTION STANDARDS) V3\.0 RC2 [\u00b7]", False, flags=re.I)
    check("Version string 'V3.0' present", d, r"V3\.0", True, flags=0)
    check("Document ID present (promoted form, no -RC2)", d, r"GEM-(BG|DDS|PS)-V3\.0(?!-RC2)", True, flags=0)
    for st in ["APPROVED", "CONDITIONAL", "PENDING VALIDATION", "REFERENCE"]:
        check(f"Status term {st}", d, r"\b" + st + r"\b", True, flags=0)
    check("Authority order: register first, then Part A/B/C, formal standards, historical, benchmarks", d,
          r"Final Brand Approval Register.{0,80}Part A.{0,120}Part B.{0,120}Part C.{0,160}(formal|Formal) technical.{0,200}(historical|superseded).{0,120}(Benchmarks|benchmarks)", True, flags=re.S)
    check("Domain-ownership note", d, r"owning document governs", True)
    if d == "C":
        check("Governance roles cite the canonical register list (Part A 72)", d, r"Owners & Governance.{0,40}Part A slide 72", True, flags=re.S)
    else:
        check("Twelve-role governance list (register names)", d, r"Asset Librarian / Governance PM", True)
    check("Bilingual default: Arabic leads/first by default (S07)", d, r"(Arabic (leads|first)[^.\n]{0,80}default|default[^.\n]{0,60}Arabic (first|leads))[^.\n]{0,80}S07", True)
    check("No 'project-specific' language-lead rule", d, r"Which language leads[^\n]{0,40}PROJECT-SPECIFIC", False)
    check("File naming X12 pattern", d, r"GEM_\[STREAM\]_\[ASSET\]_\[VARIANT\]_vX\.Y_YYYYMMDD\.ext", True, flags=0)
    check("Old naming pattern absent", d, r"GEM_\[Category\]_\[Asset\]_\[Variant\]_vX\.Y\.ext", False, flags=0)
    check("Gate IDs VAL-02 / VAL-07 / AC20 present", d, r"VAL-02.*VAL-07.*AC20", True, flags=re.S)
    check("Six-level packaging hierarchy (T05)", d, r"(Six levels|six levels|six-level)", True)
    check("'Seven levels' absent", d, r"Seven levels", False)
    check("Tier status CONDITIONAL · AC03 / VAL-01", d, r"AC03[, /]+VAL-01", True)
    check("No invented production values (Pantone/CMYK/ΔE numbers)", d, r"(Pantone\s*\d{2,}|CMYK\s*\(?\s*\d{1,3}\s*[,/]\s*\d|ΔE\s*[<≤=]?\s*\d|Delta E\s*[<≤=]\s*\d|\b\d+(\.\d+)?\s*(mm|gsm)\b)", False)
    bad = [n for n, t in docs[d] for ln in t.splitlines()
           if re.search(r"VAL-\d\d[^\n]{0,30}\b(closed|complete|passed|accepted)\b", ln) and not re.match(r"\s*\d+\.\s", ln)
           and not re.match(r"\s*VAL-\d\d( to VAL-\d\d)?(, VAL-\d\d)* closed( or formally deferred)?\.\s*$", ln)]
    rows.append(("No evidence gate marked complete", d, "PASS" if not bad else "FAIL", f"pages/slides {bad[:8]}" if bad else "none · release-precondition checklist lines ('VAL-xx closed' as a condition before release) excluded"))

fa, fc = pptx_fonts(A), pptx_fonts(C)
rows.append(("Fonts used in deck (A)", "A", "PASS" if fa <= {"Jost", "Inter", "Noto Sans Arabic"} else "FAIL", ", ".join(sorted(fa))))
fb = pptx_fonts(B)
rows.append(("Fonts used in deck (B)", "B", "PASS" if fb <= {"Jost", "Inter", "Noto Sans Arabic", "Courier New"} else "FAIL", ", ".join(sorted(fb)) + " · Courier New = code specimen only, flagged [REQUIRES OWNER]"))
rows.append(("Fonts used in deck (C)", "C", "PASS" if fc <= {"Jost", "Inter", "Noto Sans Arabic"} else "FAIL", ", ".join(sorted(fc))))
for label, path in []:  # RP01: no PDFs promoted; PDF export checks removed (see header)
    if path.exists():
        info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout
        tagged = "yes" in re.search(r"Tagged:\s+(\w+)", info).group(1)
        fonts = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True).stdout.splitlines()[2:]
        names = sorted({re.sub(r"^[A-Z]{6}\+", "", l.split()[0]) for l in fonts if l.strip()})
        rows.append((f"PDF export tagged", label, "PASS" if tagged else "FAIL", f"Tagged: {tagged}"))
        rows.append((f"PDF embedded fonts", label, "INFO", ", ".join(names)))

# alt text
for label, path in [("A", A), ("B", B), ("C", C)]:
    z = zipfile.ZipFile(path); pics = 0; with_alt = 0
    for n in z.namelist():
        if n.startswith("ppt/slides/slide") and n.endswith(".xml"):
            x = z.read(n).decode("utf8")
            for m in re.finditer(r"<p:pic>.*?</p:pic>", x, re.S):
                pics += 1
                if re.search(r'descr="[^"]+"', m.group(0)): with_alt += 1
    rows.append(("Alt text on every picture", label, "PASS" if pics == with_alt else "FAIL", f"{with_alt}/{pics}"))

# cross-document: shared strings must be identical
def first(doc, pat):
    for n, t in docs[doc]:
        m = re.search(pat, t, re.S)
        if m: return re.sub(r"\s+", " ", m.group(0))[:160]
    return None
auth = {d: first(d, r"1 · V3 Final Brand Approval Register|1 V3 Final Brand Approval Register|1\. V3 Final Brand Approval Register") for d in "AC"}
# Part B states the ladder as a flat list ("Register / Part A ... / Part B ... / Part C ..."), so anchor on register-before-Part-A order.
auth["B"] = first("B", r"V3 Final Brand Approval Register[^\n]*\s+Part A, Brand Guidelines")
rows.append(("Cross-doc: authority list anchor present", "A/B/C", "PASS" if auth["A"] and auth["B"] and auth["C"] else "FAIL", f"A={bool(auth['A'])} B={bool(auth['B'])} C={bool(auth['C'])}"))

passes = sum(1 for r in rows if r[2] == "PASS"); fails = [r for r in rows if r[2] == "FAIL"]
info=sum(1 for r in rows if r[2]=="INFO")
md = ["# GEM™ V3.0 — Automated Consistency Assertions (promoted A · B · C) — RP01 successor reporting", "",
      f"**Result: {passes} AUTOMATED ASSERTIONS PASSED · {len(fails)} FAILED · {info} INFO records.**",
      "",
      "This is **not** a confirmation of full system consistency. Each assertion is a text/term/metadata check (term present, stale phrase absent, PDF tagged flag, picture alt-text count, authority-list anchor). It does not test meaning, visual rendering, runtime behaviour or native-application behaviour. See `09_Consistency_Coverage_Report.md` for what is automated, manually verified, inherited or not tested.", "",
      "Inputs: the RP01 promoted Part A, Part B and Part C PPTX files (see 07_RP01_Release_File_Index.csv). No PDFs are promoted, so the PDF export checks of the original are removed.", "",
      "| Check | Doc | Result | Detail |", "|---|---|---|---|"]
for r in rows: md.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
md += [""]
(pathlib.Path(sys.argv[2])).write_text("\n".join(md), encoding="utf-8")
print(f"{passes} PASS, {len(fails)} FAIL")
for r in fails: print("  FAIL", r)
