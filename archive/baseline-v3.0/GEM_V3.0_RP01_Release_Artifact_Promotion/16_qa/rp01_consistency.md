# GEM™ V3.0 — Automated Consistency Assertions (promoted A · B · C) — RP01 successor reporting

**Result: 112 AUTOMATED ASSERTIONS PASSED · 0 FAILED · 0 INFO records.**

This is **not** a confirmation of full system consistency. Each assertion is a text/term/metadata check (term present, stale phrase absent, PDF tagged flag, picture alt-text count, authority-list anchor). It does not test meaning, visual rendering, runtime behaviour or native-application behaviour. See `09_Consistency_Coverage_Report.md` for what is automated, manually verified, inherited or not tested.

Inputs: the RP01 promoted Part A, Part B and Part C PPTX files (see 07_RP01_Release_File_Index.csv). No PDFs are promoted, so the PDF export checks of the original are removed.

| Check | Doc | Result | Detail |
|---|---|---|---|
| Primary tagline present | A | PASS | pages/slides [1, 23, 24, 36, 77, 80] |
| Secondary line present (A, B) / absent (C by design) | A | PASS | pages/slides [6, 23] |
| Palette #12171D | A | PASS | pages/slides [32] |
| Palette #BCACA7 | A | PASS | pages/slides [32] |
| Palette #020202 | A | PASS | pages/slides [32] |
| Palette #FFFFFF | A | PASS | pages/slides [32] |
| Type family named: Jost | A | PASS | pages/slides [17, 23, 24, 34, 35, 77] |
| Type family named: Inter | A | PASS | pages/slides [15, 17, 35, 37, 41, 54, 77] |
| Type family named: Noto Sans Arabic | A | PASS | pages/slides [37] |
| Prohibited: 'Jost light' / 'Jost Light' / Jost 300 | A | PASS | none |
| Legacy fonts only as legacy/reference | A | PASS | none · any mention must sit in a legacy/reference sentence |
| Stale: 'not yet issued' | A | PASS | none |
| Stale: 'still to come' | A | PASS | none |
| Stale: 'Production Standards not issued' | A | PASS | none |
| Stale: 'Release Candidate 1' as current edition | A | PASS | none |
| Running header no longer carries the RC2 label | A | PASS | none |
| Version string 'V3.0' present | A | PASS | pages/slides [1, 2, 3, 4, 6, 7, 10, 12, 13, 14, 15, 16] |
| Document ID present (promoted form, no -RC2) | A | PASS | pages/slides [1, 79] |
| Status term APPROVED | A | PASS | pages/slides [4, 16, 73] |
| Status term CONDITIONAL | A | PASS | pages/slides [4, 13, 34, 36, 50, 51, 60, 73, 75] |
| Status term PENDING VALIDATION | A | PASS | pages/slides [4, 37, 39, 51, 73, 78] |
| Status term REFERENCE | A | PASS | pages/slides [4, 8, 11, 45, 47, 48, 49, 50, 57, 58, 63, 73] |
| Authority order: register first, then Part A/B/C, formal standards, historical, benchmarks | A | PASS | pages/slides [3] |
| Domain-ownership note | A | PASS | pages/slides [3] |
| Twelve-role governance list (register names) | A | PASS | pages/slides [72] |
| Bilingual default: Arabic leads/first by default (S07) | A | PASS | pages/slides [38] |
| No 'project-specific' language-lead rule | A | PASS | none |
| File naming X12 pattern | A | PASS | pages/slides [75] |
| Old naming pattern absent | A | PASS | none |
| Gate IDs VAL-02 / VAL-07 / AC20 present | A | PASS | pages/slides [78] |
| Six-level packaging hierarchy (T05) | A | PASS | pages/slides [61, 79] |
| 'Seven levels' absent | A | PASS | none |
| Tier status CONDITIONAL · AC03 / VAL-01 | A | PASS | pages/slides [60] |
| No invented production values (Pantone/CMYK/ΔE numbers) | A | PASS | none |
| No evidence gate marked complete | A | PASS | none · release-precondition checklist lines ('VAL-xx closed' as a condition before release) excluded |
| Primary tagline present | B | PASS | pages/slides [1, 3] |
| Secondary line present (A, B) / absent (C by design) | B | PASS | pages/slides [1, 3] |
| Palette #12171D | B | PASS | pages/slides [3, 30] |
| Palette #BCACA7 | B | PASS | pages/slides [3, 30] |
| Palette #020202 | B | PASS | pages/slides [3, 30] |
| Palette #FFFFFF | B | PASS | pages/slides [3, 30] |
| Type family named: Jost | B | PASS | pages/slides [3, 9, 29] |
| Type family named: Inter | B | PASS | pages/slides [8, 9, 18, 29] |
| Type family named: Noto Sans Arabic | B | PASS | pages/slides [9, 12, 29] |
| Prohibited: 'Jost light' / 'Jost Light' / Jost 300 | B | PASS | none |
| Legacy fonts only as legacy/reference | B | PASS | none · any mention must sit in a legacy/reference sentence |
| Stale: 'not yet issued' | B | PASS | none |
| Stale: 'still to come' | B | PASS | none |
| Stale: 'Production Standards not issued' | B | PASS | none |
| Stale: 'Release Candidate 1' as current edition | B | PASS | none |
| Running header no longer carries the RC2 label | B | PASS | none |
| Version string 'V3.0' present | B | PASS | pages/slides [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] |
| Document ID present (promoted form, no -RC2) | B | PASS | pages/slides [1, 34] |
| Status term APPROVED | B | PASS | pages/slides [2, 9, 11, 17, 21, 23] |
| Status term CONDITIONAL | B | PASS | pages/slides [2, 11, 14, 15, 17, 18, 21, 23, 25, 27, 28, 31] |
| Status term PENDING VALIDATION | B | PASS | pages/slides [2, 9, 12, 13, 17, 18, 21, 27] |
| Status term REFERENCE | B | PASS | pages/slides [2, 28] |
| Authority order: register first, then Part A/B/C, formal standards, historical, benchmarks | B | PASS | pages/slides [4] |
| Domain-ownership note | B | PASS | pages/slides [4] |
| Twelve-role governance list (register names) | B | PASS | pages/slides [5] |
| Bilingual default: Arabic leads/first by default (S07) | B | PASS | pages/slides [29] |
| No 'project-specific' language-lead rule | B | PASS | none |
| File naming X12 pattern | B | PASS | pages/slides [35] |
| Old naming pattern absent | B | PASS | none |
| Gate IDs VAL-02 / VAL-07 / AC20 present | B | PASS | pages/slides [33] |
| Six-level packaging hierarchy (T05) | B | PASS | pages/slides [27, 34] |
| 'Seven levels' absent | B | PASS | none |
| Tier status CONDITIONAL · AC03 / VAL-01 | B | PASS | pages/slides [27] |
| No invented production values (Pantone/CMYK/ΔE numbers) | B | PASS | none |
| No evidence gate marked complete | B | PASS | none · release-precondition checklist lines ('VAL-xx closed' as a condition before release) excluded |
| Primary tagline present | C | PASS | pages/slides [78] |
| Secondary line present (A, B) / absent (C by design) | C | PASS | none |
| Palette #12171D | C | PASS | pages/slides [11] |
| Palette #BCACA7 | C | PASS | pages/slides [11] |
| Palette #020202 | C | PASS | pages/slides [11] |
| Palette #FFFFFF | C | PASS | pages/slides [11] |
| Type family named: Jost | C | PASS | pages/slides [15] |
| Type family named: Inter | C | PASS | pages/slides [5, 13, 15, 19, 21, 41, 45, 50, 72] |
| Type family named: Noto Sans Arabic | C | PASS | pages/slides [15, 41] |
| Prohibited: 'Jost light' / 'Jost Light' / Jost 300 | C | PASS | none |
| Legacy fonts only as legacy/reference | C | PASS | none · any mention must sit in a legacy/reference sentence |
| Stale: 'not yet issued' | C | PASS | none |
| Stale: 'still to come' | C | PASS | none |
| Stale: 'Production Standards not issued' | C | PASS | none |
| Stale: 'Release Candidate 1' as current edition | C | PASS | none |
| Running header no longer carries the RC2 label | C | PASS | none |
| Version string 'V3.0' present | C | PASS | pages/slides [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13] |
| Document ID present (promoted form, no -RC2) | C | PASS | pages/slides [1, 77] |
| Status term APPROVED | C | PASS | pages/slides [1, 3, 10, 23, 56, 57, 69, 73, 76] |
| Status term CONDITIONAL | C | PASS | pages/slides [3, 27, 56, 57, 60, 69, 73] |
| Status term PENDING VALIDATION | C | PASS | pages/slides [3, 13, 15, 17, 35, 41, 44, 57, 68, 69, 73, 75] |
| Status term REFERENCE | C | PASS | pages/slides [3, 57, 73] |
| Authority order: register first, then Part A/B/C, formal standards, historical, benchmarks | C | PASS | pages/slides [2] |
| Domain-ownership note | C | PASS | pages/slides [2] |
| Governance roles cite the canonical register list (Part A 72) | C | PASS | pages/slides [4] |
| Bilingual default: Arabic leads/first by default (S07) | C | PASS | pages/slides [41] |
| No 'project-specific' language-lead rule | C | PASS | none |
| File naming X12 pattern | C | PASS | pages/slides [56, 73] |
| Old naming pattern absent | C | PASS | none |
| Gate IDs VAL-02 / VAL-07 / AC20 present | C | PASS | pages/slides [75] |
| Six-level packaging hierarchy (T05) | C | PASS | pages/slides [29, 77] |
| 'Seven levels' absent | C | PASS | none |
| Tier status CONDITIONAL · AC03 / VAL-01 | C | PASS | pages/slides [27] |
| No invented production values (Pantone/CMYK/ΔE numbers) | C | PASS | none |
| No evidence gate marked complete | C | PASS | none · release-precondition checklist lines ('VAL-xx closed' as a condition before release) excluded |
| Fonts used in deck (A) | A | PASS | Inter, Jost, Noto Sans Arabic |
| Fonts used in deck (B) | B | PASS | Courier New, Inter, Jost, Noto Sans Arabic · Courier New = code specimen only, flagged [REQUIRES OWNER] |
| Fonts used in deck (C) | C | PASS | Inter, Jost |
| Alt text on every picture | A | PASS | 89/89 |
| Alt text on every picture | B | PASS | 0/0 |
| Alt text on every picture | C | PASS | 14/14 |
| Cross-doc: authority list anchor present | A/B/C | PASS | A=True B=True C=True |
