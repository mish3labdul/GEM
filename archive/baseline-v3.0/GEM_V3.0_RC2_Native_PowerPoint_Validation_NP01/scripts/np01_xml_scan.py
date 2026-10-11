"""NP01 read-only XML pre-scan of candidate PPTX files (no writes). Usage: np01_xml_scan.py <pptx>..."""
import sys, zipfile, re, json, collections
BOLD = re.compile(r'\bb="(?:1|true|on)"')
AR = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
def scan(path):
    z = zipfile.ZipFile(path); names = z.namelist()
    r = {"file": path.split('/')[-1]}
    slides = sorted((n for n in names if re.match(r'ppt/slides/slide\d+\.xml$', n)), key=lambda n:int(re.findall(r'\d+',n)[0]))
    r["slides"] = len(slides)
    r["notesSlides"] = len([n for n in names if re.match(r'ppt/notesSlides/notesSlide\d+\.xml$', n)])
    r["charts"] = [n for n in names if n.startswith('ppt/charts/') and n.endswith('.xml')]
    r["diagrams"] = [n for n in names if n.startswith('ppt/diagrams/') and n.endswith('.xml')]
    r["embedded_fonts"] = 'embeddedFont' in z.read('ppt/presentation.xml').decode('utf8','ignore')
    r["media_external_links"] = [n for n in names if n.endswith('.rels') and b'TargetMode="External"' in z.read(n)]
    pres = z.read('ppt/presentation.xml').decode('utf8','ignore')
    r["defaultTextStyle_bold"] = len(BOLD.findall(pres))
    bold = collections.Counter()
    for n in names:
        if n.endswith('.xml') and re.match(r'ppt/(slides|slideLayouts|slideMasters|notesSlides|notesMasters|handoutMasters|charts|diagrams|theme)/', n):
            c = len(BOLD.findall(z.read(n).decode('utf8','ignore')))
            if c: bold[n] = c
    r["explicit_bold_parts"] = dict(bold)
    tsid = collections.Counter(); flags = collections.Counter()
    for n in slides:
        x = z.read(n).decode('utf8','ignore')
        for m in re.findall(r'<a:tableStyleId>([^<]+)</a:tableStyleId>', x): tsid[m]+=1
        for m in re.findall(r'<a:tblPr([^>]*)>', x):
            for f in re.findall(r'(firstRow|firstCol|lastRow|lastCol|bandRow|bandCol)="1"', m): flags[f]+=1
    r["tableStyleIds"] = dict(tsid); r["tableFlags"] = dict(flags)
    ts = z.read('ppt/tableStyles.xml').decode('utf8','ignore') if 'ppt/tableStyles.xml' in names else ''
    r["tableStyles_defined_ids"] = re.findall(r'styleId="([^"]+)"', ts)
    r["tableStyles_bold_tokens"] = len(re.findall(r'<a:tcTxStyle[^>]*\bb="on"', ts))
    ar = {}
    for i, n in enumerate(slides, 1):
        x = z.read(n).decode('utf8','ignore')
        runs = re.findall(r'<a:r>(.*?)</a:r>', x, re.S)
        k = [rr for rr in runs if AR.search(re.sub(r'<[^>]+>','',rr))]
        if k:
            cs = sum(1 for rr in k if re.search(r'<a:cs typeface="Noto Sans Arabic"', rr))
            ar[i] = {"arabic_runs": len(k), "runs_with_cs_noto": cs, "rtl_paras": len(re.findall(r'rtl="1"', x))}
    r["arabic_slides"] = ar
    return r
if __name__ == "__main__":
    print(json.dumps([scan(p) for p in sys.argv[1:]], ensure_ascii=False, indent=1))
