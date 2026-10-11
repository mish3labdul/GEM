# 05 · NP01-R1 — Structural, PDF and Consistency QA

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE** · D3 RESOLVED AT OWNER-DECISION LEVEL (X12 STREAM = BRAND) · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN · D8 external Arabic/bilingual PDF BLOCKED.

## OOXML (`qa_evidence/04_structural_diff.json`)
- 158 zip members before and after; **order and ZipInfo identical; exactly one member differs: `ppt/slides/slide30.xml`**. Notes slides, masters, layouts, themes, `docProps` and all other slides are byte-identical (no normalization).
- Inside `slide30.xml` (347 tokens): **exactly two attribute values differ** (`Text 3` `a:ext@cy`, `Text 5` `a:off@y`). All 7 `<a:t>` strings, every `rPr`, `bodyPr`, colour, typeface, font size and line-spacing value are identical.
- **D5 400-only unchanged:** `b="0"` only (no `b="1"|"true"|"on"` on the slide or in any part; masters/layouts/notes/defaultTextStyle none); no embedded fonts, charts or diagrams (`13_ooxml_scan_corrected_candidate.json`).
- **D4 token values/statuses unchanged:** no token file or token table is touched; the ODI01-R1 and D3 package checksums still verify (0 non-OK lines).
- **35 slides**, as before.

## PDF (`qa_evidence/09_pdf_compare.json`; LibreOffice review evidence only, not native)
**Status: INTERNAL WORKING / PENDING VALIDATION — not an approved external artifact.**
- Export: `soffice --headless … --convert-to "pdf:impress_pdf_Export:{UseTaggedPDF=true}"`, LibreOffice 26.8.1.1; a fresh profile whose `user/fonts` holds only the three accepted **Regular** files (repo copies: `Jost-Regular.ttf` db44231d…, `Inter-Regular.ttf` 8bac02d5…, `NotoSansArabic-Regular.ttf` 35965bc1…), as in R1. Embedded: Jost-Regular, Inter-Regular, NotoSansArabic-Regular, LiberationMono (stand-in for Courier New), OpenSymbol. *A first render in a profile without those files substituted a serif for Jost/Inter; it was detected via the embedded-font INFO line and discarded.*
- 35 pages, tagged. Re-rendered "before" text equals the delivered ODI01-R1 PDF text on all 35 pages.
- **Before vs after, word bounding boxes: all 35 pages have identical text; only page 30 differs, and only the 32 words of the paragraph below the panel (+35.6 pt vertical shift).** Nothing else moved.
- **Visual confirmation of the delivered PDF's page 30** (local-only render, 70 dpi): the dark panel now encloses all ten lines with padding below the last line, the paragraph sits clear below it, the footer is far below. In the matching 'before' render the last line sat flush against the panel's bottom edge with no padding. The word-box comparison above covers text; this look covers the panel shape.
- Part B carries Arabic on slides 9 and 12: **D8 applies — this PDF is internal working use only; external issue blocked.**

## Consistency assertions (`qa_evidence/11_…`, `12_…`)
`consistency_check_odi01.py` with output redirected into this package and candidate override paths (A, C = D3 candidates; B/BPDF = ODI01-R1 baseline, then NP01-R1). **Baseline: 112 PASS / 0 FAIL / 3 INFO. After: 112 PASS / 0 FAIL / 3 INFO; the two reports are identical below the header** (37 B-specific PASS, 1 B INFO). No tracked file was written. Tools: python-pptx 1.0.2, lxml 6.0.2 (docling venv), LibreOffice 26.8.1.1.

## Repository integrity
All 20 source PPTX files identical to their pre-test hashes; tracked-file diff empty; ODI01-R1 and D3 packages untouched.
