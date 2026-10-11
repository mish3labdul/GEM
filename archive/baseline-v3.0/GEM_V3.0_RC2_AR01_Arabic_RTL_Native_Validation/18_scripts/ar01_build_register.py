"""AR01 local screenshot register (metadata only): filename, document, slide, purpose, SHA-256, Local-only = YES, D7 restriction = PENDING. Usage: ar01_build_register.py <package_dir>"""
import os, re, csv, hashlib, sys
P = sys.argv[1]; D = f"{P}/local_only/screenshots"; sh = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); rows = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.png'): continue
    m = re.match(r'A_(baseline_D3|corrected_AR01)_slide(\d+)\.png', f)
    if m: doc, slide, pur = ("Part A (D3 baseline)" if m.group(1) == 'baseline_D3' else "Part A (AR01 stage-1 candidate: slide 39 only corrected)"), str(int(m.group(2))), "Native PowerPoint slide capture (pixel-diff pair)"
    elif re.match(r'A_AR01_final2_slide(\d+)\.png', f): doc, slide, pur = "Part A (AR01 candidate after the slide-39 Text 8 run split)", str(int(re.match(r'A_AR01_final2_slide(\d+)', f).group(1))), "Native PowerPoint slide capture of the final Part A candidate"
    elif re.match(r'(before|splitA|splitB)_slide039\.png', f): doc, slide, pur = "Part A slide 39 scratch variant (" + f.split('_')[0] + ")", "39", "Native capture for the run-split position test (before split / variant A / variant B)"
    elif f.startswith('AR01_slide39_split_before_after'): doc, slide, pur = "Part A slide 39 (before vs after run split)", "39", "Crop of the only differing region (PowerPoint's floating Copilot button, not slide content)"
    elif re.match(r'A_AR01_final_slide(\d+)\.png', f): doc, slide, pur = "Part A (AR01 candidate, final)", str(int(re.match(r'A_AR01_final_slide(\d+)', f).group(1))), "Native PowerPoint slide capture after all 11 paragraph corrections"
    elif f.startswith('B_AR01_final_slide'): doc, slide, pur = "Part B (AR01 candidate)", "9", "Native PowerPoint slide capture after slide-9 metadata correction"
    elif f.startswith('AR01_final_vs_baseline_diff'): doc, slide, pur = "Part A 37, 38, 65, 66, 68 and Part B 9 (baseline vs AR01 candidates)", "37, 38, 65, 66, 68 / 9", "Before / after / difference crops (sub-pixel glyph-edge differences only)"
    elif f.startswith('AR01_word_') and 'inmemory' in f: doc, slide, pur = "Letterhead Arabic First Page (native Word, in-memory continuation test)", "2", "Native Word capture of a temporary copy edited in memory only (page break + one letter; never saved) to show page-2 header/footer"
    elif f.startswith('AR01_word_'): doc, slide, pur = "Letterhead " + re.sub(r'^AR01_word_|_footer|\.png$', '', f).replace('_', ' ') + " (native Word)", "1", "Native Microsoft Word window capture of a byte-identical temporary copy"
    elif f.startswith('PDF_A_') and 'crop' in f: doc, slide, pur = "Part A INTERNAL WORKING PDF (LibreOffice)", re.sub(r'.*_p(\d+)_.*', r'\1', f), "Before/after crop of a PDF page raster (observation only)"
    elif f.startswith('PDF_A_baseline') or f.startswith('PDF_A_final') or f.startswith('PDF_A_p'): doc, slide, pur = "Part A INTERNAL WORKING PDF (LibreOffice)", re.sub(r'.*_p(\d+).*', r'\1', f), "Raster of the internal working PDF page (observation only)"
    elif f.startswith('B_NP01R1_slide'): doc, slide, pur = "Part B (NP01-R1 candidate)", "9", "Native PowerPoint slide capture (Arabic specimen)"
    elif re.match(r'A39_V\d_', f): doc, slide, pur = "Part A slide 39 scratch variant", "39", "Native capture of scratch variant " + re.match(r'A39_(V\d)', f).group(1) + " (direction/alignment/language test)"
    elif f.startswith('A39_variants_compare'): doc, slide, pur = "Part A slide 39 scratch variants", "39", "Comparison strip V0/V1/V3/V4 (technical-identifier line)"
    elif f.startswith('A39_before_after'): doc, slide, pur = "Part A slide 39 (baseline vs AR01 candidate)", "39", "Before/after crop of both Arabic lines"
    elif f.startswith('A39_latin_glyph'): doc, slide, pur = "Part A slide 39 (baseline vs AR01 candidate)", "39", "2x glyph comparison of the Latin code and digits"
    elif f.startswith('AR01_seven_arabic'): doc, slide, pur = "Part A 37, 38, 65, 66, 68, 39 and Part B 9 (AR01 candidates)", "37, 38, 65, 66, 68, 39 / 9", "Contact sheet used to inspect shaping on all seven Arabic slides"
    elif f.startswith('LH_four'): doc, slide, pur = "Letterheads Arabic/Bilingual First+Continuation (LibreOffice render)", "1", "Contact sheet of four LibreOffice renders (observation only; not Word)"
    elif f.startswith('LH_'): doc, slide, pur = "Letterhead " + f.split('_LibreOffice')[0][3:].replace('_', ' ') + " (LibreOffice render)", "1", "LibreOffice render of test copy (observation only; not Word)"
    else: doc, slide, pur = "(other)", "", f
    rows.append([f"{D}/{f}", doc, slide, pur, sh(f"{D}/{f}"), "YES", "PENDING"])
csv.writer(open(f"{P}/16_AR01_Local_Screenshot_Register.csv", 'w', newline='', encoding='utf8')).writerows([["Screenshot filename (repo-relative path)", "Document", "Slide / page", "Purpose", "SHA-256", "Local-only?", "D7 restriction"]] + rows)
print(len(rows), "screenshots registered")
