# Part B RC2 — Accessibility QA Report

**Target:** WCAG 2.2 AA minimum (K08, V01). **Scope available:** the Part B RC2 deck and its PDF export, plus the documented rules. **Not available:** the component bundle, Storybook, any running UI. Component-level results are therefore **NOT TESTED**; this is a self-check, not independent validation (VAL-08 stays "In progress" per the register).

Legend: PASS · FAIL · NOT TESTED · PENDING NATIVE QA · DOCUMENTED (rule exists in the system; behaviour untestable here).

## A. Document (deck and PDF) checks
| Check | Result | Evidence / note |
|---|---|---|
| Slide titles present (V04) | PASS | every content slide has a title shape |
| Logical reading order (V05) | PASS (deck) / NOT TESTED (AT) | shape order follows visual order; cloned shapes inserted next to their siblings; not verified with a screen reader |
| Tagged PDF (V13) | PASS (export) | `Tagged: yes`; tag quality not verified with assistive technology (VAL-15) |
| Table headers (V06) | PASS | every table has a header row; LibreOffice export marks first row as header |
| Images alt text (V02, V03) | PASS (vacuous) | 0 pictures in deck |
| Text contrast (K01–K06) | PASS | Ink/White, Ink/Beige, White/Ink only; no Beige-on-White text |
| Meaning not by colour (V10) | PASS | status labels use word + border style |
| Fonts embedded (L06) | PASS with note | Jost, Inter, Noto Sans Arabic embedded; Courier New substituted by LiberationMono |
| Document language | NOT TESTED | PDF language metadata not set by the exporter; add in a native PowerPoint export |
| Link semantics (V07) | DOCUMENTED | no hyperlinks in the deck; rule on slide 16 |

## B. Component and interaction checks (rules documented; runtime untestable)
| Area | Requirement (slide) | Result |
|---|---|---|
| Keyboard: full navigation, no traps, dialog Esc/close, focus restoration | 16 (V09), 13, 21 DatePicker, Modal | NOT TESTED — no running components; rules DOCUMENTED |
| Focus: visible, 2 px ring, 2 px offset, Ink on light / White on signature | 8, 16 (V08); tokens `semantic.focus.*` | DOCUMENTED; token values present in `gem-tokens.v3.0-rc2.json` |
| Screen reader: English | 16 (role=alert/status, aria-invalid + describedby, aria-current, aria-selected/pressed) | NOT TESTED |
| Screen reader: Arabic, reading order | 16 (V14), 13 | PENDING NATIVE QA (VAL-07, V14) |
| Zoom / reflow 320 CSS px, 400 % | 15 (WCAG 1.4.10) | NOT TESTED — DOCUMENTED |
| Reduced motion | 17 (`duration-instant` 0 ms, V11); CSS `prefers-reduced-motion` block in token CSS | DOCUMENTED; token CSS generated |
| Colour independence | 7, 16, 19 (state label + title + sentence) | DOCUMENTED |
| Target size ≥ 44 × 44 | 16 (V12); `size.target.min` | DOCUMENTED |
| Forced colours | 16 (per-release list) | NOT TESTED |
| Disabled controls focusable with reason | 16 | DOCUMENTED |
| Booking flow (slide 26) focus order, error placement | 26, `02_build/flow/booking-flow-test.md` | DOCUMENTED; NOT TESTED |

## C. Evidence status
- VAL-08 Accessibility implementation QA: **In progress** (register). Nothing here closes it.
- VAL-15 Native presentation/PDF QA: **Not started**; the tagged export is an input to it, not its result.
- Independent accessibility QA by a named Accessibility QA holder: **not performed** (holder TBD, AC19).

## D. Limitations recorded honestly
1. No independent tester, no assistive technology run, no browser-based component harness exists in this workspace.
2. The LibreOffice tagged export sets structure tags but not document language; a native PowerPoint accessible export is required for VAL-15.
3. Arabic strings remain working placeholders; any Arabic accessibility result is PENDING NATIVE QA.
