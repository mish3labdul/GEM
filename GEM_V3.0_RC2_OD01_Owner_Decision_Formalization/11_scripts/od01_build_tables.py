#!/usr/bin/env python3
"""OD01 table builder.

Run from the repository root:  python3 -I GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/11_scripts/od01_build_tables.py

Writes (inside the OD01 package only):
  02_OD01_Owner_Decision_Register.csv
  04_OD01_Gate_Impact_Matrix.csv
  08_OD01_Open_Evidence_After_Decisions.csv
  OD01_Mashal_Arabic_Review_Queue.csv
  OD01_Mashal_Accessibility_Content_Queue.csv

Reads (read-only):
  AR01 11_AR01_Native_Arabic_Reviewer_Queue.csv  (no Arabic text in that file)
  AX01 05_AX01_Title_Remediation_Register.csv
  AX01 07_AX01_Alt_Text_Register.csv

Relative paths only. No source file is modified. No decision field is populated on behalf of a reviewer.
"""
import csv
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_OD01_Owner_Decision_Formalization")
AR01 = Path("GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation")
AX01 = Path("GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation")
DATE = "2026-10-09"
SRC = ("Brand Owner instruction in the OD01 task brief, " + DATE +
       ". No individual name, signature or time was supplied; none is invented.")


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


# ---------------------------------------------------------------- 02 register
REG_HEADER = ["Decision ID", "Title", "Status", "Owner", "Decision", "Effective scope",
              "Does this close an evidence gate?", "Affected gates", "Remaining evidence",
              "Source / authority", "Date recorded"]
