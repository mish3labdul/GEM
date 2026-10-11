# 01 · NP01-R1 — Native Layout Correction (Part B slide 30 only)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D3 RESOLVED AT OWNER-DECISION LEVEL (X12 STREAM = BRAND) · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN · D8 external Arabic/bilingual PDF BLOCKED. **NOT RELEASED. Not suitable for release.**

## Outcome
| | |
|---|---|
| NP01 original finding | **Part B slide 30 = P2** (native PowerPoint clips the token-excerpt box; "motion · layout · locale" not visible). **Preserved unchanged in NP01.** |
| NP01-R1 correction | Slide 30 of the **controlled candidate** corrected (two numeric attributes) and **revalidated natively**: all ten lines visible, 2.7 pt slack, no collision, Inter 400, no bold, no substitution warning. |
| P2 count | Before: **1** · After: **0 — P2 OPEN COUNT (controlled candidate lineage) = 0** |
| Scope of "0" | Applies to the candidate lineage only. The identical geometry remains in `PartB_RC2/05_release` and `01_source` (authoritative, untouched, not opened natively) until a separately authorized promotion. |
| Everything else | Unchanged: 34 other Part B slides, Parts A/C/D, ODI01-R1 and D3 packages, tokens, notes, masters; P3 findings deferred; Arabic slide 39 and accessibility untouched. |

## Current controlled candidate lineage (after NP01-R1)
| Part | Current controlled candidate | SHA-256 (first 12) | Note |
|---|---|---|---|
| A | D3 candidate (`GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/…`) | eca6b80ba6f3 | unchanged |
| **B** | **NP01-R1 candidate (`GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction/candidate_documents/…`)** | **44145a44c452** | **supersedes the ODI01-R1 Part B candidate (22802377eb73) for Part B only**; the ODI01-R1 file is left in place, untouched, as history |
| C | D3 candidate | 3a8d291816d7 | unchanged |
| D | ODI01-R1 candidate | 04d325f83fc7 | unchanged |

## Controlled-candidate status (owner disposition)
The Part B slide 30 fix is **accepted in the CONTROLLED CANDIDATE lineage**. It does **not** modify or retroactively correct the authoritative Part B RC2 release deck, the authoritative source deck, or the historical ODI01-R1 baseline; those remain unchanged for audit traceability. The authoritative RC2 geometry defect remains recorded as historical/source-state evidence and is not silently overwritten.

**Finding status:** NP01 P2 BEFORE = 1 (Part B slide 30, native clipping) → NP01-R1 P2 AFTER = 0, **for the current controlled candidate lineage only**. The original P2 record and provenance are preserved in the NP01 package. P3 findings remain ACCEPTED MINOR NATIVE VARIANCE / DEFERRED. Part A slide 39 remains a LOCALIZATION / RTL OBSERVATION — DEFERRED TO ARABIC VALIDATION. Accessibility findings remain open.

**PDF status:** the regenerated Part B PDF is **INTERNAL WORKING / PENDING VALIDATION** and is not externally releasable under D8 (Part B contains Arabic; external Arabic/bilingual PDF validation remains open). An initial render with substituted fonts was discarded; the final render used the accepted Regular font inputs.

Artifacts: `candidate_documents/` (corrected PPTX and its LibreOffice PDF), `02`–`06` reports, `qa_evidence/` (textual QA), `07_Local_Screenshot_Evidence_Register.csv` (the 4 NP01-R1 captures; the 58 NP01 screenshots are registered in the NP01 package). NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION. Screenshots are listed by filename and SHA-256 only; no image content is embedded or copied into any report.

Not done and not claimed: no promotion into authoritative sources; no Arabic or accessibility change; no gate closed (Gate #11, VAL-05/07/08/15/16/19, D7, AC20); no commit, push, merge, PR, tag or release.
