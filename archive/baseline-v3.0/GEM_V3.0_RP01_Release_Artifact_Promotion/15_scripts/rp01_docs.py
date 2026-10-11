#!/usr/bin/env python3
"""RP01 documents and registers that depend on the build result.
Run from the repository root after rp01_build.py, rp01_preservation.py and the visual regression:
  python3 -I GEM_V3.0_RP01_Release_Artifact_Promotion/15_scripts/rp01_docs.py <visual_csv>
Writes 01, 05, 06, 07, 09, 10, 11, 12, 13, 14 and the 17_release_artifacts/06 and 08 pointer files. Generated text only restates evidence in the registers."""
import csv
import hashlib
import subprocess
import sys
from collections import Counter
from pathlib import Path

RP = Path("GEM_V3.0_RP01_Release_Artifact_Promotion")
OUT = RP / "17_release_artifacts"
EM, TM, DOT = "—", "™", "·"
BASE = "GEM%s V3.0 %s OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE %s FORMAL DEFERRALS RECORDED %s ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY" % (TM, EM, EM, EM)
HEAD = "**%s**\nAC20: AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS (FA01). RP01 promotes release-state labels only; no gate is closed.\n\n" % BASE
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def w(name, body):
    (RP / name).write_text(body.rstrip() + "\n", encoding="utf-8")


def wcsv(name, header, rows):
    with open(RP / name, "w", encoding="utf-8", newline="") as fh:
        c = csv.writer(fh, lineterminator="\n")
        c.writerow(header)
        c.writerows(rows)


promo = list(csv.DictReader(open(RP / "03_RP01_Artifact_Promotion_Register.csv", encoding="utf-8")))
base = list(csv.DictReader(open(RP / "02_RP01_Authorized_Baseline.csv", encoding="utf-8")))
pres = list(csv.DictReader(open(RP / "16_qa" / "rp01_preservation.csv", encoding="utf-8")))
labels = list(csv.DictReader(open(RP / "04_RP01_Status_Label_Change_Register.csv", encoding="utf-8")))
P = {r["Artifact ID"]: r for r in promo}

# ---------------------------------------------------------------- visual regression (heuristic class + recorded human review of every flagged page)
vis = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
REVIEWED = {("P-A", "78"), ("P-A", "79"), ("P-B", "4"), ("P-B", "30"), ("P-B", "31"), ("P-B", "33"), ("P-B", "34"), ("P-C", "1"), ("P-C", "75"), ("P-C", "76"), ("P-C", "77"), ("P-D", "23")}
flagged = {(r["Artifact"], r["Page/slide"]) for r in vis if r["Class"] == "VISIBLE REGRESSION"}
assert flagged == REVIEWED, "flagged set changed; re-review required: %s" % sorted(flagged ^ REVIEWED)
vrows = []
for r in vis:
    cls, note = r["Class"], ""
    if cls == "VISIBLE REGRESSION":
        cls, note = "EXPECTED RELEASE-LABEL CHANGE ONLY", "automatic flag (large diff box); human side-by-side review: only the intended status wording changed and re-flowed inside its own text box; no overflow, clipping or unrelated change"
    vrows.append([r["Artifact"], r["Page/slide"], cls, r["Class"], r["Differing pixels"], r["Diff bbox (px @72dpi)"], note])
wcsv("16_qa/rp01_visual_regression.csv", ["Artifact", "Page/slide", "Final class", "Automatic class", "Differing pixels", "Diff bbox (px @72dpi)", "Human review note"], vrows)
vc = Counter(r[2] for r in vrows)
per = {}
for r in vrows:
    per.setdefault(r[0], Counter())[r[2]] += 1
