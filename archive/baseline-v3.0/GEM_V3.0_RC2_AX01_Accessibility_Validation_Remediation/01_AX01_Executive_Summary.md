# 01 · AX01 — Accessibility Native Validation & Remediation: Executive Summary

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · VAL-07 / VAL-08 / VAL-15 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a document-accessibility validation and remediation pass. It is not a redesign, not an Arabic linguistic review, not a release pass, and it closes no gate. No screen-reader test was run.**

## Status
**AX01 — TECHNICAL ACCESSIBILITY VALIDATION AND SAFE STRUCTURAL REMEDIATION COMPLETE FOR DEFINED SCOPE.**
Open: manual screen-reader tests; unresolved title semantics (30 slides: Part A 27, Part C 3, including both covers); informative alt-text content (23 Part D images + 89 objects); manual reading-order review (200 flags); contrast governance decision; content-owner decisions. Not stated: accessibility approved, WCAG 2.2 AA compliant/certified, screen-reader validated.

## What was done
- **Baseline.** Controlled lineage: Part A = AR01 candidate (`bb75f1c1…`), Part B = AR01 candidate (`63f70622…`), Part C = D3 candidate (`3a8d2918…`), Part D = ODI01-R1 candidate (`04d325f8…`), plus the eight Revision 03 Word templates (`02`). Starting HEAD `79409f4`.
- **Native checks.** PowerPoint's Accessibility Assistant was run on all four decks, before and after (`04`), and Word's Accessibility Assistant on all eight templates (`13`). Before this pass only Part A had a completed native run. The earlier gaps for Parts B/C/D are consistent with an Assistant behaviour observed again here: Parts B, C and D completed when opened first after a PowerPoint relaunch and stalled when opened later in the same session (Part A never stalled); see `04`.
- **Calibration.** Static OOXML predicates reproduce the native counts exactly (titles 27/0/3/24, alt text 313/80/105/100, table headers 1/30/34/1), so object-level lists come from the predicates, keyed by shape id.
- **Classification before remediation** (`05`–`09`): titles, reading order, alt text, tables, contrast.
- **Remediation (Category A only, 576 edits in isolated candidate copies):** 24 Part D headings mapped to title placeholders; 486 decorative shapes marked decorative; 66 column-header tables given a header-row flag. Every edit is a zip-level anchored edit; the Part A/B/C candidates are proved by inverse transform to differ from their sources only by those flags; Part D additionally pins line spacing so the headings keep their appearance.
- **Word.** All eight templates: "Looks good! No issues found." No Word change was warranted (`12`).

## Results (native checker, count before → after)
| Deck | Missing alt text | Missing table header | Missing slide title | Check reading order (advisory) |
|---|---|---|---|---|
| Part A | 313 → 31 | 1 → 0 | 27 → 27 | 58 → 55 |
| Part B | 80 → 30 | 30 → 0 | 0 → 0 | 35 → 35 |
| Part C | 105 → 26 | 34 → 0 | 3 → 3 | 75 → 75 |
| Part D | 100 → 25 | 1 → 0 | 24 → 0 | 23 → 24 |
The counts are **not** the success metric. The remaining 31 + 30 + 26 shapes and 25 Part D items (23 product pictures + 2 shapes) are informative or unclassified and go to the content owner; the 30 untitled Part A/C slides need a title decision; reading-order advisories are generic review prompts that need a screen reader.

## Visual regression
Native PowerPoint before/after captures of 58 slides (all Arabic slides, all converted headings, table and decorative-heavy samples): 48 PIXEL-IDENTICAL, 10 SUB-PIXEL NATIVE VARIANCE (no pixel differs by more than 24 grey levels), no visible regression. LibreOffice full-deck rasters: Parts A, B, C identical on every page; Part D identical except two pages with edge-only differences that PowerPoint itself renders identically. Masks used (disclosed in `14`): PowerPoint's floating Copilot button, a transient "Welcome back" toast, and the bottom-right corner of the capture (slide numbers there are covered by the LibreOffice rasters, not by the native capture).

## Held on purpose
- **Cover headings, Part A slide 1 and Part C slide 1** — CONTENT / GOVERNANCE DECISION REQUIRED. The tested title-placeholder mapping produces an approximately 0.8 pt visible shift; it was not applied, and no compensating geometry, hidden offset or hidden title was added. The visible layout remains authoritative.
- **27 Part A and 3 Part C slides** with no unambiguous structural title — CONTENT / GOVERNANCE DECISION REQUIRED. No title was invented and no small label, peer statement or bilingual fragment was promoted. S07 governs wayfinding, not presentation semantics, and is not used to resolve bilingual slides.
- **Reading order** (200 heuristic review flags) — MANUAL / ASSISTIVE-TECH REVIEW REQUIRED: PowerPoint object order affects stacking, so nothing was reordered.
- **Alt text** — CONTENT OWNER REQUIRED for the 23 Part D product images; the 89 informative/unclassified objects stay open. No speculative or generic labels were written.
- **Contrast** — GOVERNANCE / DESIGN ACCESSIBILITY REVIEW: BEIGE #BCACA7 on WHITE #FFFFFF, about 2.19:1, Part A slide 33; it may intentionally demonstrate a prohibited combination. The governed palette is not changed and no change to it is inferred.

## Preserved
AR01: every Arabic run is still `ar-SA` with `rtl="1"` paragraphs, slide-39 split runs intact, text hashes identical (native Arabic captures identical). NP01-R1: slide-30 geometry preserved (`Text 3` cy 2565400, `Text 5` y 4546550; slide 30 differs only by decorative flags). No text, font, size, weight, tracking, colour or geometry change; no new font or colour; 112 consistency assertions 112 PASS, identical to the AR01 lineage. Originals, historical packages and the Revision 03 files are untouched.

## What AX01 does NOT show
No screen reader was run (`10`: 13 manual tests). WCAG 2.2 AA is **not** demonstrated: documents were checked structurally, 44 px targets, focus and reduced motion are N/A for static decks (not a pass), text over pictures cannot be measured statically, and the PowerPoint checker does not test every success criterion. PDFs are INTERNAL WORKING and were not regenerated; alt text propagation to tagged PDF is untested (D8, VAL-15).

## Hygiene
Committed files contain identifiers, counts and hashes only (no deck text); screenshots, raw object dumps, probes and scratch are in `local_only/` (excluded via `.git/info/exclude`) pending D7. Nothing was staged, committed or pushed.
