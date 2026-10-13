# Delivery and recovery

Candidate: **v0.5.4 / PROPOSED WORKING PREVIEW**. Branch: `codex/gem-assets-website-refinement-20261013`. Base: `codex/gem-concept-discussion-20261011`, commit `9fad24f76c7eeb2d39d20142a46a0f3119719c51`. Submit as a separate draft PR targeting that branch. No merge, deployment or release.

## Review artifacts

- index.html: before/after comparisons and link to candidate website.
- CHANGE_REGISTER.md and placement-register.csv: exact scope, asset identities and retained qualifications.
- VERIFICATION.md and suite summaries/checks: 484 regression, 81 correction/font and 50 layout assertions, all passing. Review-page checks pass 20/20, including actual required fonts, references, reflow and local inventory filter.
- collection-validation.json: repository validation with remote checks and checksums enabled; source/release identity and current preview packaging validated.
- source-comparison.csv and source-preservation.json: preserved standalone/supplied bytes and source reconciliation.
- CODE_REVIEW.md: focused source and public-payload review.

The initial collection check rejected stale active destinations for the two changed files. Those inventory entries now resolve to exact archived bytes and two new v0.5.4 entries preserve the continuing lineage. The validator was not relaxed. Initial failure and complete raw browser runs remain local.

## Preview ZIP

`website/previews/GEM_Website_Preview_v0.5.4_2026-10-13.zip`: 80 files, exact site-only membership and bytes. SHA-256: `4f22b59fdbb331c5556f2f2318869880f76e405843e733c076d58ec79b8dc056`. Existing packages remain unchanged.

## Recovery

Restore only homepage and CSS from `archive/website-v0.5.3-before-asset-refinement/site/` in a new corrective commit and update version/provenance/preview manifests accordingly. Preserve branch, tag, release and commit history. Never reset or force-push the parent/Arabic branches.

Unresolved new images and the complete 360-file catalogue remain in the separately delivered local asset-review package. Full review is not a public-use grant; original input files are unchanged. Final GitHub PR identity, remote commit and uploaded-byte verification are recorded in the local remote-verification receipt after push, avoiding a self-referential commit hash.
