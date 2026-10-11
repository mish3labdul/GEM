#!/usr/bin/env python3
"""HR01 Queue 1 and Queue 2 registers (03 Arabic, 05 Accessibility content).

Run from the repository root:
  python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_build_registers.py <decisions.json>

<decisions.json> is the local-only record of the reviewer's session dispositions. The committed registers hold item IDs, dispositions,
English approved titles/alt text and SHA-256 prefixes of Arabic strings; they never hold Arabic text.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

DEC = json.load(open(sys.argv[1], encoding="utf-8"))
PKG = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure")
OD = Path("GEM_V3.0_RC2_OD01_Owner_Decision_Formalization")
ROLE = "Mashal (Native Arabic Reviewer / Localization Lead, OD-G09); disposition stated in session"
ROLE2 = "Mashal (Accessibility Content Owner, OD-G10); disposition stated in session"
h12 = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()[:12]
AR = DEC["arabic"]


def expand(spec):
    return [int(x.split("-")[1]) for x in spec.split(",")]


disp = {}
for i in (1, 2, 4, 5, 6, 8, 9, 10, 12, 23, 38):
    disp[i] = ("APPROVE AS IS", None)
for i in expand("AR-03"):
    disp[i] = ("APPROVE CLAUDE RECOMMENDATION", AR["AR-03"]["new"])
for key in ("AR-07,AR-11", "AR-16,AR-32", "AR-17,AR-33", "AR-19,AR-25", "AR-20,AR-26,AR-35,AR-40"):
    for i in expand(key):
        disp[i] = ("APPROVE CLAUDE RECOMMENDATION", AR[key]["new"])
for tag in AR["letter_set_as_is"]:
    disp[int(tag.split("-")[1])] = ("APPROVE AS IS", None)
disp[43] = ("APPROVE AS IS", None)
disp[44] = ("APPROVE AS IS", None)
NOTES = {43: "Tagline stays English only (rule: Part B slide 3 / Part C slide 17, brand approval M10 not requested). Linguistic disposition only; not a brand approval.",
         44: "Policy: Western digits (0-9) for guest-facing Arabic copy, dates and page labels. No wording change. Technical IDs stay Latin (OD-G07)."}

queue = list(csv.DictReader(open(OD / "OD01_Mashal_Arabic_Review_Queue.csv", encoding="utf-8")))
key_slide = [k for k in queue[0] if k.startswith("Slide/page")][0]
old_sha = {}
rows = []
for r in queue:
    n = int(r["Item ID"].split("-")[2])
    d, new = disp[n]
    m = re.search(r"SHA ([0-9a-f]{12})", r[key_slide])
    before = m.group(1) if m else ""
    rows.append([r["Item ID"], r["Document"], r[key_slide].split(" · SHA")[0], r["Category"], r["Priority"], r["Existing technical result"][:90],
                 d, NOTES.get(n, ""), "yes" if new else "no", before, h12(new) if new else "", ROLE, "DISPOSITIONED"])
extras = [
    ["HR01-X01", "Letterhead Arabic/Bilingual (4 templates, 6 footer parts)", "footer page label", "Functional label (OD-G06)", "High", "English 'Page n of N' in Arabic and bilingual footers",
     "APPROVE CLAUDE RECOMMENDATION", "Localized page label with live PAGE/NUMPAGES fields; separator spaces kept in a left-to-right run after the first native check showed a spacing defect.", "yes", "", "", ROLE, "DISPOSITIONED"],
    ["HR01-X02", "Letterhead Arabic/Bilingual (4 templates)", "working markers", "Functional label (OD-G06)", "Medium", "English release-state markers", "APPROVE AS IS",
     "Working markers stay English; removed at release.", "no", "", "", ROLE, "DISPOSITIONED"],
    ["HR01-X03", "Letterhead Arabic/Bilingual (4 templates)", "footer contact initials", "Functional label (OD-G06)", "Low", "Latin placeholder initials", "APPROVE AS IS",
     "Placeholders stay as they are.", "no", "", "", ROLE, "DISPOSITIONED"],
    ["HR01-X04", "Part D images (7 Arabic strings inside raster images)", "slides 1-20", "Wording inside concept imagery", "Medium", "Images are AI-generated concept imagery; not editable here", "APPROVE AS IS",
     "Recorded as concept only; wording NOT approved (slides already state PENDING LOCALIZATION APPROVAL). No production approval.", "no", "", "", ROLE, "DISPOSITIONED (concept only; wording not approved)"],
]
with open(PKG / "03_HR01_Arabic_Review_Register.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["Item ID", "Document", "Slide/page reference", "Category", "Priority", "Existing technical result (AR01)", "Reviewer disposition", "Note",
                "Wording changed in HR01 candidate?", "Text SHA-256 prefix before", "Text SHA-256 prefix after", "Reviewer", "Status"])
    w.writerows(rows + extras)
cnt = {}
for r in rows:
    cnt[r[6]] = cnt.get(r[6], 0) + 1
print("arabic queue rows", len(rows), cnt, "extras", len(extras))

# ----------------------------------------------------------------------- accessibility content register
acc = list(csv.DictReader(open(OD / "OD01_Mashal_Accessibility_Content_Queue.csv", encoding="utf-8")))
TT = DEC["titles"]
spec = {("Part B", "8"): DEC["shapes"]["B8_first"], ("Part B", "14"): DEC["shapes"]["B14_first"]}
# alt text of Part D pictures: identical to the builder constants (single source of truth is hr01_build_candidates.py)
sys.path.insert(0, str(PKG / "16_scripts"))
import importlib.util
sp = importlib.util.spec_from_file_location("bc", str(PKG / "16_scripts" / "hr01_build_candidates.py"))
sys.argv = [sys.argv[0], sys.argv[1], str(PKG / "local_only" / "_tmp"), str(PKG / "local_only" / "_tmp.json")]
bc = importlib.util.module_from_spec(sp)
sp.loader.exec_module(bc)
D_ALT, D_EXTRA = bc.D_ALT, bc.D_ALT_EXTRA
out = []
first_b8 = first_b14 = False
alt_reg = list(csv.DictReader(open("GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation/07_AX01_Alt_Text_Register.csv", encoding="utf-8")))
pic_rows = [r for r in alt_reg if r["Applied in AX01 candidate?"] == "no" and r["Classification"] == "INFORMATIVE"]
pic_map = {("A%02d" % (i + 1)): r for i, r in enumerate(pic_rows)}
for r in acc:
    iid = r["Item ID"]
    doc, slide = r["Document"], r["Slide"]
    cat, cls = r["Object/category"], r["Current technical classification"][:80]
    kind = iid.split("-")[2][0]
    if kind == "T":
        key = ("A" if doc == "Part A" else "C") + slide
        out.append([iid, doc, slide, "Slide title", "TITLE REQUIRED — approved", "n/a", TT[key], "off-slide title placeholder (OD-G02)", "APPROVED AS PROPOSED", "yes", ROLE2, "DISPOSITIONED"])
    elif kind == "A":
        sid = re.search(r"shape id (\d+)", cat).group(1)
        a = D_ALT[(int(slide), sid)]
        out.append([iid, doc, slide, cat, "INFORMATIVE — ALT TEXT REQUIRED", "n/a", a, "alt text (concept image; Arabic label text not transcribed)", "APPROVED AS PROPOSED", "yes", ROLE2, "DISPOSITIONED"])
    elif kind == "S":
        sid = re.search(r"id (\d+)", cat).group(1)
        key = (doc, slide)
        if key in spec and ((doc, slide) == ("Part B", "8") and sid == "5" or (doc, slide) == ("Part B", "14") and sid == "6"):
            out.append([iid, doc, slide, cat, "INFORMATIVE (specimen set, first shape carries the description)", "n/a", spec[key], "alt text", "APPROVED (one description per set)", "yes", ROLE2, "DISPOSITIONED"])
        else:
            if key in (("Part B", "8"), ("Part B", "14")):
                c = "DECORATIVE (part of the described specimen set)"
            else:
                c = "DECORATIVE / REDUNDANT"
            out.append([iid, doc, slide, cat, c, "marked decorative", "", "decorative flag (OD-G03)", "APPROVED (group decision)", "yes", ROLE2, "DISPOSITIONED"])
    elif iid == "OD01-AC-G01":
        out.append([iid, "Part D", "1, 2, 5, 6, 12, 24", "6 logo pictures with generic alt text", "INFORMATIVE — ALT TEXT REPLACED", "n/a", "GEM logo", "alt text (replaces 'Supplied GEM raster artwork. PENDING PRODUCTION MASTER.')", "APPROVED AS PROPOSED", "yes", ROLE2, "DISPOSITIONED"])
    elif iid == "OD01-AC-C01":
        out.append([iid, "Part A", "33", "Beige on White run (2.2:1)", "PALETTE SPECIMEN (OD-G05)", "n/a", "", "owner-confirmed specimen; no change; contrast finding stays recorded as a documented exception", "CONFIRMED SPECIMEN", "no", ROLE2, "DISPOSITIONED"])
for iid, ref in (("HR01-AC-X01", (16, "17")), ("HR01-AC-X02", (17, "17"))):
    out.append([iid, "Part D", str(ref[0]), "materials picture with generic 'AI-generated ... concept' alt text", "INFORMATIVE — ALT TEXT REPLACED", "n/a", D_EXTRA[ref], "alt text", "APPROVED AS PROPOSED", "yes", ROLE2, "DISPOSITIONED"])
with open(PKG / "05_HR01_Accessibility_Content_Register.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["Item ID", "Document", "Slide", "Object / category", "Owner classification", "Decorative flag", "Approved title / alt-text reference", "Method / note", "Owner disposition", "Applied in HR01 candidate?", "Owner", "Status"])
    w.writerows(out)
kinds = {}
for o in out:
    kinds[o[0].split("-")[2][0] if o[0].startswith("OD01") else "X"] = kinds.get(o[0].split("-")[2][0] if o[0].startswith("OD01") else "X", 0) + 1
print("accessibility rows", len(out), kinds)
import shutil
shutil.rmtree(PKG / "local_only" / "_tmp", ignore_errors=True)
Path(PKG / "local_only" / "_tmp.json").unlink(missing_ok=True)
