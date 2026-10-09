"""NP01 analyzer: parses native-sweep TSVs (read-only inputs) into evidence CSVs/JSON. Usage: np01_analyze.py <sweepdir> <outdir>"""
import sys, re, csv, json, collections, os
ALLOWED = {"Jost", "Inter", "Noto Sans Arabic"}
AR = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
PRIORITY = {"Part A": [34, 35, 75, 79, 80], "Part B": [3, 9, 10, 11, 12, 13, 18, 19, 21, 22, 24, 30, 33],
            "Part C": [15, 44], "Part D": list(range(1, 25))}

# Visual inspection results (native PowerPoint window screenshots on fresh, unmodified test copies). (doc, slide): (class, severity, note, evidence file)
VISUAL = {
 ("Part A",33):("PASS","","Visually clean; 3pt box overrun is a metric only.","A_slide033_native.jpg"),
 ("Part A",34):("MINOR NATIVE VARIANCE","P3","400-only wording correct ('500 WEIGHT PENDING ACCEPTED FONT FILE (use 400)'). Body text overruns its box by ~12pt but clears the footer.","A_slide034_native.jpg; A_slide034_body_vs_footer_zoom.jpg"),
 ("Part A",35):("MINOR NATIVE VARIANCE","P3","'EMPHASIS · INTER 400 · 500 PENDING' fits on one line and renders regular weight. Kicker wraps to two lines and sits directly above the 'Aa' specimen.","A_slide035_native.jpg"),
 ("Part A",37):("PASS","OBSERVATION","Arabic string shapes and aligns right correctly. Observation only; localization approval pending.","A_slide037_arabic_native.jpg"),
 ("Part A",38):("PASS","OBSERVATION","Arabic strings shape correctly in both bilingual panels. Observation only.","A_slide038_arabic_native.jpg"),
 ("Part A",39):("REQUIRES NATIVE REVIEW","P3","Mixed Arabic/Latin line resolves with a left-to-right base direction (no rtl=1 on the paragraph); label and code order is not the RTL reading order. Working placeholder string; belongs to the localization pass (VAL-07/08/15 stay open).","A_slide039_arabic_mixed_order_native.jpg"),
 ("Part A",41):("MINOR NATIVE VARIANCE","P3","Four-line headline sits tight against the body paragraph below it; no overlap.","A_slide041_native.jpg"),
 ("Part A",45):("PASS","","Visually clean.","A_slide045_native.jpg"),
 ("Part A",48):("PASS","","Visually clean; caption fits above the bottom frame.","A_slide048_native.jpg"),
 ("Part A",61):("PASS","","Six-level hierarchy reads clearly by size with 400 weight only.","A_slide061_native.jpg"),
 ("Part A",65):("PASS","OBSERVATION","Arabic bracketed placeholder renders; bilingual order panel matches the stated rule. Observation only.","A_slide065_arabic_native.jpg"),
 ("Part A",66):("PASS","OBSERVATION","Arabic words shape correctly. Observation only.","A_slide066_arabic_native.jpg"),
 ("Part A",72):("MINOR NATIVE VARIANCE","P3","Footer text wraps to a second line ('GOVERNANCE'); no collision.","A_slide072_footer_wrap_native.jpg"),
 ("Part A",75):("PASS","","Example reads 'GEM_BRAND_Horizontal_Black_v3.0_20261006.svg'; STREAM = BRAND; no overflow or ambiguity; footer clear.","A_slide075_native.jpg"),
 ("Part A",79):("MINOR NATIVE VARIANCE","P3","Notes pane shows the C1 wording for slide 79, correctly attached. A hairline rule runs through the first line of the change-log text; slide XML is identical to ODI01-R1 (pre-existing, not introduced by D3).","A_slide079_with_notes_pane.jpg; A_slide079_changelog_rule_zoom.jpg"),
 ("Part A",80):("PASS","","Notes pane shows the C1 wording for slide 80 ('Closing. Part B is the Digital Design System V3.0...'); no 79/80 inversion in the user-visible UI.","A_slide080_with_notes_pane.jpg"),
 
 ("Part A",15):("PASS","","Table header at regular weight; layout clean (D5-touched slide).","A_slide015_native.jpg"),
 ("Part B",5):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet01.png"),
 ("Part B",6):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet01.png"),
 ("Part B",7):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet01.png"),
 ("Part B",14):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet01.png"),
 ("Part B",15):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet02.png"),
 ("Part B",16):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet02.png"),
 ("Part B",17):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet02.png"),
 ("Part B",20):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet02.png"),
 ("Part B",23):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet03.png"),
 ("Part B",25):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet03.png"),
 ("Part B",26):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet03.png"),
 ("Part B",27):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet03.png"),
 ("Part B",29):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet04.png"),
 ("Part B",31):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet04.png"),
 ("Part B",32):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","B_D5_coverage_sheet04.png"),
 ("Part C",7):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet01.png"),
 ("Part C",9):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet01.png"),
 ("Part C",21):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet01.png"),
 ("Part C",23):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet02.png"),
 ("Part C",28):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet02.png"),
 ("Part C",30):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet02.png"),
 ("Part C",32):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet02.png"),
 ("Part C",34):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet03.png"),
 ("Part C",39):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet03.png"),
 ("Part C",43):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet03.png"),
 ("Part C",47):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet03.png"),
 ("Part C",49):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet04.png"),
 ("Part C",51):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet04.png"),
 ("Part C",52):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet04.png"),
 ("Part C",54):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet04.png"),
 ("Part C",57):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet05.png"),
 ("Part C",60):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet05.png"),
 ("Part C",61):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet05.png"),
 ("Part C",63):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet06.png"),
 ("Part C",64):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet06.png"),
 ("Part C",65):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet06.png"),
 ("Part C",66):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet06.png"),
 ("Part C",67):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet07.png"),
 ("Part C",68):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet07.png"),
 ("Part C",69):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet07.png"),
 ("Part C",70):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet07.png"),
 ("Part C",71):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet08.png"),
 ("Part C",72):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet08.png"),
 ("Part C",74):("PASS","","D5-touched slide; viewed on contact sheet; regular-weight tables/text, no overflow or collision.","C_D5_coverage_sheet08.png"),
 ("Part C",4):("MINOR NATIVE VARIANCE","P3","D5-touched slide; table last row grows and the paragraph below starts with no clearance (no glyph overlap).","C_D5_coverage_sheet01.png"),
 ("Part C",62):("MINOR NATIVE VARIANCE","P3","D5-touched slide; the right-hand table is flush with the slide right edge (table right boundary = slide width in the XML: zero right margin; all content visible). Geometry is in the file, identical in the ODI01-R1 candidate.","C_slide062_right_table_flush_to_edge_native.jpg; C_D5_coverage_sheet05.png"),

 ("Part B",2):("PASS","","Visually clean (flagged by extent metric only).","B_slide002_flagged_coverage.png"),
 ("Part C",2):("PASS","","Visually clean (flagged by extent metric only).","C_flagged_coverage_sheet01.png"),
 ("Part C",3):("MINOR NATIVE VARIANCE","P3","The third line of the placeholder list abuts the 'Edition states' line below it (no leading between them); both legible.","C_slide003_placeholder_lines_abut_zoom.jpg; C_flagged_coverage_sheet01.png"),
 ("Part C",20):("PASS","","Visually clean (flagged by extent metric only).","C_flagged_coverage_sheet01.png"),
 ("Part C",75):("PASS","","Visually clean (flagged by extent metric only).","C_flagged_coverage_sheet01.png"),
 ("Part C",77):("MINOR NATIVE VARIANCE","P3","'Edition state: WORKING EDITION · NOT RELEASED' renders; the release-status box text fills its box tightly.","C_flagged_coverage_sheet02.png"),
 ("Part B",3):("PASS","OBSERVATION","Run-in lead-ins ('Character.', 'Principles.', 'Tagline.', 'Not allowed.') render at regular weight: the hierarchy cue is gone. Accepted D5 consequence (400 only); bold not restored.","B_slide003_native.jpg"),
 ("Part B",4):("MINOR NATIVE VARIANCE","P3","Table row grows to three lines natively; the 'Authority order' and 'Source of truth' headings sit directly against the table bottom.","B_slide004_table_growth_native.jpg"),
 ("Part B",9):("PASS","","Families slide; 'Weights in use: 400 only...' wording correct; Arabic 'أب' shapes.","B_slide009_native.jpg"),
 ("Part B",10):("PASS","","Type styles table at regular weight; 'CURRENT IMPLEMENTATION: 400 for every row. 500: PENDING ACCEPTED FONT FILE.' visible.","B_slide010_native.jpg"),
 ("Part B",11):("PASS","","Tracking specimens render with the stated letter-spacing.","B_slide011_native.jpg"),
 ("Part B",12):("MINOR NATIVE VARIANCE","P3","Wt column shows 400; note present. Right-hand table last row grows to three lines and the paragraph below starts with no clearance (no glyph overlap).","B_slide012_native.jpg; B_slide012_table_to_paragraph_zoom.jpg"),
 ("Part B",13):("PASS","","Visually clean.","B_slide013_native.jpg"),
 ("Part B",18):("PASS","","Visually clean; third column clears the footer.","B_slide018_native.jpg"),
 ("Part B",19):("PASS","OBSERVATION","Visually clean. 'Voice (G01-G10).' lead-in at regular weight (accepted D5 consequence).","B_slide019_native.jpg"),
 ("Part B",21):("PASS","","Visually clean.","B_slide021_native.jpg"),
 ("Part B",22):("PASS","","'Navigates; underlined, 400, ink' wording present.","B_slide022_native.jpg"),
 ("Part B",24):("PASS","","Visually clean; RTL/screen-reader rows still show native QA PENDING (VAL-07/08).","B_slide024_native.jpg"),
 ("Part B",30):("REAL CANDIDATE DEFECT","P2","Token-excerpt box is shorter than its text (9 logical lines that wrap to 10 in Courier New). In native PowerPoint the last line ('motion · layout · locale') falls outside the dark box and is not visible, and the line above is partly clipped. The candidate's LibreOffice PDF shows all lines, so this is a native-only visible defect. Not fixed in NP01.","B_slide030_native.jpg; B_slide030_excerpt_box_overflow_zoom.jpg; B_slide030_candidate_PDF_LibreOffice_comparison.png"),
 ("Part B",33):("PASS","","Visually clean.","B_slide033_native.jpg"),
 ("Part B",35):("PASS","","Visually clean.","(inspected; screenshot not retained)"),
 ("Part C",15):("PASS","","'400 · 500 PENDING' and 'CURRENT IMPLEMENTED WEIGHT = 400 (Jost, Inter). 500 is PENDING ACCEPTED FONT FILE...' render correctly.","C_slide015_native.jpg"),
 ("Part C",27):("MINOR NATIVE VARIANCE","P3","Paragraph sits tight above the dashed boxes; no overlap.","C_slide027_native.jpg"),
 ("Part C",44):("PASS","","C2 wording renders: 'a Letterhead Set (Application Revision 03) exists as a WORKING APPLICATION / PENDING VALIDATION; no template is accepted.' Text wraps one line past its one-line box with clear space below.","C_slide044_native.jpg"),
 ("Part D",1):("PASS","","Opens cleanly; images intact; 'CONCEPT / NOT PRODUCTION ARTWORK' visible.","D_slide001_native.jpg"),
 ("Part D",9):("PASS","","Concept status retained ('CONCEPT / NOT PRODUCTION ARTWORK / DISPENSING FORMAT PENDING', 'v1.0 WORKING EDITION').","D_slide009_native.jpg"),
}

