#!/usr/bin/env python3
"""RP01 promotion rule tables. Each rule: (member_regex, old, new, expected_count, where, classification, reason).
Classification A = stale release-state label (changed). Preserved occurrences (B/C/D) are listed in PRESERVE and checked by the engine's residual scan.
All text edits are release-state labels, version labels, document IDs, the release date, and status text superseded by FA01.
No brand content, Arabic wording, layout, alt text, token value or image is touched."""
EM = "—"
TM = "™"
DOT = "·"
SL = r"ppt/slides/slide\d+\.xml"
NT = r"ppt/notesSlides/notesSlide\d+\.xml"


def s(n):
    return r"ppt/slides/slide%d\.xml" % n


def nt(n):
    return r"ppt/notesSlides/notesSlide%d\.xml" % n


A = "A"
ISSUE = "2026-10-09"
BASELINE = "OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE"
FORMAL = "formal deferrals recorded"

# ---------------------------------------------------------------- Part A
PART_A = [
    (SL, "V3.0 RC2 %s PART A" % DOT, "V3.0 %s PART A" % DOT, 59, "text", A, "running header: RC2 is a stale release-state label"),
    (s(1), "V3.0 RC2 %s Working edition %s release not yet authorized (AC20) %s logo from supplied vector kit, owner acceptance PENDING (VAL-02) %s Document ID GEM-BG-V3.0-RC2 %s issued 2026-10-06" % (DOT, DOT, DOT, DOT, DOT),
     "V3.0 %s Owner authorized final brand-system baseline (AC20) %s formal deferrals recorded %s logo from supplied vector kit, owner acceptance PENDING (VAL-02) %s Document ID GEM-BG-V3.0 %s issued %s" % (DOT, DOT, DOT, DOT, DOT, ISSUE),
     1, "text", A, "cover edition line: RC2 / working edition / AC20 not authorized are superseded by FA01; VAL-02 qualifier preserved"),
    (s(3), "Issued as RC2, pending production validation.", "Issued as V3.0, pending production validation.", 1, "text", A, "RC2 label; pending production validation qualifier preserved"),
    (s(72), "Release authorization (AC20) rests with the Brand Owner.", "Release authorization (AC20) was issued by the Brand Owner, with formal deferrals.", 1, "text", A, "AC20 sentence superseded by FA01; role placeholders and AC19 sentence untouched"),
    (s(78), "Production standards, Part C RC2 ", "Production standards, Part C ", 1, "text", A, "RC2 label; ISSUED / AC17 / VAL-10 / VAL-11 OPEN preserved"),
    (s(78), "%s AC20 %s [REQUIRES OWNER]" % (DOT, DOT), "%s AC20 %s AUTHORIZED, WITH FORMAL DEFERRALS" % (DOT, DOT), 1, "text", A, "AC20 status superseded by FA01"),
    (s(79), "%s GEM-BG-V3.0-RC2" % DOT, "%s GEM-BG-V3.0" % DOT, 1, "text", A, "document ID"),
    (s(79), "%s V3.0 RC2 (Release Candidate 2)" % DOT, "%s V3.0 (final brand-system baseline)" % DOT, 1, "text", A, "version label"),
    (s(79), "%s WORKING EDITION %s NOT RELEASED" % (DOT, DOT), "%s %s" % (DOT, BASELINE), 1, "text", A, "edition state superseded by FA01"),
    (s(79), "%s 2026-10-06" % DOT, "%s %s" % (DOT, ISSUE), 1, "text", A, "release date"),
    (s(79), "%s Brand Owner %s AC20 PENDING" % (DOT, DOT), "%s Brand Owner %s AC20 AUTHORIZED WITH FORMAL DEFERRALS" % (DOT, DOT), 1, "text", A, "approver status"),
    (s(79), "%s RC2 synchronized %s evidence gates open" % (DOT, DOT),
     "%s Owner authorized baseline %s formal deferrals recorded %s evidence gates open or deferred" % (DOT, DOT, DOT), 1, "text", A, "release status"),
    (s(79), "%s V3.0 working edition (undated, pre-RC2)" % DOT, "%s V3.0 RC2 (2026-10-06) and V3.0 working edition (undated)" % DOT, 1, "text", A, "supersedes line names the RC2 edition explicitly"),
    (s(79), "%s GEM-DDS-V3.0-RC2 (Part B) %s GEM-PS-V3.0-RC2 (Part C)" % (DOT, DOT), "%s GEM-DDS-V3.0 (Part B) %s GEM-PS-V3.0 (Part C)" % (DOT, DOT), 1, "text", A, "related document IDs"),
    (s(79), "Change log %s RC2, 2026-10-06:" % DOT,
     "Change log %s V3.0 labels; RC2, 2026-10-06:" % DOT, 1, "text", A, "change-log entry for this promotion"),
    (s(80), "Brand Guidelines V3.0 RC2 %s Part A %s Working edition %s not released" % (DOT, DOT, DOT), "Brand Guidelines V3.0 %s Part A %s Owner authorized final brand-system baseline" % (DOT, DOT), 1, "text", A, "closing line"),
    (nt(1), "Edition: V3.0 Release Candidate 2 (RC2), a working edition synchronized with Part B and Part C RC2 and with the V3 Final Brand Approval Register. Brand Owner release authorization (AC20) is pending.",
     "Edition: V3.0, the owner-authorized final brand-system baseline, synchronized with Part B and Part C and with the V3 Final Brand Approval Register. Brand Owner release authorization (AC20) was issued with formal deferrals and artifact-specific external-issue restrictions.", 1, "text", A, "speaker note: edition"),
    (nt(3), "Part C exists as Release Candidate 2 and is a working edition pending production validation (AC17).", "Part C exists as V3.0; its production-standard edition state is working edition pending production validation (AC17).", 1, "text", A, "speaker note"),
    (nt(79), "issued as Release Candidate 2 with a token package", "issued as V3.0 with a token package", 1, "text", A, "speaker note"),
    (nt(79), "Part C, Production Standards V3.0, is issued as Release Candidate 2, a working edition pending production validation.", "Part C, Production Standards V3.0, is issued as V3.0, pending production validation.", 1, "text", A, "speaker note"),
    (nt(80), "Owner and approver names are recorded by the Brand Owner before AC20. Part B is issued as its own RC2 deck with a token package (PartB_RC2/05_release);",
     "Owner and approver names are recorded by the Brand Owner (AC19 is formally deferred). Part B is issued as its own deck with a token package;", 1, "text", A, "speaker note"),
]

