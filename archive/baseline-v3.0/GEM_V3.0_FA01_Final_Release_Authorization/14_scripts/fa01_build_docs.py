#!/usr/bin/env python3
"""FA01 narrative documents 01, 02, 05, 06, 07, 08, 11, 12, 13.

Run from the repository root:
  python3 -I GEM_V3.0_FA01_Final_Release_Authorization/14_scripts/fa01_build_docs.py [--authorized]
Without --authorized every document states that AC20 is PROPOSED and still OPEN.
Placeholders: {B} banner, {A} AC20 status line, {W} AC20 wording, {-} em dash, {TM} trademark sign.
"""
import sys
from pathlib import Path

AUTH = "--authorized" in sys.argv
PKG = Path("GEM_V3.0_FA01_Final_Release_Authorization")
TM = "™"
EM = "—"

if AUTH:
    BANNER = ("GEM{TM} V3.0 {-} OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE {-} FORMAL DEFERRALS RECORDED {-} "
              "ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY")
    AC20 = "AC20: AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS"
    WHEN = "The Brand Owner confirmed the wording below in chat."
else:
    BANNER = "GEM{TM} V3.0 RC2 {-} OWNER ACCEPTED WITH FORMAL DEFERRALS {-} AC20 PROPOSED, NOT YET AUTHORIZED (FA01 DRAFT)"
    AC20 = "AC20: OPEN / FINAL BRAND OWNER RELEASE AUTHORIZATION PENDING (proposal prepared; the Brand Owner's explicit confirmation has not been given)"
    WHEN = "The Brand Owner has NOT yet confirmed this wording; it is a proposal."

WORDING = (
    "AC20 {-} FINAL BRAND OWNER RELEASE AUTHORIZATION: The Brand Owner (Mashal) authorizes GEM{TM} V3.0 as the controlled final "
    "brand-system baseline defined in 10_FA01_Release_Scope_Matrix.csv, subject to the formal deferrals, artifact-specific restrictions "
    "and residual limitations recorded in FA01. This authorization does not constitute independent Legal/IP verification, WCAG "
    "certification, validation of any artifact explicitly excluded from external release, production-master acceptance of the logo kit, "
    "or approval of Part D as production artwork.")


def w(name, body):
    text = body
    for k, v in (("{B}", BANNER), ("{A}", AC20), ("{W}", WORDING), ("{WHEN}", WHEN)):
        text = text.replace(k, v)
    text = text.replace("{TM}", TM).replace("{-}", EM)
    (PKG / name).write_text(text.rstrip() + "\n", encoding="utf-8")


HEAD = "**{B}**\n{A}\n\n"

w("01_FA01_Executive_Summary.md", "# 01 · FA01 {-} Executive Summary\n\n" + HEAD + """## Question
Can AC20 (final Brand Owner release authorization) be authorized when the Approval Register says not to authorize it while critical gates remain open, and the owner has formally deferred the evidence behind those gates?

## Answer
""" + ("Yes, but only under a narrow superseding release-disposition rule (05) that the Brand Owner decided. The release is a **limited release baseline** (State 2): nothing unperformed is recorded as passed, and artifacts that depend on unperformed work are restricted.\n"
       if AUTH else
       "It can be, but only under a narrow superseding release-disposition rule (05). This package proposes that rule and the exact AC20 wording (02). **The Brand Owner's explicit confirmation of the wording, scope, exclusions and baseline file set has not been given; until it is, AC20 stays OPEN.**\n") + """
## What the owner decided in FA01
| Decision | Selection |
|---|---|
| A | A3 {-} limited release baseline |
| B | Brand Owner holder: Mashal (Role: Brand Owner; Authority: final brand governance and AC20 release authorization) |
| C | C2 {-} narrow D8: controlled internal use; external issue of affected Arabic/bilingual DOCX/PDF blocked |
| E | The independent legal-clearance requirement is waivable by the Brand Owner, accepted as owner risk under formal deferral (never recorded as verified or cleared) |
| F | AC07, AC10, AC17, VAL-01 and every other evidence/work gate not previously deferred are formally deferred |
| G | Baseline = HR01 candidates + logo kit + tokens |

## What this is not
- Not independent verification of anything. One person is the Brand Owner, the Arabic / Localization Lead, the macOS VoiceOver reviewer and the declarer of the offline Legal/IP evidence (06, 11).
- Not legal clearance, trademark verification, ownership verification or WCAG certification.
- Not a production release: the logo kit remains WORKING ASSETS, Part D remains CONCEPT / NOT PRODUCTION ARTWORK, no PDF is authorized for external issue, and the visible labels inside the baseline files still read working edition / not released / AC20 pending until a separate promotion pass (10).
- Not a push, merge, tag, GitHub Release or visibility change. FA01 authorizes none of them.

## Where to look
02 decision record and exact AC20 wording {-} 05 superseding rule {-} 05b gate disposition {-} 07 D8 policy {-} 08 AC19 {-} 09 acceptance test {-} 10 scope matrix {-} 11 residual limitations {-} 12 supersession log.
""")