w("10_RP01_Visual_Regression.md", "# 10 · RP01 %s Visual Regression\n\n" % EM + HEAD + """## Method
Every FA01-baseline source and every promoted file was rendered with LibreOffice (headless PDF export) and rasterized at 72 dpi; each page or slide was compared pixel by pixel (difference above 24 per channel). This is a LibreOffice render, not a native PowerPoint or Word render: it detects unintended change, it does not certify native layout. Native opens are recorded in 09.

## Result
| Final class | Pages / slides |
|---|---|
| PIXEL IDENTICAL | %(ident)d |
| EXPECTED RELEASE-LABEL CHANGE ONLY | %(exp)d |
| SUB-PIXEL NATIVE VARIANCE | %(sub)d |
| VISIBLE REGRESSION | %(reg)d |
| **Total compared** | **%(tot)d** |

12 pages were flagged automatically because their differing area was large (status and document-control slides whose wording changed and re-flowed). Each was reviewed side by side by the main session: A78, A79, B4, B30, B31, B33, B34, C1, C75, C76, C77, D23. Findings: only the intended status wording changed; four layout problems found in the first LibreOffice build (Part A and Part C change-log lines, the Part C edition-state cell, the Part C slide 75 gate cell) were fixed by shortening the new text and the pages re-rendered; three further problems visible only in native PowerPoint (A79, B33, C77) were fixed afterwards (see 09) and the visual regression was re-run. A single known pre-existing collision on A78 (left column text meeting the right column under the substitute font) is present in the source render too.

Per artifact: %(per)s

Letterheads: the four English templates differ only in the removed footer marker line; the four Arabic and bilingual templates differ only in the added restriction line at the footer; nothing above the footer moved.

Full page-level table: `16_qa/rp01_visual_regression.csv`.
""" % dict(ident=vc["PIXEL IDENTICAL"], exp=vc["EXPECTED RELEASE-LABEL CHANGE ONLY"], sub=vc["SUB-PIXEL NATIVE VARIANCE"], reg=vc["VISIBLE REGRESSION"], tot=len(vrows),
           per="; ".join("%s %s" % (k, dict(v)) for k, v in sorted(per.items()))))

# ---------------------------------------------------------------- scope matrix, restricted register, file index
S_H = ["Artifact", "Category", "Promoted path", "SHA256", "Internal use", "External issue eligibility (artifact level)", "Restriction", "FA01 basis"]
EXT_OK = "ELIGIBLE (artifact level) after this promotion; no external issue has occurred or is authorized by RP01 itself"
srows = []
for aid in ("P-A", "P-B", "P-C"):
    p = P[aid]
    srows.append([p["Artifact"], p["Category"], p["Promoted path (in RP01)"], p["Promoted SHA256"], "YES", EXT_OK + " (full PPTX only)", p["Restriction"], "FA01 10: baseline member; external NOT YET pending relabel pass (done here)"])
p = P["P-D"]
srows.append([p["Artifact"], p["Category"], p["Promoted path (in RP01)"], p["Promoted SHA256"], "YES", "ELIGIBLE as a CONCEPT portfolio only (full PPTX); never as production artwork", p["Restriction"], "FA01 10: concept portfolio only"])
for aid in ("L-English_First_Page", "L-English_Continuation", "L-Executive", "L-Minimal"):
    p = P[aid]
    srows.append([p["Artifact"], p["Category"], p["Promoted path (in RP01)"], p["Promoted SHA256"], "YES", EXT_OK + " (DOCX template)", p["Restriction"], "FA01 10: not affected by D8"])
for aid in ("L-Arabic_First_Page", "L-Arabic_Continuation", "L-Bilingual_First_Page", "L-Bilingual_Continuation"):
    p = P[aid]
    srows.append([p["Artifact"], p["Category"], p["Promoted path (in RP01)"], p["Promoted SHA256"], "YES, controlled internal use only, D8 markings on every page", "NO", p["Restriction"], "FA01 10 and 07: AFFECTED BY D8"])
for aid in ("T-JSON", "T-CSS"):
    p = P[aid]
    srows.append([p["Artifact"], p["Category"], p["Promoted path (in RP01)"], p["Promoted SHA256"], "YES", "ELIGIBLE as documentation of the token values; no component implementation authorized", p["Restriction"], "FA01 10: digital components"])
srows.append(["Official Logo Kit (GEM_Brand_Assets_v1.0)", "D WORKING ASSET / PRODUCTION-MASTER ACCEPTANCE PENDING", "GEM_Brand_Assets_v1.0/ (referenced in place, not copied)", "04_official_kit/SHA256SUMS.txt %s" % sha("GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt"),
              "YES (working use)", "RESTRICTED: not released or labelled as a production master", "WORKING ASSETS; acceptance as production master PENDING (VAL-02 deferred)", "FA01 10: logo kit RESTRICTED"])
