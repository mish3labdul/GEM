# Collection tools

Run from any directory; these helpers locate the repository through their own path.

- `python3 tools/validate_collection.py`: verify source dispositions and byte identity, release-copy digests, Unicode/case filename collisions, active HTML/CSS references, catalogue integrity, historical byte identity, frozen remote release/source branches and history-preserving main advancement, and the final collection checksums. Exits nonzero on failure. Use `--skip-remote` for explicitly offline validation, or `--skip-checksums` only while preparing a new checksum manifest. Add `--check-index` before committing to verify Git membership and absence of unstaged tracked changes.
- `python3 tools/package_website.py`: create a versioned, Asia/Riyadh-dated site-only ZIP without overwriting an existing package; excludes cache and Finder metadata and verifies archive membership/bytes.
- `python3 tools/refresh_manifests.py`: deliberately regenerate duplicate and checksum manifests after authorized changes. Run validation again afterward.
- `python3 tools/compare_website.py --baseline <site-directory> --out <new-directory>`: render the immutable baseline and migrated site with identical Chromium settings and compare all three pages at desktop/mobile sizes. Stores paired screenshots and pixel-difference evidence. Requires Playwright and Pillow.

Maintained website QA remains under `website/qa/`. Source-era brand build scripts remain archived as historical helpers, not active tools. These commands do not merge, release, deploy, contact anyone, follow mailto links, or alter original source files.

## Continuous integration

[GEM checks](../.github/workflows/gem-checks.yml) defines two independent jobs for pull requests to any branch, pushes to `main`, and manual runs:

- **Collection integrity** first runs the isolated validator adversarial regression tests from `tools/` using `python3 -m unittest test_validate_previews.py -v`; a test failure fails the job. It then validates migration/source identity, release-copy hashes, public references, preview contents, collection checksums and the Git index. It fetches complete history so the frozen source commits are available. PRs and manual runs outside `main` use the explicit `--skip-remote` mode: the default live-history check requires the checkout to be contained in live `main`, which does not apply to unmerged or stacked PRs. Runs on `main` also check live release/tag/source-branch preservation using a read-only token. PR results do not establish those live checks; retain full remote validation before any authorized delivery.
- **Chromium QA** runs the maintained regression, correction/font, refinement and Arabic/bilingual journey suites. It provisions Playwright 1.57.0 and Chromium in the hosted runner, matching the Playwright version used for local verification. Python 3.12 and Ubuntu 24.04 are explicit runner choices. Each suite writes to a separate directory under `RUNNER_TEMP`, outside the checksummed checkout. After successful runtime provisioning, later suites run even if an earlier suite fails, unless the run is cancelled. Any suite failure keeps the job red.

Action references are pinned to upstream commit hashes. Repository permissions are read-only, checkout credentials are not persisted, and the workflow does not upload artifacts, publish, deploy, submit enquiries, or open email links. Raw evidence is temporary to the runner; step logs retain the check summaries and failures. Local evidence must also remain outside the repository. No new local dependency installation is required by these changes.

Adding the file locally does not activate hosted checks. After separately authorized publication, verify a successful GitHub run and configure required checks (`Collection integrity` and `Chromium QA`) through the owner's branch-protection/ruleset process. No branch-protection change or hosted success is implied. Chromium automation does not establish native Arabic/Office, other-browser/device, screen-reader, email-client, production, legal or WCAG acceptance; B01/B02 and D8 remain open.
