#!/usr/bin/env python3
"""RP01 Task 1 + Task 6: baseline hash verification and status-label inventory.
Run from the repository root: python3 -I GEM_V3.0_RP01_Release_Artifact_Promotion/15_scripts/rp01_inventory.py
Reads the FA01 MANIFEST (baseline_files_outside_package) as the authorized hash source. Read-only; writes only the
two CSVs named below into the RP01 package. Label inventory is a candidate list: classification is a human decision."""
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

RP = Path("GEM_V3.0_RP01_Release_Artifact_Promotion")
FA = Path("GEM_V3.0_FA01_Final_Release_Authorization")
sha = lambda b: hashlib.sha256(b).hexdigest()
man = json.load(open(FA / "MANIFEST.json", encoding="utf-8"))
base = man["baseline_files_outside_package"]

# FA01 scope matrix: independent second source of the same hashes (full sha256 appear in column 2 as "sha256 <hash>")
scope_txt = (FA / "10_FA01_Release_Scope_Matrix.csv").read_text(encoding="utf-8")

rows = []
for i, e in enumerate(base, 1):
    p = Path(e["path"])
    cur = sha(p.read_bytes()) if p.exists() else "MISSING"
    in_matrix = e["sha256"] in scope_txt
    rows.append([i, p.name, e["path"], e["sha256"], cur, "YES" if cur == e["sha256"] else "NO", "in FA01 10: %s" % ("yes" if in_matrix else "no")])
with open(RP / "02_RP01_Authorized_Baseline_hashcheck.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["#", "File", "Source path", "FA01 SHA256", "Current SHA256", "Hash match?", "Cross-check"])
    w.writerows(rows)
print("baseline files:", len(rows), "matches:", sum(r[5] == "YES" for r in rows))

PAT = re.compile(r"RC2|RELEASE CANDIDATE|WORKING EDITION|WORKING APPLICATION|PENDING VALIDATION|NOT RELEASED|UNAPPROVED|AC20|HR01|CANDIDATE|PENDING LOCALIZATION|CONCEPT|NOT PRODUCTION|WORKING ASSET|D8|DRAFT|PENDING", re.I)
out = []
for e in base:
    p = Path(e["path"])
    if p.suffix not in (".pptx", ".docx"):
        continue
    with zipfile.ZipFile(p) as z:
        for n in sorted(z.namelist()):
            if not n.endswith(".xml") and not n.endswith(".rels"):
                continue
            if not re.match(r"(ppt/(slides|slideLayouts|slideMasters|notesSlides|notesMasters|handoutMasters)/|docProps/|word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml|ppt/presentation\.xml|ppt/commentAuthors|ppt/comments)", n):
                continue
            x = z.read(n).decode("utf-8", "replace")
            # paragraph-level text (join a:t / w:t runs per paragraph)
            paras = re.findall(r"<(?:a:p|w:p)[ >].*?</(?:a:p|w:p)>", x, re.S) or [x]
            for pi, para in enumerate(paras):
                t = "".join(re.findall(r"<(?:a:t|w:t)[^>]*>([^<]*)</(?:a:t|w:t)>", para))
                if not t and n.startswith("docProps"):
                    t = re.sub(r"<[^>]+>", " ", para)
                if t and PAT.search(t):
                    out.append([p.name, n, pi, t.strip()[:200]])
            if n.startswith("docProps"):
                for m in re.finditer(r"<(dc:title|dc:subject|cp:keywords|dc:description|cp:category|cp:contentStatus|cp:version)[^>]*>([^<]*)<", x):
                    out.append([p.name, n, "prop", "%s=%s" % (m.group(1), m.group(2))[:200]])
with open(RP / "04a_RP01_Label_Candidates_raw.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["File", "Zip member", "Para#", "Text"])
    w.writerows(out)
print("label candidate rows:", len(out))
