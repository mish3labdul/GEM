# Local `main` ref movement — read-only investigation (ODI01-R1 closure)

**Scope:** read-only. No branch, ref, index or working-tree file was modified by this investigation. Raw command output is preserved in `18_qa_evidence/git_evidence/` (file names below). Evidence was collected 2026-10-09 ≈ 01:49 +0300.

## Verdict
**CAUSE NOT ATTRIBUTABLE FROM AVAILABLE GIT EVIDENCE.**

Git proves *what* moved, *when* and *to what*. It does not identify *which program or person* ran it. Circumstantial timing is recorded below, clearly marked as such. No actor is asserted.

**Correction to earlier ODI01-R1 statements.** Earlier text said the primary checkout was "not modified". That was true of every command I ran, but it was **not true of the primary working tree**: it was fast-forwarded at the same second as the ref move (see answer 6). The statement in `02_Preflight.md` has been corrected accordingly.

## Answers to the eight questions
| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Exact timestamp of the `main` ref movement | **2026-10-09 01:10:05 +0300** (epoch 1791497405) | `git_reflog_show_main.txt`; `common_git_dir_logs_refs_heads_main.txt`; mtime of `.git/refs/heads/main` = 01:10:05 |
| 2 | Old SHA | `334744c72dbbb6681034996fcca595213a7623a2` (main since the clone, 2026-10-07 15:17:44 +0300) | same |
| 3 | New SHA | `4ea0d117da03850854654288afcdde98f39994d5` (= `origin/main`; GitHub merge of PR #11, committed 2026-10-08 03:26:45 +0300) | same; `extra_readonly_checks.txt` |
| 4 | Reflog action / message | `merge 4ea0d117da03850854654288afcdde98f39994d5: Fast-forward`, recorded under identity `mashaelalh <51502047+mashaelalh@users.noreply.github.com>` (the global `~/.gitconfig` identity, so it does not discriminate between programs) | `git_reflog_show_main.txt` |
| 5 | Cause: fetch / pull / merge / reset / checkout / GitHub Desktop / Claude Code / other / unknown | **Unknown.** The message form is that of a fast-forward merge by commit SHA. It is **not** the form `git pull` or `git fetch` write (`pull: Fast-forward`, `fetch …`), not a reset, not a checkout. Beyond that the log does not name a program. Two anomalies prevent more: (a) the primary's `HEAD` reflog has **no** entry for this move, which a plain `git merge` run inside the primary would normally also write; (b) `origin/main` and `origin/claude/pensive-mayer-s1xbmb` were updated without any remote-tracking reflog entries. No git hooks are installed. No git process was running when checked. | `git_reflog_all.txt`; `extra_readonly_checks.txt` |
| 6 | Did the primary checkout working tree change? | **Yes.** The 143 files of `GEM_Letterhead_Set_v1.1_Application_Revision_03/` and `README.md` (the only paths that differ between `334744c` and `4ea0d11`) have birth / modify time **01:10:05**, the same second as the ref move. The primary's tracked files now equal `4ea0d11` (`git diff --quiet HEAD` clean). Its untracked entries (`.DS_Store` files, `GEM_Letterhead_Set_v1.0/`) are unchanged; `GEM_Letterhead_Set_v1.0/` last modified 2026-10-08 23:51:11, before the move. The primary's `.git/index` mtime is 01:17:08, after the move; I ran read-only `git status` against the primary around then, which can refresh the index stat cache, but the evidence does not let me separate that from any other cause. | `extra_readonly_checks.txt`; `git_status*.txt` |
| 7 | Was any authoritative source file modified? | **Content: no divergence.** The only paths touched are the two commits' own paths (letterhead Rev03 folder, `README.md`), and they now equal the committed content of `origin/main` / `4ea0d11`. In this worktree (created from `4ea0d11`) the same paths are byte-identical to the committed objects, and the R1 commit adds only the new ODI01-R1 folder (`git diff a5d9acc^ a5d9acc` touches no tracked file). **Working-tree state of the primary: yes, advanced to `4ea0d11`** (answer 6). | `git_status.txt`; commit `a5d9acc` |
| 8 | Does it affect ODI01-R1 audit lineage? | **No.** R1 was based on `HEAD` = `origin/main` = `4ea0d11`, as the brief required, and never on local `main`. `origin/main` was already `4ea0d11` from 2026-10-08 23:32:12, so local `main` was merely stale until 01:10:05 and then caught up to the commit R1 already used. The brief's "Primary local main may be stale. Do NOT reset … to stale local main" condition therefore described the state before this move; it no longer applies. The R1 commit's parent is `4ea0d11`. | `git_log_graph_all_30.txt`; `git_reflog_all.txt` |

## Timeline (Git evidence)
| Time (+0300) | Event | Source |
|---|---|---|
| 2026-10-07 15:17:44 | `main` created by clone at `334744c` | main reflog |
| 2026-10-08 23:32:12 | `origin/main` ref file written (value now `4ea0d11`); no reflog entry | ref mtime |
| 2026-10-08 23:50:41–23:51:11 | stash + `checkout: moving from claude/gem-letterhead-v1.1-rev03 to main` in the primary (HEAD → `334744c`) | `.git/logs/HEAD`; `git_reflog_all.txt` |
| 2026-10-09 01:09:57 | this worktree's admin directory (`.git/worktrees/gem-worktree-safety-30b559/`) created | directory mtime |
| 2026-10-09 01:09:58 | files checked out in this worktree | file birth time |
| 2026-10-09 01:10:04 | `origin/claude/pensive-mayer-s1xbmb` ref file written; no reflog entry | ref mtime |
| **2026-10-09 01:10:05** | **`main`: `334744c` → `4ea0d11` (`merge …: Fast-forward`); 143 + 1 working-tree files in the primary created/modified** | main reflog; file times |
| 2026-10-09 01:40:38 | R1 commit `a5d9acc` on `claude/gem-worktree-safety-30b559` (parent `4ea0d11`) | branch reflog |

## Circumstantial observations (not attribution)
- The move came **8 seconds after** this worktree was created and about **1 second after** the `origin/claude/pensive-mayer-s1xbmb` ref was written. That coincidence is consistent with tooling that prepares a worktree (fetch, then bring local `main` up to date), but Git does not record the caller, so this is not established.
- In this session, my first `git worktree list` showed `main` at `334744c` and my second command showed `4ea0d11`. That is a conversation observation, not Git evidence. It places the move between my first and second commands. Every command I issued in those calls was read-only; none wrote to `main`, to the primary working tree or to any ref. I cannot rule out that another process ran at that moment, and I do not claim to.
- The identity on the reflog line is the machine's global Git identity and is shared by every program that uses this Git installation.

## What the movement does and does not affect
- ODI01-R1 candidate files, manifests and QA: **unaffected** (they depend on `HEAD` 4ea0d11, `origin/main`, and the committed originals, all unchanged).
- Authoritative originals: unchanged relative to `4ea0d11`; the primary working tree now matches them.
- Nothing was lost: the primary's pre-existing untracked files are intact, and no stash or branch was altered by the move (the pre-existing `refs/stash` entry dates from 2026-10-08 23:50:37).
- Push-readiness: **non-impacting** for a branch-only push of `claude/gem-worktree-safety-30b559`, which does not involve local `main`.

## Not established
Which program ran the fast-forward; why the primary's `HEAD` reflog lacks the entry; why the remote-tracking refs lack reflog entries; whether a pending uncommitted change existed in the primary at that moment (none is visible now). These are stated as unknown, not inferred.

## Raw evidence files (`18_qa_evidence/git_evidence/`)
`git_reflog_show_main.txt` · `git_reflog_all.txt` · `git_log_graph_all_30.txt` · `git_worktree_list_porcelain.txt` · `git_status.txt` (collected when the worktree was clean, before this closure's new files) · `git_status_porcelain_v2.txt` (empty = clean) · `common_git_dir_logs_refs_heads_main.txt` (`.git/logs/refs/heads/main` from the common Git directory) · `extra_readonly_checks.txt`.
