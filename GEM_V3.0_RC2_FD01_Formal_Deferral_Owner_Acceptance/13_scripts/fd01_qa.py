#!/usr/bin/env python3
"""FD01 QA. Run from the repository root:  python3 -I GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance/13_scripts/fd01_qa.py
Writes 14_qa/fd01_qa_results.json and .md. Read-only otherwise. Relative paths only."""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance")
REGISTER = Path("GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx")
REGISTER_SHA = "ccce46135a4f2244dbff21cef94a6160e9d2b6fd96a63647c1e5ea6b662e7ab3"
results = []


def check(name, ok, detail=""):
    results.append({"check": name, "result": "PASS" if ok else "FAIL", "detail": str(detail)[:200]})


def rows(name):
    with open(PKG / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout

od = {r["Decision ID"]: r for r in rows("02_FD01_Owner_Decision_Register.csv")}
check("FD-G01..FD-G06 recorded", sorted(od) == ["FD-G0%d" % i for i in range(1, 7)])
check("FD-G01 status OWNER ACCEPTED / DIGITAL REVIEW FORMALLY DEFERRED", od["FD-G01"]["Status"] == "OWNER ACCEPTED / DIGITAL REVIEW FORMALLY DEFERRED")
check("FD-G02, G03, G04 FORMALLY DEFERRED BY BRAND OWNER", all(od[k]["Status"] == "FORMALLY DEFERRED BY BRAND OWNER" for k in ("FD-G02", "FD-G03", "FD-G04")))
check("FD-G05 and FD-G06 APPROVED", od["FD-G05"]["Status"] == "APPROVED" and od["FD-G06"]["Status"] == "APPROVED")
check("every owner decision has a 'does NOT' limit and no signature is invented", all(r["What the decision does NOT do"] and "no individual name or signature" in r["Owner"] for r in od.values()))
texts_pre = {p: p.read_text(encoding="utf-8") for p in PKG.rglob("*") if p.is_file() and p.suffix in (".md", ".csv") and "14_qa" not in p.parts}
gm = {r["Gate / test"]: r for r in rows("08_FD01_Gate_Impact_Matrix.csv")}
need = ["VAL-03", "VAL-04", "VAL-05", "VAL-06", "Y01", "Y02", "Y03", "Y04", "AC19", "D8", "SR-11", "SR-12", "AC20"]
check("all required gates reassessed", all(n in gm for n in need), [n for n in need if n not in gm])
check("no gate can close (Can close? = NO everywhere)", all(r["Can close?"] == "NO" for r in gm.values()))
check("Legal/IP gates: owner-declared offline, independent verification NOT PERFORMED, none VERIFIED",
      all(gm[g]["Independent verification"].startswith("NOT PERFORMED") and not gm[g]["Evidence level"].startswith("VERIFIED") for g in ("VAL-03", "VAL-04", "VAL-06", "Y01", "Y02", "Y04")))
check("VAL-03 / Y01 stay OPEN — EXTERNAL VERIFICATION NOT PERFORMED", all(gm[g]["New governance status"].startswith("OPEN — EXTERNAL VERIFICATION NOT PERFORMED") for g in ("VAL-03", "Y01")))
check("VAL-06 / Y04 use OWNER ACCEPTED / DIGITAL TERMS REVIEW DEFERRED", all("DIGITAL TERMS REVIEW DEFERRED" in gm[g]["New governance status"] for g in ("VAL-06", "Y04")))
check("no evidence-level cell claims VERIFIED except the font rows' PARTIALLY VERIFIED",
      all((not r["Evidence level"].startswith("VERIFIED")) for r in gm.values()) and all(gm[g]["Evidence level"].startswith("PARTIALLY VERIFIED") for g in ("VAL-05", "Y03")))
check("VAL-07 / VAL-08 macOS evidence labelled REVIEWER OBSERVED, not verified", all(gm[g]["Evidence level"].startswith("REVIEWER OBSERVED") for g in ("VAL-07", "VAL-08")))
check("digital-evidence-retained column set (NO by owner decision for six gates; YES for fonts)", all(gm[g]["Digital evidence retained"].startswith("NO") for g in ("VAL-03", "VAL-04", "VAL-06", "Y01", "Y02", "Y04")) and all(gm[g]["Digital evidence retained"].startswith("YES") for g in ("VAL-05", "Y03")))
check("no row calls the hard copies missing", not [p.name for p, tx in texts_pre.items() if re.search(r"\bmissing\b", tx, re.I)])
check("font evidence kept distinct and preserved (partially verified, repository OFL text)", gm["VAL-05"]["Evidence level"].startswith("PARTIALLY VERIFIED"))
check("AC19 OPEN — FORMALLY DEFERRED; SR-12, SR-11 FORMALLY DEFERRED; D8 OPEN — FORMALLY DEFERRED",
      gm["AC19"]["New governance status"].startswith("OPEN — FORMALLY DEFERRED") and gm["SR-12"]["New governance status"].startswith("FORMALLY DEFERRED BY BRAND OWNER")
      and gm["SR-11"]["New governance status"].startswith("FORMALLY DEFERRED BY BRAND OWNER") and gm["D8"]["New governance status"] == "OPEN — FORMALLY DEFERRED BY BRAND OWNER")
check("AC20 OPEN / FINAL BRAND OWNER RELEASE AUTHORIZATION PENDING", gm["AC20"]["New governance status"].startswith("OPEN / FINAL BRAND OWNER RELEASE AUTHORIZATION PENDING"))

texts = {p: p.read_text(encoding="utf-8") for p in PKG.rglob("*") if p.is_file() and p.suffix in (".md", ".csv", ".json", ".py")}
decl = (PKG / "04_FD01_Legal_IP_Offline_Evidence_Declaration.md").read_text(encoding="utf-8")
check("owner declaration wording present and 'does not mean Claude inspected'",
      "Their absence from the repository shall not be interpreted as evidence that such documentation does not exist" in decl and "does not say that Claude" in decl)
bad_up = []
req = re.compile(r"please (upload|send|provide)|send (me )?(the )?(scans|documents)|upload (the|your) (documents|scans)|provide (the )?scans", re.I)
for p, t in texts.items():
    if p.suffix == ".py":
        continue
    for n, line in enumerate(t.splitlines(), 1):
        if req.search(line):
            bad_up.append("%s:%d" % (p.name, n))
check("no request for confidential documents anywhere in the package", not bad_up, ", ".join(bad_up))
claims = re.compile(r"Legal/IP cleared|TRADEMARK VERIFIED|OWNERSHIP INDEPENDENTLY VERIFIED|NO EVIDENCE EXISTS|FULL CROSS-PLATFORM ACCESSIBILITY VERIFIED|WCAG 2\.2 AA (CERTIFIED|compliant|fully)|APPROVED V3\.0|FINAL RELEASE(?! AUTHORI[ZS])|PRODUCTION RELEASE|\bRELEASED\b|AC20 (is )?closed", re.I)
neg = re.compile(r"\bnot\b|\bno\b|\bnever\b|n't|does not|do not|nothing|without|unless|prohibit|pending|NOT YET|neither|none", re.I)
bad = []
for p, t in texts.items():
    if p.suffix == ".py" or p.parent.name == "14_qa":
        continue
    for n, line in enumerate(t.splitlines(), 1):
        if claims.search(line) and not neg.search(line):
            bad.append("%s:%d" % (p.name, n))
check("overclaim phrases appear only in negated/prohibiting context", not bad, ", ".join(bad))
check("no scan, image or PDF files in the package", not [str(p) for p in PKG.rglob("*") if p.is_file() and p.suffix.lower() in (".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".heic", ".docx", ".pptx", ".xlsx")])
path_pat = re.compile("/Us" + "ers/|/pri" + "vate/|/ho" + "me/|media" + "center1|claude-" + "501|\\.claude/work" + "trees|file:" + "///")
secret = re.compile("gh[opsu]_[A-Za-z0-9]{20,}|github" + "_pat_|-----" + "BEGIN|AKIA[0-9A-Z]{16}|xox[baprs]-")
check("no absolute paths and no credential patterns", not [str(p) for p, t in texts.items() if path_pat.search(t) or secret.search(t)])
arabic = re.compile("[" + chr(0x600) + "-" + chr(0x6ff) + "]")
check("no Arabic-script text", not [str(p) for p, t in texts.items() if arabic.search(t)])

check("original Approval Register unchanged", sha(REGISTER) == REGISTER_SHA)
changed = {c for c in git("diff", "--name-only", "HEAD").split("\n") if c}
check("only README.md changed among tracked files", changed <= {"README.md"}, sorted(changed))
untracked = [u for u in git("-c", "core.quotepath=off", "ls-files", "--others", "--exclude-standard").split("\n") if u]
check("only the FD01 package is new", all(u.startswith(str(PKG) + "/") for u in untracked), [u for u in untracked if not u.startswith(str(PKG) + "/")])
for pkg in ("GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation", "GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation", "GEM_V3.0_RC2_OD01_Owner_Decision_Formalization",
            "GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure", "GEM_V3.0_RC2_D7_Repository_Visibility_Decision_Package"):
    bad_sum = []
    for line in (Path(pkg) / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        f = Path(pkg) / name
        if f.is_file() and sha(f) != digest:
            bad_sum.append(name)
    check("%s unchanged (checksums verify)" % pkg.split("_")[2], not bad_sum, bad_sum[:3])
check("HR01 / AR01 / AX01 / OD01 packages have no git changes", not [c for c in changed if c.startswith("GEM_V3.0_RC2_")])
tracked = set(git("ls-files").split("\n"))
check("local-only files not tracked", not [t for t in tracked if t.startswith(".claude/") or t == "CLAUDE.local.md" or "/local_only/" in t])
fails = [r for r in results if r["result"] == "FAIL"]
(PKG / "14_qa" / "fd01_qa_results.json").write_text(json.dumps({"checks": results, "failures": len(fails)}, indent=1) + "\n", encoding="utf-8")
md = ["# FD01 QA results", "", "GEM™ V3.0 RC2 — OWNER ACCEPTED WITH FORMAL DEFERRALS · NOT YET FINAL-RELEASE AUTHORIZED", "",
      "Generated by `13_scripts/fd01_qa.py`. %d checks, %d failures." % (len(results), len(fails)), "", "| # | Check | Result | Detail |", "|---|---|---|---|"]
for i, r in enumerate(results, 1):
    md.append("| %d | %s | %s | %s |" % (i, r["check"], r["result"], r["detail"].replace("|", "/")[:150]))
(PKG / "14_qa" / "fd01_qa_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("%d checks, %d failures" % (len(results), len(fails)))
for r in fails:
    print("FAIL:", r["check"], r["detail"])
