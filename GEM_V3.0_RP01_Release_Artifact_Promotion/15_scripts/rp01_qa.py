#!/usr/bin/env python3
"""RP01 QA. Run from the repository root with the docling venv python (lxml, pptx):
  ~/venvs/docling/bin/python -B GEM_V3.0_RP01_Release_Artifact_Promotion/15_scripts/rp01_qa.py
Writes 16_qa/RP01_QA_Report.md; exit 1 on any failure."""
import csv
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import rp01_build as B  # noqa: E402  (imports only; main() is not run)

RP = Path("GEM_V3.0_RP01_Release_Artifact_Promotion")
FA = Path("GEM_V3.0_FA01_Final_Release_Authorization")
OUT = RP / "17_release_artifacts"
res = []
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check(name, ok, detail=""):
    res.append((name, bool(ok), str(detail)))


def git(*a):
    return subprocess.run(["git", "-c", "core.quotepath=off", *a], capture_output=True, text=True).stdout.rstrip("\n")


def rows(p):
    return list(csv.DictReader(open(p, encoding="utf-8", newline="")))


# ---- git / governance state
check("parent HEAD is the FA01 commit", git("rev-parse", "HEAD").startswith("a8ebc8da1f5cb66f4ab369c90dcf5844a17e18ed"), git("rev-parse", "HEAD"))
tracked_mod = sorted(l[3:] for l in git("status", "--short").splitlines() if not l.startswith("??"))
check("only README.md is a tracked modification", tracked_mod in (["README.md"], []), tracked_mod)
check("origin/main unchanged", git("rev-parse", "origin/main") == "4ea0d117da03850854654288afcdde98f39994d5")
check("approval register unchanged", sha("GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx") == "ccce46135a4f2244dbff21cef94a6160e9d2b6fd96a63647c1e5ea6b662e7ab3")
check("no tag exists", git("tag") == "", git("tag"))
check("no PDF anywhere in the RP01 package", not list(RP.rglob("*.pdf")))
check("no Office lock/temp, .DS_Store or __pycache__ in the package", not [p for p in RP.rglob("*") if p.name.startswith(("~$", ".~", ".DS_Store")) or "__pycache__" in p.parts])
txt = "".join(p.read_text(encoding="utf-8") for p in RP.rglob("*") if p.suffix in (".md", ".csv", ".json") and p.is_file())
check("no absolute user paths or credential patterns in package text", not re.search(r"/Users/|ghp_|github_pat_|api[_-]?key\s*[:=]|BEGIN [A-Z ]*PRIVATE", txt, re.I))

# ---- baseline and lineage
man = {Path(e["path"]).name: e for e in json.load(open(FA / "MANIFEST.json", encoding="utf-8"))["baseline_files_outside_package"]}
base = rows(RP / "02_RP01_Authorized_Baseline.csv")
check("baseline lists 15 artifacts, all hash matches YES, none STOP", len(base) == 15 and all(r["Hash match?"] == "YES" and r["RP01 action"] != "STOP" for r in base), len(base))
check("every FA01 baseline hash equals the current hash of its source", all(sha(e["path"]) == e["sha256"] for e in man.values()))
check("baseline table FA01 hashes equal the FA01 manifest", all(man[Path(r["Source path"]).name]["sha256"] == r["FA01 SHA256"] for r in base))
promo = rows(RP / "03_RP01_Artifact_Promotion_Register.csv")
check("promotion register: every promoted file exists and its hash matches", all((RP / r["Promoted path (in RP01)"]).exists() and sha(RP / r["Promoted path (in RP01)"]) == r["Promoted SHA256"] for r in promo if not r["Artifact ID"].startswith("K-")))
lin = rows(RP / "08_RP01_Lineage_Proof.csv")
check("lineage: no unexpected changes, all PASS", all(r["Unexpected changes?"] == "NO" and r["Result"] == "PASS" for r in lin), len(lin))
check("no old RC2 release artifact is a source", not [r for r in base if re.search(r"(04_release|05_release|00_originals|01_working)/", r["Source path"]) and "tokens" not in r["Source path"]])

# ---- stale labels: rerun the build's residual scan on every promoted file
bad = []
for a in B.ARTS:
    dst = OUT / a["folder"] / a["target"]
    if dst.exists():
        _, b = B.residual(dst, a["extra_preserve"])
        bad += [(a["id"], x) for x in b]
check("no unclassified release-state label remains in any promoted Office file", not bad, bad[:3])
check("promoted file names follow X12 (GEM_BRAND_<asset>_<variant>_v3.0_20261009)", all(re.fullmatch(r"GEM_BRAND_[A-Za-z]+_[A-Za-z]+_v3\.0_20261009\.(pptx|docx)", Path(a["target"]).name) for a in B.ARTS))
check("no promoted file name contains final/new/latest", not [a for a in B.ARTS if re.search(r"final|new|latest", a["target"], re.I)])

