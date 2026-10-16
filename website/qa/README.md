# GEM local QA

Run all four suites after changes from the `website/` directory. Use a new evidence
directory; none publishes, submits enquiries or follows an email-app link. Each starts
its own 127.0.0.1 static server.

```sh
python3 qa/run_qa.py --root site --out-base <new-evidence-directory>/regression
python3 qa/run_corrections_qa.py --root site --out-base <new-evidence-directory>/corrections
python3 qa/run_refinement_qa.py --root site --out-base <new-evidence-directory>/refinement
python3 qa/run_arabic_qa.py --root site --out-base <new-evidence-directory>/arabic
```

Requires Python, Playwright and its Chromium binary. The original suite also locates the
available axe-core script (or accepts `--axe /path/to/axe.min.js`). See its `--help`.
Each suite refuses to overwrite a timestamped run folder and exits nonzero on failure.

The refinement runner retains `summary.json`, `checks.json` and `environment.json`
after runtime exceptions, including accumulated checks, site hashes and exception
details; the exception still exits nonzero. Its focused evidence-retention tests run
from `website/qa/` with `python3 -m unittest test_run_refinement_qa.py -v`.

`font_validation.py` validates actual Chromium platform glyph usage as well as required
loaded regular 400 Jost/Inter faces. Current visible text, field values and placeholders
form the samples. Required-face errors, system fallback or unsupported glyphs return
**FAIL brand acceptance**. Future Arabic DOM text is subject to the same rule; these Latin
files do not establish Arabic support. The targeted suite includes expected negative tests:
its PASS means it correctly detected a failed brand state, not that blocked fonts or Arabic
fallback are acceptable. No missing font is replaced or approved automatically.

The suites are Chromium automation. They do not establish Safari/Firefox behavior, native
screen-reader acceptance, native browser zoom, actual email-client compatibility, legal
clearance, supplier/production proof or WCAG certification.

The Arabic suite checks the current static-site bilingual journeys, DOM direction,
font usage and local draft behavior. Its automated results do not establish native
Arabic linguistic approval, assistive-technology acceptance or D8 closure.

Latest authorized correction evidence: `../records/remediation-2026-10-11-01/START_HERE.md`.
