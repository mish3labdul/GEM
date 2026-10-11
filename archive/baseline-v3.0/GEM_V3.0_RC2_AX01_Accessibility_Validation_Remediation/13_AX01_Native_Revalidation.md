# 13 · AX01 — Native Revalidation (PowerPoint and Word)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · VAL-07 / VAL-08 / VAL-15 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a document-accessibility validation and remediation pass. It is not a redesign, not an Arabic linguistic review, not a release pass, and it closes no gate. No screen-reader test was run.**

## Method
Fresh copies staged in the application's own sandbox container, opened one at a time, **closed without saving**, hash re-verified, deleted. No Quick Fix, "Review shapes" or other auto-fix control was pressed. For PowerPoint, Parts B, C and D were checked one deck per freshly launched session because the Assistant stalled on later documents in a session (observed behaviour; see `04`). Word: byte-identical copies of the eight Revision 03 templates; the "update fields?" prompt was declined.

## PowerPoint — before / after
See `04_AX01_PowerPoint_Native_Checker.csv` and the summary table in `01`. Calibration: the static predicates reproduce every native count (before: A 27/313/1, B 0/80/30, C 3/105/34, D 24/100/1; after: A 27/31/0, B 0/30/0, C 3/26/0, D 0/25/0). The "Check reading order" figure is a generic review prompt that also moved for unrelated reasons (Part A 58 → 55 after decorative marking; Part D 23 → 24 after titles), so it is not read as a defect count.
Manual confirmations: the 24 Part D headings are now recognised as slide titles (checker 24 → 0; no visible text added); navigation behaviour is untested (SR-01); decorative objects are flagged decorative (announcement not tested without a screen reader); informative imagery still lacks descriptions where the owner has not supplied them (Part D, 23 pictures); tables remain usable and render unchanged; Arabic/RTL structure intact (AR01 paragraphs unchanged; Arabic slides pixel-identical or sub-pixel).

## Word — native Accessibility Assistant (all eight templates)
| Template | Result |
|---|---|
| English First Page | "Looks good! No issues found." |
| English Continuation | no issues |
| Arabic First Page | no issues |
| Arabic Continuation | no issues |
| Bilingual First Page | no issues |
| Bilingual Continuation | no issues |
| Executive | no issues (window title shows Compatibility Mode) |
| Minimal | no issues (window title shows Compatibility Mode) |
Observations that "no issues" does not cover: (1) every template is `compatibilityMode=14` (Word 2010); whether Word then runs a reduced rule set was not tested; (2) both Continuation templates contain **no heading paragraphs** yet the "No headings in document" check passes, so checker-clean does not mean structurally complete; (3) every template sets `w:updateFields`, producing an "update fields?" prompt on open (not a repair dialog); (4) document title metadata is set on all eight; the logo carries alt text; no tables or floating drawings; PAGE/NUMPAGES fields resolve. Static inventory: `20_qa/ax01_word_structural_inventory.csv`; native results: `20_qa/ax01_native_word_checker.csv`.

## Not covered
Screen readers; Windows Word / Word Online; Acrobat or PDF tagging; real multi-page content with real Arabic.

## Task 8 — AR01 language/RTL intersection
No AX01 edit touched an AR01-changed paragraph: the static verification (`20_qa/ax01_static_verification.csv`) compares every paragraph's text hash, run languages, size, tracking, bold, fonts and paragraph direction between each source and its AX01 candidate (1,215 / 1,050 / 1,792 / 448 paragraphs, all identical), with one disclosed exception: the 24 Part D title-mapped heading paragraphs gained an explicit 100% `lnSpc` element (equal to their previous effective value; the only paragraph-property addition, outside what the attribute-level signature compares); including all 12 Arabic paragraphs (`ar-SA`, `rtl="1"`) and the slide-39 Arabic/Latin run split. The Arabic slides are pixel-identical or sub-pixel (Part A slides 37, 38, 39, 66 identical; 65 and 68 sub-pixel; Part B slide 9 identical). No new run segmentation was introduced. No screen-reader claim is made.
