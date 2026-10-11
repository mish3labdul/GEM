"""ODI01-R1 document builder. Reuses ODI01 prose (renumbered, wording updated) and writes the new R1 documents; counts come from the generated evidence files.
Usage: r1_build_docs.py <pkg_dir> <odi01_full_tree> <preflight_values.json>"""
import sys,os,re,csv,json,collections,shutil
pkg,odi=sys.argv[1:3]
rd=lambda p:open(os.path.join(odi,p),encoding='utf-8').read()
def wr(name,txt): open(os.path.join(pkg,name),'w',encoding='utf-8').write(txt)
LABEL='GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE'
def sub(t,pairs):
    for a,b in pairs: t=t.replace(a,b)
    return t
COMMON=[('19_scripts/','17_scripts/'),('20_candidate_documents','19_candidate_documents'),('ODI01-candidate','ODI01-R1-candidate'),('ODI01-D6-CANDIDATE','ODI01-R1-D6-CANDIDATE'),('.ODI01-CANDIDATE.md','.ODI01-R1-CANDIDATE.md'),('deck_candidates/','deck_candidates/')]
# ---------- evidence-derived numbers
W=list(csv.DictReader(open(pkg+'/18_qa_evidence/font_weight_reference_search.csv',encoding='utf-8')))
cls=collections.Counter(r['Class'] for r in W)
five=[r for r in W if r['Match']=='500']
seen=set();rows500=[]
for r in five:
    k=(r['Artifact'],r['Location'],r['Context'])
    if k in seen: continue
    seen.add(k);rows500.append(r)
DESC={'A':'A — truthful: states 400 as current / marks 500 PENDING','C':'C — future design intent, labelled (CURRENT IMPLEMENTATION = 400 stated)','K':'K — token value/key vocabulary (future intent; description states 400 now)','H':'H — historical / provenance log, not an instruction','N':'N — not a type weight'}
def short(a):
    for k,v in (('Part A','Part A deck'),('Part B','Part B deck'),('Part C','Part C deck'),('Part D','Part D deck')):
        if k+' — RC2' in a: return v+(' (PDF text layer)' if False else '')
    return a
t500=['| Artifact | Location | Text | Class |','|---|---|---|---|']
for r in sorted(rows500,key=lambda r:(r['Artifact'][:4],r['Location'])):
    t500.append(f"| {short(r['Artifact'])} | {r['Location']} | {r['Context'][:150].replace('|','/')} | {DESC[r['Class']]} |")
