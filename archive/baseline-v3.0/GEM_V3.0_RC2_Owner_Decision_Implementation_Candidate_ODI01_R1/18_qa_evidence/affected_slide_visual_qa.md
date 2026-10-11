# Affected-slide visual QA — ODI01-R1

**Renderer: LibreOffice 26.8.1 (macOS, headless) — REVIEW EVIDENCE ONLY. This is not native PowerPoint validation; native PowerPoint QA remains OPEN.** ODI01 PDFs were made with LibreOffice 24.2; to compare like with like, **both** the ODI01 candidate ("before") and the R1 candidate ("after") were re-rendered here with identical settings (tagged PDF; accepted Regular 400 files of Jost, Inter and Noto Sans Arabic supplied from the repository, so bold requests render as the same synthetic bold seen in the ODI01 PDFs).

**Affected slides = every slide whose OOXML part changed: 64 slides** (Part A 2, Part B 29, Part C 33, Part D 0). Derived from `17_scripts/r1_verify_edits.py`, not from searching for the string "500".

Method per slide: (1) rasterised before and after at 80 dpi and joined side by side (`render/<Part><slide>_before_after.png`: left = before, right = after); (2) word boxes compared via `pdftotext -bbox-layout`: word count, line count, largest word-origin shift, words outside the page, overlapping words; (3) visual inspection where marked.

Checks covered by (2): overflow, clipping, changed line wrapping, table fit, footer alignment and logo/text collision (no word box overlaps or leaves the page), unintended object movement (origin shift), font substitution (PDF fonts after: Inter-Regular, Jost-Regular, NotoSansArabic-Regular + the same non-brand helpers as before). Accidental colour change: colours are unchanged in the XML (srgbClr sets identical, QA item 6). Arabic shaping/RTL: no Arabic run was changed except bold-flag removal on the Part B tables; text and shaping geometry unchanged (shift 0).

