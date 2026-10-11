"""ODI01-R1 review closure — DOCUMENT-ONLY edits (no deck, PDF or token file is opened for writing).
Records the owner decision PART B INLINE EMPHASIS — TEMPORARY 400 TREATMENT ACCEPTED and the main-ref investigation finding.
Usage: r1_closure_docs.py <pkg_dir>   (every replacement asserts that its old text exists exactly as expected)"""
import sys,re
pkg=sys.argv[1]
DEC='PART B INLINE EMPHASIS — TEMPORARY 400 TREATMENT ACCEPTED'
SENT='Intended emphasis may be restored only when an accepted corresponding 500-weight font file is introduced through the governed font-validation process.'
SLIDES='Part B slides 3, 11, 13, 18, 19, 21, 24, 30 and 33'
def edit(name,pairs,regex=False):
    p=pkg+'/'+name;s=open(p,encoding='utf-8').read()
    for a,b in pairs:
        if regex:
            s2,n=re.subn(a,lambda m:b,s)
            assert n>=1,(name,a[:60]);s=s2
        else:
            assert a in s,(name,a[:70]);s=s.replace(a,b)
    open(p,'w',encoding='utf-8').write(s)
BOX=f'''**{DEC}.** Owner decision recorded after ODI01-R1 review. {SLIDES} read slightly weaker at 400 after the synthetic bold was removed, because bold run-in heads and emphasised passages now render at Inter 400. This is **accepted as-is** for the current 400-only implementation.
- **No visual workaround is authorized.** Not permitted as compensation: synthetic bold, underline, new colours, new font families, Jost substitution, tracking on running text, arbitrary size changes, new rules or shapes, new typographic tokens. The current Inter 400 treatment remains; the nine slides are not edited again.
- **Current implementation remains 400.**
- {SENT}
- This is a temporary implementation limitation, not a redesign request. It does **not** close the font gates (VAL-05, VAL-19 stay open as applicable), Y03, VAL-07, or native PowerPoint / accessibility QA.'''
# ---- 01
edit('01_Executive_Summary.md',[
 ("One hierarchy finding for owner review: bold run-in heads now read at 400 (`18_qa_evidence/affected_slide_visual_qa.md`).","One hierarchy finding, now **accepted by the owner** as a temporary 400 treatment (see \"Review closure\" below; `18_qa_evidence/affected_slide_visual_qa.md`)."),
 ("## Honest limits",f"## Review closure (after ODI01-R1)\n{BOX}\n\n**Local `main` ref movement** (2026-10-09 01:10:05 +0300, `334744c` → `4ea0d11`) was investigated read-only: **CAUSE NOT ATTRIBUTABLE FROM AVAILABLE GIT EVIDENCE**. It does not affect the ODI01-R1 lineage (based on `origin/main` = `4ea0d11`). The primary checkout's working tree was advanced to `4ea0d11` at that second; the earlier \"primary checkout untouched\" wording is corrected. See `18_qa_evidence/main_ref_movement_investigation.md`. A second local commit records this closure; `a5d9acc` is preserved; the candidate decks and PDFs are byte-identical to `a5d9acc`.\n\n## Honest limits"),
])
# ---- 02 preflight text lives in the generator; patch the generated file and the script
edit('02_Preflight.md',[("Primary checkout was **not modified**. It has its own untracked entries that pre-date this session (`.DS_Store` files, `GEM_Letterhead_Set_v1.0/`); they were not touched.","**Correction (review closure):** no command run for ODI01-R1 wrote to the primary checkout. However, the primary's local `main` was fast-forwarded from `334744c` to `4ea0d11` at 2026-10-09 01:10:05 +0300, and its working tree was updated to match at the same second, by a process this Git evidence cannot identify (`18_qa_evidence/main_ref_movement_investigation.md`). Its untracked entries (`.DS_Store` files, `GEM_Letterhead_Set_v1.0/`) pre-date the session and were not touched. The primary local `main` value recorded in the table above is the value at preflight generation time and is the post-movement value `4ea0d11`.")])
edit('17_scripts/r1_preflight.py',[("Primary checkout was **not modified**. It has its own untracked entries that pre-date this session (`.DS_Store` files, `GEM_Letterhead_Set_v1.0/`); they were not touched.","**Correction (review closure):** no command run for ODI01-R1 wrote to the primary checkout. However, the primary's local `main` was fast-forwarded from `334744c` to `4ea0d11` at 2026-10-09 01:10:05 +0300, and its working tree was updated to match at the same second, by a process this Git evidence cannot identify (`18_qa_evidence/main_ref_movement_investigation.md`). Its untracked entries (`.DS_Store` files, `GEM_Letterhead_Set_v1.0/`) pre-date the session and were not touched. The primary local `main` value recorded in the table above is the value at preflight generation time and is the post-movement value `4ea0d11`.")])
# ---- 03
edit('03_Owner_Decisions_Carried_Forward.md',[("## R1 effect on each decision",f"## Owner decision recorded at review closure (ODI01-R1)\n{BOX}\n\n## R1 effect on each decision"),
 ("| **D5** | **Completed in R1** (`07`): 400 only; no faux bold; 500 = FUTURE DESIGN INTENT, PENDING ACCEPTED FONT FILE. |","| **D5** | **Completed in R1** (`07`): 400 only; no faux bold; 500 = FUTURE DESIGN INTENT, PENDING ACCEPTED FONT FILE. Closure: Part B inline-emphasis degradation on nine slides accepted as a temporary 400 treatment; no workaround authorized. |")])
