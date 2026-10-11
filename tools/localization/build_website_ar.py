#!/usr/bin/env python3
"""Build proposed Arabic pages from preserved v0.5.3 templates and reviewed string register.
Requires beautifulsoup4. Does not edit English source or generate artwork.
"""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup,Comment,Doctype
ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'website/site'
def build():
 data=json.loads((ROOT/'tools/localization/website-ar.json').read_text());tr=data['translations'];retained=data['retained']
 (SITE/'ar').mkdir(exist_ok=True)
 for name in ('index','reference','privacy'):
  source=ROOT/f'archive/website-v0.5.3-before-localization/site/{name}.html'
  soup=BeautifulSoup(source.read_text(),'html.parser')
  soup.html['lang']='ar';soup.html['dir']='rtl'
  for node in list(soup.find_all(string=True)):
   if isinstance(node,(Comment,Doctype)) or node.parent.name in ('script','style'):continue
   text=str(node);key=text.strip()
   if not key:continue
   if key in tr:node.replace_with(text.replace(key,tr[key]))
   elif key not in retained:raise ValueError('Unregistered string: '+key)
   elif re.search('[A-Za-z]',key):
    span=soup.new_tag('bdi',dir='ltr',lang='en');span['class']='latin-copy';span.string=key;node.replace_with(span)
  for tag in soup.find_all():
   for attr in ('alt','aria-label','placeholder','title','content','value'):
    value=tag.get(attr)
    if value in tr:tag[attr]=tr[value]
   for attr in ('src','href'):
    value=tag.get(attr,'')
    if value.startswith(('assets/','favicon','apple-touch-icon')):tag[attr]='../'+value
   if tag.has_attr('srcset'):tag['srcset']=tag['srcset'].replace('assets/','../assets/')
  # Arabic font: same interim licensed face as the controlled document work.
  css=soup.new_tag('link',rel='stylesheet',href='../assets/css/arabic.css');soup.head.append(css)
  preload=soup.new_tag('link',rel='preload',href='../assets/fonts/noto-sans-arabic-400.woff2',attrs={'as':'font','type':'font/woff2','crossorigin':''});soup.head.append(preload)
  messages=soup.new_tag('script',src='../assets/js/messages-ar.js',defer='');soup.find('script',src='../assets/js/site.js').insert_before(messages)
  add_language_links(soup,name,'ar')
  for sel in ('#f-email','#q-rooms'):
   field=soup.select_one(sel)
   if field:field['dir']='ltr';field['lang']='en'
  for sel in ('#f-name','#f-org','#f-message'):
   field=soup.select_one(sel)
   if field:field['dir']='auto'
  # Wrap Latin tokens in mixed Arabic prose; do not reverse or mirror logo/image assets.
  for node in list(soup.find_all(string=True)):
   if isinstance(node,(Comment,Doctype)) or node.parent.name in ('script','style','bdi','title') or not re.search('[\u0600-\u06ff]',str(node)):continue
   text=str(node)
   for part in re.split(r'([A-Za-z][A-Za-z0-9™@._/="–\-]*(?: [A-Za-z0-9][A-Za-z0-9™@._/="–\-]*)*|#[A-Fa-f0-9]{6}|[0-9]+(?:[.:×–][0-9]+)*(?: ?(?:px|em|u))?)',text):
    if not part:continue
    if re.match(r'[A-Za-z0-9#]',part):
     bdi=soup.new_tag('bdi',dir='ltr',lang='en');bdi['class']='latin-copy';bdi.string=part;node.insert_before(bdi)
    else:node.insert_before(part)
   node.extract()
  (SITE/'ar'/f'{name}.html').write_text(str(soup)+'\n')
 (SITE/'assets/js/messages-ar.js').write_text('/* Proposed Arabic messages; source: tools/localization/website-ar.json */\nwindow.GEM_AR_MESSAGES = '+json.dumps(data['messages'],ensure_ascii=False,indent=2)+';\n')
def add_language_links(soup,name,lang):
 target='../'+name+'.html' if lang=='ar' else 'ar/'+name+'.html'
 label='English' if lang=='ar' else 'العربية'
 a=soup.new_tag('a',href=target,lang='en' if lang=='ar' else 'ar',dir='ltr' if lang=='ar' else 'rtl',hreflang='en' if lang=='ar' else 'ar');a['class']='language-switch';a.string=label
 soup.select_one('.nav-toggle').insert_before(a)
 footer=soup.select('.footer-grid > div')[-1].find('ul');footer.clear();li=soup.new_tag('li');link=soup.new_tag('a',href=target,lang='en' if lang=='ar' else 'ar',hreflang='en' if lang=='ar' else 'ar',dir='ltr' if lang=='ar' else 'rtl');link.string=label;li.append(link);footer.append(li)
 if lang=='ar':
  li=soup.new_tag('li');li.string='العربية — مسودة بانتظار اعتماد الصياغة';footer.append(li)
 for code,url in [('en','../'+name+'.html' if lang=='ar' else name+'.html'),('ar',name+'.html' if lang=='ar' else 'ar/'+name+'.html')]:soup.head.append(soup.new_tag('link',rel='alternate',hreflang=code,href=url))
if __name__=='__main__':build()
