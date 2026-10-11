# GEM™ V3.0 RC2 — Visual QA Report

**Method.** Every slide of Part A RC2 (80) and Part C RC2 (78) was exported with LibreOffice to a tagged PDF with the brand fonts installed (Jost, Inter, Noto Sans Arabic; Google Fonts OFL builds used for rendering only), rendered to PNG with pdftoppm, and inspected as contact sheets. Every modified slide was additionally inspected side by side against the RC1/working-edition render of the same slide (`02_renders/A_pairs*`, `C_pairs*`). Renders are not committed (`.gitignore`); they regenerate with `05_logs/edit_part*.py` + `soffice`.

**Part B** was not re-rendered: the review PDF is unchanged (no editable source). Its existing render state is recorded in the audit and in `PartB_RC2_Exact_Patch_Spec.md` §PB-EXPORT.

## Export facts

| File | Pages | Tagged PDF | Embedded fonts in export | Deck fonts referenced |
|---|---|---|---|---|
| A-RC2.pdf | 80 | yes | Jost-Regular, Inter-Regular, NotoSansArabic-Regular, DejaVuSans (bullet glyphs) | Jost, Inter, Noto Sans Arabic |
| C-RC2.pdf | 78 | yes | Jost-Regular, Inter-Regular | Jost, Inter |
| B (original) | 77 | **no** | Jost-Regular, Inter-Regular, DejaVuSans | n/a |

Note on weights: the LibreOffice export of A and C embeds the variable-font instances under the "Regular" name; Jost/Inter 500 runs render from the same variable file. This is a rendering-environment fact, not evidence for VAL-05/VAL-19, which stay open. Tagged export was achieved with the `UseTaggedPDF` filter option; reading order and tag quality have not been verified with assistive technology (VAL-15 open).

## Checklist applied to every modified slide

overlaps · clipping · type substitution · Arabic shaping · RTL flow · geometry/text collisions · table overflow · footer consistency · slide numbering · status labels · line breaks · tracking · image quality · drift against the original.

## Part A — modified slides (28) and result

| Slide | Change | Result | Notes |
|---|---|---|---|
| 1 | status line, document ID | PASS | two-line status, no clipping |
| 3 | seven-step authority list, domain note, C tile | PASS after fix | first pass: tile text overflowed, note clipped (autofit removed, box resized); reading order of cloned shapes moved next to item 6 |
| 4 | labels and edition states | PASS after fix | box height increased |
| 6 | headline moved below ring | PASS | ring no longer crosses "Every arrival" |
| 23 | Jost 400 | PASS | |
| 33 | Beige-on-White tile text | PASS after two fixes | text shortened to fit the tile |
| 34 | tracking sentence | PASS after fix | box grown upward; no overlap with alphabet specimen |
| 35 | label example | PASS | |
| 36 | CONDITIONAL VAL-19 | PASS after fix | note box re-sized |
| 38 | S07 cross-reference | PASS | Arabic shaping correct, RTL alignment preserved |
| 41 | headline/body narrowed, rule wording | PASS | ring (in background image, cannot move) now clear of text |
| 43 | placement rule | PASS | |
| 45 | glyph wording | PASS | |
| 46 | subtitle moved below title | PASS | pre-existing title/subtitle overlap also removed |
| 48 | category note | PASS | 10 pt note, two lines |
| 50 | status label | PASS | |
| 51 | CONDITIONAL / VAL-14 | PASS after fix | note moved up 0.22" |
| 53 | radius wording | PASS | |
| 60 | tier status | PASS | |
| 61 | six levels | PASS | rows re-spaced; rules realigned |
| 65 | S07 default, S02 deferral | PASS after fix | status line re-positioned |
| 68, 69 | template gates | PASS | |
| 72 | twelve roles, 4×3 grid | PASS | tiles 1.2" tall; long names wrap to two lines inside tiles |
| 75 | X12 naming | PASS | |
| 78 | VAL IDs | PASS | right column items wrap to two lines within their 0.69" boxes |
| 79 (new) | document control | PASS after fix | change-log line widened to 9.5"; footer label updated |
| 80 | closing line | PASS | |
| all | footer "V3.0 RC2" | PASS | 59 footers |

Unmodified slides (2, 5, 7–22, 24–32, 37, 39, 40, 42, 44, 47, 49, 52, 54–59, 62–64, 66, 67, 70, 71, 73, 74, 76, 77): no drift observed against the original render.

## Part C — modified slides (27) and result

| Slide | Change | Result | Notes |
|---|---|---|---|
| 1 | RC2, document ID | PASS | |
| 2 | authority list + domain note | PASS after fix | first pass overflowed into the core-rule line; text shortened, rule moved down |
| 3 | labels, edition states | PASS | two notes stacked, no overlap |
| 4 | register role names, merged Supplier QA row | PASS | table one row shorter; note re-positioned |
| 7 | Black symbol row, file list | PASS | |
| 12, 13 | promotion rule | PASS | |
| 14 | footer prefix | PASS | |
| 20 | T13 wording | PASS | rules shifted 0.22" |
| 27 | tier status | PASS after fix | "Core Collection [REQUIRES OWNER]" at 13 pt; owner tiles moved below note |
| 29 | six levels | PASS | |
| 39 | external signage row | PASS | table grew one row |
| 41 | Arabic-first default | PASS after fix | tile text shortened |
| 44 | template gate | PASS | |
| 56 | X12 pattern + proposal box | PASS | |
| 61 | Y06 clause | PASS | row wraps to three lines |
| 63, 64, 71 | added rows | PASS | result lines shifted 0.36" |
| 65 | four added rows | PASS | |
| 73 | X12 note, proposals split into two lines | PASS after two fixes | |
| 75 | gate IDs | PASS | |
| 76 | gate ID lines | PASS | |
| 77 (new) | document control | PASS after fix | two status boxes 0.85" tall |
| 78 | RC2 closing | PASS | |
| all | footer "V3.0 RC2" | PASS | 70 footers |

Unmodified slides: no drift observed.

## Residual observations (not changed)
- A 15 table keeps the default grey style (CR-49, optional polish, left for the Design Custodian).
- A 41's ring is baked into the background image; text was moved instead of the ring.
- Section numbers in Part C titles still differ from slide numbers (CR-55, optional).
- Arabic strings remain working placeholders; shaping verified visually only, not by a native reviewer (VAL-07 open).

## Verdict
A-RC2 and C-RC2: all modified slides rendered and checked; no overlap, clipping, substitution or numbering defect remains. Part B: not re-rendered; blocked on source.
