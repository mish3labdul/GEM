# GEM Business Stationery Working Suite

**Status: WORKING TEMPLATE SET / INTERNAL REVIEW ONLY. Not approved for external issue.**

Four editable A4 Word templates and matching PDF review previews are provided. The Word files are the working masters; complete each content-control field (placeholder text is the field's name, such as "Legal name", shown as ordinary text) before use. Item tables can be extended in Word by adding rows, after which the Subtotal range must be updated (see `FILL-IN-GUIDE.md`).

| Template | Editable Word file | PDF review preview |
|---|---|---|
| Request for Quotation | GEM_Request_for_Quotation_Template_working.docx | GEM_Request_for_Quotation_Template_working.pdf |
| Quotation and Proposal | GEM_Quotation_Proposal_Template_working.docx | GEM_Quotation_Proposal_Template_working.pdf |
| Invoice | GEM_Invoice_Template_working.docx | GEM_Invoice_Template_working.pdf |
| Purchase Order | GEM_Purchase_Order_Template_working.docx | GEM_Purchase_Order_Template_working.pdf |

**Letterhead:** this suite does not include its own letterhead. Use the existing GEM Letterhead Set v1.1 Application Revision 03 (English, Arabic and bilingual First Page and Continuation files) in `archive/baseline-v3.0/GEM_Letterhead_Set_v1.1_Application_Revision_03/05_release/`. That set carries its own open acceptance items (LH03, LH08, R03-03, D8); they apply here too.

## Design and source

The forms inherit the letterhead set's masthead and settings: the supplied V3.0 horizontal ink logo at 32 mm (embedded directly in each Word file), the fixed tagline on the first page, a quiet continuation header, 25 mm side margins (160 mm writing width), Inter Regular for body and metadata at 9 pt, Jost Regular for titles and headings, Noto Sans Arabic Regular for Arabic (labels 10 pt), and a Beige hairline footer rule. Colours are the approved Ink #12171D, Beige #BCACA7 and White #FFFFFF. Beige and Ink appear only as rules; there are no colour fills and no cell boxes (the only boxes are the free-text entry areas). Uppercase Latin labels carry 0.08 em tracking and section headings 0.16 em, as the Part B tokens set; Arabic labels are 10.5 pt against 8 pt Latin labels (the tokens' 1.33 ratio) and are never tracked. No bold weights are used. Page size is A4.

**Forms exceptions, for owner acceptance** (not approved by this suite):

- The vertical frame is more compact than the letterhead set: bottom margin 25 mm instead of 37 mm, and a two-line footer (confirmed contact line and page number; issue restriction in English and Arabic) instead of up to four lines. The letterhead set specifies a bottom margin of 37 mm for its four-line zone.
- Labels are English first with Arabic beneath. The letterhead set places Arabic first in bilingual documents; applying either hierarchy to forms is a proposed application that requires owner approval.
- The footer status line is shortened to fit one line: "NOT FOR EXTERNAL ISSUE · غير مخصص للإصدار الخارجي · PENDING VALIDATION (D8)". The letterhead set's separate "PENDING LOCALIZATION APPROVAL" line is not repeated.
- The forms print confirmed contact facts (see below) in the footer, where the letterhead set keeps `[ADDRESS] [T] [E] [W]` placeholders. The owner confirmed these values for stationery on 30 Oct 2026.

English and Arabic labels are included to support bilingual completion. Arabic wording is a working translation and needs review by the owner and a qualified Arabic-language reviewer, including the labels added to the forms in this revision. Preview PDFs were exported with Jost Regular, Inter Regular and Noto Sans Arabic Regular, which are byte-identical to the font files in the letterhead set's `00_source/fonts/`; the PDFs embed the fonts used. The editable Word files refer to font names and do not embed the typefaces, so the editing computer must have those fonts available to preserve the layout.

## Fields still requiring confirmation

