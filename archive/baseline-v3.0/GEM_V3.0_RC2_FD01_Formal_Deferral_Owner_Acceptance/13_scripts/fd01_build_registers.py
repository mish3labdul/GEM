#!/usr/bin/env python3
"""FD01 registers: 02 owner decisions, 03 formal deferrals, 08 gate impact, 09 remaining evidence after deferral.

Run from the repository root:  python3 -I GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance/13_scripts/fd01_build_registers.py
Status model (never collapsed): VERIFIED = evidence inspected against the acceptance requirement; OWNER DECLARED = owner confirms evidence/status, not
independently inspected; FORMALLY DEFERRED = required review/testing postponed by authorized decision; OWNER ACCEPTED = Brand Owner accepts the resulting
limitation; CLOSED = the Register acceptance condition is actually satisfied. No gate is CLOSED by FD01. No confidential document was requested or read.
"""
import csv
from pathlib import Path

PKG = Path("GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance")
OWNER = "Brand Owner (no individual name or signature supplied)"
DECL = ("Relevant Legal/IP supporting documentation is retained offline in hard copy according to Brand Owner declaration. The Brand Owner has intentionally "
        "elected not to upload or reproduce those documents in the GEM repository or internet-connected review environment. Independent digital evidence "
        "verification is therefore formally deferred.")


