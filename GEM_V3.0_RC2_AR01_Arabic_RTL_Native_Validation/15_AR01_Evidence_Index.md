# 15 · AR01 — Evidence Index

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW

| File | Content |
|---|---|
| `01_AR01_Executive_Summary.md` | Result summary, lineage, limits |
| `02_AR01_Candidate_Baseline.csv` | 12 baseline files plus the two AR01 candidates: path, lineage, SHA-256, page/slide count, Arabic/mixed present, status |
| `03_AR01_Arabic_Content_Inventory.csv` | One row per Arabic paragraph (42; reflects the baseline D3 / NP01-R1 / Revision 03 sources, i.e. BEFORE the corrections): structure, direction, language, font, size, bold, tracking, class, bidi dependencies, length, text SHA-256 (no text) |
| `04_AR01_Language_Metadata_Findings.csv` | Language/direction metadata audit per paragraph |
| `05_AR01_RTL_Bidi_Findings.csv` | Classification and severity per paragraph, before/after |
| `06_AR01_Arabic_Typography_Findings.csv` | Font, size, bold, tracking audit |
| `07_AR01_Native_PowerPoint_Findings.md` | Native results, slide 39 root cause, variant measurements |
| `08_AR01_Word_Letterhead_Findings.md` | Native Word results (four templates), static audit, observations, Arabic-first check |
| `09_AR01_Mixed_Run_Test_Matrix.csv` | Mixed-run cases from existing content; untested cases marked NOT TESTED |
| `10_AR01_Technical_Correction_Register.csv` | All applied corrections (slide 39 at stage 1; ten more under owner decision 1) |
| `AR01_PowerPoint_Metadata_Correction_Register.csv` | Per-paragraph before/after register for all 12 PowerPoint Arabic paragraphs (rtl, run language, text hash and length, font, size, tracking, bold, alignment, line spacing, geometry, slide-XML hash); no Arabic text |
| `11_AR01_Native_Arabic_Reviewer_Queue.csv` | 44 items, PENDING NATIVE ARABIC REVIEW |
| `12_AR01_Accessibility_Intersection.md` | Observations only |
| `13_AR01_Validation_Gate_Assessment.md` | VAL-07, VAL-08, VAL-15, AC10, D8, AC20: none closable (all OPEN) |
| `14_AR01_Open_Findings.md` | Severity table, governance review, not-tested list |
| `16_AR01_Local_Screenshot_Register.csv` | Local-only captures: filename, document, slide, purpose, SHA-256, Local-only = YES, D7 restriction = PENDING (metadata only) |
| `17_qa/` | `native_pass_*.csv` (A baseline, A stage-1, A final, B NP01-R1, B final), `ar01_mixed_run_native_char_order_final.csv`, `native_word_template_summary.csv`, `native_word_paragraphs.csv`, `native_word_continuation_test.csv`, `ar01_metadata_correction_table_PRE_EDIT.csv`, `ar01_edit_log_slide39.json`, `ar01_edit_log_remaining_ten.json`, `ar01_slide39_text8_run_split.json`, `screenshot_pixel_diff_final_vs_split.json`, `native_pass_A_AR01_final2.csv`, `ar01_structural_diff_slide39.json`, `ar01_structural_diff_remaining_ten.json`, `screenshot_pixel_diff_*.json`, `ar01_partA_pdf_compare*.json`, `ar01_partB_pdf_compare_final.json`, `pdfkit_logical_order_class_runs*.json`, `ar01_static_checks.json`, `consistency_*.md` (112 assertions: baseline, after stage 1, after final) |
| `18_scripts/` | Read-only audit scripts, scratch-variant builder, native PowerPoint and Word runners/probes, correction scripts (`ar01_apply_slide39_fix.py`, `ar01_apply_remaining_metadata.py`), register and summary builders |
| `19_candidate_corrections/` | **AR01 Part A candidate** (`bb75f1c1…`) and **AR01 Part B candidate** (`63f70622…`) PPTX with their INTERNAL WORKING / PENDING VALIDATION LibreOffice PDFs (not externally releasable, D8) |
| `local_only/` | **Local-only, not committed (D7 pending):** raw text-bearing inventory, scratch variants and probes, PDFs, all screenshots |

NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.

## Method notes
- Inventory: lxml paragraph-level walk of every slide, notes, layout and master part (PowerPoint) and body/header/footer parts (Word); committed outputs hold no Arabic strings.
- Native PowerPoint: sandbox-container copies, hash-verified, closed unsaved; screenshots before property reads; requested (not rendered) fonts; language read from XML.
- Native Word: byte-identical temporary copies in Word's sandbox container, opened one at a time, read-only AppleScript probes (alignment, language ID, font, size, bold, spacing, per-character horizontal position, header/footer and field counts), closed unsaved, copies deleted.
- PDFs: LibreOffice 26.8.1.1 with the three accepted Regular fonts in the profile; internal working only; PDFKit used for extraction (generic extractors are known to reorder Arabic, LH03).
- Tools: python-pptx/lxml from the docling venv; fontconfig for coverage.

## Integrity
Candidates, originals and prior packages are untouched (`git status` shows only this package as untracked). NP01 and NP01-R1 were not edited.

## Rebuild order (committed scripts)
1. `ar01_inventory.py <repo_root> <package_dir>` (writes 02, 03, 04, 06 from the baseline sources); 2. `ar01_build_findings.py <package_dir>` (05, 09, 10, 11); 3. `ar01_update_after_owner_decision.py <package_dir>` (post-correction and post-native-Word state; also fills the AR01 candidate hashes in 02 and adds the status column to 04); 4. `ar01_build_register.py <repo-relative package dir>` (16); 5. `ar01_word_summarize.py <package_dir>` (Word CSVs, reads local-only probe output); 6. `ar01_manifest.py <package_dir> <template_json>`. The CSVs were rebuilt this way and compared byte-for-byte with the committed files.
**Run split:** after `ar01_apply_remaining_metadata.py`, `ar01_split_slide39_text8.py <stage-2 pptx> <candidate pptx> A <json>` produces the final Part A candidate (variant B is scratch only); `ar01_native_slide39_probe.py` compares variants natively.
**Caution:** `ar01_apply_slide39_fix.py` writes the stage-1 Part A candidate to the same filename as the final Part A candidate; re-running it alone would overwrite the final candidate. Apply it first, then `ar01_apply_remaining_metadata.py` (which takes the stage-1 copy as input).
**Consistency check input:** the final 112-assertion run used the AR01 INTERNAL WORKING Part B PDF (LibreOffice), whereas the stage-1 run used the NP01-R1 PDF; results are identical.