srows.append(["Production vectors (kit SVG/EPS/PDF masters)", "D WORKING ASSET", "GEM_Brand_Assets_v1.0/ (in place)", "see kit checksum list", "YES (working use)", "NO as production masters", "Not accepted production masters (VAL-02, AC07 deferred)", "FA01 10"])
srows.append(["PDF release artifacts", "NONE GENERATED", "n/a", "n/a", "n/a", "NO", "FA01 authorizes no PDF for external issue; none was generated; the PPTX and DOCX files are authoritative", "FA01 10: PDF release artifacts"])
srows.append(["Part A slides 37, 38, 39, 65, 66, 68; Part B slide 9 (Arabic)", "B RESTRICTED EXTRACT", "inside the Part A and Part B PPTX", "n/a", "YES", "Full PPTX only; NO PDF or DOCX extract", "AFFECTED BY D8: an extract is not issued externally until the D8 tests pass", "FA01 07"])
srows.append(["Part D images with Arabic inside the picture", "B RESTRICTED EXTRACT", "inside the Part D PPTX", "n/a", "YES", "Full concept PPTX only; NO PDF or DOCX extract", "No text layer; Arabic not approved; D8", "FA01 07"])
wcsv("05_RP01_Release_Scope_Matrix.csv", S_H, srows)

rrows = []
for aid in ("L-Arabic_First_Page", "L-Arabic_Continuation", "L-Bilingual_First_Page", "L-Bilingual_Continuation"):
    p = P[aid]
    rrows.append([p["Artifact"], p["Promoted path (in RP01)"], p["Promoted SHA256"], "YES, controlled internal only", "NO (DOCX and PDF)", "D8: Windows Word, Word Online, Acrobat text layer, tagged PDF, reading order, NVDA/JAWS, accessibility QA, final localization approval not performed",
                  "Footer carries WORKING APPLICATION / PENDING VALIDATION and PENDING LOCALIZATION APPROVAL verbatim plus CONTROLLED INTERNAL TEMPLATE %s EXTERNAL ISSUE RESTRICTED PENDING D8 VALIDATION" % DOT, "A native macOS pass does not satisfy D8"])
rrows.append(["Part A Arabic slides 37, 38, 39, 65, 66, 68", "inside the Part A PPTX", "n/a", "YES", "Full PPTX only; no PDF/DOCX extract", "D8", "No restriction label added to the slides (the governance records state the extract rule)", "FA01 07 and this register"])
rrows.append(["Part B Arabic slide 9", "inside the Part B PPTX", "n/a", "YES", "Full PPTX only; no PDF/DOCX extract", "D8", "as above", "FA01 07"])
rrows.append(["Part D images with baked-in Arabic", "inside the Part D PPTX", "n/a", "YES", "Full concept PPTX only; no PDF/DOCX extract", "D8; Arabic not approved (AC10 deferred)", "CONCEPT / NOT PRODUCTION ARTWORK stays on the slides", "FA01 07"])
rrows.append(["Official Logo Kit and production vectors", "GEM_Brand_Assets_v1.0/", "see kit checksum list", "YES (working use)", "RESTRICTED (not a production master)", "VAL-02, AC07 deferred", "Kit README states WORKING ASSETS; production-master acceptance PENDING", "FA01 10"])
wcsv("06_RP01_Restricted_Artifact_Register.csv", ["Artifact", "Path", "SHA256", "Internal use", "External issue", "Reason", "Marking / control", "Basis"], rrows)

irows = []
for r in promo:
    if r["Artifact ID"].startswith("K-"):
        continue
    irows.append([r["Promoted path (in RP01)"].replace("17_release_artifacts/", ""), r["Artifact"], r["Category"], r["Promoted SHA256"], Path(RP / r["Promoted path (in RP01)"]).stat().st_size])
for extra, desc in (("07_tokens/README.md", "Token package README"), ("06_brand_assets/README.md", "Logo kit pointer and checksum verification"), ("08_release_index/RELEASE_INDEX.md", "Release index")):
    irows.append([extra, desc, "index / documentation", sha(OUT / extra), (OUT / extra).stat().st_size]) if (OUT / extra).exists() else None
wcsv("07_RP01_Release_File_Index.csv", ["Path (under 17_release_artifacts)", "Artifact", "Category", "SHA256", "Bytes"], irows)

