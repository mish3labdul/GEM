# Repository source-of-truth review — 18 October 2026

## Verified baseline

Repository: https://github.com/mish3labdul/GEM (public). Canonical development branch: `main`, GitHub default and protected by the active required-checks ruleset. Audited HEAD: `f743e16b3df831a210c21fa431ef93784617d9a4`. Recent merges: #18 bilingual integration/validator hardening, #17 CI, #13 library organization. No evidence supports replacing main with a working branch.

Required checks on main: `Collection integrity` and `Chromium QA`; strict up-to-date checks enabled. Authenticated access permits push but not administration or ruleset bypass. Classic branch-protection endpoint returned 404; effective rules were verified with rulesets and the applied-branch-rules endpoint. Ruleset `br` is active but has an empty include list; its rules were not returned as effective for main. No required-review rule appeared in the effective rule list. Automatic merged-branch deletion is disabled. No settings were changed.

## Canonical locations

| Information | Canonical location/process |
|---|---|
| Current repository development | main; changes through reviewable PRs |
| Released V3.0 artifacts | documents/released/v3.0 and preserved v3.0 release/tag; original bytes retained |
| Decisions and restrictions | governance records, applicable Approval Register and scoped owner decisions; newer files do not automatically supersede authority |
| English product naming | governance/product-naming-approval-2026-10-18.md; copied from c53cf50625255429c170168ffa59dd0442733c54 without rewriting its historical wording |
| Part E internal-distribution decision | governance/parte-internal-distribution-approval-2026-10-18.md; metadata only |
| Part E internally approved binaries | External controlled private storage, location not yet designated; not the public repo |
| Native static website | website/site; website/records for build-specific decisions/evidence |
| Standalone template preview | Separate audit reference, not canonical website/site; no QA transfer |
| Working localization | documents/working/arabic-localization-l10n01 after explicit provenance reconciliation; never automatic Arabic acceptance |
| Historical copies and previews | archive and versioned preview records; retained evidence, not competing current standards |
| Checksums and migration | governance manifests plus tools validation; refresh deliberately after authorized changes |

## Pending PRs at audit

All four have no GitHub check runs, no formal reviews and no linked closing issues. Aggregate commit status `pending` with no check runs is not a running or passing CI result. Historical QA counts in descriptions were not rerun on these heads. Author-recorded approval comment exists on #14 but is not an independent GitHub review.

| PR | Purpose/base/head | Currency and conflicts | Recommendation |
|---|---|---|---|
| #12 draft | Arabic R4 evidence; base claude/gem-worktree-safety-30b559; head codex/gem-arabic-localization-l10n01 at d8921f13aa485a5afeefb42dd6cbee105eee0149 | 4 ahead/0 behind named base; 4 ahead/8 behind main; simulated merge into main clean | Keep draft. Explicit do-not-merge scope, private/native gates and historical path migration require reconciliation |
| #14 open | Concept/colourway/room estimate decisions; base main; head codex/gem-concept-discussion-20261011 at 9fad24f76c7eeb2d39d20142a46a0f3119719c51 | 2 ahead/5 behind current main; 8 simulated conflicting paths | Do not merge as-is. Reconcile unique decisions/evidence against #18 integration before any closure |
| #15 draft | Arabic website/private document QA controls; base codex/gem-concept-discussion-20261011; head codex/gem-arabic-website-documents-20261012 at c45743c5279e1f49540ca97d1a595ac87e2a18f3 | 3 ahead/0 behind named base; 5 ahead/5 behind main including inherited stack; 17 conflicts against main | Keep draft; extract only approved missing evidence after provenance/native review; do not retarget blindly |
| #16 draft | Hero/package refinement plus style brief; same base as #15; head codex/gem-assets-website-refinement-20261013 at ff36af59454e591d4bb356e89be8cbc64f6f1c5a | 2 ahead/0 behind named base; 4 ahead/5 behind main including inherited stack; 8 conflicts against main | Keep pending disposition. Visual work remains cancelled; preserve unique style-brief/evidence before considering superseded closure |

Path-level overlap against main (including inherited stack) was measured: #14 302 paths, 1 identical / 13 different / 288 absent; #15 665 paths, 7 identical / 22 different / 636 absent; #16 338 paths, 2 identical / 15 different / 321 absent; #12 38 paths absent at their original paths. Absence at an original path does not establish loss: migrated records and semantic overlap require reconciliation. No complete PR is proven redundant by these checks. Merge simulations did not modify branches or worktrees.

## Branch audit

Counts are ahead/behind current main after full-history fetch; age alone is not a deletion criterion.

| Branch | Ahead/behind | Disposition |
|---|---|---|
| main | 0/0 | Keep protected canonical branch |
| claude/gem-worktree-safety-30b559 | 0/8 | Keep: frozen provenance source and active #12 base |
| claude/pensive-mayer-s1xbmb | 0/24 | Keep: frozen provenance source, not disposable merely because merged |
| codex/gem-arabic-localization-l10n01 | 4/8 | Keep: frozen source and active #12 |
| codex/gem-arabic-website-documents-20261012 | 5/5 | Keep: active #15 and unmerged commits |
| codex/gem-assets-website-refinement-20261013 | 4/5 | Keep: active #16 and unmerged commits |
| codex/gem-ci-docs-20261014 | 0/4 | Remote deletion candidate after owner confirmation; #17 merged, no active PR; local checkout retained |
| codex/gem-concept-discussion-20261011 | 2/5 | Keep: #14 head and #15/#16 base |
| codex/gem-handoff-remediation-20261014 | 1/1 | Keep: #18 merged but later naming commit unmerged; local Part E work exists |
| codex/gem-repository-cleanup-20261011 | 0/6 | Remote deletion candidate after owner confirmation; #13 merged, no active PR; local checkout retained |

## Actions and limits

The new documentation PR carries the existing naming decision, this navigation/audit record, and Part E approval metadata. No existing PR was merged, closed, retargeted or updated. No branch/tag was deleted, no history rewritten, no setting changed, no website edited, and no internal deck or PDF uploaded.

Awaiting approval: reconcile/close or replace #14–#16; disposition #12; remove only the two verified merged non-frozen branch candidates; select private storage for Part E binaries. Complete line-by-line code, native localization, accessibility and regulatory acceptance are outside this repository-state audit. Check execution and CI outcomes are recorded in the delivery report/PR, not inferred from old descriptions.
