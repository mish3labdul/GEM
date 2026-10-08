# 04 · Implementation Trace Matrix (ODI01 + R1)

One entry per implemented decision (D1, D4, D5, D6, D7, D8, AC20). **D3 is not implemented** (not resolved): its carried-forward candidates are tracked in `13` and `14` and `19_candidate_documents/d3a_carried_forward/`. Same content as `03_Implementation_Trace_Matrix.csv`.

## D1
- **Owner instruction:** Confirm Register as OWNER-ADOPTED WORKING DECISION BASELINE (456 adopted / 8 Evidence Required / 2 Deferred / 12 of 12 role holders unnamed / AC20 OPEN); do not edit the 466 rows; create a dated adoption record with the exact statement.
- **Source evidence:** Register xlsx (sha256 ccce4613…7ab3), recalculated in LibreOffice: 384 / 72 / 8 / 2; Dashboard Overall "Not ready"; Owners & Governance 12 of 12 TBD; ODI01 brief D1.
- **Affected files:** NEW: 19_candidate_documents/register_adoption/GEM_V3_Final_Brand_Approval_Register_Prefilled.ADOPTION_RECORD_2026-10-08.md; 04_Register_Adoption_Record.md. Register xlsx: NOT touched.
- **Before state:** Register adopted only by indirect evidence; no dated owner record; AFC02 status "PASS (indirect) · owner confirmation pending".
- **Implementation:** Adoption record written with source hash, adoption date, decision counts, evidence status, AC20 OPEN and the verbatim statement.
- **After state:** Register is the owner-adopted working baseline (record is a candidate file until placed next to the register by an authorized change). 466 rows unchanged.
- **QA run:** Cross-doc QA #1 (Register alignment), #18, #19, #20
- **Result:** See 12 (item 1)
- **Open dependencies:** 8 evidence-required rows, 2 deferred, 76 adopted rows flagged Evidence Required?=Yes, role holders, AC19, AC20.
- **Release effect:** None. Explicitly not AC20 authorization.

## D4
- **Owner instruction:** Accept all 26 AFC02 downward token status normalizations; do not alter values, names or semantic meaning; promote nothing; re-run all 153 tokens; target 0 unexplained inflation.
- **Source evidence:** AFC02 dependency audit; Part B slide 12 (Arabic PENDING VALIDATION); Register M02/M04, L08, L09, Y03; ODI01 re-run.
- **Affected files:** NEW: 19_candidate_documents/tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.json/.css; token_verification.json; 06_Token_Status_Implementation.csv/.md. Originals in PartB_RC2/05_release/tokens/ NOT touched.
- **Before state:** 26 derived tokens carried a stronger status than their weakest dependency (10 APPROVED→CONDITIONAL, 9 APPROVED→PENDING VALIDATION, 7 CONDITIONAL→PENDING VALIDATION targets).
- **Implementation:** All 26 applied in candidate JSON and CSS comments; value/type/name/decision unchanged; 153 tokens re-verified.
- **After state:** 26 normalizations applied; 0 unexplained inflation; Value changed? = NO for 153/153.
- **QA run:** token_status_implementation.py (16 verifications); audit_tokens.py (65 PASS/0 FAIL/12 INFO); cross-doc QA #9, #10, #11
- **Result:** PASS (see 06)
- **Open dependencies:** Y03, VAL-05, VAL-07, VAL-19 open; component bundle (VAL-13/20) absent.
- **Release effect:** None. Statuses only go down.

## D5
- **Owner instruction:** Temporarily restrict to weight 400 until accepted 500 files exist. No faux bold, no application-generated 500/bold, no substitution. Classify 500 refs A/B/C. Keep family architecture. Do not close VAL-05, Y03, VAL-07.
- **Source evidence:** Font binaries in main (Regular only; sha256 verified); letterhead Original_Font_Manifest.json; PR #10 variable builds (hash-verified, not accepted); deck XML scan of 500 references.
- **Affected files:** CANDIDATES: Part A s34; Part B s9, s10; Part C s15 (deck_candidates/); tokens JSON/CSS (4 annotations); 07_Font_400_Restriction_Implementation.md; 07_Font_Claim_File_Matrix.csv; 07_Font_500_Reference_Classification.csv.
- **Before state:** Decks and tokens claimed 500 for Jost, Inter and Noto Sans Arabic; no 500 file in main.
- **Implementation:** 10 references classified: A 3 · B 5 · C 2. B wording changed to "500 WEIGHT PENDING ACCEPTED FONT FILE" (short form "500 PENDING" in table cells). Matrix has the 8 required columns.
- **After state:** 400-only restriction stated; 500 pending; architecture unchanged.
- **QA run:** font_matrix_odi01.py; build_deck_candidates.py; LibreOffice render check of 4 slides; cross-doc QA #7, #8
- **Result:** See 12 (items 7, 8)
- **Open dependencies:** VAL-05, Y03, VAL-19, VAL-07 open. 228 b="1" runs not normalized (logged).
- **Release effect:** None. Restriction is temporary and closes nothing.

