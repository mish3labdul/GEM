#!/usr/bin/env python3
"""HR01 Queue 4 registers (09 Legal/IP evidence inventory, 10 Legal/IP disposition register).

Run from the repository root:  python3 -I GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/16_scripts/hr01_build_legal_registers.py [owner_evidence.json]

Evidence = what the repository files say (found by read-only research and verified directly). Repository evidence only: no external source was
consulted (owner decision in session). An evidence review is NOT legal clearance. Optional owner_evidence.json (local-only) records evidence
pointers the owner stated in session ({gate: "statement"}); such statements are logged as pointers, never as reviewed evidence.
"""
import csv
import json
import sys
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure")
OWN = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}
LH = "GEM_Letterhead_Set_v1.1_Application_Revision_03"

INV_H = ["Asset/evidence ID", "Category", "Source", "Owner / provenance as recorded", "Licence / evidence located?", "Evidence path / reference", "Legal review required?", "Gap", "Recommended disposition"]
INV = [
    ["LI-01", "Trademark / wordmark", "GEM name and wordmark (GEM™)", "Brand Owner (no ownership document in repository)", "NO",
     "Register VAL-03 / Y01 (Not started / Evidence Required); qa/GEM_V3_RC2_Final_Open_Evidence_Register.md lines 9, 27; D7 05_Open_Legal_IP_Dependencies.md", "YES — Legal / IP Counsel",
     "No target-market clearance, registration record or legal advice. The ™ mark appears in documents; a ™-usage rule is itself marked [REQUIRES OWNER / Legal] (CR-57).", "LEGAL COUNSEL REVIEW REQUIRED"],
    ["LI-02", "Trademark / tagline", "'HOSPITALITY, IN PERFECT PROPORTION' (fixed tagline)", "Brand Owner (no record)", "NO", "Part B slide 3; Part C slide 17 (usage rule only)", "YES — Legal / IP Counsel",
     "No availability or ownership evidence for the tagline; only a usage rule exists.", "LEGAL COUNSEL REVIEW REQUIRED"],
    ["LI-03", "Logo artwork", "GEM_Brand_Assets_v1.0/04_official_kit (64 vector masters: SVG/EPS/PDF; PNGs; icons; motion)", "'Vector logo kit received from the project owner' (README line 3); no creator, assignment or work-for-hire record", "NO",
     "GEM_Brand_Assets_v1.0/README.md; Register VAL-04 / Y02 (Not started / Evidence Required); VAL-02 acceptance pending", "YES — Brand Owner + Legal / IP Counsel",
     "Executed ownership or assignment evidence is absent; kit acceptance as production master is pending (VAL-02).", "OWNER EVIDENCE REQUIRED"],
    ["LI-04", "Logo artwork (derived)", "GEM_Brand_Assets_v1.0/05_layout_matched (10 files)", "Derived from the kit (only the SVG viewBox differs; README line 8)", "NO", "GEM_Brand_Assets_v1.0/README.md", "YES", "Depends on LI-03; no separate record.", "OWNER EVIDENCE REQUIRED"],
    ["LI-05", "Created brand assets", "GEM_Brand_Assets_v1.0/01_svg (11 files: tagline outlines, palette sheet, status labels)", "'Created from the specification' (README line 9); no named author", "NO", "GEM_Brand_Assets_v1.0/README.md", "YES", "No authorship record; tagline outline depends on LI-02.", "OWNER EVIDENCE REQUIRED"],
    ["LI-06", "Font — Jost", "%s/00_source/fonts/jost/Jost-Regular.ttf (Regular 400)" % LH, "Copyright 2020 The Jost Project Authors; SIL OFL 1.1 text included; no Reserved Font Name declared", "PARTIAL — licence text located",
     "%s/00_source/fonts/jost/OFL.txt; Original_Font_Manifest.json (status WORKING BUILD / VAL-05 AND VAL-19 OPEN)" % LH, "YES — Design Custodian + Legal (deployment uses and exact build)",
     "Licence text is present for the Regular build. Exact final build not frozen/accepted; deployment uses (print, web, app, office, distribution) not verified; 500/700/variable builds not in the repository (ODI01 07_Font_Claim_File_Matrix.csv).", "LICENCE DOCUMENT REQUIRED (for any build beyond the included Regular) + counsel confirmation of uses"],
    ["LI-07", "Font — Inter", "%s/00_source/fonts/inter/Inter-Regular.ttf (Regular 400)" % LH, "Copyright 2020 The Inter Project Authors; SIL OFL 1.1 text included; no Reserved Font Name declared", "PARTIAL — licence text located",
     "%s/00_source/fonts/inter/OFL.txt; Original_Font_Manifest.json" % LH, "YES — Design Custodian + Legal", "As LI-06.", "LICENCE DOCUMENT REQUIRED (for any build beyond the included Regular) + counsel confirmation of uses"],
    ["LI-08", "Font — Noto Sans Arabic", "%s/00_source/fonts/notosansarabic/NotoSansArabic-Regular.ttf (Regular 400)" % LH, "Copyright 2022 The Noto Project Authors; SIL OFL 1.1 text included; no Reserved Font Name declared", "PARTIAL — licence text located",
     "%s/00_source/fonts/notosansarabic/OFL.txt; Original_Font_Manifest.json" % LH, "YES — Design Custodian + Legal", "As LI-06. Arabic family is interim (M02) pending VAL-07.", "LICENCE DOCUMENT REQUIRED (for any build beyond the included Regular) + counsel confirmation of uses"],
    ["LI-09", "Font redistribution", "3 TTF files committed in the public repository; Word templates may embed font stubs", "OFL.txt text accompanies the files; QA report R03-01 notes 'redistributes third-party fonts the package has no recorded right to ship' (outside template control; noted for rights review)", "PARTIAL",
     "%s/05_release/GEM_Letterhead_QA_Report.md line 28; D7 08_Legal_IP_Questions.md Q2" % LH, "YES — Legal / IP Counsel",
     "The file note and the OFL text are not reconciled in the repository. Repository publication does not settle it.", "LEGAL COUNSEL REVIEW REQUIRED"],
    ["LI-10", "Imagery — AI-generated concept", "Amenities_Portfolio_PartD_RC2/01_mockups (15 PNG) and the 31 pictures in Part D", "'All imagery is AI-generated concept imagery' (CHANGE_LOG.md line 16). " + (OWN["imagery"] + "; " if "imagery" in OWN else "Creator/tool not named; ") + "PowerPoint metadata names an export tool only (not provenance)", "NO",
     "Amenities_Portfolio_PartD_RC2/CHANGE_LOG.md lines 14, 16; Register VAL-06 / Y04 (Not started / Evidence Required)", "YES — Art Direction + Legal / IP Counsel",
     "Tool terms / licence record not supplied, no rights register, no source/usage metadata. The images also show GEM label artwork and unreviewed Arabic strings.", "RIGHTS REGISTER REQUIRED"],
    ["LI-11", "Imagery — rendered reference studies", "Part A slides 48, 49, 58, 63 (reference studies) and Part D slides 16-17 materials pictures", "'Rendered reference study' / 'AI-generated … concept' alt wording; generator not recorded", "NO", "Part A/Part D candidate slides", "YES", "Source and rights not recorded; class UNKNOWN unless a file says otherwise.", "RIGHTS REGISTER REQUIRED"],
    ["LI-12", "Imagery — stock / supplier / photographs", "None identified", "Part A rule: avoid generic stock; no supplier imagery found", "n/a", "Searched md/csv/json in qa, PartD, ODI01, AX01", "n/a", "No stock, supplier or photographic assets located; model and property releases not applicable on current evidence.", "NOT APPLICABLE (on repository evidence)"],
    ["LI-13", "Third-party marks / names", "Typeface names listed as reference or legacy only (Part B slide 9); partner/property placeholders ([PROPERTY NAME])", "Reference mentions only", "n/a", "Part B slide 9; Part D slide 12", "YES where any third-party mark is used", "No third-party mark is reproduced as artwork on current evidence; D7 05 lists 'third-party and property marks, partner content: UNKNOWN'.", "OWNER EVIDENCE REQUIRED (confirm none used)"],
    ["LI-14", "Source register coverage", "%s/05_release/GEM_Letterhead_Asset_Source_Register.md" % LH, "Rows only for horizontal ink/black logo files and the three fonts", "PARTIAL", "%s/05_release/GEM_Letterhead_Asset_Source_Register.md lines 9-18" % LH, "n/a",
     "No rows for symbol, stacked, symbol-nospark, 01_svg or 05_layout_matched files; no ownership/licence rows for logos.", "RIGHTS REGISTER REQUIRED"],
    ["LI-15", "Repository terms", "mish3labdul/GEM (public by owner decision OD-G11)", "No LICENSE or NOTICE file; no trademark or brand-use licence declared", "NO", "D7 03_Existing_Public_Exposure.md line 34; evidence/14_license_file_search.txt", "YES — Legal / IP Counsel",
     "Owner visibility approval is not a licence grant or legal opinion.", "LEGAL COUNSEL REVIEW REQUIRED"],
    ["LI-16", "Supplier legal clause", "Part C Appendix B Y06 supplier clause wording", "[LEGAL REVIEW REQUIRED]", "NO", "qa/GEM_V3_RC2_Final_Open_Evidence_Register.md (VAL-11)", "YES", "Outside the eight core gates; tracked under VAL-11 / Y06.", "LEGAL COUNSEL REVIEW REQUIRED"],
]
DISP_H = ["Gate", "Governing definition (Register)", "Owner per Register", "Evidence located (repository)", "Evidence missing", "Queue 4 disposition", "Owner-side evidence pointer given in session", "Governing acceptance condition satisfied?", "Can close now?", "Reason", "Next action"]
DISP = [
    ["VAL-03", "Target-market clearance or documented legal advice; benchmarking is separate from legal clearance", "Legal / IP Counsel", "None", "Legal review or clearance for GEM in target markets", "LEGAL COUNSEL REVIEW REQUIRED", OWN.get("VAL-03", "none given"), "NO", "NO", "No legal review exists; Mashal cannot substitute for Legal / IP Counsel", "Commission trademark/distinctiveness review"],
    ["Y01", "Trademark availability/registration legally reviewed", "Legal / IP Counsel", "None", "As VAL-03", "LEGAL COUNSEL REVIEW REQUIRED", OWN.get("Y01", "none given"), "NO", "NO", "As VAL-03", "As VAL-03"],
    ["VAL-04", "Ownership or assignment/licence evidence retained with the brand archive", "Brand Owner / Legal", "Kit provenance statement only ('received from the project owner')", "Executed ownership or assignment evidence", "OWNER EVIDENCE REQUIRED", OWN.get("VAL-04", "none given"), "NO", "NO", "A provenance statement is not ownership evidence", "Owner supplies creator agreement / assignment; counsel reviews"],
    ["Y02", "Logo artwork ownership documented", "Brand Owner + Legal / IP Counsel", "As VAL-04", "As VAL-04", "OWNER EVIDENCE REQUIRED", OWN.get("Y02", "none given"), "NO", "NO", "As VAL-04", "As VAL-04"],
    ["VAL-05", "Licences support intended print, web, app, office and distribution uses; exact builds tested where needed", "Design Custodian / Legal", "OFL 1.1 text + copyright line for Jost, Inter, Noto Sans Arabic Regular; font manifest with hashes", "Exact final builds frozen/accepted; deployment-use verification; licence documents for any non-Regular build; counsel confirmation of redistribution", "LICENCE DOCUMENT REQUIRED", OWN.get("VAL-05", "none given"), "NO", "NO", "Licence text exists for the Regular builds only; acceptance conditions (exact builds, deployment) are not met; external verification not used", "Freeze builds; obtain licence documents for any further build; counsel confirms uses"],
    ["Y03", "Licences adequate for print/web/app use", "Design Custodian + Legal / IP Counsel", "As VAL-05", "As VAL-05", "LICENCE DOCUMENT REQUIRED", OWN.get("Y03", "none given"), "NO", "NO", "As VAL-05", "As VAL-05"],
    ["VAL-06", "Every approved production image has rights/source/usage metadata", "Art Direction / Legal", "None (imagery recorded as AI-generated concept; no register)", "Rights register with source and usage metadata for every approved production image", "RIGHTS REGISTER REQUIRED", OWN.get("VAL-06", "none given"), "NO", "NO", "No rights register exists; Part D imagery remains concept/reference only", "Build the register; record generation-tool terms; counsel review"],
    ["Y04", "Image/model/property rights documented", "Design Custodian / Art Direction + Legal / IP Counsel", "As VAL-06", "As VAL-06", "RIGHTS REGISTER REQUIRED", OWN.get("Y04", "none given"), "NO", "NO", "As VAL-06", "As VAL-06"],
]
with open(PKG / "09_HR01_Legal_IP_Evidence_Inventory.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(INV_H)
    w.writerows(INV)
with open(PKG / "10_HR01_Legal_IP_Disposition_Register.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(DISP_H)
    w.writerows(DISP)
print("inventory", len(INV), "dispositions", len(DISP))
