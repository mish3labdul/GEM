"""AX01 task 13: build the four AX01 candidate decks by chaining the three anchored edit scripts (titles -> decorative -> table header rows).
Reads plans from local_only/raw (regenerate with ax01_titles_reading.py / ax01_classify_alt.py / ax01_classify_tables.py). Usage: ax01_build_candidates.py <repo_root> <package_dir>"""
import sys, os, json, subprocess, shutil, hashlib, zipfile
sys.path.insert(0, os.path.dirname(__file__)); from ax01_common import *
root, pkg = sys.argv[1:3]; here = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
plans = {k: json.load(open(f"{pkg}/local_only/raw/{k}_plan.json")) for k in ('title', 'decorative', 'table')}
sc = f"{pkg}/local_only/scratch/build"; os.makedirs(sc, exist_ok=True); out = f"{pkg}/21_candidate_corrections"; os.makedirs(out, exist_ok=True); report = {}
for key, (label, path, lineage) in DECKS.items():
    cur = f"{root}/{path}"; steps = []
    for kind, script in (('title', 'ax01_apply_titles.py'), ('decorative', 'ax01_apply_decorative.py'), ('table', 'ax01_apply_tables.py')):
        pl = plans[kind].get(label, [])
        if not pl: continue
        pj = f"{sc}/{key}_{kind}_plan.json"; json.dump(pl, open(pj, 'w')); nxt = f"{sc}/{key}_{kind}.pptx"; lg = f"{sc}/{key}_{kind}_log.json"
        r = subprocess.run([PY, f"{here}/{script}", cur, nxt, pj, lg], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        steps.append((kind, json.load(open(lg)), r.stdout.strip())); cur = nxt
    dst = f"{out}/" + os.path.basename(path).replace('AR01 CANDIDATE', 'AX01 CANDIDATE').replace('D3 CANDIDATE', 'AX01 CANDIDATE').replace('ODI01-R1 CANDIDATE', 'AX01 CANDIDATE'); shutil.copyfile(cur, dst)
    zs, zd = zipfile.ZipFile(f"{root}/{path}"), zipfile.ZipFile(dst); changed = sorted(n for n in zs.namelist() if zs.read(n) != zd.read(n))
    assert [i.filename for i in zs.infolist()] == [i.filename for i in zd.infolist()]
    report[label] = dict(source=path, source_sha256=shaf(f"{root}/{path}"), output=os.path.basename(dst), output_sha256=shaf(dst), members_changed=changed, steps={k: dict(n=(v.get('shapes_marked') or v.get('tables_flagged') or len(v.get('edits', []))), log=v) for k, v, _ in steps})
    print(label, os.path.basename(dst), shaf(dst)[:12], 'members changed:', len(changed), {k: (v.get('shapes_marked') or v.get('tables_flagged') or len(v.get('edits', []))) for k, v, _ in steps})
json.dump(report, open(f"{pkg}/local_only/raw/ax01_edit_log_raw.json", 'w'), indent=1)   # unscrubbed (shape names may hold deck text): local-only
def scrub(o):
    if isinstance(o, dict): return {k: (gl(v, o.get('shape_id')) if k == 'shape' and isinstance(v, str) else scrub(v)) for k, v in o.items()}
    if isinstance(o, list): return [scrub(x) for x in o]
    return o
json.dump(scrub(report), open(f"{pkg}/20_qa/ax01_edit_log.json", 'w'), indent=1)
