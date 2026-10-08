from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,TextStringObject
R=Path(__file__).resolve().parent.parent
titles=['English first page','English continuation','Arabic first page','Arabic continuation','Bilingual first page','Bilingual continuation','Executive','Minimal']
for typ in ['Digital','Print']:
 r=PdfReader(R/'04_qa/renders/GEM_Letterhead_Portfolio/GEM_Letterhead_Portfolio.pdf');w=PdfWriter();w.clone_document_from_reader(r)
 w.root_object[NameObject('/Lang')]=TextStringObject('en-GB')
 w.add_metadata({'/Title':'GEM™ Branded Letterhead Set v1.0 '+typ,'/Subject':'WORKING APPLICATION / PENDING VALIDATION'+(' · PENDING PREPRESS STANDARD / PENDING PHYSICAL PROOF' if typ=='Print' else ''),'/Author':'GEM'})
 for i,t in enumerate(titles):w.add_outline_item(t,i)
 for p in w.pages:p.compress_content_streams()
 w.write(R/'02_pdf'/('GEM_Letterhead_'+typ+'.pdf'))
for p in (R/'01_templates').glob('GEM*.docx'):
 r=PdfReader(R/'04_qa/renders'/p.stem/(p.stem+'.pdf'));w=PdfWriter();w.clone_document_from_reader(r);w.root_object[NameObject('/Lang')]=TextStringObject('ar-SA' if 'Arabic' in p.name or 'Bilingual' in p.name else 'en-GB');w.write(R/'02_pdf'/(p.stem+'.pdf'))
