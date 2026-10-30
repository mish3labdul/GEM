#!/usr/bin/env python3
"""Layout regression checks on the exported business stationery PDFs."""
import subprocess, unittest
from pathlib import Path

FORMS = Path(__file__).resolve().parent.parent / 'documents/working/business-stationery-20261027'
PDFS = {
    'rfq': FORMS / 'GEM_Request_for_Quotation_Template_working.pdf',
    'quotation': FORMS / 'GEM_Quotation_Proposal_Template_working.pdf',
    'invoice': FORMS / 'GEM_Invoice_Template_working.pdf',
    'po': FORMS / 'GEM_Purchase_Order_Template_working.pdf',
}


def pdf_pages(path):
    """Return the text of each page, as pdftotext -layout extracts it."""
    out = subprocess.run(['pdftotext', '-layout', str(path), '-'], check=True, capture_output=True, text=True).stdout
    return [page for page in out.split('\f') if page.strip()]


class StationeryLayoutTests(unittest.TestCase):
    def test_every_form_has_at_most_two_pages(self):
        for name, path in PDFS.items():
            with self.subTest(form=name):
                self.assertLessEqual(len(pdf_pages(path)), 2)

    def test_invoice_items_and_total_on_first_page(self):
        first = pdf_pages(PDFS['invoice'])[0]
        self.assertIn('ITEMS', first.upper())
        self.assertIn('BALANCE DUE', first.upper())

    def test_invoice_has_qr_slot(self):
        self.assertIn('E-INVOICE QR', '\n'.join(pdf_pages(PDFS['invoice'])).upper())

    def test_no_instruction_sentence_placeholders(self):
        for name, path in PDFS.items():
            text = '\n'.join(pdf_pages(path))
            with self.subTest(form=name):
                self.assertNotIn('Enter Registered Legal Name', text)
                self.assertNotIn('Enter Customer Billing Address', text)

    def test_footer_marking_present(self):
        for name, path in PDFS.items():
            for i, page in enumerate(pdf_pages(path), 1):
                with self.subTest(form=name, page=i):
                    self.assertIn('NOT FOR EXTERNAL ISSUE', page)


if __name__ == '__main__':
    unittest.main()
