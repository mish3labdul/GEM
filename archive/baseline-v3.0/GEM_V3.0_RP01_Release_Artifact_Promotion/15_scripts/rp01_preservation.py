#!/usr/bin/env python3
"""RP01 preservation proof (accessibility, Arabic/RTL, structure, geometry, Word fields). Read-only.
Run from the repository root with a Python that has lxml (the docling venv):
  ~/venvs/docling/bin/python -B GEM_V3.0_RP01_Release_Artifact_Promotion/15_scripts/rp01_preservation.py
Method: for every PowerPoint part the promoted XML, with the text of every <a:t> element and every shape-name attribute blanked, must be byte-identical to the
FA01-baseline source (this proves slide structure, geometry, alt text, decorative flags, titles, RTL/lang attributes, table header-row flags, picture
references and reading order unchanged). The set of Arabic-bearing text runs must be identical. The AX01 static predicates are recomputed on both files.
For Word templates every part other than the footers and core.xml must be byte-identical; footers must equal the source after removing the inserted
restriction line (restricted templates) or after blanking the removed marker (English templates)."""
import csv
import re
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, "GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation/19_scripts")
from ax01_common import etree, ns, slide_order, walk  # noqa: E402

RP = Path("GEM_V3.0_RP01_Release_Artifact_Promotion")
AR = re.compile("[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
rows = []


def blank_text(x):
    x = re.sub(r"(<a:t(?: [^>]*)?>)[^<]*(</a:t>)", r"\1\2", x)
    return re.sub(r'(<p:cNvPr [^>]*?name=")[^"]*(")', r"\1\2", x)


def preds(z):
    slides = notitle = shapes = tables = deco = alt = 0
    for part in slide_order(z):
        slides += 1
        objs = list(walk(etree.fromstring(z.read(part)).find(".//p:spTree", ns)))
        notitle += 0 if any(o["placeholder"] in ("title", "ctrTitle") and o["has_text"] for o in objs) else 1
        shapes += sum(1 for o in objs if o["kind"] in ("pic", "sp", "cxnSp", "grpSp") and not o["has_text"] and not o["descr"].strip() and not o["decorative"] and o["placeholder"] is None)
        tables += sum(1 for o in objs if o["kind"] == "table" and not o["descr"].strip() and not o["decorative"])
        deco += sum(1 for o in objs if o["decorative"])
        alt += sum(1 for o in objs if o["descr"].strip())
    return slides, notitle, shapes, tables, deco, alt


def arabic_runs(z):
    out = []
    for n in sorted(z.namelist()):
        if n.endswith(".xml") and re.match(r"(ppt|word)/(slides|notesSlides|document|header|footer)", n):
            out += [(n, t) for t in re.findall(r"<(?:a:t|w:t)[^>]*>([^<]*)</(?:a:t|w:t)>", z.read(n).decode("utf-8")) if AR.search(t)]
    return out


def rec(art, check, ok, detail=""):
    rows.append([art, check, "PASS" if ok else "FAIL", detail])


reg = {r["Artifact ID"]: r for r in csv.DictReader(open(RP / "02_RP01_Authorized_Baseline.csv", encoding="utf-8"))}
prom = {r["Artifact ID"]: r for r in csv.DictReader(open(RP / "03_RP01_Artifact_Promotion_Register.csv", encoding="utf-8"))}
for aid, b in reg.items():
    if aid.startswith(("T-", "K-")):
        continue
    src, dst = Path(b["Source path"]), RP / prom[aid]["Promoted path (in RP01)"]
    zs, zd = zipfile.ZipFile(src), zipfile.ZipFile(dst)
    rec(aid, "member list and order identical", [i.filename for i in zs.infolist()] == [i.filename for i in zd.infolist()])
    rec(aid, "zip integrity", zd.testzip() is None)
    if src.suffix == ".pptx":
        bad = [n for n in zs.namelist() if n.endswith((".xml", ".rels")) and ((blank_text(zs.read(n).decode()) != blank_text(zd.read(n).decode())) if re.match(r"ppt/(slides|slideLayouts|slideMasters|notesSlides)/", n) else zs.read(n) != zd.read(n) and not n.startswith("docProps/"))]
        rec(aid, "all parts identical after blanking text/shape names (structure, geometry, alt text, decorative, titles, RTL, tables)", not bad, str(bad[:4]))
        binary = [n for n in zs.namelist() if not n.endswith((".xml", ".rels")) and zs.read(n) != zd.read(n)]
        rec(aid, "media / binary members byte-identical", not binary, str(binary[:3]))
        ps, pd = preds(zs), preds(zd)
        rec(aid, "AX01 static predicates unchanged (slides, no-title, shapes+pics w/o alt, tables w/o alt, decorative, alt)", ps == pd, "%s -> %s" % (ps, pd))
        rec(aid, "Arabic text runs identical (content and count)", sorted(arabic_runs(zs)) == sorted(arabic_runs(zd)), "%d runs" % len(arabic_runs(zs)))
        # Arabic-bearing slides keep their RTL / lang attributes: covered by structural identity above; assert counts explicitly
        rtl_s = sum(zs.read(n).decode().count('rtl="1"') for n in zs.namelist() if n.startswith("ppt/slides/") and n.endswith(".xml"))
        rtl_d = sum(zd.read(n).decode().count('rtl="1"') for n in zd.namelist() if n.startswith("ppt/slides/") and n.endswith(".xml"))
        lang_s = sum(zs.read(n).decode().count('lang="ar-SA"') for n in zs.namelist() if n.startswith("ppt/slides/") and n.endswith(".xml"))
        lang_d = sum(zd.read(n).decode().count('lang="ar-SA"') for n in zd.namelist() if n.startswith("ppt/slides/") and n.endswith(".xml"))
        rec(aid, 'rtl="1" and lang="ar-SA" attribute counts unchanged', rtl_s == rtl_d and lang_s == lang_d, "rtl %d->%d, ar-SA %d->%d" % (rtl_s, rtl_d, lang_s, lang_d))
        if aid == "P-A":
            rec(aid, "AR01 slide 39 mixed Arabic/Latin run structure preserved", blank_text(zs.read("ppt/slides/slide39.xml").decode()) == blank_text(zd.read("ppt/slides/slide39.xml").decode()))
        if aid == "P-B":
            rec(aid, "NP01-R1 slide 30 structure preserved", blank_text(zs.read("ppt/slides/slide30.xml").decode()) == blank_text(zd.read("ppt/slides/slide30.xml").decode()))
    else:
        changed_ok = []
        for n in zs.namelist():
            a, c = zs.read(n), zd.read(n)
            if a == c:
                continue
            if re.fullmatch(r"word/footer\d+\.xml", n):
                if aid.startswith(("L-English", "L-Executive", "L-Minimal")):
                    ok = re.sub(r"(<w:t[^>]*>)[^<]*(</w:t>)", r"\1\2", a.decode()) == re.sub(r"(<w:t[^>]*>)[^<]*(</w:t>)", r"\1\2", c.decode())
                else:
                    stripped = re.sub(r"<w:r><w:br/></w:r><w:r><w:rPr>(?:(?!</w:rPr>).)*?</w:rPr><w:t xml:space=\"preserve\">CONTROLLED INTERNAL TEMPLATE[^<]*</w:t></w:r>", "", c.decode(), flags=re.S)
                    ok = stripped == a.decode()
                changed_ok.append((n, ok))
            elif n == "docProps/core.xml":
                changed_ok.append((n, re.sub(r"<dc:subject>[^<]*</dc:subject>", "", a.decode()) == re.sub(r"<dc:subject>[^<]*</dc:subject>", "", c.decode())))
            else:
                changed_ok.append((n, False))
        rec(aid, "only footers and core.xml (subject) differ; everything else byte-identical (body, headers, logo media, styles, settings, numbering, fields)", all(ok for _, ok in changed_ok), str(changed_ok))
        fa = zs.read("word/footer1.xml").decode(); fd = zd.read("word/footer1.xml").decode()
        rec(aid, "PAGE / NUMPAGES field structure in footer unchanged", fa.count("fldChar") == fd.count("fldChar") and fa.count("instrText") == fd.count("instrText"), "fldChar %d->%d" % (fa.count("fldChar"), fd.count("fldChar")))
        if aid.startswith("L-Arabic") or aid.startswith("L-Bilingual"):
            ftxt = "".join(zd.read(n).decode() for n in zd.namelist() if re.fullmatch(r"word/footer\d+\.xml", n))
            rec(aid, "both D8 markings verbatim and restriction line present in every footer", all("WORKING APPLICATION / PENDING VALIDATION" in zd.read(n).decode() and "PENDING LOCALIZATION APPROVAL" in zd.read(n).decode() and "EXTERNAL ISSUE RESTRICTED PENDING D8 VALIDATION" in zd.read(n).decode() for n in zd.namelist() if re.fullmatch(r"word/footer\d+\.xml", n)), "")
            rec(aid, "Arabic body text identical", sorted(arabic_runs(zs)) == sorted(arabic_runs(zd)), "%d runs" % len(arabic_runs(zs)))

(RP / "16_qa").mkdir(exist_ok=True)
with open(RP / "16_qa" / "rp01_preservation.csv", "w", encoding="utf-8", newline="") as fh:
    c = csv.writer(fh, lineterminator="\n")
    c.writerow(["Artifact", "Check", "Result", "Detail"])
    c.writerows(rows)
fails = [r for r in rows if r[2] != "PASS"]
print("checks", len(rows), "failed", len(fails))
for r in fails:
    print("FAIL", r)
sys.exit(1 if fails else 0)
