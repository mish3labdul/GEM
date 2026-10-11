# GEM Letterhead Change Log

## Set v1.1 Application Revision 03 • 2026-10-08 • WORKING APPLICATION / PENDING VALIDATION

New controlled derivative of Revision 02. Baseline: user-supplied `GEM_Letterhead_Set_v1.1_Application_Revision_02.zip`, SHA256 `3714344af0450c9e8bd4efc049a9c7e1ad641c897188d26153879b02205267a6`. Revision 02 was absent from GitHub when verified. It is preserved unmodified beside this revision. v1.0, governing sources, official logo/media bytes, embedded Regular font payloads and visible design are unchanged.

- **R03-01 (P1): PASS.** `word/settings.xml` in all 8 templates and 12 fixtures: removed `w:embedSystemFonts`, added `w:saveSubsetFonts`. A native Word save no longer embeds Times New Roman, Calibri, Cambria, Arial, Symbol, Courier or unused Bold/Italic faces (6.6 MB → 0.35–0.6 MB).
- **R03-02 (P1): PASS.** `word/document.xml` in Arabic and Bilingual First Page and 8 Arabic/bilingual fixtures: each Latin (`rtl=0`) run inside an RTL paragraph is bounded by U+200E LEFT-TO-RIGHT MARK (2 runs per file: date and reference). Native PDFKit search for `[DATE]`/`[REFERENCE NUMBER]`: 0 → 1 hit. Native Word date replacement no longer reverses.
- **R03-07 (P2): PASS.** Arabic/Bilingual Continuation placeholder `[نص الصفحة التالية]` → `«نص الصفحة التالية»` (the set's Arabic placeholder punctuation); the published-PDF exporter dropped the ASCII brackets in that RTL run.
- **R03-08 (P2): PASS.** Footer PAGE/NUMPAGES rewritten from `w:fldSimple` to equivalent complex fields carrying the 9 pt Inter Ink run properties; published PDFs had printed the digits at 10.5 pt.
- **R03-00: metadata.** `docProps/core.xml` revision label and modified date only.
- **R03-03 (P1): FAIL / REQUIRES OWNER.** Word for Mac Save as PDF produces a non-searchable Arabic text layer. Documented in the specification and README; no DOCX fix is possible.
- **R03-04 (P2), R03-05 (P3), R03-06 (P3):** guidance and owner/localization decisions recorded; no invented wording or values.
- Specification (DOCX/PDF, still 3 pages): revision line, LRM rule, subset-font saving, Word for Mac PDF warning and provenance sentence updated by equal-length replacement.
- Regenerated: all individual PDFs, Digital/Print portfolios, QA fixture PDFs, specification PDF, visual-review sheets, technical checks, checksums and manifests. Added native Word, PDFKit, font-embedding and Rev03 evidence. Revision 02 evidence records retained under `04_qa/evidence/rev02_record/`.
- LH03 remains **FAIL** for generic extractors and **PENDING** for assistive technology. LH08 remains **REQUIRES OWNER / REQUIRES SUPPLIER**.

## Set v1.1 Application Revision 02 • 2026-10-07

New controlled derivative; v1.0 is preserved. No changes to RC2 identity, governing sources, official logo/media bytes or open evidence gates.

- **LH01: PASS.** Selected corrected baseline, retained useful release edits, regenerated all companions and synchronized release copies. Original variants archived in place, not overwritten.
- **LH02: PASS / PENDING PLATFORM RETEST.** Inter LTR identifiers remain whole; Executive subject is Jost Regular; fresh exports use only Inter/Jost/Noto Regular. Specification theme-font inheritance also removed after the final check detected an unintended substitute. No active substitute or synthetic Bold observed. Native Word platform matrix pending.
- **LH03: FAIL REMAINING / PENDING ACCESSIBILITY ACCEPTANCE.** Repaired omitted Arabic combining-mark ToUnicode entries from exporter ActualText, corrected base/mark cluster allocation, and preserved logical source paragraph ActualText. Pypdf layout and pdfplumber independently match the complete Arabic glyph inventory; semantic source paragraphs match DOCX. Generic plain extraction still reverses/omits mixed RTL fragments. This finding is not closed. Native copy/search and AT must pass before controlled real-world PDF use.
- **LH04: PASS / PENDING PLATFORM RETEST.** Separated date and reference into editable lines; full technical ID uses one explicit Inter LTR run. Short/long codes render in correct bracket order. Email/URL/phone test fields are fixtures only, never company details.
- **LH05: PASS / PENDING NATIVE RETEST.** Selected robust live PAGE/NUMPAGES fields with 9 pt Inter formatting. One-page templates and 2/3-page explicit/automatic-flow fixtures show correct page values in the bundled renderer. No incomplete Page of output.
- **LH06: PASS.** Working and localization status retained in all first/default footers of Arabic and bilingual templates, including automatic continuations.
- **LH07: PASS.** Selected corrected Jost Regular tagline at 10.5 pt, 38 twips (~0.181em). Body and Arabic have zero expanded tracking.
- **LH08: PENDING / REQUIRES OWNER / REQUIRES SUPPLIER.** Raised essential footer/status and SAMPLE CONTENT to 9 pt; footer explicitly 12.6 pt exact leading. Visual/grayscale review passed with no collision. This is a working digital application choice, not a newly approved stationery/physical minimum. Owner digital legibility and supplier print proof remain required.
- **LH09: PASS / PENDING NATIVE RETEST.** Selected clean editable corrected source and discarded corrupt release re-save structures while preserving originals. No unintended clipboard-like symbol appears in fresh exports. Exact original renderer/add-in cause is not asserted.
- **LH10: PASS / PENDING RIGHTS ACCEPTANCE.** Preserved three valid Regular-only font payloads from the corrected candidate. Every payload decoded as a usable TTF with cmap; decoded hashes recorded. No zero-byte embedded parts. Acceptance/licence gate remains open.

Additional synchronized output controls: logical PDF paragraph text and vector-logo alternatives; merged tag/parent-tree preservation; matching specification; no verified author attribution; source dates/reconciliation/asset/font register; fresh checksums.
