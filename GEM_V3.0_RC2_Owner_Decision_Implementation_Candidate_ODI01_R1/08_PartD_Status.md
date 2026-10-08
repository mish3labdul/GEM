# 08 · Part D Claim Implementation (Owner decision D6)

**Status: UNAPPROVED IMPLEMENTATION CANDIDATE.** Only wording that removes unsupported ambiguity was changed. "CONCEPT / NOT PRODUCTION ARTWORK" and every other concept marking is retained; no visual design changed; no production, regulatory, supplier, physical-proof, rights or material approval is implied.

## Re-audit with the ODI01 classes

Keywords scanned in shapes, tables, groups and speaker notes of all 24 slides: approved, approval, accepted, validated/validation, final, production, owner-approved, proof, master. Classes: **BRAND RULE APPROVED** (decided in the Register/Part A) · **OWNER-DESIGNATED CONCEPT** (owner-directed concept, labels, negations) · **EVIDENCE REQUIRED** (open gate stated) · **PRODUCTION STATUS** (production sequence or status) · **UNSUPPORTED CLAIM** (asserts something the package cannot show).

| Class | Original: unique / occurrences | Candidate: unique / occurrences |
|---|---|---|
| BRAND RULE APPROVED | 6 / 7 | 6 / 7 |
| OWNER-DESIGNATED CONCEPT | 31 / 127 | 31 / 127 |
| EVIDENCE REQUIRED | 12 / 14 | 12 / 14 |
| PRODUCTION STATUS | 13 / 13 | 13 / 13 |
| UNSUPPORTED CLAIM | 1 / 1 | 0 / 0 |
| **Total** | 63 / 162 | 62 / 161 |

Full lists: `18_qa_evidence/partd_claim_audit_original.csv`, `partd_claim_audit_candidate.csv`. Result: the original had **1 UNSUPPORTED CLAIM**; the candidate has **0**. The one-occurrence difference in the total is the rewritten slide-23 sentence, which no longer contains a keyword.

## Wording changed (fix unsupported claims only)

| Where | Original | Candidate | Class change | Visible? |
|---|---|---|---|---|
| Slide 15 (shape) | Bleed, safe area and tolerances come from the approved supplier dieline. | Bleed, safe area and tolerances come from the supplier dieline, once supplied and approved. | EVIDENCE REQUIRED (read as if an approved dieline exists) → EVIDENCE REQUIRED (conditional, no such dieline implied) | Yes (one line; rendered, fits) |
| Slide 23 (notes) | Supporting CSV registers contain full concept, source, asset, change and open-decision records. | A mockup register is provided with this package; other registers are not part of it. | UNSUPPORTED CLAIM → OWNER-DESIGNATED CONCEPT (states only what exists) | Notes only |

## The slide-23 registers reference (resolved without inventing anything)
Part D's package contains exactly one register: `Amenities_Portfolio_PartD_RC2/01_mockups/MOCKUP_REGISTER.csv`. No authoritative concept/source/asset/change/open-decision CSV registers exist in the current package. Earlier markdown registers (Concept_Product_Register, Asset_Source_List, Change_and_Source_Log, QA_Report, Visual_QA) belonged to the superseded v1.0 portfolio and were removed by PR #7; they remain only in git history and were **not reinstated** (they describe a different deck). The reference was therefore **corrected** to what exists. No register was created.

## Kept as is (reviewed, not unsupported)
- Slide 14 "GEM master artwork" — EVIDENCE REQUIRED label; production-master acceptance is open (AC07, VAL-02), and slide 10 already states "production master acceptance pending". Not changed (label, design-bound).
- Slides 5/6 notes "chat product direction" — OWNER-DESIGNATED CONCEPT (owner direction, not a validated rule); wording is accurate.
- Slide 23 "No item in this portfolio is an approved production asset." and every notes line "No production or commercial release is authorized by this portfolio." — retained.
- Notes on slide 23 still say "Concept Portfolio v1.0. Working edition"; the file is Part D V3.0 RC2. Version-label question stays with the owner (logged, not changed: it is not an unsupported approval claim).

## Repository prose copies (D6 wording only; D3A edits not mixed in)

| File | Original | Candidate | Candidate path |
|---|---|---|---|
| `README.md` line 9 | …concept portfolio, approved mockups, change log | …owner-designated concept mockups (concept direction only), change log | `19_candidate_documents/partd/README.ODI01-R1-CANDIDATE.md` |
| `qa/GEM_V3_RC2_Asset_Sync_Change_Log.md` | the approved Part D concept portfolio | the owner-designated Part D concept portfolio | `…/qa__GEM_V3_RC2_Asset_Sync_Change_Log.ODI01-R1-CANDIDATE.md` |
| `qa/GEM_V3_RC2_Final_Release_Notes.md` | with its approved mockups | with its owner-designated concept mockups | `…/qa__GEM_V3_RC2_Final_Release_Notes.ODI01-R1-D6-CANDIDATE.md` (its "SYSTEM READY" text is deliberately left as in the original: that is D3A candidate C4) |
| `Amenities_Portfolio_PartD_RC2/README.md` | "Designated approved by the project owner on 2026-10-06 as the mockup set to use; … not labelled Approved V3.0" | unchanged — already accurate and scoped | — |

## Still open (wording cannot fix)
All imagery is AI-generated concept imagery; image/model/property rights are unrecorded (Y04, VAL-06). Baked-in Arabic strings are PENDING LOCALIZATION APPROVAL. Physical production, supplier proof and localization gates remain open (slide 22). Supplier values stay [REQUIRES SUPPLIER] / [PENDING PHYSICAL PROOF] / [PENDING PREPRESS STANDARD]; no CMYK, Pantone, stock, GSM, Delta E, line weight, substrate or tolerance was added.

## R1
Part D was **not edited in R1**. The R1 Part D deck is a renamed, byte-identical copy of the ODI01 candidate (SHA-256 `04d325f8…`), with 0 explicit bold flags and no 500 reference, so D5 required no Part D change. Claim audit re-run: 63 unique claims / 162 occurrences on the original (1 UNSUPPORTED CLAIM) → 62 / 161 on the candidate (**0 unsupported claims**). "CONCEPT / NOT PRODUCTION ARTWORK" markings: 12 original, 12 candidate. Part D continues to state that no item is an approved production asset; nothing implies production approval, regulatory approval, supplier acceptance, physical proof or a final production master.
