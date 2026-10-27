# GEM Business Stationery Working Suite

**Status: WORKING TEMPLATE SET / INTERNAL REVIEW ONLY. Not approved for external issue.**

Four editable A4 Word templates and matching PDF review previews are provided. The Word files are the working masters; replace each bracketed field before use. Item tables can be extended in Word by adding rows.

| Template | Editable Word file | PDF review preview |
|---|---|---|
| Request for Quotation | GEM_Request_for_Quotation_Template_working.docx | GEM_Request_for_Quotation_Template_working.pdf |
| Quotation and Proposal | GEM_Quotation_Proposal_Template_working.docx | GEM_Quotation_Proposal_Template_working.pdf |
| Invoice | GEM_Invoice_Template_working.docx | GEM_Invoice_Template_working.pdf |
| Purchase Order | GEM_Purchase_Order_Template_working.docx | GEM_Purchase_Order_Template_working.pdf |

**Letterhead:** this suite does not include its own letterhead. Use the existing GEM Letterhead Set v1.1 Application Revision 03 (English, Arabic and bilingual First Page and Continuation files) in `archive/baseline-v3.0/GEM_Letterhead_Set_v1.1_Application_Revision_03/05_release/`. That set carries its own open acceptance items (LH03, LH08, R03-03, D8); they apply here too.

## Design and source

The forms inherit the letterhead set's masthead and settings: the supplied V3.0 horizontal ink logo at 32 mm (embedded directly in each Word file), the fixed tagline on the first page, a quiet continuation header, 25 mm side margins (160 mm writing width), Inter Regular for body and metadata at 9 pt, Jost Regular for titles and headings, Noto Sans Arabic Regular for Arabic (labels 10 pt), and a Beige hairline footer rule. Colours are the approved Ink #12171D, Beige #BCACA7 and White #FFFFFF. Beige and Ink appear only as rules; there are no colour fills except the Ink header row of each item table. No bold weights are used. Page size is A4.

**Forms exceptions, for owner acceptance** (not approved by this suite):

- The vertical frame is more compact than the letterhead set: bottom margin 25 mm instead of 37 mm, and a two-line footer (address, contact placeholders and page number; working and issue status) instead of up to four lines. The letterhead set specifies a bottom margin of 37 mm for its four-line zone.
- The Ink fill on the item-table header row is a small departure from the letterhead set's "no background flood" rule.
- Labels are English first with Arabic beneath. The letterhead set places Arabic first in bilingual documents; applying either hierarchy to forms is a proposed application that requires owner approval.
- The footer status line is shortened to fit one line: "WORKING APPLICATION / PENDING VALIDATION · EXTERNAL ISSUE RESTRICTED (D8 PENDING)". The letterhead set's separate "PENDING LOCALIZATION APPROVAL" line is not repeated.

English and Arabic labels are included to support bilingual completion. Arabic wording is a working translation and needs review by the owner and a qualified Arabic-language reviewer, including the labels added to the forms in this revision. Preview PDFs were exported with Jost Regular, Inter Regular and Noto Sans Arabic Regular, which are byte-identical to the font files in the letterhead set's `00_source/fonts/`; the PDFs embed the fonts used. The editable Word files refer to font names and do not embed the typefaces, so the editing computer must have those fonts available to preserve the layout.

## Fields still requiring confirmation

- The legal or registered entity name, postal and billing addresses, telephone number, email and transaction contacts remain editable placeholders. The footer uses the letterhead set's `[ADDRESS]`, `[T]`, `[E]`, `[W]` placeholders; no real contact value is printed.
- The owner record of 26 October 2026 describes contact@mish3l.com as a tested contact address. Its use on commercial stationery still needs confirmation alongside the open L09 business-contact facts, so it is not printed in these templates.
- Currency, tax registration identifiers, applicable tax name and rate, bank and beneficiary details, payment terms, delivery terms, and quote validity values are placeholders. No rate, account detail, address, or jurisdiction-specific legal wording has been supplied or inferred. Confirm with GEM's accountant whether an Invoice in this form satisfies the tax-invoice rules of the issuing jurisdiction.
- The Arabic and bilingual external-issue gate D8 remains open in the V3.0 document records. Keep this set internal until owner and native-language review is complete; confirm the legal, tax, payment, and commercial fields before issuing any document.

The purchase-order authorization fields are workflow placeholders only. This suite supplies no contract terms, warranty promise, tax calculation, or claim about a registered legal entity.

## Remove before issue

Each file carries internal-review markings that must be removed or replaced by the owner once the gates above are cleared, and not before: the footer status line, the "TEMPLATE 0x" kicker above each title, the `[REFERENCE NUMBER]` continuation header, and every bracketed placeholder.

## Rebuild and verification

Run `node build.mjs` from this directory to rebuild the four Word files from the source in the repository's archived V3.0 brand asset kit. Run `bash export-pdf.sh` to regenerate the four PDF previews from the Word files with LibreOffice. The script copies the three Regular font files from `FONT_DIR` (default `~/Library/Fonts`) into a throwaway LibreOffice profile, so the PDFs embed those exact fonts. After either step, regenerate `SHA256SUMS.txt`. PDF checksums are not reproducible across exports because LibreOffice stamps creation times.

Checked in LibreOffice only: the four DOCX files open and export, and every PDF page was rendered and inspected for layout, logo size and placement, tagline, placeholder visibility, repeated table headers, page breaks, right-aligned Arabic text and the footer. Each form runs to two pages. `pdffonts` shows only Jost Regular, Inter Regular and Noto Sans Arabic Regular, all embedded. Text extraction found Arabic characters and no replacement glyphs. Arabic paragraphs use logical (`start`/`end`) alignment as the letterhead set does; that set was tested in Word for Mac, this suite was not. Not checked: native Microsoft Word (including separator paragraphs, keep-with-next chains and fonts missing from the editing computer), physical printing, accessibility, legal, tax, or owner acceptance.