NO = "NO"
REGISTER = [
    ["OD-G01", "Arabic-first correspondence", "APPROVED", "Brand Owner",
     "For Saudi/GCC bilingual business correspondence Arabic leads and English follows. Latin technical identifiers, filenames, URLs, codes and system references stay Latin/LTR. The GEM logo is never mirrored.",
     "Correspondence only. It does NOT broaden S07 beyond its existing wayfinding scope.",
     NO, "VAL-07; AC10", "Native Arabic linguistic review (44-item queue); continuous production RTL layouts; screen-reader order; AC10 Brand Owner decision.",
     SRC, DATE],
    ["OD-G02", "Accessibility title policy", "APPROVED", "Brand Owner",
     "Every slide needing semantic navigation should have a meaningful accessibility title. Remediation must not alter approved visible geometry merely to satisfy a native checker. Use an existing visible heading where it can safely serve; otherwise a non-visible structural title only if visually neutral, semantically accurate and geometry-neutral. Title wording that needs interpretation is provided or approved by the Accessibility Content Owner.",
     "Future title remediation in Parts A-D candidates.",
     NO, "VAL-08", "30 unresolved slide titles still need an owner disposition; assistive-technology testing.",
     SRC, DATE],
    ["OD-G03", "Alt-text ownership", "APPROVED", "Brand Owner",
     "Informative imagery gets concise, meaningful alt text written or approved by the Accessibility Content Owner. Decorative, redundant, background and ornamental assets are marked decorative where supported. Generic filler descriptions that add no information are not acceptable.",
     "All informative imagery in Parts A-D candidates.",
     NO, "VAL-08", "23 Part D product-image alt-text items, 6 generic Part D alt texts and 89 unclassified shapes still need an owner disposition.",
     SRC, DATE],
    ["OD-G04", "Reading order", "APPROVED", "Brand Owner",
     "Final semantic reading order is validated manually through assistive-technology review. PowerPoint z-order or heuristic checker output is not changed in bulk without evidence that the resulting order is correct and visually safe.",
     "Reading-order handling for Parts A-D candidates.",
     NO, "VAL-07; VAL-08", "Manual assistive-technology review (200 heuristic-flagged slides and 7 Arabic/bilingual slides); screen-reader test matrix (13 scenarios) not run.",
     SRC, DATE],
    ["OD-G05", "Contrast", "APPROVED", "Brand Owner",
     "The approved GEM palette is unchanged. Beige #BCACA7 on White #FFFFFF is not used for functional small text or other text needing WCAG AA contrast. The pairing may remain in palette specimens, demonstrations, decorative contexts and non-essential visual uses. The palette itself is not inferred to need change.",
     "Palette-use policy. Treats the Beige-on-White pair on Part A slide 33 (a specimen candidate) as a policy matter.",
     NO, "VAL-08", "Contrast of 113 text runs over pictures (manual); formal exceptions; confirmation that Part A slide 33 is a specimen.",
     SRC, DATE],
    ["OD-G06", "Arabic / bilingual footer localization", "APPROVED", "Brand Owner",
     "Functional labels in Arabic and bilingual correspondence, including page labels where relevant, are localized appropriately. Tagline treatment follows the formally approved bilingual brand-language rule. No Arabic translation counts as linguistically approved until native Arabic linguistic review is complete.",
     "Arabic and bilingual correspondence footers and functional labels.",
     NO, "VAL-07; AC10", "Native Arabic linguistic sign-off of every localized label and the tagline translation.",
     SRC, DATE],
    ["OD-G07", "Latin technical IDs", "APPROVED", "Brand Owner",
     "Technical identifiers stay in original Latin/LTR form inside Arabic and bilingual content. Latin language metadata is used where technically appropriate. Inter may be used for Latin technical identifiers only if it can be introduced without disrupting native layout, bidi behavior stays correct and native validation confirms it; otherwise the validated existing typography is preserved. No unnecessary mixed-script changes are forced.",
     "Latin technical identifiers within Arabic and bilingual content.",
     NO, "VAL-05; VAL-07; VAL-19; Y03", "Native validation of any Inter introduction; font licence and build verification (Y03, VAL-05).",
     SRC, DATE],
    ["OD-G08", "Word section direction", "APPROVED", "Brand Owner",
     "Section-level RTL is not forced for consistency where paragraph- and run-level bidi settings already give correct native behavior. Section direction changes only when native Microsoft Word evidence shows a functional issue.",
     "Word letterhead templates.",
     NO, "VAL-07", "Windows Word and Word Online validation; multi-page continuation flow with real content.",
     SRC, DATE],
    ["OD-G09", "Native Arabic Reviewer / Localization Lead", "ASSIGNED", "Brand Owner",
     "Role assigned to Mashal: Native Arabic Reviewer / Localization Lead. Authority: translation accuracy, Saudi/GCC terminology, punctuation, numeral convention, bilingual phrasing, tone, tagline translation and linguistic sign-off. The assignment identifies the authorized reviewer. It does not complete the 44-item Arabic reviewer queue.",
     "Role assignment. Assignee: Mashal (first name only as supplied).",
     NO, "VAL-07; AC10; AC19 (role holder)", "The 44-item queue must actually be reviewed and evidenced. Whether this role is the Register role 'Arabic / Localization Lead' needs owner confirmation.",
     SRC, DATE],
    ["OD-G10", "Accessibility Content Owner / Brand Content Owner", "ASSIGNED", "Brand Owner",
     "Role assigned to Mashal: Accessibility Content Owner / Brand Content Owner. Authority: semantic slide-title decisions, image purpose, alt text, complex visual descriptions, informative/decorative/redundant classification and ambiguous accessibility-content decisions. The assignment does not resolve the 30 unresolved slide titles, the 23 Part D product-image alt-text items or the remaining ambiguous objects.",
     "Role assignment. Assignee: Mashal (first name only as supplied). This role is not one of the 12 Register roles.",
     NO, "VAL-08", "30 titles, 23 Part D alt-text items, 6 generic alt texts and 89 unclassified shapes still need decisions exercised and recorded.",
     SRC, DATE],
    ["OD-G11", "Repository / Legal-IP visibility policy", "RESOLVED — OWNER REPOSITORY VISIBILITY APPROVAL", "Brand Owner",
     "Owner label: 'C — CURRENT PUBLIC REPOSITORY APPROVED'. The current GEM repository may remain public; public visibility is approved for the current repository and future controlled project material. This is an owner decision, not a legal opinion. It is not evidence of trademark availability, logo-artwork ownership, font licences, image/model/property rights, third-party marks, supplier legal clauses or publication rights for every asset. Note: the label 'C' is the owner's; option C in the D7 package reads 'Make repository private' and was NOT selected (see 06).",
     "mish3labdul/GEM (origin), as named by the D7 package. The second public repository mashaelalh/GEM is not covered by this record.",
     NO, "D7 (owner visibility decision only); VAL-03; VAL-04; VAL-05; VAL-06; Y01; Y02; Y03; Y04", "All Legal/IP evidence stays open where the governing gates require it.",
     SRC, DATE],
    ["OD-G12", "AC20 final release authorization", "OPEN — FINAL RELEASE AUTHORIZATION PENDING", "Brand Owner",
     "Keep AC20 open. 'Brand Owner release authorization shall occur only after the required upstream validation, Legal/IP, localization, accessibility, production and release-consistency evidence has been satisfactorily dispositioned or formally deferred by authorized owners.'",
     "AC20 only. No release, approval or production-ready label is authorized.",
     NO, "AC20 (and every upstream gate it depends on)", "All upstream evidence; a named Brand Owner holder (Register 'Owners & Governance' requires it before AC20 authorization).",
     SRC, DATE],
]