# ---------------------------------------------------------------- Part B
PART_B = [
    (SL, "V3.0 RC2 %s working specification" % DOT, "V3.0 %s specification" % DOT, 34, "text", A, "running footer"),
    (s(1), "V3.0 RC2 %s WORKING SPECIFICATION %s NOT RELEASED (AC20 PENDING) %s GEM-DDS-V3.0-RC2 %s ISSUED 2026-10-06" % (DOT, DOT, DOT, DOT),
     "V3.0 %s %s %s GEM-DDS-V3.0 %s ISSUED %s" % (DOT, BASELINE, DOT, DOT, ISSUE.replace("-", "-")), 1, "text", A, "cover edition line"),
    (s(4), "A. Brand Guidelines V3.0 RC2", "A. Brand Guidelines V3.0", 1, "text", A, "part list"),
    (s(4), "B. Digital Design System V3.0 RC2", "B. Digital Design System V3.0", 1, "text", A, "part list"),
    (s(4), "C. Production Standards V3.0 RC2", "C. Production Standards V3.0", 1, "text", A, "part list"),
    (s(4), "Issued as RC2 %s WORKING EDITION / PENDING PRODUCTION VALIDATION (DS04, AC17)" % DOT, "Issued as V3.0 %s WORKING EDITION / PENDING PRODUCTION VALIDATION (DS04, AC17)" % DOT, 1, "text", A, "RC2 label; Part C's own production-standard edition state preserved"),
    (s(30), "gem-tokens.v3.0-rc2.json / .css", "gem-tokens.v3.0.json / .css", 1, "text", A, "token file names follow the promoted package"),
    (s(30), "gem-tokens.v3.0-rc2.json and .css", "gem-tokens.v3.0.json and .css", 1, "text", A, "token file names"),
    (s(30), "Versioning: semantic 3.0.0-rc.2 (document edition V3.0 RC2).", "Versioning: semantic 3.0.0 (document edition V3.0).", 1, "text", A, "token package semver and edition"),
    (s(31), "Part C issued as RC2, physical evidence open", "Part C issued as V3.0, physical evidence open", 1, "text", A, "RC2 label"),
    (s(31), "All role holders TBD; release authorization pending (AC20)", "Role holders TBD (AC19 formally deferred); release authorization issued with formal deferrals (AC20)", 1, "text", A, "AC20 status superseded by FA01"),
    (s(33), "3.0.0-rc.2 %s V3.0 RC2 (this edition)" % DOT, "3.0.0 %s V3.0 (this edition)" % DOT, 1, "text", A, "version history"),
    (s(34), "%s GEM-DDS-V3.0-RC2" % DOT, "%s GEM-DDS-V3.0" % DOT, 1, "text", A, "document ID"),
    (s(34), "%s V3.0 RC2 (Release Candidate 2) %s semantic 3.0.0-rc.2" % (DOT, DOT), "%s V3.0 (final brand-system baseline) %s semantic 3.0.0" % (DOT, DOT), 1, "text", A, "version label"),
    (s(34), "%s WORKING SPECIFICATION %s NOT RELEASED" % (DOT, DOT), "%s %s %s SPECIFICATION ONLY, NO COMPONENT IMPLEMENTATION" % (DOT, BASELINE, DOT), 1, "text", A, "edition state"),
    (s(34), "=Issue date %s 2026-10-06" % DOT, "Issue date %s %s" % (DOT, ISSUE), 1, "text", A, "release date (exact run only; change-log history untouched)"),
    (s(34), "%s Brand Owner %s AC20 PENDING" % (DOT, DOT), "%s Brand Owner %s AC20 AUTHORIZED WITH FORMAL DEFERRALS" % (DOT, DOT), 1, "text", A, "approver status"),
    (s(34), "%s RC2 synchronized with Parts A and C %s evidence gates open" % (DOT, DOT),
     "%s Owner authorized baseline, synchronized with Parts A and C %s formal deferrals recorded; release-checklist items (slide 33) deferred, not closed %s evidence gates open or deferred" % (DOT, DOT, DOT), 1, "text", A, "release status"),
    (s(34), "%s GEM-BG-V3.0-RC2 (Part A) %s GEM-PS-V3.0-RC2 (Part C)" % (DOT, DOT), "%s GEM-BG-V3.0 (Part A) %s GEM-PS-V3.0 (Part C)" % (DOT, DOT), 1, "text", A, "related document IDs"),
    (s(34), "3.0.0-rc.2 %s 2026-10-06 %s RC2 synchronization" % (DOT, DOT),
     "3.0.0 %s %s %s release labels only; no content, token or layout change. 3.0.0-rc.2 %s 2026-10-06 %s RC2 synchronization" % (DOT, ISSUE, DOT, DOT, DOT), 1, "text", A, "change-log entry for this promotion"),
    (nt(1), "Editable source of the GEM Digital Design System V3.0, Release Candidate 2 (RC2), synchronized with Part A RC2, Part C RC2 and the V3 Final Brand Approval Register",
     "Editable source of the GEM Digital Design System V3.0, the owner-authorized final brand-system baseline, synchronized with Part A, Part C and the V3 Final Brand Approval Register", 1, "text", A, "speaker note"),
    (nt(4), "Part C exists as Release Candidate 2; it is a working edition pending production validation (AC17), not a production-approved standard.",
     "Part C exists as V3.0; its production-standard edition state is working edition pending production validation (AC17), not a production-approved standard.", 1, "text", A, "speaker note"),
]

