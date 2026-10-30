# Business Stationery Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the four stationery forms so the Invoice leads with the amount due and its items on page 1, and Quotation, RFQ and PO share the same system.

**Architecture:** `build.mjs` already has the shared pieces (`titleBlock`, `summaryStrip`, `parties`, `fieldRows`, `itemsTable`, `noteBlock`; one-line bilingual `labelLine`). The work is a targeted iteration inside it: shorter placeholders, a cleaner summary strip, a reordered Invoice, a QR slot, and removal of avoidable brand deviations. A new layout test reads the exported PDFs with `pdftotext` so layout regressions fail fast.

**Tech Stack:** Node 22 (`build.mjs`, built-ins only), LibreOffice (`export-pdf.sh`), `pdftotext`, `xmllint`, Python `unittest` in `tools/`.

**Spec:** `docs/superpowers/specs/2026-10-30-business-stationery-redesign-design.md`

## Global Constraints

- A4; 25 mm side margins (`MARGIN_X = 1417`); logo 32 mm; tagline on first page only.
- Inter Regular 9 pt body, Jost Regular titles and headings, Noto Sans Arabic Regular for Arabic. No bold, no italic.
- Colours: Ink `12171D`, Beige `BCACA7`, White `FFFFFF` only. No fills.
- Labels are single line `ENGLISH` left and Arabic right; values entered once; Latin 0-9 for amounts, dates, codes.
- Every form at most two pages; at least 8 mm clear above the footer rule.
- Status stays "WORKING TEMPLATE SET / INTERNAL REVIEW ONLY"; no gate or governance wording changes.
- Confirmed facts only: GEM, Riyadh, Saudi Arabia, `contact@mish3l.com`, `+966114502929`, "Mashal Abdulrahman, GM / Owner", SAR. Everything else stays a placeholder.
- Totals use unlocked Word formula fields in the `=(B7*B8)/100` parenthesised form.

## Review Focus

- A customer name or address in Arabic that is much longer than the placeholder: the party block must wrap without overlapping the next row.
- More than four line items added in Word: the table header repeats and no total is stranded alone on a page.
- An empty form opened as-is: no placeholder reads like a sentence of instructions, and the totals show `0.00`.
- Arabic-Indic digits pasted into a number field: the check flags them (existing Arabic run check).
- Editing machine without Jost, Inter or Noto Sans Arabic: documented in the README as a layout risk, not a build failure.

---

### Task 1: Layout regression test

**Files:**
- Create: `tools/test_stationery_layout.py`
- Modify: none

**Interfaces:**
- Produces: `pdf_pages(path: Path) -> list[str]` (page texts from `pdftotext -layout`), used by later tasks' verification steps. Test class `StationeryLayoutTests`.

- [ ] **Step 1: Write the failing tests** in `tools/test_stationery_layout.py`, in the style of `tools/test_validate_previews.py`. Names and assertions:
  - `test_every_form_has_at_most_two_pages`: for the four PDFs in `documents/working/business-stationery-20261027/`, `len(pdf_pages(p)) <= 2`.
  - `test_invoice_items_and_total_on_first_page`: page 1 of the Invoice PDF contains `ITEMS` and `BALANCE DUE`.
  - `test_invoice_has_qr_slot`: Invoice text contains `E-INVOICE QR`.
  - `test_no_instruction_sentence_placeholders`: no PDF contains `Enter Registered Legal Name` or `Enter Customer Billing Address` (placeholders are short).
  - `test_footer_marking_present`: every page contains `NOT FOR EXTERNAL ISSUE`.
- [ ] **Step 2: Run to verify failure**
  Run: `cd tools && python3 -m unittest test_stationery_layout -v`
  Expected: `test_invoice_items_and_total_on_first_page`, `test_invoice_has_qr_slot` and `test_no_instruction_sentence_placeholders` FAIL; the other two pass.
- [ ] **Step 3: Commit** `test: add stationery layout regression tests`

### Task 2: Shared placeholders and summary strip

**Files:**
- Modify: `documents/working/business-stationery-20261027/build.mjs` (helpers `dateField`, `stripDate`, `refField`, `TAX_ID`, `text`, `summaryStrip` at ~L214-228 and L475-489; constants `LEGAL_NAME`, `BUSINESS_ADDRESS`, `CR_NUMBER`, `CURRENCY`)

**Interfaces:**
- Consumes: existing `sdt(alias, placeholder, opts)`.
- Produces: placeholders without the `Enter ` prefix and without instruction clauses (for example `Legal name`, `Address`, `DD/MM/YYYY`); `REF_PLACEHOLDER = "Reference no."`. `summaryStrip(cells)` keeps its signature; the Arabic label line aligns to the right edge of the cell, matching `labelLine`, so strip labels read like every other label.

