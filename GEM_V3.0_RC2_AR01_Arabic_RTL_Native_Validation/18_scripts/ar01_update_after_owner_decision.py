"""AR01 owner-decision pass: update the committed CSVs from the 'proposed / Word NOT TESTED' state to the post-correction, post-native-Word state. Idempotent; text edits only (no Arabic). Usage: ar01_update_after_owner_decision.py <package_dir>"""
import sys, csv, re, hashlib, os
P = sys.argv[1]
sh = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
def load(n): return list(csv.reader(open(f"{P}/{n}", encoding='utf8')))
def save(n, rows): csv.writer(open(f"{P}/{n}", 'w', newline='', encoding='utf8')).writerows(rows)
NATIVE_WORD = "native Word PASS in AR01 (4 templates opened without repair; Arabic paragraphs RTL, Latin runs LTR, Noto Sans Arabic, not bold, spacing 0)"
# 05
r = load("05_AR01_RTL_Bidi_Findings.csv"); h = r[0]; ic, ir = h.index("Corrected in AR01?"), h.index("Result after")
for row in r[1:]:
    if row[0] in ("Part A", "Part B") and row[ic].startswith("No"):
        row[ic] = "YES — owner decision 1 (pPr rtl=1; Arabic run lang ar-SA); no text/font/size/tracking/geometry change"; row[ir] = "native PowerPoint revalidation PASS: requested direction right-to-left, text bounds identical, no clipping"
    row[:] = [c.replace("PASS (static OOXML) — native Word NOT TESTED in AR01", "PASS (static OOXML + native Word, AR01)") for c in row]
    row[:] = [c.replace("LibreOffice render order plausible", "LibreOffice render order plausible; native Word: character positions confirm order") if "native Word: character positions" not in c else c for c in row]
save("05_AR01_RTL_Bidi_Findings.csv", r)
# 09
r = load("09_AR01_Mixed_Run_Test_Matrix.csv")
for row in r[1:]:
    row[:] = [c.replace("Word native NOT TESTED", "native Word PASS (Arabic segment RTL, Latin placeholder LTR by per-character positions)") for c in row]
    row[:] = [c.replace("no direction-dependent difference for a fully bracketed single-script string)", "native bracket glyph positions and raster unchanged apart from sub-pixel edges; the PDF text layer of both pages now records the opening/closing brackets in the logical RTL order)") for c in row]
    row[:] = [c.replace("Prior Word-for-Mac evidence (R03-02) inherited, not re-verified", "Prior Word-for-Mac evidence (R03-02) remains inherited; AR01 native Word observation recorded separately (17_qa/native_word_paragraphs.csv)") for c in row]
save("09_AR01_Mixed_Run_Test_Matrix.csv", r)
# 10
r = load("10_AR01_Technical_Correction_Register.csv"); out = [r[0]]
for row in r[1:]:
    if "proposed, NOT applied" in row[0]:
        doc = row[0].replace("(proposed, NOT applied)", "(AR01 candidate)")
        row = [doc, row[1], row[2], "a:pPr rtl absent; a:rPr lang=\"en-US\"", "a:pPr rtl=\"1\"; a:rPr lang=\"ar-SA\"",
               "Technical language/direction metadata defect (owner decision 1: one uniform model across all 12 PowerPoint Arabic paragraphs). Native PowerPoint now reports right-to-left; text bounds identical to the baseline; no wording, font, size, tracking, bold, alignment or geometry change.",
               row[6], "no", "Box geometry: no. Native text bounds identical (0.1 pt). Sub-pixel glyph-edge differences only.", "no", "Applied (owner decision 1)"]
    out.append(row)
