"""NP01-R1 detection only (no PowerPoint, no edits): inset-aware overflow scan of filled or outlined text boxes.
Inputs: NP01 native sweep TSVs (text bounds height 'bh', shape height 'sh', points) + the four candidate PPTX slide XML (fill/outline, bodyPr insets).
A box is flagged if tIns + bh + bIns > sh + 0.5pt (box content would not fit inside the visible container).
Usage: np01r1_inset_aware_scan.py <repo_root> <sweep_dir> <out_csv>"""
import sys, re, csv, zipfile, collections
root, sweep, outc = sys.argv[1:4]
DECKS = {
 "Part A": ("Part_A", "GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/GEM Brand Guidelines V3.0 — Part A — RC2 — D3 CANDIDATE (UNAPPROVED).pptx"),
 "Part B": ("Part_B", "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Digital Design System V3.0 — Part B — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx"),
 "Part C": ("Part_C", "GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/GEM Production Standards V3.0 — Part C — RC2 — D3 CANDIDATE (UNAPPROVED).pptx"),
 "Part D": ("Part_D", "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx"),
}
ROWSTART = re.compile(r'^[SPNB]\t\d+\t')
def sweep_rows(p):
    rows, cur = [], None
    for line in open(p, encoding='utf8').read().split('\n'):
        if ROWSTART.match(line):
            if cur is not None: rows.append(cur)
            cur = line
        elif cur is not None and line != '': cur += ' ⏎ ' + line
    if cur is not None: rows.append(cur)
    return [r.split('\t') for r in rows]
def emu(v, d): return (int(v) if v is not None else d) / 12700
out = []; summary = collections.Counter()
for doc, (tag, path) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}")
    sw = collections.defaultdict(list)
    for r in sweep_rows(f"{sweep}/{tag}.tsv"):
        if r[0] == 'S' and len(r) >= 18 and r[17].strip(): sw[(int(r[1]), r[3])].append(r)
    for n in sorted((n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)), key=lambda s: int(re.findall(r'\d+', s)[0])):
        sl = int(re.findall(r'\d+', n)[0]); x = z.read(n).decode('utf8')
        for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S):
            b = m.group(0); name = re.search(r'name="([^"]*)"', b).group(1)
            sp = re.search(r'<p:spPr>(.*?)</p:spPr>', b, re.S); sp = sp.group(1) if sp else ''
            ln = re.search(r'<a:ln\b.*?(?:</a:ln>|/>)', sp, re.S); lnx = ln.group(0) if ln else ''
            sp_no_ln = sp.replace(lnx, '')
            filled = '<a:solidFill>' in sp_no_ln; outlined = '<a:solidFill>' in lnx or 'prstDash' in lnx
            if not (filled or outlined) or (sl, name) not in sw: continue
            if len(sw[(sl, name)]) != 1: summary['skipped_duplicate_name'] += 1; continue
            bp = re.search(r'<a:bodyPr([^>]*)>', b); bp = bp.group(1) if bp else ''
            g = lambda k, d: emu(re.search(k + r'="(\d+)"', bp).group(1) if re.search(k + r'="(\d+)"', bp) else None, d / 12700)
            tI, bI = g('tIns', 45720), g('bIns', 45720)
            r = sw[(sl, name)][0]; bh, sh = float(r[13]), float(r[14]); need = tI + bh + bI; over = need - sh; glyph = tI + bh - sh
            auto = ('normAutofit' in b) or ('spAutoFit' in b)
            summary['boxes'] += 1
            out.append([doc, sl, name, 'filled' if filled else 'outlined', f"{tI:.1f}", f"{bI:.1f}", f"{bh:.1f}", f"{sh:.1f}", f"{need:.1f}", f"{over:.1f}", f"{glyph:.1f}", 'AUTOFIT' if auto else 'fixed', 'FLAG' if over > 0.5 else 'ok'])
            if over > 0.5: summary['flag'] += 1
out.sort(key=lambda r: -float(r[9]))
w = csv.writer(open(outc, 'w', newline='', encoding='utf8'))
w.writerow(["Document", "Slide", "Shape", "Container", "tIns pt", "bIns pt", "Text bounds height pt (native)", "Box height pt", "Needed = tIns+text+bIns pt", "Overflow pt incl. bottom inset (needed - box)", "Glyph overflow pt beyond box edge (tIns+text-box; >0 = text escapes the container)", "Autofit?", "Result"]); w.writerows(out)
print(dict(summary)); [print(r) for r in out if r[12] == 'FLAG']
