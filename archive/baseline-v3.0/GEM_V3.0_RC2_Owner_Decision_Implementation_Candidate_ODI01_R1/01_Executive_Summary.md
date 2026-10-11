# 01 · Executive Summary — ODI01-R1 Technical Reconciliation

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**

Date: 2026-10-09 · Branch: `claude/gem-worktree-safety-30b559` (isolated worktree) · Baseline: `HEAD` = `origin/main` = `4ea0d117da03850854654288afcdde98f39994d5` · Local only: not pushed, merged, published or opened as a PR.

## What "SYNCHRONIZED" means here
Governing-content, terminology, identifier and status alignment. It does **not** mean validated in every native application or production process, and it is not release readiness.

## What R1 did
R1 is a narrow technical reconciliation of ODI01. It is not a new audit, a redesign, a new owner-decision round or a release candidate. It fixed exactly two verified ODI01 defects:

| # | Defect in ODI01 | R1 result |
|---|---|---|
| 1 | The validation-ID checker mistook the explanation that one ID number is intentionally unallocated for a live reference, so cross-document QA item 15 failed (19 of 20). | Replaced the ID-set test with a structured sentence classifier (`17_scripts/validation_id_checker.py`). Explanatory mentions are allowed. Use as an owner, status, evidence, dependency, closure, release, approval, gate or pass/fail state fails, and so do unknown IDs. 30 regression cases pass. VAL-18 stays documented as unallocated; it was **not** created. **20/20 cross-document QA checks passed.** Separately: **112 automated assertions passed.** |
| 2 | D5 was incompletely implemented: 228 explicit bold flags (b="1") on brand-font runs and wording that still read as if weight 500 were usable (Part A slide 35, Part B slides 10/12/22, Part C slide 15). | Recounted independently (2 + 121 + 105 = 228, all Inter), cleared all 228 (b="1" → b="0"), corrected the five wording locations, added three clarification boxes, and separated FUTURE DESIGN INTENT = 500 from CURRENT IMPLEMENTATION = 400 in the four 500-weight tokens. **Brand-font bold flags: 228 → 0. Current faux-bold dependency: 0.** No font added, no weight synthesized, no token value or status changed. |

## Headline results
- Cross-document QA: **20/20 PASS, 0 FAIL** (`12`). 112 automated assertions: **112 PASS, 0 FAIL** (originals and candidates).
- Tokens: **153/153** names, types and values identical to the originals; **26** downward status normalizations retained; **0** promotions.
- Fonts: Jost 400, Inter 400, Noto Sans Arabic 400 present; **no 500 file exists** (stop condition not triggered). 500 = PENDING ACCEPTED FONT FILE.
- Weight-reference search: 135 hits across the candidate decks, PDFs, tokens and prose; every one classified; **0 current-implementation uses of 500 or bold**.
- Part D: unchanged from ODI01 (0 bold flags, 0 unsupported claims); "CONCEPT / NOT PRODUCTION ARTWORK" retained.
- Visual QA: 64 affected slides rendered before and after (LibreOffice, review evidence only). No layout regression. One hierarchy finding, now **accepted by the owner** as a temporary 400 treatment (see "Review closure" below; `18_qa_evidence/affected_slide_visual_qa.md`).

## Review closure (after ODI01-R1)
**PART B INLINE EMPHASIS — TEMPORARY 400 TREATMENT ACCEPTED.** Owner decision recorded after ODI01-R1 review. Part B slides 3, 11, 13, 18, 19, 21, 24, 30 and 33 read slightly weaker at 400 after the synthetic bold was removed, because bold run-in heads and emphasised passages now render at Inter 400. This is **accepted as-is** for the current 400-only implementation.
- **No visual workaround is authorized.** Not permitted as compensation: synthetic bold, underline, new colours, new font families, Jost substitution, tracking on running text, arbitrary size changes, new rules or shapes, new typographic tokens. The current Inter 400 treatment remains; the nine slides are not edited again.
- **Current implementation remains 400.**
- Intended emphasis may be restored only when an accepted corresponding 500-weight font file is introduced through the governed font-validation process.
- This is a temporary implementation limitation, not a redesign request. It does **not** close the font gates (VAL-05, VAL-19 stay open as applicable), Y03, VAL-07, or native PowerPoint / accessibility QA.

**Local `main` ref movement** (2026-10-09 01:10:05 +0300, `334744c` → `4ea0d11`) was investigated read-only: **CAUSE NOT ATTRIBUTABLE FROM AVAILABLE GIT EVIDENCE**. It does not affect the ODI01-R1 lineage (based on `origin/main` = `4ea0d11`). The primary checkout's working tree was advanced to `4ea0d11` at that second; the earlier "primary checkout untouched" wording is corrected. See `18_qa_evidence/main_ref_movement_investigation.md`. A second local commit records this closure; `a5d9acc` is preserved; the candidate decks and PDFs are byte-identical to `a5d9acc`.

## Honest limits
- **112 automated assertions passed** and **20/20 cross-document QA checks passed** are text/metadata/structure results. They are not a statement of full system consistency, and none is made.
- Renders are LibreOffice 26.8 only. **Native PowerPoint rendering, accessibility checking and reading order remain open.**
- ODI01, AFC01 and AFC02 history (`6fbd951`, `f346133`, `5dbd017`) is not in this repository; ODI01 was consumed as hash-verified delivered packages (`02`). ODI01 was not overwritten.
- PDFs for Parts A–C were re-exported with LibreOffice 26.8.1 (ODI01 used 24.2), so they differ from the ODI01 PDFs on every page at byte level; the text, fonts and layout checks above are the comparison, not byte equality.
- 25 of the 64 affected slides were inspected by eye; the other 39 are covered by automated word-geometry checks (labelled in the visual QA file).

## Gates that remain
AC20 OPEN; named role holders; trademark, logo ownership, master artwork, fonts and licences, image rights; Arabic linguistic and native QA (VAL-07, VAL-08, VAL-15 open); native PowerPoint / Windows Word / Word Online / Acrobat / assistive technology; supplier evidence; component bundle (VAL-13, VAL-20); D3 (unresolved); Legal/IP (D7). See `14`.

## Suitability
Suitable for Brand Owner review. Suitable for an explicitly authorized **branch** push only if the owner authorizes it. Suitable for PR review only after that. **Not suitable for release.** See `16`.