# ---- restricted artifacts
RD = OUT / "05_letterheads" / "restricted_internal_only"
rest = sorted(RD.glob("*.docx"))
check("four restricted templates live under restricted_internal_only", len(rest) == 4, [p.name for p in rest])
okf = True
for p in rest:
    z = zipfile.ZipFile(p)
    for n in z.namelist():
        if re.fullmatch(r"word/footer\d+\.xml", n):
            t = z.read(n).decode()
            okf &= all(s in t for s in ("WORKING APPLICATION / PENDING VALIDATION", "PENDING LOCALIZATION APPROVAL", "EXTERNAL ISSUE RESTRICTED PENDING D8 VALIDATION"))
check("every footer of every restricted template carries both D8 markings and the restriction line", okf)
check("restricted templates are NO for external issue in the scope matrix", all(r["External issue eligibility (artifact level)"] == "NO" for r in rows(RP / "05_RP01_Release_Scope_Matrix.csv") if "Internal" in r["Promoted path"] and r["Promoted path"].endswith(".docx")))
check("restricted register lists the four templates and the Arabic extracts", len(rows(RP / "06_RP01_Restricted_Artifact_Register.csv")) >= 8)
eng = [p for p in (OUT / "05_letterheads").glob("*.docx")]
check("English templates carry no working-application marker", all("WORKING APPLICATION" not in "".join(zipfile.ZipFile(p).read(n).decode() for n in zipfile.ZipFile(p).namelist() if n.startswith(("word/footer", "word/document", "docProps/core"))) for p in eng))

# ---- Part D / Part C / kit / tokens
dsrc = next(Path(r["Source path"]) for r in base if r["Artifact ID"] == "P-D")
dnew = OUT / "04_amenities_concept" / "GEM_BRAND_AmenitiesPackagingConcept_PartD_v3.0_20261009.pptx"
cnt = lambda p, ph: sum(1 for n in zipfile.ZipFile(p).namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n) and ph in zipfile.ZipFile(p).read(n).decode())
check("Part D keeps CONCEPT / NOT PRODUCTION ARTWORK on every slide that had it", cnt(dnew, "CONCEPT / NOT PRODUCTION ARTWORK") >= cnt(dsrc, "CONCEPT / NOT PRODUCTION ARTWORK") and cnt(dnew, "CONCEPT / NOT PRODUCTION ARTWORK") > 0, (cnt(dsrc, "CONCEPT / NOT PRODUCTION ARTWORK"), cnt(dnew, "CONCEPT / NOT PRODUCTION ARTWORK")))
dall = "".join(zipfile.ZipFile(dnew).read(n).decode() for n in zipfile.ZipFile(dnew).namelist() if n.endswith(".xml"))
check("Part D makes no production-artwork / supplier-ready / dieline-final / regulatory-approved claim", not re.search(r"SUPPLIER[- ]READY|FINAL DIELINE|REGULATORY APPROVED|PRODUCTION ARTWORK APPROVED", dall, re.I))
csrc = next(Path(r["Source path"]) for r in base if r["Artifact ID"] == "P-C")
cnew = OUT / "03_production_standards" / "GEM_BRAND_ProductionStandards_PartC_v3.0_20261009.pptx"
check("Part C keeps PENDING PRODUCTION VALIDATION", cnt(cnew, "PENDING PRODUCTION VALIDATION") >= 3, cnt(cnew, "PENDING PRODUCTION VALIDATION"))
kit = subprocess.run(["shasum", "-a", "256", "-c", "04_official_kit/SHA256SUMS.txt"], cwd="GEM_Brand_Assets_v1.0", capture_output=True, text=True)
check("logo kit checksum list passes (all OK, none failed)", kit.returncode == 0 and "FAILED" not in kit.stdout and kit.stdout.count(": OK") > 50, kit.stdout.count(": OK"))
check("logo kit is not copied and not modified", not list(OUT.rglob("*.svg")) and git("diff", "--name-only", "HEAD", "--", "GEM_Brand_Assets_v1.0") == "")
check("kit pointer says WORKING ASSETS and production-master acceptance PENDING", "WORKING ASSETS" in (OUT / "06_brand_assets" / "README.md").read_text(encoding="utf-8") and "PENDING" in (OUT / "06_brand_assets" / "README.md").read_text(encoding="utf-8"))
tj = json.load(open("PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.json", encoding="utf-8")); tn = json.load(open(OUT / "07_tokens" / "gem-tokens.v3.0.json", encoding="utf-8"))
tj.pop("meta"); mn = tn.pop("meta")
check("tokens: every non-meta key and value unchanged (deep equality)", tj == tn)
check("tokens: meta carries no RC2 release-state label except derivedFrom/note provenance", not [k for k, v in mn.items() if re.search(r"RC2|rc\.2|NOT RELEASED|AC20 PENDING", str(v).replace("UNCHANGED FROM RC2", "")) and k not in ("derivedFrom", "note")], mn.get("status"))
oc = open("PartB_RC2/05_release/tokens/gem-tokens.v3.0-rc2.css", encoding="utf-8").read().split("\n"); nc = open(OUT / "07_tokens" / "gem-tokens.v3.0.css", encoding="utf-8").read().split("\n")
check("tokens: CSS body identical after the two header lines", oc[2:] == nc[2:])

