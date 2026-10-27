# GEM Business Stationery Working Suite

**Status: WORKING TEMPLATE SET / INTERNAL REVIEW ONLY. Not approved for external issue.**

Five editable A4 Word templates and matching PDF review previews are provided. The Word files are the working masters; replace each bracketed field before use. Item tables can be extended in Word by adding rows.

| Template | Editable Word file | PDF review preview |
|---|---|---|
| Business letterhead | GEM_Business_Letterhead_Template_working.docx | GEM_Business_Letterhead_Template_working.pdf |
| Request for Quotation | GEM_Request_for_Quotation_Template_working.docx | GEM_Request_for_Quotation_Template_working.pdf |
| Quotation and Proposal | GEM_Quotation_Proposal_Template_working.docx | GEM_Quotation_Proposal_Template_working.pdf |
| Invoice | GEM_Invoice_Template_working.docx | GEM_Invoice_Template_working.pdf |
| Purchase Order | GEM_Purchase_Order_Template_working.docx | GEM_Purchase_Order_Template_working.pdf |

## Design and source

The templates use the supplied V3.0 horizontal ink logo, embedded directly in each Word file, and the approved Ink #12171D, Beige #BCACA7, and White #FFFFFF palette. Jost is used for display headings, Inter for Latin text, and Noto Sans Arabic for Arabic labels. Page size is A4. Page numbers appear in the footer.

English and Arabic labels are included to support bilingual completion. Arabic wording is a working translation and needs review by the owner and a qualified Arabic-language reviewer. Preview PDFs were exported with the exact Jost, Inter, and Noto Sans Arabic fonts; the PDFs embed the fonts used. The editable Word files refer to font names and do not embed the typefaces, so the editing computer must have those fonts available to preserve the layout.

## Fields still requiring confirmation

- The legal or registered entity name, postal and billing addresses, telephone number, and transaction contacts remain editable placeholders.
- contact@mish3l.com is included from the owner record as a tested contact address on 26 October 2026. Its use on commercial stationery still needs confirmation alongside the open L09 business-contact facts.
- Currency, tax registration identifiers, applicable tax name and rate, bank and beneficiary details, payment terms, delivery terms, and quote validity values are placeholders. No rate, account detail, address, or jurisdiction-specific legal wording has been supplied or inferred.
- The Arabic and bilingual external-issue gate D8 remains open in the V3.0 document records. Keep this set internal until owner and native-language review is complete; confirm the legal, tax, payment, and commercial fields before issuing any document.

The purchase-order authorization fields are workflow placeholders only. This suite supplies no contract terms, warranty promise, tax calculation, or claim about a registered legal entity.

## Remove before issue

Each file carries internal-review markings that must be removed or replaced by the owner once the gates below are cleared, and not before: the header label "INTERNAL REVIEW DRAFT" and its Arabic line, the "TEMPLATE 0x" kicker above each title, and every bracketed placeholder. The footer contact line and its Arabic line are placeholders too.

## Rebuild and verification

Run `node build.mjs` from this directory to rebuild the five Word files from the source in the repository's archived V3.0 brand asset kit. Run `bash export-pdf.sh` to regenerate the five PDF previews from the Word files with LibreOffice. The script copies Jost, Inter and Noto Sans Arabic (Regular and Bold) from `FONT_DIR` (default `~/Library/Fonts`) into a throwaway LibreOffice profile, so the PDFs embed those exact fonts. After either step, regenerate `SHA256SUMS.txt`. PDF checksums are not reproducible across exports because LibreOffice stamps creation times.

Checked in LibreOffice only: the five DOCX files open and export, and every PDF page was rendered and inspected for layout, logo placement, placeholder visibility, repeated table headers, page breaks, right-aligned Arabic text and the bilingual footer. `pdffonts` shows only Jost, Inter and Noto Sans Arabic, all embedded. Text extraction found Arabic characters and no replacement glyphs. Not checked: native Microsoft Word (including how it handles the separator paragraphs, keep-with-next chains and fonts missing from the editing computer), physical printing, accessibility, legal, tax, or owner acceptance.