# ---------------------------------------------------------------- native validation
w("09_RP01_Native_Validation.md", "# 09 · RP01 %s Native Validation (macOS)\n\n" % EM + HEAD + """Native validation was run on scratch copies of the promoted files (never on the files in this package, so no Office lock files were created here). It is macOS PowerPoint and macOS Word only: Windows Word, Word Online, Acrobat, NVDA and JAWS were not tested and **a native macOS pass does not satisfy D8**.

## PowerPoint
| Deck | Opened natively | Repair prompt | Slides | Notes |
|---|---|---|---|---|
| Part A (80 slides) | yes | none | 80 | cover shows the promoted wording |
| Part B (35 slides) | yes | none | 35 | Accessibility Assistant opened (see below) |
| Part C (78 slides) | yes | none | 78 | cover shows V3.0 and PENDING PRODUCTION VALIDATION |
| Part D (24 slides) | yes | none | 24 | cover shows V3.0 and CONCEPT / NOT PRODUCTION ARTWORK |

No missing-font or missing-media dialog appeared for any deck.

**Accessibility (native).** PowerPoint's Accessibility Assistant was run on the promoted Part B and, for comparison, on the HR01 source Part B. The two results are identical: every rule category (text contrast, missing alt text, missing audio/video subtitles, missing table header, merged or split cells, missing slide title, duplicate slide title, default and duplicate section name, restricted access) reports no violations; the only count shown is "Check reading order: 35", PowerPoint's manual-review advisory (one per slide, 35 slides). The panel's headline reads "Keep going!" only because that advisory remains. Each category was opened for Part B and states "no accessibility violations for this rule". The first RP01 pass mis-described this panel as still updating; that was wrong and is corrected here. FA01 `10` records the older checker wording "no missing alt text or title" for Part B; the two records agree in substance (no alt-text, title or table violations); the Assistant is a newer panel that also lists categories the older rule did not. The native Assistant was not run on Parts A, C and D; for those the position rests on the AX01 static predicates (recomputed, identical to source) and the structural identity proof in `16_qa/rp01_preservation.csv`. No new accessibility conformance claim is made.

**Native layout check of the changed slides.** After the LibreOffice review, the changed slides were viewed natively in PowerPoint (which uses the installed Jost and Inter fonts and wraps differently): Part A slides 1, 72, 78, 79, 80; Part B 1, 30 (build check), 31, 33, 34; Part C 1, 75, 76, 77; Part D 1, 22, 23, 24. Three native overflows were found in the first build (A79 change-log line wrapping into the footer, B33 version-history heading wrapping into the next paragraph, C77 edition-state cell wrapping to its border) and fixed by shortening the new text; the chain was re-run and those slides were re-checked natively. Pages not listed were not viewed natively (their changes are a running-header word removal or a shorter replacement).

## Word
| Template | Opened | Repair prompt | Fields | Accessibility Assistant |
|---|---|---|---|---|
| English First Page | yes | none | standard update-fields prompt declined | Looks good, no issues |
| English Continuation | yes | none | as above | Looks good, no issues |
| Executive | yes | none | as above | Looks good, no issues |
| Minimal | yes | none | as above | Looks good, no issues |
| Arabic First Page | yes | none | as above | Looks good, no issues |
| Arabic Continuation | yes | none | as above | Looks good, no issues |
| Bilingual First Page | yes | none | as above | Looks good, no issues |
| Bilingual Continuation | yes | none | as above | Looks good, no issues |

The update-fields prompt is Word's standard prompt for templates holding PAGE and NUMPAGES fields; it was declined so nothing was altered. The Arabic First Page footer was viewed natively: the three lines (both D8 markings plus the restriction line) fit inside the page below the rule with no collision. Arabic text, RTL and the logo are unchanged (byte-identical parts).

## Not done
Native PowerPoint checker counts for Parts A, C and D; Windows; PDF/Acrobat; screen readers (no new VoiceOver pass was run, because no structure changed).
""")

