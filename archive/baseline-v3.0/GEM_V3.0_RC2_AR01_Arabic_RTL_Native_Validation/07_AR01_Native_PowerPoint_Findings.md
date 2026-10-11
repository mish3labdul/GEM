# 07 · AR01 — Native PowerPoint Findings (Arabic / RTL)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a technical Arabic / RTL validation. It is not native-speaker, translation or localization approval, and it closes no gate.**

Method: byte-identical copies staged in PowerPoint's own sandbox container (as in NP01), opened fresh, **closed without saving**, staged copies re-hashed unchanged. For each Arabic shape: a local-only screenshot (taken before any property read) and a native probe of the **requested** direction, alignment, font, size and bold, plus per-character horizontal positions (`17_qa/native_pass_*.csv`; numbers and generic labels only). PowerPoint 16.113.3. PowerPoint's object model exposes no proofing-language property, so language is read from the XML; it also reports *requested* fonts, not rendered ones.

## Scope actually containing Arabic
Part A slides 37, 38, 39, 65, 66, 68 (11 paragraphs); Part B slide 9 (1 paragraph). **Part C and Part D contain no Arabic text.** Part D's Arabic appears only inside bottle-label pictures, so bidi is **NOT TESTABLE** there. No Arabic in notes, masters, layouts or charts (`17_qa/ar01_static_checks.json`).

## Results on the baseline (D3 Part A / NP01-R1 Part B)
| Check | Result |
|---|---|
| Shaping and joining | Visually correct on **all seven Arabic slides** (Part A 37, 38, 39, 65, 66, 68 and Part B 9), inspected on AR01 contact sheets of the native captures; bracketed placeholders on slides 65 and 68 render with no direction-dependent difference (a fully bracketed single-script string looks the same under either base direction) |
| Requested font | Noto Sans Arabic (latin, ea and cs all set) on all 12 paragraphs; **bold = false; spacing 0** |
| Unaccepted Bold / variable file exercised? | **No**: no bold requested anywhere; no 500; no missing-font banner |
| Containment | Every shape's text lies inside its box; no clipping or footer collision |
| Declared paragraph direction | **Absent on all 12** (PowerPoint reports "left to right") |
| Run language | **`en-US` on all 12 Arabic runs** (should be Arabic) |
| Single-script Arabic paragraphs (10) | Correct visual order in either base direction — **no visual defect** |
| Slide 39 digits paragraph (label + 3 digits) | Correct visual order (digits left of the word) before and after |
| **Slide 39 mixed paragraph (label + Latin code)** | **DEFECT (P2): the code sits to the RIGHT of the Arabic label** (label x 400–490 pt, code x 497–612 pt, right-aligned). For an Arabic reader the code should lie to the left of the label. |

## Slide 39 root cause (technical)
The paragraph has no `rtl` flag, so PowerPoint resolves it with a **left-to-right base direction**; the Arabic run is also tagged `lang="en-US"`. In an LTR paragraph the logical sequence *label → code* is laid out left-to-right as *label | code*, i.e. the code ends up on the right. The stored text order is correct and intended (label first, code after: the slide teaches that technical codes stay Latin and left-to-right, register M12, and the letterhead R03-02 precedent uses the same label-then-code order), so this is **not** character-order corruption and needs no wording change.

## Native variant test (scratch copies of slide 39; positions are native measurements)
| Variant | Mixed paragraph: order | Mixed paragraph: label/code gap | Alignment effect | Verdict |
|---|---|---|---|---|
| V0 baseline | code right of label | 7 pt | right | defect |
| V1 `rtl=1` only | code left of label | **0 pt (touching)** | stays at right edge | order fixed, spacing wrong |
| V2 `rtl=1` + `algn="l"` | code left of label | — | **whole text moves to the left side** | rejected: `algn` is physical (left/right), not start/end; no `algn` change is needed |
| **V3 `rtl=1` + run `lang="ar-SA"`** | **code left of label** | **6 pt (gap restored)** | stays at right edge (612 pt) | **complete fix** |
| V4 `lang="ar-SA"` only | code right of label | 0 pt | right | no order change |

