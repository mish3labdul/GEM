"""AR01 findings builder: derives 05 (RTL/bidi findings), 09 (mixed-run matrix), 10 (technical correction register), 11 (native Arabic reviewer queue) from the committed inventory CSV,
the native-pass CSVs and the static checks. No Arabic strings are written: identifiers, SHA-256 prefixes, lengths and feature descriptors only.
Usage: ar01_build_findings.py <package_dir>"""
import sys, csv, json, re, os
pkg = sys.argv[1]
rd = lambda f: list(csv.reader(open(f"{pkg}/{f}", encoding='utf8')))
inv = rd("03_AR01_Arabic_Content_Inventory.csv"); H = inv[0]; ix = {h: i for i, h in enumerate(H)}; rows = inv[1:]
wr = lambda f, hdr, data: csv.writer(open(f"{pkg}/{f}", 'w', newline='', encoding='utf8')).writerows([hdr] + data)
def slide_of(r): return r[ix['Slide']] or r[ix['Part / kind']].replace('word/', '')
is_ppt = lambda r: r[0].startswith('Part')
AUTH_RTL = "Register M06 (true RTL flow) · M12 (standardised codes stay LTR inside RTL) · M05 (no Latin tracking on Arabic)"

# ---------------------------------------------------------------- 05 RTL / bidi findings
out05 = []
for r in rows:
    doc, sl, label, cat = r[0], slide_of(r), r[ix['Shape label']] or f"para {r[ix['Paragraph index']]}", r[ix['Technical classification']]
    h = r[ix['Text SHA-256']][:12]
    if is_ppt(r):
        s39 = (doc == 'Part A' and r[ix['Slide']] == '39')
        if s39 and cat == 'ARABIC + TECHNICAL ID':
            out05.append([doc, sl, label, cat, 'paragraph direction absent (requested left-to-right); lang en-US', 'label then code left-to-right: code appears to the RIGHT of the Arabic label (native PowerPoint)', 'MIXED-RUN BIDI DEFECT (also LANGUAGE-METADATA DEFECT)', 'P2',
                          'Yes — AR01 candidate: rtl=1 + lang ar-SA', 'code to the LEFT of the label, gap preserved (native PowerPoint, positions measured)', h])
        elif s39:
            out05.append([doc, sl, label, cat, 'paragraph direction absent (requested left-to-right); lang en-US', 'digits left of word: visually correct in either direction (native PowerPoint)', 'LANGUAGE-METADATA DEFECT (visual order PASS)', 'P3',
                          'Yes — AR01 candidate (paired example, consistency)', 'unchanged visually; direction and language now declared', h])
        else:
            out05.append([doc, sl, label, cat, 'paragraph direction absent (requested left-to-right); lang en-US', 'single-script Arabic: correct in either direction (native PowerPoint)', 'LANGUAGE-METADATA DEFECT (visual order PASS)', 'P3',
                          'No — proposed for owner approval (no native defect shown)', 'n/a', h])
    else:
        mixed = r[ix['Latin present?']] == 'yes'
        out05.append([doc, sl, label, cat, r[ix['Paragraph rtl / bidi']][:60], 'static: Latin identifiers are separate rtl=0 runs bounded by explicit LRM marks (R03-02); LibreOffice render order plausible' if mixed else 'static: RTL paragraph; LibreOffice render order plausible',
                      'PASS (static OOXML) — native Word NOT TESTED in AR01', 'none', 'No change needed', 'n/a', h])
wr("05_AR01_RTL_Bidi_Findings.csv", ["Document", "Slide / part", "Element", "Technical classification", "Direction / language before", "Visual order before", "Classification", "Severity", "Corrected in AR01?", "Result after", "Text SHA-256 (prefix)"], out05)

