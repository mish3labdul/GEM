"""AX01: build 02 candidate baseline, 11 PowerPoint correction register and 12 Word correction register from the edit log + inventory (identifiers only; shape names that may hold deck text are replaced by generic labels).
Usage: ax01_build_registers.py <repo_root> <package_dir>"""
import sys, os, re, csv, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]
log = json.load(open(f"{pkg}/20_qa/ax01_edit_log.json")); pix = {}
for r in json.load(open(f"{pkg}/20_qa/ax01_native_pixel_compare_all.json")): pix[(r[0], r[1])] = r[2]
rows = []; base = json.load(open(f"{pkg}/local_only/raw/baseline_rows.json"))
for label, d in log.items():
    for kind, st in d['steps'].items():
        L = st['log']
        if kind == 'title':
            for e in L['edits']:
                sl = int(re.search(r'slide(\d+)', e['part']).group(1)); rows.append([label, sl, f"shape id {e['shape_id']} (existing visible heading)", 'text box (no placeholder); not exposed as a slide title', '<p:ph type="title"/> on the same shape' + ('; explicit line spacing 100% pinned (previous effective value)' if e.get('pinned_to_preserve_appearance') else ''),
                             'Existing visible heading made the structural slide title (no text added)', 'VAL-08 scope (K01:K09, V01:V15); AX01 owner brief (meaningful titles, logical structure)', 'no', 'no', pix.get((label, sl), 'native capture: ' + ('see Part D sample' if label == 'Part D' else 'n/a')) if False else (pix.get((label, sl)) or 'not individually captured; Part D 24/24 native captures PIXEL-IDENTICAL')])
        elif kind == 'decorative':
            plan = json.load(open(f"{pkg}/local_only/raw/decorative_plan.json"))[label]
            for part, sid, name in plan:
                sl = int(re.search(r'slide(\d+)', part).group(1)); rows.append([label, sl, f"{gl(name, sid)} (id {sid})", 'no alt text and not marked decorative (flagged by checker)', 'marked decorative (adec:decorative val=1)', 'Hairline rule / panel behind text / large background field carries no information of its own (classification rules R1-R3)',
                             'AX01 task 6/12 Category A; WCAG 1.1.1 decorative treatment', 'no', 'no', pix.get((label, sl)) or 'not individually captured; deck-level LibreOffice raster identical' + (' (A/B/C)' if label != 'Part D' else '') + '; native checker count reduced'])
        else:
            plan = json.load(open(f"{pkg}/local_only/raw/table_plan.json"))[label]
            for part, sid, name in plan:
                sl = int(re.search(r'slide(\d+)', part).group(1)); rows.append([label, sl, f"{gl(name, sid)} (id {sid})", 'table without header-row flag', 'tblPr firstRow="1"', 'First row is a distinct column-header row (fill/colour/caps evidence); no table style is applied so no restyling', 'AX01 task 7; WCAG 1.3.1 info and relationships', 'no', 'no', pix.get((label, sl)) or 'not individually captured; deck-level LibreOffice raster identical; native checker "Missing table header" count reduced'])
H = ["Document", "Slide", "Object", "Before", "After", "Reason", "Authority", "Visible change?", "Content change?", "Native revalidation result"]
csv.writer(open(f"{pkg}/11_AX01_PowerPoint_Correction_Register.csv", 'w', newline='', encoding='utf8')).writerows([H] + rows)
csv.writer(open(f"{pkg}/12_AX01_Word_Correction_Register.csv", 'w', newline='', encoding='utf8')).writerows([["Template", "Change", "Reason"]] + [[t, 'NONE', 'Native Word Accessibility Assistant: "Looks good! No issues found." Static inventory: document title set, heading styles used on first pages, logo alt text present, no tables, no floating drawings, PAGE/NUMPAGES fields intact. No Word correction was warranted; no template was modified.'] for t in LETTERHEADS])
C = [["Document", "Path", "Lineage", "SHA-256", "Slide/page count", "Current status", "Accessibility evidence available before AX01", "Native checker completed before AX01?", "AX01 candidate (SHA-256)"]]
cand = {l: d['output_sha256'] for l, d in log.items()}
for label, path, lineage, sha, cnt, nat, status in [(b[0], b[1], b[2], b[3], b[4], b[5], b[6]) for b in base]:
    ev = 'NP01 observation (27 untitled, 58 reading-order, 313 no alt, 1 table header)' if label == 'Part A' else ('queue only (3 slides); checker stalled' if label == 'Part C' else 'none')
    C.append([label, path, lineage, sha, cnt, status, ev, 'Part A only' if label == 'Part A' else 'no', cand[label]])
for n in LETTERHEADS: C.append([f"Letterhead {n.replace('_', ' ')}", LH % n, 'Set v1.1 Application Revision 03 (WORKING APPLICATION / PENDING VALIDATION); 01_templates == 05_release', shaf(f"{root}/{LH % n}"), '1 page', 'working candidate (unapproved)', 'static OOXML audit (AR01), native Word layout (AR01); no accessibility checker', 'no', 'unchanged (no Word change)'])
csv.writer(open(f"{pkg}/02_AX01_Candidate_Baseline.csv", 'w', newline='', encoding='utf8')).writerows(C)
print(len(rows), 'correction rows;', collections.Counter(r[0] for r in rows))
