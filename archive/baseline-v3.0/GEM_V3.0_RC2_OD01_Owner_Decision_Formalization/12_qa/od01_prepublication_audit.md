# OD01 — Pre-publication audit of the outgoing commit range

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
This audit is a content check, not a legal review. It is not a release authorization.

## Scope
Range: `origin/main..HEAD` at the OD01 start, where `origin/main` = `4ea0d117da03850854654288afcdde98f39994d5` (fetched with `git fetch origin --prune`) and HEAD = `f550ddc901c012f0f0c3acfa4893f91569e87384`. This is **9 commits**, 432 files, 29,130 inserted lines, 0 files removed. The OD01 commit is added on top; the whole range, OD01 commit included, is re-scanned immediately before any push with `11_scripts/od01_prepublication_scan.py`.

| Commit | Subject |
|---|---|
| `a5d9acc` | audit: reconcile ODI01 validation-id QA and 400-only font implementation |
| `209c934` | audit: close ODI01-R1 review notes and document git ref movement |
| `ab6d886` | governance: prepare D7 repository visibility decision package |
| `ba526a1` | governance: resolve D3A synchronization and prepare X12 owner decision |
| `ed81b56` | governance: resolve D3B X12 stream as BRAND |
| `00bec02` | qa: add NP01 native PowerPoint validation evidence |
| `1a66c10` | fix: correct Part B slide 30 native PowerPoint clipping |
| `79409f4` | qa: complete AR01 Arabic/RTL native validation and technical metadata corrections |
| `f550ddc` | qa: complete AX01 accessibility validation and safe structural remediation |

All 9 commits carry the author identity of a GitHub no-reply address.

## Method
The scan reads each changed file from the head revision, not the working tree, and covers every commit through the union of touched paths:
- text files line by line;
- Office containers (13 PPTX): every member, including `docProps/*.xml` and all `*.rels` relationship targets;
- PDFs (9) and PNGs (66): raw bytes, including info dictionaries, XMP and text chunks;
- patterns tested against known sample strings before the scan runs (self-test), so an empty result is meaningful.

## Results
| Check | Result |
|---|---|
| Files removed within the range | None |
| Prohibited path names (local-only folders, raw sweeps, `.tsv`, lock/temp Office files, `.DS_Store`, Claude local configuration, recordings) touched by any commit | None |
| Screenshot image files from local-only evidence | None. Files with "screenshot" in the name are registers, pixel-diff JSON summaries and a register-builder script |
| Raw native sweeps | None. `NP01/14_raw_native_sweeps/` holds three committed aggregates that the NP01 evidence index lists as committed; per-part raw sweeps are excluded |
| Credentials, tokens, keys, certificates, cookies | **0 hits** across all text, Office members, PDFs and PNGs |
| Session or temp-container paths, `file:` relationship targets | None |
| **Absolute local filesystem paths** | **7 lines in 3 text files:** `D7/evidence/01_local_git_state.txt` (1), `ODI01-R1/02_Preflight.md` (4), `ODI01-R1/18_qa_evidence/git_evidence/git_worktree_list_porcelain.txt` (2). They contain a macOS user-directory name and the worktree path. The D7 package (`04_New_ODI01_R1_Exposure.md`, `04_D7_New_Exposure_Inventory.csv`) documents this class of exposure. They are not credentials. They remain in committed history; OD01 does not rewrite history |
| Personal data in Office metadata | 2 Part D candidate PPTX carry the creator `Walnut Exporter` and a named individual as last-modified-by. The same values are already public on `origin/main` in the two Part D files, and D7 `03_Existing_Public_Exposure.md` documents it. Parts A–C candidates carry no creator or last-modified-by value |
| Binary additions | 66 PNG before/after renders (64 in `ODI01-R1/18_qa_evidence/render/`, inventoried by D7; 2 in `D3/11_QA_Evidence/`), 13 candidate PPTX, 9 PDFs. None is a local-only screenshot |
| Governance overclaims | The scan flagged 27 lines as possibly positive. All were reviewed by file: D3/ODI01-R1 build and checker scripts and checker test fixtures; descriptions of the D3A correction C4 ("SYSTEM READY" → "NOT RELEASED"); a "This does NOT mean" list; and the ODI01-R1 D6 candidate release notes, a new unpromoted candidate copy of `qa/GEM_V3_RC2_Final_Release_Notes.md` that keeps the older "SYSTEM READY — EVIDENCE GATES REMAIN" line (the same wording is already on `origin/main` in `qa/`) and states in the same text that it is not "Approved V3.0" and that AC20 and the evidence gates remain open. No line states that AC20 is closed, Legal/IP is cleared, Arabic linguistic approval or screen-reader validation is complete, or WCAG 2.2 AA is demonstrated |
| Writes to `main` | None. Only the branch `claude/gem-worktree-safety-30b559` is within the authorization |

## Observations for the owner
1. The 7 local-path lines are the only item that reads as "absolute local filesystem paths" under the publication audit. They were treated as inherited, documented material and not as a blocker. A history rewrite to remove them would be a separate owner instruction; OD01 does not do that.
2. The older "SYSTEM READY" wording in the D6 candidate notes is a quoted legacy phrase, not a current claim: it is the target of D3A correction C4, which is still waiting for promotion (a separate authorized change).
