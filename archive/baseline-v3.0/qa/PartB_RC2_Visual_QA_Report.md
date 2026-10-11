# Part B RC2 — Visual QA Report

**Method.** All 35 slides of B-RC2 exported with LibreOffice (tagged PDF filter, brand fonts installed: Jost, Inter, Noto Sans Arabic from Google Fonts OFL builds, used for rendering only), rendered with pdftoppm, inspected on contact sheets; every modified slide compared side by side with the original 33-slide deck (`PartB_RC2/03_renders/pairs*`). The previous 77-page review PDF was used only to confirm that the deck carries the same rules; it is not regenerated (its HTML source was never supplied).

## Export facts
| Item | Result |
|---|---|
| Pages | 35 |
| Tagged PDF | yes (`UseTaggedPDF`) |
| Embedded fonts | Jost-Regular, Inter-Regular (two subsets), NotoSansArabic-Regular, LiberationMono (substitute for the Courier New code specimen on slide 30), OpenSymbol (bullets) |
| Font substitution | Courier New → LiberationMono in this environment only; Jost/Inter/Noto rendered from the installed OFL variable builds. Weight 500 runs render from the variable file under the "Regular" face name. |
| OOXML validation | All validations passed (against the original deck) |
| Pictures / alt text | 0 pictures in the deck (no logo artwork embedded, VAL-02); nothing to alt-text. Decorative cover geometry is vector shapes without text. |

## Slide-by-slide (modified slides)
| Slide | Change | Result | Notes |
|---|---|---|---|
| 1 | status line | PASS | one line, Jost 12 tracked |
| 2 | edition states | PASS | box grown to 1.2" |
| 3 | tagline rule | PASS | |
| 4 | table row C, authority list, domain note, read order | PASS after fix | first pass: list overflowed into the footer and the table overlapped the headings; cell text shortened, list re-set as seven numbered paragraphs at 11 pt, headings moved to 4.08" |
| 5 | role names, citation | PASS after fix | table rows wrapped; notes moved to 5.0" |
| 9 | weights, licence cross-reference | PASS | |
| 11 | navigation rule | PASS | |
| 12 | S07 row | PASS | table grew 0.3"; note moved |
| 13 | mechanics sentence | PASS | |
| 18 | warning glyph | PASS | three notes equalised at 1.1" |
| 21 | currency row | PASS after fix | row text shortened; DatePicker paragraph moved to 4.85" |
| 25 | template rows | PASS | |
| 26 (new) | booking-flow test | PASS | five outlined boxes with arrows, five annotation columns; status note names CONCEPT / IMPLEMENTATION TEST |
| 27 | hierarchy sentence, policy placeholder | PASS | table moved down 0.25" |
| 28 | photography cross-reference | PASS | |
| 29 | S07 row | PASS after two fixes | cell shortened; note moved to 5.3" |
| 30 | EXCERPT label, source note, version | PASS | code block in Courier New (flagged) |
| 31 | Production row | PASS | |
| 32 | VAL-18 note | PASS | footer wraps to two lines, clear of table |
| 33 | change-log heading | PASS | |
| 34 (new) | document control + change log | PASS after two fixes | ten numbered lines at 11 pt; change-log paragraphs un-bolded and re-stacked |
| 35 | X12 note | PASS | |
| all | footers | PASS | 34 footers "GEM™ Digital Design System V3.0 RC2 · working specification · n"; cover has no footer by design |

Unmodified slides 6, 7, 8, 10, 14, 15, 16, 17, 19, 20, 22, 23, 24: no drift.

## Checks applied
clipping · overlap · accidental empty pages (none) · font substitution (Courier New only) · Arabic shaping (slide 9 specimen, slide 12/13 tables: correct joining, RTL alignment) · footer consistency · slide numbering (renumbered after insertions) · line breaks · table overflow (fixed on 4, 5, 12, 21, 29) · status labels (shape coding preserved on slide 2) · geometry/text collisions (cover only; none).

## Residual observations
- Courier New on slide 30 is not an approved family; retained as a code specimen and flagged [REQUIRES OWNER] (no monospace decision in L01–L16).
- The deck contains no component specimens or screenshots; the 77-page review PDF remains the only visual record of components until the component bundle exists (VAL-13).
