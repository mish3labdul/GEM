"""Rev03 render. Same LibreOffice binary (Codex runtime override soffice) and font configuration as Revision 02
render.py; invoked directly because this host's Python lacks render_docx.py's pdf2image dependency.
Usage: python render.py <revision_root> <tmp_render_dir>"""
from pathlib import Path
import subprocess,os,sys,json,tempfile,shutil
R=Path(sys.argv[1]).resolve();TMP=Path(sys.argv[2]).resolve();TMP.mkdir(parents=True,exist_ok=True)
SOFFICE='/Users/mediacenter1/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/soffice'
FONTS='/Users/mediacenter1/Documents/Codex/2026-10-07/github-plugin-github-openai-curated-remote-3/work/fonts.conf'
env=os.environ.copy();env['FONTCONFIG_FILE']=FONTS
files=sorted((R/'01_templates').glob('*.docx'))+sorted((R/'04_qa/fixtures').glob('*.docx'))+sorted((R/'03_specs').glob('*.docx'))
res=[]
with tempfile.TemporaryDirectory(prefix='lo_profile_') as prof:
 for p in files:
  out=TMP/p.stem;shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
  r=subprocess.run([SOFFICE,'-env:UserInstallation=file://'+prof,'--invisible','--headless','--norestore','--convert-to','pdf','--outdir',str(out),str(p)],env=env,capture_output=True,text=True,timeout=300)
  pdf=out/(p.stem+'.pdf');ok=pdf.exists() and pdf.stat().st_size>0
  if ok:subprocess.run(['pdftoppm','-r','100','-png',str(pdf),str(out/'page')],check=True)
  res.append({'file':str(p.relative_to(R)),'rendered':ok,'pages':len(list(out.glob('page-*.png')))});print(res[-1],flush=True)
(TMP/'Render_Results.json').write_text(json.dumps(res,indent=2))
assert all(r['rendered'] for r in res)
