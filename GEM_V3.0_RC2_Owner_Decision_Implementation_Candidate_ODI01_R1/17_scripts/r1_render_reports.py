"""ODI01-R1: render 12_Consistency_Coverage_Report.md and the QA results files from the cross-document QA JSON.
Usage: r1_render_reports.py <pkg_dir> <qa_json>"""
import sys,json,re,os
pkg,qj=sys.argv[1:3];R=json.load(open(qj));Q=pkg+'/18_qa_evidence/'
base=open(Q+'consistency_baseline_originals.md',encoding='utf-8').read();cand=open(Q+'consistency_candidates_ODI01_R1.md',encoding='utf-8').read()
pb=re.search(r'(\d+) AUTOMATED ASSERTIONS PASSED · (\d+) FAILED',base);pc=re.search(r'(\d+) AUTOMATED ASSERTIONS PASSED · (\d+) FAILED',cand)
npass=sum(1 for r in R if r['result']=='PASS');nfail=sum(1 for r in R if r['result']!='PASS')
rows='\n'.join(f"| {r['n']} | {r['name']} | **{r['result']}** | {r['evidence'].replace('|','/')} |" for r in R)
open(Q+'cross_document_qa_results.md','w',encoding='utf-8').write(f'# Cross-Document QA — 20 separate results (ODI01-R1)\n\n**{npass}/20 cross-document QA checks passed** · {nfail} failed. There is **no single overall PASS** statement beyond these twenty lines; each stands on its own. This is not a statement of full system consistency. Script: `17_scripts/cross_document_qa.py`.\n\n| # | Check | Result | Evidence |\n|---|---|---|---|\n'+rows+'\n')
json.dump(R,open(Q+'cross_document_qa_results.json','w'),indent=1,ensure_ascii=False)
tv=json.load(open(pkg+'/18_qa_evidence/validation_id_checker_test_results.json'))
md=f'''# 12 · Consistency and Coverage Report (ODI01-R1)

## Headline
**{npass}/20 cross-document QA checks passed ({nfail} failed)** and, separately, **{pc.group(1)} automated assertions passed ({pc.group(2)} failed)** on the R1 candidate decks (A, B, C). The same assertion count ({pb.group(1)} passed, {pb.group(2)} failed) holds on the unchanged originals. Validation-ID regression tests: **{tv['passed']}/{tv['total']} passed**.

These are text, metadata and structure checks. They are **not** a statement of full system consistency, and no such statement is made anywhere in this package.

Reports: `18_qa_evidence/consistency_baseline_originals.md` (originals), `consistency_candidates_ODI01_R1.md` (candidates), `cross_document_qa_results.md/.json`. Scripts: `17_scripts/consistency_check_odi01.py` (ODI01 checker, assertions unchanged, candidate-path overrides) and `17_scripts/cross_document_qa.py`.

## What an assertion is
A term present or absent in slide text, tables and notes (palette hexes, family names, status terms, tagline, version string, document ID, authority-list anchor, twelve-role list, stale phrases absent), a PDF tagged flag, picture alt-text counts. No assertion tests meaning, rendering, runtime behaviour or native-application behaviour.

## Reporting categories (kept separate)
| Category | Meaning | Items in R1 |
|---|---|---|
| **AUTOMATED ASSERTIONS** | Re-run by script | {pc.group(1)} text/metadata assertions (originals and candidates) · 20-point cross-document QA · 23 validation-ID regression cases · token verification (all checks PASS, 153 tokens) · OOXML edit verifier (only intended differences) · bold-flag recount (228 → 0) · font binary scan · 135-hit weight search (0 unclassified, 0 class B) · word-geometry comparison of 64 slides · Part D claim scan · repository checksum lists |
| **MANUAL VERIFIED** | Read and judged by the author | Classification of the remaining 500 references and the five wording edits · visual inspection of 25 of the 64 affected slides (individual images and contact sheets) · the hierarchy finding on bold run-in heads · carried-forward ODI01 judgments (register adoption, Part D wording, X12 option comparison) |
| **INHERITED** | Quoted from ODI01 / earlier packages, not repeated | Word for Mac 16.113.3 results · PDFKit copy/search results · letterhead visual parity · earlier `qa/` statements · letterhead structure audit and bilingual hierarchy (ODI01 evidence files) |
| **NOT TESTED** | Not run | Native PowerPoint rendering/accessibility check of any deck · Windows Word · Word Online · iPad · Acrobat (accessibility, Unicode text layer) · screen readers / AT · component bundle runtime (does not exist) · rendered-page contrast · print/colour proofs |
| **NATIVE QA PENDING** | Needs a native application and a person | Title placeholders and reading order (30 slides) · Arabic copy/search in Acrobat and Windows Word · letterhead in Windows/Online Word · R1 candidate decks opened in PowerPoint |
| **SUPPLIER EVIDENCE PENDING** | Needs supplier or physical evidence | CMYK, Pantone, stock/GSM, Delta E, line weights, substrate, tolerances, dielines, physical proofs. None invented |

## Final cross-document QA — 20 separate results
| # | Check | Result | Evidence |
|---|---|---|---|
{rows}

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
'''
open(pkg+'/12_Consistency_Coverage_Report.md','w',encoding='utf-8').write(md)
print('rendered',npass,nfail)
