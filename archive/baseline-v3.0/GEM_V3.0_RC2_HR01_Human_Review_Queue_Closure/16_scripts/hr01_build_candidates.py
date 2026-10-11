#!/usr/bin/env python3
"""HR01 candidate builder (zip-level, anchored edits; no other member is touched).

Run from the repository root:
  python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_build_candidates.py <decisions.json> <out_dir> <log_json>

<decisions.json> is a local-only file holding the reviewer-approved wording (Arabic text is kept out of committed registers).
Sources (read-only, latest controlled lineage proven by hash in 02/15):
  PowerPoint: AX01 candidates (AR01/D3/ODI01-R1 lineage + AX01 safe structural remediation)
  Word:       Revision 03 letterhead templates (byte-identical to the AX01 baseline)
Every edit is recorded as an (old fragment, new fragment) pair; the inverse proof re-applies them backwards and must reproduce the
source member byte-for-byte. Relative paths only.
"""
import csv
import hashlib
import html
import json
import re
import sys
import zipfile
from pathlib import Path

DEC = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = Path(sys.argv[2])
LOGP = sys.argv[3]
OUT.mkdir(parents=True, exist_ok=True)
AX = Path("GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation")
LH = Path("GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates")
EM = "—"
DECKS = {
    "A": (AX / "21_candidate_corrections" / ("GEM Brand Guidelines V3.0 %s Part A %s RC2 %s AX01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM)),
          "GEM Brand Guidelines V3.0 %s Part A %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM)),
    "B": (AX / "21_candidate_corrections" / ("GEM Digital Design System V3.0 %s Part B %s RC2 %s AX01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM)),
          "GEM Digital Design System V3.0 %s Part B %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM)),
    "C": (AX / "21_candidate_corrections" / ("GEM Production Standards V3.0 %s Part C %s RC2 %s AX01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM)),
          "GEM Production Standards V3.0 %s Part C %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM)),
    "D": (AX / "21_candidate_corrections" / ("GEM Amenities & Packaging %s Concept Product Portfolio V3.0 %s Part D %s RC2 %s AX01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM, EM)),
          "GEM Amenities & Packaging %s Concept Product Portfolio V3.0 %s Part D %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM, EM)),
}
PART = {"Part A": "A", "Part B": "B", "Part C": "C", "Part D": "D"}
sha = lambda b: hashlib.sha256(b).hexdigest()
esc = lambda s: html.escape(s, quote=True)
DECOR = ('<a:extLst><a:ext uri="{C183D7F6-B498-43B3-948B-1728B52AA6E4}"><adec:decorative xmlns:adec="http://schemas.microsoft.com/office/drawing/2017/decorative" val="1"/></a:ext></a:extLst>')
EXT = DECOR[len("<a:extLst>"):-len("</a:extLst>")]

# ---------------------------------------------------------------- approved English content
D_ALT = {  # Part D picture alt text, keyed (slide, shape id); approved by the Accessibility Content Owner in session
    (1, "17"): "Concept image: GEM shampoo bottle with a black pump and a dark label showing the GEM wordmark and the product name in English and Arabic.",
    (3, "23"): "Concept image: four GEM amenity bottles (shampoo, conditioner, body wash, body lotion) on a stone bathroom counter beside a folded towel, a plant and a soap dish.",
    (4, "39"): "Concept image: GEM shampoo bottle, dark label.", (5, "34"): "Concept image: GEM shampoo bottle, dark label.",
    (4, "44"): "Concept image: GEM conditioner bottle, dark label.", (6, "34"): "Concept image: GEM conditioner bottle, dark label.",
    (4, "49"): "Concept image: GEM body wash bottle, dark label.", (7, "26"): "Concept image: GEM body wash bottle, dark label.", (10, "8"): "Concept image: GEM body wash bottle, dark label.",
    (4, "54"): "Concept image: GEM body lotion bottle, cream label.", (8, "7"): "Concept image: GEM body lotion bottle, cream label.",
    (4, "59"): "Concept image: GEM hand wash bottle, cream label.", (9, "24"): "Concept image: GEM hand wash bottle, cream label.", (10, "7"): "Concept image: GEM hand wash bottle, cream label.",
    (5, "52"): "Concept image: GEM shampoo bottle on a sunlit stone ledge beside a folded white towel.",
    (6, "52"): "Concept image: GEM conditioner bottle on a sunlit stone ledge beside a folded white towel.",
    (5, "7"): "Close-up of the shared pump cap and bottle shoulder.", (6, "7"): "Close-up of the shared pump cap and bottle shoulder.",
    (7, "30"): "Concept image: GEM body wash bottle held in a black wall-mounted bracket on a stone wall.",
    (7, "31"): "Concept image: GEM body wash refill container, white with a black cap and a dark label marked REFILL.",
    (13, "17"): "Concept image: open GEM amenities gift box holding five bottles (shampoo, conditioner, body wash, body lotion, hand wash), its lid showing the GEM wordmark and an Arabic collection name.",
    (19, "17"): "Concept image: a cream GEM welcome card, a dark key sleeve and a key card on a stone surface.",
    (20, "17"): "Concept image: five GEM bottles (shampoo, conditioner, body wash, body lotion, hand wash) in a tray on a stone shelf beside a folded towel and a cream card.",
}
D_ALT_EXTRA = {  # replaced generic alt text (extras approved in session)
    (1, "13"): "GEM logo", (2, "22"): "GEM logo", (5, "45"): "GEM logo", (6, "45"): "GEM logo", (12, "21"): "GEM logo", (24, "6"): "GEM logo",
    (16, "17"): "Concept image: stacked cream, black and tan card stocks with a blind-embossed ring on the cream sheet.",
    (17, "17"): "Concept image: corner of a pale box with a debossed double ring on its lid.",
}
SPECIMEN_FIRST = {("Part B", 8, "5"): DEC["shapes"]["B8_first"], ("Part B", 14, "6"): DEC["shapes"]["B14_first"]}
TITLES = {("A", int(k[1:])) if k[0] == "A" else ("C", int(k[1:])): v for k, v in DEC["titles"].items()}
AR_PPT = {  # (deck, slide, shape name) -> new text; wording from the decisions file
    ("A", 38, "Text 7"): DEC["arabic"]["AR-03"]["new"],
    ("A", 65, "Text 9"): DEC["arabic"]["AR-07,AR-11"]["new"],
    ("A", 68, "Text 10"): DEC["arabic"]["AR-07,AR-11"]["new"],
}
WORD_NEW = {k: DEC["arabic"][k]["new"] for k in ("AR-16,AR-32", "AR-17,AR-33", "AR-19,AR-25", "AR-20,AR-26,AR-35,AR-40")}
PAGE_AR = " " + "".join(chr(c) for c in (0x635, 0x641, 0x62d, 0x629)) + " "  # page label word (approved wording, built from code points)
OF_AR = " " + "".join(chr(c) for c in (0x645, 0x646)) + " "

edits_log = {}


class Pkg:
    def __init__(self, src):
        self.src = src
        z = zipfile.ZipFile(src)
        self.infos = z.infolist()
        self.orig = {i.filename: z.read(i.filename) for i in self.infos}
        self.new = dict(self.orig)
        self.pairs = {}  # member -> [(old, new)]

    def get(self, m):
        return self.new[m].decode("utf8")

    def rep(self, m, old, new, label):
        x = self.get(m)
        assert x.count(old) == 1, (m, label, x.count(old))
        self.new[m] = x.replace(old, new, 1).encode("utf8")
        self.pairs.setdefault(m, []).append((old, new))

    def save(self, dst):
        with zipfile.ZipFile(dst, "w") as zo:
            for i in self.infos:
                zi = zipfile.ZipInfo(i.filename, i.date_time)
                zi.compress_type = i.compress_type
                zi.external_attr = i.external_attr
                zi.create_system = i.create_system
                zo.writestr(zi, self.new[i.filename])
        changed = sorted(k for k in self.orig if self.new[k] != self.orig[k])
        # inverse proof: undo every recorded pair backwards, must reproduce the source bytes
        for m, prs in self.pairs.items():
            x = self.new[m].decode("utf8")
            for old, new in reversed(prs):
                assert x.count(new) >= 1
                x = x.replace(new, old, 1)
            assert x.encode("utf8") == self.orig[m], ("inverse proof failed", m)
        return changed


def slide_parts(pk):
    pres = pk.get("ppt/presentation.xml")
    rels = dict(re.findall(r'<Relationship [^>]*?Id="([^"]+)"[^>]*?Target="([^"]+)"', pk.get("ppt/_rels/presentation.xml.rels")))
    rels.update({a: b for b, a in re.findall(r'<Relationship [^>]*?Target="([^"]+)"[^>]*?Id="([^"]+)"', pk.get("ppt/_rels/presentation.xml.rels"))})
    order = re.findall(r'<p:sldId [^>]*?r:id="([^"]+)"', pres)
    return ["ppt/" + rels[r].lstrip("/").replace("ppt/", "") for r in order]


def cnvpr(pk, part, sid):
    x = pk.get(part)
    ms = list(re.finditer(r'<p:cNvPr id="%s" ([^>]*?)(/?)>' % re.escape(sid), x))
    assert len(ms) == 1, (part, sid, len(ms))
    return ms[0]


def set_descr(pk, part, sid, text, replace_ok=False):
    m = cnvpr(pk, part, sid)
    attrs = m.group(1)
    if "descr=" in attrs:
        assert replace_ok, (part, sid, "has descr")
        new_attrs = re.sub(r'descr="[^"]*"', 'descr="%s"' % esc(text), attrs, count=1)
    else:
        new_attrs = re.sub(r'(name="[^"]*")', lambda mm: mm.group(1) + ' descr="%s"' % esc(text), attrs, count=1)
    pk.rep(part, m.group(0), '<p:cNvPr id="%s" %s%s>' % (sid, new_attrs, m.group(2)), "descr")


def mark_decorative(pk, part, sid):
    x = pk.get(part)
    pat = re.compile(r'<p:cNvPr id="%s" name="([^"]*)"(/>|>.*?</p:cNvPr>)' % re.escape(sid), re.S)
    ms = list(pat.finditer(x))
    assert len(ms) == 1, (part, sid)
    m = ms[0]
    assert "adec:decorative" not in m.group(0) and "descr=" not in m.group(0), (part, sid, "already marked or has descr")
    if m.group(2) == "/>":
        rep = '<p:cNvPr id="%s" name="%s">%s</p:cNvPr>' % (sid, m.group(1), DECOR)
    else:
        assert m.group(2).count("</a:extLst></p:cNvPr>") == 1, (part, sid)
        rep = m.group(0).replace("</a:extLst></p:cNvPr>", EXT + "</a:extLst></p:cNvPr>")
    pk.rep(part, m.group(0), rep, "decorative")


def add_title(pk, part, text, slide_h):
    x = pk.get(part)
    assert not re.search(r'<p:ph type="(title|ctrTitle)"', x), (part, "title already present")
    ids = [int(i) for i in re.findall(r'<p:cNvPr id="(\d+)"', x)]
    nid = max(ids) + 1
    sp = ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="Title %d"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
          '<p:spPr><a:xfrm><a:off x="457200" y="%d"/><a:ext cx="8229600" cy="365760"/></a:xfrm></p:spPr>'
          '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:pPr><a:lnSpc><a:spcPct val="100000"/></a:lnSpc></a:pPr><a:r><a:rPr lang="en-US" sz="1200" dirty="0"/><a:t>%s</a:t></a:r></a:p></p:txBody></p:sp>'
          % (nid, nid, slide_h + 457200, esc(text)))
    m = re.search(r"</p:grpSpPr>|<p:grpSpPr/>", x)
    assert m
    pk.rep(part, m.group(0), m.group(0) + sp, "title")
    return nid


def set_ar_text(pk, part, name, new_text):
    x = pk.get(part)
    blocks = [b for b in re.findall(r"<p:sp>.*?</p:sp>", x, re.S) if 'name="%s"' % name in b[:400] and re.search("[" + chr(0x600) + "-" + chr(0x6ff) + "]", b)]
    assert len(blocks) == 1, (part, name, len(blocks))
    ts = re.findall(r"<a:t>([^<]*)</a:t>", blocks[0])
    assert len(ts) == 1, (part, name, ts)
    old = "<a:t>%s</a:t>" % ts[0]
    pk.rep(part, blocks[0], blocks[0].replace(old, "<a:t>%s</a:t>" % esc(new_text), 1), "arabic text")
    return hashlib.sha256(html.unescape(ts[0]).encode("utf8")).hexdigest()[:12]


def build_ppt(key):
    src, outname = DECKS[key]
    pk = Pkg(src)
    parts = slide_parts(pk)
    pres = pk.get("ppt/presentation.xml")
    slide_h = int(re.search(r"<p:sldSz cx=\"\d+\" cy=\"(\d+)\"", pres).group(1))
    log = {"source": str(src), "source_sha256": sha(open(src, "rb").read()), "titles": [], "decorative": 0, "alt": 0, "arabic": []}
    if key in ("A", "C"):
        for (k, s), t in sorted(TITLES.items()):
            if k == key:
                add_title(pk, parts[s - 1], t, slide_h)
                log["titles"].append(s)
    for (k, s, name), t in AR_PPT.items():
        if k == key:
            h = set_ar_text(pk, parts[s - 1], name, t)
            log["arabic"].append([s, name, "old_sha12=" + h, "new_sha12=" + hashlib.sha256(t.encode("utf8")).hexdigest()[:12]])
    # the 89 unclassified shapes from the AX01 alt-text register that were not applied in AX01
    with open(AX / "07_AX01_Alt_Text_Register.csv", encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["Applied in AX01 candidate?"] == "no" and r["Classification"] != "INFORMATIVE" and PART[r["Document"]] == key]
    for r in rows:
        part, sid, s = parts[int(r["Slide"]) - 1], r["Shape id"], int(r["Slide"])
        spec = SPECIMEN_FIRST.get((r["Document"], s, sid))
        if spec:
            set_descr(pk, part, sid, spec)
            log["alt"] += 1
        else:
            mark_decorative(pk, part, sid)
            log["decorative"] += 1
    if key == "D":
        for (s, sid), t in D_ALT.items():
            set_descr(pk, parts[s - 1], sid, t)
            log["alt"] += 1
        for (s, sid), t in D_ALT_EXTRA.items():
            set_descr(pk, parts[s - 1], sid, t, replace_ok=True)
            log["alt"] += 1
    dst = OUT / outname
    changed = pk.save(dst)
    log.update(candidate=outname, candidate_sha256=sha(open(dst, "rb").read()), members_changed=changed, inverse_proof="PASS")
    return log


def build_word(name, edits_for):
    src = LH / ("GEM_Letterhead_%s.docx" % name)
    pk = Pkg(src)
    log = {"source": str(src), "source_sha256": sha(open(src, "rb").read()), "text_edits": [], "footer_page_labels": 0}
    doc = pk.get("word/document.xml")
    for key, count in edits_for.items():
        new = WORD_NEW[key]
        # the old wording is whatever the template holds for this paragraph class; matched by the queue SHA prefixes recorded in the register
        olds = DEC["arabic_old"][key]
        for old in olds:
            n = doc.count("<w:t>%s</w:t>" % esc(old))
            if n:
                assert n == count, (name, key, n, count)
                pk.rep("word/document.xml", "<w:t>%s</w:t>" % esc(old), "<w:t>%s</w:t>" % esc(new), key)
                doc = pk.get("word/document.xml")
                log["text_edits"].append([key, count])
                break
        else:
            raise AssertionError((name, key, "old wording not found"))
    for part in sorted(k for k in pk.orig if re.match(r"word/footer\d*\.xml", k)):
        x = pk.get(part)
        AR_RPR = ('<w:rFonts w:ascii="Noto Sans Arabic" w:hAnsi="Noto Sans Arabic" w:cs="Noto Sans Arabic" w:eastAsia="Noto Sans Arabic"/><w:b w:val="0"/>'
                  '<w:color w:val="12171D"/><w:sz w:val="18"/><w:lang w:val="ar-SA" w:bidi="ar-SA"/><w:rtl w:val="1"/><w:szCs w:val="18"/><w:bCs w:val="0"/><w:spacing w:val="0"/>')
        # "Page" label: the separator spaces stay in their own left-to-right run (original run properties); the Arabic word is a separate right-to-left run
        pat = re.compile(r'<w:r><w:rPr>((?:(?!</w:rPr>).)*)</w:rPr><w:t xml:space="preserve">( *)Page </w:t></w:r>', re.S)
        ms = list(pat.finditer(x))
        assert len(ms) == 1, (name, part, "Page", len(ms))
        rpr, lead = ms[0].group(1), ms[0].group(2)
        new_runs = ('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, lead)
                    + '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s </w:t></w:r>' % (AR_RPR, PAGE_AR.strip()))
        pk.rep(part, ms[0].group(0), new_runs, "footer Page")
        x = pk.get(part)
        pat = re.compile(r'<w:r><w:rPr>(?:(?!</w:rPr>).)*</w:rPr><w:t xml:space="preserve"> of </w:t></w:r>', re.S)
        ms = list(pat.finditer(x))
        assert len(ms) == 1, (name, part, "of", len(ms))
        pk.rep(part, ms[0].group(0), '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve"> %s </w:t></w:r>' % (AR_RPR, OF_AR.strip()), "footer of")
        x = pk.get(part)
        log["footer_page_labels"] += 1
    dst = OUT / ("GEM_Letterhead_%s_HR01_CANDIDATE.docx" % name)
    changed = pk.save(dst)
    log.update(candidate=dst.name, candidate_sha256=sha(open(dst, "rb").read()), members_changed=changed, inverse_proof="PASS")
    return log


def main():
    logs = {}
    for k in "ABCD":
        logs["Part " + k] = build_ppt(k)
    S, A, C, D = "AR-16,AR-32", "AR-17,AR-33", "AR-19,AR-25", "AR-20,AR-26,AR-35,AR-40"
    logs["Letterhead Arabic First Page"] = build_word("Arabic_First_Page", {S: 1, A: 1, C: 1, D: 1})
    logs["Letterhead Arabic Continuation"] = build_word("Arabic_Continuation", {C: 1, D: 1})
    logs["Letterhead Bilingual First Page"] = build_word("Bilingual_First_Page", {S: 1, A: 1, D: 1})
    logs["Letterhead Bilingual Continuation"] = build_word("Bilingual_Continuation", {D: 1})
    json.dump(logs, open(LOGP, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for k, v in logs.items():
        print(k, "| members changed:", len(v["members_changed"]), "| titles", len(v.get("titles", [])), "| decorative", v.get("decorative", "-"), "| alt", v.get("alt", "-"), "| inverse", v["inverse_proof"])


if __name__ == "__main__":
    main()