GEN = re.compile(r'^(Text|Shape|Table|Picture|Group|TextBox|Rectangle|Line|Title|Content Placeholder|Notes Placeholder|Slide Number Placeholder|Flow box)\s?\d+', re.I)
def lab(s):
    """Shape label for committed CSVs: generic PowerPoint names pass through; names that are really deck text become 'shape #<index>' so no governed excerpt enters committed evidence."""
    return s['name'] if GEN.match(s['name']) else f"shape #{s['idx']}"
ROWSTART = re.compile(r'^[SPNB]\t\d+\t')

def read_rows(path):
    rows, cur = [], None
    for line in open(path, encoding='utf8').read().split('\n'):
        if ROWSTART.match(line):
            if cur is not None: rows.append(cur)
            cur = line
        elif cur is not None and line != '':
            cur += ' ⏎ ' + line          # shape names/text containing line breaks
    if cur is not None: rows.append(cur)
    return [r.split('\t') for r in rows]

def analyze(part, path):
    doc = part.replace('_', ' ')
    shapes, bolds, notes = [], {}, {}
    for r in read_rows(path):
        if r[0] == 'S':
            d = dict(slide=int(r[1]), idx=r[2], name=r[3], stype=r[4], vis=r[5], txt='', fam='', bld='false', sz='', bh=0.0, sh=0.0, au='')
            if len(r) >= 18:
                d.update(fam=r[7], asc=r[8], ea=r[9], cs=r[10], bld=r[11], sz=r[12], bh=float(r[13] or 0), sh=float(r[14] or 0), au=r[16], txt=r[17] if len(r) > 17 else '')
            shapes.append(d)
        elif r[0] == 'B':
            bolds[(int(r[1]), r[2])] = dict(boldN=int(r[3]), nch=int(r[4]), firstB=int(r[5]), fset=r[6] if len(r) > 6 else '')
        elif r[0] == 'N':
            c = r[5] if len(r) > 5 else ''
            if 'Slide Number' not in r[3] and c.strip(): notes[int(r[1])] = c
    return doc, shapes, bolds, notes

