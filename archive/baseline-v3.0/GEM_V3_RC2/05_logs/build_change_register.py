"""Builds qa/GEM_V3_RC2_Verified_Change_Register.{csv,md} from one row list.

Each audit finding was checked against the GEM V3 Final Brand Approval Register
(Approval Register, Validation & Evidence, Owners & Governance sheets) before
classification. Classifications:
  VERIFIED               - implement now (document-level fact, no register conflict)
  REGISTER-DEPENDENT     - register decision verified; implement as the register says
  REGISTER-CONFLICT      - audit recommendation contradicts the register; register wins
  EVIDENCE-GATED         - cannot be closed by editing; stays open
  OPTIONAL POLISH        - implemented only where trivial and deterministic
  FALSE POSITIVE         - no change required
"""
import csv, pathlib

ROWS = [
# ID, Audit ref, Doc, Page/slide, Finding, Register decisions checked, Classification, RC2 action, Priority
("CR-01","§10.1","A","3","'C · Production Standards … [PENDING] not yet issued' is stale; Part C exists (RC1).","DS01, DS04, AC17","VERIFIED — IMPLEMENT NOW","Reword tile: issued as Release Candidate 2 · WORKING EDITION / PENDING PRODUCTION VALIDATION. Notes updated.","P0"),
("CR-02","§10.2","A","78","'Production standards, Part C · PENDING' is stale.","DS04, AC17, VAL-09 to VAL-11","VERIFIED — IMPLEMENT NOW","Row becomes 'Part C RC2 issued · production evidence open · AC17, VAL-09 to VAL-11'.","P0"),
("CR-03","§10.3","A","79 (notes)","'Part C … is still to come' is stale.","DS04","VERIFIED — IMPLEMENT NOW","Notes: Part C issued as RC2.","P1"),
("CR-04","§10.4","B","3","'C. Production Standards — Referenced; not yet issued (DS04, VAL-11)' is stale.","DS04, VAL-11","VERIFIED — IMPLEMENT NOW (patch spec; no editable source)","Patch spec entry PB-03.","P0"),
("CR-05","§10.5","B","43","'Production Standards not issued' is stale.","DS04","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec entry PB-20.","P0"),
("CR-06","§10.6","B","3–4","Authority order lists Design System v2.1 above V3 content and omits Parts A and C.","RF01, RF02, DS01, Reference & Benchmark sheet source hierarchy (decisions → GEM source evidence → formal standards → benchmarks → inspiration)","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT (patch spec)","One order for A/B/C: 1 Register · 2 Part A (brand) · 3 Part B (digital) · 4 Part C (production) · 5 formal technical/legal standards where they apply · 6 V2/V2.1/V1 historical, superseded · 7 benchmarks and inspiration. Register places formal standards above benchmarks, so the audit/brief order (standards last) is corrected. Domain-ownership note added.","P0"),
("CR-07","§10.7","A","3","Authority order omits Part A itself and Part C; V2/V2.1 above Part C.","RF01, RF02, DS01","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Same seven-step order as CR-06 plus domain-ownership note.","P0"),
("CR-08","§10.8","C","2","Third authority order; no domain-ownership caveat.","RF01, RF02, DS01","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Same order as CR-06; domain-ownership note.","P0"),
("CR-09","§10.9","A / B / C","A 72, B p.5–6, C 4","Three governance role lists (8 / 12 / 9).","Owners & Governance sheet defines exactly twelve roles (= Part B list); A03–A08; AC19","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","A 72 becomes the canonical twelve-role list (register wording). C 4 rows renamed to register roles; 'Production Lead' is not a register role → [REQUIRES OWNER]. B already matches; patch spec adds cross-reference.","P1"),
("CR-10","§10.10","B / C (A)","B p.14, 40; C 41; A 38, 65","Bilingual language-lead conflict: B Arabic-first (S07) vs C project-specific.","S07 (Arabic first/right, English secondary/left by default for Saudi/GCC bilingual wayfinding; adapt only where regulation or operations require); RF08; M13","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","A 65 states the principle once (scoped to Saudi/GCC wayfinding, S07); A 38 keeps both compositions and cross-references 65; C 41: Arabic leads by default, exceptions are documented project-specific deviations (App. K). B unchanged in substance; patch spec cites A.","P0"),
("CR-11","§10.11","A","23","Secondary line specified in 'Jost light'; no light weight in the approved set.","L01, L06, L08 (two weights; exact build frozen); A 34, B p.10, C 15 define 400/500","VERIFIED — IMPLEMENT NOW","'Jost light' → 'Jost 400'.","P1"),
("CR-12","§10.12","B","2","Fixed tagline set in bold sentence case.","B04, B05, B06, AC05","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec entry PB-02.","P2"),
("CR-13","§10.13","A","53","'Square edges' contradicts Part B control radius token.","Q06 (radius tokens approved; Part B owns values)","VERIFIED — IMPLEMENT NOW","'Near-square: control radius per Part B'.","P2"),
("CR-14","§10.14","A / C","A 60; C 27","Tier status conflict (all CONDITIONAL vs two 'Approved direction').","T01, T04, E14 (Property Edition / Bespoke named), AC03 (approved with condition), VAL-01 in progress; 'Core Collection' appears nowhere in the register","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Both documents: all tiers CONDITIONAL · AC03 / VAL-01. Name 'Core Collection' marked [REQUIRES OWNER]. Chronology not used.","P1"),
("CR-15","§10.15","A / C (notes)","A 39; C 17","Circular numeral-ownership notes.","M11, M12, DS06 (Part B owns mechanics)","VERIFIED — IMPLEMENT NOW","C 17 notes: numeral mechanics follow Part B; A 39 unchanged.","P2"),
("CR-16","§10.16","B","11, 13, 64","navLabel prohibits sentence-case navigation while p.13/p.64 make it the product-UI default.","No register decision on navigation case","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-07: product UI sentence case, tracking 0; tracked capitals (navLabel) only on editorial signature surfaces.","P1"),
("CR-17","§10.17","A / B / C","A 78; B p.43–45; C 75","Three unrelated gate lists.","Validation & Evidence sheet VAL-01…VAL-21 (no VAL-18); AC07, AC10, AC17, AC20","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Register VAL IDs are the single ID set. A 78 and C 75 items carry VAL/AC IDs; C's six production gates retained and mapped. Brand / digital / production / release distinctions preserved.","P1"),
("CR-18","§10.18","B","44–45","VAL-18 missing from the gate table.","Register Validation & Evidence sheet has no VAL-18","FALSE POSITIVE / NO CHANGE REQUIRED","No renumbering. Patch spec adds one note: 'VAL-18 is not allocated in the register'.","—"),
("CR-19","§10.19","C","7","'Standalone Ink symbol' is an asset defined nowhere; Black symbol only in footnote.","H06, H08; B p.47 lists five supplied PNGs incl. GEM_Symbol_Black.png","VERIFIED — IMPLEMENT NOW","Row renamed 'Standalone Black symbol · PNG supplied'; rows aligned to the five controlled file names.","P1"),
("CR-20","§10.20","B","12","'(see Licenses)' points to nothing.","L06, AB04, C 15","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-08 → Part C slide 15.","P2"),
("CR-21","§10.21","A / B / C","A 68–69; B p.33, 40; C 44","Templates referenced as deliverables but none exist.","W01–W14, AB10, AB11 (approved deliverables), W07, W12","EVIDENCE-GATED — DO NOT PRETEND TO COMPLETE","Open deliverable recorded (OD-TPL) on A 68/69, A 78, C 44 and patch spec. No template designed.","P1"),
("CR-22","§10.22","B / C","B p.36; C 20","'Safe zones and bleeds are standardised' vs 'no universal dimensions'.","T13 = Yes (standardised)","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","B wording is register-faithful. Both clarified: roles standardised (T13); dimensions from the supplier dieline.","P2"),
("CR-23","§10.23","A / B","A 48; B p.37","Nine subjects vs six required categories.","O11–O16 (six; dining and staff/service 'if relevant')","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","A 48 note maps the nine subjects to the register-required categories; guest ritual, room details, human presence labelled supplementary. B unchanged.","P2"),
("CR-24","§10.24","A","71 (notes)","Deck claims alt text; 87 pictures have none.","V02 (mandatory), V03 (decorative marked)","VERIFIED — IMPLEMENT NOW","Alt text added to every picture in A and C; decorative full-bleed geometry flagged decorative. Claim retained only once true.","P1"),
("CR-25","§10.25","A / B / C","covers, footers","Three edition labels; two version formats; no dates or IDs.","A01, A11, X12 (vX.Y); no register RC vocabulary","VERIFIED — IMPLEMENT NOW","One convention: 'V3.0 RC2'. Edition states defined (Working edition → Release Candidate → Approved). Document-control block with ID, title, version, edition, issue date, owner, approver, status, supersedes, related. B via patch spec.","P1"),
("CR-26","§10.26","C","14","Footer drops document prefix.","—","OPTIONAL POLISH — IMPLEMENT","Footer restored.","P3"),
("CR-27","§10.27","C","3, 9, 10, 21, 23, App.","Undeclared status labels.","AA01","OPTIONAL POLISH — IMPLEMENT","Labels declared on C 3.","P3"),
("CR-28","§10.28","A","4, 57","Photography label variants undefined.","AA01, O17","OPTIONAL POLISH — IMPLEMENT","Defined on A 4.","P3"),
("CR-29","§10.29","A","34, 36","Tracking range '.04 to .12em' mismatches tokens; no status.","L09 (Display XL ≈0.12, tagline ≈0.18, eyebrow ≈0.16, small label ≈0.08, headings 0–0.02; final values need optical QA), VAL-19","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","A 34: '.08 to .12em (Part B tokens)'; A 36: CONDITIONAL · VAL-19 added.","P2"),
("CR-30","§10.30","B / C","B p.40; C 75","VAL-12 'Deferred' vs 'open'.","VAL-12 Deferred; S01; AC14","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","C 75 item reads 'deferred until a live property brief (VAL-12)'.","P3"),
("CR-31","§14 P2","A","33","Beige-on-White wording stricter than register.","K05 (prohibited for essential text), K07 (decorative allowed)","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","'NEVER for essential text, control boundaries and the logo (K05). Decorative use only (K07).'","P2"),
("CR-32","§14 P2","A","35","'LABEL · INTER 500 · CAPITALS' has no Part B token.","L02; Part B labelSmall 400 capitals / label 500 sentence case","VERIFIED — IMPLEMENT NOW","'LABEL SMALL · INTER 400 · CAPITALS'.","P2"),
("CR-33","§14 P1","B","PDF","PDF embeds only Jost Regular, Inter Regular, DejaVu Sans; untagged.","L06, V13, VAL-15, VAL-19","EVIDENCE-GATED (no editable source) — record status","Patch spec export requirements (Inter 500, Noto Sans Arabic embedded, tagged). Embedded-font status recorded in QA. Not closable here.","P1"),
("CR-34","§14 P1","A / C (B)","A 75; C 56, App. N; B p.47","File naming, asset ID and checksum.","X12 = GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext; X15 checksums (no algorithm); H21 asset ID in naming (no format)","REGISTER-CONFLICT on naming — register wins; ID/checksum as CONDITIONAL proposals","A 75 and C 56/App. N adopt X12 exactly (date field required; 'no dates' sentence removed). Asset ID GEM-[CATEGORY]-[NNN] and SHA-256 recorded as CONDITIONAL · [REQUIRES OWNER] proposals, not standards. Supplied PNGs to be renamed at first manifest (VAL-16).","P1"),
("CR-35","§14 P1","C","App. B","Supplier acknowledgement lacks artwork-use restriction.","Y06 (Yes, contractually where appropriate)","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Clause added with LEGAL REVIEW REQUIRED.","P1"),
("CR-36","§14 P1","C","12–13","No visual target exists for step 4 of proofing.","J16, T18, U13","VERIFIED — IMPLEMENT NOW","Rule: the first formally approved physical proof becomes the controlled process-specific reference and is logged as a golden sample (App. M). No values created.","P1"),
("CR-37","§14 P1","A / B / C","Arabic strings","Native Arabic QA not run.","VAL-07 Not started; M16; AC10","EVIDENCE-GATED — DO NOT PRETEND TO COMPLETE","Remains open.","P1"),
("CR-38","§14 P1","A / B / C","—","Independent usability test not run.","VAL-17 Not started; RF05","EVIDENCE-GATED — DO NOT PRETEND TO COMPLETE","Remains open: agency test (A), developer test (B), supplier/printer test (C).","P1"),
("CR-39","§14 P2","B","65 (ProductCard)","Level-2 line 'BATH AND BODY' is a family, not a tier.","T02 (bath/body = pilot product family), T04, T05","REGISTER-DEPENDENT — FLAG","Patch spec PB-14: whether a family name may occupy the collection/tier level is [REQUIRES OWNER · Product / Amenities Lead].","P2"),
("CR-40","§14 P2","A / C (B)","A 61; C 29; B p.35","Audit asked B to adopt seven hierarchy levels.","T05 standard hierarchy = six levels: GEM → collection/tier → product/function → quantity/size → instructions/required market information → SKU/artwork version","REGISTER-CONFLICT — audit recommendation rejected; register wins","B p.35 is correct. A 61 and C 29 re-set to the six T05 levels (product and function merged).","P2"),
("CR-41","§14 P2","B","9, 12, 23, 36","Folder names used as cross-references.","—","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-09 page references.","P2"),
("CR-42","§14 P2","C","App. D, E, F, L","Missing form fields.","T11, T12–T20, Y05, C 23 (grain direction), C 30 (primary/secondary pack)","VERIFIED — IMPLEMENT NOW","App. D: Proof ID, Samples. App. E: Grain direction. App. F: Market(s), Language / bilingual status, Primary pack, Secondary pack. App. L: Raised by, Date raised / closed.","P2"),
("CR-43","§14 P2","C / A","C 39; A 65","External signage deferral absent.","S02 Deferred","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","C 39 row 'External / building identification · Deferred (S02)'; A 65 note.","P2"),
("CR-44","§14 P2","B","28","No currency format rule.","DS06 (locale-aware); no currency decision","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-16: currency row [REQUIRES OWNER · Arabic / Localization Lead].","P2"),
("CR-45","§14 P2","A","6, 41, 43, 46","Ring crosses text; rule wording contradictory.","N06–N08 (no text-overlap decision); A's own 'never crowd the type'","VERIFIED (internal rule) — IMPLEMENT NOW","Rule reworded on 41/43: forms sit in the field, never intersect headlines or running text. Rings on 6, 41, 46 moved clear of text boxes; duplicate ring stroke on 41 removed.","P2"),
("CR-46","§14 P2","B","41","Token JSON shows empty groups without saying it is an excerpt.","Q01–Q09","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-18.","P2"),
("CR-47","§14 P2","B","33","No end-to-end booking flow.","Q11–Q15","OPTIONAL — NOT IMPLEMENTED","New design content is outside this revision's scope; recorded for the next edition.","P2"),
("CR-48","§14 P2","B","8, 23, 50","Alert has no warning variant while a 'warning' glyph exists.","Q10","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-19 note.","P2"),
("CR-49","§14 P3","A","15","Default grey table style.","—","OPTIONAL POLISH — NOT IMPLEMENTED","Visual-only; left for the Design Custodian to avoid layout drift.","P3"),
("CR-50","§14 P3","B","27, 29, 34, 46, 49, 51","Near-empty pages.","—","OPTIONAL POLISH (patch spec)","Reflow at regeneration.","P3"),
("CR-51","§14 P3","A","50, 51","Missing CONDITIONAL labels.","W07, VAL-14","OPTIONAL POLISH — IMPLEMENT","Labels added.","P3"),
("CR-52","§14 P3","C","1","Tagline absent from cover.","B04","OPTIONAL POLISH — NOT IMPLEMENTED","Cover composition unchanged; tagline remains on closing slide.","P3"),
("CR-53","§14 P3","A","45","Glyph description differs from register wording.","N15","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Wording aligned to N15.","P3"),
("CR-54","§14 P3","A","13","Buyer-benefit sentence.","D12","OPTIONAL — NOT IMPLEMENTED","Strategy content unchanged (locked).","P3"),
("CR-55","§14 P3","C","all","Section numbers diverge from page numbers.","—","OPTIONAL POLISH — NOT IMPLEMENTED","Would renumber every title; deferred.","P3"),
("CR-56","§14 P3","A / B / C","footers","Footer grammar differs.","—","OPTIONAL POLISH — IMPLEMENT (A, C); patch spec (B)","Footers carry 'V3.0 RC2'.","P3"),
("CR-57","§12 Legal","A","72","No ™ usage rule for running text.","B02 (™ part of artwork), Y07","VERIFIED — IMPLEMENT NOW (placeholder only)","Line added: ™ in running text and packs [REQUIRES OWNER · Legal / IP Counsel]. No rule invented.","P2"),
("CR-58","§12 Arabic","A","24","Arabic tagline decision open.","B07, M10","EVIDENCE-GATED","Remains PENDING LOCALIZATION APPROVAL.","P1"),
("CR-59","§12 Arabic","B","28","Hijri and numeral policy sign-off.","M11, DS06","EVIDENCE-GATED","Remains CONDITIONAL / [REQUIRES OWNER].","P1"),
("CR-60","§6 B","B","37","Photography direction duplicated from A.","O01–O20","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-17: cross-reference A 47–50; keep alt text, rights, ratios.","P2"),
("CR-61","§6 B","B","5–6","Governance list should cite the canonical list.","Owners & Governance sheet","VERIFIED — IMPLEMENT NOW (patch spec)","Patch spec PB-05.","P1"),
("CR-62","§7 C","C","3, 76","'Release Candidate' undefined.","A11","VERIFIED — IMPLEMENT NOW","Edition states defined on C 3 (and A 4).","P1"),
("CR-63","§7 C","C","4","'Production Lead' and split 'Procurement' / 'Supplier QA' are not register roles.","Owners & Governance sheet; A06","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Rows use register names; Production Lead duties marked [REQUIRES OWNER] (proposed delegate of Procurement / Supplier QA).","P1"),
("CR-64","§12 Governance","A / B / C","new slides","No document control or change log.","A11, Z24, AB19, AB20","VERIFIED — IMPLEMENT NOW","New 'Document control & change log' slide in A and C; patch spec for B.","P1"),
("CR-65","§13","A / B / C","—","All evidence gates.","VAL-01…VAL-21, Y01–Y04, AC07, AC10, AC17, AC20","EVIDENCE-GATED — DO NOT PRETEND TO COMPLETE","Recorded in Open Evidence Register; none closed.","—"),
("CR-66","§5 Arabic","A","38","Bilingual composition shows two orders without a default.","S07 scope is bilingual wayfinding; no general packaging/UI order decided","REGISTER-DEPENDENT — VERIFIED AND IMPLEMENT","Both compositions kept; caption cross-references the S07 wayfinding default on 65. No general default invented.","P1"),
("CR-67","§12 Documentation","C","App. N","Appendix N is a field list, not a form.","AB17, X15","OPTIONAL POLISH — NOT IMPLEMENTED (slide); recorded","Spreadsheet template is an open deliverable under VAL-16.","P1"),
("CR-68","Brief §B","B","source","No editable Part B source in the workspace.","DS03, AB21","BLOCKING DEPENDENCY — RECORDED","Part B PDF left untouched; corrections delivered as qa/PartB_RC2_Exact_Patch_Spec.md.","P0"),
("CR-69","Brief §C","A / C","1, cover","Document ID convention.","A11","VERIFIED — IMPLEMENT NOW","GEM-BG-V3.0-RC2 (A), GEM-DDS-V3.0-RC2 (B, patch spec), GEM-PS-V3.0-RC2 (C).","P1"),
]

