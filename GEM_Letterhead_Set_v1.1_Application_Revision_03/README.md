# GEM Branded Letterhead Set v1.1

Application Revision 03 • 8 October 2026

**WORKING APPLICATION / PENDING VALIDATION**

Eight editable Word templates (English, Arabic and bilingual First Page plus Continuation, Executive, Minimal), matching individual PDFs, eight-page Digital/Print sample portfolios, a three-page specification, QA report, change log, asset/source register, checksums and evidence. It derives from Revision 02, which was supplied as a package and was not on GitHub. Revision 02 and v1.0 are preserved unchanged. This package does not authorize production or owner release.

## What changed from Revision 02

- **Native Word save is controlled.** Word no longer embeds unused Office/system fonts (Times New Roman, Calibri, Cambria, Arial …) when a user saves a letter (R03-01). A saved letter stays at about 0.4–0.6 MB instead of 6.6 MB.
- **Identifiers inside Arabic paragraphs stay in order.** Date and reference placeholders are bounded by invisible U+200E marks, so copy/search and Word replacement keep `[DATE]`, `[REFERENCE NUMBER]` and real dates/codes left to right (R03-02, Register M12).
- **Published PDFs print correctly.** Page numbers now match the 9 pt footer (R03-08), and the Arabic continuation placeholder keeps its marks: `«نص الصفحة التالية»` (R03-07).
- Logo bytes, fonts, styles, margins, layout and live field codes are unchanged.

## Start here

- `05_release/`: synchronized distribution candidate. Eight DOCX templates, the specification DOCX/PDF, all matching PDFs and control records.
- `01_templates/`: canonical editable templates; exact copies in release.
- `02_pdf/`: validated sample exports (sample correspondence, not fillable forms).
- `03_specs/`: specification, asset/source register, change log.
- `04_qa/`: QA report, findings disposition, fixtures (QA ONLY; reserved dummy contacts) and evidence. Includes `native_word/` (Microsoft Word for Mac tests), `PDFKit_Native_Extraction.json`, `Rev03_Checks.json`, `visual_review/`, and Revision 02's own records in `rev02_record/`.
- `00_source/`: governing snapshot, Revision 02 scripts and, in `rev03/`, the Revision 03 replay scripts.

## Using the templates

1. Start every letter from a **First Page** file. Later pages pick up the continuation header and footer automatically. The Continuation files are companions.
2. Replace SAMPLE CONTENT and every field, including the reference in the continuation header and the contact placeholders in both footers. In Arabic paragraphs, replace only the text inside the brackets, so the invisible direction marks remain.
3. Use Latin 0–9 for codes, phone numbers, URLs and references (M11). Keep identifiers in the reference/footer fields rather than typing them into Arabic sentences. The Arabic date numeral convention is not yet signed off.
4. Let long text flow; never shrink type to save a page. Update PAGE/NUMPAGES before export.
5. **PDF export:** Word for Mac *Save as PDF* currently produces Arabic text that looks right but cannot be searched or copied. Do not send Arabic or bilingual PDFs made that way until copy/search is checked. The packaged PDFs use a separately validated export and repair step. Every completed letter needs its own check.

## Open acceptance items

- **LH03:** generic PDF extractors still reorder Arabic. Native macOS copy/search passes for all template content. Assistive-technology testing has not been done.
- **LH08:** the 9 pt footer/status and its tracking need Brand Owner acceptance and a supplier physical proof.
- **R03-03:** an approved PDF export route for Arabic/bilingual letters requires owner decision and testing (Word online accessibility export, Windows Word, Acrobat).
- Also open: Windows/Online Word, localization approval of all Arabic strings, logo/font master and rights acceptance, prepress/CMYK/stock (REQUIRES SUPPLIER; nothing invented) and AC20 owner authorization.

Do not describe this set as Approved, production-ready or commercially print-ready.

## Reproduction

`00_source/rev03/` contains the exact Revision 03 steps: `rev03_fixes.py` (DOCX corrections), `render.py` (LibreOffice export with the verified fonts), `pdf_fix.py` (ToUnicode/ActualText/Figure/portfolio repair, from Revision 02), `proof.py`, `spec.py`, `verify.py`, `extra_checks.py`, the native Word harness `wtest.py`/`wanalyze.py`, and the PDFKit checker `pk.swift`/`pkcheck2.py`. The paths refer to this workstation's runtime and font configuration. They are replay evidence, not an installed application.
