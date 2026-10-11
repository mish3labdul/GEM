# 05 · NP01 Priority Slide Findings

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**. "PASS" below means *native-integrity pass in PowerPoint 16.113.3 on this Mac*: the content opened, rendered and read as intended. It is **not** design approval, brand approval, release approval, or closure of any evidence gate. All views were taken on fresh, unmodified test copies (`saved=true`) except where noted.

## A · Part A slides 79–80 (notes synchronization C1)
**PASS.** Native Notes pane shows the C1 wording on the correct slide for both (details in `07`). No 79/80 inversion in the user-visible UI. Slide 79 also carries a **P3** pre-existing layout issue: a hairline rule runs through the first line of the change-log text; legible; slide XML identical to ODI01-R1.

## B · Part A slide 75 (X12 STREAM after D3B)
**PASS.** Native render: `Example: GEM_BRAND_Horizontal_Black_v3.0_20261006.svg · convention X12 of the V3 Approval Register`. **STREAM = BRAND.** The generic pattern line `GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext` is unchanged. No overflow, wrapping change, clipping or footer collision; no ambiguity introduced by the example. (The sweep's "text extent exceeds box" flag on this slide belongs to the third text column, which visibly fits above the footer.) This does not resolve the ASSET/VARIANT taxonomy (D3 Remaining Gates item 4) and does not approve the BRAND mapping for use.

## C · Part A slides 34–35 (400-only / 500-pending wording)
- **34:** body reads "Display and headings: 400. Controlled labels and emphasis: 500 WEIGHT PENDING ACCEPTED FONT FILE (use 400)…". Correct. **P3:** the body box overruns by ~12 pt; the last line clears the footer.
- **35:** label reads "EMPHASIS · INTER 400 · 500 PENDING" on one line; "Every detail, in its place" renders regular weight, not bold. Correct. **P3:** the kicker "TYPOGRAPHY · INTER · BODY AND INTERFACE" wraps to two lines and sits directly above the "Aa" specimen.

## D · Part B slides 3, 9, 10, 11, 12, 13, 18, 19, 21, 22, 24, 30, 33 (temporary 400-weight hierarchy)
Bold was **not** restored. All 13 inspected natively.
- **3, 19:** run-in lead-ins ("Character.", "Principles.", "Tagline.", "Not allowed.", "Voice (G01–G10).") render at regular weight, so the bold hierarchy cue is gone. **OBSERVATION — the accepted D5 consequence**, not a defect, and not a release blocker on its own.
- **9, 10, 11, 13, 18, 21, 22, 24, 33:** PASS. Slide 10's table is entirely regular weight and shows "CURRENT IMPLEMENTATION: 400 for every row. 500: PENDING ACCEPTED FONT FILE."; slide 22 reads "Navigates; underlined, 400, ink"; slide 11's tracking specimens render with the stated spacing.
- **12:** Wt column shows 400 and the future-intent note is present. **P3:** the right-hand table's last row grows to three lines and the paragraph below starts with no clearance (no glyph overlap).
- **30: REAL CANDIDATE DEFECT, P2.** The token-excerpt box (Courier New 12 pt, 9 logical lines that wrap to 10, box 166 pt tall) is shorter than its text. Natively the last line "motion · layout · locale" falls outside the dark box and is not visible, and the line above is partly clipped. The candidate's own LibreOffice PDF shows every line, so this is a native-only visible defect. The same box geometry (4826000 × 2112963 EMU), text and Courier New typeface are present in `PartB_RC2/05_release/…Part B — RC2.pptx` and `PartB_RC2/01_source/B-RC2.pptx`, so the issue predates ODI01/D5 and is in the issued RC2 deck as well (that deck was not opened natively). Not fixed in NP01 (no governed content was changed); needs a controlled change. **Update: corrected in NP01-R1 (candidate lineage only) and revalidated natively — see `GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/`. The original P2 finding is preserved here.**
- Additional Part B slides viewed: **4** (P3, table grows and headings abut it), **35** (PASS).

## E · Part C slide 15 (400 / 500 pending)
**PASS.** "400 · 500 PENDING" cells and "CURRENT IMPLEMENTED WEIGHT = 400 (Jost, Inter). 500 is PENDING ACCEPTED FONT FILE and is not available to any current build. Noto Sans Arabic weights remain [PENDING]." render correctly; table header regular weight.

## F · Part C slide 44 (letterhead status C2)
**PASS.** Renders: "Layout follows Part A. Print process and stock follow the print and materials standards. Templates are an OPEN DELIVERABLE (AB10, AB11, W01–W10): a Letterhead Set (Application Revision 03) exists as a WORKING APPLICATION / PENDING VALIDATION; no template is accepted." Table rows still read [PENDING] / [PENDING PRODUCTION MASTER]. The text wraps one line past its one-line box, with clear space below (**P3**-level metric only). This confirms the statement displays; it does not accept the Letterhead Set.

## G · Part D
**PASS (native integrity).** Opens cleanly (24 slides, images intact, `saved=true`). Cover shows "CONCEPT / NOT PRODUCTION ARTWORK"; slide 9 shows "CONCEPT / NOT PRODUCTION ARTWORK / DISPENSING FORMAT PENDING" and "v1.0 WORKING EDITION". Fonts: Jost and Inter only; 0 bold characters; Calibri only on empty shapes. Only slides 1 and 9 were viewed; the other 22 are covered by the property sweep alone.

## D5 coverage (Task 6): slides whose bold flags were removed
ODI01-R1's inventory (`07_Font_Bold_Flag_Inventory.csv`, 228 runs) covers **63 slides**: Part A 15; Part B 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 35; Part C 4, 7, 9, 15, 21, 23, 28, 30, 32, 34, 39, 43, 44, 47, 49, 51, 52, 54, 57, 60–72 (60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72), 74 — 33 slides (the exact lists are in the inventory). **All 63 were viewed natively (63 of 63)**, as was Part A slide 35 (label wording change). All 21 'REQUIRES VISUAL REVIEW' runs sit on Part B slides 3, 11, 13, 18, 19, 21, 24, 30, 33, each viewed. Result: every table header and run-in lead-in renders at regular weight; no bold appears; no hierarchy collapse beyond the accepted D5 flattening; findings: Part B 4, 12 (P3), Part B 30 (P2), Part C 4, 62 (P3) below. Viewing used contact sheets (`12_screenshots/*_D5_coverage_sheet*.png`) captured with `screencapture` on fresh, unmodified test copies, cropped to the slide canvas.

## Other slides viewed
Part A 33, 37, 38, 39, 41, 45, 48, 61, 65, 66, 72; Part B 2, 35; Part C 2, 3, 20, 27, 62, 75, 77. **Every slide flagged by the extent metric was viewed.** Additional P3 findings: **Part C 3** (third placeholder line abuts the 'Edition states' line), **Part C 4** (table growth, paragraph abuts), **Part C 62** (right-hand table flush with the slide's right edge: table right boundary = slide width, zero right margin; all content visible; geometry is in the file and identical in the ODI01-R1 candidate), **Part C 77** (release-status box tight). Total slides viewed: 89 of 217.
