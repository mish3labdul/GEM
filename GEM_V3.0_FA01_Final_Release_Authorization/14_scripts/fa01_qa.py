#!/usr/bin/env python3
"""FA01 QA. Run from the repository root: python3 -I GEM_V3.0_FA01_Final_Release_Authorization/14_scripts/fa01_qa.py
Writes 15_qa/FA01_QA_Report.md and exits non-zero on any failure."""
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

PKG = Path("GEM_V3.0_FA01_Final_Release_Authorization")
HR = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/18_candidate_corrections")
REG = Path("GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def git(*a):
    return subprocess.run(["git", "-c", "core.quotepath=off", *a], capture_output=True, text=True).stdout.rstrip("\n")


def rows(name):
    with open(PKG / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


md = sorted(PKG.glob("*.md"))
texts = {p.name: p.read_text(encoding="utf-8") for p in md}
alltxt = "\n".join(texts.values()) + "\n".join(p.read_text(encoding="utf-8") for p in PKG.glob("*.csv"))

# structure
need = ["01_FA01_Executive_Summary.md", "02_FA01_AC20_Decision_Record.md", "03_FA01_Release_Governance_Options.md", "05_FA01_Deferral_Treatment.md",
        "06_FA01_Brand_Owner_Holder_Record.md", "07_FA01_D8_External_Issue_Policy.md", "08_FA01_AC19_Disposition.md", "11_FA01_Residual_Limitations.md",
        "12_FA01_Governance_Supersession_Log.md", "13_FA01_Evidence_Index.md", "04_FA01_Final_Owner_Decisions.csv", "05b_FA01_Gate_Disposition_Register.csv",
        "09_FA01_AC20_Acceptance_Test.csv", "10_FA01_Release_Scope_Matrix.csv"]
check("all required FA01 files exist", all((PKG / n).exists() for n in need), str([n for n in need if not (PKG / n).exists()]))

# git state: only README tracked-modified; nothing pushed
changed = [l[3:] for l in git("status", "--short").splitlines() if not l.startswith("??")]
check("only README.md is a tracked modification", changed == ["README.md"], str(changed))
check("origin/main unchanged", git("rev-parse", "origin/main") == "4ea0d117da03850854654288afcdde98f39994d5")
check("origin branch still at HR01", git("rev-parse", "origin/claude/gem-worktree-safety-30b559").startswith("617456255231a6b3"))
check("approval register sha unchanged", hashlib.sha256(REG.read_bytes()).hexdigest() == "ccce46135a4f2244dbff21cef94a6160e9d2b6fd96a63647c1e5ea6b662e7ab3")
protected = git("diff", "--name-only", "HEAD").splitlines()
check("no historical package edited", not [p for p in protected if re.match(r"GEM_V3\.0_RC2_(AR01|AX01|OD01|HR01|FD01)|GEM_V3_RC2/00_originals|GEM_V3\.0_RC2_(D3|D7|NP01)|qa/", p)], str(protected))
check("no local-only files in FA01", not [p for p in PKG.rglob("*") if p.name in ("CLAUDE.local.md", "settings.local.json")])

# banners and wording
check("every markdown file carries the status banner", all(("GEM™ V3.0" in t[:400]) for n, t in texts.items() if not n.startswith("03_")))
w2 = texts["02_FA01_AC20_Decision_Record.md"]
check("02 holds the exact AC20 wording", "does not constitute independent Legal/IP verification, WCAG certification, validation of any artifact explicitly excluded from external release" in w2)
check("02 states AC20 authorized", "AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS" in w2)
stale = []
for n, t in list(texts.items()) + [(c.name, c.read_text(encoding="utf-8")) for c in PKG.glob("*.csv")]:
    if n.startswith("03_"):
        continue
    for pat in ("PROPOSED", "NOT YET AUTHORIZED", "AC20: OPEN", "AC20 OPEN", "pending owner confirmation", "PENDING OWNER CONFIRMATION", "only if the owner confirms"):
        for line in t.splitlines():
            if pat in line and not (n.startswith("12_") and line.startswith("| ")):
                stale.append((n, pat))
check("authorized-mode: no proposal / conditional / open-AC20 wording outside the 03 snapshot and the 12 table rows", not stale, str(stale[:6]))

# registers
dec = rows("04_FA01_Final_Owner_Decisions.csv")
check("04 records A, B, C, E, AC20", {"FA-A", "FA-B", "FA-C", "FA-E", "FA-AC20"} <= {r["Decision ID"] for r in dec})
check("04 holder is Mashal / Brand Owner", any("Mashal" in r["Selection (exact)"] and "Brand Owner" in r["Selection (exact)"] for r in dec))
check("04 no decision constitutes verification", all(r["Constitutes evidence verification?"] == "NO" for r in dec))
gates = rows("05b_FA01_Gate_Disposition_Register.csv")
ids = {r["Gate / item"] for r in gates}
want = {"VAL-%02d" % i for i in range(1, 22)} | {"Y01", "Y02", "Y03", "Y04", "AC07", "AC10", "AC17", "AC19", "AC20", "OD-TPL", "OD-SRC", "D8", "SR-11", "SR-12"}
check("05b covers every gate", want <= ids, str(sorted(want - ids)))
check("05b closes no gate by evidence", all(r["Closed by evidence?"] in ("NO", "n/a") for r in gates))
check("05b AC19 not closed", any(r["Gate / item"] == "AC19" and "OPEN" in r["FA01 disposition"] and "CLOSED" not in r["FA01 disposition"] for r in gates))
tests = rows("09_FA01_AC20_Acceptance_Test.csv")
check("09 has 15 tests, none FAIL or NOT YET", len(tests) == 15 and not [t for t in tests if t["Result"].startswith(("FAIL", "NOT YET"))], str([t["Result"] for t in tests]))
check("09 uses PASS WITH FORMAL DEFERRAL for gate-dependent tests", sum(t["Result"] == "PASS WITH FORMAL DEFERRAL" for t in tests) >= 6)
scope = rows("10_FA01_Release_Scope_Matrix.csv")
check("10 has the required streams", len(scope) >= 17)
d8 = [r for r in scope if "letterhead" in r["Artifact / stream"] and ("Arabic" in r["Artifact / stream"] or "Bilingual" in r["Artifact / stream"])]
check("10 blocks external issue for all four Arabic/bilingual letterheads", len(d8) == 4 and all(r["External issue eligible?"] == "NO" and "D8" in r["Restriction"] for r in d8))
check("10 no row allows unrestricted external issue", all(r["External issue eligible?"] != "YES" for r in scope))
partd = [r for r in scope if r["Artifact / stream"].startswith("Part D")]
check("10 Part D stays CONCEPT / NOT PRODUCTION ARTWORK", partd and "CONCEPT / NOT PRODUCTION ARTWORK" in partd[0]["Current evidence status"] + partd[0]["Restriction"])
kit = [r for r in scope if r["Artifact / stream"] == "Official Logo Kit"]
check("10 logo kit WORKING ASSETS", kit and "WORKING ASSETS" in kit[0]["Current evidence status"])
vec = [r for r in scope if r["Artifact / stream"].startswith("Production vectors")]
check("10 production vectors not production masters", vec and vec[0]["Release eligible (baseline member)?"].startswith("NO"))

# baseline hashes re-verified against files
bad = []
for f in HR.iterdir():
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    if f.name in alltxt and ("sha256 %s" % h) not in alltxt:
        bad.append(f.name)
check("03 is marked a pre-decision snapshot", "PRE-DECISION SNAPSHOT" in texts["03_FA01_Release_Governance_Options.md"])
check("single release name string used", all("FINAL BRAND SYSTEM BASELINE" not in t for t in texts.values()))
kit = subprocess.run(["shasum", "-a", "256", "-c", "04_official_kit/SHA256SUMS.txt"], cwd="GEM_Brand_Assets_v1.0", capture_output=True, text=True)
check("logo kit files match their SHA256SUMS.txt", kit.returncode == 0 and "FAILED" not in kit.stdout, (kit.stderr or kit.stdout)[-160:])
check("10 baseline hashes match the HR01 candidate files", not bad, str(bad))
check("10 names all 8 HR01 candidates", all(f.name in alltxt for f in HR.iterdir()))

# claim hygiene
claims = [r"WCAG 2\.2 AA (compliant|conformant|certified|conformance (is )?(achieved|demonstrated))", r"\blegally cleared\b", r"\bfully validated\b", r"trademark (is )?(verified|cleared)\b",
          r"\bowner(ship)? (is )?independently verified\b", r"\bproduction[- ]ready\b", r"(?-i:Approved V3\.0)"]
hits = []
for n, t in list(texts.items()) + [(c.name, c.read_text(encoding="utf-8")) for c in PKG.glob("*.csv")]:
    for c in claims:
        for m in re.finditer(c, t, re.I):
            ctx = t[max(0, m.start() - 60):m.start()].lower()
            if not any(k in ctx for k in ("not ", "no ", "never", "nothing", "without", "nor ")):
                hits.append((n, m.group(0)))
check("no unsupported WCAG / legal / validation claims", not hits, str(hits))
check("Legal/IP described as owner accepted under formal deferral", "OWNER ACCEPTED UNDER FORMAL DEFERRAL" in alltxt)
check("macOS VoiceOver described as reviewer observed", "REVIEWER OBSERVED" in alltxt)
check("Windows and PDF stay deferred", "SR-12" in alltxt and "FORMALLY DEFERRED (not performed)" in alltxt)
check("no remote operation recorded as done", not re.search(r"\b(pushed|merged|tag created|release created) (to|on)\b", alltxt, re.I))
check("no absolute user paths or credential patterns", not re.search(r"/Users/|ghp_|github_pat_|api[_-]?key\s*[:=]", alltxt, re.I))

# README
rd = Path("README.md").read_text(encoding="utf-8")
check("README points to FA01 narrowly", "GEM_V3.0_FA01_Final_Release_Authorization/" in rd and "limited release baseline" in rd and rd.count("FA01") >= 2)
check("README does not claim approved V3.0 or production", "Approved V3.0**" not in rd.split("Current AC20")[-1] and "production-ready" not in rd.lower())

(PKG / "15_qa").mkdir(exist_ok=True)
fails = [r for r in results if not r[1]]
lines = ["# FA01 QA Report", "", "Checks: %d, passed: %d, failed: %d" % (len(results), len(results) - len(fails), len(fails)), "", "| # | Check | Result | Detail |", "|---|---|---|---|"]
for i, (n, ok, d) in enumerate(results, 1):
    lines.append("| %d | %s | %s | %s |" % (i, n, "PASS" if ok else "FAIL", d.replace("|", "/")[:160]))
(PKG / "15_qa" / "FA01_QA_Report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("checks", len(results), "failed", len(fails))
for n, ok, d in fails:
    print("FAIL", n, d)
sys.exit(1 if fails else 0)
