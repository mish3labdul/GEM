#!/usr/bin/env python3
"""Layout regression checks on the exported business stationery PDFs."""
import os, re, shutil, subprocess, tempfile, unittest, zipfile
from pathlib import Path

FORMS = Path(__file__).resolve().parent.parent / 'documents/working/business-stationery-20261027'
PDFS = {
    'rfq': FORMS / 'GEM_Request_for_Quotation_Template_working.pdf',
    'quotation': FORMS / 'GEM_Quotation_Proposal_Template_working.pdf',
    'invoice': FORMS / 'GEM_Invoice_Template_working.pdf',
    'po': FORMS / 'GEM_Purchase_Order_Template_working.pdf',
}


def build_variant(out_dir, item_rows):
    """Build the DOCX files with a different number of item rows and export them to PDF in out_dir."""
    env = {**os.environ, 'GEM_OUT_DIR': str(out_dir), 'GEM_ITEM_ROWS': str(item_rows)}
    subprocess.run(['node', str(FORMS / 'build.mjs')], check=True, capture_output=True, env=env)
    subprocess.run(['bash', str(FORMS / 'export-pdf.sh')], check=True, capture_output=True, env={**env, 'OUT_DIR': str(out_dir)})


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
                self.assertIsNone(re.search(r'\bEnter |\bSelect ', text))

    def test_docx_has_no_bold_italic_fills_or_arabic_indic_digits(self):
        for docx in FORMS.glob('GEM_*_Template_working.docx'):
            xml = zipfile.ZipFile(docx).read('word/document.xml').decode('utf-8')
            with self.subTest(form=docx.name):
                self.assertNotIn('<w:b/>', xml)
                self.assertNotIn('<w:i/>', xml)
                self.assertIsNone(re.search(r'w:fill="[0-9A-Fa-f]{6}"', xml))
                self.assertIsNone(re.search('[\u0660-\u0669\u06f0-\u06f9]', xml))

    def test_item_table_never_starts_with_a_lone_row(self):
        for name, path in PDFS.items():
            for page in pdf_pages(path):
                if re.search(r'ITEMS OR SERVICES|PRICING', page.upper()):
                    with self.subTest(form=name):
                        self.assertGreaterEqual(len(re.findall(r'^\s*\d\s+Description', page, re.M)), 2)
                    break

    def test_placeholders_start_with_a_capital_letter(self):
        for docx in FORMS.glob('GEM_*_Template_working.docx'):
            xml = zipfile.ZipFile(docx).read('word/document.xml').decode('utf-8')
            for sdt in re.findall(r'<w:sdt>.*?</w:sdt>', xml, re.S):
                text = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', sdt))
                with self.subTest(form=docx.name, placeholder=text):
                    self.assertFalse(text[:1].islower())

    @unittest.skipUnless(shutil.which('soffice') and shutil.which('node'), 'needs node and soffice')
    def test_invoice_with_many_item_rows_splits_the_table_instead_of_moving_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_variant(tmp, 8)
            pages = pdf_pages(Path(tmp) / 'GEM_Invoice_Template_working.pdf')
            self.assertIn('ITEMS OR SERVICES', pages[0].upper())
            self.assertIn('ITEMS OR SERVICES', pages[1].upper(), 'column header row repeats on the next page')
            self.assertLessEqual(len(pages), 3)


if __name__ == '__main__':
    unittest.main()
