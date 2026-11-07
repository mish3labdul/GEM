# Obsidian truncation incident — review (written 7 Nov 2026 during M26)

## What happened
At about 05:29 on 7 Nov 2026 an orchestrator Python helper `open(p,'w').write(open(p).read()+text)` truncated four notes in `Projects/GEM website/` (`Current status.md`, `Agent handover.md`, `Open items and owner decisions.md`, `Brand and product decisions.md`) to only the appended text. The error was in the helper: the file is opened for writing (emptied) before the old content is read.

## Recovery performed (≈05:30)
Mounted the Time Machine local snapshot `com.apple.TimeMachine.2026-11-07-052536.local` read-only, restored each note's snapshot content, re-applied this session's two intended line edits and the appended sections via read-fully-then-atomic-replace writes. The truncated files were backed up to `/tmp/vault_truncated_backup/` first. A diff against the snapshot showed only the two intended line changes plus additions.

## What is verified and what is NOT
- Verified: restored files = snapshot content + intended edits (diff). No other vault note changed between snapshot time (05:25:36) and 05:31:30 except `.obsidian/workspace.json` (UI state) and the two new source notes I created (file-mtime scan on 7 Nov, M26).
- NOT verifiable: whether any edit was made to those four notes between 05:25:36 and 05:29 (their mtimes now reflect my overwrite; snapshot content mtimes were 04:03/02:44, consistent with my earlier syncs and no other writer in the snapshot). The snapshot itself cannot prove the absence of edits after it was taken. A diff against the same snapshot cannot establish complete recovery of that window. No later Time Machine snapshot existed at review time to cross-check.
- Likelihood of a lost edit is low (single-user vault, no other agent was writing there), but it is unproven.

## Preventive measures
Atomic write helper (read fully → temp file → `os.replace`) with a unit test that would have caught this bug (M25 `m25_pipeline/`); read-before-write, backup copy before every vault edit, post-write content verification (size and diff vs the pre-edit copy). The recovery record (snapshot name, backup path) is preserved here.
