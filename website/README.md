# GEM website — proposed working preview v0.6.1

The original imported site matched all 80 entries of `GEM_Website_Preview_2026-10-11.zip`. Changed original files are preserved byte-identically under `archive/website-pre-integration-20261014/`; unchanged original files retain their existing destinations. The ZIP SHA-256 is recorded in [source-freeze.json](../governance/source-freeze.json). Local Finder metadata is excluded. The existing post-v0.5.1 correction evidence is preserved in [records/remediation-2026-10-11-01](records/remediation-2026-10-11-01/START_HERE.md). This remains a proposed website, not a release or deployment.

| Folder | Purpose |
|---|---|
| `site/` | Only directory permitted as the public/preview document root |
| `source-images/` | Original imagery and concept provenance; not public |
| `records/` | Historical source/decision/QA records, retired assets, transport copies and correction evidence; not public |
| `qa/` | Maintained regression, correction and actual glyph/fallback checks |
| `previews/` | Versioned site-only downloadable ZIP |

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory website/site
python3 website/qa/run_qa.py --root website/site --out-base ../gem-local-qa/regression
python3 website/qa/run_corrections_qa.py --root website/site --out-base ../gem-local-qa/corrections
python3 tools/package_website.py
```

Keep new QA output outside the repository. The suites create timestamped runs and preserve earlier evidence; writing new runs under `website/records/` adds files outside the collection checksum manifest. Existing tracked historical records remain unchanged. GitHub Actions uses its temporary directory for new evidence; see [CI scope](../tools/README.md#continuous-integration).

QA requires Python, Playwright with Chromium, and Pillow for the visual comparison helper. Font checks fail for missing required faces or unsupported glyphs. Existing Latin fonts do not establish Arabic support. Do not substitute fonts or claim native RTL validation from these checks.

[Historical website README](../archive/website-original/README.md) and existing records retain their original wording and paths. Resolve them through [path-migration.csv](../governance/path-migration.csv); they do not override the current candidate or current limitations. Original imagery and concept status are preserved. Forms draft locally and do not submit to a backend.

Experimental concept packages, independent audit folders, unrelated previews and prior exports are retained at their original local source locations and catalogued as outside this import; the active website does not depend on them. Its selected concept masters and provenance are included under `source-images/`.

## Local integration candidate v0.6.1

The current English/refined and Arabic integrated candidate uses the static site stack. [Integration provenance](records/integration-2026-10-14-01/README.md) records exact input revisions, active file hashes, preserved originals and the current preview. Older previews retain their own immutable membership; they are not expected to match the current candidate. The candidate has bounded technical Chromium evidence only; its Git delivery state is recorded separately in the dated handoff. Arabic linguistic/native/AT, identity master, legal/IP, supplier and production acceptance remain open; B01/B02 and D8 are retained. No deployment or release is implied.