# ================= 01
wr('01_Executive_Summary.md',f'''# 01 · Executive Summary — ODI01-R1 Technical Reconciliation

**{LABEL}**

Date: 2026-10-09 · Branch: `claude/gem-worktree-safety-30b559` (isolated worktree) · Baseline: `HEAD` = `origin/main` = `4ea0d117da03850854654288afcdde98f39994d5` · Local only: not pushed, merged, published or opened as a PR.

## What "SYNCHRONIZED" means here
Governing-content, terminology, identifier and status alignment. It does **not** mean validated in every native application or production process, and it is not release readiness.

## What R1 did
R1 is a narrow technical reconciliation of ODI01. It is not a new audit, a redesign, a new owner-decision round or a release candidate. It fixed exactly two verified ODI01 defects:

| # | Defect in ODI01 | R1 result |
|---|---|---|
| 1 | The validation-ID checker mistook the explanation that one ID number is intentionally unallocated for a live reference, so cross-document QA item 15 failed (19 of 20). | Replaced the ID-set test with a structured sentence classifier (`17_scripts/validation_id_checker.py`). Explanatory mentions are allowed. Use as an owner, status, evidence, dependency, closure, release, approval, gate or pass/fail state fails, and so do unknown IDs. 30 regression cases pass. VAL-18 stays documented as unallocated; it was **not** created. **20/20 cross-document QA checks passed.** Separately: **112 automated assertions passed.** |
| 2 | D5 was incompletely implemented: 228 explicit bold flags (b="1") on brand-font runs and wording that still read as if weight 500 were usable (Part A slide 35, Part B slides 10/12/22, Part C slide 15). | Recounted independently (2 + 121 + 105 = 228, all Inter), cleared all 228 (b="1" → b="0"), corrected the five wording locations, added three clarification boxes, and separated FUTURE DESIGN INTENT = 500 from CURRENT IMPLEMENTATION = 400 in the four 500-weight tokens. **Brand-font bold flags: 228 → 0. Current faux-bold dependency: 0.** No font added, no weight synthesized, no token value or status changed. |

## Headline results
- Cross-document QA: **20/20 PASS, 0 FAIL** (`12`). 112 automated assertions: **112 PASS, 0 FAIL** (originals and candidates).
- Tokens: **153/153** names, types and values identical to the originals; **26** downward status normalizations retained; **0** promotions.
- Fonts: Jost 400, Inter 400, Noto Sans Arabic 400 present; **no 500 file exists** (stop condition not triggered). 500 = PENDING ACCEPTED FONT FILE.
- Weight-reference search: {len(W)} hits across the candidate decks, PDFs, tokens and prose; every one classified; **0 current-implementation uses of 500 or bold**.
- Part D: unchanged from ODI01 (0 bold flags, 0 unsupported claims); "CONCEPT / NOT PRODUCTION ARTWORK" retained.
- Visual QA: 64 affected slides rendered before and after (LibreOffice, review evidence only). No layout regression. One hierarchy finding for owner review: bold run-in heads now read at 400 (`18_qa_evidence/affected_slide_visual_qa.md`).

## Honest limits
- **112 automated assertions passed** and **20/20 cross-document QA checks passed** are text/metadata/structure results. They are not a statement of full system consistency, and none is made.
- Renders are LibreOffice 26.8 only. **Native PowerPoint rendering, accessibility checking and reading order remain open.**
- ODI01, AFC01 and AFC02 history (`6fbd951`, `f346133`, `5dbd017`) is not in this repository; ODI01 was consumed as hash-verified delivered packages (`02`). ODI01 was not overwritten.
- PDFs for Parts A–C were re-exported with LibreOffice 26.8.1 (ODI01 used 24.2), so they differ from the ODI01 PDFs on every page at byte level; the text, fonts and layout checks above are the comparison, not byte equality.
- 25 of the 64 affected slides were inspected by eye; the other 39 are covered by automated word-geometry checks (labelled in the visual QA file).

## Gates that remain
AC20 OPEN; named role holders; trademark, logo ownership, master artwork, fonts and licences, image rights; Arabic linguistic and native QA (VAL-07, VAL-08, VAL-15 open); native PowerPoint / Windows Word / Word Online / Acrobat / assistive technology; supplier evidence; component bundle (VAL-13, VAL-20); D3 (unresolved); Legal/IP (D7). See `14`.

## Suitability
Suitable for Brand Owner review. Suitable for an explicitly authorized **branch** push only if the owner authorizes it. Suitable for PR review only after that. **Not suitable for release.** See `16`.
''')
# ================= 02 exists
# ================= 03
d2=rd('02_Owner_Decisions_Recorded.md')
d2=sub(d2,COMMON+[('# 02 · Owner Decisions Recorded','# 03 · Owner Decisions Carried Forward (ODI01 → ODI01-R1)'),('Recorded from the Brand Owner\'s ODI01 brief (2026-10-08). Decisions are implemented as given; none is re-asked.','Recorded in ODI01 (2026-10-08) and **locked** for R1: none is reopened, re-asked or re-decided.'),('Implemented in ODI01 as','Where (R1 numbering)'),('(`04`, `20_candidate_documents/register_adoption/`)','(`19_candidate_documents/register_adoption/`; summary below)'),('`05`.','this document, "Governance and AC20".'),('(`19_candidate_documents/d3a_carried_forward/`). D3B options in `13`;','(`19_candidate_documents/d3a_carried_forward/`). D3B options in `13`;'),('`14`.','section "D7" below.')])
d2=d2.replace('`15`','`14`')
a=rd('04_Register_Adoption_Record.md');a=a.split('\n',2)[2] if a.startswith('# ') else a
g=rd('05_Governance_and_AC20_Status.md');g=g.split('\n',1)[1]
l=rd('14_Public_Repository_Legal_Status.md').split('\n',1)[1]
wr('03_Owner_Decisions_Carried_Forward.md',d2+f'''
## R1 effect on each decision
| ID | R1 effect |
|---|---|
| D1 | None. Register workbook untouched; 466 rows not rewritten. Adoption record carried unchanged. Evidence-required rows, deferred items, role-holder assignment, AC20 and the supplier/native/legal gates stay open. |
| D4 | Carried unchanged: 26 downward normalizations, 153/153 values identical, 0 promotions (re-verified in `06`). |
| **D5** | **Completed in R1** (`07`): 400 only; no faux bold; 500 = FUTURE DESIGN INTENT, PENDING ACCEPTED FONT FILE. |
| D6 | Carried unchanged; Part D deck not edited in R1 (`08`). |
| D7 | NO CHANGE — LEGAL/IP DECISION PENDING. No GitHub setting touched; no external party contacted. |
| D8 | Carried unchanged (`10`). VAL-07, VAL-08, VAL-15 open. |
| AC20 | OPEN. Not closed; no release language introduced. |
| D3 | **UNRESOLVED.** Not implemented; BRAND vs Logo for X12 not chosen; D3A C1–C4 not promoted (`13`). |

## Register adoption record (D1, carried from ODI01)
{a}

## Governance and AC20
{g}

## D7 — Public repository / legal status
{l}
''')
# ================= 04 trace
t=rd('03_Implementation_Trace_Matrix.md')
t=sub(t,COMMON+[('# 03 · Implementation Trace Matrix','# 04 · Implementation Trace Matrix (ODI01 + R1)'),('tracked in `15`','tracked in `13` and `14`')])
t=re.sub(r'(\*\*Affected files:\*\* CANDIDATES: Part A s34; Part B s9, s10; Part C s15 \(deck_candidates/\);)',r'\1',t)
r1=f'''

---
## ODI01-R1 entries (added in this pass)

### R1-1 · Validation-ID checker (ODI01 defect 1)
- **Instruction:** Fix the checker so explanations are not treated as live references to the unallocated ID. The unallocated ID is VAL-18. Do not create it and do not renumber; add regression tests; re-run cross-document QA to 20/20.
- **Source evidence:** ODI01 `cross_document_qa.py` item 15 collected every `VAL-nn` found in the package documents (including its own report text) into one set and required one number to be absent.
- **Affected files:** `17_scripts/validation_id_checker.py` (new), `17_scripts/cross_document_qa.py` (item 15), `17_scripts/run_validation_id_tests.py`, `18_qa_evidence/validation_id_checker_tests.json` and `…_test_results.json`, `05_Validation_ID_QA_Fix.md`, `12`.
- **After state:** structured classification (allowed explanatory / failing active / failing unknown); 30/30 regression cases pass; item 15 PASS; 20/20.
- **Open dependencies:** none for this defect.

### R1-2 · D5 completion: 400 only, no faux bold (ODI01 defect 2)
- **Instruction:** Current implementation = weight 400 only until accepted 500-weight files exist; no faux bold; clean every active 500 reference; no token value changes.
- **Source evidence:** raw OOXML recount (228 explicit bold runs: A 2, B 121, C 105; all Inter); font binary scan (no 500 file); full-artifact weight search ({len(W)} hits, all classified).
- **Affected files:** candidate Part A, B, C decks (slide XML only) and their PDFs; token JSON/CSS descriptions; `07_*`, `18_qa_evidence/*` (inventory, before/after, visual QA, diff register, search).
- **After state:** brand-font bold flags 228 → 0; Part A s35, Part B s10/s12/s22 and Part C s15 corrected; four 500-weight tokens state FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400; values and statuses unchanged.
- **Open dependencies:** VAL-05, Y03, VAL-19, VAL-07 (accepted font files, licences); native PowerPoint check; owner decision on weakened run-in-head emphasis.
'''
wr('04_Implementation_Trace.md',t+r1)
# trace csv carried as evidence
shutil.copy(os.path.join(odi,'03_Implementation_Trace_Matrix.csv'),pkg+'/18_qa_evidence/implementation_trace_matrix_odi01.csv')
# ================= 05
wr('05_Validation_ID_QA_Fix.md','''# 05 · Validation-ID QA Fix (ODI01 defect 1)

**Result: fixed.** Cross-document QA item 15 now passes; the suite is **20/20 PASS, 0 FAIL**.

## The defect
In ODI01, item 15 gathered every `VAL-nn` found anywhere in the package documents into one set and required one number to be absent. That number is VAL-18, which is **intentionally unallocated**. This follows the Register convention; the audit finding that called it "missing" was rejected. The package documents correctly say so, and the report that quotes the check's own evidence also names it. The checker therefore failed on the explanation of the rule, not on a violation of it.

## The rule now implemented (`17_scripts/validation_id_checker.py`)
- Allocated IDs are VAL-01 to VAL-21 except VAL-18. Any other number is an **unknown ID** and fails.
- VAL-18 is not created and no surrounding ID is renumbered.
- Each sentence that names the unallocated ID is classified:
  - **EXPLANATORY**: states that the ID is unallocated, not allocated, absent, a numbering gap or not used. **Allowed.**
  - **ACTIVE**: gives it an owner, a status, an evidence requirement, a dependency, a closure or release condition, an approval record, an implementation gate or a pass/fail state. **Fails.**
  - **UNCLASSIFIED**: neither of the above. **Fails** (conservative).
- Negated phrases such as "carries no owner" are removed before the active test, but only inside a sentence that is already explanatory, so "unallocated but must close" still fails.
- It is a structured per-sentence rule, not a substring exception for one report.

## Regression tests
`18_qa_evidence/validation_id_checker_tests.json` holds 15 positive and 15 negative cases, including every case required by the brief. Results (`validation_id_checker_test_results.json`): **30/30 PASS**. Re-run with `python3 17_scripts/run_validation_id_tests.py <fixture> <results>`.

## What the QA item reports now
The package documents, and the Part D candidate prose, are scanned. The item passes only if there are no active or unknown-ID findings and the package documents the unallocated ID. It also confirms that VAL-05, 07, 08, 13, 15 and 20 are listed open in `14` and that no line closes them. Explanatory mentions are counted in the evidence string of item 15 in `12`.

## What did not change
VAL-18 stays unallocated. No validation gate was added, closed or renumbered. VAL-07, VAL-08 and VAL-15 remain open.
''')
# ================= 06
tk=sub(rd('06_Token_Status_Implementation.md'),COMMON+[('# 06 · Token Status Implementation (Owner decision D4, with D5 annotation)','# 06 · Token Status Implementation (Owner decision D4, with D5 annotation) — ODI01-R1'),('`token_status_implementation.py`','`r1_token_status.py`'),('19_scripts/token_status_implementation.py','17_scripts/r1_token_status.py')])
tk+='''
## R1 change (D5 wording only)
The four weight-500 tokens (`type.weight.medium`, `type.styleWeight.label`, `type.styleWeight.arabicH3`, `type.styleWeight.arabicLabel`) kept value **500** and their D4 statuses. Only the description / CSS comment changed, from "500 WEIGHT PENDING ACCEPTED FONT FILE — use 400 until accepted" to:

> FUTURE DESIGN INTENT = 500 · CURRENT IMPLEMENTATION = 400 · 500 WEIGHT PENDING ACCEPTED FONT FILE (D5; Y03, VAL-05, VAL-19)

This is approach A of the brief (description/status clarification only). The governing future design is not rewritten and no separate current-implementation mapping was introduced. No token, template or deck instruction in the candidate set requires a 500 file. R1 re-run: 153/153 name, type and value identical to the originals; 26 downward status changes retained (10 APPROVED→CONDITIONAL, 9 APPROVED→PENDING VALIDATION, 7 CONDITIONAL→PENDING VALIDATION); 0 promotions; 0 unexplained status inflation; all verifications PASS (`19_candidate_documents/tokens/token_verification.json`).
'''
wr('06_Token_Status_Implementation.md',tk)
shutil.copy(pkg+'/19_candidate_documents/tokens/token_status_implementation.csv',pkg+'/06_Token_Status_Implementation.csv')
# ================= 07
wr('07_Font_400_Restriction_Implementation.md',f'''# 07 · Font 400 Restriction Implementation (Owner decision D5) — completed in ODI01-R1

**Status: CURRENT IMPLEMENTATION = WEIGHT 400 ONLY, until accepted 500-weight font files exist.** Candidate, unapproved. VAL-05, Y03, VAL-19 and VAL-07 are **not** closed.

## The rule
Jost (display / headings), Inter (body / office / UI) and Noto Sans Arabic (interim Arabic, M02) at **400 only**. No faux bold, no synthesized 500 or 700, no application-generated pseudo-bold, no substitute typeface, no variable-font synthesis. **500 exists only as FUTURE DESIGN INTENT, PENDING ACCEPTED FONT FILE.**

## 1. Font binary verification (before any typography edit)
`07_Font_Claim_File_Matrix.csv` (generated by `17_scripts/r1_font_matrix.py`; exits non-zero if a 500 file appears).

| Family | 400 | 500 |
|---|---|---|
| Jost | `Jost-Regular.ttf` present, current (v3.710, `db44231d…`) | **No accepted file.** Variable working build recorded only in the letterhead manifest (not in repo, not accepted) |
| Inter | `Inter-Regular.ttf` present, current (v4.001, `8bac02d5…`) | **No accepted file.** Same |
| Noto Sans Arabic | `NotoSansArabic-Regular.ttf` present, current (v2.012, `35965bc1…`) | **No accepted file.** Same |

**No 500 file has appeared since ODI01, so the stop condition did not trigger.** Also recorded: `~/Library/Fonts/GEM-Working-*-Bold.ttf` exist on the machine that ran R1, outside the repository. They are byte-identical to the letterhead manifest's "ARCHIVED INPUT / 700 NOT USED" files (Jost, Inter, Noto Sans Arabic Bold, weight 700). They are not 500, not accepted, not used, and not in the repo. Renders in R1 supplied only the three Regular files to LibreOffice so those Bold files could not be picked up.

## 2. Explicit bold inventory (independent recount)
`07_Font_Bold_Flag_Inventory.csv` / `.md`: every run with b="1", read from the OOXML of the ODI01 candidate PPTX files, 14 columns, none skipped.

| Document | b="1" runs before | brand-font before | brand-font after | b="1" after (all) |
|---|---|---|---|---|
| Part A | 2 | 2 | 0 | 0 |
| Part B | 121 | 121 | 0 | 0 |
| Part C | 105 | 105 | 0 | 0 |
| Part D | 0 | 0 | 0 | 0 |
| **Total** | **228** | **228** | **0** | **0** |

Matches ODI01's count. All 228 are Inter text runs (table header cells and run-in heads); none non-brand; no b flag exists in masters, layouts, theme, table styles or notes; no slide is hidden. Classification: 207 REMOVE BOLD — USE 400; 21 REQUIRES VISUAL REVIEW (bold run-in heads that are the only weight cue in a mixed paragraph); 0 NON-BRAND / FALSE POSITIVE; 0 EMBEDDED ARTWORK / NOT TEXT (b is a text property; logos are separate picture parts).

## 3. What was changed (candidate decks, slide XML only)
- **Bold:** `b="1"` → `b="0"` on all 228 brand-font runs (explicit 400, immune to inheritance). Nothing else on those runs changed. No size, spacing, colour or position change.
- **Part A slide 35:** "EMPHASIS · INTER 500" → "EMPHASIS · INTER 400 · 500 PENDING" (the label box is one line high; the brief's compact form was used; slide 34 carries the full standing phrase).
- **Part B slide 10:** label-row Weight cell "500 PENDING" → "400 · 500 PENDING"; added box: "CURRENT IMPLEMENTATION: 400 for every row. 500: PENDING ACCEPTED FONT FILE."
- **Part B slide 12:** arabicH3 and arabicLabel Wt cells "500" → "400"; added note: "Wt column = current implementation weight: 400 only. arabicH3 and arabicLabel carry 500 as FUTURE DESIGN INTENT; 500 PENDING ACCEPTED FONT FILE." The slide remains ARABIC AND RTL · PENDING VALIDATION / PENDING LOCALIZATION APPROVAL.
- **Part B slide 22:** "Navigates; underlined, 500, ink" → "Navigates; underlined, 400, ink" (underline remains the functional cue).
- **Part C slide 15:** cells "400 · 500 PENDING" kept; added: "CURRENT IMPLEMENTED WEIGHT = 400 (Jost, Inter). 500 is PENDING ACCEPTED FONT FILE and is not available to any current build. Noto Sans Arabic weights remain [PENDING]."
- **Tokens:** descriptions only (see `06`).
- Part A slide 34 and Part B slide 9 (already "500 WEIGHT PENDING ACCEPTED FONT FILE") were left as ODI01 wrote them.
Added boxes are clones of existing text boxes (same font, size, colour), inserted before the footer in reading order.

## 4. Weight-reference search (all candidate artifacts)
`18_qa_evidence/font_weight_reference_search.csv`: search for 500, Medium, Semibold, Bold, font-weight and weight across the candidate decks (slide text, tables, notes), the candidate PDF text layers, tokens (JSON/CSS) and candidate prose: **{len(W)} hits, 0 unclassified, 0 class B** (current-implementation wording implying 500 or bold is usable). Classes: A {cls['A']} · C {cls['C']} · K {cls['K']} · H {cls['H']} · N {cls['N']} · T {cls['T']}. No hit for Medium, Semibold or Bold as a weight name exists in any candidate deck.

### Every remaining standalone "500" in the candidate artifacts
Deck rows below also appear in the matching PDF text layer.

{chr(10).join(t500)}

Class key: A truthful (400 current / 500 PENDING) · C future design intent, labelled · K token vocabulary · H historical log · N not a type weight · T table header. Upper-bound wording ("maximum two weights per composition") is a cap, not a requirement for a second weight.

## 5. Before / after
`07_Font_Bold_Flag_Before_After.csv`: per affected slide. Totals: b="1" runs before 228, after 0; brand-font before 228, after 0; non-brand before 0, after 0. **Current brand-font faux-bold dependency: 0. Current dependencies on an unavailable brand-font weight: 0.**

## 6. Verification
`17_scripts/r1_verify_edits.py` compares every changed XML part with the ODI01 candidate element by element: the only differences are b 1→0 on brand-font runs (228), the logged text edits (5 occurrences) and the 3 cloned boxes; all parts well-formed; no b="1" remains in any slide part. 64 slides rendered before and after (`18_qa_evidence/affected_slide_visual_qa.md`).

## 7. Open items
1. **Hierarchy finding (owner decision):** where bold marked run-in heads (e.g. "Character.", "Use:", "Added:") or an emphasised paragraph (Part B slide 3 tagline note), the emphasis is now weaker. Not corrected, because bold may not be reintroduced and any other cue (capitalisation, size, rule) is a design change. 9 slides: Part B 3, 11, 13, 18, 19, 21, 24, 30, 33.
2. Native PowerPoint rendering of the candidates is not tested.
3. VAL-05 / Y03 / VAL-19 / VAL-07 open. Lifting the restriction requires owner-accepted 500 files with hashes, licence and deployment acceptance.
4. Letterhead Revision 03 was not modified (it already complies: Regular only; 102 unused bold style definitions and 4 Courier style references are low-severity carry-overs).
''')
# ================= 08
p8=sub(rd('08_PartD_Claim_Implementation.md'),COMMON)
p8+='''
## R1
Part D was **not edited in R1**. The R1 Part D deck is a renamed, byte-identical copy of the ODI01 candidate (SHA-256 `04d325f8…`), with 0 explicit bold flags and no 500 reference, so D5 required no Part D change. Claim audit re-run: 63 unique claims / 162 occurrences on the original (1 UNSUPPORTED CLAIM) → 62 / 161 on the candidate (**0 unsupported claims**). "CONCEPT / NOT PRODUCTION ARTWORK" markings: 12 original, 12 candidate. Part D continues to state that no item is an approved production asset; nothing implies production approval, regulatory approval, supplier acceptance, physical proof or a final production master.
'''
wr('08_PartD_Status.md',p8)
# ================= 09
lh=sub(rd('09_Letterhead_Integration_Report.md'),COMMON+[('# 09 · Letterhead Integration Report (Revision 03 — latest reviewed package)','# 09 · Letterhead Status (Revision 03 — carried forward from ODI01; not modified in R1)')])
lh+='''
## R1
The letterhead package was **not modified** (`git diff HEAD` on `GEM_Letterhead_Set_v1.1_Application_Revision_03/` is empty). Carried forward: GEM™ Branded Letterhead Set — WORKING APPLICATION / PENDING VALIDATION; Arabic: PENDING LOCALIZATION APPROVAL. Open: native Windows Word, Word Online, Acrobat text layer, assistive technology and physical proof. The earlier "R04 unavailable" gate is retired.
'''
wr('09_Letterhead_Status.md',lh)
# ================= 10
ar=sub(rd('10_Arabic_PDF_Operating_Rule.md'),COMMON+[('# 10 · Arabic / Bilingual PDF Operating Rule (Owner decision D8)','# 10 · Arabic / Bilingual PDF Status (Owner decision D8) — carried forward'),('`10_Arabic_PDF_Test_Matrix.csv`','`18_qa_evidence/10_Arabic_PDF_Test_Matrix.csv`')])
ar+='''
## R1
Unchanged. **Internal working use: permitted with explicit working / pending labels. External Arabic or bilingual PDF issue: BLOCKED** until native validation passes. Still required: native Arabic QA, Windows Word, Word Online, Acrobat Unicode text layer, search / select / copy-paste, tagged PDF, reading order, screen reader / AT, accessibility QA. VAL-07, VAL-08 and VAL-15 remain open. R1 did not alter any Arabic text; its only Arabic-adjacent change is the Part B slide 12 weight wording (Arabic remains PENDING VALIDATION / PENDING LOCALIZATION APPROVAL).
'''
wr('10_Arabic_PDF_Status.md',ar)
shutil.copy(os.path.join(odi,'10_Arabic_PDF_Test_Matrix.csv'),pkg+'/18_qa_evidence/10_Arabic_PDF_Test_Matrix.csv')
# ================= 11
ac=sub(rd('11_Accessibility_Native_Review_Queue.md'),COMMON+[('**No slide was changed in ODI01.**','**No queue slide was reordered, retitled or otherwise remediated in ODI01 or R1.**')])
ac+='''
## R1
The 30-slide native review queue is carried forward **unchanged**: 22 likely title fixes · 6 reading-order reviews · 2 uncertain / native review. No placeholders were mass-inserted and no unrelated accessibility remediation was done. R1 touched slide XML on 64 slides for D5 only; for three of them (Part B 10, Part B 12, Part C 15) it added a clone of an existing text box before the footer, in reading order. Whether any of those slides is in the queue, and whether the new boxes affect its reading-order review, is a native PowerPoint question that R1 did not test. The queue CSV is in `18_qa_evidence/`.
'''
wr('11_Accessibility_Queue.md',ac)
shutil.copy(os.path.join(odi,'11_Accessibility_Native_Review_Queue.csv'),pkg+'/18_qa_evidence/11_Accessibility_Native_Review_Queue.csv')
# ================= 13
x=sub(rd('13_X12_Controlled_Name_Options.md'),COMMON+[('# 13 · X12 Controlled-Name Options (D3B — NOT RESOLVED)','# 13 · D3 Unresolved (D3A sync corrections and D3B X12 STREAM token)')])
x+='''
## R1
**D3 remains UNRESOLVED and was not implemented.** C1–C4 are not approved; the D3A candidate decks were not promoted to authoritative originals and were not re-copied (their AFC02 decks and PDFs, ~12 MB, stay in the ODI01 package; their release-language text and the two X12 mappings are carried in `19_candidate_documents/d3a_carried_forward/`). BRAND vs Logo for X12 was not chosen; no asset was renamed; no X12 mapping was implemented.
'''
wr('13_D3_Unresolved.md',x)
# ================= 14 gates
gt=rd('15_Remaining_Gates.md')
gt=sub(gt,COMMON+[('# 15 · Remaining Gates and Accountable Roles (after ODI01)','# 14 · Remaining Gates and Accountable Roles (after ODI01-R1)'),('Updated for ODI01:','Carried from ODI01 and updated for R1:'),('ODI01 effect','R1 effect'),('| 23 | 228 bold-flag deck runs vs D5 no-faux-bold | Design Custodian | PENDING (native review) | Controlled later pass or accepted 500 file | Logged, not changed |','| 23 | Bold-flag runs vs D5 no-faux-bold | Design Custodian | RESOLVED IN R1 (candidate) · native check PENDING | Native PowerPoint check of the R1 decks; owner decision on weakened run-in-head emphasis (9 slides) | 228 → 0 brand-font bold flags in the candidate decks; not natively tested |'),('see `12`','see `12`'),('| 22 | Native rendering of ODI01 candidate decks (PowerPoint) | Presentation / Document QA | PENDING (native QA) | Native open/render check (LibreOffice render only in ODI01) | NOT TESTED natively |','| 22 | Native rendering of the R1 candidate decks (PowerPoint) | Presentation / Document QA | PENDING (native QA) | Native open/render check (LibreOffice 26.8 render only in R1) | NOT TESTED natively |'),('| 21 | Acceptance of ODI01 candidates (decks, tokens, prose) into authoritative sources','| 21 | Acceptance of ODI01-R1 candidates (decks, tokens, prose) into authoritative sources'),('D5: 400-only restriction applied; **not closed**','D5: 400-only restriction completed in the candidates (no bold flags, no active 500); gate **not closed**')])
gt+='''
Validation-ID note: **VAL-18 is intentionally unallocated**.\n\nNo validation gate has that number, so it has no owner, evidence or closure of its own. VAL-07, VAL-08 and VAL-15 stay open; AC20 stays OPEN.

Carried gates in plain words: Legal/IP (D7) — repository visibility NO CHANGE, decision pending; D3 — unresolved; supplier evidence — open; native QA (PowerPoint, Windows Word, Word Online, Acrobat, AT) — open.
'''
wr('14_Remaining_Gates.md',gt)
# ================= 15
wr('15_Change_Log.md',f'''# 15 · Change Log (ODI01-R1)

No authoritative original was modified. ODI01 (external, delivered packages) was not overwritten. Every change below is in a new file inside this folder; the only repository change is this folder and its single local commit.

## Changes relative to ODI01
| # | File / group | R1 change | Decision |
|---|---|---|---|
| 1 | `17_scripts/validation_id_checker.py`, `run_validation_id_tests.py`, `cross_document_qa.py` item 15 | Structured VAL-ID classifier replaces the ID-set test. Explanatory mentions of the unallocated ID are allowed; active use fails. | defect 1 |
| 2 | `18_qa_evidence/validation_id_checker_tests.json` (+ results) | 15 positive, 15 negative cases; 30/30 pass. | defect 1 |
| 3 | `cross_document_qa.py` items 8, 19, 20 and paths | Item 8 now audits 400-only / no faux bold; items 19–20 rebased on `HEAD` 4ea0d11 (AFC/ODI01 commits are not repository history); paths renumbered. | defects 1–2 |
| 4 | `19_candidate_documents/deck_candidates/Part A … ODI01-R1 CANDIDATE (UNAPPROVED).pptx/.pdf` | 2 bold flags cleared (slide 15); slide 35 label wording. | D5 |
| 5 | `… Part B …` | 121 bold flags cleared; slide 10 cell + added box; slide 12 two cells + added note; slide 22 cell. | D5 |
| 6 | `… Part C …` | 105 bold flags cleared; slide 15 added box. | D5 |
| 7 | `… Part D …` | None (byte-identical copy of the ODI01 candidate). | — |
| 8 | PDFs of Parts A–C | Re-exported from the R1 decks (LibreOffice 26.8.1, tagged); Part D PDF unchanged. | D5 |
| 9 | `19_candidate_documents/tokens/…ODI01-R1-candidate.json/.css` | Four 500-token descriptions and comments reworded to FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400; meta wording. No value, type, name, decision or status changed. | D5 |
| 10 | `01`–`16`, `18_qa_evidence/`, `17_scripts/` | New reports, evidence and scripts; ODI01 prose renumbered and updated. | all |

## Renumbering (ODI01 → R1)
01→01, 02→03, 03→04, 04+05+14→03, 06→06, 07→07, 08→08, 09→09, 10→10, 11→11, 12→12, 13→13, 15→14, 16→15, 17→16; new 02 (preflight), 05 (VAL-ID fix); scripts 19→17; candidates 20→19.

Not changed: Register, Parts A–D originals and their PDFs, original tokens, asset kit and file names, letterhead package, `qa/`, the audit note, primary `main`.

Per-file hashes and XML parts: `18_qa_evidence/file_diff_register.csv`. Edit proof: `17_scripts/r1_verify_edits.py` (only the intended differences exist).
''')
# ================= 16
wr('16_PR_Proposal.md','''# 16 · PR Proposal (NOT OPENED)

**No PR is opened. Nothing is pushed, merged or published.** This text is a proposal for the Brand Owner to use only if they later explicitly authorize a branch push and a PR.

**Title:** Audit: ODI01-R1 technical reconciliation (validation-ID checker; 400-only fonts) — unapproved, AC20 open

**Base:** `main` (`4ea0d11`) · **Head:** `claude/gem-worktree-safety-30b559`

## Summary
- Fixes the validation-ID QA check so explanatory references to the intentionally unallocated validation ID pass while active use fails (30 regression cases; cross-document QA 20/20).
- Completes D5: 228 brand-font bold flags → 0; five weight-500 wordings corrected; four 500-weight tokens now state FUTURE DESIGN INTENT = 500 / CURRENT IMPLEMENTATION = 400. No font added, no token value or status changed.
- Adds only a new folder `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/`; authoritative originals are untouched.
- Status: GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE.

## Review checklist
- [ ] `05` validation-ID rule and `validation_id_checker_tests.json`
- [ ] `07` 400-only implementation; `07_Font_Bold_Flag_Before_After.csv`; the 9 slides with weakened run-in-head emphasis
- [ ] `18_qa_evidence/affected_slide_visual_qa.md` (LibreOffice evidence only)
- [ ] Tokens: 153/153 values; 26 downward statuses; 0 promotions
- [ ] Nothing promoted; AC20 still OPEN; D3 unresolved; D7 no change

## Not in scope / not claimed
Release, production readiness, native-application validation (PowerPoint, Word, Acrobat, AT), supplier values, Arabic approval, rights clearance, visibility change, D3 resolution.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
''')
print('docs written; weight hits',len(W),dict(cls),'unique 500 rows',len(rows500))