def main(sweep, out):
    os.makedirs(out, exist_ok=True)
    slide_rows, font_rows, summary = [], [], {}
    for part in ("Part_A", "Part_B", "Part_C", "Part_D"):
        p = f"{sweep}/{part}.tsv"
        if not os.path.exists(p): continue
        doc, shapes, bolds, notes = analyze(part, p)
        by = collections.defaultdict(list)
        for s in shapes: by[s['slide']].append(s)
        tot = collections.Counter(); fams = collections.Counter()
        for sl in sorted(by):
            S = by[sl]; txts = [s for s in S if s['txt'].strip()]
            boldc = sum(bolds[(sl, s['idx'])]['boldN'] for s in txts if (sl, s['idx']) in bolds)
            mixed_flag = sum(1 for s in txts if s['bld'] == 'true')
            offfam, ar, over = set(), 0, []
            for s in txts:
                b = bolds.get((sl, s['idx'])); fs = {f for f in (b['fset'].split('|') if b else [s['fam']]) if f}
                s['fs'] = fs; fams.update(fs)
                for f in fs:
                    if f not in ALLOWED: offfam.add(f)
                if AR.search(s['txt']): ar += 1
                if s['bh'] > s['sh'] + 2.0: over.append(f"{lab(s)[:24]}(txt {s['bh']:.0f}>box {s['sh']:.0f},{s['au'].replace('ppAutoSize','')})")
            hidden = sum(1 for s in S if s['vis'] != 'true')
            res = "PASS (native property sweep)"
            if boldc: res = "REAL CANDIDATE DEFECT? bold characters present"
            elif offfam: res = "FONT-ENVIRONMENT ISSUE? non-brand family: " + ",".join(sorted(offfam))
            elif over: res = "REQUIRES NATIVE REVIEW (text extent exceeds box)"
            tot['bold'] += boldc; tot['over'] += bool(over); tot['hidden'] += hidden
            vis = VISUAL.get((doc, sl))
            if vis:
                res = f"{vis[0]}{(' ['+vis[1]+']') if vis[1] else ''} - visually inspected: {vis[2]}"
            elif over:
                res = "REQUIRES NATIVE REVIEW (text extent exceeds box by metric; NOT visually inspected)"
            slide_rows.append([doc, sl, len(S), len(txts), "; ".join(sorted({f for s in txts for f in s['fs']})), boldc, mixed_flag, ar, hidden,
                               ("YES " + "; ".join(over[:3])) if over else "no", "yes" if sl in notes else "empty/none", "yes" if sl in PRIORITY[doc] else "no", ("yes: " + vis[3]) if vis else "no", res])
            for s in txts:
                pri = sl in PRIORITY[doc]
                b = bolds.get((sl, s['idx'])); bc = b['boldN'] if b else 0
                exc = bc or (s['fs'] - ALLOWED)
                if pri or exc:
                    exp = "Jost / Inter / Noto Sans Arabic"
                    obs = "/".join(sorted(s['fs'])) or "?"
                    app = "Regular (0 bold chars, char-level)" if not bc else f"BOLD on {bc}/{b['nch']} chars"
                    font_rows.append([doc, sl, f"{lab(s)[:40]} [{s['idx']}]", exp, "400", obs, app, "not detectable by object model; family installed; no missing-font banner" if not (s['fs'] - ALLOWED) else "CHECK (non-brand family)", "no bold used (0 bold chars)" if not bc else "CHECK",
                                      "PASS" if not exc else "REQUIRES NATIVE REVIEW"])
        summary[doc] = dict(slides=len(by), text_shapes=sum(1 for s in shapes if s['txt'].strip()), bold_chars=tot['bold'], slides_with_extent_exceeding=tot['over'],
                            hidden_shapes=tot['hidden'], families=dict(fams), notes_slides_nonempty=len(notes))
        json.dump({"notes": notes}, open(f"{out}/{part}_notes.json", "w"), ensure_ascii=False, indent=1)
    for part in ("Part_A", "Part_B", "Part_C", "Part_D"):
        tp = f"{sweep}/{part}_tables.tsv"
        if not os.path.exists(tp): continue
        lines = open(tp, encoding='utf8').read().split('\n'); doc = part.replace('_', ' ')
        T = [l.split('\t') for l in lines if l.startswith('T\t')]; C = [l.split('\t') for l in lines if l.startswith('C\t')]
        K = [l.split('\t') for l in lines if l.startswith('K\t')]
        fam = sorted({c[5] for c in C}); bc = sum(int(k[5]) for k in K); rb = collections.Counter(c[6] for c in C)
        font_rows.append([doc, "ALL TABLES", f"{len(T)} tables / {len(C)} text cells (native table sweep)", "Jost / Inter / Noto Sans Arabic", "400", "/".join(fam), f"range bold values {dict(rb)}; {bc} bold chars after character-level drill", "not detectable by object model", "no bold used (0 bold chars)", "PASS" if bc == 0 and fam == ["Inter"] else "REQUIRES NATIVE REVIEW"])
        summary.setdefault(doc, {})["tables"] = len(T); summary[doc]["table_text_cells"] = len(C); summary[doc]["table_bold_chars"] = bc; summary[doc]["table_families"] = fam
    w = csv.writer(open(f"{out}/04_NP01_Native_Slide_Results.csv", "w", newline='', encoding='utf8'))
    w.writerow(["Document", "Slide", "Shapes", "Text shapes", "Native families (character-level where mixed)", "Bold characters", "Shapes reporting range-level mixed bold", "Arabic text shapes", "Hidden shapes", "Text extent exceeds box?", "Notes text present", "Priority slide", "Visually inspected (evidence file)", "Result (native property sweep + visual where stated)"]); w.writerows(slide_rows)
    w = csv.writer(open(f"{out}/06_NP01_Native_Font_Validation.csv", "w", newline='', encoding='utf8'))
    w.writerow(["Document", "Slide", "Element", "Allowed family set (per-role family not tested)", "Expected current weight", "Requested family (PowerPoint object model; a substituted face is not detectable)", "Observed native appearance (bold characters at character level)", "Substitution?", "Unaccepted font used?", "Result"]); w.writerows(font_rows)
    json.dump(summary, open(f"{out}/np01_sweep_summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1))
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
