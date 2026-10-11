#!/usr/bin/env python3
"""RP01 build. Run from the repository root:
  python3 -I GEM_V3.0_RP01_Release_Artifact_Promotion/15_scripts/rp01_build.py
Promotes ONLY files whose current sha256 equals the FA01-authorized sha256 (FA01 MANIFEST baseline_files_outside_package).
Writes promoted artifacts under 17_release_artifacts/, the baseline/promotion/label/lineage registers and 16_qa/rp01_build_result.json.
Never touches any source file."""
import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rp01_engine as E  # noqa: E402
import rp01_rules as R  # noqa: E402

RP = Path("GEM_V3.0_RP01_Release_Artifact_Promotion")
FA = Path("GEM_V3.0_FA01_Final_Release_Authorization")
HR = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/18_candidate_corrections")
LH = Path("GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates")
TOK = Path("PartB_RC2/05_release/tokens")
OUT = RP / "17_release_artifacts"
DATE = "20261009"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

EM = "—"
base = {Path(e["path"]).name: e for e in json.load(open(FA / "MANIFEST.json", encoding="utf-8"))["baseline_files_outside_package"]}


def src_pptx(tag):
    return next(Path(p) for p in HR.glob("*Part %s*.pptx" % tag))


def X12(asset, variant, ext):
    return "GEM_BRAND_%s_%s_v3.0_%s.%s" % (asset, variant, DATE, ext)


ARTS = []  # dicts


def add(aid, name, src, folder, target, kind, cat, rules, restriction, extra_preserve=()):
    ARTS.append(dict(id=aid, name=name, src=Path(src), folder=folder, target=target, kind=kind, cat=cat, rules=rules, restriction=restriction, extra_preserve=extra_preserve))


add("P-A", "Part A Brand Guidelines", src_pptx("A"), "01_brand_guidelines", X12("BrandGuidelines", "PartA", "pptx"), "pptx", "A AUTHORIZED RELEASE ARTIFACT", R.PART_A,
    "External issue as the full PPTX allowed after this promotion; no PDF or DOCX extract of slides 37, 38, 39, 65, 66, 68 (Arabic, D8)")
add("P-B", "Part B Digital Design System", src_pptx("B"), "02_digital_design_system", X12("DigitalDesignSystem", "PartB", "pptx"), "pptx", "A AUTHORIZED RELEASE ARTIFACT", R.PART_B,
    "External issue as the full PPTX allowed; no PDF or DOCX extract of slide 9 (Arabic, D8); specification only, no component implementation")
add("P-C", "Part C Production Standards", src_pptx("C"), "03_production_standards", X12("ProductionStandards", "PartC", "pptx"), "pptx", "A AUTHORIZED RELEASE ARTIFACT", R.PART_C,
    "External issue as the full PPTX allowed; production-standard edition state stays WORKING EDITION / PENDING PRODUCTION VALIDATION; no supplier acceptance")
add("P-D", "Part D Amenities & Packaging Concept Portfolio", src_pptx("D"), "04_amenities_concept", X12("AmenitiesPackagingConcept", "PartD", "pptx"), "pptx", "C CONCEPT / NOT PRODUCTION ARTWORK", R.PART_D,
    "CONCEPT / NOT PRODUCTION ARTWORK; images with baked-in Arabic are not for external DOCX/PDF extract (D8); not supplier-ready, no dieline, no regulatory approval")
for key, var in (("English_First_Page", "EnglishFirstPage"), ("English_Continuation", "EnglishContinuation"), ("Executive", "Executive"), ("Minimal", "Minimal")):
    add("L-" + key, "Letterhead " + key.replace("_", " "), LH / ("GEM_Letterhead_%s.docx" % key), "05_letterheads", X12("Letterhead", var, "docx"), "docx", "A AUTHORIZED RELEASE ARTIFACT",
        R.english_rules(2 if key in ("English_First_Page", "Executive", "Minimal") else 1), "Not affected by D8; second-signatory, fields, logo and layout unchanged")
for key, var, nf in (("Arabic_First_Page", "ArabicFirstPageInternal", 2), ("Arabic_Continuation", "ArabicContinuationInternal", 1), ("Bilingual_First_Page", "BilingualFirstPageInternal", 2), ("Bilingual_Continuation", "BilingualContinuationInternal", 1)):
    add("L-" + key, "Letterhead " + key.replace("_", " "), HR / ("GEM_Letterhead_%s_HR01_CANDIDATE.docx" % key), "05_letterheads/restricted_internal_only", X12("Letterhead", var, "docx"), "docx",
        "B AUTHORIZED INTERNAL / RESTRICTED ARTIFACT", R.restricted_rules(nf), "CONTROLLED INTERNAL USE ONLY; external issue as DOCX or PDF restricted pending D8 validation; D8 markings kept on every page",
        extra_preserve=[(r"WORKING APPLICATION / PENDING VALIDATION", "D", "D8 internal-use marking kept verbatim"), (r"CONTROLLED INTERNAL TEMPLATE", "D", "restriction line added in this promotion"),
                        (r"EXTERNAL ISSUE RESTRICTED", "D", "restriction wording")])

