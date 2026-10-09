#!/usr/bin/env python3
"""OD01 QA. Run from the repository root:  python3 -I GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/11_scripts/od01_qa.py

Writes 12_qa/od01_qa_results.json and 12_qa/od01_qa_results.md. Read-only otherwise. Relative paths only.
"""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

OD = Path("GEM_V3.0_RC2_OD01_Owner_Decision_Formalization")
D7 = Path("GEM_V3.0_RC2_D7_Repository_Visibility_Decision_Package")
REGISTER = Path("GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx")
REGISTER_SHA = "ccce46135a4f2244dbff21cef94a6160e9d2b6fd96a63647c1e5ea6b662e7ab3"
HISTORICAL = [
    "GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation", "GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation",
    "GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01", "GEM_V3.0_RC2_NP01-R1_Native_Layout_Correction",
    "GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1", "GEM_V3.0_RC2_D3_Owner_Decision_Package",
    "GEM_V3_RC2", "PartB_RC2", "Amenities_Portfolio_PartD_RC2", "GEM_Brand_Assets_v1.0",
    "GEM_Letterhead_Set_v1.1_Application_Revision_03", "qa",
]
ALLOWED_TRACKED_CHANGES = {
    "README.md",
    str(D7 / "09_D7_Owner_Decision_Record.md"), str(D7 / "MANIFEST.json"), str(D7 / "SHA256SUMS.txt"),
}
results = []