# ---- 04
edit('04_Implementation_Trace.md',[("native PowerPoint check; owner decision on weakened run-in-head emphasis.","native PowerPoint check. (The run-in-head emphasis question was decided at review closure: see R1-3.)")])
t=open(pkg+'/04_Implementation_Trace.md',encoding='utf-8').read()
t+=f'''
### R1-3 · Review closure: Part B inline emphasis, temporary 400 treatment
- **Owner instruction:** {DEC}. {SLIDES} stay as rendered at Inter 400; do not compensate; keep VAL-05 and VAL-19 open as applicable; record that {SENT[0].lower()+SENT[1:]}
- **Source evidence:** ODI01-R1 visual QA (`18_qa_evidence/affected_slide_visual_qa.md`), which flagged 21 runs on these nine slides.
- **Affected files:** documentation only: `01`, `03`, `04`, `07`, `14`, `15`, `12` (wording), `18_qa_evidence/affected_slide_visual_qa.md`, `07_Font_Bold_Flag_Before_After.csv` (note text), `18_qa_evidence/main_ref_movement_investigation.md` (new), manifest and checksums.
- **Implementation:** none on the decks. No slide, PDF or token file was changed; no workaround was introduced.
- **After state:** limitation recorded as accepted and temporary. Restoration requires an accepted 500-weight font file through the governed font-validation process.
- **Open dependencies:** VAL-05, VAL-19, Y03, VAL-07; native PowerPoint rendering and accessibility QA; this decision leaves all of these gates open.
'''
open(pkg+'/04_Implementation_Trace.md','w',encoding='utf-8').write(t)
# ---- 07
edit('07_Font_400_Restriction_Implementation.md',[
 ("1. **Hierarchy finding (owner decision):** where bold marked run-in heads (e.g. \"Character.\", \"Use:\", \"Added:\") or an emphasised paragraph (Part B slide 3 tagline note), the emphasis is now weaker. Not corrected, because bold may not be reintroduced and any other cue (capitalisation, size, rule) is a design change. 9 slides: Part B 3, 11, 13, 18, 19, 21, 24, 30, 33.",
  f"1. **Hierarchy finding: DECIDED — temporary 400 treatment accepted** (see section 8). Where bold marked run-in heads (e.g. \"Character.\", \"Use:\", \"Added:\") or an emphasised paragraph (Part B slide 3 tagline note), the emphasis is weaker. 9 slides: Part B 3, 11, 13, 18, 19, 21, 24, 30, 33."),
])
t=open(pkg+'/07_Font_400_Restriction_Implementation.md',encoding='utf-8').read()
t+=f'''
## 8. Owner decision at review closure
{BOX}

Scope of the acceptance: the nine slides above only, as rendered in the R1 candidate (explicit `b="0"`, Inter 400). The 21 inventoried runs on those slides (`07_Font_Bold_Flag_Inventory.csv`, class REQUIRES VISUAL REVIEW) stay as they are. Part A, Part C and the other Part B slides are not affected by the decision. Restoring intended emphasis later means introducing an accepted 500-weight file for the family concerned through the font-validation process (licence and deployment acceptance, hashes, VAL-05 / VAL-19 evidence), and only then changing the slides in a separate, controlled pass.
'''
open(pkg+'/07_Font_400_Restriction_Implementation.md','w',encoding='utf-8').write(t)
# ---- 14
edit('14_Remaining_Gates.md',[("Native PowerPoint check of the R1 decks; owner decision on weakened run-in-head emphasis (9 slides) | 228 → 0 brand-font bold flags in the candidate decks; not natively tested |","Native PowerPoint check of the R1 decks. Part B inline-emphasis degradation on 9 slides: **owner-accepted as a temporary 400 treatment** (no workaround; restoration needs an accepted 500 file) | 228 → 0 brand-font bold flags in the candidate decks; not natively tested; font gates not closed by the acceptance |")])
t=open(pkg+'/14_Remaining_Gates.md',encoding='utf-8').read()
t+=f'''
## Review-closure decision (ODI01-R1)
{BOX}
'''
open(pkg+'/14_Remaining_Gates.md','w',encoding='utf-8').write(t)
# ---- 15
t=open(pkg+'/15_Change_Log.md',encoding='utf-8').read()
t+=f'''
## Review-closure commit (documentation only; follows `a5d9acc`)
Both commits are preserved (`a5d9acc` is not squashed or amended). Decks, PDFs, tokens and scripts other than this documentation script are byte-identical to `a5d9acc`.

| # | File | Change | Decision |
|---|---|---|---|
| 11 | `01`, `03`, `04`, `07`, `14`, `15` | Record **{DEC}**: no workaround authorized; current implementation 400; restoration only via an accepted 500-weight file and the governed font-validation process; font and native QA gates not closed. | owner decision (review closure) |
| 12 | `12`, `16`, `18_qa_evidence/affected_slide_visual_qa.md`, `07_Font_Bold_Flag_Before_After.csv` | Wording only: the nine-slide hierarchy finding is now "accepted" instead of "flagged for owner review". No metric or result changed. | same |
| 13 | `02_Preflight.md`, `17_scripts/r1_preflight.py` | Corrected "primary checkout not modified" (see 14). | investigation |
| 14 | `18_qa_evidence/main_ref_movement_investigation.md`, `18_qa_evidence/git_evidence/` | New: read-only investigation of the local `main` movement 334744c → 4ea0d11 (01:10:05 +0300); cause not attributable from Git evidence; lineage not affected. | investigation |
| 15 | `17_scripts/r1_closure_docs.py` | New: the script that applied rows 11–13. | — |\n| 15a | `18_qa_evidence/push_readiness_assessment.md` | New: branch-only push-readiness assessment (nothing pushed). | investigation |
| 16 | `MANIFEST.json`, `SHA256SUMS.txt`, `12`, `18_qa_evidence/cross_document_qa_results.*` | Regenerated; verified. | — |
'''
open(pkg+'/15_Change_Log.md','w',encoding='utf-8').write(t)
# ---- 12 (generated text lives in r1_render_reports.py; patch both)
for f in ('12_Consistency_Coverage_Report.md','17_scripts/r1_render_reports.py'):
    edit(f,[("the hierarchy finding on bold run-in heads","the hierarchy finding on bold run-in heads (owner-accepted at review closure as a temporary 400 treatment)")])
# ---- 16
edit('16_PR_Proposal.md',[("the 9 slides with weakened run-in-head emphasis","the 9 Part B slides with weaker run-in-head emphasis (owner-accepted as a temporary 400 treatment; no workaround)")])
# ---- visual QA md
edit('18_qa_evidence/affected_slide_visual_qa.md',[("No. Run-in heads / emphasis now rely on punctuation and position; Brand Owner / native review to decide whether a 400-compatible cue (size, spacing, rule) is wanted. Bold NOT reintroduced.","No — **owner decision: temporary 400 treatment accepted**; no workaround authorized. Run-in heads / emphasis rely on punctuation and position. Bold NOT reintroduced."),
 ("Flagged for Brand Owner review.","**Owner decision (review closure): accepted as a temporary 400 treatment; no compensating change authorized.** "+SENT)])
# ---- before/after csv note
edit('07_Font_Bold_Flag_Before_After.csv',[("no adjustment applied (owner/native review)","no adjustment applied (owner decision: temporary 400 treatment accepted)")])
print('closure docs applied')
