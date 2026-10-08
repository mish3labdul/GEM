from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,TextStringObject
import json,hashlib,shutil,datetime
R=Path('work/GEM/GEM_Letterhead_Set_v1.1');B=R.parent/'GEM_Letterhead_Set_v1.0';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=Path('work/letterhead_revision_02/spec_release/GEM_Letterhead_Specification.pdf');r=PdfReader(src);assert len(r.pages)==3
w=PdfWriter();w.clone_document_from_reader(r);w.root_object[NameObject('/Lang')]=TextStringObject('en-GB');w.add_metadata({'/Title':'GEM Letterhead Specification Set v1.1 Application Revision 02','/Subject':'WORKING APPLICATION / PENDING VALIDATION; proposed application settings and pending production values','/Author':''});w.write(R/'03_specs/GEM_Letterhead_Specification.pdf')
for script in ['pdf_fix.py','render.py','spec.py','verify.py','proof.py','package.py']:shutil.copy2(Path('work/letterhead_revision_02')/script,R/'00_source'/script)
sources=json.loads((R/'00_source/Source_Snapshot.json').read_text())['governing_files']
asset_lines=['# GEM Letterhead Asset Source Register','', '**Set v1.1 Application Revision 02 • WORKING APPLICATION / PENDING VALIDATION**','', 'All source paths are relative to mish3labdul/GEM. Supplied SVG and PNG bytes are unchanged from the selected corrected source; exact official-kit hashes are checked. No redrawing, tracing, recolouring or mirroring. Font acceptance/licensing remains pending even where a supplied OFL is present.','', '| Repository path / filename | Type / variant | Use | Status and evidence gate | SHA256 |','|---|---|---|---|---|']
for colour in ['ink','black']:
 for typ,file in [('svg',f'gem-horizontal-{colour}.svg'),('png',f'gem-horizontal-{colour}-2048.png')]:
  path=Path(f'GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/{typ}/{file}');f=R.parent/path
  asset_lines.append(f'| {path} | {"Vector SVG" if typ=="svg" else "Supplied raster PNG fallback"} / {colour} | {"Minimal" if colour=="black" else "English, Arabic, bilingual first pages and Executive"} {"primary" if typ=="svg" else "Office compatibility only"} | Kit working asset; production-master acceptance PENDING; AC20 open | {sha(f)} |')
  # Confirm exact source is present in at least one new DOCX.
  assert any(f.read_bytes() in [ZipFile(x).read(n) for n in ZipFile(x).namelist() if n.startswith('word/media/')] for x in (R/'01_templates').glob('*.docx'))
for family,dirname in [('Inter','inter'),('Jost','jost'),('NotoSansArabic','notosansarabic')]:
 f=B/'00_source/fonts'/dirname/(family+'-Regular.ttf');path=f.relative_to(R.parent)
 asset_lines.append(f'| {path} | Verified Regular TTF working build | Body/metadata/footer; subject/tagline; Arabic respectively | Font master/build and licensing acceptance PENDING; existing font provenance preserved | {sha(f)} |')
 lic=f.parent/'OFL.txt';asset_lines.append(f'| {lic.relative_to(R.parent)} | Supplied font licence text | Provenance only | Rights acceptance still PENDING | {sha(lic)} |')
(R/'03_specs/GEM_Letterhead_Asset_Source_Register.md').write_text('\n'.join(asset_lines)+'\n')
original_dates=[]
for f in (B/'07_final_audit/corrected_docx').glob('*.docx'):
 core=E.fromstring(ZipFile(f).read('docProps/core.xml'));ns={'d':'http://purl.org/dc/terms/'}
 original_dates.append({'file':str(f.relative_to(R.parent)),'original_created':core.findtext('d:created',namespaces=ns),'original_modified':core.findtext('d:modified',namespaces=ns),'sha256':sha(f)})