root = pathlib.Path(__file__).resolve().parents[2]
qa = root / "qa"; qa.mkdir(exist_ok=True)
hdr = ["ID","Audit ref","Document","Page / slide","Finding","Register decisions checked","Classification","RC2 action","Priority"]
with open(qa / "GEM_V3_RC2_Verified_Change_Register.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(ROWS)

counts = {}
for r in ROWS:
    k = r[6].split(" —")[0].split(" (")[0].strip()
    counts[k] = counts.get(k, 0) + 1

md = ["# GEM™ V3.0 RC2 — Verified Change Register", "",
      "Source of authority: GEM V3 Final Brand Approval Register (Prefilled, SHA-256 ccce4613…e7ab3). The audit report is a review document; every row below was checked against the register before classification. Where the audit and register disagree, the register wins.", "",
      "| Classification | Rows |", "|---|---|"]
for k, v in sorted(counts.items()): md.append(f"| {k} | {v} |")
md += ["", "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
for r in ROWS: md.append("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
md += ["", "Register-conflict decisions applied (register wins): CR-34 file naming (X12), CR-40 packaging hierarchy (T05 six levels). Audit false positive: CR-18 (VAL-18 is not allocated in the register).", ""]
(qa / "GEM_V3_RC2_Verified_Change_Register.md").write_text("\n".join(md), encoding="utf-8")
print(len(ROWS), "rows;", counts)
