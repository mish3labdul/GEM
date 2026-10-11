from pathlib import Path
import subprocess,os,concurrent.futures,json
R=Path('work/GEM/GEM_Letterhead_Set_v1.1');SK=Path('/Users/mediacenter1/.codex/plugins/cache/openai-primary-runtime/documents/26.905.11957/skills/documents')
env=os.environ.copy();env['FONTCONFIG_FILE']=str(Path('work/fonts.conf').resolve())
def go(p):
 out=Path('work/letterhead_revision_02/render')/p.stem
 r=subprocess.run([os.sys.executable,str(SK/'render_docx.py'),str(p),'--output_dir',str(out),'--emit_pdf','--width','1200','--height','1700'],env=env,capture_output=True,text=True)
 result={'file':str(p.relative_to(R)),'rendered':r.returncode==0,'pages':len(list(out.glob('page-*.png'))),'log':(r.stdout+r.stderr)[-700:]};print(result,flush=True);return result
files=list((R/'01_templates').glob('*.docx'))+list((R/'04_qa/fixtures').glob('*.docx'))+list((R/'03_specs').glob('*.docx'))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(go,files))
(R/'04_qa/evidence/Render_Results.json').write_text(json.dumps(res,indent=2))
assert all(r['rendered'] for r in res)
