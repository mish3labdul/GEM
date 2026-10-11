"""AR01 PDF observation (read-only): extract text with macOS PDFKit and record, per line in extraction order, ONLY script-class run structure (A=Arabic, L=Latin, D=digit, _=space, p=punctuation) and flags. No text is written.
Usage: ar01_pdfkit_extract.py <pdf_dir> <out_json>   (docling venv python: Quartz)"""
import sys, os, re, json
import Quartz
from Foundation import NSURL
AR = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
def cls(s): return re.sub(r'(.)\1+', lambda m: m.group(1) + str(len(m.group(0))), ''.join('A' if AR.search(c) else 'L' if re.match('[A-Za-z]', c) else 'D' if c.isdigit() else '_' if c.isspace() else 'p' for c in s))
pdfdir, outp = sys.argv[1:3]
JOBS = [("A_baseline", 38), (os.environ.get("AR01_PDFKIT_PARTA", "A_split"), 38),  # set AR01_PDFKIT_PARTA=A_corrected to regenerate the stage-1 comparison
 ("LH_Arabic_First_Page", 0), ("LH_Bilingual_First_Page", 0), ("LH_Arabic_Continuation", 0), ("LH_Bilingual_Continuation", 0)]
out = {}
for name, pg in JOBS:
    doc = Quartz.PDFDocument.alloc().initWithURL_(NSURL.fileURLWithPath_(os.path.abspath(f"{pdfdir}/{name}.pdf"))); lines = (doc.pageAtIndex_(pg).string() or "").split("\n")
    rec = []
    for i, l in enumerate(lines):
        if not l.strip(): continue
        rec.append(dict(line=i, length=len(l), classes=cls(l), arabic=bool(AR.search(l)), has_code_placeholder=('GEM-0000' in l), has_code_segments_reversed=bool(re.search(r'0000-MEG|0000-GEM', l)),
                        has_bracket_placeholder=('[DATE]' in l or '[REFERENCE NUMBER]' in l)))
    near = sorted({k for j, r in enumerate(rec) if r['arabic'] for k in (j - 1, j, j + 1) if 0 <= k < len(rec)})
    out[name] = dict(page_index=pg, line_count=len(rec), arabic_lines=sum(1 for r in rec if r['arabic']), lines_arabic_and_neighbours=[rec[k] for k in near])
json.dump(out, open(outp, 'w'), indent=1); print({k: (v['line_count'], v['arabic_lines']) for k, v in out.items()})
