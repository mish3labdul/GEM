# GEM Business Stationery Fill-in Guide

Complete only with confirmed details. Leave unresolved fields as their "Enter ..." placeholders.

## Fields and calculations

- Click a placeholder to select it, then type over it. Dates use DD/MM/YYYY (Gregorian). Currency is fixed at SAR.
- Enter the VAT rate as a number (15), not 15%.
- Item totals, subtotal, VAT amount, total and invoice balance are Word table formulas. After entering values press `Ctrl+A` then `F9` (Mac: `Cmd+A`, then `Fn+F9`) to recalculate. If you add item rows, update the range in the Subtotal formula (`=SUM(F3:F6)`).
- The reference number (invoice, quotation, RFQ or PO number) is the `RefNo` document property, so the body field and the continuation header stay in step. Set it in Word under File > Properties > Advanced > Custom, then press `Ctrl+A`, `F9`.
- To type Arabic in a value field press `Ctrl+Right Shift` (Windows) or use Control+Space or the input menu (Mac).

## What each form needs

| File | Complete before use |
|---|---|
| `GEM_Invoice_Template_working.docx` | Invoice, customer, pricing, tax, due-date, supply-date and payment details. Verify payment details through a known channel. |
| `GEM_Purchase_Order_Template_working.docx` | Buyer, supplier, delivery and pricing fields from approved commercial details. |
| `GEM_Quotation_Proposal_Template_working.docx` | Scope, assumptions, clear prices, delivery details, payment terms and a validity date. |
| `GEM_Request_for_Quotation_Template_working.docx` | Requester and supplier fields, the requirement, and a priced response by the stated date. Suppliers complete unit price, line total and the VAT treatment. |

All files are working drafts marked NOT FOR EXTERNAL ISSUE. See `README.md` for the open gates.
