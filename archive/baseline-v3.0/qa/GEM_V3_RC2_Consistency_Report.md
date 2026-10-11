# GEM™ V3.0 RC2 — Automated Consistency Report

Inputs: A = `01_working/A-RC2.pptx` (RC2), C = `01_working/C-RC2.pptx` (RC2), B = `00_originals/GEM_Digital_Design_System_V3.0_1.pdf` (**unchanged review PDF; no editable source**). Checks run over slide text, tables and speaker notes (A, C) and page text (B).

**Result: 101 PASS · 9 FAIL · 3 INFO.** Every FAIL on Part B is expected until its source is regenerated per `PartB_RC2_Exact_Patch_Spec.md`; FAILs on A or C would block RC2 and there are 0.

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
| Version string 'V3.0 RC2' present | A | PASS | pages/slides [1, 2, 3, 4, 6, 7, 10, 12, 13, 14, 15, 16] |
| Document ID present | A | PASS | pages/slides [1, 79] |
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
| Tier status CONDITIONAL · AC03 / VAL-01 (A, C) | A | PASS | pages/slides [60] |
| No invented production values (Pantone/CMYK/ΔE numbers) | A | PASS | none |
| No evidence gate marked complete | A | PASS | none · release-precondition lists ('… closed' before release) excluded |
| Primary tagline present | B | PASS | pages/slides [10] |
| Secondary line present (A, B) / absent (C by design) | B | PASS | pages/slides [2] |
| Palette #12171D | B | PASS | pages/slides [2, 41] |
| Palette #BCACA7 | B | PASS | pages/slides [3, 41, 47] |
| Palette #020202 | B | PASS | pages/slides [3, 41, 47] |
| Palette #FFFFFF | B | PASS | pages/slides [3, 41, 47] |
| Type family named: Jost | B | PASS | pages/slides [10, 11, 12, 40] |
| Type family named: Inter | B | PASS | pages/slides [2, 8, 10, 11, 12, 17, 23, 40, 62, 72] |
| Type family named: Noto Sans Arabic | B | PASS | pages/slides [10, 12, 40] |
| Prohibited: 'Jost light' / 'Jost Light' / Jost 300 | B | PASS | none |
| Legacy fonts only as legacy/reference | B | PASS | none · any mention must sit in a legacy/reference sentence |
| Stale: 'not yet issued' | B | FAIL | pages/slides [3] |
| Stale: 'still to come' | B | PASS | none |
| Stale: 'Production Standards not issued' | B | FAIL | pages/slides [43] |
| Stale: 'Release Candidate 1' as current edition | B | PASS | none |
| Version string 'V3.0 RC2' present | B | FAIL | none |
| Document ID present | B | FAIL | none |
| Status term APPROVED | B | PASS | pages/slides [2, 5, 10, 17, 22, 28, 30, 37, 41, 74] |
| Status term CONDITIONAL | B | PASS | pages/slides [2, 5, 11, 17, 18, 22, 23, 28, 30, 33, 35, 37] |
| Status term PENDING VALIDATION | B | PASS | pages/slides [2, 5, 10, 12, 14, 16, 23, 28, 33, 45, 59, 74] |
| Status term REFERENCE | B | PASS | pages/slides [2, 5, 37, 38, 74] |
| Authority order: register first, then Part A/B/C, formal standards, historical, benchmarks | B | FAIL | none |
| Domain-ownership note | B | FAIL | none |
| Twelve-role governance list (register names) | B | PASS | pages/slides [6] |
| Bilingual default: Arabic leads/first by default (S07) | B | PASS | pages/slides [14] |
| No 'project-specific' language-lead rule | B | PASS | none |
| File naming X12 pattern | B | FAIL | none |
| Old naming pattern absent | B | PASS | none |
| Gate IDs VAL-02 / VAL-07 / AC20 present | B | PASS | pages/slides [45] |
| Six-level packaging hierarchy (T05) | B | FAIL | none |
| 'Seven levels' absent | B | PASS | none |
| Tier status CONDITIONAL · AC03 / VAL-01 (A, C) | B | PASS | none |
| No invented production values (Pantone/CMYK/ΔE numbers) | B | PASS | none |
| No evidence gate marked complete | B | PASS | none · release-precondition lists ('… closed' before release) excluded |
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
| Version string 'V3.0 RC2' present | C | PASS | pages/slides [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13] |
| Document ID present | C | PASS | pages/slides [1, 77] |
| Status term APPROVED | C | PASS | pages/slides [1, 3, 10, 23, 56, 57, 69, 73, 76] |
| Status term CONDITIONAL | C | PASS | pages/slides [3, 27, 56, 57, 60, 69, 73] |
| Status term PENDING VALIDATION | C | PASS | pages/slides [3, 13, 15, 17, 35, 41, 57, 68, 69, 73, 75] |
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
| Tier status CONDITIONAL · AC03 / VAL-01 (A, C) | C | PASS | pages/slides [27] |
| No invented production values (Pantone/CMYK/ΔE numbers) | C | PASS | none |
| No evidence gate marked complete | C | PASS | none · release-precondition lists ('… closed' before release) excluded |
| Fonts used in deck (A) | A | PASS | Inter, Jost, Noto Sans Arabic |
| Fonts used in deck (C) | C | PASS | Inter, Jost |
| PDF export tagged | A | PASS | Tagged: True |
| PDF embedded fonts | A | INFO | DejaVuSans, Inter-Regular, Jost-Regular, NotoSansArabic-Regular |
| PDF export tagged | C | PASS | Tagged: True |
| PDF embedded fonts | C | INFO | Inter-Regular, Jost-Regular |
| PDF export tagged | B | FAIL | Tagged: False |
| PDF embedded fonts | B | INFO | DejaVuSans, Inter-Regular, Jost-Regular |
| Alt text on every picture | A | PASS | 87/87 |
| Alt text on every picture | C | PASS | 14/14 |
| Cross-doc: authority list anchor present | A/B/C | PASS | A=True B=False C=True |

## Part B failures mapped to patch entries

| Check | Patch entry |
|---|---|
| Stale 'not yet issued' / 'Production Standards not issued' | PB-04, PB-23 |
| Version string / document ID | PB-01, PB-22 |
| Authority order and domain ownership | PB-05 |
| Bilingual default cross-reference | PB-20 |
| File naming X12 | PB-26 |
| Tier status AC03 / VAL-01 | not applicable to B (no tier status stated) |
| Six-level hierarchy wording | PB-16 (B lists six levels; the phrase is added) |
| Tagged PDF, embedded fonts | PB-EXPORT |
