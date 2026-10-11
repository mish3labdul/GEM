# 09 · Source register supplement — 2026-10-10 (audit GEM-09)

Supplements `01_Source_Register.md`, which is kept unchanged as the session-1 record. Where they differ, this supplement governs.

## Correction to record 01
Record 01 says the V3 Final Brand Approval Register was "not supplied". That is wrong as a blanket statement. The register is present and adopted:

| Layer | File | SHA-256 / status | What it establishes |
|---|---|---|---|
| S1 Register workbook | `GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx` | `ccce46135a4f2244dbff21cef94a6160e9d2b6fd96a63647c1e5ea6b662e7ab3` (verified this session on the owner's Mac; matches S2) | 466 rows; 456 adopted decisions (384 Approved + 72 Approved with modification); 8 Evidence Required (Y01–Y04, AC07, AC10, AC17, AC20); 2 Deferred (R17, S02). Entry basis "ChatGPT prefill · 06 Oct 2026". |
| S2 Adoption record | `GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/register_adoption/…ADOPTION_RECORD_2026-10-08.md` | Owner decision D1, 2026-10-08 | The register is the **adopted working decision baseline** and first in authority order. Adoption does not close any VAL gate, does not convert prefill into evidence, and does not authorize release. 76 adopted rows still carry "Evidence Required = Yes". |
| Overlays | OD01 owner decisions; FD01 formal deferrals; FA01 final owner decisions and D8 policy | read for website-relevant rows | FA01 supersedes earlier AC20 and role-holder statuses: Brand Owner holder Mashal; AC20 authorized as a limited baseline with formal deferrals; VAL-01, AC07/VAL-02 deferred; VAL-03–06 accepted as owner risk, not verified. |
| HR01 | `GEM_V3.0_RC2_HR01_Human_Review_Queue_Closure/01_HR01_Executive_Summary.md`, `05_HR01_Accessibility_Content_Register.csv` | read | Human review **completed for its defined document scope**: 44 Arabic items reviewed by Mashal (linguistic decisions, distinct from AR01 technical validation); 144 accessibility-content items including 23 Part D product alt texts; macOS VoiceOver SR-01–10 and SR-13 observed. SR-11 (PDF) and SR-12 (Windows) deferred. **Gates closed by HR01: 0.** HR01 does not approve an Arabic website. |
| RP01 | release promotion | current release | Promoted artifacts used by the website (decks, tokens; kit referenced in place). |

Correct statement: **there is an adopted working register plus later owner overlays; there is no newly signed final register.** No final register has been invented and no deferred gate is recorded as closed.

## Carried forward from the independent audit
- **B01:** Part B slide 2 still says the edition is "V3.0 RC2" and that it "becomes APPROVED only by Brand Owner authorization (AC20)", which contradicts the promoted V3.0 cover labels. Confirmed in the session-1 text extract (Part B S2). Disposition: open document defect in Part B; the website does not repeat the slide-2 wording and does not present the component index as implemented software.
- **B02:** Arabic and bilingual letterhead templates exist in the parent release package under `restricted_internal_only/` and stay governed by FA01 D8 / RP01. None is in `site/`, none is linked, and website owner decisions WD-04 and WD-06 do not extend to them. The audit's note on prior GitHub archive distribution was not re-verified here.

## Arabic, as distinct layers
- Technical Arabic validation (AR01): document scope, historical to the website.
- Human linguistic review (HR01, Mashal): document scope; approves wording in the decks and letterheads.
- External-issue tests (D8: Windows Word, Word Online, Acrobat, NVDA/JAWS): still deferred.
- Website: no Arabic edition exists. The Part D images shown contain Arabic in the pixels (owner decision WD-06); the site's own fonts are Latin-subset only and cannot be used to judge Arabic coverage.
