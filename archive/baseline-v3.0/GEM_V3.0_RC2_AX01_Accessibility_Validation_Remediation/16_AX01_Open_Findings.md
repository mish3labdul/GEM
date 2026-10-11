# 16 · AX01 — Findings, Severity and Open Items

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · VAL-07 / VAL-08 / VAL-15 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a document-accessibility validation and remediation pass. It is not a redesign, not an Arabic linguistic review, not a release pass, and it closes no gate. No screen-reader test was run.**

## Severity (technical, after AX01)
| Severity | Count | Items |
|---|---|---|
| **P0** | 0 | none; every file opens natively and keeps its structure |
| **P1** | 0 | none evidenced; no screen reader was run, so none can be excluded for assistive-technology access |
| **P2** | 2 | AX01-F01: **23 informative product pictures in Part D carry no alt text** (images of product labels incl. Arabic label artwork; content owner). AX01-F02: **30 slides without a recognised title** (Part A 27, Part C 3; titles are a content/governance decision; Part A slide 1 and Part C slide 1 held because mapping shifts the heading about 0.8 pt) |
| **P3** | 4 | AX01-F03: 31 + 30 + 26 + 2 non-text shapes (Parts A–D) that are informative or unclassified and unlabelled (content owner). AX01-F04: generic alt text on 6 Part D pictures ("Supplied GEM raster artwork…") does not describe them. AX01-F05: Continuation Word templates have no heading paragraphs. AX01-F06: text over pictures (113 runs in Parts A and C) cannot be measured statically |
| MANUAL TEST REQUIRED | 13 | `10_AX01_Screen_Reader_Test_Matrix.csv` |
| CONTENT OWNER REVIEW | 3 | titles (30 slides), Part D pictures (23), unlabelled shapes (89) |
| GOVERNANCE REVIEW | 5 | below |
| OBSERVATION | 7 | below |
Corrected by AX01 (previously P2/P3): 66 tables without header flag; 24 Part D slides without a title; 486 decorative-class shapes without a decorative flag.

## GOVERNANCE REVIEW
1. **Cover headings (Part A slide 1, Part C slide 1)** — CONTENT / GOVERNANCE DECISION REQUIRED. The tested title mapping shifts the heading about 0.8 pt; not applied; no compensating geometry, hidden offset or hidden title; visible layout authoritative.
2. **Remaining 30 untitled slides and bilingual hierarchy** — CONTENT / GOVERNANCE DECISION REQUIRED. S07 governs wayfinding, not presentation semantics, so it does not resolve them. Reading order of paired bilingual slides is MANUAL / ASSISTIVE-TECH REVIEW REQUIRED; nothing was reordered.
3. **Brand-mark label convention** is not governed; no alt-text label was invented for the logo mark.
4. **Contrast (GOVERNANCE / DESIGN ACCESSIBILITY REVIEW).** All governed pairs used for text measure at or above 4.5:1 (INK/WHITE 18.01, BEIGE/INK 8.23, WHITE/BLACK 20.75, BEIGE/BLACK 9.48). One governed pair fails: **BEIGE #BCACA7 on WHITE #FFFFFF, about 2.19:1** (one 22 pt run, Part A slide 33; it appears to be a specimen of the prohibited pair rather than body text, to be confirmed with the owner). Recorded; no colour changed; the master palette is not inferred to need change and the slide may intentionally demonstrate a prohibited combination. 113 runs sit over pictures and need a manual check.
5. **Compatibility Mode 14** in all Word templates (Word 2010 behaviour); updating the compatibility level is a template decision.

## OBSERVATIONS
1. The Accessibility Assistant's behaviour was inconsistent: Part A completed every time (including late in a session); Parts B, C and D completed when opened first after a PowerPoint relaunch, and the same files (and B-only variants: table-only, decorative-only, style-id) stalled on "Updating results..." when opened later in the same session. Quitting PowerPoint dismissed two stale NP01-era file-access prompts (declined, nothing granted) but did not by itself prevent the later stalls. NP01's Parts B/C/D gaps are consistent with this behaviour.
2. "Check reading order" is a per-slide review prompt and moves with unrelated changes (58 → 55).
3. Every Word template sets `w:updateFields` (prompt on open).
4. Part D was saved by PowerPoint (its shapes carry creation ids and lock elements); Parts A–C are tool-generated; the edit forms differ accordingly.
5. 44 px targets, visible focus and reduced motion are digital-context rules and are N/A for static decks; recorded as N/A, not as pass.
6. Part A: all 12 pictures whose alt text begins "Decorative…" are flagged decorative (13 flagged in total; Part C 8 of 8). Consistent.
7. **Part D titles are title placeholders with no matching title placeholder in the layout or master.** What happens on Reset Slide or a layout change (restyle or reposition) is untested; not a defect now.
