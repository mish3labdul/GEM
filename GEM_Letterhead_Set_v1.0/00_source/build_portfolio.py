from build_letterheads import *
from copy import deepcopy
from docx.enum.section import WD_SECTION_START
D=Document(); first=True
items=[('en',False,''),('en',True,''),('ar',False,''),('ar',True,''),('bi',False,''),('bi',True,''),('en',False,'Executive'),('en',False,'Minimal')]
for lang,cont,variant in items:
 tmp=create('Portfolio',lang,cont,variant,return_document=True)
 if first:
  sec=D.sections[0];first=False
 else:sec=D.add_section(WD_SECTION_START.NEW_PAGE)
 ts=tmp.sections[0]
 for prop in ['page_width','page_height','top_margin','bottom_margin','left_margin','right_margin','header_distance','footer_distance']:setattr(sec,prop,getattr(ts,prop))
 for h in [sec.header,sec.first_page_header,sec.footer,sec.first_page_footer]:
  h.is_linked_to_previous=False
  for c in list(h._element):h._element.remove(c)
  h._element.append(OxmlElement('w:p'))
 header(sec,lang!='en',cont,variant=='Executive',variant=='Minimal');footer(sec,lang!='en',variant=='Minimal')
 for p in tmp.paragraphs:
  sec._sectPr.addprevious(deepcopy(p._p))
# headings/fonts styled identically to templates
for name in ['Normal','Heading 1','Heading 2']:
 D.styles[name].font.name='Inter' if name=='Normal' else 'Jost';D.styles[name].font.color.rgb=RGBColor.from_string(INK);D.styles[name].font.size=Pt(10.5 if name=='Normal' else 12)
configure_edit_styles(D,False)
D.core_properties.title='GEM Branded Letterhead Set v1.0';D.core_properties.subject='Working RC2 application proof portfolio';D.core_properties.language='en-GB'
p=R/'00_source/GEM_Letterhead_Portfolio.docx';D.save(p);embed_fonts(p)
