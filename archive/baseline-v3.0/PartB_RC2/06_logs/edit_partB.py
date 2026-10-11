"""Part B RC2 edits on 01_source/B-RC2.pptx. Usage: edit_partB.py P0|P1|P2|NEW|FOOT
Slide numbering AFTER the two host-slide insertions: 26 = flow test (copy of 25), 34 = document control (copy of 33/old 32);
old 26..33 are now 27..35."""
import sys, re, pathlib
sys.path.insert(0, "/home/user/GEM/GEM_V3_RC2/05_logs")
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx_helpers import *

F = pathlib.Path(__file__).resolve().parents[1] / "01_source" / "B-RC2.pptx"
prs = Presentation(F); S = lambda n: prs.slides[n - 1]
INK = RGBColor(0x12, 0x17, 0x1D)
log = []
def L(n, w): log.append((n, w))
def table_of(s, i=0): return [sh for sh in s.shapes if sh.shape_type == 19][i]
def cell(gf, r, c): return gf.table.cell(r, c)
def add_row(gf, texts):
    import copy
    from pptx.oxml.ns import qn
    tbl = gf.table._tbl; trs = tbl.findall(qn("a:tr")); new = copy.deepcopy(trs[-1]); tbl.append(new)
    row = gf.table.rows[len(gf.table.rows) - 1]
    for c, t in zip(row.cells, texts): set_cell(c, t)
    gf.height = gf.height + int(trs[-1].get("h"))

phase = sys.argv[1]

if phase == "P0":
    s = S(1)
    t = find(s, "WORKING SPECIFICATION"); defit(t)
    set_text(t, "V3.0 RC2 · WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING) · GEM-DDS-V3.0-RC2 · ISSUED 2026-10-06")
    set_notes(s, "Editable source of the GEM Digital Design System V3.0, Release Candidate 2 (RC2), synchronized with Part A RC2, Part C RC2 and the V3 Final Brand Approval Register (466 decisions). Logo artwork is not reproduced here: production masters are PENDING (VAL-02). Document control and change log: slide 34.")
    L(1, "RC2 status line, document ID, date")
    s = S(4); gf = table_of(s)
    set_cell(cell(gf, 3, 2), "Issued as Release Candidate 2 · WORKING EDITION / PENDING PRODUCTION VALIDATION (DS04; AC17, VAL-09 to VAL-11 open)")
    set_cell(cell(gf, 3, 0), "C. Production Standards V3.0 RC2")
    set_cell(cell(gf, 1, 0), "A. Brand Guidelines V3.0 RC2")
    set_cell(cell(gf, 1, 2), "Referenced; brand and identity rules govern (DS02)")
    set_cell(cell(gf, 2, 0), "B. Digital Design System V3.0 RC2")
    t = find(s, "The approval register (final"); defit(t)
    set_text(t, "1 · V3 Final Brand Approval Register (Evidence Required stays conditional; Deferred stays deferred)\n2 · Part A, Brand Guidelines: brand strategy, identity and expression\n3 · Part B, this system: digital implementation\n4 · Part C, Production Standards: physical production\n5 · Formal technical and legal standards (WCAG 2.2 AA and others) where they apply\n6 · Design System v2.1, Brand Guidelines V2/2.1 and V1: historical, superseded\n7 · External benchmarks and inspiration only (RF01–RF03)")
    move(t, height=1.95)
    t = find(s, "Where sources conflict"); defit(t)
    set_text(t, "Where sources conflict, the register wins. Domain ownership: where Parts A, B and C cover different implementation domains, the owning document governs that domain unless the register overrides it. Decision IDs (L09, Q17, M05…) are cited so every rule traces back. Futura PT, Montserrat, Aeonik, Satoshi and Whyte are reference or legacy only.")
    move(t, height=1.15)
    t = find(s, "Read order:"); defit(t)
    set_text(t, "Read order: slides 2–5 overview and governance → 6–21 foundations, typography, Arabic, layout, accessibility, motion, glyphs, writing, localization → 22–24 components → 25–29 patterns → 30 engineering → 31–35 QA, release, document control, assets.")
    move(t, top=5.52, height=0.6)
    set_notes(s, "Authority order shared verbatim with Part A slide 3 and Part C slide 2 (RF01, RF02, DS01). Part C exists as Release Candidate 2; it is a working edition pending production validation (AC17), not a production-approved standard.")
    L(4, "stale Part C row; seven-step authority order; domain-ownership note; read order by slide")
    gf = table_of(S(12), 1)
    set_cell(cell(gf, 8, 0), "Bilingual default: Arabic leads for approved Saudi/GCC contexts (Arabic first and right, English secondary and left); exceptions are documented deviations")
    gf.height = gf.height + Inches(0.3)
    t = find(S(12), "Noto Sans Arabic, tracking 0"); move(t, top=5.62)
    t = find(S(13), "Implementation. Logical"); defit(t)
    set_text(t, "Implementation. Part B owns the mechanics of the Arabic-first default (S07, Part A slide 65): dir=\"rtl\", logical properties only (margin-inline-start, text-align: start, inset-inline), bidi isolation. No left or right in component CSS. Fabrication follows Part C slide 41.")
    move(t, height=1.3)
    gf = table_of(S(29))
    set_cell(cell(gf, 2, 1), "Arabic first and right, English secondary and left, equal information, by default for Saudi/GCC (S07, Part A 65). Exceptions only where regulation or operations require, as a documented project-specific deviation (Part C 41, Appendix K)")
    gf.height = gf.height + Inches(0.3)
    t = find(S(29), "Viewing distances"); move(t, top=4.55)
    L(12, "S07 default wording"); L(13, "mechanics ownership sentence"); L(29, "S07 default + exception rule")
    t = find(S(30), "Storybook-ready"); replace_in_runs(t, "Versioning: semantic (V3.0.0).", "Versioning: semantic 3.0.0-rc.2 (document edition V3.0 RC2).")
    set_text(find(S(33), "3.0.0 draft"), "3.0.0-rc.2 · V3.0 RC2 (this edition)")
    L(30, "version 3.0.0-rc.2"); L(33, "change-log heading RC2")