| Document | Slide | Reason affected | Before / after render | Result | Adjustment required? |
|---|---|---|---|---|---|
| Part A | 15 | 2 explicit bold flag(s) cleared (b=1→0) | `render/A15_before_after.png` | PASS (metrics only) | No |
| Part A | 35 | 1 wording edit(s) (D5 500→400 / pending) | `render/A35_before_after.png` | PASS (inspected) | No further adjustment (text edits fit; added box clear of footer) |
| Part B | 3 | 4 explicit bold flag(s) cleared (b=1→0) | `render/B03_before_after.png` | PASS (inspected) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 4 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B04_before_after.png` | PASS (metrics only) | No |
| Part B | 5 | 5 explicit bold flag(s) cleared (b=1→0) | `render/B05_before_after.png` | PASS (metrics only) | No |
| Part B | 6 | 2 explicit bold flag(s) cleared (b=1→0) | `render/B06_before_after.png` | PASS (metrics only) | No |
| Part B | 7 | 9 explicit bold flag(s) cleared (b=1→0) | `render/B07_before_after.png` | PASS (inspected) | No |
| Part B | 10 | 5 explicit bold flag(s) cleared (b=1→0); 1 wording edit(s) (D5 500→400 / pending); clarification text box added | `render/B10_before_after.png` | PASS (inspected) | No further adjustment (text edits fit; added box clear of footer) |
| Part B | 11 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B11_before_after.png` | PASS (inspected) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 12 | 5 explicit bold flag(s) cleared (b=1→0); 2 wording edit(s) (D5 500→400 / pending); clarification text box added | `render/B12_before_after.png` | PASS (inspected) | No further adjustment (text edits fit; added box clear of footer) |
| Part B | 13 | 5 explicit bold flag(s) cleared (b=1→0) | `render/B13_before_after.png` | PASS (inspected) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 14 | 6 explicit bold flag(s) cleared (b=1→0) | `render/B14_before_after.png` | PASS (inspected) | No |
| Part B | 15 | 4 explicit bold flag(s) cleared (b=1→0) | `render/B15_before_after.png` | PASS (metrics only) | No |
| Part B | 16 | 4 explicit bold flag(s) cleared (b=1→0) | `render/B16_before_after.png` | PASS (metrics only) | No |
| Part B | 17 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B17_before_after.png` | PASS (metrics only) | No |
| Part B | 18 | 6 explicit bold flag(s) cleared (b=1→0) | `render/B18_before_after.png` | PASS (metrics only) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 19 | 8 explicit bold flag(s) cleared (b=1→0) | `render/B19_before_after.png` | PASS (metrics only) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 20 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B20_before_after.png` | PASS (metrics only) | No |
| Part B | 21 | 4 explicit bold flag(s) cleared (b=1→0) | `render/B21_before_after.png` | PASS (inspected) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 22 | 4 explicit bold flag(s) cleared (b=1→0); 1 wording edit(s) (D5 500→400 / pending) | `render/B22_before_after.png` | PASS (inspected) | No further adjustment (text edits fit; added box clear of footer) |
| Part B | 23 | 4 explicit bold flag(s) cleared (b=1→0) | `render/B23_before_after.png` | PASS (inspected) | No |
| Part B | 24 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B24_before_after.png` | PASS (inspected) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 25 | 2 explicit bold flag(s) cleared (b=1→0) | `render/B25_before_after.png` | PASS (inspected) | No |
| Part B | 26 | 5 explicit bold flag(s) cleared (b=1→0) | `render/B26_before_after.png` | PASS (inspected) | No |
| Part B | 27 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B27_before_after.png` | PASS (metrics only) | No |
| Part B | 29 | 2 explicit bold flag(s) cleared (b=1→0) | `render/B29_before_after.png` | PASS (metrics only) | No |
| Part B | 30 | 1 explicit bold flag(s) cleared (b=1→0) | `render/B30_before_after.png` | PASS (metrics only) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 31 | 3 explicit bold flag(s) cleared (b=1→0) | `render/B31_before_after.png` | PASS (metrics only) | No |
| Part B | 32 | 6 explicit bold flag(s) cleared (b=1→0) | `render/B32_before_after.png` | PASS (metrics only) | No |
| Part B | 33 | 4 explicit bold flag(s) cleared (b=1→0) | `render/B33_before_after.png` | PASS (metrics only) · hierarchy weakened | No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced. |
| Part B | 35 | 5 explicit bold flag(s) cleared (b=1→0) | `render/B35_before_after.png` | PASS (metrics only) | No |
| Part C | 4 | 6 explicit bold flag(s) cleared (b=1→0) | `render/C04_before_after.png` | PASS (metrics only) | No |
| Part C | 7 | 3 explicit bold flag(s) cleared (b=1→0) | `render/C07_before_after.png` | PASS (metrics only) | No |
| Part C | 9 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C09_before_after.png` | PASS (metrics only) | No |
| Part C | 15 | 4 explicit bold flag(s) cleared (b=1→0); clarification text box added | `render/C15_before_after.png` | PASS (inspected) | No further adjustment (text edits fit; added box clear of footer) |
| Part C | 21 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C21_before_after.png` | PASS (metrics only) | No |
| Part C | 23 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C23_before_after.png` | PASS (inspected) | No |
| Part C | 28 | 5 explicit bold flag(s) cleared (b=1→0) | `render/C28_before_after.png` | PASS (inspected) | No |
| Part C | 30 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C30_before_after.png` | PASS (inspected) | No |
| Part C | 32 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C32_before_after.png` | PASS (inspected) | No |
| Part C | 34 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C34_before_after.png` | PASS (inspected) | No |
| Part C | 39 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C39_before_after.png` | PASS (inspected) | No |
| Part C | 43 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C43_before_after.png` | PASS (metrics only) | No |
| Part C | 44 | 3 explicit bold flag(s) cleared (b=1→0) | `render/C44_before_after.png` | PASS (metrics only) | No |
| Part C | 47 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C47_before_after.png` | PASS (metrics only) | No |
| Part C | 49 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C49_before_after.png` | PASS (metrics only) | No |
| Part C | 51 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C51_before_after.png` | PASS (metrics only) | No |
| Part C | 52 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C52_before_after.png` | PASS (metrics only) | No |
| Part C | 54 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C54_before_after.png` | PASS (metrics only) | No |
| Part C | 57 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C57_before_after.png` | PASS (metrics only) | No |
| Part C | 60 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C60_before_after.png` | PASS (metrics only) | No |
| Part C | 61 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C61_before_after.png` | PASS (metrics only) | No |
| Part C | 62 | 8 explicit bold flag(s) cleared (b=1→0) | `render/C62_before_after.png` | PASS (metrics only) | No |
| Part C | 63 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C63_before_after.png` | PASS (metrics only) | No |
| Part C | 64 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C64_before_after.png` | PASS (metrics only) | No |
| Part C | 65 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C65_before_after.png` | PASS (metrics only) | No |
| Part C | 66 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C66_before_after.png` | PASS (metrics only) | No |
| Part C | 67 | 2 explicit bold flag(s) cleared (b=1→0) | `render/C67_before_after.png` | PASS (metrics only) | No |
| Part C | 68 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C68_before_after.png` | PASS (metrics only) | No |
| Part C | 69 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C69_before_after.png` | PASS (metrics only) | No |
| Part C | 70 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C70_before_after.png` | PASS (inspected) | No |
| Part C | 71 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C71_before_after.png` | PASS (inspected) | No |
| Part C | 72 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C72_before_after.png` | PASS (inspected) | No |
| Part C | 74 | 4 explicit bold flag(s) cleared (b=1→0) | `render/C74_before_after.png` | PASS (inspected) | No |

## Results

- Slides rendered before and after: **64 / 64**.
- Slides inspected by eye (individual images or contact sheets): **25**; remaining 39 are covered by the automated geometry metrics only and are labelled "metrics only".
- Word count / line count unchanged on every slide except the 5 edited slides (Part A 35, Part B 10, Part B 12, Part B 22, Part C 15); there the changes are the intended wording and clarification boxes.
- Largest word-origin shift on an unedited slide: 1.19 pt (sub-pixel; no re-wrapping).
- New overlaps after: 0. Words outside page after: 0. Footer / logo collisions: none observed.
- **Visual regressions found: none that break layout.** One **hierarchy finding**: on 9 slides (B3, B11, B13, B18, B19, B21, B24, B30, B33) bold run-in heads and emphasis ("Character.", "Principles.", "Use:", "Added:" …) now read at 400. They stay legible and identifiable by punctuation and position, but their emphasis is weaker. Not corrected: re-adding bold is prohibited by D5, and the alternative cues (capitalisation, size, rules) would be a design change beyond a narrow reconciliation. **Owner decision (review closure): accepted as a temporary 400 treatment; no compensating change authorized.** Intended emphasis may be restored only when an accepted corresponding 500-weight font file is introduced through the governed font-validation process.
- Table header rows (Part B Beige fill, Part C Ink fill with white text) keep their hierarchy through fill and contrast.

Pre-existing, unchanged by R1: on Part B slide 12 the footnote starts at the lower edge of the right-hand table in the LibreOffice render (also visible in the "before" render).

Not tested: native PowerPoint rendering, PowerPoint accessibility checker, reading order, Windows/Mac PowerPoint font fallback.
