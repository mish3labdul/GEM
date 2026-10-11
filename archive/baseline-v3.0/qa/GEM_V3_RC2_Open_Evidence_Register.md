# GEM™ V3.0 RC2 — Open Evidence Register

Status source: GEM V3 Final Brand Approval Register (Validation & Evidence sheet, Approval Register Y01–Y04 and AC01–AC20), as supplied on 2026-10-06. **No gate was closed by the RC2 document edits. Editing documentation is not evidence.** Status values below are the register's own; "RC2 effect" states only what the synchronized documents now say.

| ID | Evidence required (register wording, abridged) | Owner | Register status | Dependency | RC2 effect |
|---|---|---|---|---|---|
| VAL-01 | Signed architecture and commercial-scope decision; capability evidence; named commercial approval | Brand Owner + Commercial Lead | In progress | — | Tier status and capability claims stay CONDITIONAL in A 13, 60 and C 27 |
| VAL-02 | Production logo master verification: vector SVG/PDF/EPS/PNG with IDs, no-spark micro mark, stacked, white symbol | Design Custodian | Not started | VAL-04 | All logo instances still PENDING PRODUCTION MASTER (A 1, 26–29; C 7, 10) |
| VAL-03 | Trademark / distinctiveness legal review | Legal / IP Counsel | Not started | — | [TO BE VERIFIED] retained (A 78; C 75) |
| VAL-04 | Logo artwork ownership / rights evidence | Brand Owner / Legal | Not started | — | Manifest rights field [PENDING] (C App. N) |
| VAL-05 | Font licence and deployment verification; exact builds | Design Custodian / Legal | In progress | — | C 15 unchanged: PENDING VALIDATION; font embedding rule [PENDING] |
| VAL-06 | Image/model/property rights register | Art Direction / Legal | Not started | — | All imagery still REFERENCE / NOT PRODUCTION PHOTOGRAPHY |
| VAL-07 | Arabic / RTL native QA | Arabic / Localization Lead | Not started | — | Every Arabic string remains a working placeholder, PENDING LOCALIZATION APPROVAL |
| VAL-08 | Accessibility implementation QA (WCAG 2.2 AA) | Accessibility QA | In progress | VAL-07 | Alt text added to A and C decks; tagged exports produced; **not** independent QA |
| VAL-09 | Packaging pilot physical proof | Product + Procurement + Supplier QA | Not started | VAL-02 | C 28, 36 unchanged; first-proof promotion rule added (C 12–13) without values |
| VAL-10 | Packaging regulatory and claims review | Product / Regulatory / Legal | Not started | — | C 33, App. H unchanged |
| VAL-11 | Supplier production acceptance | Procurement + Supplier QA | Not started | VAL-09 | App. B gains Y06 clause, LEGAL REVIEW REQUIRED |
| VAL-12 | Wayfinding fabrication / physical legibility QA | Environmental Design + Accessibility QA | Deferred | Live property brief | C 75 reads "deferred"; S02 external signage row added |
| VAL-13 | Digital tokens and component implementation QA; Storybook (DS03) | Digital Design + Engineering | In progress | VAL-05 | No change possible (no Part B source) |
| VAL-14 | Motion / reduced-motion master QA | Motion / Digital Lead | In progress | VAL-02 | A 51 now labelled CONDITIONAL / VAL-14 |
| VAL-15 | Native presentation / PDF QA | Presentation / Document QA | Not started | VAL-05 | A and C exports open and render; tagged; **Part B PDF untagged, missing Inter 500 and Noto Sans Arabic** |
| VAL-16 | Controlled release manifest with checksums | Asset Librarian | Not started | ID/checksum scheme [REQUIRES OWNER] | Asset-ID and SHA-256 recorded as CONDITIONAL proposals only |
| VAL-17 | Guideline usability test by an independent designer/operator | Brand Governance / Independent Tester | Not started | RC2 | Retained as three tests: agency (A), developer (B), supplier/printer (C) |
| VAL-19 | Typography architecture and tracking optical QA | Design Custodian / Presentation QA | In progress | VAL-05, templates | A 34/36 now carry CONDITIONAL · VAL-19 |
| VAL-20 | Responsive, locale and living-system QA | Digital + Engineering + Localization QA | Not started | VAL-13 | — |
| VAL-21 | Cross-document release consistency | Brand Governance / Design Custodian | Not started | RC2 of all three | A and C pass the RC2 automated check; **B fails until regenerated**; formal VAL-21 not run |
| Y01 | Trademark availability reviewed | Legal / IP | Evidence Required | — | — |
| Y02 | Logo artwork ownership documented | Brand Owner / Legal | Evidence Required | — | — |
| Y03 | Font licences adequate for all uses | Design Custodian / Legal | Evidence Required | — | — |
| Y04 | Image/model/property rights documented | Art Direction / Legal | Evidence Required | — | — |
| AC07 | Master artwork approved | Brand Owner | Evidence Required | VAL-02 | — |
| AC10 | Arabic system approved or formally deferred | Brand Owner | Evidence Required | VAL-07 | — |
| AC17 | Production specifications approved | Brand Owner | Evidence Required | VAL-09 to VAL-11 | C remains WORKING EDITION / PENDING PRODUCTION VALIDATION |
| AC19 | Named role holders | Brand Owner | Approved with modification (holders TBD) | — | Twelve roles synchronized; all twelve still [REQUIRES OWNER] |
| AC20 | Brand Owner release authorization | Brand Owner | Evidence Required | all above | Pending on every cover |
| OD-TPL | Templates: PowerPoint master, document templates, social starter set, wayfinding templates (W01–W14, AB10, AB11) | Design Custodian | Open deliverable (not a register VAL ID) | VAL-02, VAL-05 | Named as OPEN DELIVERABLE on A 68, 69, 78; C 44; B patch PB-14/15 |
| OD-SRC | Part B editable source (DS03, AB21) | Digital Design Lead / Engineering Lead | **Blocking dependency for Part B RC2** | — | Patch spec issued; PDF unchanged |

Register facts carried into the documents without being treated as closed: VAL-18 is not allocated in the register (no gap to fill). Named holders for all twelve roles remain TBD. No Pantone, CMYK, tolerance, dimension, MOQ, price or lead-time value was introduced anywhere in RC2.

## Items that require human, native, legal or supplier validation (cannot be produced in-document)
- Native Arabic review of every string in A, B and C (VAL-07, M16); Arabic tagline decision (B07, M10).
- Legal: trademark (VAL-03/Y01), artwork ownership (VAL-04/Y02), font licences (VAL-05/Y03), image rights (VAL-06/Y04), the Y06 supplier clause wording (LEGAL REVIEW REQUIRED), ™ usage in running text (A 72 placeholder).
- Supplier/printer: dielines, materials, colour proofs and tolerances, minimum feature sizes, prepress standard, physical samples (C 9–13, 20–24, 28–36, 43, 47–55).
- Brand Owner: named role holders, tier naming ("Core Collection"), asset-ID and checksum convention, family-name-at-tier-level policy (PB-17), currency-format policy (PB-13), AC20.
- Independent testers: VAL-17 three-way usability test; VAL-13/VAL-20 implementation QA with a running Storybook; VAL-15 document QA with assistive technology.