w("11_RP01_Release_Consistency_Audit.md", "# 11 · RP01 %s Release Consistency Audit\n\n" % EM + HEAD + """## Successor consistency suite
`15_scripts/rp01_consistency.py` is a copy of the ODI01 / AFC02 checker with three explicit expectation changes (stated in its header): the "V3.0 RC2 present" check is replaced by "running header carries no RC2 label" plus "V3.0 present"; the document-ID check expects the promoted IDs (no -RC2); the PDF export checks are removed because no PDF is promoted. Result on the promoted Parts A, B and C: **112 PASS, 0 FAIL** (`16_qa/rp01_consistency.md`). The baseline run of the original checker on the unedited HR01 candidates was also 112 PASS, 0 FAIL. This counts text and metadata assertions only; it is not a statement of full system consistency.

## Stale-label audit
The build refuses any remaining release-state label that is not classified. Final counts are in `04_RP01_Status_Label_Change_Register.csv`: stale labels updated (A), still-valid qualifiers preserved (B), historical or explanatory text preserved (C), restricted-artifact warnings preserved (D).

Preserved on purpose:
- PENDING VALIDATION, PENDING LOCALIZATION APPROVAL, PENDING PRODUCTION VALIDATION, PENDING PRODUCTION MASTER: the underlying work is not performed.
- Part C's own production-standard edition state (WORKING EDITION / PENDING PRODUCTION VALIDATION, slide 76 rule): the production gates are open or deferred. The cover and document control also state that the baseline is owner authorized.
- Change-log and supersedes text naming RC2 (history).
- The D8 markings on the four Arabic and bilingual templates.
- Part D CONCEPT / NOT PRODUCTION ARTWORK.

No unrestricted promoted artifact carries RC2 as its release state, "NOT RELEASED", "AC20 PENDING", "UNAPPROVED" or "HR01 CANDIDATE" (file names, titles, headers, document IDs, notes, metadata and shape names were scanned).

## Claim hygiene
No promoted text claims legal clearance, WCAG certification, full validation, production readiness or production-master acceptance (QA checks this in 16_qa).
""")

w("13_RP01_Residual_Limitations.md", "# 13 · RP01 %s Residual Limitations\n\n" % EM + HEAD + """FA01 limitations 1 to 13 all still apply unchanged (see `GEM_V3.0_FA01_Final_Release_Authorization/11_FA01_Residual_Limitations.md`). Additional limitations created or confirmed by promotion:

| # | Limitation |
|---|---|
| 1 | Promotion changed labels only. No gate is closed; Legal/IP stays owner accepted under formal deferral, not verified; no WCAG certification; no production-master acceptance. |
| 2 | No PDF was produced: FA01 authorizes none. PPTX and DOCX are authoritative. Arabic and bilingual DOCX/PDF stay restricted (D8). |
| 3 | The native PowerPoint Accessibility Assistant was run on Part B only (source and promoted identical: no rule violations, reading-order advisory 35). For Parts A, C and D the position rests on unchanged static predicates and the structural identity proof. |
| 4 | Visual regression is a LibreOffice raster comparison plus native opens; native pixel comparison was not performed. |
| 5 | Part C keeps its production-standard edition state WORKING EDITION / PENDING PRODUCTION VALIDATION (its own slide 76 rule); promoting the baseline does not make it an approved production standard. |
| 6 | Document IDs changed from GEM-BG/DDS/PS-V3.0-RC2 to GEM-BG/DDS/PS-V3.0 (decks and token meta), recorded in each document-control slide and in the lineage proof; the RC2 IDs remain in history text. |
| 7 | Part D's internal version label changed from v1.0 to V3.0 and its cover date to 09 October 2026; Part D shape names that equalled the old footer text were renamed with it. |
| 8 | Token package: meta fields (version, edition, documentId, issued, status) and the CSS header comment were changed and the files renamed gem-tokens.v3.0.json/.css; all token values are unchanged (deep-equality proof in the build result). Part B slide 30 now cites the new file names. The `derivedFrom` provenance text still names the RC2 deck. |
| 9 | English letterhead footers no longer print WORKING APPLICATION / PENDING VALIDATION (removed in the promotion pass); Windows Word and Word Online testing of these templates remains deferred and is not stated on the printed letter. Arabic and bilingual templates keep the marker. |
| 10 | File names follow X12 with STREAM = BRAND (owner decision D3B); the ASSET and VARIANT values are not yet an owner-confirmed taxonomy. The logo kit and token files keep their governing names. |
| 11 | The new release-state wording on the status slides (all four decks and the letterhead footers) was written in this session from the FA01 wording under the RP01 instruction. It had no Brand Owner or independent review before it was committed; the Brand Owner may correct any wording by instruction. |
| 12 | The old RC2 release decks and PDFs, and all earlier candidates, are historical and unchanged (see 12). |
| 13 | Publication to GitHub is version control only; RP01 creates no tag, GitHub Release or pull request. |
""")