- **Confirmed by the owner for stationery (30 Oct 2026) and printed:** trading name GEM; city and country (Riyadh, Saudi Arabia); contact@mish3l.com; +966114502929; contact "Mashal Abdulrahman, GM / Owner"; currency SAR. No vault note records these values; the owner's confirmation in the session is the only source.
- **Still placeholders (content controls):** registered legal name, Commercial Registration No., National Address, tax identifiers, bank and beneficiary details, payment and delivery terms, quote validity, and all customer or supplier fields. No value has been supplied or inferred for them.
- **VAT:** the rate field defaults to 15 as a working value only. Confirm VAT registration, treatment and rate with GEM's accountant, and whether FATOORA e-invoicing applies, before any invoice is issued.
- The Arabic and bilingual external-issue gate D8 remains open in the V3.0 document records. Keep this set internal until owner and native-language review is complete; confirm the legal, tax, payment, and commercial fields before issuing any document.

The purchase order carries no approval or authorization block: the owner's worksheet answered "No" to approval fields. This suite supplies no contract terms, warranty promise, or claim about a registered legal entity. Totals use Word table formulas that follow the VAT rate field; they are working calculations, not tax advice.

## Completion sequence

Keep these templates internal until the following sequence is complete:

1. **Owner supplies approved business values:** registered issuing entity and addresses; transaction contact details; jurisdiction and currency; tax registration/name/rate; beneficiary and bank details; payment and delivery terms; quotation validity; and purchase-order approval roles. Use only values the owner has confirmed for stationery.
2. **Accountant reviews the invoice:** confirm the required tax-invoice fields, numbering, tax treatment, and any jurisdiction-specific wording. Do not infer these from the website or from a generic template.
3. **Owner and qualified Arabic reviewer approve the Arabic:** review each RFQ, quotation, invoice, and purchase-order label in context, including RTL order, numerals, punctuation, and mixed-direction identifiers.
4. **Owner accepts the form application:** decide the deviations listed above (vertical frame/footer, English-first label order, and shortened status line) and approve the exact final forms.
5. **Run final artifact checks:** populate only approved values; verify calculations and editable fields; render every final DOCX to PDF; inspect every page; then check the exact final files in Microsoft Word and with a print proof. Record accessibility and any required supplier proof separately.
6. **Release only after the applicable gates close:** resolve the letterhead dependencies (LH03, LH08, R03-03, D8) for the intended language and output route. Remove internal markings only from a separately approved final copy after all checks pass.

Current check: the tracked `SHA256SUMS.txt` matches all 13 listed files. The suite remains **internal review only**; checksum validity establishes file integrity, not owner, legal, tax, localization, accessibility, native-Word, or print approval.

## Remove before issue

Each file carries internal-review markings that must be removed or replaced by the owner once the gates above are cleared, and not before: the footer issue-restriction line, the "CONTINUED" reference header (set through the `RefNo` document property), and every unfilled placeholder.

## Merge of the 29 Oct v3 drafts

The v3 drafts (`GEM Business Stationery Revised v3 2026-10-29`) were merged into this build rather than kept as a second set. Taken from v3: content-control fields with date hints, the Commercial Registration, Supply Date and RFQ-reference fields, SAR and VAT rows with calculated totals, the invoice Notes and Terms box, scope and assumptions boxes of at least four lines, the VAT-treatment dropdown on the RFQ, the `RefNo` document property, `FILL-IN-GUIDE.md` and `WORD-CHECK.bas`. Kept from this suite: Beige hairline rules, the tagline, 25 mm margins, the build script and the manifest. Changes made while merging:

- The VAT amount formula is `=(B7*B8)/100`. LibreOffice rejected the unparenthesised `=B7*B8/100` as "Expression is faulty"; the parenthesised form exports cleanly.
- Formula fields are no longer locked. A locked field ignores `Ctrl+A, F9`, so the totals would never recalculate. A `\# "#,##0.00"` switch gives two decimals in Word; LibreOffice previews ignore it and show `0`.
- The RFQ total is `=B7` (the subtotal cell), matching the other forms; v3 used `=F7`, which could not be mapped to a cell in the two-cell totals row.
- v3's "Internal Draft" file names are replaced by this suite's `_Template_working` names, and the "TEMPLATE 0x" kickers and intro notes were dropped to keep two pages.
- **Redesign (30 Oct 2026):** the first merge reproduced v3's boxed grid, which read as a form and not as GEM stationery. The layout now follows the letterhead's quiet language: a summary strip under the title (number, date, due or valid date, total), Supplier/Customer (or Buyer/Supplier, Issuer/Customer, Requester/Supplier) as two side-by-side stacks, bilingual labels on one line with the Arabic at the line end, hairline rules in place of cell boxes, and the final total or balance emphasised in Jost. The Ink header fill was removed, which also closes that listed exception.

- Cells that feed a formula (quantity, unit price, amount paid) start as numeric placeholders (`0`, `0.00`) so a blank form cannot print a Word formula error; descriptive cells keep "Enter ..." text.
- The dropdown's `showingPlcHdr` element now precedes the control type, as the OOXML schema orders it.
- For the Arabic reviewer: the same concept carries two wordings in places, for example "Requested Delivery" is "موعد التسليم المطلوب" on the RFQ and "تاريخ التسليم المطلوب" on the PO. Both came from the v3 drafts and neither has been reviewed.

Calculation results could not be checked here: LibreOffice previews show cached values and do not recalculate on export. Run `WORD-CHECK.bas` in Word (see `FILL-IN-GUIDE.md`).

## Rebuild and verification

Run `node build.mjs` from this directory to rebuild the four Word files from the source in the repository's archived V3.0 brand asset kit. Run `bash export-pdf.sh` to regenerate the four PDF previews from the Word files with LibreOffice. The script copies the three Regular font files from `FONT_DIR` (default `~/Library/Fonts`) into a throwaway LibreOffice profile, so the PDFs embed those exact fonts. After either step, regenerate `SHA256SUMS.txt`. PDF checksums are not reproducible across exports because LibreOffice stamps creation times.

Checked in LibreOffice only: the four DOCX files open and export, and every PDF page was rendered and inspected for layout, logo size and placement, tagline, placeholder visibility, repeated table headers, page breaks, right-aligned Arabic text and the footer. Each form runs to two pages, and the last body rule on every page sits at least 8 mm above the footer rule, measured at 150 dpi. `pdffonts` shows only Jost Regular, Inter Regular and Noto Sans Arabic Regular, all embedded. Text extraction found Arabic characters and no replacement glyphs. Arabic paragraphs use logical (`start`/`end`) alignment as the letterhead set does; that set was tested in Word for Mac, this suite was not. Not checked: native Microsoft Word (including separator paragraphs, keep-with-next chains and fonts missing from the editing computer), physical printing, accessibility, legal, tax, or owner acceptance.
- **Layout revision (30 Oct 2026, second pass):** the Invoice now carries the title `Tax Invoice / فاتورة ضريبية` (wording pending the accountant; one constant in `build.mjs`), keeps its items and totals on page 1, and moves payment instructions, a reserved e-invoice QR slot (for the code the invoicing system adds), references and notes to page 2. The supplier block shows name, address, tax identifier and commercial registration; the contact person sits under Payment Instructions, and email and phone are printed in the footer. Placeholders now read as field names, not instructions. The Quotation prices before it lists assumptions and terms. The RFQ keeps its priced item table because the supplier fills in the prices.
- **Page capacity:** the Invoice holds four item rows on two pages. Adding more rows in Word makes the item table split across pages (the column header row repeats and the last item stays with the totals); a longer invoice runs to a third page. The summary strip keeps English and Arabic labels on two lines because one-line labels do not fit its four narrow cells; this is an owner-visible deviation from the one-line label rule.
- **Word check (30 Oct 2026):** the four .docx files were opened in Microsoft Word for Mac and exported to PDF from Word. Each is two pages; fonts embed as Inter, Jost and Noto Sans Arabic Regular only; the calculated totals show `0.00`; the item table starts intact on its page. Not covered: Word on Windows, printing, field recalculation after edits, and a machine without the three fonts.