# ---------------------------------------------------------------- Part C
PART_C = [
    (SL, "V3.0 RC2 %s PART C %s WORKING EDITION" % (DOT, DOT), "V3.0 %s PART C %s EDITION" % (DOT, DOT), 4, "text", A, "running header (section tag)"),
    (SL, "V3.0 RC2 %s PART C" % DOT, "V3.0 %s PART C" % DOT, 66, "text", A, "running header"),
    (s(1), "Production Standards V3.0 %s Release Candidate 2" % EM, "Production Standards V3.0", 1, "text", A, "cover title line (name of the slide)"),
    (s(1), "RELEASE CANDIDATE 2", "V3.0 %s FINAL BRAND-SYSTEM BASELINE" % DOT, 1, "text", A, "cover edition tag"),
    (s(1), "Release conditions incomplete %s release authorization [REQUIRES OWNER] (AC20) %s logo from supplied vector kit, acceptance PENDING (VAL-02) %s Document ID GEM-PS-V3.0-RC2 %s V3.0 RC2 %s issued 2026-10-06" % (DOT, DOT, DOT, DOT, DOT),
     "Production release conditions incomplete %s release authorization (AC20) issued with formal deferrals %s logo from supplied vector kit, acceptance PENDING (VAL-02) %s Document ID GEM-PS-V3.0 %s V3.0 %s issued %s" % (DOT, DOT, DOT, DOT, DOT, ISSUE), 1, "text", A, "cover status line; production-validation qualifier preserved"),
    (s(75), "SEVENTEEN OPEN", "SEVENTEEN LISTED", 1, "text", A, "AC20 is no longer an open gate"),
    (s(75), "Final release authorization %s AC20" % DOT, "Final authorization %s AC20 %s issued" % (DOT, DOT), 1, "text", A, "AC20 status superseded by FA01"),
    (s(76), "Open %s AC20" % DOT, "Authorized %s AC20, formal deferrals" % DOT, 1, "text", A, "gate 6 status superseded by FA01; gates 1 to 5 stay Open"),
    (s(76), "Until all six are met: V3.0 RC2 %s WORKING EDITION / PENDING PRODUCTION VALIDATION" % DOT, "Until all six are met: V3.0 %s WORKING EDITION / PENDING PRODUCTION VALIDATION" % DOT, 1, "text", A, "RC2 label; Part C's own production-standard rule preserved"),
    (s(77), "GEM-PS-V3.0-RC2", "GEM-PS-V3.0", 1, "text", A, "document ID"),
    (s(77), "V3.0 RC2 (Release Candidate 2)", "V3.0 (final brand-system baseline)", 1, "text", A, "version label"),
    (s(77), "WORKING EDITION %s NOT RELEASED" % DOT, "AUTHORIZED %s WORKING EDITION" % DOT, 1, "text", A, "edition state; production-standard state preserved"),
    (s(77), "=2026-10-06", ISSUE, 1, "text", A, "release date (exact run only; change-log history untouched)"),
    (s(77), "Brand Owner %s AC20 PENDING" % DOT, "Brand Owner %s AC20 AUTHORIZED" % DOT, 1, "text", A, "approver status"),
    (s(77), "Release status: RC2 synchronized with Part A and Part B RC2 %s evidence gates open" % DOT,
     "Release status: owner authorized baseline %s formal deferrals recorded %s gates open or deferred" % (DOT, DOT), 1, "text", A, "release status"),
    (s(77), "Supersedes: Release Candidate 1 (undated) %s Related: GEM-BG-V3.0-RC2 (Part A) %s GEM-DDS-V3.0-RC2 (Part B)" % (DOT, DOT),
     "Supersedes: V3.0 RC2 (2026-10-06), RC1 (undated) %s Related: GEM-BG-V3.0 (Part A) %s GEM-DDS-V3.0 (Part B)" % (DOT, DOT), 1, "text", A, "supersedes / related IDs"),
    (s(77), "Change log %s RC2, 2026-10-06:" % DOT, "Change log %s V3.0 labels; RC2, 2026-10-06:" % DOT, 1, "text", A, "change-log entry for this promotion"),
    (s(78), "RELEASE CANDIDATE 2 %s WORKING EDITION / PENDING PRODUCTION VALIDATION" % DOT, "V3.0 %s WORKING EDITION / PENDING PRODUCTION VALIDATION" % DOT, 1, "text", A, "back cover; RC label; production-standard state preserved"),
    (nt(1), "Edition: V3.0 Release Candidate 2 (RC2), a working edition synchronized with Part A and Part B RC2 and the V3 Final Brand Approval Register.",
     "Edition: V3.0, the owner-authorized final brand-system baseline, synchronized with Part A and Part B and the V3 Final Brand Approval Register. Its production-standard edition state remains working edition pending production validation.", 1, "text", A, "speaker note"),
    (nt(76), "This edition is Release Candidate 2, a working edition. No gate is closed; gate IDs follow the register.",
     "This edition is the V3.0 owner-authorized baseline; its production-standard edition state remains working edition pending production validation. No evidence gate is closed by that authorization; gate IDs follow the register.", 1, "text", A, "speaker note"),
    (r"docProps/core\.xml", "Release Candidate 1</dc:title>", "V3.0 %s Part C</dc:title>" % EM, 1, "xml", A, "document title metadata carried a stale RC1 label"),
]

