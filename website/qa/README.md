# GEM local QA

Run both suites after changes. Use a new evidence directory; neither command publishes,
submits enquiries or follows an email-app link. Both start their own 127.0.0.1 static server.

```sh
python3 qa/run_qa.py --root site --out-base <new-evidence-directory>/regression
python3 qa/run_corrections_qa.py --root site --out-base <new-evidence-directory>/corrections
```

Requires Python, Playwright and its Chromium binary. The original suite also locates the
available axe-core script (or accepts `--axe /path/to/axe.min.js`). See its `--help`.
Each suite refuses to overwrite a timestamped run folder and exits nonzero on failure.

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

Latest authorized correction evidence: `../records/remediation-2026-10-11-01/START_HERE.md`.

## Bilingual working v0.6.0

Run `python3 website/qa/run_arabic_qa.py --root website/site --out-base <fresh-directory>` from the repository root in addition to the English suites. The Arabic suite checks all six routes, reciprocal language links, responsive layouts, keyboard navigation, Arabic runtime messages, both draft flows, Western-digit validation, exact long room estimates, LTR isolates, fail-closed/no-JavaScript behavior and actual Chromium glyph fonts. The documented interim Noto Sans Arabic Regular 400 is required for Arabic; synthetic styling and unintended glyph fallback fail. The original two-Latin-face discussion above applies to the historical baseline. Linguistic, native screen-reader, other browser-engine and email-client acceptance remain separate gates.