w("02_FA01_AC20_Decision_Record.md", "# 02 · FA01 {-} AC20 Decision Record\n\n" + HEAD + """## Decision
**{A}**

{WHEN}

## Exact AC20 wording
> {W}

## Release name and status line
GEM{TM} V3.0 {-} OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE {-} FORMAL DEFERRALS RECORDED {-} ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY

File names keep "RC2" and "HR01 CANDIDATE (UNAPPROVED)" because no files are renamed (sources are not renamed without separate authorization). The visible labels inside the files are likewise unchanged.

## Issuing authority
Brand Owner: Mashal {-} as typed by the owner. No surname, title, signature, employer or legal entity is added or inferred (06).

## Basis
1. Owner decisions A3, B, C2, E, F1, F2, G (04).
2. The narrow superseding release-disposition rule (05), which names every Register clause it overrides for AC20 purposes only.
3. Disposition of every Register gate and the D8 rule: none closed by evidence; each formally deferred, owner accepted under formal deferral, or already Deferred in the Register (05b).
4. The 15-test acceptance result (09): no FAIL; items marked PASS WITH FORMAL DEFERRAL are not plain passes.

## What AC20 does not do
It does not close a gate, change any gate status other than recording the deferral treatment, verify any evidence, or change the position of the Approval Register file (unchanged, sha256 ccce46135a4f...). It does not authorize a push, merge, pull request, tag, GitHub Release or visibility change; those need a separate explicit Brand Owner instruction.

## Not an approval of
Part D as production artwork {-} the logo kit as a production master {-} any Arabic or bilingual DOCX/PDF for external issue {-} any Windows or PDF accessibility result {-} any legal, trademark, ownership or licence position {-} any production packaging, supplier or regulated claim {-} component implementation.
""")

