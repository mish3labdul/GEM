# 10 · Evidence Index

Collected 2026-10-09 (read-only). Local state: branch `claude/gem-worktree-safety-30b559`, HEAD `209c934` before this package. Candidate decks are **referenced by path and hash, not copied**. Names in the brief's task list map to this package as: `D7_New_Exposure_Inventory.csv` = `04_D7_New_Exposure_Inventory.csv`; `D7_Risk_Matrix.csv` = `06_D7_Risk_Matrix.csv`; `D7_Legal_IP_Repository_Visibility_Decision_Brief.md` = `07_…`; `D7_Owner_Decision_Record.md` = `09_…`.

## Raw evidence (`evidence/`)
| File | Content | Supports |
|---|---|---|
| `01_local_git_state.txt` | branch, HEAD, `git remote -v`, `git branch -a -vv` | `02` remotes; branch absent from remotes |
| `02_ls_remote.txt` | `git ls-remote` heads/tags for both remotes; `refs/pull/*` on `origin` | `02` heads, no tags, PR refs; no R1/AFC/ODI branch |
| `03_gh_repo_view_*.json` | `gh repo view` (visibility, default branch, dates, licence) for both repos | `02` visibility PUBLIC, default `main`, no licence |
| `04_gh_api_repo_*.json` | `gh api repos/<repo>` (GET): forks/stars/watchers, allow_forking, security_and_analysis | `02` |
| `05_gh_pr_list_*.json` | `gh pr list --state all` for both repos | `02` PR table (#10 open, head owner `mashaelalh`) |
| `06_gh_auth_status_redacted.txt` | authenticated account and scopes (token redacted) | `02` |
| `07_baseline_tree_4ea0d11_ls-tree.txt` | every file, size and blob of the baseline tree | `03` counts and sizes |
| `08_origin_exposed_tips.txt` | commits used as the `origin`-exposed set (branches + PR heads) | `03`, `04` |
| `09_origin_exposed_paths_ever.txt` | every path ever present in that set (755) | `03` history, removed files |
| `10_font_binaries_in_origin_history.txt` | font binaries in `origin` history (12) | `03`, `05` fonts |
| `11_ai_imagery_mentions_baseline.txt` | baseline text mentioning AI-generated imagery | `03`, `05` VAL-06 |
| `12_secret_pattern_scan_baseline.txt` | secret-pattern scan of baseline text (0 matches) | `03` |
| `13_new_exposure_summary.json` | totals for the new-exposure inventory | `04` |
| `14_license_file_search.txt` | search for LICENSE/NOTICE at repository root (none) | `02`, `05` |
| `15_gh_permissions_of_authenticated_account.txt` | permissions of the `gh` token on each repo | `02`, `07` §8 |
| `16_fork_only_objects_note.txt` | `letterhead-fork` objects not reachable from `origin` (2 commits, 204 objects) | `03` |

## Repository evidence cited (baseline `4ea0d11`)
`qa/GEM_V3_RC2_Final_Open_Evidence_Register.md` · `GEM_V3_RC2/03_qa/GEM_V3_RC2_Open_Evidence_Register.md` · `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md` · `Amenities_Portfolio_PartD_RC2/CHANGE_LOG.md` and `README.md` · `GEM_Brand_Assets_v1.0/README.md` · `README.md` · `GEM_Letterhead_Set_v1.1_Application_Revision_03/00_source/fonts/*/OFL.txt` and `Original_Font_Manifest.json`.

## ODI01-R1 evidence cited
`GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/18_qa_evidence/push_readiness_assessment.md` · `main_ref_movement_investigation.md` · `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/MANIFEST.json` and `SHA256SUMS.txt` · `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/07_Font_Claim_File_Matrix.csv`.

## Candidate artifacts (by path and hash, from the ODI01-R1 manifest)
| Candidate file (referenced, not copied) | SHA-256 | Bytes |
|---|---|---|
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pdf` | `adadbc204371a073d941b85341e611e189582b643807992bd932804197fd1db7` | 4,126,338 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx` | `04d325f83fc77a01220430c00688d73529ed6de20e912fcda9ef2ddfb5bec9e1` | 29,075,140 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Brand Guidelines V3.0 — Part A — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pdf` | `0ac4f9dc6d565feaa999b1a92022ea4633044657dd6533727eb3e2016b2b29da` | 3,977,305 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Brand Guidelines V3.0 — Part A — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx` | `86019d1e83bcf84225b95c0caf6cd2f6bead83e596dc338aabf31de4e027d3d3` | 8,402,140 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Digital Design System V3.0 — Part B — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pdf` | `1ac8892a8948340c0a1ec731f1207fbc7495833df4827ae358c58082c7128240` | 511,061 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Digital Design System V3.0 — Part B — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx` | `22802377eb73448ce3c9c7a0e9d2d3818195d19172f7c07470a415f03d975777` | 158,012 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Production Standards V3.0 — Part C — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pdf` | `a71de0ecd39355739627dc0c61c856e36aafd2e48d10b040aa64423d6af81eb6` | 985,365 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Production Standards V3.0 — Part C — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx` | `add4269aa97af6046c2be17758450525a2e2cf4ba613c67f5e797461314ed4e6` | 948,316 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.css` | `55a22d5fc301635ddb464cde449ec09533c8d3ee8848dccd7b2fa33c63475425` | 10,995 |
| `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/tokens/gem-tokens.v3.0-rc2.ODI01-R1-candidate.json` | `35f413769c72dd37fbfd2856dae7ef09989a6877c796a1ff35e2ea34adee41c0` | 25,977 |

## Method notes
- Read-only commands only. GitHub queries were `gh repo view`, `gh api` (GET), `gh pr list` and `git ls-remote`.
- "Already on remote" = blob present in the object set reachable from `origin/main`, `origin/claude/pensive-mayer-s1xbmb` and every `refs/pull/*/head` commit held locally. `refs/pull/10/merge` was not available locally and adds no new paths beyond its parents.
- Sensitivity labels in `04_D7_New_Exposure_Inventory.csv` and ratings in `06_D7_Risk_Matrix.csv` are rule-based decision aids and carry no legal weight.

## Not verified
Content of images (third-party marks inside the 15 AI-generated images and the renders); whether third-party clones or caches of the public repositories exist; the Git credential's real push rights (only the `gh` token's reported permissions); GitHub-side security settings of `origin` (not visible to this account); the `letterhead-fork` repository's settings other than those shown in the evidence.