# ---------------------------------------------------------------- Part D
PART_D = [
    (SL, "v1.0   WORKING EDITION", "V3.0   CONCEPT PORTFOLIO", 22, "text", A, "slide footer: v1.0 / working edition superseded; concept status preserved on the slide's own CONCEPT / NOT PRODUCTION ARTWORK line"),
    (SL, "v1.0   WORKING EDITION", "V3.0   CONCEPT PORTFOLIO", 22, "attr", A, "shape name"),
    (s(1), "v1.0   /   06 OCTOBER 2026", "V3.0   /   09 OCTOBER 2026", 1, "text", A, "cover version and date"),
    (s(22), "AC20   /   OPEN", "AC20   /   AUTHORIZED, CONCEPT SCOPE ONLY", 1, "text", A, "AC20 status superseded by FA01"),
    (s(22), "WORKING EDITION   /   PENDING PRODUCTION VALIDATION", "V3.0 CONCEPT PORTFOLIO   /   PENDING PRODUCTION VALIDATION", 1, "text", A, "edition tag; production qualifier preserved"),
    (s(23), "WORKING EDITION", "V3.0 BASELINE", 1, "text", A, "current-state cell for the source / change log"),
    (s(23), "REVIEW PACKAGE   /   OWNER APPROVAL AND PRODUCTION RELEASE REMAIN OPEN", "V3.0 CONCEPT PORTFOLIO   /   PRODUCTION RELEASE REMAINS OPEN", 1, "text", A, "package line: owner approval is now recorded; production release stays open"),
    (s(24), "Concept Product Portfolio v1.0", "Concept Product Portfolio V3.0", 1, "text", A, "version label"),
    (s(24), "WORKING EDITION   /   CONCEPT / NOT PRODUCTION ARTWORK", "V3.0 CONCEPT PORTFOLIO   /   CONCEPT / NOT PRODUCTION ARTWORK", 1, "text", A, "edition tag; concept status preserved"),
    (s(1), "v1.0   /   06 OCTOBER 2026", "V3.0   /   09 OCTOBER 2026", 1, "attr", A, "shape name equals its text"),
    (s(24), "Concept Product Portfolio v1.0", "Concept Product Portfolio V3.0", 1, "attr", A, "shape name equals its text"),
    (s(24), "WORKING EDITION   /   CONCEPT / NOT PRODUCTION ARTWORK", "V3.0 CONCEPT PORTFOLIO   /   CONCEPT / NOT PRODUCTION ARTWORK", 1, "attr", A, "shape name equals its text"),
    (s(22), "AC20   /   OPEN", "AC20   /   AUTHORIZED, CONCEPT SCOPE ONLY", 1, "attr", A, "shape name equals its text"),
    (s(22), "WORKING EDITION   /   PENDING PRODUCTION VALIDATION", "V3.0 CONCEPT PORTFOLIO   /   PENDING PRODUCTION VALIDATION", 1, "attr", A, "shape name equals its text"),
    (NT, "GEM Amenities and Packaging Concept Portfolio v1.0. Working edition, concept review only.", "GEM Amenities and Packaging Concept Portfolio V3.0. Concept portfolio, concept review only.", 24, "text", A, "speaker note prefix"),
    (NT, "domain-owning RC2 Part A/B/C", "domain-owning Part A/B/C", 24, "text", A, "speaker note"),
]

