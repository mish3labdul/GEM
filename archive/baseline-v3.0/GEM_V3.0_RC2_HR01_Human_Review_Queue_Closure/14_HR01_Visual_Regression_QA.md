# 14 · HR01 — Visual Regression QA

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**

## Method
Page-by-page raster comparison of each source candidate against its HR01 candidate, both rendered to PDF by the same engine (LibreOffice, the independent method AX01 also used for its raster regression) and rasterized at 60 dpi (`16_scripts/hr01_visual_regression.py`; per-page result in `17_qa/hr01_visual_regression.csv`; the rasters stay local-only). Classes: PIXEL IDENTICAL, SUB-PIXEL RENDER VARIANCE, EXPECTED CONTENT CHANGE ONLY (page in the approved-change list), VISIBLE REGRESSION. Native PowerPoint and Word renders of selected changed pages were inspected by eye as a cross-check (slide 38 Arabic tile heading; Arabic First Page letter and footer).

## Results
| Document | Pages | Pixel identical | Expected content change only | Sub-pixel variance | Visible regression |
|---|---|---|---|---|---|
| Part A | 80 | 77 | 3 (slides 38, 65, 68 — approved Arabic strings) | 0 | **0** |
| Part B | 35 | 35 | 0 | 0 | **0** |
| Part C | 78 | 78 | 0 | 0 | **0** |
| Part D | 24 | 24 | 0 | 0 | **0** |
| Word — Arabic First Page | 1 | 0 | 1 | 0 | **0** |
| Word — Arabic Continuation | 1 | 0 | 1 | 0 | **0** |
| Word — Bilingual First Page | 1 | 0 | 1 | 0 | **0** |
| Word — Bilingual Continuation | 1 | 0 | 1 | 0 | **0** |

Word differences are confined to the letter-text bands (subject, salutation, body, closing) and the footer band (about 91–92% of the page height); the logo, tagline and header areas are pixel-identical.

## Reading the result
- The off-slide titles, the 87 decorative flags, the 2 specimen descriptions and the 31 alt texts changed nothing visible on any slide: 214 of 217 slides are pixel-identical. That includes the two covers where AX01 measured a ~0.8 pt shift when mapping the visible heading.
- A native-only check of the footer found and led to the fix of the spacing defect described in `13`; the comparison above is on the corrected files.
- Limits: LibreOffice is not PowerPoint or Word; sub-pixel native variance cannot be ruled out by this method, so native inspection was used for the changed pages. Zero visible regressions are reported for the pages examined.