w("05_FA01_Deferral_Treatment.md", "# 05 · FA01 {-} Deferral Treatment and Superseding AC20 Release-Disposition Rule\n\n" + HEAD + """## Rule (applies to AC20 only)
Where a gate that the Approval Register requires to be closed before AC20 has been formally deferred, or owner accepted under formal deferral, by the Brand Owner, and the limitation is documented in the release governance record, the Brand Owner accepts the residual risk, and the artifacts that depend on the gate are restricted or excluded from the release scope, the gate is treated as **dispositioned for AC20 purposes**. It is recorded as *ACCEPTED FOR RELEASE UNDER FORMAL OWNER DEFERRAL* and is never recorded as closed, verified, cleared or passed.

## Register clauses overridden for AC20 purposes only
| Register clause | What happens |
|---|---|
| Instructions: "Do not authorize AC20 while critical gates remain open." | Overridden for AC20: critical gates remain open and AC20 is authorized with the deferral treatment above. |
| Instructions: "Before AC20, replace all TBD governance holders with actual names, close critical legal/production/Arabic/accessibility gates, and record evidence references." | Overridden for AC20: only the Brand Owner is named (Arabic / Localization Lead is also named under OD-G09); the other 10 holders stay TBD (08); the critical gates are deferred, not closed. |
| AC20 row: "Final release authorization must follow completion of critical evidence gates" | Overridden for AC20: authorization follows documented deferral, not completion. |
| AC19 row and Owners & Governance: holders "must be recorded before AC20" | Overridden for AC20: AC19 stays OPEN / FORMALLY DEFERRED / OWNER ACCEPTED FOR RELEASE (08). |
| VAL-03 / Y01 approver (Legal / IP Counsel) and VAL-04 / Y02 approver (Brand Owner / Legal) | Overridden for AC20 by Decision E: the Brand Owner waives the independent-legal-clearance requirement and accepts the risk. This is not a legal opinion and no clearance is claimed. |
| "A deferred item remains outside approved V3.0 scope until revisited." | **Kept.** Deferred items are outside the release scope and the artifacts that depend on them are restricted (10). |

The Register file itself is not edited; its text stays authoritative for every purpose other than AC20.

## What is not waived
- Nothing is recorded as PASS that was not performed. There is no claim of WCAG conformance, cross-platform accessibility, legal clearance, trademark or ownership verification, licence acceptance, or production-master acceptance.
- Unperformed D8 tests still block external issue of the affected Arabic/bilingual DOCX/PDF (07).
- A later owner decision, new evidence or a commissioned review may reopen any deferral (11).

## Why this is not a quiet reinterpretation
The tension between the Register and OD-G12 is stated in 03 and the override is declared above, clause by clause, as an owner decision (FA-A, FA-E, FA-F1, FA-F2) rather than inferred. The owner can reverse it by instruction.

## Deferral treatment table
Per-gate dispositions are in `05b_FA01_Gate_Disposition_Register.csv`.
""")

w("06_FA01_Brand_Owner_Holder_Record.md", "# 06 · FA01 {-} Brand Owner Holder Record\n\n" + HEAD + """## Record
| Field | Value |
|---|---|
| Role | Brand Owner |
| Holder | Mashal |
| Authority | Final brand governance and AC20 release authorization |
| Source | Typed by the owner in chat in response to Decision B |
| Not recorded | Surname, job title, employer, legal entity, signature, contact details, identity verification |

## Observations the record must carry
1. **Same-person overlap.** The owner also holds the Arabic / Localization Lead role (OD-G09) and the Accessibility Content Owner working authority (OD-G10), recorded the macOS VoiceOver results, and declared the offline Legal/IP evidence. No independent reviewer, approver or verifier appears anywhere in the evidence chain.
2. **Replaces earlier statements.** OD01 recorded that Mashal's role was "not linked to the Brand Owner role" and FD01 that two sources were "not asserted to be the same person". Both statements were true when written; the owner has now named Mashal as Brand Owner. Those files are not edited (12).
3. **Satisfies one Register condition only.** A named Brand Owner is the person the Register requires to issue AC20. It does not close AC19 (08).
""")

w("07_FA01_D8_External_Issue_Policy.md", "# 07 · FA01 {-} D8 External-Issue Policy (Decision C2)\n\n" + HEAD + """## Policy
1. **Controlled internal use** of Arabic and bilingual letterhead templates is permitted. Every internal use keeps the ODI01 markings "WORKING APPLICATION / PENDING VALIDATION" and "PENDING LOCALIZATION APPROVAL" (the marking condition is carried forward unchanged).
2. **External issue is blocked** for the artifacts affected by D8 until the native tests pass or the Brand Owner separately decides otherwise: Windows Word, Word Online, Acrobat text layer, tagged PDF, reading order, NVDA/JAWS, accessibility QA and final localization approval.
3. **Unaffected V3.0 artifacts are eligible** for the baseline and for internal use. External issue of any artifact still requires the separate promotion and relabel pass described in 10.

## Affected files (enforceable list)
| File | Basis |
|---|---|
| GEM_Letterhead_Arabic_First_Page_HR01_CANDIDATE.docx | Arabic Word template |
| GEM_Letterhead_Arabic_Continuation_HR01_CANDIDATE.docx | Arabic Word template |
| GEM_Letterhead_Bilingual_First_Page_HR01_CANDIDATE.docx | Bilingual Word template |
| GEM_Letterhead_Bilingual_Continuation_HR01_CANDIDATE.docx | Bilingual Word template |
| Any PDF of the four templates above | D8 / SR-11 |
| Any PDF or DOCX extract of Part A slides 37, 38, 39, 65, 66, 68 or Part B slide 9 | Arabic text content |
| Part D images that contain Arabic strings inside the pictures | No text layer; not approved |

## Not a waiver
C3 (owner waiver of the tests) was not selected. No result is recorded as D8 PASS, PDF validation complete, or Windows accessibility verified. SR-11 and SR-12 stay FORMALLY DEFERRED.
""")