# ---------------------------------------------------------------- 04 impact
IMP_HEADER = ["Decision ID", "Gate / item", "Effect of decision on this gate", "Gate closed by decision?",
              "Gate status after OD01", "Evidence still needed"]
IMPACT = [
    ["OD-G01", "VAL-07", "Removes ambiguity on correspondence order (Arabic leads). Not linguistic approval.", NO, "Not started (Register) - open", "Native review; screen-reader order; production RTL layouts"],
    ["OD-G01", "AC10", "Policy input only.", NO, "Evidence Required - open", "Brand Owner decision with localization evidence, or formal deferral where the Register allows"],
    ["OD-G01", "VAL-12 / S07", "None. S07 keeps its wayfinding scope; it is not extended to correspondence.", NO, "Deferred (unchanged)", "Unchanged"],
    ["OD-G02", "VAL-08", "Defines the title policy for remediation. Resolves none of the 30 titles.", NO, "In progress - open", "Owner disposition for 30 titles; assistive-technology testing"],
    ["OD-G03", "VAL-08", "Defines alt-text ownership. Writes or approves none of the 23 Part D descriptions.", NO, "In progress - open", "Owner-approved alt text for 23 pictures; classification of 89 shapes; 6 generic alt texts"],
    ["OD-G04", "VAL-08", "Defines reading-order policy. No order was changed or validated.", NO, "In progress - open", "Manual assistive-technology review"],
    ["OD-G04", "VAL-07", "Arabic/bilingual logical order still needs a screen reader.", NO, "Not started - open", "Screen-reader order evidence"],
    ["OD-G05", "VAL-08", "Settles palette-policy treatment of Beige on White. Accessibility evidence stays contextual.", NO, "In progress - open", "Confirm slide 33 is a specimen; manual contrast of text over pictures; formal exceptions"],
    ["OD-G06", "VAL-07", "Policy for localized functional labels. No Arabic wording approved.", NO, "Not started - open", "Native linguistic sign-off"],
    ["OD-G06", "AC10", "Policy input only.", NO, "Evidence Required - open", "As above"],
    ["OD-G07", "VAL-05 / Y03 / VAL-19", "Permits Inter for Latin IDs only where natively validated. No font licence or build is verified.", NO, "VAL-05 In progress; Y03 Evidence Required; VAL-19 In progress - open", "Font licence/build verification; native validation of any Inter introduction"],
    ["OD-G07", "VAL-07", "Preserves Latin LTR identifiers. No new typography is introduced.", NO, "Not started - open", "Native validation"],
    ["OD-G08", "VAL-07", "No forced section-level RTL. Word evidence decides.", NO, "Not started - open", "Windows Word, Word Online and multi-page checks"],
    ["OD-G09", "VAL-07", "Names the authorized reviewer. The queue is not executed.", NO, "Not started - open", "44 queue items reviewed and evidenced"],
    ["OD-G09", "AC10", "Names the authorized reviewer. No Arabic approval.", NO, "Evidence Required - open", "Brand Owner decision with localization evidence"],
    ["OD-G09", "AC19", "Possibly names 1 of 12 Register roles (Arabic / Localization Lead) once the owner confirms the mapping.", NO, "Approved with modification; role-holder condition UNMET", "11 further holders (or 12 if the mapping is not confirmed), including the named Brand Owner"],
    ["OD-G10", "VAL-08", "Names the authorized content owner. No title or alt text is decided.", NO, "In progress - open", "Dispositions for the accessibility queue"],
    ["OD-G10", "AC19", "Role is not one of the 12 Register roles; it does not name a Register holder.", NO, "Approved with modification; role-holder condition UNMET", "As above"],
    ["OD-G11", "D7 (owner level)", "Owner repository-visibility decision resolved: current public repository approved.", "NO (D7 is not a validation gate; it is an owner decision)", "Owner decision RESOLVED; Legal/IP evidence OPEN where required", "None for the owner-level visibility decision"],
    ["OD-G11", "VAL-03 / Y01", "None. Public visibility is not trademark clearance.", NO, "Not started / Evidence Required - open", "Target-market clearance or legal advice"],
    ["OD-G11", "VAL-04 / Y02", "None. Not artwork-ownership evidence.", NO, "Not started / Evidence Required - open", "Executed ownership or assignment evidence"],
    ["OD-G11", "VAL-05 / Y03", "None. Not font-licence evidence.", NO, "In progress / Evidence Required - open", "Licence and exact-build verification for intended uses"],
    ["OD-G11", "VAL-06 / Y04", "None. Not image/model/property-rights evidence.", NO, "Not started / Evidence Required - open", "Rights register for every approved production image"],
    ["OD-G12", "AC20", "Keeps AC20 open as the final Brand Owner release-authorization gate.", NO, "Evidence Required - OPEN / FINAL RELEASE AUTHORIZATION PENDING", "Upstream evidence closed or formally dispositioned/deferred by authorized owners where the governing system permits"],
]

