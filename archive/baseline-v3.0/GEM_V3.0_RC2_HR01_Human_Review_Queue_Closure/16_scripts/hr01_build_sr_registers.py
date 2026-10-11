#!/usr/bin/env python3
"""HR01 screen-reader registers (07 test register, 08 reading-order sample).

Run from the repository root:  python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_build_sr_registers.py [results.json]
Without results.json every test is PENDING (this is the state written BEFORE any test is run).
With results.json (local-only; {test_id: {"result":..., "note":..., "by":...}}) the results columns are filled; nothing is invented.
Candidate hashes are read from the candidate files. Relative paths only; no document text is copied.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure")
CAND = PKG / "18_candidate_corrections"
RES = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}
sha12 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
EM = "—"
F = {
    "A": "GEM Brand Guidelines V3.0 %s Part A %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM),
    "B": "GEM Digital Design System V3.0 %s Part B %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM),
    "C": "GEM Production Standards V3.0 %s Part C %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM),
    "D": "GEM Amenities & Packaging %s Concept Product Portfolio V3.0 %s Part D %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM, EM),
}
W = {n: "GEM_Letterhead_%s_HR01_CANDIDATE.docx" % n for n in ("Arabic_First_Page", "Arabic_Continuation", "Bilingual_First_Page", "Bilingual_Continuation")}
cand_all = "Parts A-D HR01 candidates (" + ", ".join("%s %s" % (k, sha12(CAND / F[k])) for k in "ABCD") + ")"
cand_word = "4 changed Word HR01 candidates (" + ", ".join("%s %s" % (k.replace("_", " "), sha12(CAND / v)) for k, v in W.items()) + ")"

# (id, surface, candidate, scenario RESTATED against the HR01 candidates, original AX01 definition (provenance), what to listen for, gate relevance)
TESTS = [
    ("SR-01", "VoiceOver + PowerPoint", "Part D HR01 candidate (%s)" % sha12(CAND / F["D"]), "Navigate slides 1-24 by title; each slide announces its heading as the title.",
     "Navigate slides 1-24 by title (rotor / outline); confirm each slide announces its heading as the title", "The slide title is announced for every slide", "VAL-08"),
    ("SR-02", "VoiceOver + PowerPoint", "Part A HR01 candidate (%s)" % sha12(CAND / F["A"]), "The 27 Part A slides that had no title now carry an approved title (off-slide placeholder): confirm each announces its approved title and navigation by title reaches them. Spot list: slides 1, 12, 38, 65, 76, 80.",
     "Slides lacking a recognized title (27): confirm navigation still works, note which slides are skipped by title", "Approved title announced; no slide skipped", "VAL-08"),
    ("SR-03", "VoiceOver + PowerPoint", cand_all, "Objects marked decorative in HR01 (87 shapes, e.g. Part A slides 30, 43, 63; Part C slides 11, 19; Part B slide 14) are NOT announced; the two specimen descriptions (Part B slides 8 and 14) are.",
     "Decorative objects: confirm marked-decorative rules/panels/backgrounds are NOT announced", "No hairline rule, panel, frame, swatch or checkbox announced", "VAL-08"),
    ("SR-04", "VoiceOver + PowerPoint", "Part A slide 15; Part B slides 4-5; Part C slide 4 (HR01 candidates)", "Table navigation: header row announced per column; cell-by-cell traversal.",
     "Table navigation: header row announced per column; cell-by-cell traversal", "Column header read with each cell", "VAL-08"),
    ("SR-05", "VoiceOver + PowerPoint", "Part D HR01 candidate (%s)" % sha12(CAND / F["D"]), "All 31 Part D pictures now carry approved alt text (23 new, 6 logos 'GEM logo', 2 materials): confirm the approved description is announced for each picture on slides 1, 3-10, 13, 16, 17, 19, 20, 24.",
     "Image alt text: confirm what is announced for pictures with and without descriptions (23 product images had none)", "Approved alt text announced; Arabic label text is not read out by guess", "VAL-08"),
    ("SR-06", "VoiceOver + PowerPoint", "Part A HR01 candidate slides 37, 38, 39, 65, 66, 68; Part B slide 9", "Arabic/English language switching: Arabic voiced with an Arabic voice, English with an English voice (includes the 3 revised Arabic strings on slides 38, 65, 68).",
     "Arabic/English language switching: Arabic text voiced with an Arabic voice, English with an English voice", "Arabic voice for Arabic text; English voice for English", "VAL-07; VAL-08"),
    ("SR-07", "VoiceOver + PowerPoint", "Part A HR01 candidate slide 39 (booking line)", "Mixed Arabic/Latin paragraph: Arabic run then the Latin identifier read with an English voice, digits as digits, in logical order.",
     "Mixed Arabic/Latin paragraph: Arabic run then 'GEM-0000' read with an English voice, digits as digits, in logical order", "Identifier read letter-by-letter or as digits in an English voice, after the Arabic words", "VAL-07"),
    ("SR-08", "VoiceOver + PowerPoint", "Sample in 08_HR01_Reading_Order_Manual_Review.csv (13 slides, fixed by rule before testing)", "Reading order of the sampled slides: compare VoiceOver order with the intended order (title first, then top-to-bottom / left-to-right; Arabic-first pairs for bilingual).",
     "Reading order of flagged slides: compare read order with intended order for a sample incl. Arabic/bilingual pairs", "Order matches the intended order; note any slide that does not", "VAL-07; VAL-08"),
    ("SR-09", "VoiceOver + Word", cand_word, "Header/footer behaviour: first-page vs continuation header, footer address block, localized page label 'page n of N' fields in the 4 Arabic/bilingual templates (the other 4 templates are unchanged from AX01).",
     "Header/footer behaviour: first-page vs continuation header, footer address block, 'Page n of N' fields", "Footer read in sensible order; page label reads as page number of total pages", "VAL-08; VAL-15"),
    ("SR-10", "VoiceOver + Word", cand_word, "Arabic paragraph language/direction announcements; mixed [DATE]/[REFERENCE NUMBER] placeholders; revised subject, salutation, disclaimer and closing.",
     "Arabic paragraph language/direction announcements; mixed [DATE]/[REFERENCE] placeholders", "Arabic read right-to-left with an Arabic voice; Latin placeholders in an English voice", "VAL-07; VAL-08"),
    ("SR-11", "Preview / Acrobat + VoiceOver", "INTERNAL WORKING PDFs", "Tagged-PDF reading order and Arabic text layer. HR01 regenerates no PDF.",
     "Tagged-PDF reading order and Arabic text layer (copy/search, R03-03, LH03)", "n/a unless a PDF is regenerated", "VAL-15; D8"),
    ("SR-12", "NVDA / JAWS (Windows)", "Parts A-D, letterheads", "Cross-reader confirmation of SR-01..SR-10. No Windows environment.",
     "Cross-reader confirmation of SR-01..SR-10", "n/a on this machine", "VAL-08"),
    ("SR-13", "Keyboard-only / focus", "Part A HR01 candidate", "Keyboard-only navigation through slide content in edit mode and slide-show mode (no mouse).",
     "Keyboard navigation of slide content in edit and slide-show modes", "Focus moves through the content logically and visibly", "VAL-08"),
]
with open(PKG / "07_HR01_Screen_Reader_Test_Register.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["Test ID", "Surface", "Candidate and hash", "Scenario (restated against HR01 candidates)", "Original AX01 definition (provenance)", "What to listen for",
                "Gate relevance", "Evidence type", "Result", "Observer", "Note", "Status"])
    for t in TESTS:
        r = RES.get(t[0], {})
        w.writerow([*t, ("REVIEWER OBSERVED \u2014 MASHAL (macOS VoiceOver)" if r.get("result") == "PASS" else ("NONE \u2014 DEFERRED" if r.get("result") else "")), r.get("result", ""), r.get("by", ""), r.get("note", ""), r.get("status", "PENDING")])

# ------------------------------------------------------------------ reading-order sample (rules fixed before testing)
SAMPLE = [("R1", "A", 37), ("R1", "A", 38), ("R1", "A", 39), ("R1", "A", 65), ("R1", "A", 66), ("R1", "A", 68), ("R1", "B", 9),
          ("R2", "A", 72), ("R2", "B", 3), ("R2", "C", 73), ("R2", "D", 21), ("R3", "A", 1), ("R3", "C", 1)]
RULES = {"R1": "All 7 slides carrying Arabic content (AX01 register: Arabic MANUAL TEST)",
         "R2": "Highest z-order/visual-order inversion count among the checker-flagged slides of each deck (A 72 = 42, B 3 = 20, C 73 = 125, D 21 = 100; AX01 register)",
         "R3": "The two covers whose title mapping AX01 held (now an off-slide title); confirms the title is read first and nothing else moved"}
with open(PKG / "08_HR01_Reading_Order_Manual_Review.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["Sample ID", "Selection rule", "Rule text", "Document", "Slide", "Intended order", "Observed order matches?", "Observer", "Note", "Status"])
    for i, (rule, k, s) in enumerate(SAMPLE, 1):
        r = RES.get("SR-08:%s%d" % (k, s), {})
        w.writerow(["RO-%02d" % i, rule, RULES[rule], "Part " + k, s, "Title first, then top-to-bottom / left-to-right; Arabic-first pairs for bilingual",
                    r.get("result", ""), r.get("by", ""), r.get("note", ""), r.get("status", "PENDING")])
print("tests:", len(TESTS), "reading-order sample:", len(SAMPLE))