STALE = re.compile(r"RC2|RC1|RELEASE CANDIDATE|WORKING (EDITION|SPECIFICATION|APPLICATION)|NOT RELEASED|UNAPPROVED|CANDIDATE|AC20\s*(PENDING|/\s*OPEN)|release not yet authorized|pending \(AC20\)|\[REQUIRES OWNER\] \(AC20\)|HR01|3\.0\.0-rc|rc\.2|\bv1\.0\b", re.I)


def paragraphs(zf):
    for n in sorted(zf.namelist()):
        if not n.endswith(".xml") or not re.match(r"(ppt/(slides|slideLayouts|slideMasters|notesSlides|notesMasters)/|word/(document|header\d*|footer\d*)\.xml|docProps/core\.xml)", n):
            continue
        x = zf.read(n).decode("utf-8")
        if n.startswith("docProps"):
            for t in re.findall(r"<(?:dc:title|dc:subject)[^>]*>([^<]*)<", x):
                yield n, t
            continue
        for para in re.findall(r"<(?:a:p|w:p)[ >].*?</(?:a:p|w:p)>", x, re.S):
            t = "".join(re.findall(r"<(?:a:t|w:t)[^>]*>([^<]*)</(?:a:t|w:t)>", para))
            if t:
                yield n, t
        for attr in re.findall(r'<p:cNvPr [^>]*?(?:name|descr)="([^"]*)"', x):
            yield n + "#attr", attr


def residual(path, extra):
    out, bad = [], []
    pres = list(extra) + list(R.PRESERVE)
    with zipfile.ZipFile(path) as z:
        for member, t in paragraphs(z):
            t = t.replace("&amp;", "&")
            if not STALE.search(t):
                continue
            hit = next(((c, why) for rx, c, why in pres if re.search(rx, t)), None)
            if hit:
                out.append((member, t[:160], hit[0], hit[1] + " [stale term: %s]" % STALE.search(t).group(0)))
            else:
                bad.append((member, t[:200]))
    return out, bad


