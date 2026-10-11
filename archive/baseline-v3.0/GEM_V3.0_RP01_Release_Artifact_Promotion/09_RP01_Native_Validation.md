# 09 · RP01 — Native Validation (macOS)

**GEM™ V3.0 — OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE — FORMAL DEFERRALS RECORDED — ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY**
AC20: AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS (FA01). RP01 promotes release-state labels only; no gate is closed.

Native validation was run on scratch copies of the promoted files (never on the files in this package, so no Office lock files were created here). It is macOS PowerPoint and macOS Word only: Windows Word, Word Online, Acrobat, NVDA and JAWS were not tested and **a native macOS pass does not satisfy D8**.

## PowerPoint
| Deck | Opened natively | Repair prompt | Slides | Notes |
|---|---|---|---|---|
| Part A (80 slides) | yes | none | 80 | cover shows the promoted wording |
| Part B (35 slides) | yes | none | 35 | Accessibility Assistant opened (see below) |
| Part C (78 slides) | yes | none | 78 | cover shows V3.0 and PENDING PRODUCTION VALIDATION |
| Part D (24 slides) | yes | none | 24 | cover shows V3.0 and CONCEPT / NOT PRODUCTION ARTWORK |

No missing-font or missing-media dialog appeared for any deck.

**Accessibility (native).** PowerPoint's Accessibility Assistant was run on the promoted Part B and, for comparison, on the HR01 source Part B. The two results are identical: every rule category (text contrast, missing alt text, missing audio/video subtitles, missing table header, merged or split cells, missing slide title, duplicate slide title, default and duplicate section name, restricted access) reports no violations; the only count shown is "Check reading order: 35", PowerPoint's manual-review advisory (one per slide, 35 slides). The panel's headline reads "Keep going!" only because that advisory remains. Each category was opened for Part B and states "no accessibility violations for this rule". The first RP01 pass mis-described this panel as still updating; that was wrong and is corrected here. FA01 `10` records the older checker wording "no missing alt text or title" for Part B; the two records agree in substance (no alt-text, title or table violations); the Assistant is a newer panel that also lists categories the older rule did not. The native Assistant was not run on Parts A, C and D; for those the position rests on the AX01 static predicates (recomputed, identical to source) and the structural identity proof in `16_qa/rp01_preservation.csv`. No new accessibility conformance claim is made.

**Native layout check of the changed slides.** After the LibreOffice review, the changed slides were viewed natively in PowerPoint (which uses the installed Jost and Inter fonts and wraps differently): Part A slides 1, 72, 78, 79, 80; Part B 1, 30 (build check), 31, 33, 34; Part C 1, 75, 76, 77; Part D 1, 22, 23, 24. Three native overflows were found in the first build (A79 change-log line wrapping into the footer, B33 version-history heading wrapping into the next paragraph, C77 edition-state cell wrapping to its border) and fixed by shortening the new text; the chain was re-run and those slides were re-checked natively. Pages not listed were not viewed natively (their changes are a running-header word removal or a shorter replacement).

## Word
| Template | Opened | Repair prompt | Fields | Accessibility Assistant |
|---|---|---|---|---|
| English First Page | yes | none | standard update-fields prompt declined | Looks good, no issues |
| English Continuation | yes | none | as above | Looks good, no issues |
| Executive | yes | none | as above | Looks good, no issues |
| Minimal | yes | none | as above | Looks good, no issues |
| Arabic First Page | yes | none | as above | Looks good, no issues |
| Arabic Continuation | yes | none | as above | Looks good, no issues |
| Bilingual First Page | yes | none | as above | Looks good, no issues |
| Bilingual Continuation | yes | none | as above | Looks good, no issues |

The update-fields prompt is Word's standard prompt for templates holding PAGE and NUMPAGES fields; it was declined so nothing was altered. The Arabic First Page footer was viewed natively: the three lines (both D8 markings plus the restriction line) fit inside the page below the rule with no collision. Arabic text, RTL and the logo are unchanged (byte-identical parts).

## Not done
Native PowerPoint checker counts for Parts A, C and D; Windows; PDF/Acrobat; screen readers (no new VoiceOver pass was run, because no structure changed).