def write(name, header, rows):
    with open(PKG / name, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


# ------------------------------------------------------------------ 02 owner decisions
OD_H = ["Decision ID", "Title", "Owner", "Status", "Decision", "Scope", "Affected gates", "Evidence basis", "What the decision does", "What the decision does NOT do", "Remaining limitation"]
OD = [
    ["FD-G01", "Legal/IP offline evidence confidentiality and digital-review deferral", OWNER, "OWNER ACCEPTED / DIGITAL REVIEW FORMALLY DEFERRED",
     "Relevant Legal/IP documentation is retained offline in hard copy by the Brand Owner. The Brand Owner has elected not to upload, digitize, reproduce or retain those confidential documents in the GEM repository or any internet-connected review environment. Digital review and independent verification are formally deferred.",
     "Confidential Legal/IP supporting documents (trademark, logo ownership, image/tool terms records); not font licence texts already in the repository",
     "VAL-03; Y01; VAL-04; Y02; VAL-06; Y04 (and the deployment-licence part of VAL-05; Y03)",
     "Brand Owner declaration in the FD01 instruction (Legal/IP documentation retained offline in hard copy). Recorded separately: statements given in the HR01 session by the session user answering as Mashal and logged in HR01 as owner-side pointers (a trademark document exists in hard copy; a logo ownership document exists outside the repository; image generation: 'myself, using ChatGPT image generation'). The two sources are cited as given and are not asserted to be the same person. No document was supplied, requested or inspected.",
     "Records evidence existence as DECLARED BY BRAND OWNER; digital copy NOT PROVIDED BY OWNER DECISION; repository retention NOT REQUIRED; digital review FORMALLY DEFERRED; owner acceptance YES (as-is).",
     "Does not record that no evidence exists. Does not record Legal/IP cleared, trademark verified or ownership independently verified. Does not close any gate. Does not mean Claude inspected the documents. Not a legal opinion.",
     "Independent verification not performed; the Register criteria that require legal review or advice remain unmet."],
    ["FD-G02", "Remaining governance-role assignment deferral", OWNER, "FORMALLY DEFERRED BY BRAND OWNER",
     "Completion of the remaining canonical governance role holders is postponed. Known canonical holder: Mashal, Arabic / Localization Lead. OD-G10 (Accessibility Content Owner / Brand Content Owner) remains a working authority and does not populate another canonical role.",
     "Approval Register 'Owners & Governance' roles (12); AC19", "AC19", "Brand Owner instruction; HR01 gate matrix (1 of 12 canonical roles named)",
     "Records AC19 as FORMALLY DEFERRED / HOLDER COMPLETION POSTPONED BY BRAND OWNER (not failed).",
     "Does not invent any role holder, does not name the Brand Owner, does not close AC19. The Register states holders must be recorded before AC20 final release authorization.",
     "11 canonical holders (including the Brand Owner) remain unnamed."],
    ["FD-G03", "Windows-native accessibility validation deferral", OWNER, "FORMALLY DEFERRED BY BRAND OWNER",
     "Windows-native assistive-technology validation (SR-12: NVDA / JAWS, Windows Word and Word Online) was not performed. It is outside the available environment and is postponed.",
     "SR-12; Windows-side parts of VAL-07 / VAL-08", "SR-12; VAL-07; VAL-08", "HR01 test register (SR-12 DEFERRED); no Windows environment",
     "Replaces the earlier content-owner deferral of SR-12 with a Brand Owner formal deferral. Preserves macOS VoiceOver evidence: COMPLETED / PASS FOR DEFINED SCOPE.",
     "Does not claim full cross-platform accessibility verification, WCAG 2.2 AA certification or any Windows result. Does not invalidate the macOS evidence.",
     "Windows-native behaviour untested."],
    ["FD-G04", "PDF / D8 validation deferral", OWNER, "FORMALLY DEFERRED BY BRAND OWNER",
     "PDF/Acrobat validation (SR-11 and D8) is postponed. No PDF artifact is generated in FD01.",
     "SR-11; D8; PDF parts of VAL-15 / VAL-08", "SR-11; D8; VAL-15; VAL-08", "HR01 test register (SR-11 DEFERRED — D8)",
     "Records D8 as FORMALLY DEFERRED BY BRAND OWNER; PDF/Acrobat validation NOT PERFORMED.",
     "Does not mark D8 or SR-11 PASS, does not fabricate PDF results, and does not lift the D8 operating rule: external issue of Arabic/bilingual DOCX/PDF remains blocked until the native tests pass, unless the Brand Owner separately amends that rule.",
     "Arabic/bilingual DOCX/PDF stay INTERNAL WORKING ONLY."],
    ["FD-G05", "Owner acceptance of current RC2 as-is", OWNER, "APPROVED",
     "The Brand Owner accepts the current GEM™ V3.0 RC2 system as-is at the present governance stage, including the documented limitations and formal deferrals (Legal/IP digital verification, remaining role assignments, Windows-native accessibility validation, PDF/D8 validation).",
     "The GEM\u2122 V3.0 RC2 system as it stands, for continued controlled use and development. It does not promote any candidate or remove any UNAPPROVED marking", "All gates touched by FD-G01..FD-G04 (none closed)", "Brand Owner instruction",
     "The current RC2 state is acceptable to the Brand Owner for continued controlled use and development.",
     "Does not mean approved V3.0, final release, production release, legal clearance or WCAG certification. Does not authorize release (AC20 OPEN). Does not address the other open gates not named in FD01.",
     "Gates and deliverables outside FD01 remain open (see 09)."],
    ["FD-G06", "Offline confidential-evidence policy", OWNER, "APPROVED",
     "Sensitive or confidential Legal/IP evidence may remain entirely offline. Evidence references such as 'OFFLINE HARD-COPY EVIDENCE RETAINED BY BRAND OWNER' are permitted without repository inclusion. Where evidence is intentionally withheld: do not request repeated uploads; do not treat absence from the repository as proof the evidence does not exist; do not expose confidential documents merely for Git traceability; record the owner declaration and the resulting verification limitation.",
     "Confidential supporting evidence only", "VAL-03; VAL-04; VAL-06; Y01; Y02; Y04", "Brand Owner instruction",
     "Allows owner-declared offline evidence references; stops further upload requests.",
     "Does not permit fabrication of evidence status and does not make owner-declared evidence 'verified'.",
     "Traceability for those items rests on the owner's declaration."],
]
write("02_FD01_Owner_Decision_Register.csv", OD_H, OD)

# ------------------------------------------------------------------ 03 formal deferrals
DF_H = ["Deferral ID", "Workstream", "Gates / tests affected", "Deferred by", "Basis", "What is deferred", "What is NOT deferred or changed", "Operational effect", "Reopening trigger", "Evidence existence", "Verification", "Owner acceptance"]
DF = [
    ["FD-D01", "Legal/IP digital evidence review", "VAL-03; Y01; VAL-04; Y02; VAL-06; Y04; deployment-licence acceptance of VAL-05 / Y03", OWNER,
     "Confidentiality and security; documents retained offline in hard copy (FD-G01, FD-G06)", "Digital review and independent verification of the offline documents; digital terms review for the image-generation tool",
     "Font licence texts already in the repository (HR01 findings preserved); the gates themselves stay open; no legal opinion exists or is claimed", "None for controlled use and development; no confidential document is requested again",
     "The Brand Owner chooses to make the documents available for review, or commissions counsel review, or the AC20 decision requires it", "DECLARED BY BRAND OWNER (offline hard copy)", "NOT PERFORMED", "YES — AS-IS"],
    ["FD-D02", "Governance role completion", "AC19", OWNER, "Brand Owner decision (FD-G02)", "Naming the remaining 11 canonical role holders, including the Brand Owner",
     "The one named holder (Mashal, Arabic / Localization Lead); the Register rule that holders be recorded before AC20 authorization", "Existing decisions continue to be recorded as 'Brand Owner (no name supplied)'",
     "AC20 decision; or the owner names holders", "n/a", "NOT PERFORMED", "YES — AS-IS"],
    ["FD-D03", "Windows-native accessibility validation", "SR-12", OWNER, "No Windows environment; Brand Owner decision (FD-G03)", "NVDA / JAWS testing and Windows Word / Word Online validation",
     "macOS VoiceOver evidence (HR01: 11 PASS, reviewer observed) is preserved", "Windows behaviour is untested; no Windows claim is made", "A Windows environment becomes available, or AC20 decision requires it", "n/a", "NOT PERFORMED", "YES — AS-IS"],
    ["FD-D04", "PDF / Acrobat validation", "SR-11; D8", OWNER, "Brand Owner decision (FD-G04); no PDF regenerated", "Tagged-PDF reading order, Arabic text layer and Acrobat checks",
     "The D8 operating rule (internal working use only; external issue blocked until native tests pass) is unchanged", "Arabic/bilingual DOCX/PDF remain internal working only", "An external PDF issue is planned, or AC20 decision requires it", "n/a", "NOT PERFORMED", "YES — AS-IS"],
]
write("03_FD01_Formal_Deferral_Register.csv", DF_H, DF)

# ------------------------------------------------------------------ 08 gate impact
G_H = ["Gate / test", "Register acceptance requirement", "Previous status (HR01)", "FD01 decision impact", "New governance status", "Evidence level", "Digital evidence retained", "Independent verification", "Owner acceptance", "Is deferral a governing disposition?", "Can close?", "Reason"]
EXT = "NOT PERFORMED"
LEGAL_TERM = "Formal deferral is a recognised Register status (the Validation Status list includes 'Deferred'; VAL-12 is Deferred) and OD-G12 allows 'formally deferred by authorized owners'; the Register instructions also say a deferred item stays outside approved V3.0 scope until revisited and not to authorize AC20 while critical gates are open. The AC20 decision must resolve this tension explicitly."
GATES = [
    ["VAL-03", "Target-market clearance or documented legal advice; benchmarking is separate from legal clearance", "Not started; owner pointer to hard-copy document, not reviewed",
     "FD-G01 defers digital review; evidence existence declared by the Brand Owner", "OPEN — EXTERNAL VERIFICATION NOT PERFORMED; digital review FORMALLY DEFERRED; OWNER ACCEPTED",
     "OWNER DECLARED (offline); not inspected", EXT, "YES — AS-IS", LEGAL_TERM + " The criterion explicitly requires independent legal clearance or documented legal advice.", "NO",
     "An owner declaration is not clearance or legal advice; the document type, issuer and scope are unknown to the project; the criterion calls for independent review."],
    ["Y01", "Trademark availability/registration legally reviewed (owner: Legal / IP Counsel)", "Evidence Required; pointer only", "As VAL-03", "OPEN — EXTERNAL VERIFICATION NOT PERFORMED; FORMALLY DEFERRED; OWNER ACCEPTED",
     "OWNER DECLARED (offline); not inspected", EXT, "YES — AS-IS", LEGAL_TERM, "NO", "As VAL-03."],
    ["VAL-04", "Ownership or assignment/license evidence is retained with the brand archive", "Not started; owner pointer to a document outside the repository, not reviewed",
     "FD-G01 / FD-G06: evidence retained offline by the Brand Owner; no repository retention required", "OPEN — OWNER ACCEPTED (owner-declared offline evidence; digital verification FORMALLY DEFERRED)",
     "OWNER DECLARED (offline); not inspected", EXT, "YES — AS-IS", LEGAL_TERM + " The wording 'retained with the brand archive' does not require a digital copy; whether an offline archive satisfies it, and whether the held document is ownership or assignment evidence, is for the Brand Owner / Legal to accept.", "NO",
     "No acceptance of sufficiency by the Register's owner (Brand Owner / Legal) is recorded; the owner has accepted the as-is state, which is not the same as accepting the document as satisfying the criterion."],
    ["Y02", "Logo artwork ownership documented (owner: Brand Owner + Legal / IP Counsel)", "Evidence Required; pointer only", "As VAL-04", "OPEN — OWNER ACCEPTED; digital verification FORMALLY DEFERRED",
     "OWNER DECLARED (offline); not inspected", EXT, "YES — AS-IS", LEGAL_TERM, "NO", "As VAL-04."],
    ["VAL-05", "Licenses support intended print, web, app, office and distribution uses; exact builds tested where needed", "In progress; OFL 1.1 text located for three Regular builds (inspected in HR01)",
     "No change from the confidentiality decision (fonts are not confidential). Deployment-licence acceptance beyond the repository OFL text is deferred under FD-G05", "OPEN — OWNER ACCEPTED; exact-build and deployment-licence acceptance FORMALLY DEFERRED",
     "PARTIALLY VERIFIED (repository OFL text inspected; acceptance requirement not met)", "NOT PERFORMED (no external verification used)", "YES — AS-IS", LEGAL_TERM, "NO",
     "Exact final builds are not frozen/accepted and deployment uses are not verified; HR01 findings are preserved unchanged."],
    ["Y03", "Licenses adequate for print/web/app use (owner: Design Custodian + Legal / IP Counsel)", "Evidence Required", "As VAL-05", "OPEN — OWNER ACCEPTED; FORMALLY DEFERRED",
     "PARTIALLY VERIFIED (repository OFL text)", EXT, "YES — AS-IS", LEGAL_TERM, "NO", "As VAL-05."],
    ["VAL-06", "Every approved production image has rights/source/usage metadata", "Not started; HR01 session statement that Part D concept images were generated by the respondent with ChatGPT image generation (the FD01 instruction records it as a Brand Owner declaration)",
     "FD-G01: tool terms/licence record not digitally retained or requested", "OPEN — OWNER ACCEPTED / DIGITAL TERMS REVIEW DEFERRED", "OWNER DECLARED (provenance statement); terms record not inspected", EXT, "YES — AS-IS",
     LEGAL_TERM + " No image is approved for production; Part D imagery remains concept/reference.", "NO", "No rights register exists. The declaration is a provenance statement, not a rights opinion; no personal account records are requested."],
    ["Y04", "Image/model/property rights documented", "Evidence Required", "As VAL-06", "OPEN — OWNER ACCEPTED / DIGITAL TERMS REVIEW DEFERRED", "OWNER DECLARED (provenance statement)", EXT, "YES — AS-IS", LEGAL_TERM, "NO", "As VAL-06."],
    ["AC19", "Approved — governance model accepted; actual named role holders must be assigned before release", "OPEN / HOLDER CONDITION INCOMPLETE (Register: Approved with modification); 1 of 12 canonical roles named",
     "FD-G02: holder completion postponed", "OPEN — FORMALLY DEFERRED / HOLDER COMPLETION POSTPONED BY BRAND OWNER", "Mashal named as Arabic / Localization Lead; 11 holders unnamed", "n/a", "YES — AS-IS",
     "The Register's own acceptance wording requires holders 'before release'; the Owners & Governance sheet repeats that each holder must be recorded before AC20 final release authorization. Deferral is therefore a postponement, not a satisfaction.", "NO",
     "The acceptance condition (named holders) is unmet; not failed."],
    ["SR-12", "Windows-native assistive-technology validation (NVDA / JAWS) — AX01 matrix SR-12", "DEFERRED (content-owner authority; Windows unavailable)", "FD-G03: Brand Owner formal deferral replaces the earlier content-owner deferral",
     "FORMALLY DEFERRED BY BRAND OWNER (not performed)", "n/a — test not performed", "NOT PERFORMED", "YES — AS-IS", "Deferral is recognised: VAL-08's criterion allows issues 'resolved or formally excepted'; an exception does not satisfy the WCAG test requirement.", "NO",
     "macOS VoiceOver evidence is preserved (11 PASS, reviewer observed). No Windows result is claimed."],
    ["SR-11", "PDF / Acrobat tagged-PDF and Arabic text-layer validation — AX01 matrix SR-11", "DEFERRED — D8 (content-owner authority)", "FD-G04: Brand Owner formal deferral", "FORMALLY DEFERRED BY BRAND OWNER (not performed)", "n/a — test not performed", "NOT PERFORMED",
     "YES — AS-IS", "As SR-12.", "NO", "No PDF regenerated; no result fabricated."],
    ["D8", "Approved native PDF route and tests (external Arabic/bilingual PDF validation)", "OPEN", "FD-G04", "OPEN — FORMALLY DEFERRED BY BRAND OWNER", "n/a", "NOT PERFORMED", "YES — AS-IS",
     "D8 is an ODI01 owner decision with an operating rule, not a Register row; deferral by the Brand Owner is a postponement of the tests, not a pass.", "NO",
     "The operating rule stays in force: Arabic/bilingual DOCX/PDF are INTERNAL WORKING ONLY and may not be issued externally until the listed native tests pass, unless the owner amends the rule."],
    ["VAL-07", "Continuous RTL layouts, shaping, numerals, mixed-language content and screen-reader order pass native review", "Not started; HR01: human linguistic review and macOS VoiceOver complete", "Windows-side evidence formally deferred (FD-G03)", "OPEN (unchanged); Windows part FORMALLY DEFERRED", "REVIEWER OBSERVED \u2014 MASHAL (macOS scope); not independently verified; Windows not performed", "Partial", "YES — AS-IS", "n/a", "NO", "Continuous production layouts with real content are not part of FD01."],
    ["VAL-08", "WCAG 2.2 AA target tested in real digital/document outputs; issues resolved or formally excepted", "In progress; HR01 macOS evidence", "Windows and PDF parts formally deferred (FD-G03, FD-G04)", "OPEN (unchanged); Windows and PDF parts FORMALLY DEFERRED", "REVIEWER OBSERVED \u2014 MASHAL (macOS scope); not independently verified; no conformance claim", "Partial", "YES — AS-IS", "The criterion permits 'formally excepted' issues; no exception record is created by FD01 for the unmeasured contrast and independent-QA items.", "NO", "Contrast over pictures, independent Accessibility QA and exceptions are still open."],
    ["VAL-15", "Final editable deck opens, saves, reopens and exports without repair, clipping, substitution or accessibility regression", "Not started", "PDF parts formally deferred (FD-G04)", "OPEN (unchanged); PDF part FORMALLY DEFERRED", "Partial (open/render only)", "Partial", "YES — AS-IS", "n/a", "NO", "No final deliverables exist."],
    ["AC20", "Brand Owner authorizes GEM™ Brand Guidelines V3.0 for release; follows completion of critical evidence gates and is issued by the named Brand Owner", "OPEN / FINAL RELEASE AUTHORIZATION PENDING",
     "FD-G05 accepts the current state; the three workstreams change from unresolved to FORMALLY DEFERRED / OWNER ACCEPTED", "OPEN / FINAL BRAND OWNER RELEASE AUTHORIZATION PENDING", "n/a", "n/a", "Owner acceptance of RC2 as-is is recorded; release authorization is not",
     "OD-G12 allows 'formally deferred by authorized owners'; the Register says do not authorize AC20 while critical gates remain open and requires a named Brand Owner holder.", "NO",
     "FD01 does not authorize release. It changes the dependency state of three workstreams only; many other gates remain open (09)."],
]
DIG = {g: "NO \u2014 BY OWNER DECISION" for g in ("VAL-03", "VAL-04", "VAL-06", "Y01", "Y02", "Y04")}
DIG.update({g: "YES \u2014 repository OFL text (three Regular builds)" for g in ("VAL-05", "Y03")})
GATES = [r[:6] + [DIG.get(r[0], "n/a")] + r[6:] for r in GATES]
write("08_FD01_Gate_Impact_Matrix.csv", G_H, GATES)

# ------------------------------------------------------------------ 09 remaining evidence
R_H = ["Item", "Gate(s)", "Status after FD01", "Remaining-evidence wording", "Owner", "Reopening trigger"]
OFFL = "Supporting documentation retained offline by Brand Owner; digital verification intentionally deferred."
REM = [
    ["Trademark / distinctiveness legal review document", "VAL-03; Y01", "OPEN — FORMALLY DEFERRED; OWNER ACCEPTED", OFFL, "Brand Owner (declared); Legal / IP Counsel (Register owner)", "Owner provides a review route, or the AC20 decision requires it"],
    ["Logo artwork ownership / assignment document", "VAL-04; Y02", "OPEN — OWNER ACCEPTED", OFFL, "Brand Owner / Legal", "As above"],
    ["Image-generation tool terms (ChatGPT image generation) for Part D concept imagery", "VAL-06; Y04", "OPEN — OWNER ACCEPTED / DIGITAL TERMS REVIEW DEFERRED", "Owner-declared provenance; terms record not digitally retained.", "Brand Owner", "Production use of any image is planned"],
    ["Font exact-build freeze and deployment-licence acceptance (OFL text for three Regular builds is in the repository)", "VAL-05; Y03; VAL-19", "OPEN — OWNER ACCEPTED; FORMALLY DEFERRED", "Repository OFL texts located; exact-build and deployment acceptance not performed.", "Design Custodian + Legal / IP Counsel", "Production deployment of fonts is planned"],
    ["Eleven remaining canonical role holders (including the Brand Owner)", "AC19; AC20", "OPEN — FORMALLY DEFERRED", "Holder completion postponed by Brand Owner.", "Brand Owner", "AC20 decision"],
    ["Windows-native assistive-technology validation", "SR-12; VAL-07; VAL-08", "FORMALLY DEFERRED BY BRAND OWNER", "Not performed; macOS VoiceOver evidence preserved.", "Accessibility QA (unnamed)", "A Windows environment is available, or AC20 decision requires it"],
    ["PDF / Acrobat validation", "SR-11; D8; VAL-15", "FORMALLY DEFERRED BY BRAND OWNER", "Not performed; D8 operating rule still blocks external issue of Arabic/bilingual DOCX/PDF.", "Presentation / Document QA", "An external PDF issue is planned"],
    ["NOT covered by FD01 and still open: VAL-01, VAL-02, VAL-07 (continuous production RTL layouts), VAL-08 (contrast over pictures, independent QA, exceptions), VAL-09, VAL-10, VAL-11, VAL-13, VAL-14, VAL-15 (final deliverables), VAL-16, VAL-17, VAL-19, VAL-20, VAL-21, AC07, AC10, AC17, OD-TPL, OD-SRC (VAL-12 is Deferred in the Register; VAL-18 is NOT ALLOCATED)", "see HR01 / OD01 registers", "OPEN (unchanged)", "Not addressed by this deferral; each still has its own acceptance requirement.", "Various", "AC20 decision"],
    ["Brand Owner final release authorization", "AC20", "OPEN / FINAL BRAND OWNER RELEASE AUTHORIZATION PENDING", "Dedicated decision still required; must state how the Register's 'critical gates' and 'named holders' conditions are treated.", "Brand Owner (named)", "Separate AC20 decision"],
]
write("09_FD01_Remaining_Evidence_After_Deferral.csv", R_H, REM)
print("decisions", len(OD), "deferrals", len(DF), "gates", len(GATES), "remaining", len(REM))
