"""NP01-R1 task 1: before-state and authority check for Part B slide 30 (read-only).
Compares slide 30 across: RC2 release deck, RC2 source deck, ODI01-R1 candidate. Output: JSON to argv[2]; markdown tables to stdout.
Usage: np01r1_authority_check.py <repo_root> <out_json>"""
import sys, re, json, zipfile, hashlib
root, outp = sys.argv[1:3]
D = {
 "RC2 release deck (authoritative)": "PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pptx",
 "RC2 source deck (authoritative)": "PartB_RC2/01_source/B-RC2.pptx",
 "ODI01-R1 candidate (current)": "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Digital Design System V3.0 — Part B — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx",
}
sha = lambda b: hashlib.sha256(b).hexdigest()
def shapes(x):
    out = {}
    for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S):
        b = m.group(0); n = re.search(r'name="([^"]*)"', b).group(1)
        o = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', b); e = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', b)
        bp = re.search(r'<a:bodyPr([^>]*)>', b)
        out[n] = dict(off=tuple(map(int, o.groups())) if o else None, ext=tuple(map(int, e.groups())) if e else None,
                      bodyPr=bp.group(1).strip() if bp else None, text=''.join(re.findall(r'<a:t>([^<]*)</a:t>', b)), 
                      bold=re.findall(r'\bb="([^"]+)"', b), sizes=sorted(set(re.findall(r'sz="(\d+)"', b))),
                      typefaces=sorted(set(re.findall(r'<a:latin typeface="([^"]+)"', b))), lnSpc=re.findall(r'<a:spcPts val="(\d+)"', b),
                      fills=re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', b), sha256=sha(b.encode()))
    return out
res = {}
for k, p in D.items():
    z = zipfile.ZipFile(f"{root}/{p}"); x = z.read('ppt/slides/slide30.xml').decode('utf8')
    res[k] = dict(path=p, deck_sha256=sha(open(f"{root}/{p}", 'rb').read()), slide30_sha256=sha(x.encode()), slides=len([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]), shapes=shapes(x))
keys = list(D); base = res[keys[1]]["shapes"]; cand = res[keys[2]]["shapes"]; rel = res[keys[0]]["shapes"]
diff = {}
for n in sorted(set(base) | set(cand)):
    a, b = base.get(n), cand.get(n)
    if a != b: diff[n] = {f: (a or {}).get(f) for f in ()} | {f: [ (a or {}).get(f), (b or {}).get(f)] for f in ("off","ext","bodyPr","text","bold","sizes","typefaces","lnSpc","fills") if (a or {}).get(f) != (b or {}).get(f)}
# deck text is compared internally but NOT written out (only SHA-256 and length), to keep governed excerpts out of committed evidence
res["_summary"] = dict(
  release_equals_source_slide30=res[keys[0]]["slide30_sha256"] == res[keys[1]]["slide30_sha256"],
  release_equals_source_shapes=rel == base,
  source_vs_candidate_shape_differences=diff,
  text_identical_all_shapes=all(base[n]["text"] == cand[n]["text"] for n in base),
  geometry_identical_all_shapes=all(base[n]["off"] == cand[n]["off"] and base[n]["ext"] == cand[n]["ext"] and base[n]["bodyPr"] == cand[n]["bodyPr"] for n in base))

# Deck text is compared above but NOT written out: only SHA-256 and length are kept, so no governed excerpt enters committed evidence.
for k in keys:
    for n_, sh_ in res[k]["shapes"].items():
        t_ = sh_.pop("text"); sh_["text_sha256"] = sha(t_.encode()); sh_["text_len"] = len(t_)
for n_, d_ in res["_summary"]["source_vs_candidate_shape_differences"].items():
    if "text" in d_: d_["text"] = ["(differs: hashes recorded per shape)"]
json.dump(res, open(outp, "w"), indent=1, ensure_ascii=False)
print(json.dumps(res["_summary"], indent=1, ensure_ascii=False))