w("08_FA01_AC19_Disposition.md", "# 08 · FA01 {-} AC19 Disposition\n\n" + HEAD + """## Disposition
**AC19: OPEN {-} FORMALLY DEFERRED / OWNER ACCEPTED FOR RELEASE.** AC19 is not closed.

## Why it is not closed
The Register requires actual named role holders for the canonical governance model. Two of the 12 canonical roles are named (Brand Owner and Arabic / Localization Lead, both Mashal); 10 are unnamed. FD01 formally deferred the rest (FD-G02).

## Treatment
- The Brand Owner (named in FA01, Decision B) can issue AC20 as the Register requires.
- The ten unnamed roles remain TBD. Decisions are recorded under role names; no holder is inferred.
- The role matrix, escalation paths and conflict-of-interest controls that depend on independent holders do not exist in practice. The same person occupies the owner, Arabic-lead and accessibility-content positions.
- Reopening trigger: the owner names further holders, or any later release step requires them.
""")

w("11_FA01_Residual_Limitations.md", "# 11 · FA01 {-} Residual Limitations\n\n" + HEAD + """The Brand Owner accepts these limitations as part of AC20. Accepting a limitation is not closing the gate behind it.

| # | Limitation | Consequence |
|---|---|---|
| 1 | Legal/IP: hard-copy evidence is held offline; existence is owner declared; nothing was inspected; no independent legal review (VAL-03, 04, 05 part, 06; Y01 to Y04) | No legal clearance, trademark verification, ownership verification or rights opinion is claimed anywhere |
| 2 | Windows Word, Word Online, NVDA / JAWS and PDF / Acrobat tests not performed (SR-11, SR-12, D8) | No Windows, PDF or cross-platform accessibility claim; Arabic / bilingual DOCX and PDF cannot be issued externally |
| 3 | macOS VoiceOver results are REVIEWER OBSERVED by Mashal for a defined scope | Not independent verification; not WCAG certification; contrast over pictures and independent QA remain deferred |
| 4 | Arabic wording reviewed by Mashal only; AC10 formally deferred | No Arabic system approval; no native-speaker or independent linguistic sign-off |
| 5 | Logo kit is WORKING ASSETS; VAL-02 / AC07 deferred | No accepted logo master; production vectors are unaccepted; no-spark micro mark pending |
| 6 | Part D is concept artwork with AI-generated imagery; provenance owner declared; VAL-06 / Y04 digital terms review deferred | Not production artwork; no image rights opinion |
| 7 | Fonts: OFL texts verified for three Regular builds only; exact-build freeze and deployment acceptance deferred (VAL-05, VAL-19) | Working builds only |
| 8 | Packaging, supplier, regulated-claims, digital components, motion, final deliverables, release manifest, usability test, cross-document sign-off, templates, typography QA, component source deferred (VAL-09, 10, 11, 13, 14, 15, 16, 17, 19, 20, 21, OD-TPL, OD-SRC) | Dependent artifacts are restricted (10); no production release |
| 9 | AC19: 10 of 12 canonical roles unnamed | Role matrix incomplete |
| 10 | AC17 and VAL-01 deferred | No approved production specifications; no signed commercial scope |
| 11 | One person is Brand Owner, Arabic lead, content owner, reviewer and evidence declarant | No independence anywhere in the chain |
| 12 | Visible labels in baseline files still read working edition / not released / AC20 pending; file names say RC2 / HR01 CANDIDATE (UNAPPROVED); VAL-16 release manifest does not exist | A separate promotion and relabel pass is required before any external issue |
| 13 | Public repository visibility (OD-G11) is not legal clearance | Publication closes no evidence gate |

## Reopening
The Brand Owner may reopen any deferral by instruction. Events that should prompt it: any plan for external issue of an affected artifact, a Windows environment becoming available, counsel being commissioned, a supplier engagement, or naming further governance holders.
""")

