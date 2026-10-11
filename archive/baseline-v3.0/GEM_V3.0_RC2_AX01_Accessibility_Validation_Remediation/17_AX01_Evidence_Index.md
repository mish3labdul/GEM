# 17 · AX01 — Evidence Index

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · VAL-07 / VAL-08 / VAL-15 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a document-accessibility validation and remediation pass. It is not a redesign, not an Arabic linguistic review, not a release pass, and it closes no gate. No screen-reader test was run.**

| File | Content |
|---|---|
| `01_AX01_Executive_Summary.md` | Result, counts, held items, limits |
| `02_AX01_Candidate_Baseline.csv` | 4 decks + 8 Word templates: path, lineage, SHA-256, evidence before AX01, AX01 candidate hash |
| `03_AX01_Structural_Inventory.csv` | One row per slide (217): layout, title placeholder, object kinds, decorative/alt state, hyperlinks, media, notes, languages, Arabic content (source candidates) |
| `04_AX01_PowerPoint_Native_Checker.csv` | Native Assistant counts before/after per category with classification |
| `05_AX01_Title_Remediation_Register.csv` | 54 untitled slides: heading candidate (identifiers only), class A–E, action, result |
| `06_AX01_Reading_Order_Register.csv` | 217 slides: heuristic z-order review flags, Arabic slides MANUAL |
| `07_AX01_Alt_Text_Register.csv` | Non-text objects lacking alt text: classification, category, action |
| `08_AX01_Table_Accessibility_Register.csv` | 66 tables: header evidence, action |
| `09_AX01_Contrast_Assessment.csv` | Palette pairs, ratios, thresholds, manual rows |
| `10_AX01_Screen_Reader_Test_Matrix.csv` | 13 manual tests |
| `11_AX01_PowerPoint_Correction_Register.csv` | 576 edits with before/after/reason/authority/visible change/revalidation |
| `12_AX01_Word_Correction_Register.csv` | No Word change (8 rows) |
| `13`–`16` | Native revalidation, visual regression, gate assessment, open findings |
| `18_AX01_Local_Screenshot_Register.csv` | Local-only captures: path, document, slide, purpose, SHA-256 |
| `19_scripts/` | Inventory, classification, anchored-edit, build, verification and capture scripts |
| `20_qa/` | `ax01_edit_log.json`, `ax01_static_verification.csv`, `ax01_inverse_proof.json`, `ax01_native_pixel_compare_all.json`, `ax01_lo_raster_regression.json`, `consistency_AX01.md` (112 PASS), `ax01_native_word_checker.csv` and `ax01_word_structural_inventory.csv` |
| `21_candidate_corrections/` | The four AX01 candidate PPTX files (UNAPPROVED) |
| `local_only/` | **Local-only, not committed (D7 pending):** screenshots, raw object tables, probes, scratch variants, renders |
## Rebuild order
`ax01_inventory.py` → `ax01_titles_reading.py` → `ax01_classify_alt.py` → `ax01_classify_tables.py` → `ax01_build_candidates.py` (chains `ax01_apply_titles.py`, `ax01_apply_decorative.py`, `ax01_apply_tables.py`) → `ax01_static_verify.py` → `ax01_inverse_proof.py` → native captures (`ax01_native_capture.py`, `ax01_pixel_compare.py`) → `ax01_build_registers.py`. The consistency run used the AR01 Part B PDF and the D3 Part C file; **AX01 regenerated no PDFs.**
NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.
