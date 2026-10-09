#!/usr/bin/env python3
"""HR01 static accessibility predicates (corroborates the native checker).

Run from the repository root:  python3 -B GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_static_accessibility_check.py
Imports the AX01 walker read-only (AX01 scripts are not edited; -B avoids writing bytecode there). Predicates, as calibrated by AX01 against the native
counts (AX01 31/30/26/25): slides without a title placeholder holding text; non-text shapes and pictures (not placeholders) with neither alt text nor a
decorative flag. Tables are reported separately because PowerPoint's missing-alt-text rule does not count them. Writes 17_qa/hr01_static_accessibility_check.csv.
"""
import csv
import glob
import sys
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, "GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation/19_scripts")
from ax01_common import etree, ns, slide_order, walk  # noqa: E402

PKG = "GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure"


def preds(path):
    z = zipfile.ZipFile(path)
    slides = notitle = shapes_pics = tables = deco = alt = 0
    for part in slide_order(z):
        slides += 1
        objs = list(walk(etree.fromstring(z.read(part)).find(".//p:spTree", ns)))
        notitle += 0 if any(o["placeholder"] in ("title", "ctrTitle") and o["has_text"] for o in objs) else 1
        shapes_pics += sum(1 for o in objs if o["kind"] in ("pic", "sp", "cxnSp", "grpSp") and not o["has_text"] and not o["descr"].strip() and not o["decorative"] and o["placeholder"] is None)
        tables += sum(1 for o in objs if o["kind"] == "table" and not o["descr"].strip() and not o["decorative"])
        deco += sum(1 for o in objs if o["decorative"])
        alt += sum(1 for o in objs if o["descr"].strip())
    return slides, notitle, shapes_pics, tables, deco, alt


rows = [["Document", "Slides", "Slides without title (AX01)", "Slides without title (HR01)", "Shapes+pictures without alt/decorative (AX01)",
         "Shapes+pictures without alt/decorative (HR01)", "Tables without alt text (HR01; not counted by the native rule)", "Decorative flags (AX01 -> HR01)", "Objects with alt text (AX01 -> HR01)"]]
for k in "ABCD":
    a = preds(glob.glob("GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation/21_candidate_corrections/*Part %s*.pptx" % k)[0])
    h = preds(glob.glob(PKG + "/18_candidate_corrections/*Part %s*.pptx" % k)[0])
    rows.append(["Part " + k, h[0], a[1], h[1], a[2], h[2], h[3], "%d -> %d" % (a[4], h[4]), "%d -> %d" % (a[5], h[5])])
with open(PKG + "/17_qa/hr01_static_accessibility_check.csv", "w", encoding="utf-8", newline="") as fh:
    csv.writer(fh, lineterminator="\n").writerows(rows)
for r in rows[1:]:
    print(r)