w("14_RP01_Evidence_Index.md", "# 14 · RP01 %s Evidence Index\n\n" % EM + HEAD + """| Reference | Use |
|---|---|
| `GEM_V3.0_FA01_Final_Release_Authorization/MANIFEST.json` (`baseline_files_outside_package`) | Authorized baseline hashes (15 files, all matched) |
| `GEM_V3.0_FA01_Final_Release_Authorization/10_FA01_Release_Scope_Matrix.csv`, `07`, `11` | Release scope, D8 policy, residual limitations |
| `GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/18_candidate_corrections/` | Source of the four decks and four Arabic/bilingual templates |
| `GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/` | Source of the four English templates |
| `PartB_RC2/05_release/tokens/` | Source of the token package |
| `GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt` | Logo kit checksum list (verified: all files match) |
| `GEM_V3.0_RC2_D3_Owner_Decision_Package/09_D3_Owner_Decision_Record.md` | X12 STREAM = BRAND decision |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/17_scripts/consistency_check_odi01.py` | Original consistency checker (unchanged) |
| `GEM_V3.0_RC2_AX01_.../19_scripts/ax01_common.py` | AX01 walker, imported read-only |
| RP01 `02`, `03`, `04`, `08`, `16_qa/` | Baseline, promotion, label, lineage and QA evidence |
""")

# ---------------------------------------------------------------- superseded artifact map
D = "HISTORICAL ONLY"
smap = [
    ["GEM_V3_RC2/04_release/GEM Brand Guidelines V3.0 — Part A — RC2.pptx", "HISTORICAL PRE-HR01 (RC2 release deck)", "17_release_artifacts/01_brand_guidelines/" + Path(P["P-A"]["Promoted path (in RP01)"]).name, "Lacks AR01, AX01 and HR01 corrections; RC2 labels", "NO", "YES", "NO"],
    ["GEM_V3_RC2/04_release/GEM Brand Guidelines V3.0 — Part A — RC2 (review export).pdf", "HISTORICAL PRE-HR01 review PDF", "none (no PDF authorized by FA01)", "RC2 review export", "NO", "YES", "NO"],
    ["GEM_V3_RC2/04_release/GEM Production Standards V3.0 — Part C — RC2.pptx", "HISTORICAL PRE-HR01 (RC2 release deck)", "17_release_artifacts/03_production_standards/" + Path(P["P-C"]["Promoted path (in RP01)"]).name, "Lacks AR01, AX01 and HR01 corrections", "NO", "YES", "NO"],
    ["GEM_V3_RC2/04_release/GEM Production Standards V3.0 — Part C — RC2 (review export).pdf", "HISTORICAL PRE-HR01 review PDF", "none", "RC2 review export", "NO", "YES", "NO"],
    ["PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pptx", "HISTORICAL PRE-HR01 (RC2 release deck)", "17_release_artifacts/02_digital_design_system/" + Path(P["P-B"]["Promoted path (in RP01)"]).name, "Lacks NP01-R1 slide 30 fix and AR01/AX01/HR01 corrections", "NO", "YES", "NO"],
    ["PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pdf", "HISTORICAL PRE-HR01 PDF", "none", "RC2 PDF", "NO", "YES", "NO"],
    ["PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.json and .css and README.md", "SUPERSEDED token package labels", "17_release_artifacts/07_tokens/gem-tokens.v3.0.json, .css, README.md", "RC2 meta and file names; values identical", "Values identical; labels historical", "YES (files kept in place)", "NO"],
    ["Amenities_Portfolio_PartD_RC2/04_release/ (PPTX, PDF) and 00_originals/", "HISTORICAL PRE-HR01", "17_release_artifacts/04_amenities_concept/" + Path(P["P-D"]["Promoted path (in RP01)"]).name, "Lacks AR01/AX01/HR01 corrections; v1.0 working edition", "NO", "YES", "NO"],
    ["GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/18_candidate_corrections/ (4 PPTX, 4 DOCX)", "HR01 CANDIDATES (the FA01 baseline sources)", "17_release_artifacts/ (promoted copies)", "Promoted by RP01; source files untouched", "As lineage source only", "YES (kept; hash-pinned)", "NO"],
    ["GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/ (8 DOCX)", "Revision 03 WORKING APPLICATION templates", "17_release_artifacts/05_letterheads/ (English four promoted; Arabic/bilingual four from HR01 candidates)", "Working-application markers; the four Arabic/bilingual Rev03 files lack HR01 corrections", "English: lineage source only. Arabic/bilingual: NO", "YES", "NO"],
    ["GEM_Letterhead_Set_v1.1_Application_Revision_03/02_pdf/ and 05_release/ (PDF, DOCX)", "Revision 03 working PDFs and release-folder copies", "none (no PDF authorized)", "Working-application PDFs; Arabic/bilingual PDFs are D8-affected", "Internal review only under D8 marking", "YES", "NO"],
    ["GEM_V3.0_RC2_AX01.../21_candidate_corrections/, AR01 .../19_candidate_corrections/, D3 .../12_Candidate_Files/deck_candidates/, NP01-R1 .../candidate_documents/, ODI01-R1 .../19_candidate_documents/deck_candidates/", "Earlier candidate generations", "17_release_artifacts/", "Superseded by HR01 candidates and then by RP01", "NO", "YES", "NO"],
    ["README.md previous release pointers (04_release, 05_release, Part D 04_release table rows)", "Previous release pointers", "README.md section Current release (RP01)", "Pointed to RC2 pre-HR01 decks", "n/a", "n/a", "n/a"],
]
wcsv("12_RP01_Superseded_Artifact_Map.csv", ["Old artifact", "Status", "Superseded by", "Reason", "May still be used?", "Historical only?", "External issue allowed?"], smap)

