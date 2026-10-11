# 15 · Change Log (ODI01-R1)

No authoritative original was modified. ODI01 (external, delivered packages) was not overwritten. Every change below is in a new file inside this folder; the only repository change is this folder and its single local commit.

## Changes relative to ODI01
| # | File / group | R1 change | Decision |
|---|---|---|---|
| 1 | `17_scripts/validation_id_checker.py`, `run_validation_id_tests.py`, `cross_document_qa.py` item 15 | Structured VAL-ID classifier replaces the ID-set test. Explanatory mentions of the unallocated ID are allowed; active use fails. | defect 1 |
| 2 | `18_qa_evidence/validation_id_checker_tests.json` (+ results) | 15 positive, 15 negative cases; 30/30 pass. | defect 1 |
| 3 | `cross_document_qa.py` items 8, 19, 20 and paths | Item 8 now audits 400-only / no faux bold; items 19–20 rebased on `HEAD` 4ea0d11 (AFC/ODI01 commits are not repository history); paths renumbered. | defects 1–2 |
| 4 | `19_candidate_documents/deck_candidates/Part A … ODI01-R1 CANDIDATE (UNAPPROVED).pptx/.pdf` | 2 bold flags cleared (slide 15); slide 35 label wording. | D5 |
| 5 | `… Part B …` | 121 bold flags cleared; slide 10 cell + added box; slide 12 two cells + added note; slide 22 cell. | D5 |
| 6 | `… Part C …` | 105 bold flags cleared; slide 15 added box. | D5 |
| 7 | `… Part D …` | None (byte-identical copy of the ODI01 candidate). | — |
| 8 | PDFs of Parts A–C | Re-exported from the R1 decks (LibreOffice 26.8.1, tagged); Part D PDF unchanged. | D5 |
| 9 | `19_candidate_documents/tokens/…ODI01-R1-candidate.json/.css` | Four 500-token descriptions and comments reworded to FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400; meta wording. No value, type, name, decision or status changed. | D5 |
| 10 | `01`–`16`, `18_qa_evidence/`, `17_scripts/` | New reports, evidence and scripts; ODI01 prose renumbered and updated. | all |

## Renumbering (ODI01 → R1)
01→01, 02→03, 03→04, 04+05+14→03, 06→06, 07→07, 08→08, 09→09, 10→10, 11→11, 12→12, 13→13, 15→14, 16→15, 17→16; new 02 (preflight), 05 (VAL-ID fix); scripts 19→17; candidates 20→19.

Not changed: Register, Parts A–D originals and their PDFs, original tokens, asset kit and file names, letterhead package, `qa/`, the audit note, primary `main`.

Per-file hashes and XML parts: `18_qa_evidence/file_diff_register.csv`. Edit proof: `17_scripts/r1_verify_edits.py` (only the intended differences exist).

## Review-closure commit (documentation only; follows `a5d9acc`)
Both commits are preserved (`a5d9acc` is not squashed or amended). Decks, PDFs, tokens and scripts other than this documentation script are byte-identical to `a5d9acc`.

| # | File | Change | Decision |
|---|---|---|---|
| 11 | `01`, `03`, `04`, `07`, `14`, `15` | Record **PART B INLINE EMPHASIS — TEMPORARY 400 TREATMENT ACCEPTED**: no workaround authorized; current implementation 400; restoration only via an accepted 500-weight file and the governed font-validation process; font and native QA gates not closed. | owner decision (review closure) |
| 12 | `12`, `16`, `18_qa_evidence/affected_slide_visual_qa.md`, `07_Font_Bold_Flag_Before_After.csv` | Wording only: the nine-slide hierarchy finding is now "accepted" instead of "flagged for owner review". No metric or result changed. | same |
| 13 | `02_Preflight.md`, `17_scripts/r1_preflight.py` | Corrected "primary checkout not modified" (see 14). | investigation |
| 14 | `18_qa_evidence/main_ref_movement_investigation.md`, `18_qa_evidence/git_evidence/` | New: read-only investigation of the local `main` movement 334744c → 4ea0d11 (01:10:05 +0300); cause not attributable from Git evidence; lineage not affected. | investigation |
| 15 | `17_scripts/r1_closure_docs.py` | New: the script that applied rows 11–13. | — |
| 15a | `18_qa_evidence/push_readiness_assessment.md` | New: branch-only push-readiness assessment (nothing pushed). | investigation |
| 16 | `MANIFEST.json`, `SHA256SUMS.txt`, `12`, `18_qa_evidence/cross_document_qa_results.*` | Regenerated; verified. | — |
