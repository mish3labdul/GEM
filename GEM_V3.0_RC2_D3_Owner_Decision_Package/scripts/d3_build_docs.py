"""Builds the D3 package documents from the apply log, mapping statistics and CSVs (numbers are read, not typed). Usage: d3_build_docs.py <pkg_dir> <repo_root>"""
import sys,os,json,csv,hashlib,glob
pkg,root=sys.argv[1:3]
L=json.load(open(pkg+'/11_QA_Evidence/d3a_apply_log.json'));ST=json.load(open(pkg+'/11_QA_Evidence/d3b_mapping_stats.json'))
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
def wr(n,t): open(os.path.join(pkg,n),'w',encoding='utf-8').write(t)
LABEL='GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE'
R1='GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1'
AO={'A':'c50dd3d0c45d6e2753e81b0f978879ed7e596ce52bdd24f7910ae6fcf16243d0','C':'f9f968d2e51d715658796c69e63c83dfe324bf783f6dc530b49bfc0c6fd3462b'}
dA,dC=L['decks']['A'],L['decks']['C']
H=lambda s:f'`{s[:12]}…`'
# ================= 02 authority verification
wr('02_D3A_Authority_Verification.md',f'''# 02 · D3A Authority Verification (C1–C4)

**Method.** Each correction was checked against the *actual current files*, not the AFC02 prose: the Approval Register workbook (`GEM_V3_RC2/00_originals/…Register_Prefilled.xlsx`), the authoritative Part A, Part B, Part C and Part D release files, the letterhead package, the open evidence registers, and the release-governance state (AC20 OPEN). Verification date 2026-10-09; baseline `4ea0d11`.

**Overall: C1, C2, C3 and C4 are each SUPPORTED. None introduces new policy; none needs an owner choice.** Under the owner's explicit instruction for this task, all four were implemented as candidate copies (`03`).

| | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| **Target** | Part A slides 79–80, speaker notes | Part C slide 44, body text | Part D `04_release/SHA256SUMS.txt` | "SYSTEM READY" in 3 release-notes files (4 occurrences) |
| **Verdict** | **SUPPORTED** | **SUPPORTED** | **SUPPORTED** | **SUPPORTED** |
| Visual content changes? | No | **Yes** (one body sentence; rendered and checked) | No (text list) | No (Markdown notes) |
| Notes-only? | **Yes** | No | n/a (not a deck) | n/a (not a deck) |
| New policy? | No | No | No | No |

## C1 — Part A slides 79–80 notes: Part B description
- **Current authoritative wording.** Slide 79 notes (part `notesSlide80.xml`): "Part B's document ID is applied through its patch specification until its source is regenerated." Slide 80 notes (part `notesSlide79.xml`): "Part B is the Digital Design System V3.0 (RC2 patch specification issued; PDF regeneration pending its source)." (The notes part numbers are swapped relative to the slide numbers in this deck; recorded exactly.)
- **Proposed wording.** Slide 79: "Part B is issued as its own RC2 deck with a token package (PartB_RC2/05_release); its component bundle does not yet exist (VAL-13, VAL-20)." Slide 80: "Closing. Part B is the Digital Design System V3.0, issued as Release Candidate 2 with a token package; its component bundle is pending (VAL-13, VAL-20). Part C …" (rest unchanged).
- **Governing evidence.** The Part B RC2 source and release deck exist (`PartB_RC2/01_source/B-RC2.pptx`, `05_release/…Part B — RC2.pptx`, 157,803 bytes) and carry document ID `GEM-DDS-V3.0-RC2` on the cover and on slide 34 ("Edition state · WORKING SPECIFICATION · NOT RELEASED"); a 35-page tagged PDF exists in `05_release`; a token package exists (`05_release/tokens`, 153 tokens). The component bundle does not exist: open evidence register — VAL-13 "In progress … no component source, no Storybook", VAL-20 "Not started", OD-SRC "Open". Part A slide 79's own body already lists "Related · GEM-DDS-V3.0-RC2 (Part B)". So the "patch specification … until its source is regenerated" statements are stale and the corrected text states only facts already recorded elsewhere.
- **Remark (not a defect).** The notes cite a repository path as a pointer; it names an existing folder and adds no rule.
- **Verdict: SUPPORTED.**

## C2 — Part C slide 44: letterhead status
- **Current authoritative wording.** "Templates are an OPEN DELIVERABLE (AB10, AB11, W01–W10): none exists yet."
- **Proposed wording.** "…W01–W10): a Letterhead Set (Application Revision 03) exists as a WORKING APPLICATION / PENDING VALIDATION; no template is accepted."
- **Governing evidence.** `GEM_Letterhead_Set_v1.1_Application_Revision_03/` exists in `main` with 8 Word templates; the package and its README call it a working application pending validation, and ODI01-R1 QA check 13 confirmed that all 8 templates carry the text "WORKING APPLICATION / PENDING VALIDATION". The Register records AB10, AB11 and W01–W14 as *scope decisions* (included in the final system), not as acceptance; OD-TPL (templates) is still an open deliverable and no template acceptance is recorded. The slide's own table keeps Letterhead as "[PENDING PRODUCTION MASTER]", which the new sentence agrees with. "None exists yet" is therefore contradicted by the repository, and "no template is accepted" is what the evidence supports.
- **Visual change.** Yes: the body sentence grows from two lines to two lines of different text; rendered before and after (`11_QA_Evidence/C44_before_after.png`); no overflow or collision; all other 77 pages of the candidate PDF are text-identical to the ODI01-R1 PDF.
- **Remark.** The sentence names "Application Revision 03", a package revision; if a later revision supersedes it the slide will need the same kind of synchronization again.
- **Verdict: SUPPORTED.**

## C3 — Part D checksum list: self-reference
- **Current authoritative content.** `Amenities_Portfolio_PartD_RC2/04_release/SHA256SUMS.txt` has 3 lines; one is its own entry `{L['c3']['removed_line'][:12]}…  SHA256SUMS.txt`. That value cannot be correct (a file cannot contain its own final hash): recomputed, the file hashes to `a4545133…`, not `0549416c…`.
- **Proposed content.** The same list without the self-entry (the PDF and PPTX lines, unchanged).
- **Governing evidence.** The two release hashes in the list verify against the current files. Of the 10 checksum lists in the repository, this is the only one that lists itself; the other 9 exclude themselves (scan recorded in `11_QA_Evidence/checksum_list_scan.txt`). Repository checksum verification (ODI01-R1) reported exactly this one mismatch.
- **Visual / notes-only.** Not a deck; plain-text list.
- **Verdict: SUPPORTED** (defect correction; no policy).

## C4 — "SYSTEM READY" → "NOT RELEASED"
- **Current authoritative wording.** `qa/GEM_V3_RC2_Release_Notes.md` line 3 and its identical copy `GEM_V3_RC2/03_qa/GEM_V3_RC2_Release_Notes.md` line 3: "State: RC2 SYNCHRONIZED · SYSTEM READY — EVIDENCE GATES REMAIN"; `qa/GEM_V3_RC2_Final_Release_Notes.md` lines 3 and 48: the same phrase.
- **Proposed wording.** "SYNCHRONIZED · NOT RELEASED · EVIDENCE GATES REMAIN" in all four places.
- **Governing evidence.** No deck uses "SYSTEM READY" (0 occurrences in Parts A–D release and candidate decks), whereas "NOT RELEASED" is already the decks' edition-state wording (Part A slide 79 "WORKING EDITION · NOT RELEASED"; Part B cover and slide 34; Part C). The notes themselves say "Not 'Approved V3.0'"; AC20 is Evidence Required in the Register; the owner-adopted status label uses NOT RELEASED. The correction removes a phrase that could be read as release readiness and replaces it with existing vocabulary.
- **Scope note.** The historical audit note `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md` also contains "SYSTEM READY — EVIDENCE GATES REMAIN" (a target classification in the audit text). It is a historical record outside the three notes files named in C4, so it was **not** changed and is listed under observations in `10`.
- **Combination note.** For `Final_Release_Notes`, the candidate is built on the ODI01-R1 D6 candidate, so the accepted D6 wording and C4 are combined in one file.
- **Verdict: SUPPORTED.**

## Observation (no edit)
A scan of all current decks found exactly three stale statements of the C1/C2 kind (Part A notes ×2, Part C slide 44); C1 and C2 cover all three.
''')
# ================= 03 trace
rows=[]
def rowd(e,deck,orig_hash,cand_hash,vis,notes): return f"| {e['id']} | {deck} | slide {e['slide']} | `{e['part']}` | {e['before']} | {e['after']} | {e['authority']} | {vis} | {notes} | `{orig_hash}` | `{cand_hash}` |"
ra=[rowd(e,'Part A',dA['src_sha256'],dA['dst_sha256'],('Yes' if e['id']=='D3B' else 'No'),('No' if e['id']=='D3B' else 'Yes')) for e in L['edits'] if e['document']=='Part A']
rc=[rowd(e,'Part C',dC['src_sha256'],dC['dst_sha256'],'Yes','No') for e in L['edits'] if e['document']=='Part C']
rn=[f"| C4 | `{n['source']}` | line 3{' and 48' if n['occurrences_replaced']==2 else ''} | n/a (Markdown) | …SYNCHRONIZED · SYSTEM READY — EVIDENCE GATES REMAIN… | …SYNCHRONIZED · NOT RELEASED · EVIDENCE GATES REMAIN… | see `02` C4 | No | n/a | `{n['src_sha256']}` | `{n['dst_sha256']}` |" for n in L['notes']]
c3=L['c3'];r3=f"| C3 | `{c3['source']}` | 3-line list | n/a (text) | includes `…  SHA256SUMS.txt` (self-entry) | self-entry removed; 2 lines | see `02` C3 | No | n/a | `{c3['src_sha256']}` | `{c3['dst_sha256']}` |"
wr('03_D3A_Implementation_Trace.md',f'''# 03 · D3A Implementation Trace (C1–C4) and the D3B example correction

**Owner authorization:** "If C1, C2, C3 and C4 are all verified … ACCEPT AND IMPLEMENT C1–C4" (D3A only). All four verified (`02`), so all four were implemented — as **controlled candidate copies**. A fifth, separate entry (ID D3B) records the Part A slide 75 example correction that follows the **owner decision of 2026-10-09: X12 STREAM = BRAND**; it is not part of C1–C4. **No authoritative original was modified.** Candidate decks are built on the current ODI01-R1 candidates (so accepted D4/D5/D6 work is preserved); "original hash" below is the hash of that base file. Authoritative originals: Part A `{AO['A'][:12]}…`, Part C `{AO['C'][:12]}…` (unchanged; verified by `git diff HEAD`).

Method: zip-level exact text replacement (`scripts/d3_apply_d3a.py`); every other package member is byte-identical to its base. Edit proof by element-level comparison (`11_QA_Evidence/d3a_edit_verification.json`).

| ID | Document | Slide/page | XML part | Before | After | Authority | Visible change? | Notes-only? | Original (base) hash | Candidate hash |
|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(ra+rc+[r3]+rn)}

## Files changed per candidate
- Part A candidate: parts `{', '.join(dA['parts_changed'])}` only.
- Part C candidate: part `{', '.join(dC['parts_changed'])}` only; PDF re-exported (LibreOffice 26.8, tagged); 77 of 78 pages text-identical to the ODI01-R1 PDF; page 44 differs as intended.
- Part A PDF: re-exported (LibreOffice 26.8, tagged) because slide 75 now changes visibly; 79 of 80 pages are text-identical to the ODI01-R1 Part A PDF; page 75 differs as intended (render: `11_QA_Evidence/A75_before_after.png`; no overflow, clipping, wrap change or collision; LibreOffice is review evidence, not native PowerPoint validation).
- Part D deck and PDF: not touched (C3 concerns only the checksum list).
- Notes: 3 candidate Markdown files (the 03_qa and qa copies of the Release Notes stay identical to each other).

## D3B example correction (slide 75)
Before: `Example: GEM_Logo_Horizontal_Black_v3.0_20261006.svg · convention X12 …` — After: `Example: GEM_BRAND_Horizontal_Black_v3.0_20261006.svg · convention X12 …` (shape `Text 4`, part `ppt/slides/slide75.xml`). **Only the STREAM token changed.** `Horizontal`, `Black`, `v3.0` and `20261006` are carried unchanged from Part A's own example. The ASSET taxonomy is **not** enumerated in any governing document (Part C slide 56: "Category and variant lists follow the asset library", but no list exists), so this edit does not confirm it: **ASSET token remains subject to existing controlled taxonomy confirmation.** The rule text on the slide ("The stream field follows the asset library folder.") is unchanged and is now consistent with the example.

## Not done (by design)
No original was edited in place; candidates were not promoted into authoritative folders; no deck other than A and C was changed; nothing was renamed (the BRAND mapping is a controlled-name mapping for the manifest, not a source migration).
''')
# ================= 04 comparison
def sample(csvf,names):
    r=list(csv.DictReader(open(pkg+'/'+csvf,encoding='utf-8')));d={x['Source filename (unchanged)']:x for x in r}
    return [(n,d[n]['Controlled name — exact X12 pattern'],d[n]['Controlled name if ASSET carried the noun "Logo" (readability test only)']) for n in names]