(R/'00_source/Original_Source_Dates.json').write_text(json.dumps({'revision_date':'2026-10-07','packaged_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_dates':original_dates},indent=2))
fixes={
'LH01':('PASS','Selected corrected baseline, retained useful release edits, regenerated all companions and synchronized release copies. Original variants archived in place, not overwritten.'),
'LH02':('PASS / PENDING PLATFORM RETEST','Inter LTR identifiers remain whole; Executive subject is Jost Regular; fresh exports use only Inter/Jost/Noto Regular. Specification theme-font inheritance also removed after the final check detected an unintended substitute. No active substitute or synthetic Bold observed. Native Word platform matrix pending.'),
'LH03':('FAIL REMAINING / PENDING ACCESSIBILITY ACCEPTANCE','Repaired omitted Arabic combining-mark ToUnicode entries from exporter ActualText, corrected base/mark cluster allocation, and preserved logical source paragraph ActualText. Pypdf layout and pdfplumber independently match the complete Arabic glyph inventory; semantic source paragraphs match DOCX. Generic plain extraction still reverses/omits mixed RTL fragments. This finding is not closed. Native copy/search and AT must pass before controlled real-world PDF use.'),
'LH04':('PASS / PENDING PLATFORM RETEST','Separated date and reference into editable lines; full technical ID uses one explicit Inter LTR run. Short/long codes render in correct bracket order. Email/URL/phone test fields are fixtures only, never company details.'),
'LH05':('PASS / PENDING NATIVE RETEST','Selected robust live PAGE/NUMPAGES fields with 9 pt Inter formatting. One-page templates and 2/3-page explicit/automatic-flow fixtures show correct page values in the bundled renderer. No incomplete Page of output.'),
'LH06':('PASS','Working and localization status retained in all first/default footers of Arabic and bilingual templates, including automatic continuations.'),
'LH07':('PASS','Selected corrected Jost Regular tagline at 10.5 pt, 38 twips (~0.181em). Body and Arabic have zero expanded tracking.'),
'LH08':('PENDING / REQUIRES OWNER / REQUIRES SUPPLIER','Raised essential footer/status and SAMPLE CONTENT to 9 pt; footer explicitly 12.6 pt exact leading. Visual/grayscale review passed with no collision. This is a working digital application choice, not a newly approved stationery/physical minimum. Owner digital legibility and supplier print proof remain required.'),
'LH09':('PASS / PENDING NATIVE RETEST','Selected clean editable corrected source and discarded corrupt release re-save structures while preserving originals. No unintended clipboard-like symbol appears in fresh exports. Exact original renderer/add-in cause is not asserted.'),
'LH10':('PASS / PENDING RIGHTS ACCEPTANCE','Preserved three valid Regular-only font payloads from the corrected candidate. Every payload decoded as a usable TTF with cmap; decoded hashes recorded. No zero-byte embedded parts. Acceptance/licence gate remains open.')}
old=json.loads(Path('outputs/GEM_Letterhead_UIAudit_BrandKit_Review/Findings.json').read_text());updated=[]
qa=['# GEM Letterhead QA Report','', '**Set v1.1 Application Revision 02 • 7 October 2026**','', '**WORKING APPLICATION / PENDING VALIDATION**','', 'Eight findings pass available technical checks. LH03 remains open because full Arabic plain-text extraction/reader acceptance is not proven; LH08 remains an owner/supplier validation item. This is a controlled working package, not an approved stationery system or production release.','', '## Source and method','', 'Live repository main SHA reverified: `334744c72dbbb6681034996fcca595213a7623a2`. All governing-file hashes match the audit snapshot. Register > Part A > Part B > Part C > official asset kit > QA/evidence discipline. No External Partners Brief used.','', 'Eight editable templates and twelve QA fixtures rendered using the bundled LibreOffice renderer with the verified working fonts. All template samples are one page. Explicit 2/3-page and automatic-flow fixtures pass pagination in English, Arabic and bilingual; each automatic-flow fixture produces three pages. Long bilingual fields deliberately flow to two pages. All affected visuals reviewed, plus grayscale proofs. No native Word or assistive-technology pass is claimed.','', '## Finding disposition','', '| Finding | Original severity | Current result |','|---|---|---|']
for f in old:qa.append(f'| {f["id"]} {f["title"]} | {f["severity"]} | {fixes[f["id"]][0]} |')
for f in old:
 result,change=fixes[f['id']];updated.append({**f,'revision_result':result,'implemented_correction':change})
 qa+=['',f'## {f["id"]} {f["title"]}','',f'**Severity:** {f["severity"]}. **Result:** {result}.',f'**Original file:** {f["files"]}.',f'**Page/template:** {f["page"]}.',f'**Problem:** {f["problem"]}',f'**Governing source:** {f["source"]}. Exact repository paths and hashes appear below and in the source snapshot.',f'**Correction implemented:** {change}',f'**Acceptance still required:** {f["acceptance"]}',f'**Owner role:** {f["owner"]}.', '**Evidence:** `04_qa/evidence/Technical_Checks.json`, `Render_Results.json`, `PDF_Mapping_Repairs.json`, `Visual_Preservation.json`; `00_source/Reconciliation.json`.']