# Residual (preserved) occurrences: regex over a paragraph's text -> (class, reason). Anything else matching STALE after promotion fails the build.
PRESERVE = [
    (r"PENDING VALIDATION|PENDING LOCALIZATION APPROVAL|PENDING PRODUCTION VALIDATION|PENDING PRODUCTION MASTER", "B", "still-valid qualifier: the underlying validation is not performed (FA01 deferrals)"),
    (r"WORKING EDITION / PENDING PRODUCTION VALIDATION", "B", "Part C production-standard edition state per its own rule (slide 76); production gates remain open or deferred"),
    (r"Edition states: WORKING EDITION", "C", "Part C vocabulary of edition states (explanatory)"),
    (r"RC2, 2026-10-06|3\.0\.0-rc\.2 .{0,3} 2026-10-06|RC2 synchronization|V3\.0 RC2 \(2026-10-06\)|promoted from 3\.0\.0-rc\.2|RC2 to V3\.0 baseline|updated from RC2|promoted from RC2", "C", "change-log / supersedes text naming the RC2 edition: historical context"),
    (r"^AUTHORIZED . WORKING EDITION$", "B", "Part C edition-state cell: authorized baseline; the production-standard edition state stays WORKING EDITION (slide 76 rule)"),
    (r"production-standard edition state|Part C.{0,40}(working edition|WORKING EDITION)", "B", "Part C production-standard edition state per its own rule (production validation pending)"),
    (r"Supersedes.{0,6}V3\.0 working specification|V3\.0 working edition \(undated\)", "C", "supersedes line naming earlier editions: historical context"),
    (r"is not released\.", "C", "production-file release rule (a file not in the manifest is not released), not an edition-state label"),
    (r"PartB_RC2/|PartB_RC2\\", "C", "repository path of a historical working folder"),
    (r"RC2 Open Evidence Register|GEM_V3_RC2_Release_Notes|RC2 rules and departures from chat|Earlier working editions", "C", "named historical document or explanatory reference"),
    (r"AC17, AC19 and AC20|Register AC19, AC20|AC19, AC20, VAL-01|AC20 \(authorized|release checkpoints|Brand Owner authorization \(AC20\)", "C", "gate / checkpoint identifier in explanatory or checklist text (not a pending status)"),
]


