# 08 · NP01 / NP01-R1 — Local Commit Disposition (OWNER-APPROVED)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7: LEGAL/IP DECISION PENDING — **DO NOT PUSH** · AC20: OPEN · D8: external Arabic/bilingual PDF validation OPEN. Two **local** commits only. No push, merge, PR, tag, release or visibility change.

NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.

## Owner decisions applied
1. **Raw sweep files are NOT committed** (`14_raw_native_sweeps/Part_*` in NP01; the two slide-30 TSVs in NP01-R1). They hold short excerpts of governed deck content; they stay local-only pending D7. The summarized CSVs and reports derived from them are committed.
2. **None of the 62 screenshots/contact sheets is committed** (58 NP01 + 4 NP01-R1); they stay local, not deleted.
3. **Screenshot registers are committed** (metadata only: filename, document, slide, purpose, SHA-256, Local-only = YES, D7 restriction = PENDING; no images, thumbnails or deck-text excerpts). NP01 owns the 58-row register; NP01-R1 owns its 4-row register.
4. **Exact-path entries were added to `.git/info/exclude`** (not `.gitignore`):
```
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/12_screenshots/
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/14_raw_native_sweeps/Part_*
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/local_only_screenshots/
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/06_native_sweep_slide30_BEFORE.tsv
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/07_native_sweep_slide30_AFTER.tsv
```
5. **Controlled-candidate status:** the Part B slide 30 fix is accepted in the controlled candidate lineage only; the authoritative Part B RC2 release and source decks and the historical ODI01-R1 baseline are unchanged and keep the original geometry defect on record.
6. **PDF:** committed as INTERNAL WORKING / PENDING VALIDATION; not externally releasable (D8).

## Commits (two, separate)
1. `qa: add NP01 native PowerPoint validation evidence` — 27 files, 0.25 MB.
2. `fix: correct Part B slide 30 native PowerPoint clipping` — 33 files, 0.79 MB.
No attribution trailer (global git rule).

## Explicit staging lists (stage by exact path only; never `git add -A` or `git add .`)
These are exactly git's untracked, non-ignored files in each package, and equal each package's `SHA256SUMS.txt` plus itself.

### Commit 1 — `GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/` (27 files)
```
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/01_NP01_Executive_Summary.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/02_NP01_Candidate_Baseline.csv
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/03_NP01_Font_Environment.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/04_NP01_Native_Slide_Results.csv
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/05_NP01_Priority_Slide_Findings.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/06_NP01_Native_Font_Validation.csv
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/07_NP01_Notes_Validation.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/08_NP01_Arabic_PowerPoint_Findings.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/09_NP01_Accessibility_Observation.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/10_NP01_Open_Findings.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/11_NP01_Evidence_Index.md
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/14_raw_native_sweeps/np01_sweep_summary.json
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/14_raw_native_sweeps/np01_xml_prescan.json
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/14_raw_native_sweeps/source_pptx_hashes_BEFORE_powerpoint.txt
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/MANIFEST.json
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/NP01_Local_Screenshot_Evidence_Register.csv
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/NP01_Staging_Log.csv
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/SHA256SUMS.txt
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_analyze.py
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_coverage_sheets.py
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_goto.sh
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_native_sweep_slide.applescript
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_native_table_sweep_slide.applescript
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_open1.sh
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_run_sweep.sh
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_run_table_sweep.sh
GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/scripts/np01_xml_scan.py
```

### Commit 2 — `GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/` (33 files)
```
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/01_NP01-R1_Summary.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/02_Authority_and_Before_State.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/03_Geometry_Change_and_Rationale.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/04_Native_Revalidation.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/05_Structural_and_PDF_QA.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/06_Carried_Forward_Findings.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/07_Local_Screenshot_Evidence_Register.csv
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/08_Commit_Proposal.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/MANIFEST.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/SHA256SUMS.txt
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/candidate_documents/GEM Digital Design System V3.0 — Part B — RC2 — NP01-R1 CANDIDATE (UNAPPROVED).pdf
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/candidate_documents/GEM Digital Design System V3.0 — Part B — RC2 — NP01-R1 CANDIDATE (UNAPPROVED).pptx
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/01_authority_slide30_before_state.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/02_inset_aware_scan_all_decks_BEFORE.csv
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/03_edit_log.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/04_structural_diff.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/05_native_test_copy_staging.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/08_native_slide30_before_after.csv
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/09_pdf_compare.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/10_tool_versions.txt
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/11_consistency_BASELINE_current_lineage.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/12_consistency_AFTER_NP01-R1.md
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/qa_evidence/13_ooxml_scan_corrected_candidate.json
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01_goto.sh
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01_open1.sh
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_apply_slide30_fix.py
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_authority_check.py
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_capture.py
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_inset_aware_scan.py
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_manifest.py
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_open.sh
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_pdf_compare.py
GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/scripts/np01r1_structural_qa.py
```

## Staging procedure (NUL-safe; explicit approved list only)
1. Parse the explicit list for the commit from this document into a NUL-separated file and prove it equals git's untracked, non-ignored files for that package.
2. Stage only from that file: `git add --pathspec-from-file=<file> --pathspec-file-nul` (never `git add -A` / `git add .`).
3. Prove the staged set equals the list: compare `git diff --cached --name-only -z` with the same file.

## Pre-commit checks (all must pass before each commit)
```bash
export GIT_PAGER=cat
git -c core.quotepath=false diff --cached --name-only | grep -Ei '\.(png|jpe?g|tsv)$'; test $? -eq 1
git -c core.quotepath=false diff --cached --name-only | grep -Ei '12_screenshots|local_only_screenshots|Part_._|06_native_sweep|07_native_sweep|\.DS_Store'; test $? -eq 1
git -c core.quotepath=false diff --cached --name-only | grep -Ev '^(GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01|GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction)/'; test $? -eq 1
git grep --cached -I -n -E 'mediacenter[1]|claude-50[1]|/private/tm[p]|mish3labdu[l]|scratchpa[d]|/User[s]/' -- GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01 GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction; test $? -eq 1   # character classes keep this line from matching itself; scoped to the two packages
(cd GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01 && shasum -a 256 -c SHA256SUMS.txt) && (cd GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction && shasum -a 256 -c SHA256SUMS.txt)
```
Additional checks for commit 2: corrected PPTX SHA-256 equals `44145a44c4529db0c0c5d9f38a6d2881e3c5fa549ba21686f1b694699a874d01` and matches `qa_evidence/04_structural_diff.json`; `pdffonts` on the exact committed PDF shows Jost-Regular, Inter-Regular, NotoSansArabic-Regular (no LinuxLibertineG); the two consistency reports show 112 PASS / 0 FAIL; the 20 source decks are unchanged.

## Call-outs for the record
- Binaries in commit 2: the corrected Part B candidate PPTX (~158 KB) and its LibreOffice PDF (~600 KB, INTERNAL WORKING / PENDING VALIDATION).
- `np01_analyze.py` embeds the hand-entered visual-inspection results (short wording quotes that also appear in the reports); it is committed because it reproduces the summarized CSVs.
- Nothing in either commit promotes the corrected Part B into an authoritative folder.