# ---------------------------------------------------------------- kit pointer and release index
kit = subprocess.run(["shasum", "-a", "256", "-c", "04_official_kit/SHA256SUMS.txt"], cwd="GEM_Brand_Assets_v1.0", capture_output=True, text=True)
ok_n = sum(1 for l in kit.stdout.splitlines() if l.endswith(": OK"))
bad_n = sum(1 for l in kit.stdout.splitlines() if not l.endswith(": OK") and l.strip())
(OUT / "06_brand_assets" / "README.md").write_text("""# 06 · Logo kit (carried in place)

**GEM_Brand_Assets_v1.0 is referenced, not copied.** Copying it would create a second set of binaries and break its own checksum paths.

- Location: `GEM_Brand_Assets_v1.0/` (supplied vector kit, used unchanged).
- Checksum list: `GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt` (sha256 %s).
- Verification run for RP01 (`shasum -a 256 -c`, from `GEM_Brand_Assets_v1.0/`): **%d files OK, %d not OK**.
- Status: **WORKING ASSETS. Acceptance as production master is PENDING** (VAL-02, AC07 deferred; VAL-03, VAL-04, Y01, Y02 owner accepted under formal deferral, not verified). The production vectors are not accepted production masters, and the no-spark micro mark is pending.
- Kit file names do not follow X12; renaming is a manifest-time action (VAL-16) and is not done here.
""" % (sha("GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt"), ok_n, bad_n), encoding="utf-8")
assert bad_n == 0, "logo kit checksum failure"

