"""NP01-R1 manifest/checksum generator. Usage: np01r1_manifest.py <package_dir> <manifest_template_json>
Excludes: .DS_Store, local-only screenshot folders (12_screenshots/, local_only_screenshots/), local-only raw sweep files, MANIFEST.json, SHA256SUMS.txt.
SHA256SUMS.txt covers every other file plus MANIFEST.json; neither hashes itself."""
import sys, os, json, hashlib
pkg, tpl = sys.argv[1:3]
sh = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
EXC_DIRS = ('12_screenshots', 'local_only_screenshots'); EXC_FILES = ('.DS_Store', 'MANIFEST.json', 'SHA256SUMS.txt')
import fnmatch
EXC_PATTERNS = ('14_raw_native_sweeps/Part_*', 'qa_evidence/06_native_sweep_slide30_BEFORE.tsv', 'qa_evidence/07_native_sweep_slide30_AFTER.tsv')  # local-only raw sweep files (D7 pending)
files = sorted(os.path.relpath(os.path.join(d, f), pkg) for d, _, fs in os.walk(pkg) for f in fs
               if f not in EXC_FILES and not any(os.path.relpath(os.path.join(d, f), pkg).startswith(x + os.sep) for x in EXC_DIRS)
               and not any(fnmatch.fnmatch(os.path.relpath(os.path.join(d, f), pkg), x) for x in EXC_PATTERNS))
m = json.load(open(tpl, encoding='utf8'))
m["files"] = [{"path": f, "sha256": sh(os.path.join(pkg, f)), "bytes": os.path.getsize(os.path.join(pkg, f))} for f in files]
m["excluded_from_manifest_and_version_control"] = ["12_screenshots/ (NP01, local-only)", "local_only_screenshots/ (NP01-R1, local-only)", "14_raw_native_sweeps/Part_* (NP01 raw sweeps, local-only)", "qa_evidence/06_native_sweep_slide30_BEFORE.tsv and 07_native_sweep_slide30_AFTER.tsv (NP01-R1 raw sweeps, local-only)", ".DS_Store"]
json.dump(m, open(os.path.join(pkg, "MANIFEST.json"), 'w', encoding='utf8'), indent=1, ensure_ascii=False); open(os.path.join(pkg, "MANIFEST.json"), 'a').write("\n")
allf = sorted(files + ["MANIFEST.json"])
open(os.path.join(pkg, "SHA256SUMS.txt"), 'w', encoding='utf8').write("".join(f"{sh(os.path.join(pkg, f))}  {f}\n" for f in allf))
print(pkg, len(files), "files + MANIFEST")
