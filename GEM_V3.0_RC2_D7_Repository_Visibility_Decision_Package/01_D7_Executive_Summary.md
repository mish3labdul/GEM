# 01 · D7 — Repository Visibility: Executive Summary

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**

**D7 — LEGAL/IP DECISION PENDING · DO NOT PUSH ODI01-R1 YET · AC20 — OPEN**

Prepared 2026-10-09 on branch `claude/gem-worktree-safety-30b559` (HEAD `209c934` before this package). Read-only and documentation-only: no push, merge, PR, tag, release, upload, contact, or setting change was made. This package prepares a decision. It does not make it, and it contains no legal conclusion.

## Two different questions — do not merge them
| | State | Meaning |
|---|---|---|
| **TECHNICAL PUSH READINESS** | **Suitable for a branch-only push if explicitly authorized** | Working tree clean; manifest and checksums verify; originals untouched; no unexplained tracked change (see the ODI01-R1 push-readiness assessment). |
| **LEGAL/IP PUBLICATION AUTHORIZATION** | **Not given. Governance state: DO NOT PUSH UNTIL THE D7 OWNER / LEGAL-IP DECISION.** | Both repositories that a push could target are PUBLIC. Trademark, ownership, font and image-rights gates are open. |

Technical readiness does not authorize publication.

## What was found (all read-only, evidence in `evidence/`)
1. **Both candidate remotes are public.** `mish3labdul/GEM` (`origin`, default branch `main`) and `mashaelalh/GEM` (`letterhead-fork`, default `main`) report `PUBLIC`. Neither declares a licence. Both have 0 forks, 0 stars, 0 watchers at query time; forking is allowed on both.
2. **The ODI01-R1 branch is not on either remote.** No AFC, ODI01 or R1 branch, tag or path exists on either remote.
3. **Substantial GEM material is already public** at `main` `4ea0d11` (413 files, 162 MB): 14 editable PPTX, 30 editable DOCX, 64 logo vector/PDF master files, 3 font binaries, the Approval Register workbook, tokens, QA and audit documents that openly state the open gates, and 15 AI-generated concept images with no image rights recorded. Presence is not evidence of authorized disclosure.
4. **`origin` additionally exposes the v1.0 letterhead history** through open PR #10 (`refs/pull/10/head`): 9 more font binaries, including Bold and variable builds that the D5 decision treats as not accepted.
5. **A push of ODI01-R1 would add** 2 commits and 197 objects (≈ 51 MB packed), 164 files in one folder, none of which is on any remote: 4 editable candidate decks, 4 PDFs, candidate tokens, 64 render images, 22 scripts, and the internal governance, QA and Git-evidence documents. It adds no font binaries, no logo masters and no register.
6. **The authenticated GitHub account has no push or admin right on `origin`** (`push:false`), but has admin on `mashaelalh/GEM`. Which remote a "branch-only push" would target, and who can change which repository's visibility, is therefore part of the decision.
7. **Open legal/IP gates**: VAL-03 (trademark), VAL-04 (ownership), VAL-06 (image rights) — Not started; VAL-05 / VAL-19 (fonts) — In progress; VAL-02 (master acceptance) — not recorded.

## Three kinds of exposure (not equivalent)
1. **Existing public exposure** — already in the public repositories and history (`03`).
2. **New branch exposure** — would become public only if the ODI01-R1 branch is pushed (`04`).
3. **Release / distribution** — approved external dissemination or production release. **A branch push is not a release, but it is publication to everyone who can access the repository.** While a repository is public, a pushed branch should be treated as publicly disclosed. Deleting a branch afterwards does not guarantee removal of the uploaded objects (clones, caches, pull-request refs).

## Options (none implemented; none recommended here)
A keep public, do not push · B keep public, authorize branch-only push · C make private before any push · D keep the public baseline, move candidate/audit work to a private controlled repository · E other. See `07`.

## Decision path
Legal/IP Counsel answers the eight questions in `08`; the Brand Owner records the choice in `09`. AC20 stays OPEN regardless.

## Package map
`02` remote state · `03` existing exposure · `04` new exposure (+ CSV) · `05` open legal/IP dependencies · `06` risk matrix · `07` decision brief · `08` Legal/IP questions · `09` owner decision record · `10` evidence index.
