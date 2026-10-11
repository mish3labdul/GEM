# 11 · NP01 Evidence Index

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE** · D7 PENDING / DO NOT PUSH · AC20 OPEN.

## Files in this package
| File / folder | What it is |
|---|---|
| `01_NP01_Executive_Summary.md` | Result summary and limits |
| `02_NP01_Candidate_Baseline.csv` | Document, path, SHA-256, source package, status, slide count for A–D (the `Native test copy` columns record the originally staged repo copies, since removed — see `NP01_Staging_Log.csv`) |
| `03_NP01_Font_Environment.md` | Installed fonts, acceptance status, stop-condition analysis |
| `04_NP01_Native_Slide_Results.csv` | One row per slide (217): native families, bold characters, extent flag, notes present, visual evidence, classification |
| `05_NP01_Priority_Slide_Findings.md` | Priority slides A–G |
| `06_NP01_Native_Font_Validation.csv` | Font validation rows: all priority-slide text shapes, every exception, and per-deck table summaries |
| `07_NP01_Notes_Validation.md` | Notes pane test for Part A 79/80 |
| `08_NP01_Arabic_PowerPoint_Findings.md` | Arabic/RTL observations |
| `09_NP01_Accessibility_Observation.md` | Accessibility corroboration of the queue |
| `10_NP01_Open_Findings.md` | Severity-classified findings, environment issues, standing gates |
| `12_screenshots/` | **LOCAL-ONLY, not for version control (D7 pending).** PowerPoint window captures (JPEG/PNG) of inspected slides (`<Part>_slideNNN_<topic>.jpg`), plus D5/flagged coverage contact sheets (`B_D5_coverage_sheet0N.png`, `C_D5_coverage_sheet0N.png`, `C_flagged_coverage_sheet0N.png`, `B_slide002_flagged_coverage.png`) |
| `14_raw_native_sweeps/` | **Committed:** `np01_xml_prescan.json` (structure counts), `np01_sweep_summary.json` (aggregate counts), `source_pptx_hashes_BEFORE_powerpoint.txt` (hashes of all 20 source PPTX files). **Local-only, not committed (D7 pending):** the raw sweep `Part_*_shapes_notes.tsv`, `Part_*_tables.tsv` and `Part_*_notes.json` files, which hold short deck-text excerpts. |
| `NP01_Local_Screenshot_Evidence_Register.csv` | Provenance bridge to the local-only screenshots: filename, document, slide, purpose, SHA-256, Local-only = YES, D7 restriction = PENDING |
| `NP01_Staging_Log.csv` | Hash records for every staged test copy (repo-staged copies, container copies, post-test re-verification) |
| `scripts/` | `np01_xml_scan.py`, `np01_native_sweep_slide.applescript`, `np01_native_table_sweep_slide.applescript`, `np01_run_sweep.sh`, `np01_run_table_sweep.sh`, `np01_analyze.py`, `np01_coverage_sheets.py`, `np01_open1.sh`, `np01_goto.sh` (read-only helpers; none saves or edits; they open or navigate a deck in PowerPoint) |
| `13_native_test_copies/` | **Intentionally absent.** No test deck is retained; no PowerPoint-saved copy exists. The task's `native_test_copies/` and the report layout's `13_native_test_copies/` names were reconciled by keeping no copies. |

## Current controlled candidate lineage (after NP01-R1)
Part A = D3 candidate · **Part B = NP01-R1 candidate (`44145a44…`), superseding ODI01-R1 for Part B only** (see `GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/`) · Part C = D3 candidate · Part D = ODI01-R1 candidate. `02_NP01_Candidate_Baseline.csv` records the baseline that NP01 tested (Part B = ODI01-R1 `22802377…`) and is not rewritten.

## Native test copies (all disposable, all deleted)
Staged in `~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_NP01_NATIVE_TEST/` (outside the repository), hash-verified identical to the baseline before opening and again after all sessions, then deleted. Earlier repo-folder and scratch staging copies were deleted too (`NP01_Staging_Log.csv`). Marked: NATIVE TEST COPY — NOT AUTHORITY. Every deck was closed with saving off.

## Integrity checks
- Pre-PowerPoint hashes of all 20 source PPTX files in the worktree: `14_raw_native_sweeps/source_pptx_hashes_BEFORE_powerpoint.txt`; re-checked after testing: identical (see final QA below).
- `git` HEAD `ed81b56`, branch `claude/gem-worktree-safety-30b559`; the only change is this untracked NP01 folder.
- `MANIFEST.json` and `SHA256SUMS.txt` (exclude `.DS_Store` and `12_screenshots/`; `SHA256SUMS.txt` does not hash itself or `MANIFEST.json` self-referentially — it covers `MANIFEST.json`).

## Local-only evidence
Raw native sweep evidence (per-shape and per-table-cell TSVs and per-deck notes JSON) exists locally and was used to derive the summarized results in the CSVs and reports. It is intentionally excluded from version control pending D7 because it contains short excerpts of governed deck content. The summarized results are in `04`, `06`, `05`, `07`, `08`, `09` and `10`.

## Method notes and limits
- Native property sweep: PowerPoint AppleScript, shape → text range → font; range `bold=true` resolved per character; tables swept via `table object` cells. Reads mark decks modified in memory; decks were closed unsaved and reopened fresh for visual work.
- Visual work: window screenshots at 118–125 % zoom; JPEGs are scaled. Coverage sheets were captured with `screencapture -l <windowID>` and cropped to the slide canvas. PowerPoint's scripted PNG export produced nothing.
- **NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.** The 58 NP01 screenshots in `12_screenshots/` are listed with SHA-256, document, slide and purpose in `GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/NP01_Local_Screenshot_Evidence_Register.csv` (Local-only = YES; D7 restriction = PENDING; metadata only, no image content). The 4 NP01-R1 native before/after captures are registered in the NP01-R1 package. `MANIFEST.json` and `SHA256SUMS.txt` here deliberately **exclude** `12_screenshots/` and the raw sweep files, so `shasum -c` works on a clone that lacks them. Do not stage them; do not add them to Git history; do not include them in a future remote branch unless D7 separately authorizes that exposure. They are covered by exact-path entries in the local `.git/info/exclude`.