(OUT / "08_release_index" / "RELEASE_INDEX.md").write_text("""# GEM™ V3.0 — release index

**%s**

This index lists the promoted GEM™ V3.0 artifacts (RP01, 2026-10-09). It is a human-readable guide, **not** the VAL-16 release manifest. Authority: `GEM_V3.0_FA01_Final_Release_Authorization/` (AC20 authorized with formal deferrals and release-scope exclusions). No gate is closed by promotion; Legal/IP is owner accepted under formal deferral, not verified; no WCAG certification; Windows and PDF validation deferred.

| Artifact | Path | Status |
|---|---|---|
| Part A Brand Guidelines | `01_brand_guidelines/` | Authorized release artifact (full PPTX); no PDF/DOCX extract of Arabic slides 37, 38, 39, 65, 66, 68 |
| Part B Digital Design System | `02_digital_design_system/` | Authorized release artifact (full PPTX); no extract of Arabic slide 9; specification only |
| Part C Production Standards | `03_production_standards/` | Authorized release artifact (full PPTX); production-standard state PENDING PRODUCTION VALIDATION |
| Part D Amenities & Packaging | `04_amenities_concept/` | **CONCEPT / NOT PRODUCTION ARTWORK**; concept portfolio only |
| English, Executive, Minimal letterheads | `05_letterheads/` | Authorized release artifacts (DOCX templates) |
| Arabic and bilingual letterheads | `05_letterheads/restricted_internal_only/` | **Controlled internal use only; external issue restricted pending D8 validation** |
| Logo kit | `06_brand_assets/README.md` → `GEM_Brand_Assets_v1.0/` | WORKING ASSETS; production-master acceptance PENDING |
| Tokens | `07_tokens/` | Token values documentation; no component implementation authorized |

No PDF is part of this release. Historical RC2 and candidate files are superseded (see `../../12_RP01_Superseded_Artifact_Map.csv`).
""" % BASE, encoding="utf-8")
irows2 = []
for r in promo:
    if r["Artifact ID"].startswith("K-"):
        continue
    irows2.append([r["Promoted path (in RP01)"].replace("17_release_artifacts/", ""), r["Artifact"], r["Category"], r["Promoted SHA256"], Path(RP / r["Promoted path (in RP01)"]).stat().st_size])
for extra, desc, cat in (("07_tokens/README.md", "Token package README", "A (documentation)"), ("06_brand_assets/README.md", "Logo kit pointer and checksum verification", "D (pointer)"), ("08_release_index/RELEASE_INDEX.md", "Release index", "index")):
    irows2.append([extra, desc, cat, sha(OUT / extra), (OUT / extra).stat().st_size])
wcsv("07_RP01_Release_File_Index.csv", ["Path (under 17_release_artifacts)", "Artifact", "Category", "SHA256", "Bytes"], irows2)

# ---------------------------------------------------------------- executive summary
cnt = Counter(r["Classification"][:1] for r in labels)
w("01_RP01_Executive_Summary.md", "# 01 · RP01 %s Release Artifact Promotion\n\n" % EM + HEAD + """## What RP01 did
Promoted the FA01-authorized baseline into the controlled release set under `17_release_artifacts/`. Every source file was hash-checked against FA01 first (**15 of 15 matched**); old RC2 release decks and PDFs were not used. Edits were anchored, count-checked run-level text edits (release-state labels, version labels, document IDs, release date, status text superseded by FA01, metadata) with every other part of each file byte-identical.

| Stream | Result |
|---|---|
| Parts A, B, C | Promoted; full PPTX release artifacts; Part C keeps PENDING PRODUCTION VALIDATION |
| Part D | Promoted as a V3.0 **concept** portfolio; CONCEPT / NOT PRODUCTION ARTWORK kept on every slide |
| English, Executive, Minimal letterheads | Promoted; footer working-application marker removed |
| Arabic and bilingual letterheads | Promoted into `restricted_internal_only/`; D8 markings verbatim plus a restriction line; external issue **NO** |
| Tokens | Meta and header labels promoted; token values unchanged (deep-equality proof) |
| Logo kit and production vectors | Carried in place; WORKING ASSETS; checksum list verified; not production masters |
| PDFs | **None generated**: FA01 authorizes no PDF |

## Evidence
Preservation proof 70/70 (structure, geometry, alt text, decorative flags, titles, RTL and language attributes, Arabic runs, Word fields byte-identical); consistency suite 112/112; 225 pages and slides compared visually (%d identical, %d expected label change, 0 sub-pixel, 0 visible regression); all 12 promoted Office files opened natively on macOS with no repair prompt; Word Accessibility Assistant reported no issues on all 8 templates. Label register: %s.

## Not changed or claimed
No gate closed; no Legal/IP verification; no WCAG certification; no production-master acceptance; no Windows, PDF or screen-reader result; no tag, GitHub Release, pull request, merge or visibility change.
""" % (vc["PIXEL IDENTICAL"], vc["EXPECTED RELEASE-LABEL CHANGE ONLY"], ", ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items()))))
print("docs written; label classes", dict(cnt), "visual", dict(vc))
