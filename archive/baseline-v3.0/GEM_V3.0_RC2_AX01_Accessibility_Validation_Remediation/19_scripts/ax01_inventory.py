"""AX01 task 1-2 (read-only): candidate baseline + PowerPoint structural inventory. Committed outputs hold identifiers/counts only (no deck text);
the per-object table (object names/ids/geometry/text length) is written to local_only/raw.
Usage: ax01_inventory.py <repo_root> <package_dir>   (docling venv python)"""
import sys, os, csv, json, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
root, pkg = sys.argv[1:3]
slide_rows, obj_rows, tbl_rows, base_rows = [], [], [], []
for key, (label, path, lineage) in DECKS.items():
    z = zipfile.ZipFile(f"{root}/{path}"); order = slide_order(z)
    core = z.read('docProps/core.xml').decode('utf8', 'ignore'); title = re.search(r'<dc:title>(.*?)</dc:title>', core, re.S)
    base_rows.append([label, path, lineage, shaf(f"{root}/{path}"), f"{len(order)} slides", 'PowerPoint (native checker NP01: Part A only run to completion; Part C stalled; B, D not run)' if key in 'ABCD' else '', 'unapproved controlled candidate'])
    for n, part in enumerate(order, 1):
        root_el = etree.fromstring(z.read(part)); tree = root_el.find('.//p:spTree', ns); objs = list(walk(tree))
        lay = layout_of(z, part); lroot = etree.fromstring(z.read(lay)); lname = lroot.find('.//p:cSld', ns).get('name')
        lay_title = lroot.xpath('.//p:sp/p:nvSpPr/p:nvPr/p:ph[@type="title" or @type="ctrTitle"]', namespaces=ns)
        titles = [o for o in objs if o['placeholder'] in ('title', 'ctrTitle')]
        rel = etree.fromstring(z.read(part.replace('slides/', 'slides/_rels/') + '.rels')); notes = any(r.get('Type').endswith('/notesSlide') for r in rel)
        langs = collections.Counter(re.findall(r'<a:rPr lang="([^"]*)"', z.read(part).decode('utf8')))
        kinds = collections.Counter(o['kind'] for o in objs)
        for o in objs:
            alt = 'decorative' if o['decorative'] else ('alt' if o['descr'].strip() else 'none')
            obj_rows.append([label, n, o['z'], o['id'], o['name'], o['kind'], o['placeholder'] or '', 'text' if o['has_text'] else 'no-text', o['text_len'], alt, len(o['descr']), 'hidden' if o['hidden'] else '', o['in_group'] or '', o['x'], o['y'], o['cx'], o['cy'], 'Arabic' if o['arabic'] else '', o['hlink']])
            if o['kind'] == 'table':
                tbl = o['el'].find('.//a:tbl', ns); pr = tbl.find('a:tblPr', ns); rows = tbl.findall('a:tr', ns); cells = [c for r in rows for c in r.findall('a:tc', ns)]
                tbl_rows.append([label, n, o['id'], o['name'], len(rows), len(tbl.findall('a:tblGrid/a:gridCol', ns)), pr.get('firstRow') or '0', pr.get('firstCol') or '0', pr.get('bandRow') or '0',
                                 sum(1 for c in cells if c.get('gridSpan') or c.get('rowSpan') or c.get('hMerge') or c.get('vMerge')), sum(1 for c in cells if not text_of(c).strip()), len(cells), 'alt' if o['descr'].strip() else 'none'])
        slide_rows.append([label, n, os.path.basename(part), lname, 'yes' if lay_title else 'no', len(titles), 'yes' if titles and any(t['has_text'] for t in titles) else ('title placeholder EMPTY' if titles else 'no title placeholder'),
                           'DUPLICATE' if len(titles) > 1 else '', 'hidden' if any(t['hidden'] for t in titles) else '', len(objs), kinds['pic'], kinds['grpSp'], kinds['table'], kinds['chart'], kinds['cxnSp'],
                           sum(1 for o in objs if o['kind'] == 'sp' and o['has_text']), sum(1 for o in objs if o['kind'] == 'sp' and not o['has_text']),
                           sum(1 for o in objs if o['decorative']), sum(1 for o in objs if o['descr'].strip()), sum(1 for o in objs if o['kind'] in ('pic', 'sp', 'grpSp', 'cxnSp', 'graphicFrame', 'table', 'chart') and not o['has_text'] and not o['descr'].strip() and not o['decorative']),
                           sum(o['hlink'] for o in objs), sum(1 for o in objs if o.get('media')), 'yes' if notes else 'no', 'hidden' if root_el.get('show') == '0' else '', ';'.join(f"{k}={v}" for k, v in sorted(langs.items())), 'yes' if any(o['arabic'] for o in objs) else '', 'yes' if any(o['hidden'] for o in objs) else ''])
    print(label, len(order), 'slides', len([r for r in obj_rows if r[0] == label]), 'objects')
H = ["Document", "Slide", "Part", "Layout", "Layout has title placeholder", "Title placeholders on slide", "Recognized title", "Duplicate title", "Hidden title", "Objects (incl. grouped)", "Pictures", "Groups", "Tables", "Charts", "Connectors", "Text shapes", "Non-text shapes", "Marked decorative", "Objects with alt text", "Non-text objects with neither alt text nor decorative flag (static predicate)", "Hyperlinks", "Media", "Notes slide", "Slide hidden", "Run languages (count)", "Arabic content", "Hidden objects"]
os.makedirs(f"{pkg}/local_only/raw", exist_ok=True)
csv.writer(open(f"{pkg}/03_AX01_Structural_Inventory.csv", 'w', newline='', encoding='utf8')).writerows([H] + slide_rows)
csv.writer(open(f"{pkg}/local_only/raw/objects.csv", 'w', newline='', encoding='utf8')).writerows([["Document", "Slide", "Z-order", "Shape id", "Shape name", "Kind", "Placeholder", "Text?", "Text length", "Alt state", "Alt length", "Hidden", "Group id", "x", "y", "cx", "cy", "Arabic", "Hyperlinks"]] + obj_rows)
csv.writer(open(f"{pkg}/local_only/raw/tables.csv", 'w', newline='', encoding='utf8')).writerows([["Document", "Slide", "Shape id", "Shape name", "Rows", "Cols", "firstRow", "firstCol", "bandRow", "Merged cells", "Empty cells", "Cells", "Alt"]] + tbl_rows)
json.dump(base_rows, open(f"{pkg}/local_only/raw/baseline_rows.json", 'w'))
print('tables:', len(tbl_rows))