# ---------------------------------------------------------------- 08 evidence
EV_HEADER = ["ID", "Evidence requirement", "Owner", "Current status", "Owner decision impact",
             "Technical evidence available", "Human/legal/supplier evidence missing", "Next action", "Can close now?"]
NOT_DEC = "None from OD-G01 to OD-G12"
EVID = [
    ["VAL-01", "Signed architecture and commercial-scope decision", "Brand Owner + Commercial Lead", "In progress", NOT_DEC, "Target architecture pre-decided in the Register", "Operational capability evidence; named commercial approval", "Name the Commercial Lead; obtain commercial approval", "NO"],
    ["VAL-02", "Production logo master verification", "Design Custodian", "Not started (Register); vector kit received, acceptance pending", NOT_DEC, "Vector kit received (SVG/PDF/EPS/PNG)", "Brand Owner acceptance as production master; master artwork ID and version", "Owner acceptance decision", "NO"],
    ["VAL-03", "Trademark / distinctiveness legal review", "Legal / IP Counsel", "Not started", "OD-G11: none (visibility is not legal clearance)", "None", "Target-market clearance or documented legal advice", "Commission Legal/IP review", "NO"],
    ["VAL-04", "Logo artwork ownership / rights evidence", "Brand Owner / Legal", "Not started", "OD-G11: none", "None", "Executed ownership or assignment evidence", "Obtain and archive evidence", "NO"],
    ["VAL-05", "Font licence and deployment verification", "Design Custodian / Legal", "In progress", "OD-G07 permits Inter for Latin IDs only where natively validated; OD-G11: none", "OFL material referenced in source packages; 400-only implementation (D5)", "Exact final builds and deployment/distribution licence verification; accepted 500-weight files", "Verify licences and builds", "NO"],
    ["VAL-06", "Image / model / property rights register", "Art Direction / Legal", "Not started", "OD-G11: none", "None", "Rights, source and usage metadata for every approved production image", "Build the rights register", "NO"],
    ["VAL-07", "Arabic / RTL native QA", "Arabic / Localization Lead", "Not started", "OD-G01, G04, G06, G07, G08 policy; OD-G09 reviewer assigned", "AR01 native technical validation (PowerPoint and Word); AX01 metadata preserved", "Native linguistic review of 44 items; screen-reader order; production RTL layouts; numeral sign-off; Windows Word and Word Online", "Mashal executes the Arabic review queue", "NO"],
    ["VAL-08", "Accessibility implementation QA", "Accessibility QA", "In progress", "OD-G02, G03, G04, G05 policy; OD-G10 content owner assigned", "AX01 native checker before/after; 576 Category A fixes; tables, titles (24 applied), decorative flags (486)", "Assistive-technology testing (EN and AR); 30 titles; 23 + 89 + 6 alt-text items; contrast over pictures; formal exceptions; independent QA", "Mashal works the accessibility content queue; schedule AT testing", "NO"],
    ["VAL-09", "Packaging pilot physical proof", "Product + Procurement + Supplier QA", "Not started", NOT_DEC, "None", "Supplier dielines, proofs and signed sample", "Supplier engagement", "NO"],
    ["VAL-10", "Packaging / product regulatory and claims review", "Product / Regulatory / Legal", "Not started", NOT_DEC, "None", "Per-SKU, per-market regulatory evidence", "Regulatory review", "NO"],
    ["VAL-11", "Supplier production acceptance", "Procurement + Supplier QA", "Not started", NOT_DEC, "None", "Signed supplier acceptance", "Supplier engagement", "NO"],
    ["VAL-12", "Wayfinding fabrication / physical legibility QA", "Environmental Design + Accessibility QA", "Deferred", "OD-G01 expressly leaves S07 at its wayfinding scope", "None", "Whole record (deferred until a live property brief exists)", "None until a property brief exists", "NO"],
    ["VAL-13", "Digital tokens and component implementation", "Digital Design + Engineering", "In progress", NOT_DEC, "Derived token package (153 tokens)", "Component source; Storybook; independent implementation QA", "Locate or build the living source (OD-SRC)", "NO"],
    ["VAL-14", "Motion / reduced-motion master QA", "Motion / Digital Lead", "In progress", NOT_DEC, "None", "Production motion masters and reduced-motion equivalents", "Validate masters", "NO"],
    ["VAL-15", "Native presentation / PDF QA", "Presentation Production / QA", "Not started", NOT_DEC, "Native PowerPoint and Word open/render checks of candidates (NP01, NP01-R1, AR01, AX01); no final deliverables", "Save/reopen/export of final deliverables; tagged-PDF accessibility; Acrobat", "Await final deliverables", "NO"],
    ["VAL-16", "Controlled release manifest", "Asset Librarian", "Not started", NOT_DEC, "Per-package manifests and SHA-256 lists exist; no release archive", "Final release archive manifest; asset-ID and checksum convention (REQUIRES OWNER)", "Await release archive", "NO"],
    ["VAL-17", "Guideline usability test", "Brand Governance / Independent Tester", "Not started", NOT_DEC, "None", "Independent usability test", "Run once final guidelines are assembled", "NO"],
    ["VAL-18", "NOT ALLOCATED (no such gate; not used)", "n/a", "NOT ALLOCATED", "n/a", "n/a", "n/a", "None - do not create or close", "n/a"],
    ["VAL-19", "Typography architecture and tracking QA", "Design Custodian / Presentation QA", "In progress", "OD-G07 (typography of Latin IDs only)", "None new", "Exact licensed builds; optical/native tracking QA", "Optical and native QA", "NO"],
    ["VAL-20", "Responsive, locale and living digital-system QA", "Digital Design + Engineering + Localization QA", "Not started", NOT_DEC, "None", "Implementation testing", "Await implementation", "NO"],
    ["VAL-21", "Cross-document release consistency", "Brand Governance / Design Custodian", "Not started", "OD01 adds an owner-decision layer a future VAL-21 check must include", "Automated consistency check on RC2 Parts A-C (112/112); no formal sign-off", "Formal cross-document sign-off", "Perform after assembly of final documents", "NO"],
    ["Y01", "Trademark availability / registration legally reviewed", "Legal / IP Counsel", "Evidence Required", "OD-G11: none", "None", "Target-market trademark clearance evidence", "Commission legal review", "NO"],
    ["Y02", "Logo artwork ownership documented", "Brand Owner + Legal / IP Counsel", "Evidence Required", "OD-G11: none", "None", "Executed ownership or assignment evidence", "Obtain evidence", "NO"],
    ["Y03", "Font licences adequate for print/web/app use", "Design Custodian + Legal / IP Counsel", "Evidence Required", "OD-G11: none; OD-G07 Inter policy", "OFL material referenced", "Exact build and deployment verification", "Verify licences", "NO"],
    ["Y04", "Image/model/property rights documented", "Design Custodian / Art Direction + Legal / IP Counsel", "Evidence Required", "OD-G11: none", "None", "Complete rights register", "Build rights register", "NO"],
    ["AC07", "Master artwork approved", "Brand Owner", "Evidence Required", NOT_DEC, "Vector kit received", "Final vector production masters, no-spark micro mark, all configurations verified", "Owner acceptance after verification", "NO"],
    ["AC10", "Arabic system approved or formally deferred", "Brand Owner", "Evidence Required", "OD-G09 names the reviewer; no approval or deferral exercised", "AR01 technical validation", "Native RTL/localization/accessibility QA, or a formal deferral where the Register allows it", "Mashal reviews; Brand Owner then decides or formally defers", "NO"],
    ["AC17", "Production specifications approved", "Brand Owner", "Evidence Required", NOT_DEC, "None", "Supplier-ready specifications and physical/fabrication validation", "Supplier and fabrication evidence", "NO"],
    ["AC19", "Governance model approved (named role holders required before release)", "Brand Owner", "Approved with modification; role-holder condition UNMET", "OD-G09 may name 1 of 12 Register roles (mapping needs owner confirmation); OD-G10 is not a Register role", "None", "All 12 role holders named, including the Brand Owner", "Owner names the remaining holders", "NO"],
    ["AC20", "Brand Owner release authorization", "Brand Owner", "OPEN / FINAL RELEASE AUTHORIZATION PENDING", "OD-G12 keeps it open", "None", "Upstream evidence closed or formally dispositioned/deferred by authorized owners where the governing system permits; named Brand Owner holder", "Await upstream evidence", "NO"],
    ["OD-TPL", "Templates (PowerPoint master, documents, social, email, wayfinding)", "Design Custodian", "Open deliverable", NOT_DEC, "Letterhead set (working application)", "Remaining templates", "Produce templates", "NO"],
    ["OD-SRC", "Part B living source: tokens.json + component bundle + Storybook", "Digital Design Lead / Engineering Lead", "Open", NOT_DEC, "Editable deck source controlled", "Living digital source", "Locate or build", "NO"],
]