# ---------------------------------------------------------------- 09 mixed-run test matrix (existing GEM content only)
M = [
 ["Arabic + Latin acronym", "—", "No existing example in the controlled candidates (placeholders such as [DATE] are tested under technical ID)", "NOT TESTED", "none", ""],
 ["Arabic + filename", "—", "No existing example", "NOT TESTED", "none", ""],
 ["Arabic + date", "Letterhead Arabic/Bilingual First Page", "Date line is an Arabic label + [DATE] placeholder (no real date value exists)", "PARTIAL: placeholder only; static OOXML PASS; LibreOffice render order plausible; Word native NOT TESTED", "static + LibreOffice observation", "Real date and Arabic-Indic numeral convention not signed off (R03-06 / M11)"],
 ["Arabic + percentage", "—", "No existing example", "NOT TESTED", "none", ""],
 ["Arabic + numerals", "Part A slide 39", "Arabic word + 3 Latin digits (guest-facing number example)", "PASS native PowerPoint (digits left of word, before and after; positions identical)", "native PowerPoint probe + screenshot (local-only)", "Latin digits shown 'until policy is signed off' (M11): policy item, not a defect"],
 ["Arabic + parentheses / brackets", "Part A slides 65, 68; letterheads (guillemets in placeholders)", "Bracketed Arabic placeholder; «…» placeholder wrappers", "PASS native PowerPoint (slides 65 and 68 viewed: brackets render; no direction-dependent difference for a fully bracketed single-script string); letterheads PASS static + LibreOffice observation", "native PowerPoint (slides); static + LibreOffice (letterheads)", "Word native NOT TESTED"],
 ["Arabic + colon", "Letterhead Arabic/Bilingual First Page", "Arabic label + colon + Latin placeholder (date, reference); subject line with colon", "PASS static OOXML; LibreOffice render order plausible; Word native NOT TESTED", "static + LibreOffice observation", ""],
 ["Arabic + slash", "—", "No existing example", "NOT TESTED", "none", ""],
 ["Arabic + technical ID", "Part A slide 39 (label + GEM-0000 placeholder)", "Arabic label followed in logical order by a Latin technical code", "BEFORE: FAIL native PowerPoint (code right of label). AFTER (AR01 candidate): PASS native PowerPoint (code left of label, gap preserved, code intact LTR)", "native PowerPoint probe + screenshots (local-only); LibreOffice PDF + PDFKit extraction (after: code extracted intact as one Latin line; before: the code's digit and letter segments came out in the wrong order on the label's line)", "Linguistic wording of the label: REQUIRES NATIVE ARABIC REVIEW"],
 ["Arabic + technical ID (placeholders in letterheads)", "Letterhead Arabic/Bilingual First Page ([REFERENCE NUMBER])", "Label + colon + Latin placeholder with LRM bounding marks", "PASS static OOXML; LibreOffice render order plausible; PDFKit extraction plausible; Word native NOT TESTED", "static + LibreOffice + PDFKit", "Prior Word-for-Mac evidence (R03-02) inherited, not re-verified"],
]
wr("09_AR01_Mixed_Run_Test_Matrix.csv", ["Case", "Where (existing GEM content)", "Description (no wording)", "Result", "Evidence method", "Note"], M)

# ---------------------------------------------------------------- 10 technical correction register
reason = "Native PowerPoint measured the paragraph as left-to-right with lang en-US; the mixed label+code line resolved with the code on the wrong side and the label/code space attached to the Latin segment. rtl=1 fixes the order; ar-SA restores the gap."
C = []
for shp, kind in (("Text 8", "label + Latin technical code (mixed)"), ("Text 4", "label + digits (paired example; no visible defect)")):
    geo_dir = "Box geometry: no. Text order within the box: YES, intended (code now left of the label)" if shp == "Text 8" else "Box geometry: no. Text order within the box: no"
    geo_lang = "Box geometry: no. Latin glyph stroke rendering slightly lighter (complex-script text path); advance widths unchanged (115.0 pt)" if shp == "Text 8" else "Box geometry: no. Text order: no. Latin digit glyph stroke slightly lighter; advance widths unchanged"
    C.append(["Part A (AR01 candidate)", "39", f"{shp} — {kind}", "a:pPr: rtl absent (inherits LTR)", "a:pPr rtl=\"1\"", reason if shp == "Text 8" else "Same slide, paired example; declared direction for consistency (no visual change).", AUTH_RTL + "; Part A slide 39 content; letterhead R03-02 precedent", "no", geo_dir, "no", "Applied"])
    C.append(["Part A (AR01 candidate)", "39", f"{shp} Arabic run", "a:rPr lang=\"en-US\"", "a:rPr lang=\"ar-SA\"", "Arabic run declared Arabic (proofing and assistive-technology language; also fixes the label/code gap natively).", AUTH_RTL, "no", geo_lang, "no", "Applied"])
prop = [r for r in rows if is_ppt(r) and not (r[0] == 'Part A' and r[ix['Slide']] == '39')]
for r in prop:
    C.append([f"{r[0]} (proposed, NOT applied)", r[ix['Slide']], f"{r[ix['Shape label']]} — Arabic paragraph {r[ix['Paragraph index']]}", "rtl absent; lang en-US", "rtl=\"1\"; lang ar-SA (proposed)", "Language/direction metadata only; no native visual defect shown. Applying would also supersede the NP01-R1 candidate for Part B. Deferred for owner decision.", AUTH_RTL, "no", "no", "no", "PROPOSED — owner approval required"])
