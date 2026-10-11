#!/usr/bin/env python3
"""FA01 registers: 04 final owner decisions, 05b gate disposition, 09 AC20 acceptance test, 10 release scope matrix.

Run from the repository root:
  python3 -I GEM_V3.0_FA01_Final_Release_Authorization/14_scripts/fa01_build_registers.py [--authorized]

Without --authorized the AC20 decision stays PROPOSED / OPEN (the state before the Brand Owner's explicit yes). With --authorized the AC20
rows read as authorized. Nothing here records a gate as CLOSED BY EVIDENCE; unperformed work is never called PASS.
Baseline file hashes are computed from the files; relative paths only.
"""
import csv
import hashlib
import sys
from pathlib import Path

AUTH = "--authorized" in sys.argv
PKG = Path("GEM_V3.0_FA01_Final_Release_Authorization")
EM = "—"
HR = Path("GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/18_candidate_corrections")
sha12 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # full sha256
OWNER = "Brand Owner: Mashal (as typed by the owner; no surname, title, signature, employer or legal entity added)"
STATE = ("AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS" if AUTH else "PROPOSED — AC20 STAYS OPEN UNTIL THE BRAND OWNER'S EXPLICIT CONFIRMATION")


def write(name, header, rows):
    with open(PKG / name, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def hr(name):
    return "%s (sha256 %s)" % (name, sha12(HR / name))


F = {
    "A": "GEM Brand Guidelines V3.0 %s Part A %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM),
    "B": "GEM Digital Design System V3.0 %s Part B %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM),
    "C": "GEM Production Standards V3.0 %s Part C %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM),
    "D": "GEM Amenities & Packaging %s Concept Product Portfolio V3.0 %s Part D %s RC2 %s HR01 CANDIDATE (UNAPPROVED).pptx" % (EM, EM, EM, EM),
}
W = {n: "GEM_Letterhead_%s_HR01_CANDIDATE.docx" % n for n in ("Arabic_First_Page", "Arabic_Continuation", "Bilingual_First_Page", "Bilingual_Continuation")}
LHD = Path("GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates")
ENG = {n: "GEM_Letterhead_%s.docx" % n for n in ("English_First_Page", "English_Continuation", "Executive", "Minimal")}
KIT = Path("GEM_Brand_Assets_v1.0/04_official_kit/SHA256SUMS.txt")
TOK = Path("PartB_RC2/05_release/tokens")

# ------------------------------------------------------------------ 04 final owner decisions
D_H = ["Decision ID", "Owner", "Selection (exact)", "Scope", "Effective status", "Affected gates", "Residual limitation", "Release effect", "Constitutes evidence verification?", "Amends prior governance?"]
DEC = [
    ["FA-A", OWNER, "A3 — Limited release baseline", "AC20 only; the GEM™ V3.0 baseline defined in 10", "RECORDED (owner selection)",
     "AC20; all gates dispositioned in 05b", "Everything formally deferred or excluded stays unperformed or unaccepted", "Release is a controlled final brand-system baseline with explicit artifact-specific exclusions; nothing unperformed is called PASS",
     "NO", "YES — narrowly: a superseding AC20 release-disposition rule (see 05); the Approval Register text is preserved"],
    ["FA-B", OWNER, "Mashal — Role: Brand Owner; Authority: Final brand governance and AC20 release authorization", "Canonical Brand Owner holder (Register role 'Brand Owner')", "RECORDED",
     "AC19; AC20", "Same person also holds the Arabic / Localization Lead role (OD-G09) and the Accessibility Content Owner working role (OD-G10); no independent verification exists in this chain",
     "Satisfies the Register's 'named Brand Owner' condition for AC20; does not close AC19", "NO", "YES — replaces the earlier statements that Mashal was not linked to the Brand Owner role (OD01) and that the two sources were not asserted to be the same person (FD01); those files are not edited"],
    ["FA-C", OWNER, "C2 — Narrow D8", "External issue of Arabic/bilingual DOCX/PDF", "RECORDED",
     "D8; SR-11; SR-12; VAL-07; VAL-08; VAL-15", "Windows Word, Word Online, Acrobat and NVDA/JAWS tests remain unperformed", "Internal controlled use authorized; external issue of affected Arabic/bilingual DOCX/PDF stays blocked pending D8 validation; unaffected artifacts eligible",
     "NO", "YES — clarifies the ODI01 D8 rule; the internal-use marking condition is carried forward unchanged"],
    ["FA-E", OWNER, "Yes — the independent legal-clearance requirement is waivable by the Brand Owner, accepted as owner risk under formal deferral (never recorded as verified or cleared)", "VAL-03 / Y01 and VAL-04 / Y02 (and the same treatment for VAL-05 / Y03, VAL-06 / Y04 under FD01)", "RECORDED",
     "VAL-03; Y01; VAL-04; Y02", "No legal clearance, trademark verification or ownership verification exists or is claimed", "These gates are OWNER ACCEPTED UNDER FORMAL DEFERRAL for release purposes", "NO",
     "YES — overrides, for AC20 only, the Register's approver (Legal / IP Counsel for VAL-03 / Y01; Brand Owner / Legal for VAL-04 / Y02); disclosed in 05"],
    ["FA-F1", OWNER, "Formally defer all four: AC07, AC10, AC17, VAL-01", "Brand-Owner gates not covered by FD01", "RECORDED",
     "AC07; AC10; AC17; VAL-01", "No accepted logo master, no Arabic system approval, no approved production specifications, no signed commercial scope", "Outside the authorized baseline scope until revisited (the Register's own rule for deferred items)", "NO", "YES — AC10 uses the Register's 'formally defer' route; the others are deferrals by owner decision"],
    ["FA-F2", OWNER, "Formally defer each: VAL-09, 10, 11, 13, 14, 15, 16, 17, 19, 20, 21, OD-SRC, OD-TPL and the unfinished parts of VAL-07 and VAL-08", "Evidence and work gates not covered by FD01", "RECORDED",
     "As listed", "Packaging/supplier proof, digital components, final deliverables, release manifest, usability test, cross-document sign-off, templates and typography QA are not done", "The artifacts that depend on them are restricted (see 10)", "NO", "YES — deferral by owner decision"],
    ["FA-G", OWNER, "HR01 candidates + kit + tokens", "The files that constitute 'GEM™ V3.0' for AC20", "RECORDED",
     "AC20; VAL-16 (no release manifest exists; the FA01 manifest is not one)", "Visible labels in the files still read working edition / not released / AC20 pending until a separate promotion and relabel pass; file names still say RC2 / HR01 CANDIDATE (UNAPPROVED)",
     "Defines the baseline by path and hash", "NO", "NO"],
    ["FA-H", OWNER, ("VAL-02 (production logo master verification) — formally deferred together with AC07; confirmed by the owner in the AC20 confirmation" if AUTH else "VAL-02 (production logo master verification) — not named in the owner's list; proposed as deferred together with AC07, pending the owner's confirmation"), "VAL-02", "PENDING OWNER CONFIRMATION" if not AUTH else "CONFIRMED IN THE AC20 CONFIRMATION",
     "VAL-02; AC07", "Logo kit stays WORKING ASSETS; production-master acceptance PENDING", "Logo kit is a baseline asset but not labelled or released as a production master", "NO", "NO"],
    ["FA-AC20", OWNER, "AC20 " + STATE, "AC20 final Brand Owner release authorization", "AUTHORIZED" if AUTH else "PROPOSED — NOT YET GIVEN",
     "AC20", "See 11", "GEM™ V3.0 controlled final brand-system baseline (State 2: limited release)" if AUTH else "None until the explicit yes", "NO", "NO"],
]
write("04_FA01_Final_Owner_Decisions.csv", D_H, DEC)

# ------------------------------------------------------------------ 05b gate disposition
G_H = ["Gate / item", "Register status or prior state", "FA01 disposition", "Decided by", "Evidence level", "Closed by evidence?", "Release effect"]
FD = "FD01 (FD-G01)"
DEF_NOTE = "Outside the authorized scope until revisited"
GATES = [
    ["VAL-01", "In progress", "FORMALLY DEFERRED", "FA-F1", "n/a", "NO", "No signed commercial scope in the baseline"],
    ["VAL-02", "Not started (kit received; acceptance pending)", "FORMALLY DEFERRED — " + ("CONFIRMED IN AC20 CONFIRMATION" if AUTH else "PENDING OWNER CONFIRMATION"), "FA-H (with AC07)", "n/a", "NO", "Logo kit stays WORKING ASSETS; not a production master"],
    ["VAL-03", "Not started", "OWNER ACCEPTED UNDER FORMAL DEFERRAL (offline owner-declared evidence; independent verification not performed)", FD + " + FA-E", "OWNER DECLARED", "NO", "No legal clearance claimed"],
    ["VAL-04", "Not started", "OWNER ACCEPTED UNDER FORMAL DEFERRAL", FD + " + FA-E", "OWNER DECLARED", "NO", "No ownership verification claimed"],
    ["VAL-05", "In progress", "OWNER ACCEPTED UNDER FORMAL DEFERRAL (repository OFL text for three Regular builds; exact-build and deployment acceptance deferred)", FD, "PARTIALLY VERIFIED", "NO", "Fonts: working builds only"],
    ["VAL-06", "Not started", "OWNER ACCEPTED UNDER FORMAL DEFERRAL / DIGITAL TERMS REVIEW DEFERRED", FD, "OWNER DECLARED (provenance statement)", "NO", "Part D stays concept; no production image approved"],
    ["VAL-07", "Not started", "OPEN — unfinished parts FORMALLY DEFERRED (production RTL layouts with real content; Windows; candidate promotion)", "FA-F2 + FD-G03", "REVIEWER OBSERVED (macOS) + human linguistic review; not independently verified", "NO", "Arabic/bilingual external issue restricted (D8, C2)"],
    ["VAL-08", "In progress", "OPEN — unfinished parts FORMALLY DEFERRED (contrast over pictures, independent QA, Windows, PDF, formal exceptions)", "FA-F2 + FD-G03/G04", "REVIEWER OBSERVED (macOS); no conformance claim", "NO", "No WCAG certification or conformance claim"],
    ["VAL-09", "Not started", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No production packaging authorized"],
    ["VAL-10", "Not started", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No regulated packaging/claims authorized"],
    ["VAL-11", "Not started", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No supplier acceptance"],
    ["VAL-12", "Deferred (Register status; S02)", "DEFERRED (Register)", "Register", "n/a", "NO", "Wayfinding fabrication outside scope"],
    ["VAL-13", "In progress", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No component implementation authorized"],
    ["VAL-14", "In progress", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No motion masters authorized"],
    ["VAL-15", "Not started", "FORMALLY DEFERRED", "FA-F2 + FD-G04", "Partial (open/render only)", "NO", "No final deliverables; PDFs not authorized"],
    ["VAL-16", "Not started", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No release manifest exists; the FA01 manifest is not one"],
    ["VAL-17", "Not started", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No usability test"],
    ["VAL-18", "NOT ALLOCATED", "NOT ALLOCATED (no such gate)", "Register", "n/a", "n/a", "None"],
    ["VAL-19", "In progress", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "Fonts: working builds only"],
    ["VAL-20", "Not started", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No locale/responsive implementation"],
    ["VAL-21", "Not started", "FORMALLY DEFERRED", "FA-F2", "112 automated assertions pass (not a sign-off)", "NO", "No formal cross-document sign-off"],
    ["Y01", "Evidence Required", "OWNER ACCEPTED UNDER FORMAL DEFERRAL", FD + " + FA-E", "OWNER DECLARED", "NO", "No trademark clearance claimed"],
    ["Y02", "Evidence Required", "OWNER ACCEPTED UNDER FORMAL DEFERRAL", FD + " + FA-E", "OWNER DECLARED", "NO", "No ownership verification claimed"],
    ["Y03", "Evidence Required", "OWNER ACCEPTED UNDER FORMAL DEFERRAL", FD, "PARTIALLY VERIFIED", "NO", "Fonts: working builds only"],
    ["Y04", "Evidence Required", "OWNER ACCEPTED UNDER FORMAL DEFERRAL / DIGITAL TERMS REVIEW DEFERRED", FD, "OWNER DECLARED (provenance statement)", "NO", "Part D stays concept"],
    ["AC07", "Evidence Required", "FORMALLY DEFERRED", "FA-F1", "n/a", "NO", "No accepted master artwork in the baseline"],
    ["AC10", "Evidence Required", "FORMALLY DEFERRED (Register 'formally defer' route)", "FA-F1", "Human linguistic review (Mashal); not independently verified", "NO", "No Arabic system approval"],
    ["AC17", "Evidence Required", "FORMALLY DEFERRED", "FA-F1", "n/a", "NO", "No approved production specifications"],
    ["AC19", "OPEN / HOLDER CONDITION INCOMPLETE (FD01: FORMALLY DEFERRED)", "OPEN — FORMALLY DEFERRED / OWNER ACCEPTED FOR RELEASE (2 of 12 canonical roles named; 10 unnamed)", "FD-G02 + FA-B", "n/a", "NO", "Role matrix incomplete"],
    ["AC20", "OPEN / FINAL RELEASE AUTHORIZATION PENDING", STATE, "FA-AC20", "n/a", "n/a", "See 02"],
    ["OD-TPL", "Open deliverable", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No templates beyond the working letterheads"],
    ["OD-SRC", "Open", "FORMALLY DEFERRED", "FA-F2", "n/a", "NO", "No component source or Storybook"],
    ["D8", "OPEN — FORMALLY DEFERRED", "NARROWED (C2): internal controlled use authorized; external issue of affected Arabic/bilingual DOCX/PDF restricted pending D8 validation", "FA-C", "n/a", "NO", "Enforceable file list in 10"],
    ["SR-11", "FORMALLY DEFERRED", "FORMALLY DEFERRED (not performed)", "FD-G04", "n/a", "NO", "No PDF result claimed"],
    ["SR-12", "FORMALLY DEFERRED", "FORMALLY DEFERRED (not performed)", "FD-G03", "n/a", "NO", "No Windows result claimed"],
]
write("05b_FA01_Gate_Disposition_Register.csv", G_H, GATES)

# ------------------------------------------------------------------ 09 acceptance test
T_H = ["#", "Test", "Result", "Basis"]
pf = "PASS WITH FORMAL DEFERRAL"
T = [
    [1, "Owner identity established?", "PASS", "The owner supplied the exact holder name 'Mashal' (role Brand Owner). It is recorded verbatim; no further identification exists or is claimed (FA-B)"],
    [2, "Owner release decision explicit?", "PASS" if AUTH else "NOT YET — explicit yes/no pending", "A3 was selected as the deferral treatment; the AC20 authorization itself needs a separate explicit yes (FA-AC20)" + (" — given" if AUTH else "")],
    [3, "All unresolved items closed by evidence, formally deferred, or explicitly excluded?", pf, "05b: 0 closed by evidence; every Register gate and the D8 rule are formally deferred, owner-accepted under formal deferral, or Register-Deferred; VAL-02 is covered by FA-H"],
    [4, "No non-waivable gate falsely bypassed?", pf, "Legal/IP approver overridden for AC20 only by explicit owner decision FA-E and disclosed; no gate is recorded as passed; no gate was identified as non-waivable by the owner"],
    [5, "D8 treatment explicit?", "PASS", "C2 narrowed D8; enforceable file list in 10 and policy text in 07"],
    [6, "Legal/IP limitation explicit?", pf, "OWNER ACCEPTED UNDER FORMAL DEFERRAL; offline hard copies owner-declared; no verification or clearance claimed (04, 11)"],
    [7, "AC19 treatment explicit?", pf, "OPEN — FORMALLY DEFERRED / OWNER ACCEPTED FOR RELEASE; 2 of 12 canonical roles named (08)"],
    [8, "Release scope defined?", "PASS", "10 names the baseline files by path and hash and states eligibility per artifact"],
    [9, "Candidate/working files distinguished from release artifacts?", pf, "The baseline is made of unpromoted HR01 candidates whose visible labels still read working edition / not released; promotion and relabel are a separate change not made here (FA-G, 10)"],
    [10, "Residual limitations disclosed?", "PASS", "11"],
    [11, "Historical evidence preserved?", "PASS", "QA verifies AR01, AX01, OD01, HR01, FD01 and the Approval Register are unchanged"],
    [12, "No false WCAG / legal / IP claims?", "PASS", "QA scans every FA01 file; macOS VoiceOver is recorded as reviewer observed only"],
    [13, "Release naming/version defined?", "PASS", "GEM™ V3.0 — OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE — FORMAL DEFERRALS RECORDED — ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY; file names keep RC2 / HR01 CANDIDATE until promotion"],
    [14, "Owner accepts residual risk?", "PASS" if AUTH else "NOT YET — pending the explicit yes", "FD-G05 accepted the RC2 state as-is; FA01 decisions A3, C2, E, F1, F2 accept the further limitations; the final yes confirms the complete list"],
    [15, "AC20 authority valid under current governance?", pf if AUTH else "NOT YET", "Valid only through the narrow superseding AC20 rule (05) and the named Brand Owner holder; the Register text is preserved; the same person authorizes the release and produced all human evidence (11)"],
]
write("09_FA01_AC20_Acceptance_Test.csv", T_H, T)

# ------------------------------------------------------------------ 10 release scope matrix
S_H = ["Artifact / stream", "Baseline file(s) and hash", "Current evidence status", "Deferral", "Owner acceptance", "Release eligible (baseline member)?", "Internal use eligible?", "External issue eligible?", "Restriction", "Notes"]
LAB = "Visible labels (WORKING EDITION / NOT RELEASED / AC20 PENDING) must be removed by a separate promotion and relabel pass before external issue; not done in FA01"
S = [
    ["Part A Brand Guidelines", hr(F["A"]), "Native checker: no missing alt text or title; macOS VoiceOver reviewer observed; 112 assertions pass; Arabic strings reviewed by Mashal", "Windows, PDF, Legal/IP, AC07, AC10", "YES (FD-G05, FA01)", "YES", "YES", "NOT YET", LAB + ". Arabic slides 37, 38, 39, 65, 66, 68: no external DOCX/PDF of those pages (D8, C2)", "Unpromoted candidate"],
    ["Part B Digital Design System", hr(F["B"]), "As Part A; Arabic specimen on slide 9", "Windows, PDF, OD-SRC, VAL-13, VAL-20", "YES", "YES", "YES", "NOT YET", LAB, "Specification only; no component implementation exists"],
    ["Part C Production Standards", hr(F["C"]), "As Part A; no Arabic content", "VAL-09, 10, 11, OD-TPL, AC17", "YES", "YES", "YES", "NOT YET", LAB + ". Supplier values and templates are pending", "Unpromoted candidate"],
    ["Part D Amenities Concept Portfolio", hr(F["D"]), "CONCEPT / NOT PRODUCTION ARTWORK; AI-generated imagery (owner-declared provenance); Arabic strings inside images not approved", "VAL-06, Y04, VAL-09, 10, 11", "YES", "YES (as a concept portfolio only)", "YES", "NOT YET", "Remains CONCEPT / NOT PRODUCTION ARTWORK; not production artwork; " + LAB, "Not promoted by AC20"],
    ["Official Logo Kit", "GEM_Brand_Assets_v1.0/04_official_kit (file hashes in its SHA256SUMS.txt, sha256 %s)" % sha12(KIT), "WORKING ASSETS; acceptance as production master PENDING", "VAL-02 (" + ("confirmed" if AUTH else "pending owner confirmation") + "), AC07, VAL-03/04, Y01/02", "YES", "YES (as baseline asset)", "YES", "RESTRICTED", "Not labelled or released as a production master; ownership/clearance claims not made", "Kit status text says WORKING ASSETS"],
    ["Production vectors (kit SVG/EPS/PDF masters)", "As the Official Logo Kit", "Unaccepted vectors; no-spark micro mark pending", "VAL-02, AC07", "YES", "NO as production masters", "YES (working use)", "NO as production masters", "Not production masters until VAL-02 / AC07 are satisfied", ""],
    ["Letterhead Set (overall)", "GEM_Letterhead_Set_v1.1_Application_Revision_03 (8 templates; the 4 changed ones are replaced by the HR01 candidates below)", "Working application; pending validation", "VAL-15, OD-TPL, D8", "YES", "YES (as working application)", "YES", "NOT YET", "Markers 'WORKING APPLICATION / PENDING VALIDATION' remain until a separate pass", ""],
    ["Arabic First Page letterhead", hr(W["Arabic_First_Page"]), "Word checker: no issues; macOS VoiceOver reviewer observed; Arabic wording reviewed by Mashal", "D8 tests (Windows Word, Word Online, Acrobat, NVDA/JAWS)", "YES", "YES (internal working only)", "YES — with the D8 markings on every page", "NO", "AFFECTED BY D8: no external issue as DOCX or PDF", "Internal marking condition carried forward unchanged"],
    ["Arabic Continuation letterhead", hr(W["Arabic_Continuation"]), "As above", "As above", "YES", "YES (internal working only)", "YES — with D8 markings", "NO", "AFFECTED BY D8", ""],
    ["Bilingual First Page letterhead", hr(W["Bilingual_First_Page"]), "As above", "As above", "YES", "YES (internal working only)", "YES — with D8 markings", "NO", "AFFECTED BY D8", ""],
    ["Bilingual Continuation letterhead", hr(W["Bilingual_Continuation"]), "As above", "As above", "YES", "YES (internal working only)", "YES — with D8 markings", "NO", "AFFECTED BY D8", ""],
    ["English letterheads (First Page, Continuation, Executive, Minimal)", "; ".join("%s (sha256 %s)" % (v, sha12(LHD / v)) for v in ENG.values()), "Unchanged Revision 03; Word checker: no issues (AX01); no Arabic text", "OD-TPL, VAL-15", "YES", "YES", "YES", "NOT YET", "Working-application markers remain until a separate pass; not affected by D8", ""],
    ["Digital components", "%s (sha256 %s), %s (sha256 %s)" % ("gem-tokens.v3.0-rc2.json", sha12(TOK / "gem-tokens.v3.0-rc2.json"), "gem-tokens.v3.0-rc2.css", sha12(TOK / "gem-tokens.v3.0-rc2.css")), "Derived token package (153 tokens); no component source or Storybook", "OD-SRC, VAL-13, VAL-20", "YES", "YES (tokens as documentation)", "YES", "NOT YET", "No component library or implementation is authorized; token file names still say rc2", ""],
    ["Packaging concepts", "Part D slides; Part A slide 62 (concept)", "Concept only", "VAL-09, VAL-10, VAL-11", "YES", "YES (as concepts)", "YES", "NO", "No production packaging, regulated claims or supplier acceptance", ""],
    ["PDF release artifacts", "None in the baseline (no PDF was generated by HR01 or FA01)", "Not performed", "SR-11, D8, VAL-15", "YES", "n/a", "Existing review PDFs only under D8 marking", "NO", "No PDF is authorized for external issue; Arabic/bilingual PDFs are AFFECTED BY D8", "Historical RC2 review PDFs are not part of the baseline"],
    ["Windows accessibility scope", "n/a (not performed)", "Not tested", "SR-12", "YES", "n/a", "n/a", "n/a", "No Windows or cross-platform accessibility claim", ""],
    ["macOS VoiceOver evidence", "GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/07, 08", "REVIEWER OBSERVED — MASHAL; 11 tests PASS for the defined scope", "None", "YES", "n/a", "n/a", "n/a", "Not independent verification; not a WCAG certification", "Same person is Brand Owner, reviewer and content owner"],
    ["Legal/IP stream", "No digital copy (offline, owner-declared)", "OWNER DECLARED; independent verification NOT PERFORMED", "VAL-03, 04, 05 (part), 06; Y01–Y04", "YES (owner accepted under formal deferral)", "n/a", "n/a", "n/a", "No legal clearance, trademark or ownership verification claimed", "No upload is to be requested"],
]
write("10_FA01_Release_Scope_Matrix.csv", S_H, S)
print("authorized" if AUTH else "proposed", "| decisions", len(DEC), "gates", len(GATES), "tests", len(T), "scope rows", len(S))
