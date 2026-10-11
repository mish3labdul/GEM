# 11 · FD01 — Governance Synchronization Log

**GEM™ V3.0 RC2 — OWNER ACCEPTED WITH FORMAL DEFERRALS · SYNCHRONIZED · OWNER ACCEPTED AS-IS · FORMAL DEFERRALS RECORDED · NOT YET FINAL-RELEASE AUTHORIZED**

## Starting state
Branch `claude/gem-worktree-safety-30b559`, HEAD `617456255231a6b36ca5eb688451f8a72eef0eb7` (HR01), working tree clean, in sync with `origin`; `origin/main` `4ea0d117da03850854654288afcdde98f39994d5`.

## Source classification
| Source | Class | Use in FD01 |
|---|---|---|
| `GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx` | CURRENT GOVERNANCE (authority; unchanged) | Exact acceptance wording; status vocabulary (Validation Status list includes "Deferred"); instruction sheet; Owners & Governance notes |
| `GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/` (decision register, gate matrix, OD-G12 wording) | CURRENT GOVERNANCE overlay (preceding layer; not edited) | OD-G09–OD-G12 baseline |
| `GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/` (`07`, `08`, `09`, `10`, `11`, `12`) | CURRENT EVIDENCE (immediately preceding baseline; not edited) | Queue outcomes, HR01 gate states, VoiceOver evidence, Legal/IP inventory |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/10_Arabic_PDF_Status.md` and `03_Owner_Decisions_Carried_Forward.md` | HISTORICAL SNAPSHOT (source of the D8 rule) | D8 operating rule, quoted not edited |
| `GEM_V3.0_RC2_AR01_*`, `GEM_V3.0_RC2_AX01_*`, `GEM_V3.0_RC2_D7_*`, `GEM_V3.0_RC2_NP01*`, `GEM_V3.0_RC2_D3_*`, `qa/` | HISTORICAL SNAPSHOTS | Not edited |
| Root `README.md` | CURRENT GOVERNANCE summary | Pointer updated |
| `CLAUDE.local.md` (two local copies) | LOCAL SESSION INSTRUCTION (not committed) | Guardrails updated |

## Supersession map
| Earlier statement | Where | Superseded by | Treatment |
|---|---|---|---|
| SR-11 / SR-12 "DEFERRED" on content-owner authority (not Accessibility QA approval) | HR01 `07` | FD-G03 / FD-G04 Brand Owner formal deferral | HR01 left as a historical snapshot; FD01 `08` is the current record |
| HR01 next step for VAL-03 / Y01, VAL-04 / Y02: "retain the document in the confidential archive; counsel reviews" and the offer to review scans placed in a local-only folder | HR01 `10`, `11`, `12`, chat | FD-G01 / FD-G06 | Offer withdrawn; no upload is to be requested again; the item stays OPEN with owner-declared offline evidence |
| AC19 "OPEN / HOLDER CONDITION INCOMPLETE" | OD01, HR01 | FD-G02 | Now "OPEN — FORMALLY DEFERRED"; condition itself unchanged |
| Project status "SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE" | OD01, HR01 | FD-G05 | The status now distinguishes owner acceptance from final release (see below). The candidates themselves are still unapproved implementation candidates and no document is released |

## Current status wording (after FD01)
**GEM™ V3.0 RC2 — OWNER ACCEPTED WITH FORMAL DEFERRALS** · SYNCHRONIZED · OWNER ACCEPTED AS-IS · FORMAL DEFERRALS RECORDED · NOT YET FINAL-RELEASE AUTHORIZED.
Other gates not named in FD01 remain open. The words approved V3.0, final release and production release are not used; none applies unless AC20 is separately authorized.

## Files changed outside the FD01 package
| File | Change |
|---|---|
| `README.md` | One added paragraph pointing to FD01 with the owner-acceptance status wording; the existing OD01 pointer line is left as it was |
| `CLAUDE.local.md` (both copies) | Local-only; adds the offline-evidence rule (do not request uploads) and the status wording. Not committed |

No AR01, AX01, OD01, HR01, D7, NP01, D3 or Register file was edited.

## Local operating rule added (not committed)
Confidential Legal/IP evidence is never to be requested for upload or digitization; owner-declared offline evidence is recorded as OWNER DECLARED.

## AC20 dependency reassessment
FD01 does not change AC20's status: **OPEN / FINAL BRAND OWNER RELEASE AUTHORIZATION PENDING**. It changes how three workstreams are classified (from unresolved to FORMALLY DEFERRED / OWNER ACCEPTED). A dedicated AC20 decision may now be taken as a separate step; it should state explicitly:
1. whether a formal deferral satisfies the dependency (OD-G12 wording allows "formally deferred by authorized owners") against the Register instruction not to authorize AC20 while critical gates remain open and that critical gates be closed;
2. the named Brand Owner holder the Register requires to issue the authorization;
3. the disposition of every other open gate (list in `09`);
4. whether the D8 external-issue block stays.
FD01 takes none of these decisions.