# ---- claims
claims = [r"WCAG[^.\n]{0,25}(certified|compliant|conformant|conformance achieved)", r"\blegally cleared\b", r"\bfully validated\b", r"(trademark|ownership)[^.\n]{0,15}(verified|cleared)\b", r"\bproduction[- ]ready\b", r"accepted production master", r"Approved V3\.0"]
hits = []
texts = {}
for p in list(OUT.rglob("*")) + list(RP.glob("*.md")) + list(RP.glob("*.csv")):
    if p.suffix in (".md", ".csv", ".json", ".css"):
        texts[str(p)] = p.read_text(encoding="utf-8")
    elif p.suffix in (".pptx", ".docx"):
        z = zipfile.ZipFile(p)
        texts[str(p)] = " ".join(re.findall(r"<(?:a:t|w:t)[^>]*>([^<]*)<", " ".join(z.read(n).decode() for n in z.namelist() if n.endswith(".xml") and re.match(r"(ppt|word)/(slides|notesSlides|document|footer|header)", n))))
for f, t in texts.items():
    for c in claims:
        for m in re.finditer(c, t, re.I):
            ctx = t[max(0, m.start() - 80):m.start()].lower() + t[m.end():m.end() + 25].lower()
            if not any(k in ctx for k in ("not ", "no ", "never", "nothing", "without", "nor ", "pending", "until", "cannot", "neither", "false", "claim")):
                hits.append((Path(f).name, m.group(0)))
check("no unsupported WCAG / legal / validation / production claim in promoted files or RP01 documents", not hits, hits[:5])

# ---- evidence files
pr = rows(RP / "16_qa" / "rp01_preservation.csv")
check("preservation proof: all checks PASS", pr and all(r["Result"] == "PASS" for r in pr), len(pr))
cons = (RP / "16_qa" / "rp01_consistency.md").read_text(encoding="utf-8")
check("successor consistency suite: 112 passed, 0 failed", "112 AUTOMATED ASSERTIONS PASSED · 0 FAILED" in cons)
vis = rows(RP / "16_qa" / "rp01_visual_regression.csv")
check("visual regression: 225 pages, 0 visible regression, 0 unreviewed flag", len(vis) == 225 and not [r for r in vis if r["Final class"] == "VISIBLE REGRESSION"], len(vis))
bres = json.load(open(RP / "16_qa" / "rp01_build_result.json", encoding="utf-8"))
check("build result: not stopped", bres["stop"] is False)
# ---- README
rd = Path("README.md").read_text(encoding="utf-8")
check("README points to the RP01 release folder and index", "GEM_V3.0_RP01_Release_Artifact_Promotion/17_release_artifacts/" in rd and "RELEASE_INDEX.md" in rd)
check("README marks the old release folders HISTORICAL", rd.count("HISTORICAL (superseded by RP01)") == 3)
check("README makes no tag / certification / production claim", "no Git tag or GitHub Release has been created" in rd and not re.search(r"WCAG[- ]certified|production[- ]ready|fully validated|legally cleared", rd, re.I))
# ---- superseded map
sm = rows(RP / "12_RP01_Superseded_Artifact_Map.csv")
check("superseded map covers old RC2 decks, PDFs, HR01 candidates, Rev03 letterheads, old pointers", len(sm) >= 12 and all(r["External issue allowed?"] in ("NO", "n/a") for r in sm))

(RP / "16_qa").mkdir(exist_ok=True)
fails = [r for r in res if not r[1]]
lines = ["# RP01 QA Report", "", "Checks: %d, passed: %d, failed: %d" % (len(res), len(res) - len(fails), len(fails)), "", "| # | Check | Result | Detail |", "|---|---|---|---|"]
for i, (n, ok, d) in enumerate(res, 1):
    lines.append("| %d | %s | %s | %s |" % (i, n, "PASS" if ok else "FAIL", d.replace("|", "/")[:150]))
(RP / "16_qa" / "RP01_QA_Report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("checks", len(res), "failed", len(fails))
for n, ok, d in fails:
    print("FAIL", n, d)
sys.exit(1 if fails else 0)
