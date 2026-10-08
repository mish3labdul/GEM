from pathlib import Path
import urllib.request,json,hashlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
root=Path(__file__).resolve().parent.parent;
for d in ['00_source/fonts','01_templates','02_pdf','03_specs','04_qa','05_release']: (root/d).mkdir(parents=True,exist_ok=True)
for family,file in [('jost','Jost[wght].ttf'),('inter','Inter[opsz,wght].ttf'),('notosansarabic','NotoSansArabic[wdth,wght].ttf')]:
 p=root/'00_source/fonts'/family;p.mkdir(exist_ok=True)
 for n in [file,'OFL.txt','METADATA.pb']:
  url='https://raw.githubusercontent.com/google/fonts/2c605eeda2de57af2b34822b79986f5140299862/ofl/'+family+'/'+urllib.parse.quote(n)
  urllib.request.urlretrieve(url,p/n)
 for weight,style in [(400,'Regular'),(700,'Bold')]:
  f=TTFont(p/file);axes={a.axisTag:a.defaultValue for a in f['fvar'].axes};axes['wght']=weight
  if 'opsz' in axes:axes['opsz']=14
  f=instantiateVariableFont(f,axes,inplace=True)
  name={'jost':'Jost','inter':'Inter','notosansarabic':'Noto Sans Arabic'}[family]
  for platform,enc,lang in [(3,1,1033),(1,0,0)]:
   for nid,val in [(1,name),(2,style),(4,name+' '+style),(6,name.replace(' ','')+'-'+style),(16,name),(17,style)]:f['name'].setName(val,nid,platform,enc,lang)
  f.save(p/(name.replace(' ','')+'-'+style+'.ttf'))
print(root)