SM=['gem-horizontal-black.svg','gem-stacked-ink.pdf','gem-symbol-beige.eps','gem-symbol-nospark-white-1024.png','gem-horizontal-ink-clearspace-2u.svg','gem-symbol-nospark-black.svg']
sb=sample('05_D3B_X12_BRAND_Mapping.csv',SM);sl=sample('06_D3B_X12_Logo_Mapping.csv',SM)
ex='\n'.join(f"| `{a}` | `{b}` | `{c}` |" for (a,b,_),(_,c,_) in zip(sb,sl))
wr('04_D3B_X12_STREAM_Comparison.md',f'''# 04 · D3B — X12 STREAM Token: BRAND vs Logo

**Outcome: OWNER DECISION REQUIRED.** The evidence does not clearly establish either token as the one consistent with the existing X12 taxonomy. No recommendation is made. Nothing was renamed; no asset-ID or checksum rule was invented.

## The pattern and where STREAM is (not) defined
Register X12 (Approved): `GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext` — a shape only. **No STREAM values are listed anywhere in the Register.** Part C slide 56 adds: underscores separate fields, no spaces, "Latin letters and digits only", no "final/new/copy". Part A slide 75 adds: "A name should say what it is", "The stream field follows the asset library folder", and one example: `GEM_Logo_Horizontal_Black_v3.0_20261006.svg`.

## Answers to the eight questions
1. **What does STREAM mean in X12?** The only definition in the authority set is Part A slide 75: the stream field "follows the asset library folder". The folders are defined by Register X02–X11: 01 Brand Masters · 02 Type & Color · 03 Imagery · 04 Motion · 05 Applications · 06 Packaging · 07 Digital · 08 Localization · 09 Governance · 10 Archive. The folder-to-token spelling is **not** defined.
2. **Business/document stream, asset class, or another taxonomy?** Two readings coexist and are not reconciled. (a) *Library folder*: Part A slide 75. (b) *Business stream*: the Register uses "stream" for business streams (C03 Amenities & Packaging is "a business-stream descriptor"; C06 future streams only by formal architecture approval; C07 streams inherit GEM identity; C11/C12 descriptors are not locked into the logo and use ordinary typography). Under (b) the master brand has no business stream at all. Under neither reading is "asset class" the stated meaning, although the Part A example uses an asset-class word.
3. **How are other STREAM values formed?** No other STREAM value is defined. The only X12-shaped names in the repository are the 11 working files in `GEM_Brand_Assets_v1.0/01_svg`, all `GEM_BRAND_<ASSET>_<VARIANT>_v0.1_20261006.svg` (ASSET = TAGLINE, STATUS-LABEL, PALETTE-SHEET, STREAM-LINE). The kit README calls BRAND "a working choice for the owner to confirm".
4. **Does BRAND match that taxonomy?** Under reading (a), yes in kind: logos sit in 01 Brand Masters and BRAND is a plausible short form (spelling unconfirmed). Under (b), BRAND names the master brand, which is not a business stream. It contradicts the Part A example string.
5. **Does Logo match that taxonomy?** Under reading (a), no: there is no Logo folder. Under (b), no. It matches the Part A example exactly. It names an asset class, which is the job of the ASSET field, and "Logo" is a likely CATEGORY value in Part C Appendix N (the category list is not defined).
6. **Semantic collision with ASSET?** Not with ASSET=Horizontal/Stacked/Symbol/SymbolNoSpark (both options, 128/128 names unique, 0 collisions with the 11 working names). If ASSET carried the noun "Logo" (to keep names self-describing under BRAND), `Logo` as STREAM would repeat it in **{ST['Logo']['stream_in_asset_if_noun']} of 128** names; `BRAND` would not (**{ST['BRAND']['stream_in_asset_if_noun']}**).
7. **Which gives clearer examples** across horizontal / stacked / symbol / no-spark × Ink/Beige/Black/White? With ASSET held constant, `Logo` reads as self-describing (`GEM_Logo_Horizontal_Black…`); `BRAND` leaves "logo" implicit (`GEM_BRAND_Horizontal_Black…`) unless ASSET carries it (`GEM_BRAND_LogoHorizontal_Black…`). Examples below.
8. **Does either contradict existing controlled naming?** BRAND contradicts the Part A example. Logo contradicts the Part A folder rule on the same slide and would sit beside 11 BRAND-streamed working files in the same library folder, giving two STREAM values for one folder.

## Examples (same assets, exact pattern; vX.Y and YYYYMMDD stay placeholders)
| Source file (unchanged) | If STREAM = BRAND | If STREAM = Logo |
|---|---|---|
{ex}

Full mappings: `05_D3B_X12_BRAND_Mapping.csv`, `06_D3B_X12_Logo_Mapping.csv` — {ST['kit_logo_files_mapped']} logo files each (Horizontal 32, Stacked 32, Symbol 32, SymbolNoSpark 32; SVG 32, EPS 16, PDF 16, PNG 64) plus `metrics.json` marked "not mapped". ASSET and VARIANT values are held identical in both files so only STREAM differs.

Assumptions (labelled A1–A4 in the CSVs; **none is a naming rule**): ASSET = the kit's shape word in the Title-case style of the Part A example; VARIANT = colour word plus the kit's own qualifiers (2u clearspace, pixel size) appended, because the pattern has one VARIANT field and Part C allows letters and digits only; `vX.Y` and `YYYYMMDD` left as placeholders (version and manifest issue date undecided); extension as in the source.

## Semantic test (`07_D3B_X12_Semantic_Test.csv`, 13 criteria)
BRAND wins 6 · Logo wins 2 · Indeterminate 3 · Neither 2 (computed identical for both). The BRAND wins are on taxonomy-fit, scalability and grouping, mostly MODERATE or WEAK; the Logo wins are the exact match to the Part A example and name readability, both MODERATE. The criteria that carry authority (1 definition, 2 worked example, 3 internal consistency, 13 contradiction) point in **opposite directions** or are INDETERMINATE.

## Decision rule applied
"If the evidence clearly establishes one option as consistent with the existing X12 taxonomy: recommend it. If genuinely ambiguous: do not choose." The evidence is genuinely ambiguous:
1. Part A slide 75 gives a rule (stream = library folder) and an example (`Logo`) that cannot both hold; the Register defines no values.
2. Even if the folder rule governs, the folder-to-token spelling is undefined, so the folder rule supports "something derived from Brand Masters", not BRAND specifically.
3. The tally is not authority: the extra BRAND wins are design-quality criteria, not governing text.

## What the owner needs to decide (three short questions)
1. Is STREAM the asset-library folder (rule) or an asset class (example)?
2. If the folder: which token spells "01 Brand Masters" (BRAND, or another)? If an asset class: how do non-logo master-brand assets (tagline, palette sheet, status labels, stream lines) get a STREAM?
3. Which Part A slide 75 sentence is then corrected: the example, or the folder rule?

Consequences of each choice for other documents: `08`. Owner record: `09`.
''')
# ================= 08 consequences
def cat(b,l,note): return f"| {b} | {l} | {note} |"
tbl=[('Part A slide 75 — example string `GEM_Logo_Horizontal_Black_v3.0_20261006.svg`','Part A slide 75 example','REQUIRES UPDATE','NO CHANGE','Example would need the chosen STREAM (and the ASSET-noun question under BRAND).'),
('Part A slide 75 — sentence "The stream field follows the asset library folder."','Part A slide 75 rule','NO CHANGE','REQUIRES UPDATE','Under Logo the folder rule no longer describes the STREAM field and must be restated.'),
('Part A slide 75 notes; slide 79 change log','Part A','NO CHANGE','NO CHANGE','Asset-ID and checksum proposals stay pending (VAL-16).'),
('Part C slides 7, 56, 73 (pattern, Appendix N)','Part C','NO CHANGE','NO CHANGE','Pattern only; Appendix N "Category" field may need a note on overlap with STREAM if Logo is chosen (category list undefined).'),
('Part B slide 35 (kit renaming statement)','Part B','NO CHANGE','NO CHANGE','Pattern only; lists source names, which stay.'),
('Part D deck','Part D','NO CHANGE','NO CHANGE','No X12 reference.'),
('Register X12 and X02–X11','Register','NO CHANGE','NO CHANGE','Register wording is the pattern; an owner-authorized note listing STREAM values is optional, not required.'),
('GEM_Brand_Assets_v1.0/README.md ("BRAND … working choice for the owner to confirm")','Kit README','REQUIRES UPDATE','REQUIRES UPDATE','Under BRAND: record it as confirmed. Under Logo: record that BRAND is superseded for logos.'),
('Official kit logo files (128 images) and their `SHA256SUMS.txt`','Kit source','SOURCE NAME MUST REMAIN UNCHANGED','SOURCE NAME MUST REMAIN UNCHANGED','X12 controls controlled/manifest names at first manifest (Part C slide 7); it does not authorize renaming the source kit.'),
('GEM_Brand_Assets_v1.0/01_svg working files (11 × GEM_BRAND_…_v0.1)','Kit working files','NO CHANGE','MANIFEST ONLY','Under Logo these non-logo assets keep BRAND or need another STREAM: two STREAM values in one library folder; decide in the manifest, not by renaming.'),
('GEM_Brand_Assets_v1.0/05_layout_matched files','Kit working files','SOURCE NAME MUST REMAIN UNCHANGED','SOURCE NAME MUST REMAIN UNCHANGED','Referenced by build scripts; controlled names in the manifest only.'),
('Letterhead package references to kit file names; build scripts (`sync_logos.py`, `edit_assets_*.py`, `package.py`, `spec.py`, `extra_checks.py`)','Dependents','SOURCE NAME MUST REMAIN UNCHANGED','SOURCE NAME MUST REMAIN UNCHANGED','They reference source names; touch only if a rename is separately authorized.'),
('Controlled release manifest (VAL-16, not started)','Manifest','MANIFEST ONLY','MANIFEST ONLY','Controlled names live here; the chosen mapping CSV (05 or 06) becomes its input.'),
('ODI01-R1 `13_D3_Unresolved.md` and the carried-forward X12 mapping CSVs','Earlier packages','NO CHANGE','NO CHANGE','History; superseded by this D3 package, not edited.'),
('Open evidence register / release notes','qa/','NO CHANGE','NO CHANGE','VAL-16 stays Not started.')]
wr('08_D3_Cross_Document_Consequences.md','# 08 · D3B Cross-Document Consequences\n\nNo D3B option is recommended (`04`), so consequences are shown for **both**. Nothing below was modified. Categories: REQUIRES UPDATE · NO CHANGE · MANIFEST ONLY · SOURCE NAME MUST REMAIN UNCHANGED. **X12 controls controlled names and manifests; it does not authorize renaming the historical/source kit files.**\n\n| Artifact | Scope | If BRAND is adopted | If Logo is adopted | Note |\n|---|---|---|---|---|\n'+'\n'.join(f"| {a} | {s} | {b} | {l} | {n} |" for a,s,b,l,n in tbl)+'\n\n**D3A is separate:** its four candidates (`03`) do not depend on the D3B outcome. Promoting them into authoritative folders needs a separate authorized change.\n')
# ================= 09 owner decision record
wr('09_D3_Owner_Decision_Record.md','''# 09 · D3 Owner Decision Record

D3 has two independent parts. They are recorded separately and must not be merged.

D3A — Synchronization corrections C1–C4

[x] ACCEPTED
[ ] PARTIALLY ACCEPTED
[ ] REJECTED

Evidence:
Owner instruction in this task: "If C1, C2, C3 and C4 are all verified as synchronization corrections supported by existing authority: ACCEPT AND IMPLEMENT C1–C4 … explicit owner authorization for D3A only." All four were verified SUPPORTED against the Register and the current Parts A–D (`02_D3A_Authority_Verification.md`) and implemented as controlled candidate copies (`03_D3A_Implementation_Trace.md`). Scope of acceptance: the candidates only. Promotion into authoritative folders requires a separate authorized change. No push (D7 pending).

D3B — X12 STREAM token

[ ] BRAND
[ ] Logo
[ ] OTHER: __________
[x] OWNER DECISION STILL REQUIRED

Evidence:
`04_D3B_X12_STREAM_Comparison.md` and `07_D3B_X12_Semantic_Test.csv`: Register X12 defines the pattern but no STREAM values; Part A slide 75 says the stream field follows the asset library folder (Register X02–X11: 01 Brand Masters …) yet its only example uses `Logo`; the Register uses "stream" for business streams elsewhere; the working files use BRAND (marked "a working choice for the owner to confirm"). Neither token is clearly established. The owner questions are listed in `04`.

Brand Owner: __________________

Decision date: __________________

Conditions / comments: __________________

D7 interlock: nothing in this package may be pushed while D7 is LEGAL/IP DECISION PENDING. AC20 remains OPEN.
''')
# ================= 10 remaining gates
wr('10_D3_Remaining_Gates.md',f'''# 10 · D3 Remaining Gates and Observations

| # | Item | State |
|---|---|---|
| 1 | **D3B** X12 STREAM token | **OWNER DECISION REQUIRED** (`04`, `09`) |
| 2 | Promotion of the D3A candidates (C1–C4) into authoritative sources | Needs a separate authorized change; not done |
| 3 | **D7** repository visibility / Legal-IP | **LEGAL/IP DECISION PENDING — DO NOT PUSH** |
| 4 | **AC20** release authorization | **OPEN** |
| 5 | VAL-16 controlled release manifest | Not started; D3B output is its input |
| 6 | Native PowerPoint / Word / Acrobat / AT QA of the candidates | Not performed |
| 7 | D5, D8 and the other earlier gates | Unchanged (see ODI01-R1 `14_Remaining_Gates.md`) |

## Observations (no edit made)
- `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md` still contains "SYSTEM READY — EVIDENCE GATES REMAIN" as a target classification (historical record; outside C4).
- The existing 11 working names in `GEM_Brand_Assets_v1.0/01_svg` contain hyphens inside fields (for example STATUS-LABEL); Part C slide 56 says "Latin letters and digits only". A controlled-name question for the manifest, outside D3.
- Part A slide 75's rule and example disagree (the D3B ambiguity).
- The Part C slide 44 candidate names "Application Revision 03"; a later revision would need the same synchronization.
''')
# ================= 01 exec
wr('01_D3_Executive_Summary.md',f'''# 01 · D3 Owner Decision Package — Executive Summary

**{LABEL}**
**D7 — LEGAL/IP DECISION PENDING · NO PUSH · AC20 — OPEN**

2026-10-09 · branch `claude/gem-worktree-safety-30b559` · starting HEAD `ab6d886` (on `4ea0d11` → `a5d9acc` → `209c934` → `ab6d886`). Local only: nothing pushed, merged or published; no PR, tag or release.

## Result in one table
| Part | Outcome |
|---|---|
| **D3A** — synchronization corrections C1–C4 | **All four SUPPORTED by existing authority and implemented as candidate copies** under the owner's explicit D3A instruction. Authoritative originals untouched. |
| **D3B** — X12 STREAM token (BRAND vs Logo) | **OWNER DECISION REQUIRED.** Evidence is genuinely ambiguous; no recommendation. Both mappings built on identical assets (128 logo files each). |

## D3A (`02`, `03`)
| | Change | Where | Visible? |
|---|---|---|---|
| C1 | Part B described as issued RC2 deck + token package; component bundle pending | Part A slides 79–80 notes (notes-only) | No |
| C2 | Letterhead set acknowledged as a working application pending validation; no template accepted | Part C slide 44 body | Yes (rendered; fits) |
| C3 | Self-referencing checksum entry removed | Part D `04_release/SHA256SUMS.txt` | No |
| C4 | "SYSTEM READY" → "NOT RELEASED" (4 occurrences) | 3 release-notes files | No |

Edit proof: only the intended parts differ from their base; Part C PDF is text-identical to the ODI01-R1 PDF on 77 of 78 pages (page 44 differs as intended). QA results: `11_QA_Evidence/d3_qa_results.md`.

## D3B (`04`–`08`)
STREAM is defined only by Part A slide 75 ("follows the asset library folder": 01 Brand Masters …); the Register lists no values; the same slide's example uses `Logo`; the Register uses "stream" for business streams elsewhere; the repository's 11 working files use `BRAND` (flagged as an unconfirmed working choice). Computed facts: both options give 128/128 unique names with no collisions; if ASSET carried the noun "Logo", `Logo` as STREAM would repeat it in 128 of 128 names. Semantic test: BRAND 6 · Logo 2 · Indeterminate 3 · Neither 2, but the authority-bearing criteria conflict. Three short owner questions are in `04`. Consequences for other documents under each choice: `08`.

## Not done
No source asset renamed; no asset-ID or checksum rule invented; no original modified; D3A candidates not promoted; nothing pushed.

## Package map
`02` authority verification · `03` implementation trace · `04` D3B comparison · `05`/`06` mappings · `07` semantic test · `08` consequences · `09` owner record · `10` remaining gates · `11_QA_Evidence/` · `12_Candidate_Files/`. Existing ODI01-R1 and D7 packages are referenced, not copied.
''')
print('docs built')
