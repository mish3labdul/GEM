# GEM Letterhead Change Log

**Review revision R1 · 2026-10-07 · WORKING APPLICATION / PENDING VALIDATION**

Baseline application commit: d0d13bcbf7f398d18a3292d3a994ecaba04ba6d1. Current authoritative main snapshot: 334744c72dbbb6681034996fcca595213a7623a2 (unchanged after fetch).

Only verified corrections from the repository review were implemented:

| ID | Before | After | Reason |
|---|---|---|---|
| I01 | 700/synthetic-bold subject/signatory and inherited heading bold | True Regular 400 text; explicit non-bold styles; only in-use Regular fonts embedded | A 34–35 / B 9–12 weight system; preserve actual 400/500 architecture. |
| I02 | English 10.5 / 14.7 pt leading | English 10.5 / 16.8 pt (1.6×) | Approval Register L12 is highest authority. |
| I03 | Optional tagline 8 pt, zero tracking | Jost 400 at 10.5/15 pt, 0.18em tracking quantized to 1.90 pt (Part B 14/20 px token) | A primary tagline and B minimum tracking-size rules. |
| I04 | Theme/default complex-script fonts and inherited bold left uncontrolled | Inter/Jost Latin plus explicit Noto Sans Arabic complex-script defaults, language tags and intended paragraph direction; header/footer explicitly preserve LTR technical groups; automatic inline-logo header line height avoids clipping | Word editability and B RTL mechanics; prevented a detected inheritance regression during re-render. |
| I05 | 160 mm Latin body, sample lines up to 89 characters | 130 mm Latin running measure, full-width metadata preserved | Register L11 / A 36 reading-measure target. |
| I06 | Broad typography PASS and conflicting specification; old native test evidence | Findings-based report, updated spec and regenerated PDFs/hashes; old native evidence explicitly archived | Evidence/status discipline and current-revision verification. |

All eight template filenames remain stable. Digital/Print portfolios and eight individual PDFs were regenerated; specification PDF/DOCX were regenerated. Authoring sources produce the corrected values. Review tests include explicit and automatic 2/3 pages plus the longest English four-page stress case. Corrected pagination is allowed to change.

Unchanged: actual official SVG/PNG files and colours; 32/36 mm logo widths; A4/page margins/signature allowances; continuation concept; generic contact/reference placeholders; working/pending gates. No External Partners Brief or unapproved source was used. No discretionary redesign, invented production value or owner approval was introduced.

The current QA report gives every issue’s affected file, page/template, problem, governing repository path, exact correction and P0/P1/P2 severity. Current release blockers E01–E05 remain external acceptance/testing actions; no correction falsely closes them. Native Word R1 verification covers English, Arabic and bilingual first-page open/visual inspection only.
