# 03 · NP01 Font Environment (inspected before any deck was opened)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7: LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20: OPEN. Native results below were produced with **unaccepted working-build fonts**; font acceptance (VAL-05, Y03, VAL-19, VAL-07) is **not** closed by NP01.

Method: filename search of `~/Library/Fonts`, `/Library/Fonts`, `/System/Library/Fonts`; `fc-scan` / `fc-list` family and style; SHA-256 against the repository's own records (`ODI01-R1/07_Font_Claim_File_Matrix.csv`, letterhead `Original_Font_Manifest.json`).

| Font | Location | Installed? | Accepted? | SHA-256 (first 12) | Potential native substitution risk |
|---|---|---|---|---|---|
| Jost 400 (Regular) | `~/Library/Fonts/GEM-Working-Jost-Regular.ttf` (family "Jost", style Regular) | Yes | **Working build only.** Matches the repo's `Jost-Regular.ttf` (v3.710). Font master/build and licence acceptance PENDING; ODI01-R1 07 records "no accepted file" for 500. | db44231dc34c | Low: this is the intended 400 face. |
| Inter 400 (Regular) | `~/Library/Fonts/GEM-Working-Inter-Regular.ttf` | Yes | Working build only (v4.001); acceptance PENDING | 8bac02d5d1dc | Low |
| Noto Sans Arabic 400 (Regular) | `~/Library/Fonts/GEM-Working-NotoSansArabic-Regular.ttf` | Yes | Working build only (v2.012); acceptance PENDING | 35965bc142de | Low |
| Jost Bold (700) | `~/Library/Fonts/GEM-Working-Jost-Bold.ttf` (family "Jost", style Bold) | **Yes** | **NO.** Letterhead manifest: "ARCHIVED INPUT / 700 NOT USED". | b4fe593d2c35 | **Would be picked by PowerPoint for any bold run** under family "Jost" (same family name as the Regular). |
| Inter Bold (700) | `~/Library/Fonts/GEM-Working-Inter-Bold.ttf` | **Yes** | **NO** (same status) | e71b947fd82d | Same |
| Noto Sans Arabic Bold (700) | `~/Library/Fonts/GEM-Working-NotoSansArabic-Bold.ttf` | **Yes** | **NO** (same status) | 2e369a68dbc7 | Same |
| 500 / Medium of any of the three | — | **Not installed** (none found) | No accepted file exists (D5) | — | None |
| Variable builds (`Jost[wght]`, `Inter[opsz,wght]`, `NotoSansArabic[wdth,wght]`) | — | **Not installed** | Not accepted | — | None |
| GEM-Working font builds | the six files above | Yes (named `GEM-Working-*`; family names are plain "Jost" / "Inter" / "Noto Sans Arabic") | See rows above | — | The family names carry no "GEM-Working" marker, so a bold run cannot be told apart from an accepted face by name. |

## Stop-condition analysis (task 2)
The installed Bold files share the family names of the accepted Regular files, so PowerPoint would use a **true Bold face** for any bold run. That would invalidate the 400-only test condition, and it could not be told apart visually from faux bold. The condition was therefore tested directly:
- **Static scan (OOXML, all four decks):** no `b="1"|"true"|"on"` in slides, layouts, masters, notes slides, notes masters, themes, `presentation.xml` `defaultTextStyle`, table styles (none defined), charts or diagrams (none exist). No `tableStyleId` references. No embedded fonts. No external links.
- **Native sweep (PowerPoint 16.113.3):** effective `bold` of every slide text range on all 217 slides, resolved **per character** whenever a range reported `true` or a mixed family, and of every text cell in every table (tables are not text-frame shapes and were swept separately). Scope: slide text shapes and table cells only; **notes pages and master/layout text were covered by the OOXML scan only**.
  - **Result: 0 bold characters** in 2,210 text shapes and 1,605 table text cells (Part A 887+12, Part B 252+666, Part C 769+912, Part D 302+15).
  - 41 Part B and 2 Part A ranges reported range-level `bold=true`. All resolved to 0 bold characters at character level: PowerPoint reports "mixed" as `true` when a word straddles a run boundary (a run with explicit `b="0"` next to a run with no attribute). Shape-level `bold=true` is **not** evidence of bold.
- **Conclusion: the stop condition was NOT triggered.** The installed unaccepted Bold files were not exercised by any text in the four candidate decks. Nothing was uninstalled or changed. This does not make those files accepted, and it does not show the system supports 700.

## What the 'family' evidence is and is not
PowerPoint's object model (`font name`) returns the typeface **requested in the file**; it does not reveal a face PowerPoint substituted at render time. NP01 therefore cannot prove 'no substitution' from properties alone. The supporting evidence is: the three families are installed; no missing-font banner appeared on any deck; and the 89 slides viewed rendered with the expected Jost/Inter/Noto Sans Arabic letterforms. In `06`, the column is named 'Requested family (PowerPoint object model…)', the expected-family column is the **allowed set** (per-role family was not tested), and 'Substitution?' reads 'not detectable by object model…'.

## Other native family observations
- Effective native families seen: **Jost, Inter, Noto Sans Arabic** only, plus **one Courier New** text shape (Part B slide 30, a token-excerpt code box). Courier New is a non-brand system face present in the source deck; recorded as an OBSERVATION. It is also the cause of the slide 30 overflow defect (`05`).
- **Arabic runs** set `<a:cs typeface="Noto Sans Arabic">` (Part A slides 37, 38, 39, 65, 66, 68; Part B slide 9), so shaping uses the intended face, not a system fallback. Native renders show correctly joined glyphs.
- **Part D** theme fonts are Calibri/Calibri Light, but every text run carries an explicit Jost or Inter typeface; only empty shapes report Calibri.
- No font-substitution banner and no missing-font warning appeared on any deck.
