# 12 · Consistency and Coverage Report (ODI01-R1)

## Headline
**20/20 cross-document QA checks passed (0 failed)** and, separately, **112 automated assertions passed (0 failed)** on the R1 candidate decks (A, B, C). The same assertion count (112 passed, 0 failed) holds on the unchanged originals. Validation-ID regression tests: **30/30 passed**.

These are text, metadata and structure checks. They are **not** a statement of full system consistency, and no such statement is made anywhere in this package.

Reports: `18_qa_evidence/consistency_baseline_originals.md` (originals), `consistency_candidates_ODI01_R1.md` (candidates), `cross_document_qa_results.md/.json`. Scripts: `17_scripts/consistency_check_odi01.py` (ODI01 checker, assertions unchanged, candidate-path overrides) and `17_scripts/cross_document_qa.py`.

## What an assertion is
A term present or absent in slide text, tables and notes (palette hexes, family names, status terms, tagline, version string, document ID, authority-list anchor, twelve-role list, stale phrases absent), a PDF tagged flag, picture alt-text counts. No assertion tests meaning, rendering, runtime behaviour or native-application behaviour.

## Reporting categories (kept separate)
| Category | Meaning | Items in R1 |
|---|---|---|
| **AUTOMATED ASSERTIONS** | Re-run by script | 112 text/metadata assertions (originals and candidates) · 20-point cross-document QA · 23 validation-ID regression cases · token verification (all checks PASS, 153 tokens) · OOXML edit verifier (only intended differences) · bold-flag recount (228 → 0) · font binary scan · 135-hit weight search (0 unclassified, 0 class B) · word-geometry comparison of 64 slides · Part D claim scan · repository checksum lists |
| **MANUAL VERIFIED** | Read and judged by the author | Classification of the remaining 500 references and the five wording edits · visual inspection of 25 of the 64 affected slides (individual images and contact sheets) · the hierarchy finding on bold run-in heads · carried-forward ODI01 judgments (register adoption, Part D wording, X12 option comparison) |
| **INHERITED** | Quoted from ODI01 / earlier packages, not repeated | Word for Mac 16.113.3 results · PDFKit copy/search results · letterhead visual parity · earlier `qa/` statements · letterhead structure audit and bilingual hierarchy (ODI01 evidence files) |
| **NOT TESTED** | Not run | Native PowerPoint rendering/accessibility check of any deck · Windows Word · Word Online · iPad · Acrobat (accessibility, Unicode text layer) · screen readers / AT · component bundle runtime (does not exist) · rendered-page contrast · print/colour proofs |
| **NATIVE QA PENDING** | Needs a native application and a person | Title placeholders and reading order (30 slides) · Arabic copy/search in Acrobat and Windows Word · letterhead in Windows/Online Word · R1 candidate decks opened in PowerPoint |
| **SUPPLIER EVIDENCE PENDING** | Needs supplier or physical evidence | CMYK, Pantone, stock/GSM, Delta E, line weights, substrate, tolerances, dielines, physical proofs. None invented |

