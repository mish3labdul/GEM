# 02 · NP01-R1 — Authority and Before-State (Part B slide 30)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D3 RESOLVED AT OWNER-DECISION LEVEL (X12 STREAM = BRAND) · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN · D8 external Arabic/bilingual PDF BLOCKED. **UNAPPROVED CANDIDATE. NOT RELEASED.**

Scope: **Part B slide 30 only.** Evidence: `qa_evidence/01_authority_slide30_before_state.json` (produced by `scripts/np01r1_authority_check.py`, read-only).

## Slide 30 across the three lineages
| Deck | Deck SHA-256 (first 12) | `slide30.xml` SHA-256 (first 12) |
|---|---|---|
| RC2 release deck (authoritative) | b0326b6a6d9c | 331bd81f88c9 |
| RC2 source deck (authoritative) | b0326b6a6d9c | 331bd81f88c9 |
| ODI01-R1 candidate (current) | 22802377eb73 | f5679eba6e69 |

The RC2 release deck and the RC2 source deck are the **same file** (identical deck hash), so slide 30 is identical in both; the ODI01-R1 candidate differs only by the D5 bold flag described next.

## What differs between the authoritative RC2 deck and the ODI01-R1 candidate on slide 30
Exactly one thing: shape `Text 5` (the "Storybook-ready…" paragraph) has `b="1"` in the authoritative deck and `b="0"` in the candidate. That is the accepted **D5** change (400 only). **Nothing else differs**: all seven text strings, all shape offsets and extents, all `bodyPr` insets, font sizes, typefaces (Courier New in the excerpt box, Inter elsewhere), exact line spacing (16.8 pt) and colours are identical.

## Conclusions
- **Wording unchanged.** All `<a:t>` strings identical across the three decks.
- **The defect is geometry/layout only**: the token-excerpt box (`Text 3`) is 166.4 pt tall but its content needs 199.3 pt natively.
- **No governance text needs changing** (no status, gate, release or approval wording is in the excerpt box or the paragraph below).
- **No token content needs changing**: the excerpt is a group-name listing (foundation.color … motion · layout · locale), not token values or statuses; D4 values/statuses are not on this slide.
- **Provenance:** the defect is in the authoritative RC2 release and source decks as well (not opened natively). NP01-R1 corrects the **controlled candidate lineage only**; the authoritative decks are untouched and would need a separately authorized promotion.

## Before state (native, NP01 and re-captured in NP01-R1)
- Text 3 (`Courier New`, 12 pt, exact 16.8 pt line spacing, insets L 16.0 / T 16.0 / R 5.56 / B 14.0 pt): 9 logical lines; line 1 (51 characters, 367.2 pt) wraps, giving 10 rendered lines; native text bounds height **169.3 pt**; box **166.4 pt** (4826000 × 2112963 EMU at x 64.0 pt, y 140.0 pt).
- Inset-aware need = 16.0 + 169.3 + 14.0 = **199.3 pt** against 166.4 pt: short by 32.9 pt; the text starts 16 pt below the box top, so it escapes the dark fill by **18.9 pt**. The last line, "motion · layout · locale", is outside the fill and not visible; the line above is partly clipped.
- Below the box: `Text 5` at y 322.4 pt (gap 16.0 pt).
- Local screenshot of the before state: `local_only_screenshots/B_s030_BEFORE_ODI01-R1_native.png` (local-only, see `07`).

## Detection scan (all decks, no PowerPoint, no edits)
`qa_evidence/02_inset_aware_scan_all_decks_BEFORE.csv`: 237 filled or outlined text boxes in the four candidate decks, using native text bounds (NP01 sweep) plus the slide XML insets. **Exactly one box has text escaping its container: Part B slide 30 `Text 3`.** Part C slide 77's two boxes (`Text 20`, `Text 21`) lack 4.7 / 5.7 pt of bottom padding but keep their text 2.3 / 1.8 pt *inside* the box: the existing P3 (NP01-F08), not a new finding.