## D6
- **Owner instruction:** Accept verified Part D concept/status wording corrections; remove only unsupported ambiguity; keep "CONCEPT / NOT PRODUCTION ARTWORK"; re-audit keywords with the new classes; resolve slide-23 registers reference without inventing registers.
- **Source evidence:** Part D deck text, notes, package contents (only MOCKUP_REGISTER.csv exists), Part D README, AFC02 claim audit.
- **Affected files:** CANDIDATES: Part D deck (slide 15; slide 23 notes); partd/README.ODI01-R1-CANDIDATE.md; partd/qa__…Asset_Sync_Change_Log.ODI01-R1-CANDIDATE.md; partd/qa__…Final_Release_Notes.ODI01-R1-D6-CANDIDATE.md; 08_PartD_Claim_Implementation.md; partd_claim_audit_original/candidate.csv.
- **Before state:** 1 UNSUPPORTED CLAIM (slide-23 registers); slide 15 read as if an approved dieline existed; "approved mockups" shorthand in 3 repo files.
- **Implementation:** 2 deck wording edits and 3 prose copies; no register invented or reinstated.
- **After state:** 0 UNSUPPORTED CLAIM; concept markings retained; no visual design change.
- **QA run:** partd_claim_audit.py on original and candidate; build_deck_candidates.py diff control; render check of slide 15; cross-doc QA #17
- **Result:** See 12 (item 17)
- **Open dependencies:** Y04 / VAL-06 image rights; Arabic strings; supplier/physical proof; version label "v1.0 WORKING EDITION" vs file name.
- **Release effect:** None. No production, supplier, rights or material approval implied.

## D7
- **Owner instruction:** No change to repository visibility. Record "NO CHANGE — LEGAL/IP DECISION PENDING"; carry as open Legal/IP item (Brand Owner + Legal/IP Counsel); do not recommend public or private.
- **Source evidence:** gh api repos/mish3labdul/gem → private:false (unchanged); Register Y01–Y04.
- **Affected files:** NEW: 14_Public_Repository_Legal_Status.md.
- **Before state:** Public; legal gates VAL-03/04/05/06 open.
- **Implementation:** Recorded as NO CHANGE — LEGAL/IP DECISION PENDING; carried to 15 (gate 18).
- **After state:** Unchanged.
- **QA run:** Re-check of visibility and main SHA (no setting changed)
- **Result:** See 12 (item 20) and 14
- **Open dependencies:** Written Legal/IP decision.
- **Release effect:** None.

## D8
- **Owner instruction:** Conservative Arabic/bilingual PDF rule: internal working use with markings and limitations; external issue BLOCKED until native tests pass; keep VAL-07, VAL-08, VAL-15 open; matrix with required columns and Status "INTERNAL WORKING ONLY".
- **Source evidence:** Letterhead QA report R03-03, LH03, R03-06, LH08; PDFKit_Native_Extraction.json; Rev03_Checks.json; ODI01 pdfinfo re-run.
- **Affected files:** NEW: 10_Arabic_PDF_Operating_Rule.md; 10_Arabic_PDF_Test_Matrix.csv.
- **Before state:** Open decision (AFC02 D8) with route evidence scattered across the QA report.
- **Implementation:** Rule and 8-row matrix written; untested routes marked NOT TESTED.
- **After state:** External issue blocked; internal working allowed with markings.
- **QA run:** letterhead_bilingual_hierarchy.py; pdfinfo re-run; cross-doc QA #11, #13
- **Result:** See 12 (items 11, 13)
- **Open dependencies:** Linguistic QA, Windows Word, Word Online, Acrobat, AT, accessibility QA, final localization approval.
- **Release effect:** None. No PDF route approved.

## AC20
- **Owner instruction:** AC20 remains OPEN. No APPROVED / FINAL / PRODUCTION READY / RELEASED / SYSTEM READY. Role holders stay TBD / REQUIRES OWNER. Do not close AC19.
- **Source evidence:** Register (AC20 Evidence Required; Owners & Governance 12 of 12 TBD); ODI01 brief.
- **Affected files:** NEW: 05_Governance_and_AC20_Status.md; 15_Remaining_Gates.md.
- **Before state:** AC20 OPEN
- **Implementation:** Documented prerequisites; status label applied to all deliverables.
- **After state:** AC20 OPEN
- **QA run:** cross-doc QA #14, #15, #16
- **Result:** See 12 (items 14, 15, 16)
- **Open dependencies:** All gates in 15.
- **Release effect:** None. Not release authorization.


---
## ODI01-R1 entries (added in this pass)

### R1-1 · Validation-ID checker (ODI01 defect 1)
- **Instruction:** Fix the checker so explanations are not treated as live references to the unallocated ID. The unallocated ID is VAL-18. Do not create it and do not renumber; add regression tests; re-run cross-document QA to 20/20.
- **Source evidence:** ODI01 `cross_document_qa.py` item 15 collected every `VAL-nn` found in the package documents (including its own report text) into one set and required one number to be absent.
- **Affected files:** `17_scripts/validation_id_checker.py` (new), `17_scripts/cross_document_qa.py` (item 15), `17_scripts/run_validation_id_tests.py`, `18_qa_evidence/validation_id_checker_tests.json` and `…_test_results.json`, `05_Validation_ID_QA_Fix.md`, `12`.
- **After state:** structured classification (allowed explanatory / failing active / failing unknown); 30/30 regression cases pass; item 15 PASS; 20/20.
- **Open dependencies:** none for this defect.

### R1-2 · D5 completion: 400 only, no faux bold (ODI01 defect 2)
- **Instruction:** Current implementation = weight 400 only until accepted 500-weight files exist; no faux bold; clean every active 500 reference; no token value changes.
- **Source evidence:** raw OOXML recount (228 explicit bold runs: A 2, B 121, C 105; all Inter); font binary scan (no 500 file); full-artifact weight search (135 hits, all classified).
- **Affected files:** candidate Part A, B, C decks (slide XML only) and their PDFs; token JSON/CSS descriptions; `07_*`, `18_qa_evidence/*` (inventory, before/after, visual QA, diff register, search).
- **After state:** brand-font bold flags 228 → 0; Part A s35, Part B s10/s12/s22 and Part C s15 corrected; four 500-weight tokens state FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400; values and statuses unchanged.
- **Open dependencies:** VAL-05, Y03, VAL-19, VAL-07 (accepted font files, licences); native PowerPoint check; owner decision on weakened run-in-head emphasis.
