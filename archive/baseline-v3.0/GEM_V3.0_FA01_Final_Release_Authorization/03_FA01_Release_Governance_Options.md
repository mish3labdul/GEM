# 03 · FA01 — Release Governance Options (decision preparation; PRE-DECISION SNAPSHOT)

> **PRE-DECISION SNAPSHOT.** This file was written before the Brand Owner decided. The body below, including its banner, AC20 status and "not selected" markers, is preserved as written. What was decided is in `04_FA01_Final_Owner_Decisions.csv` and `02_FA01_AC20_Decision_Record.md` (A3, C2, E yes, Brand Owner Mashal; AC20 authorized under the rule in `05`).

**GEM™ V3.0 RC2 — OWNER ACCEPTED WITH FORMAL DEFERRALS · NOT YET FINAL-RELEASE AUTHORIZED · AC20 OPEN**
This file prepares the Brand Owner's decisions. It decides nothing. No option is selected here.

## 1. The tension, stated without reconciling it
| Source | What it says |
|---|---|
| Approval Register, *Instructions* | "Do not authorize AC20 while critical gates remain open." "A deferred item remains outside approved V3.0 scope until revisited." Before AC20: "replace all TBD governance holders with actual names, close critical legal/production/Arabic/accessibility gates, and record evidence references." |
| Approval Register, AC20 row | "Final release authorization must follow completion of critical evidence gates and be issued by the named Brand Owner." |
| Approval Register, AC19 row and *Owners & Governance* | Governance model approved; "actual named role holders must be assigned before release"; each holder "must be recorded before AC20 final release authorization." |
| OD-G12 (Brand Owner, 2026-10-09) | AC20 authorization "shall occur only after the required upstream … evidence has been satisfactorily dispositioned or formally deferred by authorized owners." |
| ODI01 adoption of the Register | The Register is the owner-adopted working decision baseline; "evidence-required and deferred decisions remain subject to their stated gates." |
| D8 (Brand Owner, ODI01) | Internal working use allowed with markings; external issue of Arabic/bilingual DOCX/PDF blocked until the listed native tests pass. |

Reading: OD-G12 is a later owner decision, but it did not amend the Register, and the Register is first in the repository's authority order. The two cannot both be applied literally to a release with open critical gates. The Register's own "deferred = outside approved V3.0 scope" rule offers a path (limit the release scope), but only an explicit owner rule makes it work for AC20.

## 2. Two dependencies the three decisions rely on (need explicit answers)
**E. Is the independent-legal-clearance requirement waivable by the Brand Owner?** VAL-03 / Y01 are owned by Legal / IP Counsel and their criterion reads "target-market clearance or documented legal advice". Option A2 as drafted applies only where the deferral "does not involve a non-waivable external/legal requirement". Whether VAL-03 / Y01 (and VAL-04 / Y02) are such a requirement is a question only the Brand Owner can decide; it is not inferred here. If the owner treats them as non-waivable, A2 cannot apply to them and A3 would have to exclude what depends on them.

**F. The other open gates.** FD01 deferred three workstreams. About twenty other gates and deliverables were never deferred or closed: VAL-01, VAL-02, VAL-07 (production RTL layouts), VAL-08 (contrast, independent QA), VAL-09, VAL-10, VAL-11, VAL-13, VAL-14, VAL-15 (final deliverables), VAL-16, VAL-17, VAL-19, VAL-20, VAL-21, AC07, AC10, AC17, OD-TPL, OD-SRC (VAL-12 is Deferred; VAL-18 is not allocated). An AC20 test of "closed, formally deferred, or explicitly excluded from release scope" needs each of these to be one of the three. Under A3 the natural treatment is explicit exclusion from the release scope; that needs the owner's confirmation after Decisions A–C.

## 3. Decision A — treatment of formal deferrals for final release
| Option | Meaning | Effect on AC20 |
|---|---|---|
| **A1 Strict Register** | Formal deferrals do not permit AC20 closure | AC20 stays OPEN; GEM stays RC2 / owner accepted with formal deferrals / not final-release authorized |
| **A2 Owner governance amendment** | A narrow, explicit owner rule: an upstream gate may be treated as dispositioned for AC20 where the limitation is documented, the owner accepts the residual risk, the work is formally deferred, the deferral involves no non-waivable external/legal requirement, and it is recorded in the release governance record. The Register text is preserved; this is a superseding release-disposition rule | AC20 may be authorized; deferred items are recorded as "ACCEPTED FOR RELEASE UNDER FORMAL OWNER DEFERRAL", never as closed by evidence |
| **A3 Limited release baseline** | GEM™ V3.0 authorized as a controlled final brand-system baseline with explicit artifact-specific exclusions (for example Arabic/bilingual DOCX/PDF not authorized for external issue; Windows validation deferred; Legal/IP independent verification deferred / owner accepted) | AC20 authorized with release-scope exclusions; nothing unperformed is called PASS. *Recommended in the brief; not selected.* |

## 4. Decision B — canonical Brand Owner holder
The Register requires the named Brand Owner to issue AC20. The exact name must be given by the Brand Owner. Nothing is inferred, no title, signature, employer or legal entity is added. Naming the Brand Owner does not close AC19 (11 other canonical holders are unnamed unless also named).

## 5. Decision C — D8 external-issue policy
| Option | Meaning |
|---|---|
| **C1 Keep D8 unchanged** | No external issue of affected Arabic/bilingual DOCX/PDF until Windows Word, Acrobat, NVDA/JAWS and related native tests pass |
| **C2 Narrow D8** | Controlled internal use permitted; external issue of affected Arabic/bilingual DOCX/PDF blocked; unaffected V3.0 artifacts eligible. *Recommended in the brief; not selected.* |
| **C3 Owner waiver** | External issue authorized despite unperformed tests; recorded as OWNER WAIVER / ACCEPTED VALIDATION RISK, never as D8 PASS, PDF validation complete or Windows accessibility verified; requires an Opus check of what is non-waivable before acceptance. *Not recommended by default.* |

## 6. Combinations
- A1 with any C: AC20 stays open; C then only sets the D8 policy going forward.
- A2 or A3 with C1 or C2: AC20 may be authorized with the Arabic/bilingual external-issue restriction intact.
- A2 or A3 with C3: needs the waiver review first.
- Under every option: Part D remains CONCEPT / NOT PRODUCTION ARTWORK; production vectors keep their actual (unaccepted) status unless VAL-02 / AC07 are separately satisfied; no WCAG, Legal/IP or validation claim is made that the evidence does not support.