- [ ] **Step 1:** Shorten every `ph` string in the shared constants and form definitions: drop `Enter `, drop clauses such as `, if applicable` and `(Trading Name: GEM)`; keep `alias` unchanged so Word's content-control titles stay descriptive.
- [ ] **Step 2:** Change `summaryStrip` so label (English left, Arabic right via the same tab stop as `labelLine`) sits on one line, then the value on the next; the last cell stays larger (Jost 15 pt) when `big`.
- [ ] **Step 3: Verify**
  Run: `node documents/working/business-stationery-20261027/build.mjs && bash documents/working/business-stationery-20261027/export-pdf.sh && cd tools && python3 -m unittest test_stationery_layout -v`
  Expected: `test_no_instruction_sentence_placeholders` now PASSES. Inspect page 1 of each PDF visually; label lines are single rows.
- [ ] **Step 4: Commit** `refactor: shorten placeholders and align summary strip labels`

### Task 3: Invoice page 1 and QR slot

**Files:**
- Modify: `build.mjs` (Invoice entry in `docs`, `parties`, `itemsTable`)

**Interfaces:**
- Consumes: shared helpers from Task 2.
- Produces: `qrSlot(): string` returning a bordered 28 mm square cell labelled `E-INVOICE QR / رمز الفاتورة الإلكترونية`, placed beside the payment instructions.

- [ ] **Step 1:** Title becomes `Tax Invoice` / `فاتورة ضريبية` behind a constant `INVOICE_TITLE` so the accountant's decision is a one-line change.
- [ ] **Step 2:** Reorder the Invoice body: title, summary strip, parties, items and totals, then payment instructions with `qrSlot()`, then notes. Move the References block (PO, Related Quotation, Supply Date, Currency) below the totals, as a compact two-column block.
- [ ] **Step 3:** Fold Contact, Email and Phone into the Supplier block as a single combined field only if page 1 would otherwise overflow; keep each as its own field if it fits.
- [ ] **Step 4: Verify**
  Run: as in Task 2 Step 3.
  Expected: `test_invoice_items_and_total_on_first_page` and `test_invoice_has_qr_slot` PASS; Invoice is at most two pages with at least 8 mm above the footer rule.
- [ ] **Step 5: Commit** `feat: lead invoice with items and totals, reserve e-invoice QR slot`

### Task 4: Quotation, RFQ and Purchase Order

**Files:**
- Modify: `build.mjs` (the three remaining entries in `docs`)

**Interfaces:**
- Consumes: Tasks 2 and 3.

- [ ] **Step 1:** Quotation: order becomes title, strip (number, issue date, valid until, total), parties, scope summary, pricing table, assumptions and terms, delivery and payment, acceptance. Move scope above pricing.
- [ ] **Step 2:** RFQ: strip keeps number, issue date and response due; the requirement table has no price columns in the printed layout (keep the existing `itemsTable` only if a no-price variant is not a small change; otherwise record it in the PR description as a follow-up).
- [ ] **Step 3:** PO: strip carries total and requested delivery; no approval block; supplier confirmation line stays.
- [ ] **Step 4: Verify** as in Task 2 Step 3, plus read every page image. Expected: all five tests PASS; each form at most two pages.
- [ ] **Step 5: Commit** `feat: align quotation, RFQ and PO with the shared layout`

### Task 5: Brand deviations, docs and checks

**Files:**
- Modify: `documents/working/business-stationery-20261027/README.md`, `FILL-IN-GUIDE.md`, `SHA256SUMS.txt`; `governance/SHA256SUMS.txt`; `governance/duplicate-report.csv`

- [ ] **Step 1:** Update the README's "Forms exceptions" list to match what the build now does. Keep the compact footer frame as a documented deviation; list anything else removed.
- [ ] **Step 2:** Run the full checks:
  - `node build.mjs` twice; `shasum -a 256 *.docx` identical both times.
  - `for f in *.docx; do unzip -p "$f" word/document.xml | xmllint --noout -; done` exits 0.
  - `python3 tools/refresh_manifests.py`, then `python3 tools/validate_collection.py --skip-remote --check-index` reports no failures.
  - `cd tools && python3 -m unittest test_validate_previews test_stationery_layout -v` all pass.
- [ ] **Step 3:** Render every PDF page to images and inspect; confirm Arabic runs are RTL with no bold or Arabic-Indic digits (existing check from PR #33).
- [ ] **Step 4: Commit** `docs: update stationery README, guide and manifests`
- [ ] **Step 5:** Push the branch and update the PR #33 description (summary of the redesign, remaining TODOs). Pushing is outward-facing: confirm with the owner first.