wr("10_AR01_Technical_Correction_Register.csv", ["Document", "Slide / page", "Element", "Before property", "After property", "Reason", "Authority", "Text changed?", "Visual geometry changed?", "Linguistic meaning changed?", "Status"], C)

# ---------------------------------------------------------------- 11 native Arabic reviewer queue
CTX = {('Part A', '37'): ("Slide 'Arabic · Direction': Arabic string in a bordered example box captioned in English as a working string, not approved copy", "Is this string suitable as a Saudi/GCC working sample, correct and natural?", "High"),
       ('Part A', '38'): ("Slide 'Bilingual composition · concept': Arabic strings on the English-first tile (English counterpart text present) and the Arabic-first tile (English caption present)", "Are the Arabic strings correct, natural and consistent across the two tiles?", "High"),
       ('Part A', '39'): ("Slide 'Mixed language, numerals and codes': the 'GUEST-FACING NUMBER' example (Arabic label + digits) and the 'TECHNICAL IDENTIFIER' example (Arabic label + Latin code placeholder)", "Are the two labels correct and idiomatic; is the label-then-code order acceptable; confirm numeral convention (M11)?", "High"),
       ('Part A', '65'): ("Slide 'Wayfinding · principles · concept': bracketed Arabic placeholder in the bilingual-order panel", "Is a bracketed placeholder acceptable, or should an approved sample word replace it?", "Medium"),
       ('Part A', '66'): ("Slide 'Signage concept': Arabic terms on the Arabic and bilingual sign tiles (English counterpart 'Reception' shown)", "Are the sign terms standard and appropriate for Saudi/GCC signage?", "High"),
       ('Part A', '68'): ("Slide 'Corporate and B2B · concept': bracketed Arabic placeholder", "As slide 65.", "Medium"),
       ('Part B', '9'): ("Slide 'Typography · Families': Arabic specimen pair beside the Noto Sans Arabic tile", "Is the specimen pair acceptable as an Arabic type specimen?", "Low")}
Q = []
for r in rows:
    if is_ppt(r):
        ctx, q, pri = CTX[(r[0], r[ix['Slide']])]
        res = 'Yes (AR01 candidate)' if (r[0] == 'Part A' and r[ix['Slide']] == '39') else 'n/a (rendering acceptable; metadata proposal pending owner)'
        Q.append([r[0], f"slide {r[ix['Slide']]}", f"{r[ix['Shape label']]} / paragraph {r[ix['Paragraph index']]}", ctx, res, q, "Wording, grammar, terminology, tone", pri, r[ix['Text SHA-256']][:12], "PENDING NATIVE ARABIC REVIEW"])
for r in rows:
    if not is_ppt(r):
        dep = r[ix['Bidi dependencies']]; n = int(r[ix['Text length']])
        role = ("date/reference line: Arabic label + colon + Latin placeholder" if 'colon' in dep and 'latin-text' in dep else "label line ending in a colon (subject-style)" if 'colon' in dep
                else "placeholder block wrapped in guillemets" if 'brackets' in dep and n < 40 else "sample correspondence sentence" if n >= 40 else "short phrase (greeting, closing, signatory or status)")
        Q.append([r[0], "word/document.xml", f"paragraph {r[ix['Paragraph index']]}", role, 'Yes (static OOXML correct); Word native NOT TESTED', "Is the wording correct, idiomatic and appropriately formal for Saudi/GCC business correspondence?", "Wording, grammar, formality, terminology", "High", r[ix['Text SHA-256']][:12], "PENDING NATIVE ARABIC REVIEW"])
Q.append(["All", "all Arabic content", "—", "Translation of the brand tagline (M10) is not approved: the templates keep the tagline in English", "n/a (governance)", "Is a tagline translation wanted, and who approves it?", "Brand approval (M10)", "Medium", "", "PENDING NATIVE ARABIC REVIEW / OWNER"])
Q.append(["All", "all Arabic content", "—", "Arabic numeral convention for dates and numbers (M11, R03-06)", "n/a (policy)", "Which numeral system applies to guest-facing Arabic copy, dates and page labels?", "Policy sign-off", "Medium", "", "PENDING NATIVE ARABIC REVIEW / OWNER"])
wr("11_AR01_Native_Arabic_Reviewer_Queue.csv", ["Document", "Slide / page", "Element", "Context (no text)", "Technical issue resolved?", "Question for native reviewer", "Potential impact", "Priority", "Text SHA-256 (prefix)", "Status"], Q)
print(dict(rtl_rows=len(out05), matrix=len(M), corrections=len(C), reviewer_queue=len(Q)))