def main():
    for d in ("01_brand_guidelines", "02_digital_design_system", "03_production_standards", "04_amenities_concept", "05_letterheads/restricted_internal_only", "06_brand_assets", "07_tokens", "08_release_index"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    (RP / "16_qa").mkdir(exist_ok=True)
    result, label_rows, lineage_rows, promo_rows, base_rows = {"artifacts": []}, [], [], [], []
    stop = False
    for a in ARTS:
        e = base.get(a["src"].name)
        fa_hash = e["sha256"] if e else "NOT IN FA01 BASELINE"
        cur = sha(a["src"]) if a["src"].exists() else "MISSING"
        match = e is not None and cur == fa_hash
        base_rows.append([a["id"], a["name"], a["src"].as_posix(), fa_hash, cur, "YES" if match else "NO", a["cat"], "PROMOTE" if match else "STOP", a["restriction"],
                          "%s/%s" % (a["folder"], a["target"])])
        if not match:
            print("STOP artifact (hash mismatch):", a["id"])
            stop = True
            continue
        dst = OUT / a["folder"] / a["target"]
        log, report = E.apply_rules(a["src"], dst, a["rules"])
        # independent verification of the written file
        zs, zd = zipfile.ZipFile(a["src"]), zipfile.ZipFile(dst)
        assert [i.filename for i in zs.infolist()] == [i.filename for i in zd.infolist()], "member list/order changed"
        changed_members = [n for n in zs.namelist() if zs.read(n) != zd.read(n)]
        allowed = [n for n in zs.namelist() if any(re.fullmatch(r[0], n) for r in a["rules"])]
        unexpected = [n for n in changed_members if n not in allowed]
        assert not unexpected, unexpected
        assert zd.testzip() is None
        pres, bad = residual(dst, a["extra_preserve"])
        if bad:
            print("UNCLASSIFIED RESIDUAL LABELS in", a["id"])
            for b in bad:
                print("   ", b)
            stop = True
        merged = {}
        for ri, member, old, new, n in log:
            merged.setdefault(ri, []).append((member, n))
        for ri, rule in enumerate(a["rules"]):
            mem = merged.get(ri, [])
            label_rows.append([a["id"], a["target"], "A STALE RELEASE-STATE LABEL - UPDATED", ",".join(sorted({m.split("/")[-1] for m, _ in mem}))[:120], sum(n for _, n in mem), rule[1][:160], rule[2][:200], rule[6]])
        for member, text, cls, why in pres:
            label_rows.append([a["id"], a["target"], {"B": "B STILL-VALID QUALIFIER - PRESERVED", "C": "C HISTORICAL / EXPLANATORY - PRESERVED", "D": "D RESTRICTED-ARTIFACT WARNING - PRESERVED"}[cls],
                               member.split("/")[-1], 1, text, text, why])
        lineage_rows.append([a["id"], a["src"].as_posix(), fa_hash, (a["folder"] + "/" + a["target"]), sha(dst), "release-state labels, version labels, document IDs, release date, FA01-superseded status text, metadata",
                             "; ".join(m.split("/")[-1] for m in changed_members)[:300], "members total %d / changed %d / byte-identical %d" % (len(zs.namelist()), len(changed_members), len(zs.namelist()) - len(changed_members)),
                             "NO" if not unexpected else "YES", "PASS"])
        promo_rows.append([a["id"], a["name"], a["cat"], a["src"].name, dst.relative_to(RP).as_posix(), sha(dst), "PROMOTED", a["restriction"]])
        result["artifacts"].append(dict(id=a["id"], changed_members=len(changed_members), identical=len(zs.namelist()) - len(changed_members), residual_preserved=len(pres)))
        print("%-26s changed members %3d  identical %4d  preserved residual %3d" % (a["id"], len(changed_members), len(zs.namelist()) - len(changed_members), len(pres)))

    # tokens (meta-only edit with deep-diff proof) and README
    t_json, t_css = TOK / "gem-tokens.v3.0-rc2.json", TOK / "gem-tokens.v3.0-rc2.css"
    for f in (t_json, t_css):
        if sha(f) != base[f.name]["sha256"]:
            print("STOP token hash mismatch", f)
            stop = True
    if not stop:
        raw = t_json.read_text(encoding="utf-8")
        ed = [('"version": "3.0.0-rc.2"', '"version": "3.0.0"'), ('"edition": "V3.0 RC2"', '"edition": "V3.0"'), ('"documentId": "GEM-DDS-V3.0-RC2"', '"documentId": "GEM-DDS-V3.0"'),
              ('"issued": "2026-10-06"', '"issued": "2026-10-09"'),
              ('"status": "WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING)"', '"status": "OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE · TOKEN VALUES UNCHANGED FROM RC2 · COMPONENT IMPLEMENTATION NOT AUTHORIZED (VAL-13, VAL-20 DEFERRED)"')]
        new = raw
        for o, n in ed:
            assert new.count(o) == 1, o
            new = new.replace(o, n)
        a_, b_ = json.loads(raw), json.loads(new)
        meta_a, meta_b = a_.pop("meta"), b_.pop("meta")
        assert a_ == b_, "non-meta token content changed"
        diff = {k: (meta_a[k], meta_b[k]) for k in meta_a if meta_a[k] != meta_b[k]}
        (OUT / "07_tokens" / "gem-tokens.v3.0.json").write_text(new, encoding="utf-8")
        css = t_css.read_text(encoding="utf-8")
        lines = css.split("\n")
        assert lines[0].startswith("/* GEM Digital Design System tokens") and "NOT RELEASED" in lines[1]
        lines[0] = "/* GEM Digital Design System tokens · 3.0.0 · V3.0 · GEM-DDS-V3.0 · 2026-10-09"
        lines[1] = "   Derived from the approved specification; status per token in the JSON. OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE · TOKEN VALUES UNCHANGED FROM RC2 · COMPONENT IMPLEMENTATION NOT AUTHORIZED. */"
        (OUT / "07_tokens" / "gem-tokens.v3.0.css").write_text("\n".join(lines), encoding="utf-8")
        assert "\n".join(css.split("\n")[2:]) == "\n".join(lines[2:])
        rd = (TOK / "README.md").read_text(encoding="utf-8")
        for o, n in (("# GEM tokens · 3.0.0-rc.2 (V3.0 RC2)", "# GEM tokens · 3.0.0 (V3.0)"),
                     ("WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING). **Document:** GEM-DDS-V3.0-RC2 · 2026-10-06.", "OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE · TOKEN VALUES UNCHANGED FROM RC2 · COMPONENT IMPLEMENTATION NOT AUTHORIZED. **Document:** GEM-DDS-V3.0 · 2026-10-09."),
                     ("`gem-tokens.v3.0-rc2.json`", "`gem-tokens.v3.0.json`"), ("`gem-tokens.v3.0-rc2.css`", "`gem-tokens.v3.0.css`"),
                     ("Checksums in `../../06_logs/release_sha256.txt`.", "Checksums: see the RP01 package SHA256SUMS.txt.")):
            assert rd.count(o) == 1, o
            rd = rd.replace(o, n)
        (OUT / "07_tokens" / "README.md").write_text(rd, encoding="utf-8")
        for nm, srcp, dstn in (("T-JSON", t_json, "gem-tokens.v3.0.json"), ("T-CSS", t_css, "gem-tokens.v3.0.css")):
            fa_hash = base[srcp.name]["sha256"]
            base_rows.append([nm, "Token package " + dstn, srcp.as_posix(), fa_hash, sha(srcp), "YES", "A AUTHORIZED RELEASE ARTIFACT", "PROMOTE", "Meta/header labels only; no token value changed", "07_tokens/" + dstn])
            lineage_rows.append([nm, srcp.as_posix(), fa_hash, "07_tokens/" + dstn, sha(OUT / "07_tokens" / dstn), "JSON meta fields version/edition/documentId/issued/status; CSS header comment",
                                 "meta only" if nm == "T-JSON" else "header comment only", "non-meta JSON deep-equal: %s" % ("TRUE" if nm == "T-JSON" else "n/a; CSS body lines 3..end identical"), "NO", "PASS"])
            promo_rows.append([nm, "Token package " + dstn, "A AUTHORIZED RELEASE ARTIFACT", srcp.name, "17_release_artifacts/07_tokens/" + dstn, sha(OUT / "07_tokens" / dstn), "PROMOTED", "Token values unchanged; no component implementation authorized"])
            label_rows.append([nm, dstn, "A STALE RELEASE-STATE LABEL - UPDATED", dstn, 1, "version/edition/documentId/status RC2 labels", "V3.0 labels", "token meta/header; values unchanged (deep-diff proof: %s)" % "; ".join(sorted(diff))])
        label_rows.append(["T-JSON", "gem-tokens.v3.0.json", "C HISTORICAL / EXPLANATORY - PRESERVED", "meta.derivedFrom / meta.note", 1, "Part B — RC2 (deck)", "unchanged", "provenance text naming the source edition"])
        shutil.copyfile(TOK / "README.md", "/dev/null") if False else None
        result["token_meta_diff"] = diff

    # logo kit: carried in place (referenced, not copied)
    kit = Path("GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt")
    kfa = base["SHA256SUMS.txt"]["sha256"]
    base_rows.append(["K-KIT", "Logo kit GEM_Brand_Assets_v1.0 (04_official_kit checksum list)", kit.as_posix(), kfa, sha(kit), "YES" if sha(kit) == kfa else "NO", "D WORKING ASSET / PRODUCTION-MASTER ACCEPTANCE PENDING",
                      "CARRY IN PLACE (reference, not copied)", "WORKING ASSETS; acceptance as production master PENDING (VAL-02 deferred); production vectors not accepted masters", "06_brand_assets/README.md (pointer)"])
    promo_rows.append(["K-KIT", "Logo kit", "D WORKING ASSET / PRODUCTION-MASTER ACCEPTANCE PENDING", kit.as_posix(), "GEM_Brand_Assets_v1.0/ (in place)", kfa, "REFERENCED IN PLACE", "WORKING ASSETS; not a production master"])
    lineage_rows.append(["K-KIT", kit.as_posix(), kfa, "GEM_Brand_Assets_v1.0/ (in place)", sha(kit), "none (not modified or copied)", "none", "byte-identical by non-modification", "NO", "PASS"])

    def w(name, header, rows):
        with open(RP / name, "w", encoding="utf-8", newline="") as fh:
            c = csv.writer(fh, lineterminator="\n")
            c.writerow(header)
            c.writerows(rows)
    w("02_RP01_Authorized_Baseline.csv", ["Artifact ID", "Artifact name", "Source path", "FA01 SHA256", "Current SHA256", "Hash match?", "FA01 release classification (RP01 category)", "RP01 action", "Restriction", "Target artifact path"], base_rows)
    w("03_RP01_Artifact_Promotion_Register.csv", ["Artifact ID", "Artifact", "Category", "Source file", "Promoted path (in RP01)", "Promoted SHA256", "Result", "Restriction"], promo_rows)
    w("04_RP01_Status_Label_Change_Register.csv", ["Artifact ID", "Promoted file", "Classification", "Location(s)", "Occurrences", "Old text", "New text", "Reason"], label_rows)
    w("08_RP01_Lineage_Proof.csv", ["Artifact ID", "Source path", "FA01 SHA256", "Promoted path", "Promoted SHA256", "Permitted changes", "Actual changed members", "Member accounting", "Unexpected changes?", "Result"], lineage_rows)
    result["stop"] = stop
    (RP / "16_qa" / "rp01_build_result.json").write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("baseline rows", len(base_rows), "label rows", len(label_rows), "STOP" if stop else "OK")
    return 1 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
