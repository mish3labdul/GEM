# 06 · OD01 — D7 Repository Visibility Decision

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
REPOSITORY VISIBILITY OWNER DECISION: RESOLVED · LEGAL/IP EVIDENCE: OPEN WHERE REQUIRED · AC20 OPEN

## Current D7 wording (replaces "LEGAL/IP DECISION PENDING — DO NOT PUSH")
| Aspect | Current wording |
|---|---|
| Repository visibility owner decision | **RESOLVED — CURRENT PUBLIC REPOSITORY APPROVED** (OD-G11, Brand Owner, 2026-10-09) |
| Public repository | **APPROVED BY OWNER** for the current repository and future controlled project material |
| Legal/IP evidence | **OPEN WHERE THE GOVERNING GATES REQUIRE IT** |
| Remote operations | **Task-specific only.** The OD01 brief authorizes one controlled branch push after QA. Future remote operations require a new explicit task-specific owner instruction |

Statement to use wherever public visibility is mentioned: *"Public repository visibility has been approved by the Brand Owner. This is not a legal opinion and does not substitute for the Legal/IP evidence required by the Approval Register."*

## Selection label
**OD-G11 — C — CURRENT PUBLIC REPOSITORY APPROVED.** OD-G11 option lettering belongs to the OD01 Owner Decision Register taxonomy and is independent of the historical D7 option lettering. Historical D7 options are preserved as provenance and are not rewritten. The D7 record (`GEM_V3.0_RC2_D7_Repository_Visibility_Decision_Package/09_D7_Owner_Decision_Record.md`) therefore records the decision verbatim and keeps the historical options A–E unticked as provenance; it does not map the decision to any of them.

## Scope
- Covered: `mish3labdul/GEM` (`origin`).
- Not covered: `mashaelalh/GEM` (`letterhead-fork`), a second, independent public repository that carries overlapping GEM history.
- The visibility setting itself is not changed by OD01 and is outside this task.

## What changed in the D7 package
Only `09_D7_Owner_Decision_Record.md` was populated (the record exists to receive this decision), with `MANIFEST.json` and `SHA256SUMS.txt` re-hashed for it. A supersession pointer was added to the manifest. Files `01`–`08`, `10`, `evidence/` and `scripts/` are unchanged and remain the provenance of the analysis.

## Matrix: repository visibility decision versus Legal/IP evidence
| Item | What OD-G11 settles | What stays open |
|---|---|---|
| Repository visibility (owner level) | **RESOLVED** — current public repository approved | Nothing at owner level. Changing visibility later is a separate owner action |
| VAL-03 / Y01 — trademark availability / distinctiveness | Nothing | Target-market clearance or documented legal advice |
| VAL-04 / Y02 — logo artwork ownership | Nothing | Executed ownership or assignment evidence retained with the brand archive |
| VAL-05 / Y03 — font licensing | Nothing | Licences covering intended print, web, app, office and distribution uses; exact builds tested |
| VAL-06 / Y04 — image / model / property rights | Nothing | Rights, source and usage metadata for every approved production image |
| Third-party marks | Nothing | Clearance where applicable |
| Supplier legal clauses (e.g. Part C Appendix B Y06) | Nothing | Legal review |
| Publication rights for each individual asset | Nothing | Per-asset confirmation where the governing gates require it |
| VAL-10 packaging regulatory / claims | Nothing | Per-SKU, per-market evidence |

**No row in the "What stays open" column is closed by OD-G11, by the push authorization, or by the branch being published.**

## Residual exposure noted for the owner
The D7 package (`04_New_ODI01_R1_Exposure.md`, `04_D7_New_Exposure_Inventory.csv`) recorded that ODI01-R1 Git-evidence files carry absolute local paths including a macOS user-directory name, a `noreply` committer identity and ref history. That exposure is documented, not new; the paths remain in the committed history and OD01 does not rewrite history. It is listed again in the pre-publication audit (`12_qa/`) so the owner can see it.
