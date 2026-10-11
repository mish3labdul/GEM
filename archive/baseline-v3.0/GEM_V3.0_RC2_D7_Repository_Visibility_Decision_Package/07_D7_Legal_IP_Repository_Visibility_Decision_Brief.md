# 07 · D7 Legal/IP Repository Visibility — Decision Brief

**D7 — LEGAL/IP DECISION PENDING · DO NOT PUSH ODI01-R1 YET · AC20 — OPEN**
GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE

> **Technical push readiness** (suitable for a branch-only push *if explicitly authorized*) is **not** **legal/IP publication authorization** (not given: **do not push until the D7 owner / Legal-IP decision**). This brief prepares the decision; it contains no legal conclusion and no recommendation among the options.

## 1. Decision required
Should the GEM repository, and/or the ODI01-R1 candidate branch, remain publicly accessible, or should visibility change before candidate material is pushed or reviewed remotely? Decision owners: **Brand Owner + Legal/IP Counsel** (role holders TBD in the Register).

## 2. Current repository state (`02`)
- `mish3labdul/GEM` (`origin`) and `mashaelalh/GEM` (`letterhead-fork`): both **PUBLIC**, default `main`, no licence, forking enabled, 0 forks/stars/watchers at query time.
- ODI01-R1 branch: on neither remote. No AFC/ODI01/R1 branch, PR or path anywhere remotely.
- Authenticated account: **pull-only on `origin`** (push and admin not permitted), **admin on `letterhead-fork`**.

## 3. Existing exposure (`03`)
`main` `4ea0d11` (413 files, 162 MB) already publishes: 14 editable PPTX, 30 editable DOCX, 64 logo vector/PDF masters, 3 font binaries (+ 9 more via open PR #10, incl. Bold and variable builds), the Register workbook, tokens, QA/audit documents that state the open gates, and 15 AI-generated concept images with no rights recorded. 0 secret-pattern matches. Document metadata in two Part D files names an individual.

## 4. New exposure if ODI01-R1 is pushed (`04`)
2 commits, 197 objects, **164 new files** (≈ 55 MB raw, ≈ 51 MB packed), none already remote: 4 editable candidate decks, 4 PDFs, 64 render images, candidate tokens, 22 scripts, and internal governance/QA/Git-evidence documents (draft commentary, validation gaps, decisions D1–D8, local machine paths). **No** font binaries, logo masters or Register.

## 5. Open Legal/IP gates (`05`)
Y01/VAL-03 trademark — Not started · Y02/VAL-04 ownership — Not started · Y03/VAL-05/VAL-19 fonts — In progress · Y04/VAL-06 image & AI rights — Not started · AC07/VAL-02 master acceptance — not recorded · Y06 supplier clause — legal review required · third-party marks in images — UNKNOWN · no repository licence · AC20 OPEN.

## 6. Options (none implemented)
| | Meaning | Main effect |
|---|---|---|
| **A** | Keep public; do not push R1 | No new exposure; existing exposure stays; R1 stays local only |
| **B** | Keep public; authorize branch-only push | R1 candidate and internal records become public; objects not recallable |
| **C** | Make private before any push | Future access restricted; **does not undo prior disclosure**; needs admin rights on the repository (the authenticated account has none on `origin`) |
| **D** | Keep public baseline; move candidate work to a private controlled repo | No new public exposure; duplication and lineage-split overhead |
| **E** | Other | Owner-specified; includes deciding which of the two public repositories is in scope |

Three exposure types stay distinct: existing public exposure · new branch exposure · release/distribution. **A branch push is not a release, but it is publication to everyone who can access a public repository; deleting the branch later does not guarantee removal.**

## 7. Risk matrix summary (`06`, ratings with notes; not legal conclusions)
| Dimension (higher = more exposure or friction) | A | B | C | D |
|---|---|---|---|---|
| Trademark exposure | MEDIUM | MEDIUM | MEDIUM | MEDIUM |
| Copyright / ownership uncertainty | HIGH | HIGH | HIGH | HIGH |
| Font licensing | MEDIUM | MEDIUM | MEDIUM | MEDIUM |
| Image / AI rights | HIGH | HIGH | HIGH | HIGH |
| Editable source-file exposure | HIGH | HIGH | HIGH | HIGH |
| Internal governance exposure | MEDIUM | HIGH | MEDIUM | MEDIUM |
| Operational convenience (friction) | LOW | MEDIUM | HIGH | HIGH |
| Collaboration / review convenience (friction) | HIGH | LOW | MEDIUM | MEDIUM |
| Traceability | MEDIUM | LOW | LOW | MEDIUM |
| Rollback / removal limitations | MEDIUM | HIGH | MEDIUM | MEDIUM |
| Future release governance | MEDIUM | MEDIUM | LOW | MEDIUM |

Reading it: the **baseline** rows (trademark, ownership, fonts, image rights, editable sources) are dominated by what is *already public* and look similar across options; the options differ mainly in **new** exposure (internal governance, editable sources, rollback) and in **friction**.

## 8. Operational consequences
- **Which remote?** A push to `origin` is reported as not permitted for the authenticated account; a push to `letterhead-fork` would publish to the *second* public repository. A decision to push must name the target.
- **Visibility change** of `origin` needs its owner's admin rights; changing only one of the two repositories leaves the other public.
- **Open PR #10** on `origin` keeps v1.0 letterhead objects (including Bold/variable fonts) reachable; any visibility or remediation decision should consider pull-request refs.
- **This D7 package**, if committed on the candidate branch, would travel with a push of that branch (it holds the open Legal/IP questions).
- **No setting, branch, tag, PR or release** was changed or created by this work.

## 9. Decision questions for Legal/IP (`08`)
Eight focused questions: continued public hosting while gates are open; font binaries; photography/AI/third-party visuals; logo masters and implementation assets; audit/QA material; private until VAL-03/04/05/06 close; remediation of prior disclosure; branch-only publication before AC20.

## 10. Brand Owner decision field
Choice A / B / C / D / E, reviewer names, date and conditions are recorded in **`09_D7_Owner_Decision_Record.md`**. Until it is completed and signed by the owner and Legal/IP reviewer, **D7 stays open and ODI01-R1 stays local.** AC20 remains OPEN regardless of the choice.