def check(name, ok, detail=""):
    results.append({"check": name, "result": "PASS" if ok else "FAIL", "detail": detail})


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(name):
    with open(OD / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


# 1 decision register
reg = {r["Decision ID"]: r for r in rows("02_OD01_Owner_Decision_Register.csv")}
check("register has OD-G01..OD-G12", sorted(reg) == ["OD-G%02d" % i for i in range(1, 13)], str(sorted(reg)))
check("OD-G01..G08 = APPROVED", all(reg["OD-G%02d" % i]["Status"] == "APPROVED" for i in range(1, 9)))
check("OD-G09 and OD-G10 = ASSIGNED to Mashal",
      all(reg[k]["Status"] == "ASSIGNED" and "Mashal" in reg[k]["Decision"] for k in ("OD-G09", "OD-G10")))
check("OD-G11 = RESOLVED — OWNER REPOSITORY VISIBILITY APPROVAL (exact string), current public approved",
      reg["OD-G11"]["Status"] == "RESOLVED — OWNER REPOSITORY VISIBILITY APPROVAL"
      and "OD-G11 — C — CURRENT PUBLIC REPOSITORY APPROVED" in reg["OD-G11"]["Decision"])
check("OD-G12 = OPEN — FINAL RELEASE AUTHORIZATION PENDING (exact string)", reg["OD-G12"]["Status"] == "OPEN — FINAL RELEASE AUTHORIZATION PENDING")
check("no decision closes an evidence gate", all(r["Does this close an evidence gate?"] == "NO" for r in reg.values()))
imp = rows("04_OD01_Gate_Impact_Matrix.csv")
check("impact matrix closes no gate", all(r["Gate closed by decision?"].startswith("NO") for r in imp), "%d rows" % len(imp))

# 2 evidence view
ev = {r["ID"]: r for r in rows("08_OD01_Open_Evidence_After_Decisions.csv")}
need = ["VAL-%02d" % i for i in range(1, 22)] + ["Y01", "Y02", "Y03", "Y04", "AC07", "AC10", "AC17", "AC19", "AC20", "OD-TPL", "OD-SRC"]
check("evidence view covers every required ID", all(i in ev for i in need), str([i for i in need if i not in ev]))
check("no evidence item can close now", all(r["Can close now?"] in ("NO", "n/a") for r in ev.values()))
check("VAL-18 = NOT ALLOCATED", ev["VAL-18"]["Current status"] == "NOT ALLOCATED")
check("AC20 = OPEN / FINAL RELEASE AUTHORIZATION PENDING", ev["AC20"]["Current status"] == "OPEN / FINAL RELEASE AUTHORIZATION PENDING")
check("Legal/IP gates VAL-03..06 and Y01..Y04 not closed",
      all(ev[i]["Can close now?"] == "NO" for i in ["VAL-03", "VAL-04", "VAL-05", "VAL-06", "Y01", "Y02", "Y03", "Y04"]))

# 3 queues
ar = rows("OD01_Mashal_Arabic_Review_Queue.csv")
ac = rows("OD01_Mashal_Accessibility_Content_Queue.csv")
check("Arabic review queue rows carry element, SHA prefix and AR01 row",
      all("SHA " in r["Slide/page (slide \u00b7 element \u00b7 text SHA prefix \u00b7 AR01 row)"] and "AR01 queue row" in r["Slide/page (slide \u00b7 element \u00b7 text SHA prefix \u00b7 AR01 row)"] for r in ar))
check("Arabic review queue has 44 items, all PENDING, dispositions blank",
      len(ar) == 44 and all(r["Status"] == "PENDING" and not r["Reviewer disposition"] and not r["Reviewer note"] for r in ar))
check("accessibility queue: 30 titles, 23 pictures, 89 shapes, 2 further; all pending, nothing pre-filled",
      len(ac) == 144 and sum(r["Item ID"].startswith("OD01-AC-T") for r in ac) == 30
      and sum(r["Item ID"].startswith("OD01-AC-A") for r in ac) == 23
      and sum(r["Item ID"].startswith("OD01-AC-S") for r in ac) == 89
      and all(r["Status"].startswith("PENDING") and not r["Owner disposition"] and not r["Approved title/alt-text reference"] for r in ac))

# 4 text hygiene
texts = {p: p.read_text(encoding="utf-8") for p in OD.rglob("*") if p.is_file() and p.suffix in (".md", ".csv", ".json")}
arabic = re.compile("[؀-ۿݐ-ݿ]")
check("no Arabic-script text in the package", not any(arabic.search(t) for t in texts.values()))
path_pat = re.compile("/Us" + "ers/|/pri" + "vate/|/ho" + "me/|media" + "center1|claude-" + "501|\\.claude/work" + "trees")
check("no absolute or session-local paths in the package",
      not [str(p) for p, t in texts.items() if path_pat.search(t) and p.name != "od01_qa.py"])
secret = re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}|github_pat_|-----BEGIN|AKIA[0-9A-Z]{16}|xox[baprs]-")
check("no credentials patterns", not [str(p) for p, t in texts.items() if secret.search(t)])
claims = re.compile(r"APPROVED V3\.0|Approved V3\.0|PRODUCTION READY|Production Ready|SYSTEM READY|System Ready|\bRELEASED\b|AC20 (is )?closed|"
                    r"Legal/IP cleared|WCAG 2\.2 AA fully demonstrated|linguistically approved", re.I)
neg = re.compile(r"\bnot\b|\bno\b|\bnever\b|prohibited|stays?\b|NOT RELEASED|may not|nothing|does not|without|unless", re.I)
bad = []
for p, t in texts.items():
    if p.suffix == ".py" or p.name == "od01_qa_results.md":
        continue
    for n, line in enumerate(t.splitlines(), 1):
        if claims.search(line) and not neg.search(line):
            bad.append("%s:%d" % (p.name, n))
check("overclaim phrases appear only in negated/prohibiting context", not bad, ", ".join(bad))
check("S07 not broadened (OD-G01 scope states wayfinding limit)",
      "does NOT broaden S07" in reg["OD-G01"]["Effective scope"] and "S07" in (OD / "03_OD01_Decision_Detail.md").read_text(encoding="utf-8"))
check("public approval stated as not a legal opinion",
      "not a legal opinion" in (OD / "06_OD01_D7_Repository_Visibility_Decision.md").read_text(encoding="utf-8"))
check("committed package does not claim the branch is published",
      not re.search(r"PUBLISHED TO GITHUB|has been pushed|was pushed", "\n".join(texts.values()), re.I))

