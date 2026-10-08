"""Second stage (run after d3_build_docs.py): records the D3B OWNER DECISION (X12 STREAM = BRAND, 2026-10-09) in 01, 04, 08, 09, 10. Comparison evidence is preserved and marked prior state. Usage: d3b_docs.py <pkg_dir>"""
import sys,os
P=sys.argv[1]
LABEL='GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE'
def rd(f): return open(os.path.join(P,f),encoding='utf-8').read()
def wr(f,t): open(os.path.join(P,f),'w',encoding='utf-8').write(t)
def sub(f,a,b):
    t=rd(f);assert a in t,(f,a[:60]);wr(f,t.replace(a,b,1))
RAT='''- X12 STREAM follows the asset-library / controlled stream taxonomy.
- The governing asset-library category is Brand Masters.
- BRAND applies coherently across logo, symbol and related master-brand assets.
- BRAND avoids semantic duplication between STREAM and ASSET.
- The Part A slide 75 example using Logo conflicts with the rule stated on the same slide and is therefore treated as a synchronization defect in the example, not as the governing taxonomy.
- Existing source / historical filenames are not automatically renamed by this decision.
- No asset-ID algorithm is approved. No new checksum algorithm is approved. Source assets remain unchanged unless separately authorized through controlled migration.'''
# ---------------- 09
wr('09_D3_Owner_Decision_Record.md',f'''# 09 · D3 Owner Decision Record

**D3A — RESOLVED · D3B — RESOLVED · D3 — RESOLVED AT OWNER-DECISION LEVEL · X12 STREAM = BRAND**
Recorded 2026-10-09 from the Brand Owner's explicit instruction. Not to be re-confirmed.

D3A — Synchronization corrections C1–C4

[x] ACCEPTED
[ ] PARTIALLY ACCEPTED
[ ] REJECTED

Decision:
C1–C4 are accepted as supported synchronization corrections and remain implemented in controlled candidate copies.

Evidence:
`02_D3A_Authority_Verification.md` (all four SUPPORTED against the Register and the current Parts A–D) and `03_D3A_Implementation_Trace.md`. Scope: candidate copies only; promotion into authoritative folders is a separate authorized change.

D3B — X12 STREAM token

[x] BRAND
[ ] Logo
[ ] OTHER
[ ] OWNER DECISION STILL REQUIRED

Decision:
Use BRAND as the controlled X12 STREAM token for the GEM master-brand asset family.

Owner rationale (recorded in full):
{RAT}

Evidence (decision history, preserved):
- BRAND aligns with the Brand Masters / asset-library-folder reading (Part A slide 75 rule; Register X02 "01 Brand Masters"), has no STREAM/ASSET duplication (0 of 128 names, even if ASSET carried the noun "Logo"), scales to the other master-brand assets, and is already used by the 11 working files.
- Logo matched the explicit Part A slide 75 example and reads as self-describing; it is **NOT SELECTED** and is retained as history only.
- The governing evidence conflicted (rule vs example on the same slide; no authoritative enumeration of STREAM tokens). The owner resolved the conflict in favour of the rule. The conflict stays documented in `04` and `07`.

Effect recorded in this package: STREAM = BRAND is the SELECTED CONTROLLED STREAM; `D3B_X12_Selected_BRAND_Mapping.csv` is the SELECTED CONTROLLED MAPPING (128 rows, manifest-only, no source renames); the Logo mapping is NOT SELECTED; the Part A slide 75 example is corrected in a controlled candidate (STREAM token only).

D3 = RESOLVED AT OWNER-DECISION LEVEL.

This does NOT mean:
- AC20 closed, or release authorized;
- Legal/IP cleared (D7 remains LEGAL/IP DECISION PENDING; NO PUSH);
- source assets migrated or renamed;
- an asset-ID algorithm or checksum algorithm approved;
- production readiness established, or any font, native-QA or supplier evidence gate closed.

Brand Owner: owner instruction of 2026-10-09 (named signature/initials not recorded in this file): __________________

Conditions / comments: STREAM = BRAND applies prospectively to controlled names and manifests (X12). The ASSET and VARIANT value lists remain subject to controlled taxonomy confirmation (`10`).
''')
# ---------------- 04
sub('04_D3B_X12_STREAM_Comparison.md','# 04 · D3B — X12 STREAM Token: BRAND vs Logo','# 04 · D3B — X12 STREAM Token: BRAND (SELECTED) vs Logo (NOT SELECTED) — decision record and comparison history')
sub('04_D3B_X12_STREAM_Comparison.md','**Outcome: OWNER DECISION REQUIRED.** The evidence does not clearly establish either token as the one consistent with the existing X12 taxonomy. No recommendation is made. Nothing was renamed; no asset-ID or checksum rule was invented.',f'''**OWNER DECISION RECORDED — SELECTED CONTROLLED STREAM: BRAND (2026-10-09). NOT SELECTED: Logo.** D3B is resolved at owner-decision level. Logo remains in this document as part of the decision history; it is not the governing STREAM token.

Owner rationale:
{RAT}

**Prior state (comparison stage, preserved below unchanged): OWNER DECISION REQUIRED.** At that stage the evidence did not clearly establish either token as consistent with the existing X12 taxonomy and no recommendation was made. Nothing was renamed; no asset-ID or checksum rule was invented — and that is still true.

**Controlled outputs:** `D3B_X12_Selected_BRAND_Mapping.csv` (SELECTED CONTROLLED MAPPING; 128 rows; STREAM = BRAND on every row; source rename NO; manifest-only YES). `05` is the comparison-stage copy of the same names; `06` is NOT SELECTED (historical).''')
sub('04_D3B_X12_STREAM_Comparison.md','| Source file (unchanged) | If STREAM = BRAND | If STREAM = Logo |','| Source file (unchanged) | If STREAM = BRAND — SELECTED | If STREAM = Logo — NOT SELECTED |')
sub('04_D3B_X12_STREAM_Comparison.md','Full mappings: `05_D3B_X12_BRAND_Mapping.csv`, `06_D3B_X12_Logo_Mapping.csv`','Full mappings: `D3B_X12_Selected_BRAND_Mapping.csv` (selected), `05_D3B_X12_BRAND_Mapping.csv` (comparison stage), `06_D3B_X12_Logo_Mapping.csv` (NOT SELECTED, history)')
sub('04_D3B_X12_STREAM_Comparison.md','## Decision rule applied','## Decision rule applied at the comparison stage (prior state)')
sub('04_D3B_X12_STREAM_Comparison.md','## What the owner needs to decide (three short questions)','## The three owner questions (prior state) and how the owner decision answers them')
sub('04_D3B_X12_STREAM_Comparison.md','Consequences of each choice for other documents: `08`. Owner record: `09`.','''**Answers recorded by the owner decision:** (1) STREAM follows the asset-library / controlled stream taxonomy (Brand Masters), i.e. the folder rule governs. (2) The folder-derived token is **BRAND**. (3) The Part A slide 75 **example** is the defect and is corrected (candidate: STREAM token only); the rule text stays.

**Still open (not decided by this record):** the enumerated ASSET and VARIANT value lists. `Horizontal` and `Black` appear only in Part A's own example; the kit's other shape words and qualifiers are working tokens. They are marked REQUIRES TAXONOMY CONFIRMATION in the selected mapping and are not silently normalized.

Consequences for other documents: `08`. Owner record: `09`.''')
sub('04_D3B_X12_STREAM_Comparison.md','## Semantic test (`07_D3B_X12_Semantic_Test.csv`, 13 criteria)','## Semantic test (`07_D3B_X12_Semantic_Test.csv`, 13 criteria + final disposition)')
# ---------------- 08
rows=[('Part A slide 75 — example string','UPDATE NOW — CONTROLLED CANDIDATE EXAMPLE','Done in the D3 candidate Part A (`GEM_BRAND_Horizontal_Black_v3.0_20261006.svg`; STREAM token only). The authoritative original is unchanged; promotion is a separate authorized change.'),
('Part A slide 75 — rule "The stream field follows the asset library folder."','NO CHANGE — ALREADY CONSISTENT','The rule is the governing taxonomy; the example was the defect.'),
('Part A slide 75 — ASSET and VARIANT tokens in the example (Horizontal, Black)','REQUIRES TAXONOMY CONFIRMATION','Carried unchanged from Part A; no enumerated ASSET/VARIANT list exists.'),
('Part A slide 75 notes; slide 79 change log','NO CHANGE — ALREADY CONSISTENT','Asset-ID and checksum proposals stay proposals.'),
('Part C slides 7, 56, 73 (pattern; Appendix N Category/Asset/Variant)','NO CHANGE — ALREADY CONSISTENT','Pattern only. "Category and variant lists follow the asset library" — the lists themselves need taxonomy confirmation (see above).'),
('Part B slide 35 (kit renaming statement)','NO CHANGE — ALREADY CONSISTENT','Pattern only; source names stay.'),
('Part D deck','NO CHANGE — ALREADY CONSISTENT','No X12 reference.'),
('Register X12 and X02–X11','NO CHANGE — ALREADY CONSISTENT','The Register states the pattern and the folders; no row was edited. The owner decision is recorded in `09`.'),
('D3 package documents 01, 03, 04, 07, 09, 10 and the mapping CSVs','UPDATE NOW — CANDIDATE DOCUMENTATION','Done in this pass.'),
('GEM_Brand_Assets_v1.0/README.md ("BRAND … working choice for the owner to confirm")','UPDATE LATER — CONTROLLED MANIFEST','Record BRAND as confirmed when the README/manifest is next issued under change control. Not edited now.'),
('Controlled release manifest (VAL-16, not started)','UPDATE LATER — CONTROLLED MANIFEST','Input: `D3B_X12_Selected_BRAND_Mapping.csv`. Version/date and the asset-ID/checksum proposals remain undecided.'),
('Official kit logo files (128 images) and their `SHA256SUMS.txt`','NO CHANGE — SOURCE KIT','X12 controls controlled names at first manifest (Part C slide 7); it does not authorize renaming source files. The mapping is manifest-only.'),
('GEM_Brand_Assets_v1.0/01_svg working files (11 × GEM_BRAND_…_v0.1)','NO CHANGE — SOURCE KIT','STREAM is already BRAND. Their hyphenated field values (Part C slide 56: "Latin letters and digits only") are a manifest-time question.'),
('GEM_Brand_Assets_v1.0/05_layout_matched files','NO CHANGE — SOURCE KIT','Referenced by build scripts.'),
('Letterhead package references to kit file names; build scripts','NO CHANGE — HISTORICAL SOURCE','They reference source names; touch only if a migration is separately authorized.'),
('ODI01-R1 package (`13_D3_Unresolved.md`, `14_Remaining_Gates.md`, carried-forward mapping CSVs) and the D7 package','NO CHANGE — HISTORICAL SOURCE','Point-in-time committed records stating D3 as unresolved at that time; superseded by this package, not edited.'),
('AFC01/AFC02/ODI01 history; `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md`','NO CHANGE — AUDIT HISTORY','Historical.')]
wr('08_D3_Cross_Document_Consequences.md','# 08 · D3B Cross-Document Consequences (STREAM = BRAND)\n\n**SELECTED CONTROLLED STREAM: BRAND** (owner decision 2026-10-09). **X12 governs controlled naming prospectively. Historical and source-kit filenames remain unchanged unless separately migrated through controlled change management.** The owner decision is not permission for bulk renaming; no file was renamed. Nothing below was modified except where marked "UPDATE NOW".\n\nCategories: UPDATE NOW — CANDIDATE DOCUMENTATION · UPDATE NOW — CONTROLLED CANDIDATE EXAMPLE · UPDATE LATER — CONTROLLED MANIFEST · NO CHANGE — HISTORICAL SOURCE · NO CHANGE — SOURCE KIT · NO CHANGE — AUDIT HISTORY · REQUIRES TAXONOMY CONFIRMATION · plus NO CHANGE — ALREADY CONSISTENT (one label added for text that already agrees with BRAND).\n\n| Artifact | Classification | Note |\n|---|---|---|\n'+'\n'.join(f'| {a} | **{c}** | {n} |' for a,c,n in rows)+'\n\nThe earlier two-column comparison (if BRAND / if Logo) is preserved in the committed history of this package (`ba526a1`).\n')
# ---------------- 10
wr('10_D3_Remaining_Gates.md',f'''# 10 · D3 Remaining Gates and Observations

**D3A — RESOLVED · D3B — RESOLVED · D3 — RESOLVED AT OWNER-DECISION LEVEL · X12 STREAM = BRAND.**
Resolved at owner-decision level does not mean every consequence is done, and it does not affect D7, AC20, the font evidence, native-application QA, supplier evidence or the Legal/IP gates.

| # | Item | State |
|---|---|---|
| 1 | D3A C1–C4 | ACCEPTED; implemented in candidate copies |
| 2 | D3B X12 STREAM | **BRAND — SELECTED**; Logo NOT SELECTED |
| 3 | Promotion of the D3A candidates and the slide 75 example correction into authoritative sources | Separate authorized change; not done |
| 4 | **ASSET and VARIANT value lists** (X12 [ASSET], [VARIANT]) | **REQUIRES TAXONOMY CONFIRMATION** — no enumerated list exists; the selected mapping marks 116 of 128 rows LOW and 12 MODERATE |
| 5 | Version (`vX.Y`) and issue date (`YYYYMMDD`) for controlled names | Undecided; placeholders kept |
| 6 | Asset-ID scheme (`GEM-[CATEGORY]-[NNN]`) and SHA-256 manifest checksums | Proposals only (Parts A, C); **not approved** |
| 7 | VAL-16 controlled release manifest | Not started; first use of the selected mapping |
| 8 | Migration of source-kit filenames, if ever wanted | Not authorized; would need controlled change management |
| 9 | **D7** repository visibility / Legal-IP | **LEGAL/IP DECISION PENDING — DO NOT PUSH** |
| 10 | **AC20** release authorization | **OPEN** |
| 11 | Native PowerPoint / Word / Acrobat / AT QA; font, supplier and Legal/IP evidence | Open (unchanged) |

## Observations (no edit made)
- `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md` still contains "SYSTEM READY — EVIDENCE GATES REMAIN" as a target classification (historical record).
- The 11 working names in `GEM_Brand_Assets_v1.0/01_svg` use hyphens inside fields (for example STATUS-LABEL); Part C slide 56 says "Latin letters and digits only". A manifest-time question.
- The Part C slide 44 candidate names "Application Revision 03"; a later revision would need the same synchronization.
''')
# ---------------- 01
t=rd('01_D3_Executive_Summary.md')
a=t.index('## Result in one table');b=t.index('## D3A (')
new=f'''## Governance status
**D3A — RESOLVED** (C1–C4 accepted; implemented in candidate copies).
**D3B — RESOLVED** (owner decision 2026-10-09): **X12 STREAM = BRAND**.
**D3 — RESOLVED AT OWNER-DECISION LEVEL.** This does not close AC20, authorize release, clear Legal/IP, migrate any source asset or establish production readiness.
D7 — LEGAL/IP DECISION PENDING · DO NOT PUSH. AC20 — OPEN.

## Result in one table
| Part | Outcome |
|---|---|
| **D3A** — synchronization corrections C1–C4 | **All four SUPPORTED and implemented as candidate copies.** Authoritative originals untouched. |
| **D3B** — X12 STREAM token | **BRAND SELECTED** (owner decision); Logo NOT SELECTED, kept as decision history. Selected controlled mapping: `D3B_X12_Selected_BRAND_Mapping.csv` (128 rows, manifest-only, no source renames). Part A slide 75 example corrected in a controlled candidate (STREAM token only). |

'''
t=t[:a]+new+t[b:]
t=t.replace('**D7 — LEGAL/IP DECISION PENDING · NO PUSH · AC20 — OPEN**\n\n2026-10-09','**D3A — RESOLVED · D3B — RESOLVED (STREAM = BRAND) · D3 — RESOLVED AT OWNER-DECISION LEVEL · D7 — LEGAL/IP DECISION PENDING · NO PUSH · AC20 — OPEN**\n\n2026-10-09',1)
c=t.index('## D3B (`04`');d=t.index('## Not done')
t=t[:c]+'''## D3B (`04`–`08`, `D3B_X12_Selected_BRAND_Mapping.csv`)
Decision history (preserved): STREAM is defined only by Part A slide 75 ("follows the asset library folder"; Register X02 "01 Brand Masters"); the Register lists no values; the same slide's example used `Logo`; the 11 working files use `BRAND`. The owner resolved the conflict for the rule: the example using Logo is a synchronization defect, not the governing taxonomy. Computed facts: both options gave 128/128 unique names with no collisions; BRAND never repeats ASSET, whereas `Logo` would in 128 of 128 names if ASSET carried the noun. Semantic test final disposition: BRAND — SELECTED; Logo — NOT SELECTED (the conflict stays documented). **Still open:** the enumerated ASSET/VARIANT lists (REQUIRES TAXONOMY CONFIRMATION), version/date, and the undecided asset-ID and checksum proposals. Consequences for other documents: `08`.

'''+t[d:]
t=t.replace('No source asset renamed; no asset-ID or checksum rule invented; no original modified; D3A candidates not promoted; nothing pushed.','No source asset or file renamed; no asset-ID or checksum rule invented or approved; no original modified; candidates not promoted; nothing pushed.')
t=t.replace('`05`/`06` mappings · `07` semantic test','`D3B_X12_Selected_BRAND_Mapping.csv` (selected) · `05`/`06` comparison mappings (06 NOT SELECTED) · `07` semantic test')
t=t.replace('QA results: `11_QA_Evidence/d3_qa_results.md`.','D3 QA results: `11_QA_Evidence/d3_qa_results.md` (text, structure and manifest checks; not native-application validation); QA defect log: `11_QA_Evidence/d3_qa_defect_log.md`.')
t=t.replace('starting HEAD `ab6d886` (on `4ea0d11` → `a5d9acc` → `209c934` → `ab6d886`)','D3B pass starting HEAD `ba526a1` (lineage `4ea0d11` → `a5d9acc` → `209c934` → `ab6d886` → `ba526a1`)')
t=t.replace('| C4 | "SYSTEM READY" → "NOT RELEASED" (4 occurrences) | 3 release-notes files | No |','| C4 | "SYSTEM READY" → "NOT RELEASED" (4 occurrences) | 3 release-notes files | No |\n| D3B | Example `GEM_Logo_Horizontal_Black_…` → `GEM_BRAND_Horizontal_Black_…` (STREAM token only; separate from C1–C4) | Part A slide 75 body | Yes (rendered; fits) |')
wr('01_D3_Executive_Summary.md',t)
print('docs updated')