elif phase == "P1":
    s = S(2); t = find(s, "Also required:"); defit(t)
    set_text(t, "Also required: CONCEPT / NOT PRODUCTION ARTWORK · PENDING PRODUCTION MASTER · PENDING LOCALIZATION APPROVAL · PROJECT-SPECIFIC / REQUIRES SITE VALIDATION. Edition states, shared with Parts A and C: WORKING EDITION → RELEASE CANDIDATE (RC) → APPROVED. This edition is V3.0 RC2; it becomes APPROVED only by Brand Owner authorization (AC20).")
    move(t, height=1.2)
    L(2, "edition states")
    s = S(5)
    set_text(find(s, "Owners (all role holders TBD)"), "Owners (all role holders TBD, AC19) and change control")
    g0, g1 = table_of(s, 0), table_of(s, 1)
    ren = {"Product / Amenities": "Product / Amenities Lead", "Procurement / QA": "Procurement / Supplier QA", "Localization Lead": "Arabic / Localization Lead", "Document QA": "Presentation / Document QA", "Asset Librarian": "Asset Librarian / Governance PM"}
    for gf in (g0, g1):
        for r in range(1, len(gf.table.rows)):
            n = cell(gf, r, 0).text.strip()
            if n in ren: set_cell(cell(gf, r, 0), ren[n])
    t = find(s, "Change control."); defit(t)
    set_text(t, "Canonical role list: the register's Owners & Governance sheet, stated in Part A slide 72; this table lists digital responsibilities only. Change control. Any new token, component or variant states its purpose, register decision, accessibility check and RTL check, signed off by the Design Custodian and Digital Design Lead.")
    move(t, height=1.2)
    t = find(s, "Accessibility exceptions"); move(t, height=1.2)
    L(5, "register role names; canonical-list citation; AC19")
    s = S(11); t = find(s, "Prohibited: tracking"); defit(t)
    set_text(t, "Prohibited: tracking on lowercase running text, on Arabic, below 12px, or to fit a word on a line. Navigation: product UI navigation is sentence case at tracking 0 (body or label tokens); navLabel tracked capitals are used only on editorial signature surfaces.")
    move(t, height=1.0)
    L(11, "one navigation rule")
    s = S(9); t = find(s, "Futura PT, Montserrat"); defit(t)
    set_text(t, "Futura PT, Montserrat, Aeonik, Satoshi and Whyte are reference or legacy only (L03, L07). No decorative serif or script (L15). The wordmark is never recreated in type (L16). Maximum two weights per composition (L08). Weights in use: Jost 400 (500 for controlled labels), Inter 400 and 500, Noto Sans Arabic 400 and 500. Fonts are referenced under SIL OFL 1.1; exact builds, versions and deployment rights are PENDING VALIDATION (VAL-05, Y03). Licence, build and deployment control: Part C slide 15 (Font control).")
    move(t, height=1.1)
    L(9, "weights in use; licence cross-reference to Part C 15")
    s = S(27); t = find(s, "A descriptive stream"); defit(t)
    set_text(t, "A descriptive stream under the master brand, not a sub-brand: no new symbol, colour system or stream logo. Hierarchy (T04, T05), six levels: GEM → collection or tier → product and function → quantity → instructions → SKU and artwork version; Part A slide 61 and Part C slide 29 state the same. Pilot family (T02): Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash. Whether a family name such as \"Bath and body\" may occupy the collection/tier level is [REQUIRES OWNER · Product / Amenities Lead]; tiers are CONDITIONAL (AC03, VAL-01).")
    move(t, height=1.05)
    table_of(s).top = Inches(2.85)
    set_notes(s, "Release controls before mass production: supplier dieline per SKU (T12); safe-zone and bleed roles are standardised (T13) while their values are supplier- and dieline-specific and owned by Part C (slide 20); material, finish, print process, colour tolerances (T14–T19), physical proof (T17), signed reference sample archived (U13), supplier acceptance (T20), brand sign-off (T21). A concept mockup is never production approval (T23). Surfaces: uncoated warm neutral paper, deep INK board, selective deboss or blind emboss, soft-touch selectively, precision die-cut; foil only if approved; no chrome, holographic or high-gloss; gold is not a GEM colour (U01–U10).")
    L(27, "six-level cross-reference; family-name policy placeholder; T13 note")
    gf = table_of(S(31))
    set_cell(cell(gf, 7, 2), "Raster logos only; no supplier data; Part C issued as RC2, physical evidence open (VAL-02, VAL-09 to VAL-11, AC17)")
    L(31, "stale Production row")
    s = S(32); t = find(s, "GEM Digital Design System V3.0 · working specification · 31"); defit(t)
    set_text(t, "GEM Digital Design System V3.0 · working specification · 32 · Owners per gate are listed in the speaker notes. VAL-18 is not allocated in the register; the sequence is complete as shown.")
    L(32, "VAL-18 note")
    gf = table_of(S(25))
    set_cell(cell(gf, 8, 1), "PowerPoint master: OPEN DELIVERABLE (W01, AB10), not yet produced · native QA PENDING (VAL-15)")
    set_cell(cell(gf, 7, 1), "Type scale, Button, Link · Arial or system-ui fallback · email template: OPEN DELIVERABLE (R13, AB11)")
    L(25, "template rows → OPEN DELIVERABLE")
    s = S(35); t = find(s, "Required, not supplied."); defit(t)
    set_text(t, "Required, not supplied. SVG/PDF/EPS/PNG masters, micro mark, stacked lockup, white symbol, embroidery and deboss masters, favicon and app icons (H16–H21). Controlled names follow register convention X12 (GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext) at first manifest (VAL-16); the supplied files are renamed, never redrawn.")
    move(t, height=1.0)
    L(35, "X12 note")
    # document control slide 34 (copy of checklist)
    s = S(34)
    set_text(find(s, "Release checklist and change log"), "Document control and change log")
    set_text(find(s, "08 · QA AND RELEASE"), "08 · DOCUMENT CONTROL")
    t = find(s, "All role holders named."); defit(t)
    set_text(t, "Document ID · GEM-DDS-V3.0-RC2\nTitle · GEM™ Digital Design System V3.0 — Part B\nVersion · V3.0 RC2 (Release Candidate 2) · semantic 3.0.0-rc.2\nEdition state · WORKING SPECIFICATION · NOT RELEASED\nIssue date · 2026-10-06\nOwner · Digital Design Lead [REQUIRES OWNER]\nApprover · Brand Owner · AC20 PENDING\nRelease status · RC2 synchronized with Part A and Part C RC2 · evidence gates open\nSupersedes · V3.0 working specification, 3.0.0-draft (undated)\nRelated · GEM-BG-V3.0-RC2 (Part A) · GEM-PS-V3.0-RC2 (Part C) · V3 Approval Register")
    move(t, height=2.9)
    set_text(find(s, "3.0.0 draft"), "Change log")
    t = find(s, "Added: tracking scale"); defit(t)
    set_text(t, "3.0.0-rc.2 · 2026-10-06. RC2 synchronization with Parts A and C and the register: version and document ID; authority order and domain ownership; stale Part C references; register role names; one navigation rule; S07 bilingual default with exception rule; six-level hierarchy cross-reference and family-name policy placeholder; T13 wording; template gates; VAL-18 note; X12 naming; currency placeholder; photography cross-reference; token excerpt label; warning-glyph note; booking-flow implementation test; document control. No token, component or rule value changed.")
    move(t, height=1.8)
    t = find(s, "Changed: Futura PT"); defit(t)
    set_text(t, "3.0.0-draft. Updated from v2.1 under the V3 register: tracking scale, Arabic hierarchy, semantic and layout tokens, 27 glyphs, 26 components, locale DatePicker, feedback hierarchy, Amenities & Packaging, QA audit; Futura PT and Montserrat to reference; 0.3–0.8em tracking retired.")
    move(t, top=4.25, height=0.75)
    set_text(find(s, "2.1: initial system"), "2.1: initial system from brand guidelines and digital tokens.")
    move(find(s, "2.1: initial system"), top=5.05)
    set_notes(s, "Document control per register A11 and the change-log requirement (Z24, AB19), in the same form as Part A slide 79 and Part C slide 77. Owner and approver names are recorded by the Brand Owner before AC20.")
    L(34, "new document-control and change-log slide")