**Measured effect:** the label/code gap is 7 pt in the baseline, falls to 0 pt when `rtl=1` is added alone (V1), and is 6 pt with `rtl=1` plus `ar-SA` (V3). **Inference (the mechanism is not directly observable):** under `lang="en-US"` PowerPoint appears to attach the space between label and code to the Latin segment, so the gap is lost when direction alone changes; declaring the run Arabic restores it. The digits paragraph is geometrically unchanged in every variant.

## After the slide-39 correction (stage-1 AR01 candidate = V3, byte-identical)
- Part A slide 39 both paragraphs now request "right to left" and `ar-SA`; the mixed line reads label at the right, code to its left with a gap; the code is intact left-to-right.
- At stage 1: pixel diff of native captures baseline vs stage-1 candidate was identical on slides 37, 38, 65, 66, 68 and differed only on the two Arabic lines of slide 39; native positions of the other nine Part A shapes were identical. (Superseded for those slides by the final revalidation above.)
- Latin glyph advance widths of the code and digits are unchanged (115.0 pt), so the same font file renders; the Latin characters follow the complex-script text path after the change, giving a slightly lighter stroke rendering. Recorded as an observation, not a font change.
- The Latin code is requested in **Noto Sans Arabic** (the run's `latin` typeface), not Inter/Jost: a governance observation for the owner (technical identifier typography inside an Arabic run), not changed.

## Owner decision 1: the remaining ten paragraphs (applied)
The ten single-script paragraphs (Part A 37, 38 ×3, 65, 66 ×3, 68; Part B 9) are treated as **technical language/direction metadata defects**, not as visual defects. One uniform model now holds on all 12 PowerPoint Arabic paragraphs: `a:pPr rtl="1"`, Arabic run `lang="ar-SA"`, Noto Sans Arabic 400 interim, zero tracking. Part A continued from the slide-39 candidate (`73712e1c…`) → final `2caa4c5c…`; Part B is a NEW candidate derived from NP01-R1 (`44145a44…`) → `63f70622…`; the NP01-R1 slide-30 fix is preserved (slide30.xml byte-identical; `Text 3` cy=2565400 and `Text 5` y=4546550 unchanged). None of the ten contains a Latin letter, so no Latin run exists and no Latin run-language was applied (no run fragmentation). Edits: `ar01_apply_remaining_metadata.py`; log `17_qa/ar01_edit_log_remaining_ten.json`; proof `17_qa/ar01_structural_diff_remaining_ten.json` (inverse transform equals the previous bytes for all 7 changed members; only 5 Part A members and 1 Part B member differ).

## Native revalidation of all Arabic slides (final candidates)
Fresh byte-identical copies (staged hash = candidate hash; unchanged after; closed unsaved; deleted). Data: `17_qa/native_pass_A_AR01_final.csv`, `native_pass_B_AR01_final.csv`; comparisons against the D3 baseline, the stage-1 candidate and NP01-R1.
| Check | Result |
|---|---|
| Requested direction | **right to left on all 12 paragraphs** (was left to right on 10 of 12 in the baseline) |
| Requested font / size / bold | Noto Sans Arabic; sizes and `bold=false` identical to baseline; no 500, no tracking, no missing-font banner |
| Alignment | unchanged (`algn` is physical): 11 right, Part B slide 9 left |
| Text bounds and box | left/right extents identical to the baseline for all 12 shapes (0.1 pt resolution); all inside their boxes; no clipping, collisions or neighbouring-geometry change |
| Per-character progression | slide 39 Text 8: baseline 8 → 7 rightward steps (the slide-39 fix); slides 65 and 68: 1 → 0 and 2 → 0 (bracket pairs now resolve with the RTL base). All others identical. Legitimate RTL-metadata-driven bidi resolution. |
| Screenshot pixel diff vs baseline | slides 37, 38, 65, 66, 68 and Part B 9: **small sub-pixel glyph-edge (anti-aliasing) differences confined to the Arabic text**, 269 to 4,802 differing pixels per capture, none showing a changed glyph, position, bracket orientation, order or clipping in the difference crops (`17_qa/screenshot_pixel_diff_AR01_final.json`). This **supersedes the stage-1 statement that those slides were pixel-identical**: that held only while their metadata was unchanged. The cause (complex-script text path under `ar-SA`) is an inference. Slide 39 is pixel-identical to the stage-1 candidate. |
| Slide 30 (Part B) | NP01-R1 fix preserved (slide30.xml byte-identical) |

## Mixed-run and numeral scrutiny (native character positions, final Part A)
`17_qa/ar01_mixed_run_native_char_order_final.csv` (class sequence and direction only; no text). Slide 39 Text 8 (label + Latin code + digits, now two runs: Arabic+space ar-SA, identifier en-US; class sequence A3 S A5 S L3 P D4): Arabic characters advance **right-to-left**, the Latin letters **left-to-right**, the digits **left-to-right**, and the code block lies to the **left** of the Arabic block (code stays natural LTR; Arabic stays RTL). Slide 39 Text 4 (label + digits): Arabic RTL, digits LTR, digits left of the word. Slides 65 and 68 (bracketed single-script strings): Arabic RTL. The same readings were taken on the split candidate (identical).

## PDF observation (LibreOffice renders of controlled copies; PDFKit extraction; internal working only)
Final PDFs (`19_candidate_corrections/`, INTERNAL WORKING / PENDING VALIDATION): Part A 80 pages, Part B 35 pages; embedded font sets identical to the baseline renders (no new substitution; the pre-existing DejaVuSans / OpenSymbol / LiberationMono symbol fallbacks are unchanged); pages 37, 38, 66 identical in word text and boxes; page 39 as below; **pages 65 and 68: the extracted bracket code points swap order** (pdftotext reports the closing bracket first; PDFKit reports the opening bracket first), i.e. the text layer now records the logical RTL sequence while the raster is unchanged (page 65 pixel-identical, page 68 sub-pixel word edges). Part B: all 35 pages identical in text and word boxes. No tagging or producer change (`17_qa/ar01_partA_pdf_compare_final.json`, `ar01_partB_pdf_compare_final.json`, `pdfkit_logical_order_class_runs_final.json`). D8 stays OPEN.

Baseline Part A page 39: the technical-identifier line extracts as the code's digit and letter segments in the wrong order on the same line as the label. Corrected (and retained in the final candidate): the code `GEM-0000` is extracted intact on its own line, followed by the label line. Evidence: `17_qa/pdfkit_logical_order_class_runs.json` and `…_final.json` (class runs only). This is a basic copy/search observation of a LibreOffice export; it validates no PDF route and does not close D8.

## Observations
- Part B slide 9: the Arabic specimen is left-aligned inside its tile, matching the sibling Latin specimen tiles (Jost, Inter).
- Part A PDFs rendered by LibreOffice embed `DejaVuSans` for one symbol; the delivered D3 PDF has the same font set, so this predates AR01.
- The Latin code on slide 39 stays in Noto Sans Arabic (governance observation; unchanged).

## Final correction: slide 39 Text 8 run split
Applied by `ar01_split_slide39_text8.py` (anchored, one paragraph, one source run, text-pattern asserted; before/after record in `17_qa/ar01_slide39_text8_run_split.json`). Native result on the exact candidate (`bb75f1c1…`, byte-identical to the probed variant): requested direction right-to-left, Noto Sans Arabic 24 pt, not bold; **all 18 character positions identical to the pre-split candidate** (so no spacing, wrap, growth or neighbour change); the slide-39 capture is pixel-identical to the pre-split capture (the only difference is PowerPoint's floating Copilot button, UI not slide content); native positions of the other five Part A Arabic slides unchanged and their captures unchanged apart from sub-threshold capture jitter on slides 65 and 68 (183 and 93 pixels, none above intensity 24; slide XML byte-identical between the two candidates) (`17_qa/native_pass_A_AR01_final2.csv`, `17_qa/screenshot_pixel_diff_final_vs_split.json`). Variant B (the space in the Latin run) shifted the code by 6.25 pt and was rejected. Internal working PDF regenerated: 80 pages, font set identical, text and word boxes identical to the pre-split render on every page, page 39 identical at 200 dpi, `GEM-0000` still extracts intact.

Local-only captures: `16_AR01_Local_Screenshot_Register.csv`. NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.
