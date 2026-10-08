# 10 · Arabic / Bilingual PDF Status (Owner decision D8) — carried forward

**Status: INTERNAL WORKING ONLY.** Conservative rule. Candidate; unapproved. VAL-07, VAL-08 and VAL-15 stay **OPEN**.

## 1. Internal working use — ALLOWED, with conditions
DOCX letterhead files and review PDFs that contain Arabic or bilingual text may be used **internally** if **every** page is marked:
- **WORKING APPLICATION / PENDING VALIDATION**, and
- **PENDING LOCALIZATION APPROVAL**,

and the documented limitations travel with the file (see §3). Internal use means review, drafting and internal circulation. It is not issue to a guest, supplier, partner, regulator or any external party.

## 2. External issue — BLOCKED until all native tests pass
No Arabic or bilingual DOCX/PDF may be issued externally until each of the following has a recorded passing native test:

| # | Gate | State today |
|---|---|---|
| 1 | Arabic linguistic QA by a qualified Arabic reviewer (M01, M11, M16; every Arabic string is a working layout string) | NOT DONE |
| 2 | Windows Word | NOT TESTED |
| 3 | Word Online, where that route is used | NOT TESTED |
| 4 | Acrobat Unicode text layer | NOT TESTED |
| 5 | Searchable and selectable Arabic | PASS in macOS PDFKit only; Word-for-Mac export FAILS (R03-03); generic extractors FAIL (LH03) |
| 6 | Copy/paste fidelity | As row 5 |
| 7 | Tagged PDF | Tag flag present on the packaged PDFs; structure quality NOT TESTED |
| 8 | Reading order | NOT TESTED |
| 9 | Screen reader / assistive technology (VoiceOver, NVDA, JAWS, Acrobat Read Aloud) | NOT TESTED |
| 10 | Accessibility QA (VAL-08, VAL-15) | NOT DONE |
| 11 | Final localization approval (AC10, VAL-07) | NOT GIVEN |

Until then the status of every Arabic/bilingual PDF route is **INTERNAL WORKING ONLY** (see `18_qa_evidence/10_Arabic_PDF_Test_Matrix.csv`).

## 3. Documented limitations (must accompany internal files)
- **R03-03:** Word for Mac "Save as PDF" looks right but its Arabic text layer is unusable (isolated presentation-form glyphs out of order). **Do not use that route** for Arabic/bilingual PDFs.
- **LH03:** The packaged PDFs (LibreOffice export plus ToUnicode/ActualText repair) pass native PDFKit copy/search (391 whole-line, 20 search-equivalent, 2 QA-only long-ID failures) but pypdf, poppler and pdfplumber reorder or omit Arabic fragments (e.g., Arabic first page exact lines: pypdf 4/14, pdftotext 9/14, pdfplumber 1/14, PDFKit 12/14).
- **R03-04:** phone numbers and Latin IDs typed *into Arabic text runs* reorder in native Word.
- **R03-06:** the Arabic date-numeral convention (Latin 0–9 or Arabic-Indic) is not signed off.
- Footers are 9 pt (LH08): digital choice, not an approved stationery minimum.

## 4. What this rule does not do
It does not approve any PDF route, any Arabic string, the Arabic system, or any letterhead for external use; it does not close VAL-07/08/15 or AC10; it does not authorize release (AC20 OPEN). No test was claimed that was not performed: Windows Word, Word Online, Acrobat and assistive-technology rows are NOT TESTED.

## 5. Re-evaluation
A passing native record for all eleven gates, filed with the QA package, is the evidence the owner needs to lift the block.

## R1
Unchanged. **Internal working use: permitted with explicit working / pending labels. External Arabic or bilingual PDF issue: BLOCKED** until native validation passes. Still required: native Arabic QA, Windows Word, Word Online, Acrobat Unicode text layer, search / select / copy-paste, tagged PDF, reading order, screen reader / AT, accessibility QA. VAL-07, VAL-08 and VAL-15 remain open. R1 did not alter any Arabic text; its only Arabic-adjacent change is the Part B slide 12 weight wording (Arabic remains PENDING VALIDATION / PENDING LOCALIZATION APPROVAL).
