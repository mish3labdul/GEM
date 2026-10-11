"""AX01 task 2/9 (read-only): Word template structural accessibility inventory (identifiers/counts only). Usage: ax01_word_inventory.py <repo_root> <package_dir>"""
import sys, os, re, csv, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from ax01_common import *
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'; wns = {'w': W, 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing', 'a': A, 'dc': 'http://purl.org/dc/elements/1.1/'}
root, pkg = sys.argv[1:3]; rows = []; imgs = []
for name in LETTERHEADS:
    p = f"{root}/{LH % name}"; z = zipfile.ZipFile(p); doc = etree.fromstring(z.read('word/document.xml')); core = z.read('docProps/core.xml').decode('utf8', 'ignore'); sett = z.read('word/settings.xml').decode('utf8', 'ignore')
    t = re.search(r'<dc:title>(.*?)</dc:title>', core); lang = re.search(r'<dc:language>(.*?)</dc:language>', core)
    paras = doc.findall('.//w:body/w:p', wns); styles = collections.Counter((p.find('w:pPr/w:pStyle', wns).get('{%s}val' % W) if p.find('w:pPr/w:pStyle', wns) is not None else 'Normal') for p in paras)
    heads = sum(v for k, v in styles.items() if re.match(r'(?i)heading|title', k))
    blank = sum(1 for p in paras if not ''.join(p.xpath('.//w:t/text()', namespaces=wns)).strip() and not p.xpath('.//w:drawing|.//w:pict|.//w:sectPr|.//w:br', namespaces=wns))
    parts = [n for n in z.namelist() if re.match(r'word/(header|footer)\d*\.xml$', n)]
    fields = sum(len(re.findall(r'<w:instrText[^>]*>\s*(PAGE|NUMPAGES)', z.read(n).decode('utf8'))) for n in parts)
    dr = [(n, d) for n in ['word/document.xml'] + parts for d in etree.fromstring(z.read(n)).iterfind('.//w:drawing', wns)]
    for n, d in dr:
        dp = d.find('.//wp:docPr', wns); inline = d.find('wp:inline', wns) is not None
        imgs.append([name, n.replace('word/', ''), dp.get('id'), dp.get('name'), 'inline' if inline else 'floating (anchor)', 'yes' if (dp.get('descr') or '').strip() else 'NO', 'yes' if d.xpath('.//*[local-name()="decorative"]') else 'no', len((dp.get('descr') or ''))])
    langs = collections.Counter(re.findall(r'<w:lang [^>]*?w:val="([^"]*)"', z.read('word/document.xml').decode('utf8')) + sum([re.findall(r'<w:lang [^>]*?w:val="([^"]*)"', z.read(n).decode('utf8')) for n in parts], []))
    sty = z.read('word/styles.xml').decode('utf8', 'ignore')
    rows.append([name, shaf(p), 'yes: set' if t and t.group(1).strip() else 'NO document title in core properties', 'yes' if 'updateFields' in sett else 'no', len(paras), heads, 'no Heading/Title styles used (all paragraphs Normal or custom)' if heads == 0 else f'{heads} heading paragraphs', len(doc.findall('.//w:tbl', wns)), len(dr), sum(1 for n, d in dr if d.find('wp:anchor', wns) is not None),
                 blank, len(parts), fields, 'yes' if doc.xpath('.//w:sectPr/w:titlePg', namespaces=wns) else 'no', 'yes' if doc.xpath('.//w:bidi', namespaces=wns) else 'no', ';'.join(f'{k}={v}' for k, v in sorted(langs.items())) or 'none', 'yes' if re.search(r'<w:lang [^>]*w:val="[^"]*"', sty) else 'no (docDefaults lang absent)'])
H = ["Template", "SHA-256", "Document title (core properties)", "updateFields set", "Body paragraphs", "Heading/Title-style paragraphs", "Heading structure", "Tables", "Drawings (body+header/footer)", "Floating drawings", "Blank spacing paragraphs", "Header/footer parts", "PAGE/NUMPAGES fields", "Different first page", "RTL paragraphs (w:bidi)", "Run languages (count)", "Default language in styles"]
csv.writer(open(f"{pkg}/local_only/raw/word_inventory.csv", 'w', newline='', encoding='utf8')).writerows([H] + rows)
csv.writer(open(f"{pkg}/local_only/raw/word_drawings.csv", 'w', newline='', encoding='utf8')).writerows([["Template", "Part", "docPr id", "docPr name", "Placement", "Alt text present", "Decorative flag", "Alt length"]] + imgs)
for r in rows: print(r[0], '| title:', r[2][:30], '| heads', r[5], '| tables', r[7], '| drawings', r[8], '| floating', r[9], '| blank', r[10], '| fields', r[12])
for r in imgs: print(r)
