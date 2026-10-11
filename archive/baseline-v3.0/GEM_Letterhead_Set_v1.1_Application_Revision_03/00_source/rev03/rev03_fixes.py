"""GEM Letterhead Set v1.1 Application Revision 03 - DOCX corrections.

Applied to Revision 02 templates, QA fixtures and the specification. Idempotent.
Usage: python rev03_fixes.py <docx> [<docx> ...]   (files are rewritten in place inside the new derivative only)

R03-01  Word font-embedding settings. Revision 02 sets w:embedTrueTypeFonts + w:embedSystemFonts. A native
        Word for Mac save then embeds Times New Roman, Calibri, Cambria, Arial, Symbol, Courier and Inter /
        Noto Sans Arabic Bold/Italic (21 parts, 12.3 MB, 4 zero-byte) - unused, third-party fonts that the
        package has no right to redistribute. Remove w:embedSystemFonts and add w:saveSubsetFonts, so Word
        embeds only characters actually used. The delivered templates keep their three full Regular payloads.
R03-00  docProps/core.xml: revision label "Application Revision 03" and modified date 2026-10-08 (metadata only).
R03-02  Mixed-direction identifiers. A Latin run (rtl=0) inside an RTL paragraph begins/ends with neutral
        punctuation ("[DATE]", "[REFERENCE NUMBER]", e-mail/URL/phone) that the Unicode bidi algorithm resolves
        RTL. It looks right but copy/search returns broken bracket order (macOS PDFKit: 0 hits for
        "[REFERENCE NUMBER]"). Bound each such run with U+200E LEFT-TO-RIGHT MARK (invisible, no glyph).
R03-07  Arabic/Bilingual Continuation placeholder "[نص الصفحة التالية]": ASCII brackets in a Noto Sans Arabic RTL
        run are silently dropped by the LibreOffice PDF export used for the published PDFs (Word draws them).
        Use the set's own Arabic placeholder punctuation: «نص الصفحة التالية».
R03-08  Footer PAGE/NUMPAGES: w:fldSimple results take the paragraph style size (10.5 pt) in LibreOffice exports,
        so digits print larger than "Page ... of". Rewrite each as an equivalent complex field (begin/instr/
        separate/result/end) carrying the existing 9 pt Inter Ink run properties. Same live field codes.
"""
import copy
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
N = {'w': W}
q = lambda t: '{%s}%s' % (W, t)
LRM = '‎'
LATIN = re.compile(r'[A-Za-z0-9\[\]@/:+]')


def fix_settings(xml):
    xml = xml.replace('<w:embedSystemFonts/>', '')
    if '<w:saveSubsetFonts/>' not in xml:
        xml = xml.replace('<w:embedTrueTypeFonts/>', '<w:embedTrueTypeFonts/><w:saveSubsetFonts/>')
    return xml


def isolate(root):
    changed = 0
    for p in root.iter(q('p')):
        bidi = p.find('w:pPr/w:bidi', N)
        if bidi is None or bidi.get(q('val'), '1') in ('0', 'false'):
            continue
        for r in p.iter(q('r')):
            rtl = r.find('w:rPr/w:rtl', N)
            if rtl is None or rtl.get(q('val'), '1') not in ('0', 'false'):
                continue
            ts = r.findall('w:t', N)
            text = ''.join(t.text or '' for t in ts)
            if not ts or not LATIN.search(text) or text.strip().startswith(LRM):
                continue
            first, last = ts[0], ts[-1]
            lead = re.match(r'\s*', first.text or '').group(0)
            first.text = lead + LRM + (first.text or '')[len(lead):]
            trail = re.search(r'\s*$', last.text or '').group(0)
            core = (last.text or '')[:len(last.text or '') - len(trail)]
            last.text = core + LRM + trail
            for t in (first, last):
                t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            changed += 1
    return changed


def complexify(root):
    n = 0
    for fs in list(root.iter(q('fldSimple'))):
        instr = fs.get(q('instr'))
        res = fs.find(q('r'))
        rpr = res.find(q('rPr'))

        def run(child):
            r = E.Element(q('r'))
            if rpr is not None:
                r.append(copy.deepcopy(rpr))
            r.append(child)
            return r
        b = E.Element(q('fldChar')); b.set(q('fldCharType'), 'begin')
        it = E.Element(q('instrText')); it.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); it.text = ' ' + instr + ' '
        sp = E.Element(q('fldChar')); sp.set(q('fldCharType'), 'separate')
        en = E.Element(q('fldChar')); en.set(q('fldCharType'), 'end')
        runs = [run(b), run(it), run(sp), copy.deepcopy(res), run(en)]
        parent = fs.getparent(); i = parent.index(fs); parent.remove(fs)
        for k, r in enumerate(runs):
            parent.insert(i + k, r)
        n += 1
    return n


def fix_core(xml):
    """R03 metadata: revision label and modification date only."""
    xml = xml.replace('Application Revision 02', 'Application Revision 03')
    xml = re.sub(r'; 2026-10-07</dc:subject>', '; 2026-10-08</dc:subject>', xml)
    xml = re.sub(r'(<dcterms:modified xsi:type="dcterms:W3CDTF">)[^<]*(</dcterms:modified>)', r'\g<1>2026-10-08T00:00:00Z\2', xml)
    return xml


def process(path):
    path = Path(path)
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    log = {'file': path.name, 'isolated_runs': 0}
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info, data in items:
            n = info.filename
            if n == 'docProps/core.xml':
                data = fix_core(data.decode('utf-8')).encode('utf-8')
            elif n == 'word/settings.xml':
                data = fix_settings(data.decode('utf-8')).encode('utf-8')
            elif re.match(r'word/(document|header\d+|footer\d+)\.xml$', n):
                root = E.fromstring(data)
                c = isolate(root)
                log['isolated_runs'] += c
                f = complexify(root) if n.startswith('word/footer') else 0
                log['complex_fields'] = log.get('complex_fields', 0) + f
                p = 0
                for t in root.iter(q('t')):
                    if t.text == '[نص الصفحة التالية]':
                        t.text = '«نص الصفحة التالية»'; p += 1
                log['placeholder_punctuation'] = log.get('placeholder_punctuation', 0) + p
                if c or f or p:
                    data = E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
            zout.writestr(info, data)
    return log


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(process(f))
