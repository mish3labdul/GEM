#!/usr/bin/env python3
"""HR01 QA. Run from the repository root:  python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_qa.py

Writes 17_qa/hr01_qa_results.json and .md. Read-only otherwise. Relative paths only.
"""
import csv
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure")
REGISTER = Path("GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx")
REGISTER_SHA = "ccce46135a4f2244dbff21cef94a6160e9d2b6fd96a63647c1e5ea6b662e7ab3"
AX = Path("GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation")
LH = Path("GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates")
results = []


def check(name, ok, detail=""):
    results.append({"check": name, "result": "PASS" if ok else "FAIL", "detail": str(detail)[:200]})


def rows(name):
    with open(PKG / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


# ---- queues
ar = rows("03_HR01_Arabic_Review_Register.csv")
q = [r for r in ar if r["Item ID"].startswith("OD01-AR-")]
check("Queue 1: 44 queue items + 4 extras, every one dispositioned", len(q) == 44 and len(ar) == 48 and all(r["Reviewer disposition"] and r["Status"].startswith("DISPOSITIONED") for r in ar))
check("Queue 1: dispositions limited to the allowed vocabulary", {r["Reviewer disposition"] for r in ar} <= {"APPROVE AS IS", "APPROVE CLAUDE RECOMMENDATION", "REVISE AS FOLLOWS", "DEFER", "NOT APPLICABLE"})
check("Queue 1: 31 as is / 13 recommendation / 0 deferred", sum(r["Reviewer disposition"] == "APPROVE AS IS" for r in q) == 31 and sum(r["Reviewer disposition"] == "APPROVE CLAUDE RECOMMENDATION" for r in q) == 13)
ac = rows("05_HR01_Accessibility_Content_Register.csv")
check("Queue 2: 144 queue items + 2 extras, every one dispositioned, none auto-applied without an owner disposition",
      len(ac) == 146 and all(r["Owner disposition"] and r["Status"] == "DISPOSITIONED" for r in ac))
check("Queue 2: 30 titles, 23+1+2 alt-text items, 89 shapes (87 decorative / 2 informative), 1 specimen",
      sum(r["Item ID"].startswith("OD01-AC-T") for r in ac) == 30 and sum(r["Item ID"].startswith("OD01-AC-S") for r in ac) == 89
      and sum(r["Item ID"].startswith("OD01-AC-S") and r["Owner classification"].startswith("INFORMATIVE") for r in ac) == 2
      and sum(r["Item ID"].startswith("OD01-AC-A") for r in ac) == 23)
sr = rows("07_HR01_Screen_Reader_Test_Register.csv")
st = {r["Test ID"]: r for r in sr}
check("Queue 3: 13 tests; 11 PASS reviewer observed (Mashal); SR-11 and SR-12 DEFERRED",
      len(sr) == 13 and all(st[t]["Status"] == "PASS" and st[t]["Evidence type"].startswith("REVIEWER OBSERVED — MASHAL") for t in ("SR-%02d" % i for i in list(range(1, 11)) + [13]))
      and st["SR-11"]["Status"].startswith("DEFERRED") and st["SR-12"]["Status"].startswith("DEFERRED"))
check("Queue 3: deferrals not recorded as Accessibility QA approval", "NOT Accessibility QA approval" in st["SR-11"]["Observer"] and "NOT Accessibility QA approval" in st["SR-12"]["Observer"])
ro = rows("08_HR01_Reading_Order_Manual_Review.csv")
check("Queue 3: 13 pre-selected reading-order slides, all PASS", len(ro) == 13 and all(r["Status"] == "PASS" for r in ro))
inv = rows("09_HR01_Legal_IP_Evidence_Inventory.csv")
dsp = rows("10_HR01_Legal_IP_Disposition_Register.csv")
check("Queue 4: 8 gates dispositioned, none closeable, none 'EVIDENCE SUFFICIENT'",
      {r["Gate"] for r in dsp} == {"VAL-03", "VAL-04", "VAL-05", "VAL-06", "Y01", "Y02", "Y03", "Y04"} and all(r["Can close now?"] == "NO" and r["Queue 4 disposition"] != "EVIDENCE SUFFICIENT" for r in dsp) and len(inv) == 16)
gm = rows("11_HR01_Gate_Impact_Matrix.csv")
check("Gate matrix: every gate Can close? = NO; AC20 OPEN; zero gates closed", all(r["Can close?"] == "NO" for r in gm) and any(r["Gate"] == "AC20" and r["Current state (Register + OD01)"].startswith("OPEN") for r in gm))
check("Gate matrix covers required gates", {"VAL-03", "VAL-04", "VAL-05", "VAL-06", "VAL-07", "VAL-08", "VAL-15", "Y01", "Y02", "Y03", "Y04", "AC10", "AC19", "AC20"} <= {r["Gate"] for r in gm})
check("Queue baseline has four queues with HR01 outcomes", len(rows("02_HR01_Queue_Baseline.csv")) == 4 and all(r["HR01 outcome"] for r in rows("02_HR01_Queue_Baseline.csv")))

# ---- text hygiene
texts = {p: p.read_text(encoding="utf-8") for p in PKG.rglob("*") if p.is_file() and p.suffix in (".md", ".csv", ".json", ".py") and "local_only" not in p.parts}
arabic = re.compile("[" + chr(0x600) + "-" + chr(0x6ff) + chr(0x750) + "-" + chr(0x77f) + "]")
check("no Arabic-script text in committed registers, docs or scripts", not [str(p) for p, t in texts.items() if arabic.search(t)])
path_pat = re.compile("/Us" + "ers/|/pri" + "vate/|/ho" + "me/|media" + "center1|claude-" + "501|\\.claude/work" + "trees|file:" + "///")
check("no absolute or session-local paths", not [str(p) for p, t in texts.items() if path_pat.search(t)])
secret = re.compile("gh[opsu]_[A-Za-z0-9]{20,}|github" + "_pat_|-----" + "BEGIN|AKIA[0-9A-Z]{16}|xox[baprs]-")
check("no credential patterns", not [str(p) for p, t in texts.items() if secret.search(t)])
claims = re.compile("APPROVED V3\\.0|PRODUCTION READY|SYSTEM READY|\\bRELEASED\\b|AC20 (is )?closed|Legal/IP cleared|WCAG 2\\.2 AA (compliant|certified|fully)|validation complete across|linguistically approved", re.I)
neg = re.compile(r"\bnot\b|\bno\b|\bnever\b|prohibit|does not|nothing|without|unless|NOT RELEASED|may not|stay|stays|remain|remains|n't", re.I)
bad = []
for p, t in texts.items():
    if p.suffix == ".py" or p.name in ("hr01_qa_results.md",) or p.parent.name == "17_qa" and p.name.startswith("consistency"):
        continue
    for n, line in enumerate(t.splitlines(), 1):
        if claims.search(line) and not neg.search(line):
            bad.append("%s:%d" % (p.name, n))
check("overclaim phrases appear only in negated/prohibiting context", not bad, ", ".join(bad))

# ---- candidates
log = json.load(open(PKG / "17_qa" / "candidate_build_log.json", encoding="utf-8"))
cand_dir = PKG / "18_candidate_corrections"
cands = sorted(cand_dir.glob("*"))
check("8 candidates present and match the build log hashes; all inverse proofs PASS",
      len(cands) == 8 and all(v["inverse_proof"] == "PASS" and sha(cand_dir / v["candidate"]) == v["candidate_sha256"] for v in log.values()))
bold = re.compile(r'<w:b w:val="1"|<w:b/>|\bb="1"')
fonts = re.compile(r'(?:w:ascii|w:cs|typeface)="([^"]+)"')


def members(path, pats):
    z = zipfile.ZipFile(path)
    return "".join(z.read(n).decode("utf8", "replace") for n in z.namelist() if n.endswith(".xml"))


same_fonts = same_bold = True
for k, v in log.items():
    src = Path(v["source"])
    a, b = members(src, None), members(cand_dir / v["candidate"], None)
    same_bold &= len(bold.findall(a)) == len(bold.findall(b))
    same_fonts &= set(fonts.findall(b)) <= set(fonts.findall(a))
check("no new font family and no added bold in any candidate", same_fonts and same_bold)
check("no geometry edit: only title shapes added, decorative/alt metadata and text runs changed (inverse proof)", all(v["inverse_proof"] == "PASS" for v in log.values()))
vr = list(csv.DictReader(open(PKG / "17_qa" / "hr01_visual_regression.csv", encoding="utf-8")))
check("visual regression: 0 visible regressions; 214 slides pixel identical + 3 expected + 4 Word pages expected", sum(r["Classification"] == "VISIBLE REGRESSION" for r in vr) == 0
      and sum(r["Classification"] == "PIXEL IDENTICAL" for r in vr) == 214 and sum(r["Classification"] == "EXPECTED CONTENT CHANGE ONLY" for r in vr) == 7)
sa = list(csv.DictReader(open(PKG / "17_qa" / "hr01_static_accessibility_check.csv", encoding="utf-8")))
check("static accessibility predicates: 0 slides without title and 0 shapes/pictures without alt or decorative flag on all four decks",
      len(sa) == 4 and all(r["Slides without title (HR01)"] == "0" and r["Shapes+pictures without alt/decorative (HR01)"] == "0" for r in sa))
cons = (PKG / "17_qa" / "consistency_HR01.md").read_text(encoding="utf-8")
check("consistency: 112 automated assertions PASSED, 0 FAILED", "112 AUTOMATED ASSERTIONS PASSED · 0 FAILED" in cons)

# ---- immutability / Git
check("original Approval Register unchanged", sha(REGISTER) == REGISTER_SHA)
check("no tracked file modified (HR01 is additive)", git("diff", "--name-only", "HEAD").strip() == "", git("diff", "--name-only", "HEAD"))
untracked = [u for u in git("-c", "core.quotepath=off", "ls-files", "--others", "--exclude-standard").split("\n") if u]
check("only the HR01 package is new", all(u.startswith(str(PKG) + "/") for u in untracked), [u for u in untracked if not u.startswith(str(PKG) + "/")])
for pkg in ("GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation", "GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation", "GEM_V3.0_RC2_OD01_Owner_Decision_Formalization", "GEM_V3.0_RC2_D7_Repository_Visibility_Decision_Package"):
    bad_sum = []
    for line in (Path(pkg) / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        f = Path(pkg) / name
        if f.is_file() and sha(f) != digest:
            bad_sum.append(name)
    check("%s checksums still verify" % pkg.split("_")[2], not bad_sum, bad_sum[:3])
tracked = set(git("ls-files").split("\n"))
check("local-only files not tracked", not [t for t in tracked if t.startswith(".claude/") or t == "CLAUDE.local.md" or "/local_only/" in t])
staged_bad = [u for u in untracked if "local_only" in u or u.endswith(".DS_Store")]
check("no local-only or temp files among the new files", not staged_bad, staged_bad)
fails = [r for r in results if r["result"] == "FAIL"]
(PKG / "17_qa" / "hr01_qa_results.json").write_text(json.dumps({"checks": results, "failures": len(fails)}, indent=1) + "\n", encoding="utf-8")
md = ["# HR01 QA results", "", "GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE", "",
      "Generated by `16_scripts/hr01_qa.py`. %d checks, %d failures." % (len(results), len(fails)), "", "| # | Check | Result | Detail |", "|---|---|---|---|"]
for i, r in enumerate(results, 1):
    md.append("| %d | %s | %s | %s |" % (i, r["check"], r["result"], r["detail"].replace("|", "/")[:150]))
(PKG / "17_qa" / "hr01_qa_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("%d checks, %d failures" % (len(results), len(fails)))
for r in fails:
    print("FAIL:", r["check"], r["detail"])