elif phase == "P2":
    gf = table_of(S(21)); add_row(gf, ["currency-format", "[REQUIRES OWNER]", "Arabic / Localization Lead: SAR symbol or code position for ar-SA and en; no price is invented"])
    L(21, "currency-format placeholder row")
    s = S(28)
    set_text(find(s, "Direction · Approved"), "Direction · owned by Part A")
    t = find(s, "Editorial, architectural, restrained (O01)."); defit(t)
    set_text(t, "Photography direction is governed by Part A slides 47–50 (O01–O10). This system keeps only the digital rules: crops and ratio tokens, alt text, rights metadata and the avoid list.")
    t = find(s, "Required categories:"); defit(t)
    set_text(t, "Required categories per the register (O11–O16) and Part A slide 48: architecture, material detail, arrival and threshold, amenities and product; dining and service where relevant. Every production image carries rights metadata (O18, VAL-06); AI or rendered mockups are never presented as photography (O17). Ratio tokens: 3:2 rooms, 4:5 products, 16:9 hero (CONDITIONAL).")
    move(t, height=0.75)
    L(28, "photography direction → cross-reference")
    s = S(30); t = find(s, "foundation.color"); defit(t)
    set_text(t, "EXCERPT — full set: gem-tokens.v3.0-rc2.json / .css\nfoundation.color\nink #12171D · beige #BCACA7\nblack #020202 · white #FFFFFF\nsemantic\nsurface · text · border\naction · focus · feedback\ntype · space · radius · size\nmotion · layout · locale")
    t = find(s, "Source: tokens.json"); defit(t)
    set_text(t, "Source: tokens.json (living source, DS03 open); portable gem-tokens.v3.0-rc2.json and .css (--gem- prefix), derived from this specification with status per token. Aliases use {path}.\nSemantic HTML first; ARIA only where no native element exists.\nCSS custom properties for every token; logical properties for direction.\nEvery string is a prop; Intl for dates and numbers.\n:focus-visible with focus tokens; modal traps and returns focus.")
    L(30, "token block labelled EXCERPT; package reference")
    s = S(18); t = find(s, "RTL. Only previous"); defit(t)
    set_text(t, "RTL. Only previous and next mirror. SVGs are working geometry, not supplier artwork (DS05). The warning glyph is PENDING VALIDATION and is used only inside Field error and Alert text until functional colour is decided (Q10); Alert has no warning variant.")
    move(t, height=1.1)
    for n in ["Text 4", "Text 5"]: move(by_name(s, n), height=1.1)
    L(18, "warning-glyph clarification")
    s = S(3); t = find(s, "Tagline. HOSPITALITY"); defit(t)
    set_text(t, "Tagline. HOSPITALITY, IN PERFECT PROPORTION — fixed; set only with the tagline token (Jost 400, capitals, 0.18em); not translated without brand approval (M10). Secondary line: Every arrival, precisely composed. (Jost 400, sentence case).")
    move(t, height=0.95)
    L(3, "tagline treatment rule")

