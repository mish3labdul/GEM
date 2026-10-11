# 02 · Current Remote State (read-only, collected 2026-10-09)

All values below come from `git remote -v`, `git ls-remote`, `gh repo view`, `gh api` (GET only) and `gh pr list`. Raw output: `evidence/01`–`06`, `15`. No write command of any kind was run.

## Repositories
| Item | `origin` | `letterhead-fork` |
|---|---|---|
| URL | `https://github.com/mish3labdul/GEM.git` | `https://github.com/mashaelalh/GEM.git` |
| Owner / name | `mish3labdul/GEM` | `mashaelalh/GEM` |
| **Visibility** | **PUBLIC** (`isPrivate:false`) | **PUBLIC** (`isPrivate:false`) |
| Default branch | `main` | `main` |
| GitHub "fork" of another repo? | No (`isFork:false`) | No (`isFork:false`): an independent public repository |
| Created / last push | 2026-10-06T11:21:26Z / 2026-10-08T00:26:45Z | 2026-10-07T12:45:09Z / 2026-10-08T00:16:57Z |
| Licence declared | none (`license:null`); no LICENSE/NOTICE file at repository root | none |
| Forks / stars / watchers (at query) | 0 / 0 / 0 | 0 / 0 / 0 |
| Forking allowed | Yes | Yes |
| Archived / Pages | No / no Pages | No / no Pages |
| Secret scanning (as visible to this account) | not visible (`security_and_analysis:null`) | enabled, with push protection enabled |
| Authenticated account's permissions | pull only (`push:false`, `admin:false`) | admin, maintain, push |

Authenticated GitHub account: `mashaelalh` (user). Token scopes: `gist, read:org, repo, workflow` (token value redacted in evidence). The permission values are as reported by the GitHub API for the `gh` token; the separate Git credential used by `git push` was **not** tested.

## Branches and refs on the remotes
| Remote | Heads |
|---|---|
| `origin` | `main` = `4ea0d11`; `claude/pensive-mayer-s1xbmb` = `3ba158e`. No tags. |
| `letterhead-fork` | `main` = `334744c`; `claude/pensive-mayer-s1xbmb` = `18c44b1`; `claude/gem-letterhead-v1.1-rev03` = `3f88732`; `codex/gem-letterhead-v1` = `59cac07`. No tags. |

`origin` also holds pull-request refs `refs/pull/1…11/head` (and `refs/pull/10/merge`). Pull-request refs keep their objects reachable on the repository even if a source branch is deleted.

## Is ODI01-R1 on a remote?
- Current worktree branch `claude/gem-worktree-safety-30b559` (HEAD `209c934`): **not on `origin`, not on `letterhead-fork`**. It has no upstream and no remote configured (`push.default` unset).
- AFC / ODI01 / ODI01-R1 candidate branches: **none** on either remote. No AFC/ODI01/Finalization/Implementation_Candidate path exists anywhere in the remote history that was examined (`evidence/09`).

## Pull requests
| Repo | PR | State | Branch → base | Relates to candidate work? |
|---|---|---|---|---|
| `origin` | #1–#9, #11 | MERGED | `claude/pensive-mayer-s1xbmb` ↔ `main` | Earlier brand work (audit, RC2 synchronization, asset kit, Part D, letterhead Rev03). Not AFC/ODI01/R1. |
| `origin` | #10 | **OPEN** | `codex/gem-letterhead-v1` (head repo `mashaelalh`) → `main` | Letterhead v1.0 working application. Its head ref exposes v1.0 files (see `03`). |
| `letterhead-fork` | #1 | **OPEN** | `claude/gem-letterhead-v1.1-rev03` → `codex/gem-letterhead-v1` | Letterhead Rev03. |
No PR exists for AFC01, AFC02, ODI01 or ODI01-R1.

## Are candidate binaries or audit packages already exposed?
- AFC01/AFC02/ODI01/ODI01-R1 packages and decks: **no** (not in remote history).
- Audit and QA documents: **yes**, earlier ones. `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md`, `qa/`, `GEM_V3_RC2/03_qa/` and the letterhead QA evidence are public (see `03`).
- Binary decks and PDFs: **yes**, the RC2 release decks and PDFs of Parts A–D (not the ODI01-R1 candidates).

## Practical constraints that bear on D7
1. Making `origin` private requires admin rights on `mish3labdul/GEM`; the authenticated account does not have them.
2. A push to `origin` is reported as not permitted for the authenticated account; a push to `letterhead-fork` is.
3. There are two public repositories carrying overlapping GEM history; a visibility decision that covers only one leaves the other public.
