"""AX01 manifest/checksum generator. Usage: ar01_manifest.py <package_dir> <template_json>. Excludes local_only/, .DS_Store, MANIFEST.json, SHA256SUMS.txt; SHA256SUMS.txt also covers MANIFEST.json."""
import sys, os, json, hashlib
pkg, tpl = sys.argv[1:3]
sh = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
files = sorted(os.path.relpath(os.path.join(d, f), pkg) for d, _, fs in os.walk(pkg) for f in fs
               if f not in ('.DS_Store', 'MANIFEST.json', 'SHA256SUMS.txt') and not os.path.relpath(os.path.join(d, f), pkg).startswith('local_only' + os.sep))
m = json.load(open(tpl, encoding='utf8')); m["files"] = [{"path": f, "sha256": sh(os.path.join(pkg, f)), "bytes": os.path.getsize(os.path.join(pkg, f))} for f in files]
m["excluded_from_manifest_and_version_control"] = ["local_only/ (raw text-bearing inventory, scratch variants and probes, PDFs, screenshots)", ".DS_Store"]
json.dump(m, open(os.path.join(pkg, "MANIFEST.json"), 'w', encoding='utf8'), indent=1, ensure_ascii=False); open(os.path.join(pkg, "MANIFEST.json"), 'a').write("\n")
open(os.path.join(pkg, "SHA256SUMS.txt"), 'w', encoding='utf8').write("".join(f"{sh(os.path.join(pkg, f))}  {f}\n" for f in sorted(files + ["MANIFEST.json"])))
print(pkg, len(files), "files + MANIFEST")