elif phase == "FLOW":
    s = S(26)
    for sh in list(s.shapes):
        if sh.shape_type == 19 or sh.name in ("Text 3", "Text 4"): remove(sh)
    set_text(find(s, "07 · PATTERNS"), "07 · PATTERNS · BOOKING FLOW · CONCEPT / IMPLEMENTATION TEST")
    set_text(find(s, "Hospitality patterns"), "Booking flow: five steps, one primary action each")
    steps = [("1 · Search / availability", "Field (property), DatePicker trigger, QuantityStepper summary, Button \"Check availability\" (primary)"),
             ("2 · Dates", "DatePicker range · locale week start · unavailable dates struck + named · Button \"Keep dates\""),
             ("3 · Guests", "QuantityStepper adults / children · Select rooms · error: \"Choose at least one guest.\" above the control"),
             ("4 · Room", "RoomCard list (verified facts only) · Tabs by view · aria-pressed on the selected card · Button \"Continue\""),
             ("5 · Confirmation", "Alert CONFIRMED · Booking confirmed. · Reference: [booking ID] · SpecificationTable summary · Link \"Review booking\"")]
    x0, y0, w, h, gap = 0.89, 1.95, 2.18, 1.9, 0.16
    for i, (title, body) in enumerate(steps):
        x = x0 + i * (w + gap)
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y0), Inches(w), Inches(h))
        box.fill.background(); box.line.color.rgb = INK; box.line.width = Pt(0.75); box.name = f"Flow box {i+1}"
        box.shadow.inherit = False
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.12); tf.margin_top = Inches(0.1)
        p = tf.paragraphs[0]; r = p.add_run(); r.text = title; r.font.name = "Jost"; r.font.size = Pt(13); r.font.color.rgb = INK
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = body; r2.font.name = "Inter"; r2.font.size = Pt(9.5); r2.font.color.rgb = INK
        if i < 4:
            arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + w + 0.02), Inches(y0 + h / 2 - 0.06), Inches(0.12), Inches(0.12))
            arr.fill.solid(); arr.fill.fore_color.rgb = INK; arr.line.fill.background(); arr.name = f"Flow arrow {i+1}"
    notes = [("Primary action", "One primary Button per step, full width at Compact; secondary actions are Links. Focus moves to the step heading on step change, to the first invalid field on error."),
             ("Errors and validation", "State label ERROR, title, actionable sentence (feedback hierarchy). Inline field errors above the control with aria-invalid and aria-describedby; never colour alone."),
             ("RTL / Arabic", "dir=\"rtl\" on the root: step order and arrows read right to left; DatePicker arrows swap; codes and the booking ID stay LTR in <bdi>. Arabic strings are working placeholders, PENDING LOCALIZATION APPROVAL."),
             ("Responsive", "Compact: one column, stacked actions, DatePicker as full-width sheet. Desktop: two-up for dates and guests (Tablet) and a room list at 12 columns; max 1080 / 1280."),
             ("Status", "CONCEPT / IMPLEMENTATION TEST. Not a live product. Step logic, focus, error and RTL behaviour are specified here and in 02_build/flow; runtime behaviour is NOT TESTED until the component bundle exists (VAL-13, VAL-20).")]
    nx = 0.89; nw = 2.18
    for i, (h1, body) in enumerate(notes):
        x = nx + i * (nw + gap)
        tb = s.shapes.add_textbox(Inches(x), Inches(4.05), Inches(nw), Inches(2.4)); tb.name = f"Flow note {i+1}"
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = Inches(0)
        p = tf.paragraphs[0]; r = p.add_run(); r.text = h1; r.font.name = "Inter"; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = INK
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = body; r2.font.name = "Inter"; r2.font.size = Pt(9.5); r2.font.color.rgb = INK
    set_notes(s, "Reference flow assembled from existing components only (Field, DatePicker, QuantityStepper, Select, RoomCard, Tabs, Button, Link, Alert, SpecificationTable). Purpose: test step order, primary-action logic, errors, validation, focus, responsive behaviour, Arabic/RTL, DatePicker and selected states. Labelled CONCEPT / IMPLEMENTATION TEST; it is not a live product and nothing here is evidence for VAL-13 or VAL-20. Checklist: PartB_RC2/02_build/flow/booking-flow-test.md.")
    L(26, "booking-flow implementation test slide")

elif phase == "FOOT":
    n = 0
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and "working specification" in sh.text_frame.text:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        new = re.sub(r"GEM(™)? Digital Design System V3\.0( RC2)? · working specification · \d+", f"GEM™ Digital Design System V3.0 RC2 · working specification · {i}", r.text)
                        if new != r.text: r.text = new; n += 1
    L(0, f"footers renumbered and versioned on {n} runs")

prs.save(F)
for n, w in log: print(f"B {n:>2}: {w}")