# ---------------------------------------------------------------- queues
def arabic_queue():
    src = AR01 / "11_AR01_Native_Arabic_Reviewer_Queue.csv"
    with open(src, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for i, r in enumerate(rows, 1):
        out.append([
            "OD01-AR-%02d" % i, r["Document"],
            "%s \u00b7 %s \u00b7 SHA %s \u00b7 AR01 queue row %d" % (r["Slide / page"], r["Element"], r["Text SHA-256 (prefix)"], i),
            r["Potential impact"],
            r["Question for native reviewer"], r["Priority"],
            r["Technical issue resolved?"],
            "", "", "PENDING",
        ])
    return out


def accessibility_queue():
    out = []
    # 30 unresolved slide titles
    with open(AX01 / "05_AX01_Title_Remediation_Register.csv", encoding="utf-8", newline="") as fh:
        titles = [r for r in csv.DictReader(fh) if r["Result"].startswith("NOT APPLIED")]
    for i, r in enumerate(titles, 1):
        out.append(["OD01-AC-T%02d" % i, r["Document"], r["Slide"],
                    "Slide title: " + r["Classification"],
                    "Approve title wording for this slide; implementation per OD-G02 (use an existing visible heading where safe, otherwise a visually neutral, geometry-neutral structural title). AX01 note: " + r["Recommended action"],
                    r["Classification"] + " / " + r["Result"],
                    "", "", "PENDING"])
    # 23 Part D product images + 89 unclassified shapes
    with open(AX01 / "07_AX01_Alt_Text_Register.csv", encoding="utf-8", newline="") as fh:
        alts = [r for r in csv.DictReader(fh) if r["Applied in AX01 candidate?"] == "no"]
    pics = [r for r in alts if r["Classification"] == "INFORMATIVE"]
    shapes = [r for r in alts if r["Classification"] != "INFORMATIVE"]
    for i, r in enumerate(pics, 1):
        out.append(["OD01-AC-A%02d" % i, r["Document"], r["Slide"],
                    "Informative picture (shape id %s)" % r["Shape id"],
                    "Owner to write or approve concise alt text, or classify as decorative/redundant (do not describe by guess).",
                    r["Classification"] + " / " + r["Recommended action"], "", "", "PENDING"])
    for i, r in enumerate(shapes, 1):
        out.append(["OD01-AC-S%03d" % i, r["Document"], r["Slide"],
                    "Unclassified shape (id %s, %s)" % (r["Shape id"], r["Geometry class"]),
                    "Owner to classify informative / decorative / redundant and supply alt text if informative.",
                    r["Classification"], "", "", "PENDING"])
    # items not itemized in the AX01 registers
    out.append(["OD01-AC-G01", "Part D", "(to be identified)", "Generic alt text on 6 pictures (AX01-F04)",
                "Owner to replace generic 'Supplied GEM raster artwork...' descriptions with meaningful alt text (OD-G03). The 6 pictures are not itemized in the AX01 registers and must be identified from the AX01 candidate deck.",
                "AX01-F04 (count only)", "", "", "PENDING IDENTIFICATION"])
    out.append(["OD01-AC-C01", "Part A", "33", "Beige #BCACA7 on White #FFFFFF run (specimen?)",
                "Owner to confirm the run is a palette specimen/demonstration under OD-G05 and not functional text.",
                "AX01 contrast assessment: governed pair measures about 2.19:1", "", "", "PENDING"])
    return out, len(titles), len(pics), len(shapes)


def main():
    n = {}
    n["02"] = write_csv(PKG / "02_OD01_Owner_Decision_Register.csv", REG_HEADER, REGISTER)
    n["04"] = write_csv(PKG / "04_OD01_Gate_Impact_Matrix.csv", IMP_HEADER, IMPACT)
    n["08"] = write_csv(PKG / "08_OD01_Open_Evidence_After_Decisions.csv", EV_HEADER, EVID)
    n["AR"] = write_csv(PKG / "OD01_Mashal_Arabic_Review_Queue.csv",
                        ["Item ID", "Document", "Slide/page (slide \u00b7 element \u00b7 text SHA prefix \u00b7 AR01 row)", "Category", "Decision required", "Priority",
                         "Existing technical result", "Reviewer disposition", "Reviewer note", "Status"],
                        arabic_queue())
    acc, t, p, s = accessibility_queue()
    n["AC"] = write_csv(PKG / "OD01_Mashal_Accessibility_Content_Queue.csv",
                        ["Item ID", "Document", "Slide", "Object/category", "Decision required",
                         "Current technical classification", "Owner disposition",
                         "Approved title/alt-text reference", "Status"], acc)
    print("rows:", n, "titles", t, "pictures", p, "shapes", s)
    assert n["AR"] == 44 and t == 30 and p == 23 and s == 89, "source counts changed"


if __name__ == "__main__":
    main()
