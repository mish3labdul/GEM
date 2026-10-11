# 04 · New Exposure If ODI01-R1 Is Pushed

Comparison: objects reachable from `claude/gem-worktree-safety-30b559` (HEAD `209c934`) **minus** objects already reachable on `origin` (branches and all pull-request heads). Per-file detail: `04_D7_New_Exposure_Inventory.csv` (164 rows). Method and rules: `scripts/d7_build_inventory.py`. **Sensitivity labels are rule-based decision aids, not legal conclusions.**

## Size
| Measure | Value |
|---|---|
| New commits | **2** (`a5d9acc` reconcile; `209c934` closure) |
| New objects | **197** |
| New files (one folder: `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/`) | **164**, **0 already on the remote** |
| Raw size | ≈ **54.9 MB**; estimated upload (pack to stdout, nothing written) ≈ **51.3 MB** |
| Existing files modified | **0** (no tracked file outside the folder changes) |

## By type (all new)
| Type | Files | Size |
|---|---|---|
| PPTX candidate decks (editable) | 4 | 38.6 MB |
| PDF exports of the candidate decks | 4 | 9.6 MB |
| PNG before/after slide renders | 64 | 6.0 MB |
| Markdown reports and records | 32 | 0.22 MB |
| CSV registers and matrices | 16 | 0.22 MB |
| Python QA / build scripts | 22 | 0.17 MB |
| JSON (manifest, QA results, tokens, evidence) | 10 | 0.12 MB |
| Text (SHA-256 lists, Git evidence) | 11 | 0.03 MB |
| CSS (candidate tokens) | 1 | 0.01 MB |
Editable / source-type files: **96 of 164**. Hash lists: `MANIFEST.json`, `SHA256SUMS.txt` (hashes of the files above).

## What it would newly publish — answers to the specific questions
| Question | Answer | Where |
|---|---|---|
| Draft internal commentary? | **Yes.** Executive summary, trace, change log, PR proposal and closure notes written for internal review | `01`, `04`, `12`, `15`, `16` |
| Open legal/IP questions? | **Partly.** The R1 folder records the open gates (VAL-03/04/05/06 and D7) in the same terms as already-public registers. The explicit Legal/IP question list is in **this D7 package**, which is not yet in any commit | `14`; `08` here |
| Validation gaps? | **Yes.** What is untested (native PowerPoint, Word, Acrobat, AT), the consistency/coverage limits, the hierarchy limitation on nine slides | `12`, `14`, `07` |
| Governance decisions? | **Yes.** Owner decisions D1–D8 and AC20 status, the 400-only decision and the closure decision | `03`, `04` |
| Unpublished visual candidates? | **Yes.** 4 PPTX + 4 PDFs labelled "ODI01-R1 CANDIDATE (UNAPPROVED)" and 64 render images | `19_candidate_documents/`, `18_qa_evidence/render/` |
| Source / editable brand files? | **Yes.** 4 editable decks and the candidate token JSON/CSS. **Not** new: logo masters, font binaries, the Register, DOCX templates | CSV |

## What it would **not** add
No font binaries; no logo vector masters; no Register workbook; no new image assets (the Part D candidate deck re-embeds the AI-generated concept images that are already public in the Part D original and release decks, as a new file); no secrets (0 pattern matches); no modification of any public file.

## Items with their own sensitivity notes
- **Local machine detail:** `02_Preflight.md`, the Git-evidence files and the investigation record contain absolute local paths (including a macOS user-directory name), the committer's `noreply` identity and ref history.
- **Document metadata:** the Part D candidate deck repeats the creator/last-modified-by metadata already present in the public Part D files; Parts A–C candidates carry none.
- **Third-party package hashes:** the ODI01 delivered-zip hashes appear in the manifest and preflight (hashes only; the zips are not included).

## This D7 package, if committed on the same branch
It is documentation only (34 small files, ≈ 0.3 MB including the raw evidence extracts) but it contains the open Legal/IP questions and risk ratings. **If it is committed on `claude/gem-worktree-safety-30b559`, a push of that branch would publish it too.** Whether it should travel on a pushed branch is itself a point for the owner and Legal/IP (`08`, Q5).

## Retraction limits
A branch push uploads objects to the host. Deleting the branch later removes the name, not necessarily the objects: clones, forks (forking is enabled), caches, and any pull-request ref keep them reachable, and removal from the host is not under this repository's control. Treat anything pushed to a public repository as disclosed.
