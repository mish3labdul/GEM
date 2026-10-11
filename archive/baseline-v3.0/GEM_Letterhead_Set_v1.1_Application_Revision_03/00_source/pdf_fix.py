from pathlib import Path
import re,json,unicodedata
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,TextStringObject,DecodedStreamObject,DictionaryObject,ArrayObject,NumberObject
R=Path('work/GEM/GEM_Letterhead_Set_v1.1');TMP=Path('work/letterhead_revision_02/render')
log=[]
def repair(src,dst,lang='en-GB'):
 reader=PdfReader(src);writer=PdfWriter();writer.clone_document_from_reader(reader)
 # Derive missing mappings only from explicit exporter ActualText, not guessed Arabic.
 fixes=[]
 for pi,p in enumerate(writer.pages):
  stream=p.get_contents().get_data().decode('latin1')
  for cluster,block in re.findall(r'/Span\s*<<\s*/ActualText\s*<FEFF([0-9A-F]+)>\s*>>\s*BDC(.*?)EMC',stream,re.S|re.I):
   intended=bytes.fromhex(cluster).decode('utf-16-be')
   shows=re.findall(r'/([A-Za-z0-9]+)\s+[0-9.]+\s+Tf\s*<([0-9A-F]+)>\s*Tj',block,re.I)
   if not shows:continue
   known=[];missing=[]
   for fn,code in shows:
    font=p['/Resources']['/Font']['/'+fn].get_object();cmap=font['/ToUnicode'].get_data().decode('latin1')
    m=re.search(r'<'+code+r'>\s*<([0-9A-F]+)>',cmap,re.I)
    if m:
     val=bytes.fromhex(m.group(1)).decode('utf-16-be')
     # Exporter can allocate a whole cluster to the base and omit the separate mark.
     if len(val)>1 and any(unicodedata.combining(c) for c in val):
      base=''.join(c for c in val if not unicodedata.combining(c))
      cmap=cmap[:m.start(1)]+base.encode('utf-16-be').hex().upper()+cmap[m.end(1):]
      ss=DecodedStreamObject();ss.set_data(cmap.encode('latin1'));font[NameObject('/ToUnicode')]=writer._add_object(ss);val=base
     known.append(val)
    else:missing.append((font,code,fn,cmap))
   remaining=intended
   for val in known:
    for c in val:remaining=remaining.replace(c,'',1)
   if missing:
    assert len(missing)==1 and len(remaining)==1,(intended,known,missing)
    font,code,fn,cmap=missing[0];cmap=font['/ToUnicode'].get_data().decode('latin1');mapping=f'<{code}> <{remaining.encode("utf-16-be").hex().upper()}>'
    cmap=re.sub(r'(\d+) beginbfchar',lambda m:str(int(m.group(1))+1)+' beginbfchar',cmap,count=1)
    cmap=cmap.replace('endbfchar',mapping+'\nendbfchar',1)
    s=DecodedStreamObject();s.set_data(cmap.encode('latin1'));font[NameObject('/ToUnicode')]=writer._add_object(s)
    fixes.append({'page':pi+1,'font':fn,'code':code,'unicode':f'U+{ord(remaining):04X}','evidence':'Exporter ActualText '+intended})
 # Preserve native logical paragraph text in the semantic tree.
 from zipfile import ZipFile
 from lxml import etree as E
 docpath=(R/'01_templates'/src.with_suffix('.docx').name) if not src.stem.startswith('QA_') else (R/'04_qa/fixtures'/src.with_suffix('.docx').name)
 if docpath.exists() and not src.stem.startswith('QA_'):
  doc=E.fromstring(ZipFile(docpath).read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  texts=[''.join((t.text or '') if t.tag=='{'+ns['w']+'}t' else '\n' if t.tag=='{'+ns['w']+'}br' else ' ' if t.tag=='{'+ns['w']+'}tab' else '' for t in p.iter()) for p in doc.findall('w:body/w:p',ns)]
  texts=[t for t in texts if t.strip()]
  st=writer.root_object.get('/StructTreeRoot')
  if st:
   elements=[]
   def walk(v):
    v=v.get_object() if hasattr(v,'get_object') else v
    if isinstance(v,list):
     for vv in v:walk(vv)
    elif isinstance(v,dict):
     if v.get('/S') in ['/Standard','/Text body','/P','/H1','/H2']:elements.append(v)
     if '/K' in v:walk(v['/K'])
   walk(st)
   assert len(elements)==len(texts),(src,len(elements),len(texts))
   for el,t in zip(elements,texts):
    if el.get('/S') in ['/Standard','/Text body']:el[NameObject('/S')]=NameObject('/P')
    el[NameObject('/ActualText')]=TextStringObject(t)
    el[NameObject('/Lang')]=TextStringObject('ar-SA' if any('\u0600'<=c<='\u06ff' for c in t) else 'en-GB')
 # Carry the meaningful source logo alternative into the exported vector figure.
 if 'First_Page' in src.stem or src.stem in ['GEM_Letterhead_Executive','GEM_Letterhead_Minimal']:
  for pp in writer.pages:
   stream=pp.get_contents().get_data().decode('latin1')
   matches=[m for m in re.finditer(r'/Artifact BMC(.*?)EMC',stream,re.S) if m.group(1).count('f*')>=5]
   if matches:
    assert len(matches)==1
    st=writer.root_object['/StructTreeRoot'];doc=st['/K'][0].get_object();oldnums=st['/ParentTree']['/Nums'];idx=int(pp['/StructParents']);arr=next(oldnums[j+1].get_object() for j in range(0,len(oldnums),2) if int(oldnums[j])==idx);mcid=len(arr)
    fig=DictionaryObject({NameObject('/Type'):NameObject('/StructElem'),NameObject('/S'):NameObject('/Figure'),NameObject('/P'):doc.indirect_reference,NameObject('/Pg'):pp.indirect_reference,NameObject('/K'):NumberObject(mcid),NameObject('/Alt'):TextStringObject('GEM trademark horizontal logo from the supplied official vector kit. Production-master acceptance pending.')})
    ref=writer._add_object(fig);arr.append(ref);doc['/K'].insert(0,ref);m=matches[0]
    stream=stream[:m.start()]+f'/Figure <</MCID {mcid}>> BDC'+m.group(1)+'EMC'+stream[m.end():];ss=DecodedStreamObject();ss.set_data(stream.encode('latin1'));pp[NameObject('/Contents')]=writer._add_object(ss)
 writer.root_object[NameObject('/Lang')]=TextStringObject(lang)
 writer.add_metadata({'/Title':'GEM Branded Letterhead Set v1.1 Application Revision 02 '+dst.stem.replace('GEM_Letterhead_','').replace('_',' '),'/Subject':'WORKING APPLICATION / PENDING VALIDATION'+('; PENDING LOCALIZATION APPROVAL' if lang=='ar-SA' else ''),'/Author':'','/CreationDate':'D:20261007150000+03\'00\'','/ModDate':'D:20261007150000+03\'00\''})
 writer.write(dst);log.append({'file':str(dst.relative_to(R)),'mapping_repairs':fixes})
for f in (R/'01_templates').glob('*.docx'):
 repair(TMP/f.stem/(f.stem+'.pdf'),R/'02_pdf'/(f.stem+'.pdf'),'ar-SA' if 'Arabic' in f.name or 'Bilingual' in f.name else 'en-GB')
for f in (R/'04_qa/fixtures').glob('*.docx'):
 repair(TMP/f.stem/(f.stem+'.pdf'),R/'04_qa/evidence'/(f.stem+'.pdf'),'en-GB' if 'English' in f.name else 'ar-SA')
# Merge tagged individual PDFs using the writer's structure-preserving append.
order=['English_First_Page','English_Continuation','Arabic_First_Page','Arabic_Continuation','Bilingual_First_Page','Bilingual_Continuation','Executive','Minimal']
for typ in ['Digital','Print']:
 w=PdfWriter();tree=DictionaryObject({NameObject('/Type'):NameObject('/StructTreeRoot')});tree_ref=w._add_object(tree);kids=ArrayObject();nums=ArrayObject();offset=0
 for title in order:
  rr=PdfReader(R/'02_pdf'/('GEM_Letterhead_'+title+'.pdf'));pagebase=len(w.pages);w.append(rr,outline_item=title.replace('_',' '),import_outline=False)
  st=rr.trailer['/Root'].get('/StructTreeRoot')
  if st:
   st=st.get_object();kk=st.get('/K');items=kk if isinstance(kk,list) else [kk]
   for k in items:
    cc=k.clone(w);cc.get_object()[NameObject('/P')]=tree_ref;cc.get_object()[NameObject('/Lang')]=TextStringObject('ar-SA' if 'Arabic' in title or 'Bilingual' in title else 'en-GB');kids.append(cc)
   parent=st['/ParentTree'].get_object();oldnums=parent.get('/Nums',[])
   assert oldnums,'ParentTree nested number tree requires additional handling'
   for j in range(0,len(oldnums),2):nums.extend([NumberObject(int(oldnums[j])+offset),oldnums[j+1].clone(w)])
   for j,pp in enumerate(w.pages[pagebase:]):
    if '/StructParents' in rr.pages[j]:pp[NameObject('/StructParents')]=NumberObject(int(rr.pages[j]['/StructParents'])+offset)
   offset+=max(int(oldnums[j]) for j in range(0,len(oldnums),2))+1
 tree[NameObject('/K')]=kids;tree[NameObject('/ParentTree')]=w._add_object(DictionaryObject({NameObject('/Nums'):nums}));tree[NameObject('/ParentTreeNextKey')]=NumberObject(offset)
 w.root_object[NameObject('/StructTreeRoot')]=tree_ref;w.root_object[NameObject('/MarkInfo')]=DictionaryObject({NameObject('/Marked'):__import__('pypdf').generic.BooleanObject(True)})
 w.root_object[NameObject('/Lang')]=TextStringObject('en-GB')
 w.add_metadata({'/Title':'GEM Branded Letterhead Set v1.1 Application Revision 02 '+typ,'/Author':'','/Subject':'WORKING APPLICATION / PENDING VALIDATION'+('; PENDING PREPRESS STANDARD / PENDING PHYSICAL PROOF / REQUIRES SUPPLIER' if typ=='Print' else ''),'/Producer':'pypdf controlled assembly from bundled LibreOffice tagged exports','/CreationDate':'D:20261007150000+03\'00\'','/ModDate':'D:20261007150000+03\'00\''})
 w.write(R/'02_pdf'/('GEM_Letterhead_'+typ+'.pdf'))
(R/'04_qa/evidence/PDF_Mapping_Repairs.json').write_text(json.dumps(log,indent=2,ensure_ascii=False))
print('PDFs rebuilt; missing mark mappings repaired from exporter ActualText')