qa+=['','## Technical checks and evidence gates','','| Area | Result | Evidence / remaining action |','|---|---|---|',
'| DOCX editable paragraphs, real subject heading, retained styles | PASS / PENDING | Package/XML checks and successful bundled reopening; native edit/save/reopen pending |',
'| Fields, header/footer anchoring, signature and multi-page flow | PASS / PENDING | Headless fixtures including automatic 3-page flow; native Word remains pending |',
'| Word Mac / Windows / Online | PENDING | Microsoft Word access was rejected by automatic approval review: computer use for that app was not approved. No native automation workaround attempted |',
'| RTL and mixed email/URL/phone/reference punctuation | PASS visual / PENDING | Explicit RTL paragraphs and LTR token runs; fresh fixture visuals; native Arabic lead review pending |',
'| Fonts and font substitution | PASS working renderer / PENDING | Embedded Regular payloads decode; all active fonts are required families. Host Office/font acceptance remains pending; stop on fallback |',
'| PDF A4, fonts, selectable text and metadata | PASS structural | All pages A4; subset fonts embedded; author unset; primary language assigned |',
'| Arabic generic logical plain extraction | FAIL remaining | Character integrity repaired; pypdf default extraction still omits some RTL fragments and layout/pdfplumber ordering is visual. Inventory equality is not logical-reading acceptance |',
'| PDF reading order and accessibility | PENDING | Paragraph ActualText, H1, language tags, vector-logo Figure alternatives and bookmarks inspected; parent-tree/page references retained in merged PDF. AT not exercised, no PDF/UA/WCAG completion claim |',
'| Links / field replacement | PENDING completed-letter retest | Public templates contain replaceable fields, not invented contacts; fixture uses reserved example.invalid. Real link targets must be verified after replacement |',
'| Logo source, colour, geometry and whitespace | PASS working application | Official SVG/PNG hashes unchanged, supplied colours, no extra geometry, image behind body or competing decoration |',
'| Digital/Print PDF visual equality | PASS | Repairs are pixel-identical to eight DOCX exports; Digital and Print page content streams identical |',
'| Grayscale / low ink | PASS screen proof / PENDING physical | No background flood or colour-only meaning; Minimal no rule/tagline. Printer/device physical proof not performed |',
'| CMYK/Pantone/stock/profile/tolerances | REQUIRES SUPPLIER | Not invented; print PDF is RGB print candidate, not PDF/X/prepress-accepted artwork |',
'| Localization, S07 correspondence hierarchy, footer acceptance, asset/font masters, rights and AC20 | REQUIRES OWNER / PENDING | All original evidence gates remain open; no Brand Owner authorization inferred |',
'','## Required acceptance sequence','', '1. Document QA opens all eight templates in Word, replaces fields, saves/closes/reopens, updates fields, checks font substitution and re-exports explicit/automatic 1–3-page and long-field letters.', '2. Arabic Lead and Accessibility QA compare whole normalized logical Arabic text, punctuation, marks and mixed IDs using two independent extraction engines plus native copy/search and Arabic assistive technology. Close LH03 only on evidence, not glyph inventory alone.', '3. Brand Owner validates the 9 pt digital footer and proposed bilingual correspondence application; localization wording and master/font/rights gates remain separate.', '4. Supplier records prepress standard/profile, print conversion and physical legibility/proof evidence before commercial printing. AC20 remains open until authorized by the named owner.','', '## Governing repository paths','']
qa += ['- `'+s['path']+'` SHA256 `'+s['sha256']+'`' for s in sources]
qa += ['','## Package discipline','','Original v1.0 files and unrelated Part D work remain unchanged. The new v1.1 release copies are identical to the canonical working files. Original source creation/modification dates are recorded separately; revision date is 2026-10-07. All manifests and SHA256SUMS belong only to this new working revision. Re-exporting Word files does not automatically retain the controlled PDF mapping/semantic repair; every completed letter requires a new validation cycle.','']
(R/'04_qa/GEM_Letterhead_QA_Report.md').write_text('\n'.join(qa))
(R/'04_qa/Findings_Disposition.json').write_text(json.dumps(updated,indent=2,ensure_ascii=False))
log=['# GEM Letterhead Change Log','','Set v1.1 Application Revision 02 • 2026-10-07 • WORKING APPLICATION / PENDING VALIDATION','', 'New controlled derivative; v1.0 is preserved. No changes to RC2 identity, governing sources, official logo/media bytes or open evidence gates.','']
for key,(status,change) in fixes.items():log.append(f'- **{key}: {status}.** {change}')
log+=['','Additional synchronized output controls: logical PDF paragraph text and vector-logo alternatives; merged tag/parent-tree preservation; matching specification; no verified author attribution; source dates/reconciliation/asset/font register; fresh checksums.','']
(R/'03_specs/GEM_Letterhead_Change_Log.md').write_text('\n'.join(log))
readme='''# GEM Branded Letterhead Set v1.1

Application Revision 02 • 7 October 2026

**WORKING APPLICATION / PENDING VALIDATION**

Eight corrected editable Word templates, matching individual PDFs, eight-page Digital/Print sample portfolios, three-page specification, QA report, change log and source register. v1.0 is unchanged. This working package does not authorize production or owner release.

## Start here

- `05_release/`: synchronized review/distribution candidate. Eight DOCX templates plus specification DOCX; all matching PDFs and the control records.
- `01_templates/`: canonical editable template files; exact copies in release.
- `02_pdf/`: validated sample exports. These are sample correspondence, not blank fillable PDF forms.
- `03_specs/`: application specification, exact asset register and change log.
- `04_qa/`: report and evidence, including fixtures clearly marked QA ONLY. Test contacts are reserved dummy values, not company information.
- `00_source/`: governing snapshot, reconciliation, original dates and deterministic revision/export checks.

Replace every sample and field, including contact/reference placeholders in both first and continuation headers/footers. Update PAGE/NUMPAGES in Word. Allow long text to flow. Do not force a page by reducing font size. Arabic/bilingual status remains pending localization.

## Open acceptance items

LH03 remains open: mapping repairs and complete Arabic glyph inventories pass, but full generic logical extraction/native copy/search/assistive reading does not yet pass. LH08 needs owner acceptance and physical proof. Native Word access was rejected by automatic approval review because app computer use was not approved. Windows/Online Word, assistive technology, supplier/prepress, localization, rights/master/font acceptance and AC20 remain open. Do not describe this as Approved or commercially print-ready.

The Print PDF is the same RGB A4 artwork as Digital, with print-candidate metadata. No CMYK/Pantone, stock/GSM, profile, PDF/X, output intent or tolerance is invented. The document body remains real editable text. Logo artwork is unchanged official SVG with supplied PNG Office fallback; PDF logos remain vector.

## Reproduction

Source scripts reference the retained repository/workspace paths and the bundled runtime. They are evidence-bearing replay sources, not a standalone installed application. Run against the same source snapshot, installed verified fonts and retained v1.0 candidate. PDF repair is a separate controlled step; normal Word export does not include it. Every new correspondence PDF needs its own Unicode/reading-order validation.
'''
(R/'README.md').write_text(readme)
for src in list((R/'01_templates').glob('*.docx'))+list((R/'02_pdf').glob('*.pdf'))+list((R/'03_specs').glob('*'))+[R/'04_qa/GEM_Letterhead_QA_Report.md',R/'04_qa/Findings_Disposition.json']:
 if src.is_file():shutil.copy2(src,R/'05_release'/src.name)
shutil.copy2(R/'README.md',R/'05_release/README.md')
for folder in [R/'05_release',R]:
 manifest={str(p.relative_to(folder)):sha(p) for p in folder.rglob('*') if p.is_file() and p.name not in ['SHA256SUMS.txt','package_manifest.json']}
 (folder/'package_manifest.json').write_text(json.dumps({'revision':'Set v1.1 Application Revision 02','status':'WORKING APPLICATION / PENDING VALIDATION','files':manifest},indent=2))
 (folder/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(folder)}\n' for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'))
print('Controlled package assembled with QA, exact sources, reconciliation, manifests and checksums')