# 5 immutability
check("original Approval Register unchanged", sha(REGISTER) == REGISTER_SHA)
changed = set(git("diff", "--name-only", "HEAD").split("\n")) - {""}
outside = {c for c in changed - ALLOWED_TRACKED_CHANGES if not c.startswith(str(OD) + "/")}
check("only allowed tracked files changed (OD01 package, D7 record + checksums, README)", not outside, str(sorted(outside)))
untracked = set(git("ls-files", "--others", "--exclude-standard").split("\n")) - {""}
check("only the OD01 package is new", all(u.startswith(str(OD) + "/") for u in untracked), str(sorted(u for u in untracked if not u.startswith(str(OD) + "/"))))
touched_hist = [c for c in changed if any(c == h or c.startswith(h + "/") for h in HISTORICAL)]
check("no historical package modified (AR01, AX01, NP01, NP01-R1, ODI01-R1, D3, RC2 originals, qa)", not touched_hist, str(touched_hist))
for pkg in ("GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation", "GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation",
            "GEM_V3.0_RC2_Native_PowerPoint_Validation_NP01"):
    bad_sum = []
    for line in (Path(pkg) / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        f = Path(pkg) / name
        if f.is_file() and sha(f) != digest:
            bad_sum.append(name)
    check("%s checksums still verify" % pkg.split("_")[2], not bad_sum, str(bad_sum[:5]))
bad_d7 = []
for line in (D7 / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    digest, name = line.split("  ", 1)
    if sha(D7 / name) != digest:
        bad_d7.append(name)
check("D7 package checksums verify after the 09 update", not bad_d7, str(bad_d7))
d7rec = (D7 / "09_D7_Owner_Decision_Record.md").read_text(encoding="utf-8")
check("D7 record: OD-G11 recorded verbatim, taxonomy note present, no legacy option ticked, Legal/IP reviewer NOT PROVIDED",
      ("OD-G11 \u2014 C \u2014 CURRENT PUBLIC REPOSITORY APPROVED" in d7rec or "**OD-G11 \u2014 C \u2014 CURRENT PUBLIC REPOSITORY APPROVED**" in d7rec)
      and "independent of the historical D7 option lettering" in d7rec
      and len(re.findall(r"\[x\] [A-E] ", d7rec)) == 0 and "NOT PROVIDED" in d7rec)
check("AC19 stated OPEN / HOLDER CONDITION INCOMPLETE and not closed",
      "OPEN / HOLDER CONDITION INCOMPLETE" in ev["AC19"]["Current status"] and ev["AC19"]["Can close now?"] == "NO")
check("D7 record keeps Legal/IP evidence open and AC20 open", "AC20 remains OPEN" in d7rec and "OPEN WHERE THE GOVERNING GATES REQUIRE IT" in d7rec)

# 6 local-only files
tracked = set(git("ls-files").split("\n"))
check("CLAUDE.local.md, .claude/ and local_only/ not tracked",
      not [t for t in tracked if t.startswith(".claude/") or t == "CLAUDE.local.md" or "/local_only/" in t])

fails = [r for r in results if r["result"] == "FAIL"]
(OD / "12_qa" / "od01_qa_results.json").write_text(json.dumps({"checks": results, "failures": len(fails)}, indent=1) + "\n", encoding="utf-8")
md = ["# OD01 QA results", "",
      "GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE", "",
      "Generated by `11_scripts/od01_qa.py`. %d checks, %d failures." % (len(results), len(fails)), "",
      "| # | Check | Result | Detail |", "|---|---|---|---|"]
for i, r in enumerate(results, 1):
    md.append("| %d | %s | %s | %s |" % (i, r["check"], r["result"], r["detail"].replace("|", "/")[:160]))
(OD / "12_qa" / "od01_qa_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("%d checks, %d failures" % (len(results), len(fails)))
for r in fails:
    print("FAIL:", r["check"], r["detail"])
