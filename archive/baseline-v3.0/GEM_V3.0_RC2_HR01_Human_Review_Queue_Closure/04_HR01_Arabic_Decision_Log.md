# 04 · HR01 — Arabic Decision Log

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
This log records linguistic decisions only. It does not close VAL-07, AC10 or VAL-15 and it contains no Arabic text (item IDs and SHA-256 prefixes only; the approved wording lives in the candidate files).

## Reviewer and method
- Reviewer: Mashal, Native Arabic Reviewer / Localization Lead (OD-G09). Dispositions were stated by the session user as Mashal. No account, Git identity or Brand Owner link is recorded.
- Claude's suggestions were labelled "non-native" and were advisory. Where no problem was seen the entry said "no change suggested". Each disposition was an explicit choice by the reviewer, in batches of related items; one decision governed identical repeats and every item is recorded separately in `03_HR01_Arabic_Review_Register.csv`.
- Source: the OD01 Arabic review queue (44 items; same population as the AR01 queue). Wording was read from the latest controlled candidates (AX01 PowerPoint candidates; Revision 03 Word templates, byte-identical to the AX01 baseline).

## Decisions
| Batch | Items | Disposition | Effect on the candidates |
|---|---|---|---|
| 1 Slides | AR-01, 02, 04 welcome string; AR-05, 06, 08, 09, 10, 12 | APPROVE AS IS | none |
| 1 Slides | AR-03 tile heading (pairs with the English "ENGLISH-FIRST") | APPROVE CLAUDE RECOMMENDATION | Part A slide 38 heading revised |
| 1 Slides | AR-07, AR-11 language placeholder | APPROVE CLAUDE RECOMMENDATION | Part A slides 65 and 68 revised (consistent with the language name used on slide 66) |
| 2 Letter | AR-16 / 32 subject (English adds "product") | APPROVE CLAUDE RECOMMENDATION | Arabic First Page and Bilingual First Page |
| 2 Letter | AR-17 / 33 salutation | APPROVE CLAUDE RECOMMENDATION | Arabic First Page and Bilingual First Page |
| 2 Letter | AR-19 / 25 sample disclaimer (meaning drift against the English) | APPROVE CLAUDE RECOMMENDATION | Arabic First Page and Arabic Continuation |
| 2 Letter | AR-20 / 26 / 35 / 40 closing | APPROVE CLAUDE RECOMMENDATION | all four Word templates |
| 3 Letter set | 18 repeated items (date, reference, recipient block, body paragraph, signature, signatory) and AR-23 / 38 continuation placeholder | APPROVE AS IS | none |
| 3 Policy | AR-43 tagline | Tagline stays English only (rule: Part B slide 3, Part C slide 17; brand approval M10 not requested) | none |
| 3 Policy | AR-44 numerals | Western digits (0-9) for guest-facing Arabic copy, dates and page labels; technical IDs stay Latin (OD-G07) | none |
| 4 Functional labels (extras, OD-G06) | X01 page label | Localized, live PAGE/NUMPAGES fields kept | 6 footer parts in 4 templates |
| 4 | X02 working markers; X03 contact initials | Keep as they are (English markers are removed at release; placeholders) | none |
| 4 | X04 Arabic strings inside the Part D images | CONCEPT ONLY — wording NOT approved | none |

Totals for the 44 queue items: **31 approved as is, 13 approved as Claude recommendation, 0 revised by reviewer wording, 0 deferred, 0 not applicable, 0 remaining.**

## Preserved
AR01 direction and ar-SA metadata, Latin/LTR technical identifiers, Noto Sans Arabic 400 interim typography, geometry, no Arabic tracking, no font change. The edits replace text inside existing runs only.

## What this does not do
- It is not a brand approval of any wording. The Arabic tagline question (M10) was not raised for approval.
- It does not approve the Arabic text inside the Part D images.
- VoiceOver results SR-06, SR-07 and SR-10 are technical accessibility observations and are not linguistic approval.
- AC10 (a Brand Owner decision) and VAL-07 (needs continuous production layouts with real content, Windows/Word Online evidence and the other conditions) remain open.