w("12_FA01_Governance_Supersession_Log.md", "# 12 · FA01 {-} Governance Supersession Log\n\n" + HEAD + """## Starting state
Branch `claude/gem-worktree-safety-30b559`, HEAD `e99c4100eef6e547105be1c1563653d9a7aed109` (FD01, local only), working tree clean. `origin/main` `4ea0d117da03850854654288afcdde98f39994d5`; origin branch `617456255231a6b36ca5eb688451f8a72eef0eb7` (HR01).

## Supersession map
| Earlier statement | Where | Superseded by | Treatment |
|---|---|---|---|
| "Do not authorize AC20 while critical gates remain open"; critical gates must be closed before AC20 | Register, Instructions and AC20 row | FA01 rule (05), for AC20 only | Register not edited; override declared clause by clause |
| Mashal's role "not linked to the Brand Owner role" | OD01 role assignments | FA01 Decision B (06) | OD01 left as historical snapshot |
| "Not asserted to be the same person" | FD01 `04` | FA01 Decision B (06) | FD01 left as historical snapshot |
| AC20 "OPEN / FINAL RELEASE AUTHORIZATION PENDING" | OD01, HR01, FD01 | FA01 02 | Only on the Brand Owner's confirmation; see the status line above |
| D8 rule as ODI01 stated it | ODI01-R1 `10_Arabic_PDF_Status.md` | FA01 Decision C2 (07) | Marking condition carried forward unchanged; external issue blocked for the listed files |
| Unlisted gates "remain open with their own acceptance requirements" | FD01 `09`, `10` | FA01 F1 / F2 (05b) | Now FORMALLY DEFERRED |
| Project status "NOT RELEASED / UNAPPROVED IMPLEMENTATION CANDIDATE" | CLAUDE.local.md, README.md | FA01 02 | `README.md` updated narrowly in the FA01 commit; `CLAUDE.local.md` (both copies) updated locally and not committed. The candidate file names and visible labels are not changed |

## Files changed outside the FA01 package
""" + ("`README.md`: one paragraph pointing to FA01 with the authorized status wording. No other file.\n" if AUTH else "None. (README stays unchanged while AC20 is proposed.)\n") + """
No AR01, AX01, OD01, HR01, FD01, ODI01-R1, D3, D7, NP01 or Register file was edited. `CLAUDE.local.md` and `.claude/` are local-only and are not committed.

## Remote operations
None performed. A push, merge, pull request, tag, GitHub Release or visibility change needs a separate explicit Brand Owner instruction.
""")

w("13_FA01_Evidence_Index.md", "# 13 · FA01 {-} Evidence Index\n\n" + HEAD + """| Reference | Role in FA01 |
|---|---|
| `GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx` (sha256 ccce46135a4f...) | Authority; unchanged; clauses overridden are listed in 05 |
| `GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/` | OD-G01..G12; OD-G09 / OD-G10 role assignments; OD-G12 AC20 sequencing |
| `GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/` | Review queue outcomes; VoiceOver evidence (07, 08); `18_candidate_corrections` (baseline candidate files) |
| `GEM_V3.0_RC2_FD01_Formal_Deferral_Owner_Acceptance/` | FD-G01..G06; gate matrix; Legal/IP offline declaration; risk acceptance |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/10_Arabic_PDF_Status.md` | Source of the D8 rule |
| `GEM_Brand_Assets_v1.0/` | Logo kit (WORKING ASSETS) |
| `PartB_RC2/05_release/tokens/` | Derived design tokens |
| `GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/` | English letterhead templates |
| FA01 `04`, `05b`, `09`, `10` | Owner decisions, gate dispositions, acceptance test, release scope matrix (generated by `14_scripts/fa01_build_registers.py`) |

Offline Legal/IP hard copies are referenced only as "OFFLINE HARD-COPY EVIDENCE RETAINED BY BRAND OWNER". They were not supplied, requested or read.
""")
print("authorized" if AUTH else "proposed", "docs written")
