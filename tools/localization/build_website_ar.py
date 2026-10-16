#!/usr/bin/env python3
"""Build proposed Arabic pages from current English templates and reviewed string register.
Requires beautifulsoup4. Adds idempotent English language links; does not generate artwork.
"""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup,Comment,Doctype
ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'website/site'
def validate_runtime_messages(messages):
 script=(SITE/'assets/js/site.js').read_text()
 contract=re.search(r'var REQUIRED_AR_MESSAGE_KEYS = (\[[\s\S]*?\]);',script)
 if not contract:raise ValueError('Missing runtime message contract')
 keys=json.loads(contract[1])
 if not isinstance(keys,list) or not keys or any(not isinstance(k,str) or not k for k in keys) or len(set(keys))!=len(keys):
  raise ValueError('Invalid runtime message contract')
 # This maintained runtime supports only literal JSON-string arguments to t().
 # Reject other call forms rather than silently missing new localization requirements.
 calls=[]
 for call in re.finditer(r'\bt\s*\(',script):
  literal=re.match(r'\s*("(?:[^"\\]|\\.)*")\s*\)',script[call.end():])
  if not literal:raise ValueError('Unsupported dynamic runtime message call')
  calls.append(json.loads(literal[1]))
 if set(calls)!=set(keys):raise ValueError('Drift in runtime message contract')
 if not isinstance(messages,dict):raise ValueError('Invalid runtime message catalog')
 for key in keys:
  value=messages.get(key)
  if not isinstance(value,str) or not value.strip():raise ValueError('Missing or invalid runtime message: '+key)
def build():
 data=json.loads((ROOT/'tools/localization/website-ar.json').read_text());tr=data['translations'];retained=data['retained']
 validate_runtime_messages(data.get('messages'))
 outputs={}
 for name in ('index','reference','privacy'):
  source=SITE/f'{name}.html'
  english=english_language_links(source.read_text(),name)
  soup=BeautifulSoup(english,'html.parser')
  for old in soup.select('.language-switch, link[rel=alternate]'):old.decompose()
  for old in soup.select('.footer-grid > div:last-child ul [hreflang]'):old.parent.decompose()
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
    elif value and value not in retained:
     technical=(tag.name=='meta' and tag.get('name') in ('viewport','robots')) or (attr=='value' and tag.name=='input' and tag.get('type')=='checkbox')
     if not technical:raise ValueError(f'Unregistered attribute on {name}: {attr}={value}')
   for attr in ('src','href'):
    value=tag.get(attr,'')
    if value.startswith(('assets/','favicon','apple-touch-icon')):tag[attr]='../'+value
   if tag.has_attr('srcset'):tag['srcset']=tag['srcset'].replace('assets/','../assets/')
  # Arabic font: same interim licensed face as the controlled document work.
  if not soup.find('link',href='../assets/css/arabic.css'):
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
  outputs[SITE/'ar'/f'{name}.html']=str(soup)+'\n'
  outputs[source]=english
 outputs[SITE/'assets/js/messages-ar.js']='/* Proposed Arabic messages; source: tools/localization/website-ar.json */\nwindow.GEM_AR_MESSAGES = '+json.dumps(data['messages'],ensure_ascii=False,indent=2)+';\n'
 # Validate every page before writing any output: untranslated copy cannot leave a partial toggle.
 for path,content in outputs.items():
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
def english_language_links(text,name):
 if 'class="language-switch"' in text:return text
 target='ar/'+name+'.html'
 nav=f'<a class="language-switch" href="{target}" lang="ar" dir="rtl" hreflang="ar">العربية</a>\n      '
 anchor='<button class="nav-toggle"'
 if text.count(anchor)!=1:raise ValueError('Expected one navigation toggle on '+name)
 text=text.replace(anchor,nav+anchor,1)
 original='<li>English. An Arabic edition is in preparation.</li>'
 if text.count(original)!=1:raise ValueError('Expected language footer on '+name)
 text=text.replace(original,f'<li><a href="{target}" lang="ar" dir="rtl" hreflang="ar">العربية</a></li>',1)
 head=f'  <link rel="stylesheet" href="assets/css/arabic.css">\n  <link rel="alternate" hreflang="en" href="{name}.html">\n  <link rel="alternate" hreflang="ar" href="{target}">\n'
 return text.replace('</head>',head+'</head>',1)
def add_language_links(soup,name,lang):
 for old in soup.select('.language-switch, link[rel=alternate]'):old.decompose()
 if lang=='en' and not soup.find('link',href='assets/css/arabic.css'):
  soup.head.append(soup.new_tag('link',rel='stylesheet',href='assets/css/arabic.css'))
 target='../'+name+'.html' if lang=='ar' else 'ar/'+name+'.html'
 label='English' if lang=='ar' else 'العربية'
 a=soup.new_tag('a',href=target,lang='en' if lang=='ar' else 'ar',dir='ltr' if lang=='ar' else 'rtl',hreflang='en' if lang=='ar' else 'ar');a['class']='language-switch';a.string=label
 soup.select_one('.nav-toggle').insert_before(a)
 footer=soup.select('.footer-grid > div')[-1].find('ul');footer.clear();li=soup.new_tag('li');link=soup.new_tag('a',href=target,lang='en' if lang=='ar' else 'ar',hreflang='en' if lang=='ar' else 'ar',dir='ltr' if lang=='ar' else 'rtl');link.string=label;li.append(link);footer.append(li)
 if lang=='ar':
  li=soup.new_tag('li');li.string='العربية — مسودة بانتظار اعتماد الصياغة';footer.append(li)
 for code,url in [('en','../'+name+'.html' if lang=='ar' else name+'.html'),('ar',name+'.html' if lang=='ar' else 'ar/'+name+'.html')]:soup.head.append(soup.new_tag('link',rel='alternate',hreflang=code,href=url))
if __name__=='__main__':build()
