# GEM Business Stationery Redesign: Design

Date: 2026-10-30
Branch: `fix/gem-stationery-audit-20261027` (PR #33)
Status: WORKING TEMPLATE SET / INTERNAL REVIEW ONLY. No gate, status line or governance wording changes.

## Purpose

Rebuild the four stationery forms (Invoice, Quotation and Proposal, Request for Quotation, Purchase Order) so they can be sent to real customers and suppliers as PDFs or filled-in Word files. The current forms read as cluttered: every label is split across two lines, the invoice puts party details on page 1 and items on page 2, and placeholder text fills every field.

Owner decisions so far:
- Use: real documents, sent as PDF or filled-in Word (not internal-only examples).
- Invoice: the template defines the visual style. Its fields follow the ZATCA baseline until an accounting system is chosen (none chosen yet), then field order is aligned to that system.

## Research basis

- Saudi tax invoices must be primarily Arabic; English may appear alongside. Standard (B2B) invoices go through ZATCA clearance as structured data with a QR code, so a hand-filled Word file is a layout, not the compliant record. Sources were vendor documents, not ZATCA's own; the accountant must confirm (ClearTax, Qoyod, Global Law Experts).
- Invoice layout practice: amount due first and prominent; flow from sender to customer to items to total to payment details; small palette (Stripe, Payanywhere).
- Bilingual practice: one-line `English / Arabic` labels or two columns; values entered once; Western numerals for amounts (TallyPrime, Frappe forum, Invovate).
- Brand: GEM Letterhead Set v1.1 Revision 03 and V3.0 Parts A/B/C: logo at 32 mm with fixed tagline, 25 mm side margins, Inter, Jost and Noto Sans Arabic in Regular weight only, Ink #12171D and Beige #BCACA7 as rules, no fills.

## Shared system (all four forms)

- Header: logo and tagline from the letterhead set. Continuation pages use the quiet continuation header.
- Title row: `English / Arabic` title on one line; document number and issue date at the right.
- Summary strip: the one or two figures the reader needs first (see each form).
- Party blocks: two columns, each with name, address and identifiers.
- Item table: shared column style, hairline rules, repeated header row, totals right-aligned under it.
- Labels: single line, `ENGLISH / عربي`, Latin tracked uppercase, Arabic untracked at the 1.33 token ratio.
- Values: entered once, in the language the user types. Western numerals for amounts, dates, codes and references. Arabic and Latin in separate runs with explicit direction.
- Type and colour: Regular weights only; the total is larger, not bold. Ink and Beige hairlines only; no fills.
- Placeholders: short and lighter in tone (for example `Legal name`), not sentences.
- Footer: confirmed contact line, page number, internal-review marking. Footer height stays compact unless the owner accepts it; the other deviations (Ink header fill, uppercase tracking differences, English-first order) are reviewed against the brand rules and removed or documented.

## Per-form content

### Invoice
- Page 1: title (`Tax Invoice / فاتورة ضريبية`, wording pending accountant), amount-due strip (total due in SAR and due date), Seller and Buyer blocks (name, address, VAT number, CR number), line items (no., description, qty, unit, unit price, VAT rate, line total), totals (subtotal, VAT, total, amount paid, balance due).
- Page 2 (only if needed): payment details (payee, bank, IBAN, reference), notes and terms, reserved square for the e-invoice QR code added by the accounting system.
- Target: one page with about four line items.

### Quotation and Proposal
- Summary strip: total and valid-until date.
- Issuer and Customer blocks, then scope summary (before pricing), priced item table with VAT totals, assumptions and terms, delivery and payment, customer acceptance block.

### Request for Quotation
- Summary strip: response deadline.
- Buyer (GEM) and Supplier blocks, requirements table with quantities and no prices, delivery requirements, what the supplier must include.

### Purchase Order
- Summary strip: total and delivery date.
- Buyer (GEM) and Supplier blocks, items with agreed prices and totals, delivery and payment terms, supplier confirmation line. No approval block (owner worksheet answered No).

## Build and output

- Keep `documents/working/business-stationery-20261027/build.mjs` as the source of truth; Word files stay editable with content-control fields and calculated totals (`=(B7*B8)/100` form, unlocked).
- Keep `export-pdf.sh`, `FILL-IN-GUIDE.md`, `WORD-CHECK.bas`, and refresh `SHA256SUMS.txt` plus the repo manifests with `tools/refresh_manifests.py`.
- Every form stays within two pages; at least 8 mm clear above the footer rule.

## Verification

1. `node build.mjs` twice with identical DOCX hashes; `xmllint` on every part.
2. `bash export-pdf.sh`; render and inspect every page.
3. Arabic checks: RTL, `ar-SA`, untracked, non-italic, no Arabic-Indic digits, Ink/Beige/White only, no bold.
4. `python3 tools/validate_collection.py --skip-remote --check-index` and the `tools/` unit tests.
5. Open the DOCX files in Microsoft Word for Mac if available; otherwise report as untested.

## Out of scope and still open

- Legal entity, tax identifiers, VAT treatment and rate, bank and payment details: placeholders until the owner supplies and the accountant confirms.
- Native Arabic review of every label; D8 external-issue gate; whether Arabic PDFs may stay in the public repository.
- Choice of accounting system; final invoice field order follows it.
- Print proof and accessibility check.
- The two unpushed commits (`1766c86`, `d3ef94b`) and PR #33 update: decided after this redesign lands on the branch.
