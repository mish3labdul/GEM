# 14 · AX01 — Visual Regression QA

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · VAL-07 / VAL-08 / VAL-15 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a document-accessibility validation and remediation pass. It is not a redesign, not an Arabic linguistic review, not a release pass, and it closes no gate. No screen-reader test was run.**

## Native PowerPoint captures (58 slides, before vs after, local-only PNGs)
`20_qa/ax01_native_pixel_compare_all.json`. Classes: PIXEL-IDENTICAL 48; SUB-PIXEL NATIVE VARIANCE 10 (differences of at most 24 grey levels: Part A slides 1, 53, 65, 68; Part B slides 5, 7, 15; Part C slides 1, 4, 73); VISIBLE REGRESSION 0.
| Deck | Slides captured | Identical | Sub-pixel |
|---|---|---|---|
| Part A | 20 (all six Arabic slides 37, 38, 39, 65, 66, 68; 1, 3, 12, 15, 19, 26, 28, 30, 32, 48, 53, 54, 76, 80) | 16 | 4 |
| Part B | 7 (incl. Arabic slide 9 and NP01-R1 slide 30) | 4 | 3 |
| Part C | 7 | 4 | 3 |
| Part D | 24 (every converted heading) | 24 | 0 |
Part D's title mapping was pixel-identical only after pinning the heading's line spacing to 100% (the master title style specifies 90%); the unpinned mapping shifted headings in LibreOffice, which is how the inheritance was found. The cover headings of Part A slide 1 and Part C slide 1 shifted about 0.8 pt natively when mapped, so they were **not** mapped.

## Masks and limits (disclosed)
The comparison ignores (a) PowerPoint's floating Copilot button (bottom-right), (b) a transient "Welcome back" toast (top-right band), and (c) a bottom-right strip of the capture (x ≥ 2050 and y ≥ 1150 of 2410 × 1350). **Slide numbers and right-hand footer content sit in region (c)**, so the native capture does not cover them; the LibreOffice rasters do.

## LibreOffice full-deck rasters (internal working renders, 50 dpi)
Part A 80 pages, Part B 35, Part C 78: every page identical; Part D 24 pages: identical except pages 3 and 24 (edge-only differences of 600 and 705 pixels; best alignment at zero shift; PowerPoint renders both identical). Page counts and font sets unchanged. No PDFs were regenerated or committed by AX01 (INTERNAL WORKING; D8 open).

## Word
No Word file was changed; no layout comparison was needed.