## Final cross-document QA — 20 separate results
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Register alignment | **PASS** | hash in record=True, equals main=True, exact statement=True, recalculated counts={'Approved': 384, 'Approved with modification': 72, 'Deferred': 2, 'Evidence Required': 8}, role holders TBD=12/12, Dashboard Overall "Not ready"=True, rows=466, rows edited=0 |
| 2 | Parts A/B/C/D terminology | **PASS** | Part A–D reference counts identical between each original and its candidate; no "Part E": A:103 refs, B:29 refs, C:116 refs, D:62 refs |
| 3 | Version IDs | **PASS** | RC2/V3.0 version-string counts original=candidate A:77=77, B:55=55, C:85=85, D:26=26; token meta version/edition/documentId/issued unchanged=True (3.0.0-rc.2, GEM-DDS-V3.0-RC2) |
| 4 | Status vocabulary | **PASS** | all 153 token statuses in ['APPROVED', 'CONDITIONAL', 'PENDING VALIDATION', 'REFERENCE']=True; no deck status word count increased; no banned status word in any added line |
| 5 | Tagline | **PASS** | "HOSPITALITY, IN PERFECT PROPORTION" occurrences original=candidate: A:8=8, B:2=2, C:1=1, D:1=1; no new tagline variant or text |
| 6 | Palette | **PASS** | srgbClr sets in all slide XML identical original vs candidate (A:7, B:8, C:8, D:3 colours); foundation tokens INK #12171D, BEIGE #BCACA7, BLACK #020202, WHITE #FFFFFF intact; CSS raw hex set = those four |
| 7 | Typography families | **PASS** | typeface sets in all slide XML identical original vs candidate; token families unchanged: Jost / Inter / Noto Sans Arabic |
| 8 | Actual available font weights (D5: 400 only, no faux bold) | **PASS** | font files in main: {'Inter-Regular.ttf': 400, 'NotoSansArabic-Regular.ttf': 400, 'Jost-Regular.ttf': 400} (all weight 400, no 500/bold/variable file); brand-font explicit bold runs original={'A': 2, 'B': 121, 'C': 105, 'D': 0} candidate={'A': 0, 'B': 0, 'C': 0, 'D': 0} (current faux-bold dependency = 0); all b="1" runs original=228 candidate=0 (non-brand b="1" candidate=0); standalone "500" occurrences in candidate decks=9, every one marked PENDING / FUTURE DESIGN INTENT=True; four 500-weight tokens keep value 500 and state FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400=True |
| 9 | Token values | **PASS** | 153 tokens: value+type identical=True; names identical=True; CSS declarations (name+value) identical=True; audit_tokens.py on originals: see audit_tokens_original.json |
| 10 | Token statuses | **PASS** | 26 normalizations, 0 promotions, transitions {'APPROVED -> CONDITIONAL': 10, 'CONDITIONAL -> PENDING VALIDATION': 7, 'APPROVED -> PENDING VALIDATION': 9}; dependency-hierarchy check: PASS — 0 |
| 11 | Arabic status | **PASS** | 16 Arabic hierarchy tokens PENDING VALIDATION; Part B slide 12 still "PENDING VALIDATION"=True; "PENDING LOCALIZATION APPROVAL" deck occurrences original=15 candidate=15; present in all Arabic/bilingual letterhead DOCX=True; VAL-07 open in 14 |
| 12 | Asset naming policy | **PASS** | GEM_Brand_Assets_v1.0 working-tree changes=False (none = no source renamed); both mappings cover 34 files with 34 unique names each, 0 collisions with the 11 existing X12-shaped files; doc 13 states no STREAM token is chosen (D3 unresolved); D3B left to owner |
| 13 | Letterhead application state | **PASS** | letterhead package unchanged=True; 8/8 templates carry "WORKING APPLICATION / PENDING VALIDATION"=True; 10 PDFs tagged=True; no Revision 04 artifact exists=True; "R04 unavailable" retired in 09; native Windows Word / Word Online / Acrobat / AT / physical proof listed NOT closed (09, 10, 14) |
| 14 | Production status | **PASS** | no production-ready / print-ready / supplier-spec words in any line added to a candidate deck; "CONCEPT / NOT PRODUCTION ARTWORK" markings original=12 candidate=12; supplier values remain [REQUIRES SUPPLIER] / [PENDING PHYSICAL PROOF] |
| 15 | Validation IDs | **PASS** | VAL ids referenced in 20 R1 documents [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]; allocated set is VAL-01..VAL-21 except VAL-18 (intentionally unallocated); 10 explanatory mention(s) of the unallocated ID classified EXPLANATORY and allowed; active-gate or unknown-ID findings=0; unallocated ID documented in 14/05=True; VAL-05/07/08/13/15/20 listed open in 14; no line closes them [] |
| 16 | Release wording | **PASS** | status label present in 01=True; AC20 OPEN stated in 03/14=True; no un-negated PRODUCTION READY / SYSTEM READY / RELEASED / FULL SYSTEM CONSISTENCY PASSED in ODI01 documents (flagged=[]); no such phrase in any candidate deck=True |
| 17 | Part D claims | **PASS** | UNSUPPORTED CLAIM original=1 candidate=0; slide-15 and slide-23-notes wording present=True,True; MOCKUP_REGISTER.csv exists=True; no register invented; changed lines are exactly two |
| 18 | Checksum integrity | **PASS** | 152 files listed in SHA256SUMS.txt verify, 0 mismatches, unlisted files on disk (excluding the sums file itself)=[], problems=[]; SHA256SUMS.txt does not list itself |
| 19 | Manifest integrity | **PASS** | MANIFEST.json lists 151 files (all present, bytes and SHA-256 match, neither manifest file lists itself); candidate baseline commit 4ea0d117da03 recorded and an ancestor of HEAD; branch claude/gem-worktree-safety-30b559; 18 original file hashes recorded and equal to the baseline blobs; ODI01 external input hashes unchanged; problems=[] |
| 20 | Candidate/original separation | **PASS** | working-tree changes outside the R1 folder=0; authoritative originals (Register, Parts A–D, tokens, asset kit, letterhead, qa/, README, audit note) unchanged vs HEAD=True; every candidate deck, token and Part D prose file carries an ODI01-R1 marker in its file name=True; ODI01 (external input, not in repository history) is not overwritten: its input hashes are in 02_Preflight.md and MANIFEST.json; D3A candidates kept in d3a_carried_forward/ |

## Coverage by document
| Document / package | Automated | Manual | Inherited | Not tested |
|---|---|---|---|---|
| Register (xlsx) | recalculated counts, hash, 12/12 TBD | adoption evidence (ODI01) | — | named role holders |
| Part A RC2 (80 sl.) | 112-assertion set, bold recount, weight search, geometry | slides 15, 35 | contrast/WCAG claims | native a11y, native rendering |
| Part B RC2 (35 sl.) + tokens | assertions, 153-token verification, CSS, bold recount, geometry | slides 3, 10, 12, 22 | booking-flow record | runtime, Storybook/bundle |
| Part C RC2 (78 sl.) | assertions, bold recount, geometry | slide 15 | process claims | supplier values |
| Part D (24 sl.) | claim scan (orig + cand) | wording (ODI01) | — | image rights, production |
| Official kit (34 SVG + files) | unchanged vs HEAD | X12 scope | — | production-master acceptance |
| Letterhead R03 (8 variants) | unchanged vs HEAD | — | structure, PDFs, hierarchy (ODI01) | Windows/Online Word, AT, print |

## Known limits of these checks
- QA item 15 ignores explanations of the unallocated ID by rule and still fails on any active use (see `05`).
- Items 19 and 20 verify against `HEAD` 4ea0d11, not the ODI01 commits, which are not in this repository.
- Check 1 recalculates the Register in LibreOffice; check 13 uses `pdfinfo`.