# ---------------------------------------------------------------- Word templates
SUBJ_OLD = "WORKING APPLICATION / PENDING VALIDATION; RC2 application; 2026-10-08"
WM = "WORKING APPLICATION / PENDING VALIDATION"
RESTRICT_LINE = "CONTROLLED INTERNAL TEMPLATE %s EXTERNAL ISSUE RESTRICTED PENDING D8 VALIDATION" % DOT


def english_rules(n_footers):
    return [
        (r"word/footer\d+\.xml", WM, "", n_footers, "text", A, "status marker in footer: working-application label superseded by the V3.0 baseline; page-number field untouched"),
        (r"docProps/core\.xml", SUBJ_OLD, "V3.0; %s" % ISSUE, 1, "text", A, "document subject metadata"),
    ]


# third footer line carrying the restriction; the two D8 markings stay verbatim. Group 1 = run prefix incl. rPr, group 2 = marker text.
_RUN = r"(<w:r><w:rPr>(?:(?!</w:rPr>).)*?</w:rPr><w:t xml:space=\"preserve\">)(PENDING LOCALIZATION APPROVAL)(</w:t></w:r>)"
_NEW = r"\1\2\3<w:r><w:br/></w:r>\1" + RESTRICT_LINE + r"\3"


def restricted_rules(n_footers):
    return [
        (r"word/footer\d+\.xml", _RUN, _NEW, n_footers, "re", A, "added a third footer line stating the external-issue restriction; both D8 markings verbatim"),
        (r"docProps/core\.xml", SUBJ_OLD, "V3.0; CONTROLLED INTERNAL TEMPLATE; EXTERNAL ISSUE RESTRICTED PENDING D8 VALIDATION; %s" % ISSUE, 1, "text", A, "document subject metadata"),
    ]