save("10_AR01_Technical_Correction_Register.csv", out)
# 05 / 10: final owner decision: slide 39 Text 8 run split
r = load("05_AR01_RTL_Bidi_Findings.csv"); ir = r[0].index("Result after")
for row in r[1:]:
    if row[0] == "Part A" and row[1] == "39" and row[2] == "Text 8" and "run split" not in row[ir]: row[ir] += "; final owner decision: run split into Arabic run (ar-SA) and Latin identifier run (en-US), natively revalidated (all 18 character positions unchanged)"
save("05_AR01_RTL_Bidi_Findings.csv", r)
r = load("10_AR01_Technical_Correction_Register.csv")
if not any("run split" in c for row in r for c in row):
    r.append(["Part A (AR01 candidate)", "39", "Text 8 — mixed label + Latin identifier (run split)", "one run, lang=\"ar-SA\" (Arabic words, spaces, GEM-0000)", "run 1 (Arabic words + the following space, 10 characters) lang=\"ar-SA\"; run 2 (GEM-0000, 8 characters) lang=\"en-US\"",
              "Final owner decision: script-appropriate runs for proofing and assistive technology. Same rPr (font trio, size, colour) on both runs; no control characters, spaces, direction attributes or geometry change; digits and hyphen stay inside the Latin run.",
              "Register M06 · M12 (standardised codes stay LTR inside RTL) · M05", "no", "Box geometry: no. All 18 native character positions identical; slide capture pixel-identical.", "no", "Applied (final owner decision; run split)"])
save("10_AR01_Technical_Correction_Register.csv", r)
# 11
r = load("11_AR01_Native_Arabic_Reviewer_Queue.csv"); ix = r[0].index("Technical issue resolved?")
for row in r[1:]:
    if row[ix].startswith("n/a (rendering acceptable"): row[ix] = "Yes — direction/language metadata applied (owner decision 1) and natively revalidated; wording unreviewed"
    row[ix] = row[ix].replace("Word native NOT TESTED", "native Word PASS (technical only); wording unreviewed")
save("11_AR01_Native_Arabic_Reviewer_Queue.csv", r)
# 04
r = load("04_AR01_Language_Metadata_Findings.csv")
if r[0][-1] != "Status after AR01 (owner decision 1)":
    r[0].append("Status after AR01 (owner decision 1)")
    for row in r[1:]: row.append("CORRECTED in AR01 candidate: pPr rtl=1; Arabic run lang ar-SA" if row[0] in ("Part A", "Part B") else "No change (Word template not modified; native Word PASS in AR01)")
    save("04_AR01_Language_Metadata_Findings.csv", r)
# 02
r = load("02_AR01_Candidate_Baseline.csv")
if not any("AR01 CANDIDATE" in (c or "") for row in r for c in row):
    r.append(["Part A (AR01 candidate)", "GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/19_candidate_corrections/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx", "AR01 (derives from D3 Part A; 11 paragraphs on slides 37, 38, 39, 65, 66, 68 metadata-corrected)", sh(f"{P}/19_candidate_corrections/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx"), "80 slides", "YES", "YES", "UNAPPROVED controlled candidate", "WORKING CANDIDATE (not authoritative)"])
    r.append(["Part B (AR01 candidate)", "GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/19_candidate_corrections/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx", "AR01 (derives from NP01-R1 Part B; slide 9 metadata-corrected; NP01-R1 slide-30 fix preserved byte-identically)", sh(f"{P}/19_candidate_corrections/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx"), "35 slides", "YES", "NO", "UNAPPROVED controlled candidate", "WORKING CANDIDATE (not authoritative)"])
for row in r:
    if row[0] == "Part A (AR01 candidate)": row[3] = sh(f"{P}/19_candidate_corrections/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx"); row[2] = "AR01 (derives from D3 Part A; 11 paragraphs on slides 37, 38, 39, 65, 66, 68 metadata-corrected; slide 39 Text 8 split into Arabic and Latin runs)"
    if row[0] == "Part B (AR01 candidate)": row[3] = sh(f"{P}/19_candidate_corrections/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx")
save("02_AR01_Candidate_Baseline.csv", r); print("updated")
