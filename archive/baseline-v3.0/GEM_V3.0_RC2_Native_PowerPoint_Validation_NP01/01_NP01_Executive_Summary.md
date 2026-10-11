# 01 · NP01 Executive Summary — Native PowerPoint Validation Pass

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D3 RESOLVED AT OWNER-DECISION LEVEL (X12 STREAM = BRAND) · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN · D8 external Arabic/bilingual PDF BLOCKED. **Not suitable for release.** NP01 is native-PowerPoint **evidence**, not approval.

## NP01-R1 update (owner disposition)
- **NP01 ORIGINAL FINDING (preserved): Part B slide 30 = P2** — native PowerPoint clips the token-excerpt box; the last line "motion · layout · locale" is not visible.
- **NP01-R1 CORRECTION:** Part B slide 30 **corrected and revalidated natively** in the controlled candidate lineage (`GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/`). **P2 OPEN COUNT (controlled candidate lineage): before = 1, after = 0.** The identical geometry remains in the authoritative RC2 release/source decks (untouched, not opened natively) pending a separately authorized promotion.
- **P3 findings are carried forward as ACCEPTED MINOR NATIVE VARIANCE / DEFERRED**; Part A slide 39 (Arabic order) and the accessibility findings are unchanged and deferred.
- **NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.** The local register (filenames and SHA-256 only; no image content) is `GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01/NP01_Local_Screenshot_Evidence_Register.csv` (58 NP01 screenshots; the 4 NP01-R1 captures have their own register in the NP01-R1 package).

- **Raw native sweep evidence (per-shape and per-table-cell TSVs and per-deck notes JSON) exists locally and was used to derive the summarized results in the CSVs and reports. It is intentionally excluded from version control pending D7 because it contains short excerpts of governed deck content.**
- **NP01 STATUS: COMPLETE FOR THE DEFINED NATIVE POWERPOINT EVIDENCE SCOPE** (evidence, not approval; not released).

## What was tested
Byte-identical copies of the four current controlled candidates, in Microsoft PowerPoint 16.113.3 (macOS) on this Mac. Lineage proven by zip-member comparison: Part A and Part C = D3 candidates (differ from ODI01-R1 only in Part A slide 75 and notes of slides 79/80, and Part C slide 44); Part B and Part D = ODI01-R1 candidates (not reissued under D3). Hashes in `02`; all four copies were re-hashed after every native session and stayed identical. Fonts in the environment were **unaccepted working builds** (`03`).

## Results in one view (NP01 ORIGINAL FINDINGS — see the NP01-R1 update above for the Part B slide 30 correction)
| | Part A (D3) | Part B (ODI01-R1) | Part C (D3) | Part D (ODI01-R1) |
|---|---|---|---|---|
| Slides | 80 | 35 | 78 | 24 |
| Opened without repair / missing-font / linked-asset warning | yes | yes | yes | yes |
| Native property sweep (every slide) | 80 | 35 | 78 | 24 |
| Bold characters natively (text shapes + table cells) | 0 | 0 | 0 | 0 |
| Native families seen | Jost, Inter, Noto Sans Arabic | Jost, Inter, Noto Sans Arabic, Courier New (1) | Jost, Inter | Jost, Inter |
| Slides also viewed visually (native window captures) | 17 | 31 | 39 | 2 |
| P0 / P1 / P2 / P3 | 0 / 0 / 0 / 6 | 0 / 0 / 1 / 2 | 0 / 0 / 0 / 5 | 0 / 0 / 0 / 0 |

- **Faux-bold / unaccepted-font dependence: none observed.** Effective bold checked per character on 2,210 slide text shapes and 1,605 table text cells: 0 (notes, masters and layouts were covered by the OOXML scan only). The installed unaccepted Bold files were not exercised. Fonts remain a standing risk (`03`). The object model reports the *requested* family and cannot detect a substituted face; no missing-font banner appeared and viewed slides were visually consistent.
- **D5 coverage (Task 6):** all 63 slides in ODI01-R1's bold-flag inventory (Part A 1, Part B 29, Part C 33), including all 21 'REQUIRES VISUAL REVIEW' runs (Part B 3, 11, 13, 18, 19, 21, 24, 30, 33), plus Part A slide 35 (label wording), were viewed natively: 63 of 63. The other 128 slides rely on the property sweep (and, where flagged by the extent metric, were also viewed).
- **Priority items (`05`, `07`):** Part A 75 shows `GEM_BRAND_…` (STREAM = BRAND); Part A 79/80 notes carry the C1 wording on the correct slides in the Notes pane (no inversion); Part C 44 shows the working-letterhead status; Part C 15 and Part A 34/35 carry the 400-only/500-pending wording; Part B's 13 slides inspected, bold not restored; Part D retains "CONCEPT / NOT PRODUCTION ARTWORK".
- **One P2 native defect (NP01 original finding; corrected in NP01-R1, candidate lineage only):** Part B slide 30, the token-excerpt box clips its last line (`10`). The same box geometry, text and Courier New typeface exist in the RC2 **release** deck and the source deck, so it predates ODI01/D5 and is not limited to the candidate (the release deck itself was not opened natively). Not fixed in NP01; corrected in NP01-R1 in the controlled candidate lineage.
- **Arabic (`08`):** native shaping and fallback behaved; one mixed Arabic/Latin line (Part A 39) resolves LTR. Observation only; VAL-07/08/15 stay open.
- **Accessibility (`09`):** Part A: the 20 'needs title' queue slides CONFIRMED natively; 7 other queue slides (5 reading-order, 2 uncertain) are also untitled natively; new advisories (58 reading-order, 313 alt-text, 1 table header); Part B/C/D not completed.
- **Environment issue (not a candidate defect):** macOS/PowerPoint sandbox file-access prompts blocked A, C and D from the repo and scratch folders; worked around by staging copies inside PowerPoint's container (`10` E1). Scripted PNG export attempts produced no files.

## What NP01 does NOT show
- It does not approve any design, wording, font, mapping, or the Letterhead Set; it closes none of VAL-05/07/08/15/16/19, Y03, D7, AC20, or Remaining Gate #11 (native PowerPoint/Word/Acrobat/AT QA — PowerPoint only, one machine, partial visual coverage: 89 of 217 slides viewed, the rest by property sweep).
- It does not validate fonts: every result used unaccepted working builds; no 500 weight exists.
- Part B/C/D accessibility was not completed; PDF/Word/Acrobat were not tested; 128 slides were not viewed (property sweep only).

## Integrity
Authoritative originals, candidate inputs and all 20 source PPTX files: hash-identical before and after (`11`). No deck was saved: every test copy was closed with saving off, and no PowerPoint-written file exists. Two scripted `save … as PNG` export attempts were made; neither produced any file. No commit, push, merge, PR, tag, release or visibility change was made.
