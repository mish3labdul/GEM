# Part B RC2 — RTL / Localization QA Report

**Status retained:** every Arabic string is a working layout string, **PENDING LOCALIZATION APPROVAL**; Arabic release status **PENDING VALIDATION** until native RTL, localization, mixed-language and accessibility QA passes (M01, VAL-07, AC10). No native reviewer was available; the gate stays open.

Legend: PASS (verifiable in the deck/tokens) · DOCUMENTED (rule present, runtime untestable) · NOT TESTED · PENDING NATIVE QA.

| Check | Where | Result | Note |
|---|---|---|---|
| Bilingual default synchronized (Arabic leads for approved Saudi/GCC contexts; exceptions documented) | B 12, 13, 29; A 38/65; C 41 | PASS | S07 verified in the register; wording aligned across A/B/C |
| Part B owns the mechanics (dir, logical properties, bidi) | B 13 | PASS | stated explicitly |
| `dir="rtl"` on document root | B 2, 12, 13 | DOCUMENTED | M06 |
| Logical CSS properties only | B 13; token CSS `[dir="rtl"]` note | DOCUMENTED | no left/right in component CSS |
| Mixed-language isolation (`<bdi>` / `dir="ltr"` spans) | B 13 | DOCUMENTED | |
| Arabic/Latin codes stay LTR (SKU, URL, phone, batch, booking ID) | B 12, 13, 21, 26 | DOCUMENTED | M12; booking ID in flow test kept LTR |
| Numerals: Arabic-Indic for guest copy (CONDITIONAL), Latin for technical | B 12, 21; tokens `locale.numerals*` | DOCUMENTED | M11 |
| Dates: locale week start via `Intl.Locale weekInfo`; Gregorian default; Hijri [REQUIRES OWNER] | B 21; tokens `locale.calendarDefault` | DOCUMENTED | DS06 |
| Currency format | B 21 new row; tokens `locale.currencyFormat` | [REQUIRES OWNER] | no price invented |
| Navigation, Tabs, Cards, Forms, Dialogs in RTL | B 13 (mirror table), 15 | DOCUMENTED; NOT TESTED | component bundle absent |
| DatePicker in RTL (arrows swap, Arabic-Indic digits, text summary) | B 21 | DOCUMENTED; NOT TESTED | |
| Wayfinding bilingual examples | B 29; A 65/66; C 41 | DOCUMENTED | fabrication PROJECT-SPECIFIC (VAL-12 deferred) |
| Responsive RTL across the matrix (Q18) | B 13 footer, 14, 15 | PENDING VALIDATION | VAL-20 |
| Arabic typography: Noto Sans Arabic, tracking 0, line-height ≥ 1.7, no italics | B 9, 11, 12; tokens `type.tracking.arabic`, `type.arabicLineHeightMin` | PASS (rules) / PENDING NATIVE QA (optics) | M02, M04, M05 |
| Logo never mirrored | B 12, 13, 35 | PASS (rule) | M08 |
| No Latin tracking on Arabic | B 11, 12 | PASS (rule) | M05 |
| No fake RTL (no flipped Latin, no mirrored artwork) | B 13 | PASS (rule) | |
| Arabic shaping in the deck specimen (slide 9 "أب") | render | PASS | Noto Sans Arabic embedded in export |
| Arabic copy approval | all | PENDING NATIVE QA | professional copyediting mandatory before release (M16) |

**Evidence status:** VAL-07 Not started · AC10 Evidence Required · VAL-20 Not started. Nothing in this report changes them.
