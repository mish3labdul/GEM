"""Shared OOXML helpers for ODI01-R1 (stdlib + lxml only)."""
import zipfile,re
from lxml import etree
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','rel':'http://schemas.openxmlformats.org/package/2006/relationships'}
BRAND=('Jost','Inter','Noto Sans Arabic')
BOLD_VALS=('1','true','on')
ARABIC=re.compile('[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')
def slide_order(z):
    """[(slide_number, 'ppt/slides/slideN.xml')] in presentation order."""
    pres=etree.fromstring(z.read('ppt/presentation.xml'));rels=etree.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
    rid={r.get('Id'):r.get('Target') for r in rels}
    out=[]
    for i,s in enumerate(pres.find('p:sldIdLst',NS),1):
        t=rid[s.get('{%s}id'%NS['r'])];out.append((i,'ppt/'+t.lstrip('/').replace('ppt/','')))
    return out
def theme_fonts(z):
    t=etree.fromstring(z.read('ppt/theme/theme1.xml'));f=t.find('.//a:fontScheme',NS)
    return {'+mj-lt':f.find('a:majorFont/a:latin',NS).get('typeface'),'+mn-lt':f.find('a:minorFont/a:latin',NS).get('typeface')}
